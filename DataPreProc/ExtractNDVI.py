# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:53:00 2019

@author: Andrew

This module will cut out data from each county and then produce NDVI.

This will then be added to the current NDVI.

"""

# Importing modules
import os
from datetime import datetime,timedelta
import rasterio
from rasterio.mask import mask
import numpy as np
import json
import geopandas as gpd

current_dir = os.getcwd()

# Simple function to convert from MODIS' day of the year to an actual date

def serial_date_to_string(year,srl_no):
    new_date = datetime(int(year),1,1,0,0) + timedelta(int(srl_no) - 1)
    return new_date.strftime("%d-%m-%Y")

# Function from Eddie's code. Take the shapefiles and convert to how rasterio wants them
    
def getFeatures(gdf):
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


#~~~~~~~~~~~~~~NDVI FUNCTION~~~~~~~~~~~~~~~~~#

def NDVIProduction(RedImage,NIRImage,REDmask,NIRmask):
   
    #Take date from image title
    
    Date = RedImage.split('_')[-4].split('A')[-1]
    Date = serial_date_to_string(Date[0:4],Date[4:])
    print(Date)

    # Open all 4 bands of the same image
    
    NIR=rasterio.open(NIRImage)
    RED= rasterio.open(RedImage)
    NIRMASK=rasterio.open(NIRmask)
    REDMASK= rasterio.open(REDmask)  
    
    # Read in shapefiles for all counties using geopandas. Use MODIS projectio too
    
    geom = gpd.read_file(current_dir+'/CountyShapes/county.shp')
    geom = geom.to_crs(crs=NIR.crs.data)
    
    #Create an empty array for date, NDVI, Amount of pixels and Standard deviation of the pixels to be saved to.
    TempArray = np.empty((47,6),dtype=object)
    
    
    # for loop to go through all shapefiles.
    
    for i in range(1,48):

        # Using Eddie's function to grab features of shapefiles.
        
        County = geom[geom['ID']==i].Name.values[0]
        
        cord1=getFeatures(geom[geom['ID']==i])

        # Creating the NIR and RED images for each county. Cropped using shapefiles.
        NIROut,TransformOutNIR=mask(NIR,cord1,crop=True)
        REDOut,TransformOutRED=mask(RED,cord1,crop=True)
        
        # Do the same thing, but this time for quality masks.
        
        Final_Red_Mask,masks=mask(REDMASK,cord1,crop=True)
        Final_NIR_Mask,masks=mask(NIRMASK,cord1,crop=True)
        
        
        # Convert images and masks to numpy arrays. Take relevant data. 
        # 0 For top quality, 1 for middling quality and everything else is masked out.
        
        Final_Red_Mask1 = np.ma.array(Final_Red_Mask) 
        Final_Red_Mask = np.ma.array(np.where(Final_Red_Mask1 ==1, 0, Final_Red_Mask1))


            
        Final_NIR_Mask1 = np.ma.array(Final_NIR_Mask)
        Final_NIR_Mask = np.ma.array(np.where(Final_NIR_Mask1==1, 0, Final_NIR_Mask1))
    

        
        # The final arrays are then outputted.
        
        NIRFinal = np.ma.array(NIROut,mask=Final_NIR_Mask)
        REDFinal = np.ma.array(REDOut,mask=Final_Red_Mask)
        
        # Before using these to create our timeseries we check to see if we have over 1% of the data
        
        if Final_Red_Mask.count() < Final_Red_Mask1.count()/100:
            NIRFinal = np.nan
            REDFinal = np.nan
            
        
        if Final_NIR_Mask.count() < Final_NIR_Mask1.count()/100:
            NIRFinal = np.nan
            REDFinal = np.nan
        
        
        # Calculate the NDVI from the masked RED and NIR images
        
        NDVI = (NIRFinal-REDFinal)/(NIRFinal+REDFinal)
        
        # Save the Date, NDVI, pixel count and standard deviation to numpy array.
        
        TempArray[i-1,0] =  i
        TempArray[i-1,1] =  County
        TempArray[i-1,2] =  Date
        TempArray[i-1,3] =  np.ma.mean(NDVI)
        TempArray[i-1,4] =  NDVI.count()
        TempArray[i-1,5] =  np.std(NDVI)
    
    # Return the final array
    return TempArray[:,0],TempArray[:,1],TempArray[:,2],TempArray[:,3],TempArray[:,4],TempArray[:,5]
