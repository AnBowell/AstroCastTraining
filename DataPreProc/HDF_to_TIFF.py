# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:18:10 2019

@author: Andrew

This function takes the downloaded raw data and converts it to a tiff for mosiacing.

hdf_file is a file path to an HDF file, ds_dir is the output directory and 

subdataset is the MODIS band we want to convert

"""


# Import necessary modules 

import os
import gdal
import numpy as np


def HDFtoTIFF(hdf_file, dst_dir, subdataset):

    
    # Open the HDF file and read subset (MODIS band)
    hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)
    file_names = hdf_ds.GetSubDatasets()[subdataset][0].split('_')
    band_ds = gdal.Open(hdf_ds.GetSubDatasets()[subdataset][0], gdal.GA_ReadOnly)

    # Read data into a numpy array 
    band_array = band_ds.ReadAsArray().astype(np.int16)

    # Change over fill values for sea etc
    band_array[band_array == -28672] = -32768

    # Using specified output path save TIFF files
    
    band_path = os.path.join(dst_dir, os.path.basename(os.path.splitext(hdf_file)[0]) + '_' + str(file_names[-2]) + '_' +str(file_names[-1]) + ".tif")

    # Create the data for the TIFF (Raster stuff). This includes projections etc
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  band_ds.RasterXSize,
                                                  band_ds.RasterYSize,
                                                  1,  #Number of bands
                                                  gdal.GDT_Int16,
                                                  ['COMPRESS=LZW', 'TILED=YES'])
    out_ds.SetGeoTransform(band_ds.GetGeoTransform())
    out_ds.SetProjection(band_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(band_array)
    out_ds.GetRasterBand(1).SetNoDataValue(-32768)
    
    # Close dataset and save
    out_ds = None  