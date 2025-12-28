#https://github.com/tsoding/formula
#https://youtu.be/qjWkNZ0SXfo?si=_9_TgZSU8SuA4JhB
import math
import time

WIDTH  = 128
HEIGHT = 64

# --- Cube vertices ---
vs = [
    ( 0.25,  0.25,  0.25),
    (-0.25,  0.25,  0.25),
    (-0.25, -0.25,  0.25),
    ( 0.25, -0.25,  0.25),

    ( 0.25,  0.25, -0.25),
    (-0.25,  0.25, -0.25),
    (-0.25, -0.25, -0.25),
    ( 0.25, -0.25, -0.25),
]

# --- Edges ---
fs = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]

# --- Math ---
def rotate_xz(p, a):
    x, y, z = p
    c = math.cos(a)
    s = math.sin(a)
    return (x*c - z*s, y, x*s + z*c)

def translate_z(p, dz):
    x, y, z = p
    return (x, y, z + dz)

def project(p):
    x, y, z = p
    return (x / z, y / z)

def screen(p, width=WIDTH, height=HEIGHT):
    x, y = p
    sx = int((x + 1) * 0.5 * width)
    sy = int((1 - (y + 1) * 0.5) * height)
    return (sx, sy)

# --- Renderer ---
def draw_cube(oled, angle, dz):
    for f in fs:
        for i in range(len(f)):
            a = vs[f[i]]
            b = vs[(f[(i + 1) % len(f)])]

            pa = screen(project(translate_z(rotate_xz(a, angle), dz)))
            pb = screen(project(translate_z(rotate_xz(b, angle), dz)))

            oled.line(pa[0], pa[1], pb[0], pb[1], 1)
