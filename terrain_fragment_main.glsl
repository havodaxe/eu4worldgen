#version 330

/* ----- setup ----- */

out vec4 outputColor;

uniform bool isTexture;
uniform vec2 renderOffset;
uniform vec2 resolution;
uniform float elapsedTime;
uniform bool dividesLand;

vec2 iResolution = resolution;
float iTime = elapsedTime;

uniform sampler2D selfProvinces;
uniform sampler2D landProvinces;
uniform sampler2D waterProvinces;
uniform sampler2D heightmap;

/* ----- main ----- */

out vec4 glFragColor;

vec2 coordNorm( in vec2 fragCoord )
{
  return vec2(fragCoord.xy / iResolution.xy);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
  vec4 tMid = texture( heightmap, coordNorm(fragCoord) );
  if(tMid.r < 0.5)
    {
      fragColor = vec4(vec3(8.0, 31.0, 130.0) / 255.0, 1.0);
    }
  else
    {
      fragColor = vec4(vec3(86.0, 124.0, 27.0) / 255.0, 1.0);
    }
}

void main()
{
  //glFragColor.w = 1.;

  mainImage(glFragColor, gl_FragCoord.xy );
}
