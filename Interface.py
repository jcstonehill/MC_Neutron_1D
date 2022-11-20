from enum import Enum
from abc import ABC, abstractmethod

from Region import Region

class InterfaceType(Enum):
  Coupled = 1
  Reflective = 2
  Void = 3

class Interface(ABC):

  interfaceID: int
  position: list[float]
  regions: list[Region]
  interfaceType: InterfaceType

  @abstractmethod
  def GetCollisionDistance(self, position: list[float], direction: list[float]) -> float:
    pass

  @abstractmethod
  def IsHitByParticleDuringFlight(self, startPosition: list[float], endPosition: list[float]) -> bool:
    pass

  @abstractmethod
  def GetCoupledRegion(self, region: Region):
    pass
  # def GetCoupledRegion(self, region: Region):
  #   if(region is self.region1):
  #     return self.region2
  #   elif(region is self.region2):
  #     return self.region1
  #   else:
  #     print("DEBUG: Interface.py: GetCoupledRegion: Input does not match either region on this interface.\nInput: " + region.name + "\nregion1: " + self.region1.name + "\nregion2: " + self.region2.name + "\n\n")



class Point(Interface):

  def __init__(self, interfaceID: int, position: list[float], interfaceType: InterfaceType):
    self.interfaceID = interfaceID
    self.position = position
    self.interfaceType = interfaceType

  def SetRegions(self, regions: list[Region]):
    self.regions = regions

  def IsHitByParticleDuringFlight(self, startPosition: list[float], endPosition: list[float]) -> bool:
    if(startPosition[0] == self.position[0]):
      return False
    elif(endPosition[0] == self.position[0]):
      print("Interface.py: Point(): CollisionOccursDuringFlight: The calculated end position was EXACTLY on the interface.")
      breakpoint()
    else:
      return (startPosition[0] > self.position[0]) != (endPosition[0] > self.position[0])

  def GetCollisionDistance(self, startPosition: list[float], endPosition: list[float]):
    return abs(self.position[0] - startPosition[0])

  def GetCoupledRegion(self, oldRegion: Region) -> Region:
    newRegion: Region
    
    for region in self.regions:
      if(region != oldRegion):
        newRegion = region

    if(newRegion is None):
      print("Interface.py: Point(): Input does not match either region on this interface.\nInput: " + oldRegion.name + "\nregion1: " + self.regions[0].name + "\nregion2: " + self.regions[1].name + "\n\n")
    
    return newRegion