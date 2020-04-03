import math
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *

from funkcije import Euler2A
from funkcije import AxisAngle
from funkcije import AxisAngle2Q
from funkcije import Q2AxisAngle
from funkcije import slerp

class Globalne:
    def __init__(self):
        self.animation_ongoing = False
        self.t = 0
        self.tm = 40
        self.q1 = []
        self.q2 = []

        self.x1 = -6
        self.y1 = 2.5
        self.z1 = -2
        self.fi1 = math.pi/7
        self.teta1 = math.pi/2
        self.psi1 = math.pi

        self.fi2 = math.pi/4
        self.teta2 = math.pi/8
        self.psi2 = 3*math.pi/2
        self.x2 = 6
        self.y2 = 3
        self.z2 = -5

g = Globalne()


def on_display():
    global g

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # podesava se tacka pogleda
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(4, 15, 6,
              0, 0, 0,
              0, 2, 0)

    # objekti zadrzavaju boju
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Iscrtava se koordinatni sistem
    coordSystem(15)

    # Iscrtavaju se pocetni i krajnji objekat
    objekti(g.x1, g.y1, g.z1, g.fi1, g.teta1, g.psi1, 106, 13, 173)
    objekti(g.x2, g.y2, g.z2, g.fi2, g.teta2, g.psi2, 106, 13, 173)

    # pomeranje objekta
    active(106, 10, 173)

    glutSwapBuffers()

def coordSystem(d):
    glBegin(GL_LINES)

    # plava x koordinata
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(d, 0, 0)

    # zelena y koordinata
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex(0, d, 0)

    # crvena z koordinata
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, d)

    glEnd()


def objekti(x, y, z, fi, teta, psi, r, g, b):
    glPushMatrix()

    glColor3f(r, g, b)
    glTranslatef(x, y, z)

    A = Euler2A(fi, teta, psi)
    p, alpha = AxisAngle(A)

    # ugao u stepene
    ugao = alpha / math.pi * 180
    glRotatef(ugao, p[0], p[1], p[2])

    glutWireCone(1, 1.3, 4, 1)
    coordSystem(5)

    glPopMatrix()


def active(r, gr, b):
    global g

    glPushMatrix()
    glColor3f(r, gr, b)

    x = (1 - g.t / g.tm) * g.x1 + (g.t / g.tm) * g.x2
    y = (1 - g.t / g.tm) * g.y1 + (g.t / g.tm) * g.y2
    z = (1 - g.t / g.tm) * g.z1 + (g.t / g.tm) * g.z2

    glTranslatef(x, y, z)

    q = slerp(g.q1, g.q2, g.tm, g.t)
    p, fi = Q2AxisAngle(q)

    ugao = fi / math.pi * 180
    glRotatef(ugao, p[0], p[1], p[2])

    glutWireCone(1, 1.3, 4, 1)
    coordSystem(5)

    glPopMatrix()


def on_keyboard(key, x, y):
    global g

    # Get the ASCII number of a character
    # number = ord(char)

    if ord(key) == 27:   # Esc
        sys.exit(0)
    elif ord(key) == ord('g') or ord(key) == ord('G'):
        if not g.animation_ongoing:
            glutTimerFunc(100, on_timer, 0)
            g.animation_ongoing = True
    elif ord(key) == ord('s') or ord(key) == ord('S'):
        g.animation_ongoing = False


def on_reshape(width, height):

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(width) / height, 1, 40)


def on_timer(value):
    global g

    if value != 0:
        return

    g.t += 1
    if g.t > g.tm:
        g.t = 0
        g.animation_ongoing = False
        return

    glutPostRedisplay()

    if g.animation_ongoing:
        glutTimerFunc(100, on_timer, 0)


def main():
    global g

    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("SLerp")

    glutKeyboardFunc(on_keyboard)
    glutReshapeFunc(on_reshape)
    glutDisplayFunc(on_display)

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)

    # kvaternion q1
    A = Euler2A(g.fi1, g.teta1, g.psi1)
    p, alpha = AxisAngle(A)
    g.q1 = AxisAngle2Q(p, alpha)

    # kvaternion q2
    A = Euler2A(g.fi2, g.teta2, g.psi2)
    p, alpha = AxisAngle(A)
    g.q2 = AxisAngle2Q(p, alpha)

    glutMainLoop()


if __name__ == '__main__':
    main()