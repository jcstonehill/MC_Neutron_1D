from Materials.Material import Material
import json
from scipy.interpolate import interp1d


# U-235
class FissionTestMaterial(Material):

  def __init__(self):
    self.CreateCrossSectionObjects()

  def MassDensity(self) -> float:
    return 19.1

  def MolarMass(self) -> float:
    return 235.0439299

  def ScatteringCrossSection(self, E) -> float:
    return self.AtomDensity() * self.xs_scattering(E) * (10 ** -24)

  def FissionCrossSection(self, E) -> float:
    return self.AtomDensity() * self.xs_fission(E) * (10 ** -24)

  def CaptureCrossSection(self, E) -> float:
    return self.AtomDensity() * self.xs_capture(E) * (10 ** -24)

  def NeutronsPerFission(self) -> int:
    return 3

  def CreateCrossSectionObjects(self):
    file = open("./CrossSections/U235/total.txt")
    test = json.load(file)
    E = []
    xs = []
    for i in test['datasets']:
      for j in i['pts']:
        E.append(j['E'])
        xs.append(j['Sig'])
    self.xs_total = interp1d(E, xs)
    file.close()

    file = open("./CrossSections/U235/capture.txt")
    test = json.load(file)
    E = []
    xs = []
    for i in test['datasets']:
      for j in i['pts']:
        E.append(j['E'])
        xs.append(j['Sig'])
    self.xs_capture = interp1d(E, xs)
    file.close()

    file = open("./CrossSections/U235/elastic.txt")
    test = json.load(file)
    E = []
    xs = []
    for i in test['datasets']:
      for j in i['pts']:
        E.append(j['E'])
        xs.append(j['Sig'])
    self.xs_scattering = interp1d(E, xs)
    file.close()

    file = open("./CrossSections/U235/fission.txt")
    test = json.load(file)
    E = []
    xs = []
    for i in test['datasets']:
      for j in i['pts']:
        E.append(j['E'])
        xs.append(j['Sig'])
    self.xs_fission = interp1d(E, xs)
    file.close()