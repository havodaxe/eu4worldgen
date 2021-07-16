#!/usr/bin/env python3

# This file was derived from Sean McKiernan's gltut examples, hosted at:
# https://bitbucket.org/Mekire/gltut-python-pygame-pyopengl/src/master/
#
# The basis is 02_playing_with_colors/02_FragPosition.py
#
# Original code is under the MIT License, as is this file.
#
# The MIT License
# Copyright (C) 2010-2012 by Jason L. McKesson
# Copyright (C) 2013 by Sean McKiernan
# Copyright (C) 2021 by Havodaxe
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys,os
import pygame as pg
from OpenGL import GL
from time import time, strftime, localtime
from PIL import Image

BASE_SIZE = (11,4)
TEXBLOCK = (512,512)
DISPLAYBLOCK = (150,150)
DISPLAYRES = (BASE_SIZE[0] * DISPLAYBLOCK[0], BASE_SIZE[1] * DISPLAYBLOCK[1])
TEXRES = (BASE_SIZE[0] * TEXBLOCK[0], BASE_SIZE[1] * TEXBLOCK[1])

VERTICES = [ 1.0,  1.0,  0.0,  1.0,
             1.0, -1.0,  0.0,  1.0,
            -1.0, -1.0,  0.0,  1.0,
            -1.0, -1.0,  0.0,  1.0,
            -1.0,  1.0,  0.0,  1.0,
             1.0,  1.0,  0.0,  1.0 ]

SIZE_FLOAT = VERT_COMPONENTS = 4

SHADER2STRING = {GL.GL_VERTEX_SHADER   : "vertex",
                 GL.GL_FRAGMENT_SHADER : "fragment"}

#Load shaders from files.
with open("vertex_main.glsl",'r') as myfile:
    VERT = myfile.read()
with open("fragment_setup.glsl",'r') as myfile:
    FRAG_SETUP = myfile.read()
with open("fragment_noise.glsl",'r') as myfile:
    FRAG_NOISE = myfile.read()
with open("fragment_main.glsl",'r') as myfile:
    FRAG_MAIN = myfile.read()

FRAG = FRAG_SETUP + FRAG_NOISE + FRAG_MAIN

class GLtests:
    def __init__(self):
        self.shader = GL.glCreateProgram()
        self.vbo = None
        self.texture_fbo = None
        self.init_all()
        self.reshape(*DISPLAYRES)
    def init_all(self):
        self.attach_shaders()
        self.init_vertex_buf()
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)

        self.init_tex()
        self.init_tex_frame_buf()
    def init_vertex_buf(self):
        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        array_type = (GL.GLfloat*len(VERTICES))
        GL.glBufferData(GL.GL_ARRAY_BUFFER,len(VERTICES)*SIZE_FLOAT,
                        array_type(*VERTICES),GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,0)

    def init_tex(self):
        self.tex = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 1)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER,
                           GL.GL_NEAREST);
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER,
                           GL.GL_NEAREST);
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S,
                           GL.GL_CLAMP_TO_EDGE);
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T,
                           GL.GL_CLAMP_TO_EDGE);

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8, *TEXBLOCK,
                        0, GL.GL_RGBA, GL.GL_UNSIGNED_INT_8_8_8_8, 0);

    def init_tex_frame_buf(self):
        self.texture_fbo = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.texture_fbo)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0,
                                self.tex, 0)
        GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

    def attach_shaders(self):
        shade_list = []
        shade_list.append(self.compile(GL.GL_VERTEX_SHADER,VERT))
        shade_list.append(self.compile(GL.GL_FRAGMENT_SHADER,FRAG))
        for shade in shade_list:
            GL.glAttachShader(self.shader,shade)
        self.link()
        for shade in shade_list:
            GL.glDetachShader(self.shader,shade)
            GL.glDeleteShader(shade)
    def compile(self,shader_type,shader_str):
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader,shader_str)
        GL.glCompileShader(shader)
        status = GL.glGetShaderiv(shader,GL.GL_COMPILE_STATUS)
        if not status:
            log = GL.glGetShaderInfoLog(shader)
            shader_name = SHADER2STRING[shader_type]
            raise ShaderException("Compile failure in {} shader:\n{}\n".format(shader_name,log))
        return shader

    def link(self):
        GL.glLinkProgram(self.shader)
        status = GL.glGetProgramiv(self.shader,GL.GL_LINK_STATUS)
        if not status:
            log = GL.glGetProgramInfoLog(self.shader)
            raise ShaderException("Linking failure:\n{}\n".format(log))

    def display(self, elapsedTime, resolution, renderOffset, isTexture):
        GL.glClearColor(1,1,1,1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.shader)
        isTexUniformLoc = GL.glGetUniformLocation(self.shader, "isTexture")
        roUniformLoc = GL.glGetUniformLocation(self.shader, "renderOffset")
        resUniformLoc = GL.glGetUniformLocation(self.shader, "resolution")
        timeUniformLoc = GL.glGetUniformLocation(self.shader, "elapsedTime")
        GL.glUniform1f(isTexUniformLoc, isTexture)
        GL.glUniform2f(roUniformLoc, *renderOffset)
        GL.glUniform2f(resUniformLoc, *resolution)
        GL.glUniform1f(timeUniformLoc, elapsedTime)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0,VERT_COMPONENTS,GL.GL_FLOAT,False,0,None)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(VERTICES)//VERT_COMPONENTS)
        GL.glDisableVertexAttribArray(0)
        GL.glUseProgram(0)

    def reshape(self,width,height):
        GL.glViewport(0,0,width,height)

class ShaderException(Exception):
    pass

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode(DISPLAYRES,pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF)
    MyClock = pg.time.Clock()
    MyGL = GLtests()
    start_time = time()
    elapsedTime = 0
    while 1:
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                print(elapsedTime)
                pg.quit();sys.exit()
            elif event.type == pg.KEYDOWN:
                if(event.unicode == 'p'):
                    #loopdims = (4,2)
                    loopdims = BASE_SIZE
                    texsize = (loopdims[0] * TEXBLOCK[0],
                              loopdims[1] * TEXBLOCK[1])
                    print(texsize)
                    if(texsize[0] * texsize[1] > 8192 * 8192):
                        raise ValueError("Image too large to be rendered.")
                    tex_preflip = Image.new("L", texsize)
                    GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, MyGL.texture_fbo)
                    GL.glBindTexture(GL.GL_TEXTURE_2D, MyGL.tex)
                    for y in range(loopdims[1]):
                        for x in range(loopdims[0]):
                            texoffset = (TEXBLOCK[0] * x, TEXBLOCK[0] * y)
                            MyGL.display(elapsedTime, TEXRES, texoffset, True)
                            pixels = GL.glGetTexImage(GL.GL_TEXTURE_2D, 0,
                                                      GL.GL_RGBA,
                                                      GL.GL_UNSIGNED_BYTE)
                            im = Image.frombytes("L", TEXBLOCK, pixels[0::4])
                            texbox = (*texoffset,
                                      texoffset[0] + TEXBLOCK[0],
                                      texoffset[1] + TEXBLOCK[1])
                            tex_preflip.paste(im, texbox)
                    GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
                    timestamp = strftime("%Y%m%d-%H%M%S", localtime())
                    tex_file_name = "texture_output_{}.png".format(timestamp)
                    print(tex_file_name)
                    tex_out = tex_preflip.transpose(Image.FLIP_TOP_BOTTOM)
                    tex_out.save(tex_file_name)
                    print("Saved texture to {}".format(tex_file_name))
        elapsedTime = time() - start_time
        MyGL.display(elapsedTime, DISPLAYRES, (0,0), False)
        pg.display.flip()
        MyClock.tick(60)

if __name__ == '__main__':
    main()
