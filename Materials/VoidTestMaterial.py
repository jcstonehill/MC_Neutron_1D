import json
from Materials.Material import Material
from scipy.interpolate import interp1d

class VoidTestMaterial(Material):

  def __init__(self):
    self.CreateCrossSectionObjects()

  def MassDensity(self) -> float:
    return 0

  def MolarMass(self) -> float:
    return 0

  def ScatteringCrossSection(self, E: float) -> float:
    return 0

  def FissionCrossSection(self, E: float) -> float:
    return 0

  def CaptureCrossSection(self, E: float) -> float:
    return 0

  def NeutronsPerFission(self) -> int:
    return 0

  def CreateCrossSectionObjects(self):
    pass