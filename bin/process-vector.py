#!/usr/bin/env python3

from svgnarrative import Model

#############################################################
################################################# definitions

i = 0
m = Model('figs/vector.svg')

circle = "path3"
curve  = "path4"
line   = "path5"
group  = "layer1"

#############################################################
##################################################### helpers

def store ():
  global i
  filename_svg = 'figs/vector%d.svg' % i
  m.store(filename_svg)
  i += 1

#############################################################
######################################################## main

# clean start
m.hide(circle)
m.hide(curve)
m.hide(line)
store()

# reveal circle
m.show(circle)
store()

# reveal curve
m.show(curve)
store()

# reveal line
m.show(line)
store()

# hide everything through outer group (elements still visible)
m.hide(group)
store()

# add some color
m.stroke(circle, "#ff8800")
m.show(group)
store()

