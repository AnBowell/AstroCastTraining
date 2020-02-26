# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:59:36 2019

@author: Andrew

This module is for plotting the graph. And saving as PDF


The PDF function takes the predicted dates, VCI3M values and the previous values and dates.

The County and errors are also fed in as an input.

"""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mp
from shapely.geometry import Point
import matplotlib.gridspec as gridspec
from datetime import timedelta


def PDF(PredictedTimeStamps3m,PredictedValues3m,Dates3m,VCI3M,eb,county):
    
    
    #------------------- Kenya map and colourbar.-----------------------#

    # The shapefile is read again so the county can be drawn. (Geopandas dataframe)

    df = gpd.read_file('..\CountyShapes\County.shp')
    
    # An zeroed list is created and county VCI3M is also enetered into the DF
    
    VCIS = np.full(47,0)
    for SomeCounter,item in enumerate(df['Name']):
        if item == county:
            CountyNo = SomeCounter
       
    VCIS[int(CountyNo)] = PredictedValues3m[3]
    df['VCI3M'] = VCIS
    
    # The VCI3M bounds are then defined.
    # This is simply used to create a discrete colourmap with our custom colours.
    
    bounds = [0,0.00001, 10, 20, 35,50,100]
    cmap = mp.colors.ListedColormap(['white','r', 'darkorange', 'yellow', 'limegreen','darkgreen'])
    norm = mp.colors.BoundaryNorm(bounds, cmap.N)
    
    # This is some set up for the layout of the PDF.
    # Each axis is a different feature of the plot. The size is defined within GridSpec
    
    fig2 = plt.figure(figsize=(11.69*2,8.27*2))
    spec2 = gridspec.GridSpec(ncols=141, nrows=100, figure=fig2)
    ax1 = fig2.add_subplot(spec2[5:8, 0:60])
    ax2 = fig2.add_subplot(spec2[0:, 0:60])
    ax3 = fig2.add_subplot(spec2[6:18, 0:])
    ax4 = fig2.add_subplot(spec2[5:45,65:])
    ax5 = fig2.add_subplot(spec2[65:85,1:20])
    ax2.axis('off')
    ax3.axis('off')
    ax5.axis('off')
    plt.subplots_adjust(hspace = -.175)
    plt.subplots_adjust(wspace = +1.5)
    

    # In axis 2 the main map of Kenya is created. Using VCI3M our colours are put onto the map.
    # A colourbar is then created to go alongside the map.
    
    ax2=df.plot(ax=ax2,column ='VCI3M',cmap = cmap,norm=norm,legend= False, edgecolor='Black',label= df['Name'])
    mp.colorbar.ColorbarBase(ax1, cmap=cmap,norm=norm,orientation='horizontal')
    
    
    # A title is set for the colourbar as well as the labels being defined (And size changed)
    ax1.set_title('VCI3M Forecast For ' + str(PredictedTimeStamps3m[3]),fontsize=20)
    ax1.tick_params(labelsize=20)
    labels = [item.get_text() for item in ax1.get_xticklabels()]
    labels[0] = 'No Data'
    ax1.set_xticklabels(labels)
    
    
    # The trend is then set. this is just whether or not there is an increase in week 4 compared to 3
    
    if PredictedValues3m[4] > PredictedValues3m[3]:
        ax3.text(0.277,0.45,'Trend = Up',verticalalignment='center', horizontalalignment='right',
           transform=ax3.transAxes, fontsize=22)
    else:
        ax3.text(0.277,0.45,'Trend = Down',verticalalignment='center', horizontalalignment='right',
                 transform=ax3.transAxes, fontsize=22)

        
    #------------------- VCI3M Graph -----------------------#
        
    # The 4th axis plots the past 30 weeks of actual data and then the predicted data is also plotted
    # The data then has the error shaded onto it. 
        
    ax4.fill_between(PredictedTimeStamps3m, PredictedValues3m-eb, PredictedValues3m+eb,lw=3,
                     label='Forecast VCI3M',color='blue',alpha=0.45,zorder=4,interpolate=True)
    ax4.plot(PredictedTimeStamps3m,PredictedValues3m,linestyle = 'solid', lw = 3, color = 'black')
    ax4.plot(np.array(Dates3m,dtype='datetime64[D]'),VCI3M, linestyle = 'solid', lw = 3, color = 'black',label='Known VCI3M')
    ax4.plot([np.max(Dates3m),np.max(Dates3m)],[0,102],linestyle = '--',color = 'black', lw = 3,\
                label = 'Day of last observation')
    ax4.set_xlim(Dates3m[-30],PredictedTimeStamps3m[-1]+timedelta(days=7))
    ax4.set_ylim(0,102)
    
    
    
    # Shading the background based on where the VCI3M is
    
    ax4.axhspan(0, 10, alpha=0.5, color='r')
    ax4.axhspan(10, 20, alpha=0.5, color='darkorange')
    ax4.axhspan(20, 35, alpha=0.5, color='yellow')
    ax4.axhspan(35, 50, alpha=0.5, color='limegreen')
    ax4.axhspan(50, 102, alpha=0.5, color='darkgreen')
    ax4.set_title(str(county)+' VCI3M',fontsize=20)
           
    
    ax4.legend()
    

    
    #--------------------Title and table---------------------#
    
    # Sets the title for the PDF as well as background colour
    fig2.suptitle(str(county)+" Vegetation Outlook", fontsize=24)
    fig2.subplots_adjust(top=0.95)
    fig2.patch.set_facecolor('lightblue')
    
    
    
    
   # A simple table is also added. This uses our custom colourmap created above and fills in our VCI3M values.
    
    
    TableList = [np.round(PredictedValues3m,1)]
    RowLabels = ['VCI3M']
    ax4.table(cellText=TableList,colLabels = PredictedTimeStamps3m,
              rowLabels =RowLabels,bbox=[0.0,-0.5,1,.28],fontsize=30,cellColours=cmap(norm(TableList)))
    
    plt.subplots_adjust(left=0.15, bottom=0.005, right=0.93, top=0.95, wspace=0, hspace=0)
    
    
    
    #---------------- Adding Astrocast logo and saving---------------#
    img = plt.imread('../AC_logo.png')
    ax5.imshow(img)
    fig2.text(0.577,0.26, 'Please find our weekly forecasts at the link below \n \n       https://tinyurl.com/AstroCastForecasts',fontsize=18)
    plt.savefig('..\Forecasts\Forecast for '+str(county)+' dated' +str(PredictedTimeStamps3m[0])+'.pdf',dpi = 400,facecolor=fig2.get_facecolor())
    plt.show()
    
    

    
    
    
    
    
    
    