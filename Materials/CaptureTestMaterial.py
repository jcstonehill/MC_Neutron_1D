from Materials.Material import Material

class CaptureTestMaterial(Material):

  def ScatteringCrossSection(self) -> float:
    return 0.01

  def FissionCrossSection(self) -> float:
    return 0.01

  def CaptureCrossSection(self) -> float:
    return 5

  def NeutronsPerFission(self) -> int:
    return 0