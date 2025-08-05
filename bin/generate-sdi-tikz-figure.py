#!/usr/bin/env python3

from sys import argv, exit
import re

# node patterns
node_pattern     = re.compile("\<node id\=\"([^\"]+)\"\>")
geometry_pattern = re.compile("\<y\:Geometry ([^\\\\]+)\/\>")
fill_pattern     = re.compile("\<y\:Fill ([^\\\\]+)\/\>")
shape_pattern    = re.compile("\<y\:Shape type\=\"([^\"]+)\"\/\>")
trigger_pattern  = re.compile("\<\/node\>")

# edge patterns
edge_pattern   = re.compile("\<edge ([^\>]+)\>")
arrows_pattern = re.compile("\<y\:Arrows ([^\\\\]+)\/\>")

# define bounding box (in mm units)
scale = 0.1
bbox_h = 390*scale
bbox_w = 427*scale
bboxL_offset_x = 10
bboxL_offset_y = 0
bboxR_offset_x = 145 - 20 - bbox_w
bboxR_offset_y = bboxL_offset_y
bboxL_n = bboxL_offset_y
bboxL_s = bboxL_offset_y-bbox_h
bboxL_e = bboxL_offset_x
bboxL_w = bboxL_offset_x+bbox_w
bboxR_n = bboxR_offset_y
bboxR_s = bboxR_offset_y-bbox_h
bboxR_e = bboxR_offset_x
bboxR_w = bboxR_offset_x+bbox_w

prefix = """
\\begin{tikzpicture}[remember picture,overlay]
  \\newcommand{\\spacing}[0]{6mm}
  \\newcommand{\\modelColor}[0]{black!70}
  \\newcommand{\\highlightColor}[0]{purple}
  
  \\coordinate (origo) at (0cm,0cm);
  
  \\coordinate (pattern) at (1cm,-4.2cm);
  \\coordinate (matchI) at (3cm,-4.2cm);
  
  \\tikzstyle{node}=[
    overlay,
    draw=\\modelColor,
    anchor=center,
    align=center,
%    very thick,
    inner sep=0pt,
  ]
  \\tikzstyle{snode} = [
    node,
    rectangle,
    minimum height=2.2mm,
    minimum width=2.2mm,
  ]
  \\tikzstyle{dnode} = [
    node,
    diamond,
    minimum height=3mm,
    minimum width=3mm,
  ]
  \\tikzstyle{cnode} = [
    node,
    circle,
    minimum height=2.5mm,
    minimum width=2.5mm,
  ]
  
  \\tikzstyle{edge} = [
    -,
%    very thick,
    >=stealth,
    draw=\\modelColor,
  ]
  
  \\tikzstyle{path} = [
    -,
    very thick,
    >=stealth,
    draw=\\modelColor,
    decoration={snake,amplitude=0.4mm},
    decorate,
  ]
"""
postfix = """
\\end{tikzpicture}
"""

# guard: arguments
if len(argv)!=3:
  print("Syntax: %s INPUT_GRAPHML_FILENAME OUTPUT_TEX_FILENAME"%argv[0])
  print("        %s figs/sdi.graphml figs/graph-queries.tex"%argv[0])
  exit(1)

ifilename = argv[1]
ofilename = argv[2]

# read file
with open(ifilename) as fo:
  lines = fo.readlines()

# parse inputs
nodes = []
edges = []
for line in lines:
  line = line.strip()
  
  node_mo     = re.match(node_pattern, line)
  geometry_mo = re.match(geometry_pattern, line)
  fill_mo     = re.match(fill_pattern, line)
  shape_mo    = re.match(shape_pattern, line)
  trigger_mo  = re.match(trigger_pattern, line)
  edge_mo     = re.match(edge_pattern, line)
  arrows_mo   = re.match(arrows_pattern, line)
  
  if node_mo:
    node_id = node_mo.group(1)
  elif geometry_mo:
    for entry in geometry_mo.group(1).split(" "):
      pair = entry.split("=")
      if pair[0]=="x":
        x = float(pair[1][1:-1])
      elif pair[0]=="y":
        y = float(pair[1][1:-1])
  elif fill_mo:
    for entry in fill_mo.group(1).split(" "):
      pair = entry.split("=")
      if pair[0]=="color":
        color = pair[1][1:-1]
  elif shape_mo:
    shape = shape_mo.group(1)
  elif trigger_mo:
    #print("node (%f,%f) %s '%s' %s" % (x,y,shape, node_id,color))
    nodes.append({
      "x": x,
      "y": y,
      "shape": shape,
      "id": node_id,
      "color": color,
    })
  elif edge_mo:
    for entry in edge_mo.group(1).split(" "):
      pair = entry.split("=")
      if pair[0]=="source":
        source = pair[1][1:-1]
      elif pair[0]=="target":
        target = pair[1][1:-1]
  elif arrows_mo:
    for entry in arrows_mo.group(1).split(" "):
      pair = entry.split("=")
      if pair[0]=="source":
        source_arrow = pair[1][1:-1]
      elif pair[0]=="target":
        target_arrow = pair[1][1:-1]
    
    edge_type = "edge" if source_arrow=="none" and target_arrow=="none" else "path"
    edges.append({
      "source": source,
      "target": target,
      "type": edge_type,
    })

# find extremes
minx = None
maxx = None
miny = None
maxy = None
for node in nodes:
  x = node["x"]
  y = node["y"]
  if minx==None or x<minx: minx = x
  if maxx==None or x>maxx: maxx = x
  if miny==None or y<miny: miny = y
  if maxy==None or y>maxy: maxy = y
print("x=[%f,%f] y=[%f,%f]"%(minx, maxx, miny, maxy))

# define scaling functions
scaleLx = lambda x: bboxL_e - (bboxL_e-bboxL_w)*x/(maxx-minx)
scaleLy = lambda y: bboxL_n + (bboxL_s-bboxL_n)*y/(maxy-miny)
scaleRx = lambda x: bboxR_e - (bboxR_e-bboxR_w)*x/(maxx-minx)
scaleRy = lambda y: bboxR_n + (bboxR_s-bboxR_n)*y/(maxy-miny)
scalerL = (scaleLx, scaleLy)
scalerR = (scaleRx, scaleRy)

# emitters
def emit_nodes (lines, nodes, only, filter_fun, thickness, scalers, stroke=None, fill=None, prefix=""):
  (scalex, scaley) = scalers
  typemod = ""
  if stroke: typemod += ",draw=%s" % stroke
  if fill: typemod += ",fill=%s" % fill
  
  if filter_fun==None: filter_fun = lambda entry: True
  if only:
    lines.append("\\only<%s>{" % only)
  for node in filter(filter_fun, nodes):
#    nodetype = {"rectangle": "snode", "ellipse": "cnode", "diamond": "dnode"}[node["shape"]]
    nodetype = "cnode"
    pars = (
      nodetype,
      typemod,
      thickness,
      prefix,
      node["id"],
      scalex(node["x"]),
      scaley(node["y"]),
    )
    lines.append("  \\node[%s%s%s] (%s%s) at ([xshift=%fmm, yshift=%fmm] origo) {};" % pars)
  if only:
    lines.append("}")
def emit_edges (lines, edges, only, filter_fun, thickness, stroke=None, prefixSrc="", prefixDst=""):
  typemod = ""
  if stroke: typemod += ",draw=%s" % stroke
  
  if filter_fun==None: filter_fun = lambda entry: True
  if only:
    lines.append("\\only<%s>{" % only)
  for edge in filter(filter_fun, edges):
    pars = (
      edge["type"],
      typemod,
      thickness,
      prefixSrc,
      edge["source"],
      prefixDst,
      edge["target"],
    )
    lines.append("  \draw[%s%s%s] (%s%s) to (%s%s);" % pars)
  if only:
    lines.append("}")

nodes_domain1  = list(filter(lambda node: node["color"]=="#FF00FF", nodes))
nodes_domain2  = list(filter(lambda node: node["color"]=="#00FFFF", nodes))
nodes_domain3  = list(filter(lambda node: node["color"]=="#800080", nodes))
nodes_highlight1  = list(filter(lambda node: node["shape"]=="hexagon" and node["color"]=="#FF00FF", nodes))
nodes_highlight2  = list(filter(lambda node: node["shape"]=="hexagon" and node["color"]=="#00FFFF", nodes))
nodes_highlight3  = list(filter(lambda node: node["shape"]=="hexagon" and node["color"]=="#800080", nodes))
nodes_domain1_ids  = list(map(lambda node: node["id"], nodes_domain1))
nodes_domain2_ids  = list(map(lambda node: node["id"], nodes_domain2))
nodes_domain3_ids  = list(map(lambda node: node["id"], nodes_domain3))
nodes_highlight1_ids  = list(map(lambda node: node["id"], nodes_highlight1))
nodes_highlight2_ids  = list(map(lambda node: node["id"], nodes_highlight2))
nodes_highlight3_ids  = list(map(lambda node: node["id"], nodes_highlight3))
#print(set(list(map(lambda node: node["color"], nodes))))

# generate tikz code
lines=prefix.split("\n")
emit_nodes(lines, nodes_domain1, "1-", None, "", scalerL, stroke="black", fill="black!40", prefix="L")
emit_nodes(lines, nodes_domain2, "1-", None, "", scalerL, stroke="black", fill="black!40", prefix="L")
emit_nodes(lines, nodes_domain3, "1-", None, "", scalerL, stroke="black", fill="black!40", prefix="L")
emit_edges(lines, edges, "1-", lambda edge: True, "", stroke="black", prefixSrc="L", prefixDst="L")
emit_nodes(lines, nodes_domain1, "2-", None, "", scalerR, stroke="black!20", fill="black!20", prefix="R")
emit_nodes(lines, nodes_domain2, "2-", None, "", scalerR, stroke="black!20", fill="black!20", prefix="R")
emit_nodes(lines, nodes_domain3, "2-", None, "", scalerR, stroke="black!20", fill="black!20", prefix="R")
emit_edges(lines, edges, "2-", lambda edge: True, "", stroke="black!20", prefixSrc="R", prefixDst="R")
emit_nodes(lines, nodes_domain1, "3-", None, "", scalerR, stroke="purple", fill="purple!40", prefix="R")
emit_edges(lines, edges, "3-", lambda edge: edge["source"] in nodes_domain1_ids and edge["target"] in nodes_domain1_ids, "", stroke="purple", prefixSrc="R", prefixDst="R")
emit_nodes(lines, nodes_domain2, "4-", None, "", scalerR, stroke="teal", fill="teal!40", prefix="R")
emit_edges(lines, edges, "4-", lambda edge: edge["source"] in nodes_domain2_ids and edge["target"] in nodes_domain2_ids, "", stroke="teal", prefixSrc="R", prefixDst="R")
emit_nodes(lines, nodes_domain3, "5-", None, "", scalerR, stroke="blue", fill="blue!40", prefix="R")
emit_edges(lines, edges, "5-", lambda edge: edge["source"] in nodes_domain3_ids and edge["target"] in nodes_domain3_ids, "", stroke="blue", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "6-", lambda edge: edge["source"] in nodes_domain1_ids and edge["target"] in nodes_domain2_ids, "", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "6-", lambda edge: edge["source"] in nodes_domain1_ids and edge["target"] in nodes_domain3_ids, "", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "6-", lambda edge: edge["source"] in nodes_domain2_ids and edge["target"] in nodes_domain1_ids, "", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "6-", lambda edge: edge["source"] in nodes_domain2_ids and edge["target"] in nodes_domain3_ids, "", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "6-", lambda edge: edge["source"] in nodes_domain3_ids and edge["target"] in nodes_domain1_ids, "", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "6-", lambda edge: edge["source"] in nodes_domain3_ids and edge["target"] in nodes_domain2_ids, "", stroke="black", prefixSrc="R", prefixDst="R")
emit_nodes(lines, nodes_highlight1, "7-", None, ",very thick", scalerL, stroke="black", fill="black!40", prefix="L")
emit_nodes(lines, nodes_highlight2, "7-", None, ",very thick", scalerL, stroke="black", fill="black!40", prefix="L")
emit_nodes(lines, nodes_highlight3, "7-", None, ",very thick", scalerL, stroke="black", fill="black!40", prefix="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight1_ids and edge["target"] in nodes_highlight1_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight2_ids and edge["target"] in nodes_highlight2_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight3_ids and edge["target"] in nodes_highlight3_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight1_ids and edge["target"] in nodes_highlight2_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight1_ids and edge["target"] in nodes_highlight3_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight2_ids and edge["target"] in nodes_highlight1_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight2_ids and edge["target"] in nodes_highlight3_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight3_ids and edge["target"] in nodes_highlight1_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_edges(lines, edges, "7-", lambda edge: edge["source"] in nodes_highlight3_ids and edge["target"] in nodes_highlight2_ids, ",very thick", stroke="black", prefixSrc="L", prefixDst="L")
emit_nodes(lines, nodes_highlight1, "8-", None, ",very thick", scalerR, stroke="purple", fill="purple!40", prefix="R")
emit_nodes(lines, nodes_highlight2, "8-", None, ",very thick", scalerR, stroke="teal", fill="teal!40", prefix="R")
emit_nodes(lines, nodes_highlight3, "8-", None, ",very thick", scalerR, stroke="blue", fill="blue!40", prefix="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight1_ids and edge["target"] in nodes_highlight1_ids, ",very thick", stroke="purple", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight2_ids and edge["target"] in nodes_highlight2_ids, ",very thick", stroke="teal", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight3_ids and edge["target"] in nodes_highlight3_ids, ",very thick", stroke="blue", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight1_ids and edge["target"] in nodes_highlight2_ids, ",very thick", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight1_ids and edge["target"] in nodes_highlight3_ids, ",very thick", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight2_ids and edge["target"] in nodes_highlight1_ids, ",very thick", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight2_ids and edge["target"] in nodes_highlight3_ids, ",very thick", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight3_ids and edge["target"] in nodes_highlight1_ids, ",very thick", stroke="black", prefixSrc="R", prefixDst="R")
emit_edges(lines, edges, "8-", lambda edge: edge["source"] in nodes_highlight3_ids and edge["target"] in nodes_highlight2_ids, ",very thick", stroke="black", prefixSrc="R", prefixDst="R")
for line in postfix.split("\n"): lines.append(line)

# write output
with open(ofilename, "w") as fo:
  fo.writelines(map(lambda line: "%s\n"%line, lines))

