
const mat3 m = mat3( 0.00,  0.80,  0.60,
                    -0.80,  0.36, -0.48,
                    -0.60, -0.48,  0.64 );

float tau = 3.14159265 * 2;

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
  vec2 p = (fragCoord.xy + renderOffset) / iResolution.xy;
  float r = iResolution.y / iResolution.x;
  vec2 uv = p*vec2(iResolution.x/iResolution.y,1.0 ) * tau * r;
  vec2 o_uv = uv + vec2(0, 0);
  vec3 latsurf = vec3(cos(o_uv.x), sin(o_uv.x), o_uv.y);

  float f = 0.0;

  float bm = 1.0;

  f += (0.5 /   1) * noise(latsurf *  1   * bm);
  f += (0.5 /   2) * noise(latsurf *  2   * bm);
  f += (0.5 /   4) * noise(latsurf *  4   * bm);
  f += (0.5 /   8) * noise(latsurf *  8   * bm);
  f += (0.5 /  16) * noise(latsurf * 16   * bm);
  f += (0.5 /  32) * noise(latsurf * 32   * bm);
  f += (0.5 /  64) * noise(latsurf * 64   * bm);
  f += (0.5 / 128) * noise(latsurf * 128  * bm);
  f += (0.5 / 256) * noise(latsurf * 256  * bm);

  //float leftlerp = min(uv.x * 3, 1);
  float leftlerp = smoothstep(0, 0.5, uv.x);
  //float rightlerp = min((uv.x - tau) * -3, 1);
  float rightlerp = 1 - smoothstep(tau - 0.5, tau, uv.x);
  //float bottomlerp = min(uv.y * 3, 1);
  float bottomlerp = smoothstep(0, 0.4, uv.y);
  //float toplerp = min((uv.y - tau * r) * -3, 1);
  float toplerp = 1 - smoothstep(tau * r - 0.4, tau * r, uv.y);

  float wateredge = f - 0.44;

  //f = mix(wateredge * 0.5, f, leftlerp);
  //f = mix(wateredge * 0.5, f, rightlerp);
  //f = mix(wateredge * 0.5, f, bottomlerp);
  //f = mix(wateredge * 0.5, f, toplerp);

  f = f * 1.2;
  f = 0.5 + 0.5*f;

  //f = mix(f - 0.15, f, leftlerp);
  //f = mix(f - 0.15, f, rightlerp);
  //f = mix(f - 0.15, f, bottomlerp);
  //f = mix(f - 0.15, f, toplerp);

  float g = f;
  float b = f;

  if(f <0.5)
    {
      f = min(0.495, f);
      g = 0.5 * f;
    }
  else
    {
      f = max(0.505, f);
      b = 0.0;
    }
  fragColor = vec4( f * float(isTexture), g, b, 1.0 );
}

out vec4 glFragColor;

void main()
{
  glFragColor.w = 1.;

  mainImage(glFragColor, gl_FragCoord.xy );
}
