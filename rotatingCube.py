import pygame
from pygame.locals import *
import time

from tkinter import *
from threading import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
count = 0
frames = 0
fpslock = 90

cubes = []

a = 0.25

vertices = (
    (a, -a, -a),
    (a, a, -a),
    (-a, a, -a),
    (-a, -a, -a),
    (a, -a, a),
    (a, a, a),
    (-a, -a, a),
    (-a, a, a)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7),
    )

def Cube(posX = 0, posY = 0, posZ = 0):
    glBegin(GL_LINES)
    
    for edge in edges:
        for vertex in edge:
            glVertex3fv((vertices[vertex][0]+posX, vertices[vertex][1]+posY, vertices[vertex][2]+posZ))  
    glEnd()

def drawCubes():
    global cubes
    for x in range(len(cubes)):
        Cube(cubes[x][0]*2*a, cubes[x][1]*2*a, cubes[x][2]*2*a)

def addCube(posX, posY, posZ):
    global cubes
    cubes.append([posX, posY, posZ])

def main():
    global frames, count, fpslock, full_rotation_time
    pygame.init()
    display = (800, 600)
    display_surface = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('A 3D Project')

    gluPerspective(80, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    glRotatef(0, 0, 0, 0)

    font = pygame.font.Font('freesansbold.ttf', 32)
    t3 = 1
    t4 = time.time()

    full_rotation_time = 5

    while True:
        try:
            t1 = time.time()
            if t1 - t4 >= 1:
                try:
                    updatefps(int(1/(frames/count)))
                    t4 = time.time()
                    frames = 0
                    count = 0
                except:
                    quit()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            speedconstant = 1
            
            calctime = t3
            
            glRotatef((360*t3)/full_rotation_time, 0, 1, 0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            drawCubes()
            
            pygame.display.flip()
            pygame.time.wait(int((1/fpslock)*1000))
            
            t2 = time.time()
            t3 = t2 - t1
            frames += t3
            count += 1
        except:
            quit()
        

def rotsetcmd():
    global full_rotation_time
    try:
        full_rotation_time = int(rotent.get())
    except:
        full_rotation_time = 60

def updatefps(fps):
    fpslbl.config(text = "fps: " + str(fps))

addCube(0, 0, 0)

def change_a(b1, b2, *k):
    global a, vertices, scrlbar
    a = float(b2)*2
    if a < 0:
        b2 = 0.05
        a = float(b2)*2
        scrlbar.set(a, a)
    vertices = (
        (a, -a, -a),
        (a, a, -a),
        (-a, a, -a),
        (-a, -a, -a),
        (a, -a, a),
        (a, a, a),
        (-a, -a, a),
        (-a, a, a)
        )
    scrlbar.set(b2, b2)
    scrlbl.config(text = str(a))

gui = Tk()
gui.geometry("250x150")
gui.resizable(height = False, width = False)

rottimebtn = Button(text = "Rot Time", command = rotsetcmd)
rottimebtn.place(x = 5, y = 5)

rotent = Entry(width = 8)
rotent.place(x = 65, y = 9)

fpslbl = Label(text = "fps: ")
fpslbl.place(x = 5, y = 32)

cnv = Canvas(gui, width = 95, height = 10, bg = "#000000")
cnv.place(x = 5, y = 59)
cnv.pack_propagate(False)
scrlbar = Scrollbar(cnv, orient = 'horizontal', command = change_a)
scrlbar.pack(fill = "x", expand = True)
cnv.update()

scrlbl = Label(text = str(a))
scrlbl.place(x = 105, y =59)

Thread(target = main, daemon = True).start()

gui.mainloop()
