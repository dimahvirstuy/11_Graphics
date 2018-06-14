import mdl
from display import *
from matrix import *
from draw import *
import math

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    s = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    polygons = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    for i in p[0]:
        print i
        if i[0] == 'sphere':
            add_sphere(polygons,float(i[1]), float(i[2]), float(i[3]),float(i[4]), step_3d)
            matrix_mult( s[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []

        elif i[0] == 'torus':
            add_torus(polygons,float(i[1]), float(i[2]), float(i[3]),float(i[4]), float(i[5]), step_3d)
            matrix_mult( s[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif i[0] == 'box':
            add_box(polygons,float(i[1]), float(i[2]), float(i[3]),float(i[4]), float(i[5]), float(i[6]))
            matrix_mult( s[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif i[0] == 'circle':
            add_circle(edges,float(i[1]), float(i[2]), float(i[3]),float(i[4]), step)
            matrix_mult( s[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []
        elif i[0] == 'hermite' or i[0] == 'bezier':
            add_curve(edges,
                      float(i[1]), float(i[2]),
                      float(i[3]), float(i[4]),
                      float(i[5]), float(i[6]),
                      float(i[7]), float(i[8]),
                      step, i[0])
            matrix_mult( s[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []
        elif i[0] == 'line':
            add_edge( edges,float(i[1]), float(i[2]), float(i[3]),float(i[4]), float(i[5]), float(i[6]))
            matrix_mult( s[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []
        elif i[0] == 'scale':
            t = make_scale(float(i[1]), float(i[2]), float(i[3]))
            matrix_mult( s[-1], t )
            s[-1] = [ x[:] for x in t]
        elif i[0] == 'move':
            t = make_translate(float(i[1]), float(i[2]), float(i[3]))
            matrix_mult( s[-1], t )
            s[-1] = [ x[:] for x in t]
        elif i[0] == 'rotate':
            theta = float(i[2]) * (math.pi / 180)
            if i[1] == 'x':
                t = make_rotX(theta)
            elif i[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
                matrix_mult( s[-1], t )
                s[-1] = [ x[:] for x in t]
        elif i[0] == 'display' or i[0] == 'save':
            if i[0] == 'display':
                display(screen)
        elif i[0] == 'push':
            s.append( [x[:] for x in s[-1]] )
        elif i[0] == 'pop':
            s.pop()
        else:
            save_extension(screen, i[1] + i[2])
