# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:18:10 2019

@author: Andrew

This is a function to download the Raw Modis Data

Function takes in two dates both in string format YYYY-MM-DD
"""


# Importing the specific functions from each module for speed.
import os
current_dir = os.getcwd()
from pymodis.downmodis import downModis


#~~~~~~~~~~~Create function to download raw data~~~~~~~~~~~~~~~#


def DownLoadData(LastKnownDate,CurrentDate):
    # Set the destination folder

    dest = current_dir + '/RawData'

    # These are four tiles that cover Kenya

    tiles = 'h21v08,h21v09,h22v08,h22v09'

    # Using the Pymodis module to download the 4 tiles from the server

    Modis_Down =downModis(destinationFolder=dest,tiles=tiles,url='https://e4ftl01.cr.usgs.gov',
                                             path='MOTA',
                                             product='MCD43A4.006',user='abowell',password='Astrocast1',today=CurrentDate,
                                             enddate=LastKnownDate)

    Modis_Down.connect()
    Modis_Down.downloadsAllDay()
