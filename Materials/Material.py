from abc import ABC, abstractmethod

class Material(ABC):

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

  def TotalCrossSection(self) -> float:
    return self.ScatteringCrossSection() + self.FissionCrossSection() + self.CaptureCrossSection()

  def ScatteringFraction(self) -> float:
    return self.ScatteringCrossSection() / self.TotalCrossSection()

  def CaptureFraction(self) -> float:
    return self.CaptureCrossSection() / self.TotalCrossSection()

  def FissionFraction(self) -> float:
    return self.FissionCrossSection() / self.TotalCrossSection()