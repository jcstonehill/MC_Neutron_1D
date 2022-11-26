import json
from Materials.Material import Material
from scipy.interpolate import interp1d

class CaptureTestMaterial(Material):

  def __init__(self):
    self.CreateCrossSectionObjects()

  def MassDensity(self) -> float:
    return 2.34

  def MolarMass(self) -> float:
    return 10.0129

  def ScatteringCrossSection(self, E: float) -> float:
    return self.AtomDensity() * self.xs_scattering(E) * (10 ** -24)

  def FissionCrossSection(self, E: float) -> float:
    return 0

  def CaptureCrossSection(self, E: float) -> float:
    return self.AtomDensity() * self.xs_capture(E) * (10 ** -24)

  def NeutronsPerFission(self, E: float) -> int:
    return 0

  def CreateCrossSectionObjects(self):
    file = open("./CrossSections/B10/total.txt")
    test = json.load(file)
    E = []
    xs = []
    for i in test['datasets']:
      for j in i['pts']:
        E.append(j['E'])
        xs.append(j['Sig'])
    self.xs_total = interp1d(E, xs)
    file.close()

    file = open("./CrossSections/B10/capture.txt")
    test = json.load(file)
    E = []
    xs = []
    for i in test['datasets']:
      for j in i['pts']:
        E.append(j['E'])
        xs.append(j['Sig'])
    self.xs_capture = interp1d(E, xs)
    file.close()

    file = open("./CrossSections/B10/elastic.txt")
    test = json.load(file)
    E = []
    xs = []
    for i in test['datasets']:
      for j in i['pts']:
        E.append(j['E'])
        xs.append(j['Sig'])
    self.xs_scattering = interp1d(E, xs)
    file.close()