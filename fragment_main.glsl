#version 330

out vec4 outputColor;

uniform vec2 resolution;
uniform float elapsedTime;

vec2 iResolution = resolution;
float iTime = elapsedTime;

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
  // Normalized pixel coordinates (from 0 to 1)
  vec2 uv = fragCoord/iResolution.xy;

  // Time varying pixel color
  vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));

  // Output to screen
  fragColor = vec4(col,1.0);
}

out vec4 glFragColor;

void main()
{
  glFragColor.w = 1.;

  mainImage(glFragColor, gl_FragCoord.xy );
}
