import numpy as np
from RNG import CustomRNG as rng
from Region import Region

class Neutron():
  position: list[float]
  direction: list[float]
  travelDistance: float
  region: Region
  isAlive: bool
  
  def __init__(self, startingPosition: list[float], startingRegion: Region):
    self.position = startingPosition
    self.region = startingRegion
    self.isAlive = True
    self.DetermineNewFlightAngle()
    self.DetermineUnrestrictedTravelDistance()

  def SetFlightAngle(self, newDirection):
    self.direction = newDirection

  def DetermineNewFlightAngle(self):
    self.direction = [rng.RandomFromRange(-1, 1), 0, 0]

  def DetermineUnrestrictedTravelDistance(self):
    self.travelDistance = -(1/self.region.material.TotalCrossSection())*np.log(rng.RandomFromRange(0, 1))

  def GetTravelVector(self) -> list[float]:
    travelVector = []
    for element in self.direction:
      travelVector.append(element*self.travelDistance)
    return travelVector

  def DesiredDestination(self) -> list[float]:
    travelVector = self.GetTravelVector()
    desiredDestination = []
    for i in range(len(travelVector)):
      desiredDestination.append(travelVector[i] + self.position[i])

    return desiredDestination

  def GetDirectionUnitVector(self) -> list[float]:
    return self.direction

  def SetRegion(self, newRegion: Region):
    self.region = newRegion

  def Kill(self):
    self.isAlive = False