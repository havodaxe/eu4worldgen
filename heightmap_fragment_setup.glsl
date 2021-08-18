#version 330

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
