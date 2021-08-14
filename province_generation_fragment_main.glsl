#version 330

/* ----- setup ----- */

out vec4 outputColor;

uniform bool isTexture;
uniform vec2 renderOffset;
uniform vec2 resolution;
uniform float elapsedTime;

vec2 iResolution = resolution;
float iTime = elapsedTime;

uniform sampler2D selfProvinces;
uniform sampler2D terrain;

/* ----- main ----- */

float sqrtOf2 = 1.4142135623730951;
// Square roots are expensive, let's keep it precalculated

out vec4 glFragColor;

vec2 coordNorm( in vec2 fragCoord )
{
  return vec2(fragCoord.xy / iResolution.xy);
}

void costCalc( out vec4 lowest, out float dts,
	       in vec4 pNeighbor, in vec4 pMid,
	       in vec4 tNeighbor, in vec4 tMid, in float len )
{
  lowest = pNeighbor;
  dts = len;
  dts = len * (1 + abs(tNeighbor.r * 255 - tMid.r * 255) * 10);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
  float diagCost = sqrtOf2;
  // 2.8 is worth considering with how lumpy it makes things
  //diagCost = (sin(iTime) * sin(iTime) + 1) * sqrt2;
  vec4 pBotleft  = texture( selfProvinces, coordNorm(fragCoord + vec2(-1,-1)) );
  vec4 pBottom   = texture( selfProvinces, coordNorm(fragCoord + vec2( 0,-1)) );
  vec4 pBotright = texture( selfProvinces, coordNorm(fragCoord + vec2( 1,-1)) );
  vec4 pLeft     = texture( selfProvinces, coordNorm(fragCoord + vec2(-1, 0)) );
  vec4 pMid      = texture( selfProvinces, coordNorm(fragCoord + vec2( 0, 0)) );
  vec4 pRight    = texture( selfProvinces, coordNorm(fragCoord + vec2( 1, 0)) );
  vec4 pTopleft  = texture( selfProvinces, coordNorm(fragCoord + vec2(-1, 1)) );
  vec4 pTop      = texture( selfProvinces, coordNorm(fragCoord + vec2( 0, 1)) );
  vec4 pTopright = texture( selfProvinces, coordNorm(fragCoord + vec2( 1, 1)) );
  // terrain samples
  vec4 tBotleft  = texture( terrain, coordNorm(fragCoord + vec2(-1,-1)) );
  vec4 tBottom   = texture( terrain, coordNorm(fragCoord + vec2( 0,-1)) );
  vec4 tBotright = texture( terrain, coordNorm(fragCoord + vec2( 1,-1)) );
  vec4 tLeft     = texture( terrain, coordNorm(fragCoord + vec2(-1, 0)) );
  vec4 tMid      = texture( terrain, coordNorm(fragCoord + vec2( 0, 0)) );
  vec4 tRight    = texture( terrain, coordNorm(fragCoord + vec2( 1, 0)) );
  vec4 tTopleft  = texture( terrain, coordNorm(fragCoord + vec2(-1, 1)) );
  vec4 tTop      = texture( terrain, coordNorm(fragCoord + vec2( 0, 1)) );
  vec4 tTopright = texture( terrain, coordNorm(fragCoord + vec2( 1, 1)) );

  // Distance to seed pixel is stored in the alpha channel
  vec4 lowest = vec4(0, 0, 0, 1);
  float dts = 510; // Distance to seed
  if(pBotleft.a < lowest.a)
    {
      costCalc(lowest, dts, pBotleft, pMid, tBotleft, tMid, diagCost);
    }
  if(pBottom.a < lowest.a)
    {
      costCalc(lowest, dts, pBottom, pMid, tBottom, tMid, 1.0);
    }
  if(pBotright.a < lowest.a)
    {
      costCalc(lowest, dts, pBotright, pMid, tBotright, tMid, diagCost);
    }
  if(pLeft.a < lowest.a)
    {
      costCalc(lowest, dts, pLeft, pMid, tLeft, tMid, 1.0);
    }
  if(pMid.a < lowest.a)
    {
      lowest = pMid;
      dts = 0.0;
      // No need to compare here. No distance to self.
    }
  if(pRight.a < lowest.a)
    {
      costCalc(lowest, dts, pRight, pMid, tRight, tMid, 1.0);
    }
  if(pTopleft.a < lowest.a)
    {
      costCalc(lowest, dts, pTopleft, pMid, tTopleft, tMid, diagCost);
    }
  if(pTop.a < lowest.a)
    {
      costCalc(lowest, dts, pTop, pMid, tTop, tMid, 1.0);
    }
  if(pTopright.a < lowest.a)
    {
      costCalc(lowest, dts, pTopright, pMid, tTopright, tMid, diagCost);
    }

  if(lowest.rgb == vec3(0.0, 0.0, 0.0))
    {
      lowest = vec4(0.0, 0.0, 0.0, 1.0);
      dts = 1.0;
    }

  fragColor = lowest + vec4(0, 0, 0, dts / 512);
  //fragColor = tMid;
}

void diffviz( out vec4 fragColor, in vec2 fragCoord )
{
  vec4 mid      = texture( terrain, coordNorm(fragCoord + vec2( 0, 0)) );
  vec4 botleft  = texture( terrain, coordNorm(fragCoord + vec2(-1, 0)) );
  float f = abs(mid.r * 255 - botleft.r * 255) / 2.6;
  fragColor = vec4(f,f,f,1);
  //fragColor = mid;
}

void main()
{
  //glFragColor.w = 1.;

  mainImage(glFragColor, gl_FragCoord.xy );
  //diffviz(glFragColor, gl_FragCoord.xy );
}
