from numpy import random

class CustomRNG:
  def RandomFromRange(lowerLim: float, upperLim: float):
    return (upperLim - lowerLim)*random.random() + lowerLim