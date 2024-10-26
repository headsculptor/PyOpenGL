import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#Options
lighting = True
smooth_models = True
height = 3
width = 8
length = 8

scale = 1

pygame.init()

blocks = []
surface_blocks = []

vertices = (
    (scale, -scale, -scale),
    (scale, scale, -scale),
    (-scale, scale, -scale),
    (-scale, -scale, -scale),
    (scale, -scale, scale),
    (scale, scale, scale),
    (-scale, -scale, scale),
    (-scale, scale, scale)
    )

def drawFace(vertex1, vertex2, vertex3, vertex4, rgbcolour):
    glBegin(GL_QUADS)
    glColor3fv(rgbcolour)
    glVertex3fv(vertex1)
    glVertex3fv(vertex2)
    glVertex3fv(vertex3)
    glVertex3fv(vertex4)
    glEnd()

def drawCube(x, y, z, xpf, xnf, ypf, ynf, zpf, znf):
    global scale
    v0 = (vertices[0][0] + x*scale*2, vertices[0][1] + y*scale*2, vertices[0][2] + z*scale*2)
    v1 = (vertices[1][0] + x*scale*2, vertices[1][1] + y*scale*2, vertices[1][2] + z*scale*2)
    v2 = (vertices[2][0] + x*scale*2, vertices[2][1] + y*scale*2, vertices[2][2] + z*scale*2)
    v3 = (vertices[3][0] + x*scale*2, vertices[3][1] + y*scale*2, vertices[3][2] + z*scale*2)
    v4 = (vertices[4][0] + x*scale*2, vertices[4][1] + y*scale*2, vertices[4][2] + z*scale*2)
    v5 = (vertices[5][0] + x*scale*2, vertices[5][1] + y*scale*2, vertices[5][2] + z*scale*2)
    v6 = (vertices[6][0] + x*scale*2, vertices[6][1] + y*scale*2, vertices[6][2] + z*scale*2)
    v7 = (vertices[7][0] + x*scale*2, vertices[7][1] + y*scale*2, vertices[7][2] + z*scale*2)
    xpf, xnf, ypf, ynf, zpf, znf = not xpf, not xnf, not ypf, not ynf, not zpf, not znf

    colour_scheme = (
        (1, 1, 1),
        (0.9, 1, 1),
        (1, 0.95, 0.9),
        (0.9, 0.9, 0.9),
        (0.95, 1, 0.95),
        (1, 1, 0.9)
        )

    if xpf:
        drawFace(v1, v0, v4, v5, colour_scheme[0])
    if xnf:
        drawFace(v2, v3, v6, v7, colour_scheme[1])
    if ypf:
        drawFace(v7, v2, v1, v5, colour_scheme[2])
    if ynf:
        drawFace(v3, v0, v4, v6, colour_scheme[3])
    if zpf:
        drawFace(v6, v4, v5, v7, colour_scheme[4])
    if znf:
        drawFace(v0, v1, v2, v3, colour_scheme[5])

def update():
    glColor4f(0.8, 0.8, 0.8, 1)
    glBegin(GL_QUADS)
    glVertex3f(-10, -10, -2)
    glVertex3f(10, -10, -2)
    glVertex3f(10, 10, -2)
    glVertex3f(-10, 10, -2)
    glEnd()
    

def main():
    global paused, run, up_down_angle, mousMove
    display = (600, 500)
    pydisplay = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    if lighting:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
    if smooth_models:
        glShadeModel(GL_SMOOTH)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    sphere = gluNewQuadric()
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    displayCenter = [pydisplay.get_size()[i] // 2 for i in range(2)]
    mouseMove = [0, 0]
    pygame.mouse.set_pos(displayCenter)
    
    up_down_angle = 0.0
    paused = False
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    paused = not paused
                    pygame.mouse.set_pos(displayCenter) 
            if not paused: 
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                pygame.mouse.set_pos(displayCenter)    

        if not paused:
            # get keys
            keypress = pygame.key.get_pressed()
            #mouseMove = pygame.mouse.get_rel()
        
            # init model view matrix
            glLoadIdentity()

            # apply the look up and down
            up_down_angle += mouseMove[1]*0.1
            glRotatef(up_down_angle, 1.0, 0.0, 0.0)

            # init the view matrix
            glPushMatrix()
            glLoadIdentity()

            # apply the movment 
            if keypress[pygame.K_w]:
                glTranslatef(0,0,0.1)
            if keypress[pygame.K_s]:
                glTranslatef(0,0,-0.1)
            if keypress[pygame.K_d]:
                glTranslatef(-0.1,0,0)
            if keypress[pygame.K_a]:
                glTranslatef(0.1,0,0)

            # apply the left and right rotation
            glRotatef(mouseMove[0]*0.1, 0.0, 1.0, 0.0)

            # multiply the current matrix by the get the new view matrix and store the final vie matrix 
            glMultMatrixf(viewMatrix)
            viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            # apply view matrix
            glPopMatrix()
            glMultMatrixf(viewMatrix)

            if lighting:
                glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glPushMatrix()

            update()

            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(10)

def displayBlocks():
    for block in range(len(surface_blocks)):
        block_info = surface_blocks[block]
        x = block_info[0]
        y = block_info[1]
        z = block_info[2]
        xpf = block_info[3]
        xnf = block_info[4]
        ypf = block_info[5]
        ynf = block_info[6]
        zpf = block_info[7]
        znf = block_info[8]
        drawCube(x, y, z, xpf, xnf, ypf, ynf, zpf, znf)

for y in range(height):
    for x in range(width):
        for z in range(length):
            blocks.append([x, y, z])
try:
    for x in range(width-2):
        for z in range(length-2):
            blocks.append([x+1, height, z+1])
except: pass

for block in range(len(blocks)):
    offset = scale
    x = blocks[block][0]
    y = blocks[block][1]
    z = blocks[block][2]
    xpf, xnf, ypf, ynf, zpf, znf = False, False, False, False, False, False
    if [x + offset, y, z] in blocks:
        xpf = True
    if [x - offset, y, z] in blocks:
        xnf = True
    if [x, y + offset, z] in blocks:
        ypf = True
    if [x, y - offset, z] in blocks:
        ynf = True
    if [x, y, z + offset] in blocks:
        zpf = True
    if [x, y, z - offset] in blocks:
        znf = True
    if not xpf or not xnf or not ypf or not ynf or not zpf or not znf:
        surface_blocks.append([x, y, z, xpf, xnf, ypf, ynf, zpf, znf])

main()

pygame.quit()
