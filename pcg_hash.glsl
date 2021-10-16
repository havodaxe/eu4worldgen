/*
 * 3-dimensional Permuted Congruential Generator, "pcg3d".
 * pcg3d first described by Mark Jarzynski and Marc Olano.
 * Permuted congruential generator family first described by Melissa O'Neill.
 *
 * See the following two papers for details:
 *
 * Mark Jarzynski and Marc Olano, Hash Functions for GPU Rendering,
 * Journal of Computer Graphics Techniques (JCGT), vol. 9, no. 3, 21-38, 2020
 * Available online http://jcgt.org/published/0009/03/02/
 *
 * Melissa E. O'Neill, PCG: A Family of Simple Fast Space-Efficient
 * Statistically Good Algorithms for Random Number Generation, Harvey Mudd
 * College, HMC-CS-2014-0905.
 * Available online https://www.cs.hmc.edu/tr/hmc-cs-2014-0905.pdf
 */
uvec3 pcg3d(uvec3 p) {
  uvec3 state = p;

  state = state * 1664525u + 1013904223u;

  state.x += state.y * state.z;
  state.y += state.z * state.x;
  state.z += state.x * state.y;

  state ^= state >> 16u;

  state.x += state.y * state.z;
  state.y += state.z * state.x;
  state.z += state.x * state.y;

  return state;
}
