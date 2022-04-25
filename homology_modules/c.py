# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:54:49 2022

@author: epick
"""
import ctypes
import sys
import os 

#dir_path = os.path.dirname(os.path.realpath(__file__))
handle = ctypes.CDLL( "homology_modules/libTest.so")     

handle.FindCliques.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_wchar_p] 
  
def FindCliques(c,filename):
    return handle.FindCliques(0,0,c, filename)    


