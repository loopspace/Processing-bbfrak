import Bezier as bz
from Path import Path
import bbfrak
import math

def setup():
    size(480,480)
    global t, mt, sp, pen, letter, coords, wd, ht, pt, bt
    pen = Path()
    pen.addMoveTo(PVector(-.25,-.25))
    pen.addLineTo(PVector(.25,.25))
    #pen.addMoveTo(PVector(.5,.5))
    pen.scale=10
    pen.colour = (0,0,0)
    t = 0
    bt = 50
    mt = bbfrak.a.length + bt
    sp = 8
    pt = 50
    letter = 0

    wds = []
    wd = bbfrak.a.boundingbox[1].x - bbfrak.a.boundingbox[0].x
    ht = bbfrak.f.boundingbox[1].y - bbfrak.g.boundingbox[0].y
        
    coords = []
    for i in range(26):
        coords.append([180*math.sin(TWO_PI/26*i),180*math.cos(TWO_PI*i/26)-ht/5])
    coords[5][0] += 15
    coords[6][0] += 15
    coords[6][1] += 10
    coords[7][0] -= 10
    coords[9][0] += 10
    coords[11][0] += 15
    coords[16] = [180*math.sin(TWO_PI/26*16.5),180*math.cos(TWO_PI*16.5/26)-ht/5]
    coords[19][0] -= 10


def draw():
    global t, letter, x, mt
    background(255)
    translate(240,240)
    scale(1,-1)
    noFill()
    stroke(0)
    strokeWeight(3)
    for i in range(letter):
        lt = getattr(bbfrak,chr(97+i))
        pushMatrix()
        translate(coords[i][0],coords[i][1])
        scale(.6)
        lt.draw()
        popMatrix()
        
    pushMatrix()
    if letter < 26:
        translate(-wd,-ht/2)
        if t > mt:
            translate((t - mt)*(coords[letter][0] + wd)/pt,(t - mt)*(coords[letter][1] + ht/2)/pt)
            scale(2 - (t - mt)*1.4/pt)
        else:
            scale(2)
        lt = getattr(bbfrak,chr(97+letter))
        lt.drawAtLength(t)
    popMatrix()
    saveFrame("frames/bbfrak-####.png")
    t += sp
    if t > mt + pt:
        if letter < 26:
            letter += 1
        t = 0
        if letter < 26:
            mt = getattr(bbfrak,chr(97+letter)).length + bt
        else:
            noLoop()
    
