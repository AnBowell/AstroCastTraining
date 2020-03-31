# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:37:11 2019

@author: Andrew

This function mosiacs the four tiles that cover Kenya.
It essentially turns 4 tiff images into a single large one. 

The input to the function is a list of filepaths to be merged.

"""

import rasterio 

from rasterio.merge import merge

def Merge(ToMerge):
    src_files_to_mosaic = []
    for fp in ToMerge:
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)
    mosaic, out_trans = merge(src_files_to_mosaic)
    
    # Copy the metadata
    out_meta = src.meta.copy()
    
    # Update the metadata
    out_meta.update({"driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "crs": "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"})
    
    Names = ToMerge[0].split('\\')[-1].split('.')
    
    OutputName = str(Names[1])+ str(Names[-2].split('-')[-1]) #This will need to be changed if file dest changes
    
    with rasterio.open('..\MergedTiffData\\'+str(OutputName)+'.tif', "w",**out_meta) as dest:
        dest.write(mosaic)