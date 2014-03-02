import maya.cmds as cmds
import random
from maya import cmds
from random import uniform

class LSystem_Grid:
    def __init__(self, axiom, x=4, y=4, z=4, offset=4):
        self.gridCubes = [ [ [(u,v,w) for w in xrange(z) ] for v in xrange(y) ] for u in xrange(x) ]
        self.grid(x, y, z, axiom, offset)

    def printself( self ):
        for x in xrange(len(self.gridCubes)):
            for y in xrange(len(self.gridCubes[x])):
                for z in xrange(len(self.gridCubes[y])):
                    print "%i %i %i:" % (x, y, z),
                    print self.gridCubes[x][y][z]

    def grid(self, width, height, depth, axiom, offset=4, ):
        for x in xrange(width):
            for y in xrange(height):
                for z in xrange(depth):
                    newCube = cmds.polyCube(name='grid_%i_%i_%i'%(x,y,z), h=0.25)[0]
                    cmds.select(newCube)
                    cmds.xform(t=(offset*x, offset*z, offset*y))
                    self.gridCubes[x][y][z] = newCube

        self.mapGrid(axiom, width, height, depth, offset)

    def mapGrid(self, axiom, width, height, depth, offset):
        self.mapping = { 'x':[], 'y':[], 'z':[] }
        lenX = len(axiom[0])
        lenY = len(axiom[1])
        lenZ = len(axiom[2])

        for x in xrange(width):
            self.mapping['x'].append(axiom[0][x % lenX])
            self.addLabel(offset*x, -offset, -offset, self.mapping['x'][-1])
        for y in xrange(height):
            self.mapping['y'].append(axiom[1][y % lenY])
            self.addLabel(-offset, offset*y, -offset, self.mapping['y'][-1])
        for z in xrange(depth):
            self.mapping['z'].append(axiom[2][z % lenZ])
            self.addLabel(-offset, -offset, offset*z, self.mapping['z'][-1])

    def addLabel(self, x, y, z, label):
        cmds.textCurves(f="Times New Roman|h-4|w400|c0",t=label)
        cmds.xform(ro=(270,180,0), t=(x, z, y) )

    def parse(self, inputs):
        for x in xrange(len(self.gridCubes)):
            for y in xrange(len(self.gridCubes[x])):
                for z in xrange(len(self.gridCubes[x][y])):
                    if self.mapping['x'][x] in inputs:
                        cmds.select(self.gridCubes[x][y][z])
                        inputs[ self.mapping['x'][x] ]()

                    if self.mapping['y'][y] in inputs:
                        cmds.select(self.gridCubes[x][y][z])
                        inputs[ self.mapping['y'][y] ]()

                    if self.mapping['z'][z] in inputs:
                        cmds.select(self.gridCubes[x][y][z])
                        inputs[ self.mapping['z'][z] ]()

cmds.select(all=True)
cmds.delete()
test = LSystem_Grid(("ABCBBCA", "ACBB", "BCABAB"), 6, 8, 32, 8)
test.parse( { "A":lambda : (cmds.scale(0.5, 48, 0.5)),
              "B":lambda : (cmds.scale(8,8,8)),
              "C":lambda : (cmds.scale(3,9,3)) } )