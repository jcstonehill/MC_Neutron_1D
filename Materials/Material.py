from abc import ABC, abstractmethod

class Material(ABC):

  neutronMass = 1.008

  @abstractmethod
  def MassDensity(self) -> float:
    return 0

  @abstractmethod
  def MolarMass(self) -> float:
    return 0

  def AtomDensity(self) -> float:
    return 6.0221408*(10**23)*self.MassDensity() / self.MolarMass()

  @abstractmethod
  def ScatteringCrossSection(self) -> float:
    return 0

  @abstractmethod
  def FissionCrossSection(self) -> float:
    return 0

  @abstractmethod
  def CaptureCrossSection(self) -> float:
    return 0

  @abstractmethod
  def NeutronsPerFission(self) -> int:
    pass

  def TotalCrossSection(self, E: float) -> float:
    return self.ScatteringCrossSection(E) + self.FissionCrossSection(E) + self.CaptureCrossSection(E)

  def ScatteringFraction(self, E: float) -> float:
    totalCrossSection = self.TotalCrossSection(E)
    if(totalCrossSection == 0):
      return 0
    else:
      return self.ScatteringCrossSection(E) / self.TotalCrossSection(E)

  def CaptureFraction(self, E: float) -> float:
    totalCrossSection = self.TotalCrossSection(E)
    if(totalCrossSection == 0):
      return 0
    else:
      return self.CaptureCrossSection(E) / self.TotalCrossSection(E)

  def FissionFraction(self, E: float) -> float:
    totalCrossSection = self.TotalCrossSection(E)
    if(totalCrossSection == 0):
      return 0
    else:
      return self.FissionCrossSection(E) / self.TotalCrossSection(E)