#version 330

out vec4 outputColor;

uniform vec2 resolution;
uniform float elapsedTime;

void main()
{
  vec2 normCoords = gl_FragCoord.xy / resolution;
  float sineTime = sin(elapsedTime);
  // sin(x)^2 ranges between 0 and 1
  outputColor = vec4(normCoords, sineTime * sineTime, 1.0f);
}
