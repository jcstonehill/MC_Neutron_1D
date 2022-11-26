from abc import ABC, abstractmethod

class Bin(ABC):
  numberOfCollisions: float = 0
  numberOfScatterings: float = 0
  numberOfCaptures: float = 0
  numberOfFissions: float = 0

  @abstractmethod
  def Contains(position: list[float]):
    pass

  def RecordCollision(self):
    self.numberOfCollisions = self.numberOfCollisions + 1

  def RecordScattering(self):
    self.numberOfScatterings = self.numberOfScatterings + 1
  
  def RecordCapture(self):
    self.numberOfCaptures = self.numberOfCaptures + 1

  def RecordFission(self):
    self.numberOfFissions = self.numberOfFissions + 1

  def Reset(self):
    self.numberOfCollisions = 0
    self.numberOfScatterings = 0
    self.numberOfCaptures = 0
    self.numberOfFissions = 0

class Bin1D(Bin):
  xMin: float
  xMax: float
  location: float

  def __init__(self, xMin: float, xMax: float):
    self.xMin = xMin
    self.xMax = xMax
    self.location = (xMin + xMax) / 2

  def Contains(self, position: list[float]):
    return position[0] >= self.xMin and position[0] <= self.xMax

class FluxDetector1D:
  position: list[float]
  flux: float = 0

  def __init__(self, position: list[float]):
    self.position = position

  def CheckForFlux(self, startPosition: list[float], endPosition: list[float]):
    if((startPosition[0] > self.position[0]) != (endPosition[0] > self.position[0])):
      self.flux = self.flux + 1

  def Reset(self):
    self.flux = 0

class Recorder():

  leftGlobalBound: float
  rightGlobalBound: float
  numberOfXBins: int

  bins: list[Bin1D] = []
  fluxDetectors: list[FluxDetector1D] = []

  def __init__(self, leftGlobalBound: float, rightGlobalBound: float, numberOfXBins: int):
    self.leftGlobalBound = leftGlobalBound
    self.rightGlobalBound = rightGlobalBound
    self.numberOfXBins = numberOfXBins
    
    self.dx = (self.rightGlobalBound - self.leftGlobalBound) / self.numberOfXBins

    self.CreateBins()
    self.CreateFluxDetectors()

  def CreateBins(self):
    for i in range(self.numberOfXBins):
      xMin = self.leftGlobalBound + i*self.dx
      xMax = self.leftGlobalBound + (i+1)*self.dx
      self.bins.append(Bin1D(xMin, xMax))

  def CreateFluxDetectors(self):
    xStart = -100 + self.dx/2

    for i in range(self.numberOfXBins):
      self.fluxDetectors.append(FluxDetector1D([(xStart + i*self.dx), 0, 0]))

  def RecordFlux(self, startPosition: list[float], endPosition: list[float]):
    for fluxDetector in self.fluxDetectors:
      fluxDetector.CheckForFlux(startPosition, endPosition)

  def Reset(self):
    for bin in self.bins:
      bin.Reset()

    for fluxDetector in self.fluxDetectors:
      fluxDetector.Reset()

  def GetBinThatContains(self, position: list[float]) -> Bin:
    for bin in self.bins:
      if(bin.Contains(position)):
        return bin
    print("DEBUG: Recording.py: Recorder: GetBinThatContains: Tried to find a bin at [" + str(position[0]) + ", " + str(position[0]) + ", " + str(position[0]) + "], but there was no bin that matches.\n")

  def RecordCollision(self, position: list[float]):
    bin = self.GetBinThatContains(position)
    bin.RecordCollision()

  def RecordScattering(self, position: list[float]):
    bin = self.GetBinThatContains(position)
    bin.RecordScattering()

  def RecordCapture(self, position: list[float]):
    bin = self.GetBinThatContains(position)
    bin.RecordCapture()

  def RecordFission(self, position: list[float]):
    bin = self.GetBinThatContains(position)
    bin.RecordFission()