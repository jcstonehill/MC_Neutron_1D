from __future__ import annotations
from typing import TYPE_CHECKING

from Materials.Material import Material
from dataclasses import dataclass

if(TYPE_CHECKING):
  from Interface import Interface

@dataclass
class Region():

  id: int
  name: str
  interfaces: list[Interface]
  material: Material