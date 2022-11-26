import numpy as np
from RNG import CustomRNG as rng
from Region import Region
from math import sqrt, acos, sin, cos, pi

class Neutron():
  position: list[float]
  direction: list[float]
  travelDistance: float
  region: Region
  isAlive: bool
  
  E: float

  def __init__(self, startingPosition: list[float], startingRegion: Region):
    self.position = startingPosition
    self.region = startingRegion
    self.isAlive = True
    self.E = 2*(10**6)

    self.DetermineNewFlightAngle()
    self.DetermineUnrestrictedTravelDistance()

  def Scatter(self):
    oldDirection = self.direction
    self.DetermineNewFlightAngle()
    newDirection = self.direction

    dotProduct = 0

    for i in range(len(oldDirection)):
      dotProduct = dotProduct + abs(oldDirection[i]*newDirection[i])

    angle = acos(dotProduct)

    a = self.region.material.MolarMass() / self.region.material.neutronMass

    oldE = self.E

    
    C1 = oldE / ((a+1)**2)
    C2 = cos(angle)

    try:
      C3 = sqrt((cos(angle)**2)+(a**2)-1)
    except:
      print(angle)
      print(a)

    self.E = C1*((C2+C3)**2)

    if(self.E < 1e-5):
      self.E = 1e-5

  def SetFlightAngle(self, newDirection):
    self.direction = newDirection

  def DetermineNewFlightAngle(self):
    mu = rng.RandomFromRange(-1, 1)
    omega = rng.RandomFromRange(0, 2*pi)

    x = mu
    y = sqrt(1-(mu**2)) * cos(omega)
    z = sqrt(1-(mu**2)) * sin(omega)
    
    newDirection = [x, y, z]
    magnitude = sqrt((x**2)+(y**2)+(z**2))
    for i in range(len(newDirection)):
      newDirection[i] = newDirection[i] / magnitude

    self.direction = newDirection

  def DetermineUnrestrictedTravelDistance(self):
    self.travelDistance = -(1/self.region.material.TotalCrossSection(self.E))*np.log(rng.RandomFromRange(0, 1))

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