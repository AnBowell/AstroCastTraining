from datetime import datetime,timedelta
from numpy import load
from glob import glob
from numpy import column_stack
from shutil import rmtree
import os
from os import mkdir
import numpy as np
import pandas as pd

current_dir = os.getcwd()
# os.mkdir(current_dir + 'VCIFiles')
#~~~~~~~~~~~~~~~~~~~~~Create new VCI1W and VCI3M time series~~~~~~~~~~~~~~~~~~~~~~#
def CalcVCI(NewNDVIArray):        
    for CountyCounter,County in enumerate(NewNDVIArray):

        NDVI = np.array(County[1],dtype=float)

        VCI = 100*((NDVI-np.nanmin(NDVI[:6880]))/(np.nanmax(NDVI[:6880])-np.nanmin(NDVI[:6880])))
       # VCI = 100*((NDVI-np.nanmin(NDVI))/(np.nanmax(NDVI)-np.nanmin(NDVI)))


        # Put into dataframe to obtain monthly averages
        Data = {'Dates' : pd.to_datetime(County[0],dayfirst=True),'VCI':VCI}

        VCIStuff = pd.DataFrame(data=Data)
        VCIStuff.index = VCIStuff['Dates']

        VCIStuff = VCIStuff.sort_index()

        VCI3M = VCIStuff['VCI'].rolling('91D').mean().ffill()
        VCI1W = VCIStuff['VCI'].rolling('7D').mean().ffill()


        VCI3M = np.array(VCI3M).reshape(len(VCI3M))
        VCI1W = np.array(VCI1W).reshape(len(VCI1W))


        # Save the Data #
        NewNDVIArray[CountyCounter,2] = VCI1W
        NewNDVIArray[CountyCounter,3] = VCI3M

        print(str(CountyCounter+1),'out of 47 done')


    #~~~~~~~~~~~~~ Saving compressed numpy file with all output info for counties~~~~~#

    np.savez(current_dir + 'VCIFiles',
             Mombasa =NewNDVIArray[ 0 ],
             Kwale =NewNDVIArray[ 1 ],
             Kilifi =NewNDVIArray[ 2 ],
             TanaRiver =NewNDVIArray[ 3 ],
             Lamu =NewNDVIArray[ 4 ],
             TaitaTaveta =NewNDVIArray[ 5 ],
             Garissa =NewNDVIArray[ 6 ],
             Wajir =NewNDVIArray[ 7 ],
             Mandera =NewNDVIArray[ 8 ],
             Marsabit =NewNDVIArray[ 9 ],
             Isiolo =NewNDVIArray[ 10 ],
             Meru =NewNDVIArray[ 11 ],
             TharakaNithi =NewNDVIArray[ 12 ],
             Embu =NewNDVIArray[ 13 ],
             Kitui =NewNDVIArray[ 14 ],
             Machakos =NewNDVIArray[ 15 ],
             Makueni =NewNDVIArray[ 16 ],
             Nyandarua =NewNDVIArray[ 17 ],
             Nyeri =NewNDVIArray[ 18 ],
             Kirinyaga =NewNDVIArray[ 19 ],
             Muranga =NewNDVIArray[ 20 ],
             Kiambu =NewNDVIArray[ 21 ],
             Turkana =NewNDVIArray[ 22 ],
             WestPokot =NewNDVIArray[ 23 ],
             Samburu =NewNDVIArray[ 24 ],
             TransNzoia =NewNDVIArray[ 25 ],
             UasinGishu =NewNDVIArray[ 26 ],
             ElgeyoMarakwet =NewNDVIArray[ 27 ],
             Nandi =NewNDVIArray[ 28 ],
             Baringo =NewNDVIArray[ 29 ],
             Laikipia =NewNDVIArray[ 30 ],
             Nakuru =NewNDVIArray[ 31 ],
             Narok =NewNDVIArray[ 32 ],
             Kajiado =NewNDVIArray[ 33 ],
             Kericho =NewNDVIArray[ 34 ],
             Bomet =NewNDVIArray[ 35 ],
             Kakamega =NewNDVIArray[ 36 ],
             Vihiga =NewNDVIArray[ 37 ],
             Bungoma =NewNDVIArray[ 38 ],
             Busia =NewNDVIArray[ 39 ],
             Siaya =NewNDVIArray[ 40 ],
             Kisumu =NewNDVIArray[ 41 ],
             HomaBay =NewNDVIArray[ 42 ],
             Migori =NewNDVIArray[ 43 ],
             Kisii =NewNDVIArray[ 44 ],
             Nyamira =NewNDVIArray[ 45 ],
             Nairobi=NewNDVIArray[ 46 ]
             )
