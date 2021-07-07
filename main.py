import sys,os
import pygame as pg
from OpenGL import GL
from time import time, strftime, localtime
from PIL import Image

RESOLUTION = (1024,1024)
TEXBLOCK = (512,512)

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
with open("fragment_main.glsl",'r') as myfile:
    FRAG = myfile.read()

class GLtests:
    def __init__(self):
        self.shader = GL.glCreateProgram()
        self.vbo = None
        self.texture_fbo = None
        self.init_all()
        self.reshape(*RESOLUTION)
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

    def display(self):
        GL.glClearColor(1,1,1,1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.shader)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0,VERT_COMPONENTS,GL.GL_FLOAT,False,0,None)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(VERTICES)//VERT_COMPONENTS)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.texture_fbo)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(VERTICES)//VERT_COMPONENTS)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glDisableVertexAttribArray(0)
        #GL.glUseProgram(0)

    def reshape(self,width,height):
        GL.glViewport(0,0,width,height)

class ShaderException(Exception):
    pass

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode(RESOLUTION,pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF)
    MyClock = pg.time.Clock()
    MyGL = GLtests()
    start_time = time()
    while 1:
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                print(time() - start_time)
                pg.quit();sys.exit()
            elif event.type == pg.KEYDOWN:
                if(event.unicode == 'p'):
                    #print(event)
                    timestamp = strftime("%Y%m%d-%H%M%S", localtime())
                    tex_file_name = "texture_output_{}.png".format(timestamp)
                    print(tex_file_name)
                    GL.glBindTexture(GL.GL_TEXTURE_2D, MyGL.tex)
                    pixels = GL.glGetTexImage(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA,
                                              GL.GL_UNSIGNED_BYTE)
                    im = Image.frombytes("RGBA", TEXBLOCK, pixels)
                    im.save(tex_file_name)
                    print("Saved texture to {}".format(tex_file_name))
        MyGL.display()
        resUniformLoc = GL.glGetUniformLocation(MyGL.shader, "resolution")
        timeUniformLoc = GL.glGetUniformLocation(MyGL.shader, "elapsedTime")
        GL.glUniform2f(resUniformLoc, *SCREEN.get_size())
        GL.glUniform1f(timeUniformLoc, time() - start_time)
        GL.glUseProgram(0)
        pg.display.flip()
        MyClock.tick(60)

if __name__ == '__main__':
    main()
