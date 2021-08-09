#version 330

/* ----- setup ----- */

out vec4 outputColor;

uniform bool isTexture;
uniform vec2 renderOffset;
uniform vec2 resolution;
uniform float elapsedTime;

vec2 iResolution = resolution;
float iTime = elapsedTime;

uniform sampler2D provinces;

/* ----- main ----- */

float sqrtOf2 = 1.4142135623730951;
// Square roots are expensive, let's keep it precalculated

out vec4 glFragColor;

vec2 coordNorm( in vec2 fragCoord )
{
  return vec2(fragCoord.xy / iResolution.xy);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
  float diagCost = sqrtOf2;
  // 2.8 is worth considering with how lumpy it makes things
  //diagCost = (sin(iTime) * sin(iTime) + 1) * sqrt2;
  vec2 normCoords = fragCoord.xy / iResolution.xy;
  vec2 nc = coordNorm( fragCoord );
  vec4 botleft  = texture( provinces, coordNorm(fragCoord + vec2(-1,-1)) );
  vec4 bottom   = texture( provinces, coordNorm(fragCoord + vec2( 0,-1)) );
  vec4 botright = texture( provinces, coordNorm(fragCoord + vec2( 1,-1)) );
  vec4 left     = texture( provinces, coordNorm(fragCoord + vec2(-1, 0)) );
  vec4 mid      = texture( provinces, coordNorm(fragCoord + vec2( 0, 0)) );
  vec4 right    = texture( provinces, coordNorm(fragCoord + vec2( 1, 0)) );
  vec4 topleft  = texture( provinces, coordNorm(fragCoord + vec2(-1, 1)) );
  vec4 top      = texture( provinces, coordNorm(fragCoord + vec2( 0, 1)) );
  vec4 topright = texture( provinces, coordNorm(fragCoord + vec2( 1, 1)) );

  // Distance to seed pixel is stored in the alpha channel
  vec4 lowest = vec4(0, 0, 0, 1);
  float dts = 255.0; // Distance to seed
  if(botleft.a < lowest.a)
    {
      lowest = botleft;
      dts = diagCost;
    }
  if(bottom.a < lowest.a)
    {
      lowest = bottom;
      dts = 1.0;
    }
  if(botright.a < lowest.a)
    {
      lowest = botright;
      dts = diagCost;
    }
  if(left.a < lowest.a)
    {
      lowest = left;
      dts = 1.0;
    }
  if(mid.a < lowest.a)
    {
      lowest = mid;
      dts = 0.0;
    }
  if(right.a < lowest.a)
    {
      lowest = right;
      dts = 1.0;
    }
  if(topleft.a < lowest.a)
    {
      lowest = topleft;
      dts = diagCost;
    }
  if(top.a < lowest.a)
    {
      lowest = top;
      dts = 1.0;
    }
  if(topright.a < lowest.a)
    {
      lowest = topright;
      dts = diagCost;
    }

  if(lowest.rgb == vec3(0.0, 0.0, 0.0))
    {
      lowest = vec4(0.0, 0.0, 0.0, 1.0);
      dts = 1.0;
    }

  fragColor = lowest + vec4(0, 0, 0, dts / 256);
  //fragColor = mid;
}

void main()
{
  //glFragColor.w = 1.;

  mainImage(glFragColor, gl_FragCoord.xy );
}
