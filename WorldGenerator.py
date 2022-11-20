from Interface import *
from Region import Region
from Materials.FissionTestMaterial import FissionTestMaterial
from Materials.CaptureTestMaterial import CaptureTestMaterial
from Materials.ScatteringTestMaterial import ScatteringTestMaterial


class UserInput():
  interfaces = [
    Point(0, [-1, 0, 0], InterfaceType.Reflective),
    Point(1, [-0.5, 0, 0], InterfaceType.Coupled),
    Point(2, [0.9, 0, 0], InterfaceType.Coupled),
    Point(3, [1, 0, 0], InterfaceType.Void)
  ]

  regions = [
    Region(0, "fuel", [interfaces[0], interfaces[1]], FissionTestMaterial()),
    Region(1, "moderator", [interfaces[1], interfaces[2]], ScatteringTestMaterial()),
    Region(3, "poison", [interfaces[2], interfaces[3]], CaptureTestMaterial())
  ]

  interfaces[0].SetRegions([regions[0]])
  interfaces[1].SetRegions([regions[0], regions[1]])
  interfaces[2].SetRegions([regions[1], regions[2]])
  interfaces[3].SetRegions([regions[2]])
  
  startingSourcePosition = [-0.75, 0, 0]
  startingRegion = regions[0]

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