from Interface import *
from Region import Region
from Materials.FissionTestMaterial import FissionTestMaterial
from Materials.CaptureTestMaterial import CaptureTestMaterial
from Materials.ScatteringTestMaterial import ScatteringTestMaterial
from Materials.VoidTestMaterial import VoidTestMaterial


class UserInput():
  interfaces = [
    Point(0, [-100, 0, 0], InterfaceType.Void),
    Point(1, [-25, 0, 0], InterfaceType.Coupled),
    Point(2, [25,0,0], InterfaceType.Coupled),
    Point(3, [65, 0, 0], InterfaceType.Coupled),
    Point(4, [85, 0, 0], InterfaceType.Coupled),
    Point(5, [100, 0, 0], InterfaceType.Void)
  ]

  regions = [
    Region(0, "leftMod", [interfaces[0], interfaces[1]], ScatteringTestMaterial()),
    Region(1, "fuel", [interfaces[1], interfaces[2]], FissionTestMaterial()),
    Region(2, "rightMod1", [interfaces[2], interfaces[3]], ScatteringTestMaterial()),
    Region(3, "void", [interfaces[3], interfaces[4]], VoidTestMaterial()),
    Region(4, "rightmod2", [interfaces[4], interfaces[5]], ScatteringTestMaterial())
  ]

  interfaces[0].SetRegions([regions[0]])
  interfaces[1].SetRegions([regions[0], regions[1]])
  interfaces[2].SetRegions([regions[1], regions[2]])
  interfaces[3].SetRegions([regions[2], regions[3]])
  interfaces[4].SetRegions([regions[3], regions[4]])
  interfaces[5].SetRegions([regions[4]])

  startingSourcePosition = [0, 0, 0]
  startingRegion = regions[1]

class WorldGenerator():

  def __init__(self):
    userInput = UserInput()
    self.interfaces = userInput.interfaces
    self.regions = userInput.regions
    self.startingSourcePosition = userInput.startingSourcePosition
    self.startingRegion = userInput.startingRegion

  def GetStartingPointSource(self):
    return self.startingSourcePosition

  def GetStartingRegion(self):
    return self.startingRegion