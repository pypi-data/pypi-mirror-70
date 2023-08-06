#include "consts.h"
#include "rand.h"
#include "geom.h"
#include "ref.h"

#define ITMAX 100
#define EPS 3e-9


float brent_intersect(float16* neutron, char coord, float dt, float d, 
                      float omega, float ph0) {
    /* Takes neutron ray as argument and returns time of flight
       for coordinate = d in time interval [0, dt] primed frame */

    float3 pos_i = (*neutron).s012;
    // TODO: create wrapper on frame_rotate to implement curved mirrors
    float tof_i = 0;
    float3 pos_i_prime = frame_rotate(pos_i, (float3){0, omega*tof_i + ph0, 0});
    float3 vel = (*neutron).s345;

    float3 pos_f = pos_i + vel*dt;
    float tof_f = tof_i + dt;
    float3 pos_f_prime = frame_rotate(pos_f, (float3){0, omega*tof_f + ph0, 0});

    float coord_i_prime, coord_f_prime;

    if (coord == 'x') {
        coord_i_prime = pos_i_prime.s0 - d;
        coord_f_prime = pos_f_prime.s0 - d;
    } else if (coord == 'z') {
        coord_i_prime = pos_i_prime.s2 - d;
        coord_f_prime = pos_f_prime.s2 - d;
    } else {
        return -1;
    }
    
    float a = tof_i, b = tof_f, c = tof_f, dd, e, min1, min2;
    float fa = coord_i_prime, fb = coord_f_prime, fc, tof_test, coord_test_prime;
    float3 pos_test_prime;
    float tol = 1e-9;

    //printf("f(%e) = %e, f(%e) = %e\n", a, fa, b, fb);

    if (fb*fa > 0.0f) {
        // Root is not bracketed
        return -3;
    }

    fc = fb;
    for (int iter = 1; iter <= ITMAX; iter++) {
        c = (a + b) / 2.0f;

        tof_test = tof_i + c;
        pos_test_prime = frame_rotate(pos_i + vel*c, (float3){0, omega*tof_test + ph0, 0});

        if (coord == 'x') {
            coord_test_prime = pos_test_prime.s0 - d;
        } else if (coord == 'z') {
            coord_test_prime = pos_test_prime.s2 - d;
        } else {
            return -1;
        }

        fc = coord_test_prime;

        if (fc == 0.0f || ((b - a)/2.0f) < tol) {
          return c;
        }

        if(fc*fa > 0.0f) {
          a = c;
          fa = fc;
        } else {
          b = c;
          fb = fc;
        }

        fb = coord_f_prime;
    }

    return -2;
}

__kernel void fermichop(__global float16* neutrons,
    __global float8* intersections, __global uint* iidx,
    float const radius, uint const nslit, float const len,
    float const width, float const phase, float const nu, float const eff,
    float const curvature, float const m, float const alpha,
    float const Qc, float const W, float const R0, uint const comp_idx) {

  uint global_addr        = get_global_id(0);
  float16 neutron         = neutrons[global_addr];
  float8 intersection = intersections[global_addr];
  uint this_iidx          = iidx[global_addr];

  /* Check we are scattering from the intersected component */
  if (!(this_iidx == comp_idx)) {
      return;
  }

  /* Check termination flag */
  if (neutron.sf > 0.f)  {
      return;
  }

  /* Perform scattering here */

  // Propagate to first intersection
  neutron.s012 = intersection.s012;
  neutron.sa += intersection.s3;

  float xp1, zp1, xp2, zp2, vxp1, vxp2, xp3, vzp1, slit_input;
  float q, t1, t2, t3, dt;
  int n1, n2, n3;
  uint iter = 0;
  float omega = 2*M_PI*nu;

  float3 pos_rot, vel_rot, frame_vel;

  pos_rot = frame_rotate(neutron.s012, (float3){0, omega*neutron.sa + phase, 0});

  dt = intersection.s7 - intersection.s3;
  vxp1 = length(neutron.s345);
  xp1 = pos_rot.s0;
  printf("%e %e %e\n", neutron.s0, xp1, nslit*width/2.0f);

  if (fabs(xp1) >= nslit*width/2.0f) {
    neutron.sf = 1.0f;
    return;
  }

  zp1 = pos_rot.s2;
  slit_input = (zp1 > 0 ? len/2.0f : -1.0f*len / 2.0f);

  t3 = brent_intersect(&neutron, 'z', dt, slit_input, omega, phase);

  if ( (t3 < 0.0f) || (t3 > dt)) {
    neutron.sf = 1.0f;
    return;
  }

  neutron.s012 += neutron.s345*t3;
  neutron.sa += t3;
  
  dt -= t3;
  pos_rot = frame_rotate(neutron.s012, (float3){0, omega*neutron.sa + phase, 0});
  xp1 = pos_rot.s0;
  zp1 = pos_rot.s2;

  t3 = brent_intersect(&neutron, 'z', dt, -slit_input, omega, phase);

  //TODO: chopper accuracy here
  if ( (t3 < EPS) || (t3 > dt)) {
    neutron.sf = 1.0f;
    return;
  } else {
    dt = t3;
  }

  n1 = floor(xp1 / width);

  // printf("%d %e\n", n1, xp1);

  for (iter = 0; iter < ITMAX; iter++) {
    float dt_to_tangent = 0.0f;

    pos_rot = frame_rotate(neutron.s012, (float3){0, omega*neutron.sa + phase, 0});
    float3 vp = neutron.s345;
    vp.s0 += neutron.s2*omega;
    vp.s2 -= neutron.s0*omega;
    vel_rot = frame_rotate(vp, (float3){0, omega*neutron.sa + phase, 0});
    xp1 = pos_rot.s0;
    vxp1 = vel_rot.s0;

    pos_rot = frame_rotate(neutron.s012+neutron.s345*dt, (float3){0, omega*(neutron.sa+dt) + phase, 0});
    vp = neutron.s345;
    vp.s0 += (neutron.s2 + neutron.s5*dt)*omega;
    vp.s2 -= (neutron.s0 + neutron.s3*dt)*omega;
    vel_rot = frame_rotate(vp, (float3){0, omega*(neutron.sa+dt) + phase, 0});
    xp2 = pos_rot.s0;
    vxp2 = vel_rot.s0;

    n2 = floor(xp2 / width);

    dt_to_tangent = (vxp1 - vxp2 ? ((xp2 - xp1) + (neutron.sa*vxp1 - (neutron.sa+dt)*vxp2))/(vxp1 - vxp2) - neutron.sa : -1);
    
    if((dt_to_tangent < 0)||(dt_to_tangent > dt)) {
      dt_to_tangent = dt * 0.5;
    }

    pos_rot = frame_rotate(neutron.s012+neutron.s345*dt_to_tangent, (float3){0, omega*(neutron.sa+dt_to_tangent) + phase, 0});
    xp3 = pos_rot.s0;

    n3 = floor(xp3 / width);

    if ( (n2!=n1) || (n3!=n1)) {
      double t3a, t3b, distance_Wa, distance_Wb;
      //if (m == 0 || R0 == 0) {
      //  neutron.sf = 1.0f;
      //  return;
      //}

      if (n3 != n1) {
        n2 = n3;
      }

      if (n2 > n1) {
        distance_Wa = n1*width+width;
        distance_Wb = n1*width;
      } else {
        distance_Wb = n1*width+width;
        distance_Wa = n1*width;
      }

      t3a = brent_intersect(&neutron, 'x', dt_to_tangent, distance_Wa, omega, phase);
      t3b = brent_intersect(&neutron, 'x', dt_to_tangent, distance_Wb, omega, phase);

      if (t3b < 0) {
        t3 = t3a;
      } else if (t3a < 0.0f && t3b >= 0.0f) {
        t3 = t3b;
      } else {
        t3 = (t3a < t3b) ? t3a : t3b;
      }

      // TODO: chopper acc
      if ((t3 < EPS) || (t3 >= dt_to_tangent)) {
        dt_to_tangent = dt;
        t3a = brent_intersect(&neutron, 'x', dt_to_tangent, distance_Wa, omega, phase);
        t3b = brent_intersect(&neutron, 'x', dt_to_tangent, distance_Wb, omega, phase);

        if (t3b < 0) {
          t3 = t3a;
        } else if (t3a < 0.0f && t3b >= 0.0f) {
          t3 = t3b;
        } else {
          t3 = (t3a < t3b) ? t3a : t3b;
        }
      }

      if ((t3 < EPS) || (t3 >= dt_to_tangent)) {
        neutron.sf = 1.0f;
        return;
      }

      neutron.s012 += neutron.s345*t3;
      neutron.sa += t3;

      dt -= t3;

      pos_rot = frame_rotate(neutron.s012, (float3){0, omega*neutron.sa + phase, 0});  
      vel_rot = frame_rotate(neutron.s345, (float3){0, omega*neutron.sa + phase, 0});
      zp1 = pos_rot.s2;
      vxp1 = vel_rot.s0;
      vzp1 = vel_rot.s2;

      if (fabs(zp1) > len/2.0f) {
        break;
      }

      q = 2 * V2Q*(fabs(vxp1));

      float ref = reflectivity_func(q, R0, Qc, alpha, m, W);
      if (ref > 0)  {
        neutron.s9 *= ref;
      }
      else {
        neutron.sf = 1.0f;
        return;
      }

      vxp1 *= -1.0f;

      neutron.s345 = frame_derotate((float3){vxp1, neutron.s4, vzp1}, (float3){0, omega*neutron.sa + phase, 0});
      t3 = brent_intersect(&neutron, 'z', dt, -1.0f*slit_input, omega, phase);

      if ( (t3 < 0) || (t3 > dt) ) {
        neutron.sf = 1.0f;
        return;
      } else {
        dt = t3;
      }
    } else {
      // printf("Transmitting neutron with energy %e meV\n", VS2E*pow(length(neutron.s345), 2));
      break;
    }
  }

  /* ----------------------- */

  /* Update global memory and reset intersection */
  iidx[global_addr] = 0;
  neutron.sc = comp_idx;

  neutrons[global_addr]      = neutron;
  intersections[global_addr] = (float8)( 0.0f, 0.0f, 0.0f, 100000.0f,
                                       0.0f, 0.0f, 0.0f, 100000.0f );

}