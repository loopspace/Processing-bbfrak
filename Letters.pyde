import Bezier as bz
from Path import Path
import bbfrak

def setup():
    size(480,480)
    global t, mt, sp, pen, letter, coords
    pen = Path()
    pen.addMoveTo(PVector(-.25,-.25))
    pen.addLineTo(PVector(.25,.25))
    #pen.addMoveTo(PVector(.5,.5))
    pen.scale=10
    pen.colour = (0,0,0)
    t = 0
    mt = bbfrak.a.length + 50
    sp = 5
    letter = 0

    wds = []
    wd = bbfrak.a.boundingbox[1].x - bbfrak.a.boundingbox[0].x
    ht = bbfrak.f.boundingbox[1].y - bbfrak.g.boundingbox[0].y
    
    for i in range(26):
        wds.append(wd)
    wds[5] = .7*wd
    wds[8] = .6*wd
    wds[11] = .5*wd
    wds[12] = 1.9*wd
    wds[19] = .6*wd
    wds[22] = 1.9*wd
    
    coords = []
    x = -140
    y = 150
    for i in range(26):
        coords.append([x,y])
        x += wds[i]+20
        if i%7 == 6:
            x = -140
            y += -ht


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
        lt.draw()
        popMatrix()
        
    
    pushMatrix()
    if letter < 26:
        translate(-220,0)
        if t > mt:
            translate((t - mt)*(coords[letter][0]+220)/100,(t - mt)*(coords[letter][1])/100)
        lt = getattr(bbfrak,chr(97+letter))
        lt.drawAtLength(t)
    popMatrix()
    #saveFrame("frames/bbfrak-####.png")
    t += sp
    if t > mt + 100:
        if letter < 26:
            letter += 1
        t = 0
        if letter < 26:
            mt = getattr(bbfrak,chr(97+letter)).length + 50
    
