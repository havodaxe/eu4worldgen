
const mat3 m = mat3( 0.00,  0.80,  0.60,
                    -0.80,  0.36, -0.48,
                    -0.60, -0.48,  0.64 );

float tau = 3.14159265 * 2;

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
  vec2 p = fragCoord.xy / iResolution.xy;
  vec2 uv = p*vec2(iResolution.x/iResolution.y,1.0 ) * tau * 4/11 + vec2(0);

  vec3 coat = vec3(cos(uv.x), sin(uv.x), uv.y);

  float f = 0.0;

  float b1m = 2.0;

  f += (0.5 / 1)  * noise(coat * 0.5 * b1m);
  f += (0.5 / 2)  * noise(coat * 1 * b1m);
  f += (0.5 / 4)  * noise(coat * 2 * b1m);
  f += (0.5 / 8)  * noise(coat * 4 * b1m);
  f += (0.5 / 16) * noise(coat * 8 * b1m);
  f += (0.5 / 32) * noise(coat * 16 * b1m);
  f += (0.5 / 64) * noise(coat * 32 * b1m);
  f += (0.5 / 128) * noise(coat * 64 * b1m);

  f = f * 1.2;
  f = 0.5 + 0.5*f;

  float g = f;
  float b = f;

  if(f <0.50)
    {
      g = 0.5 * f;
    }
  else
    {
      b = 0.0;
    }

  fragColor = vec4( 0.0, g, b, 1.0 );
}

out vec4 glFragColor;

void main()
{
  glFragColor.w = 1.;

  mainImage(glFragColor, gl_FragCoord.xy );
}
