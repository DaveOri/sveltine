#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 16:30:05 2018

@author: dori
"""

from pytmatrix import tmatrix

scatt = tmatrix.Scatterer(radius=0.01)

def Sorinet(scatt, t0=None, t=None, p0=None, p=None):
  if t0 is not None:
    scatt.thet0 = t0
  if p0 is not None:
    scatt.p0 = p0
  if t is not None:
    scatt.thet = t
  if p is not None:
    scatt.phi = p
  return scatt.get_S()[0,0]