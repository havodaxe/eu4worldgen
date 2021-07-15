#version 330

out vec4 outputColor;

uniform vec2 renderOffset;
uniform vec2 resolution;
uniform float elapsedTime;

vec2 iResolution = resolution;
float iTime = elapsedTime;
