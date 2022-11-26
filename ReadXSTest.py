from Materials.CaptureTestMaterial import CaptureTestMaterial

if __name__ == "__main__":
  object = CaptureTestMaterial()
  print(object.xs_total(0.01))
  print(object.TotalCrossSection(0.01))