from Materials.Material import Material

class FissionTestMaterial(Material):

  def ScatteringCrossSection(self) -> float:
    return 0.01

  def FissionCrossSection(self) -> float:
    return 5

  def CaptureCrossSection(self) -> float:
    return 0.01

  def NeutronsPerFission(self) -> int:
    return 4