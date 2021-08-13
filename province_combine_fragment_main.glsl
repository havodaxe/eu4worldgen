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
uniform sampler2D terrain;

/* ----- main ----- */

out vec4 glFragColor;

vec2 coordNorm( in vec2 fragCoord )
{
  return vec2(fragCoord.xy / iResolution.xy);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
  vec4 land = texture( provinces, coordNorm(fragCoord) );
  vec4 tMid = texture( terrain,   coordNorm(fragCoord) );

  vec4 colorOut = land;

  if(tMid.r < 0.5)
    {
      colorOut = mix(colorOut, vec4(0.5, 0.5, 0.5, 1.0), 0.75);
      //colorOut = vec4(0.0, 0.0, 0.0, 1.0);
    }

  fragColor = colorOut;
  //fragColor = land;
}

void main()
{
  //glFragColor.w = 1.;

  mainImage(glFragColor, gl_FragCoord.xy );
}
