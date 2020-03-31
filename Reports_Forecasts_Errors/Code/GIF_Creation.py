# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:37:55 2019

@author: Andrew
"""

import matplotlib.pyplot as plt

import geopandas as gpd
import matplotlib.gridspec as gridspec
import moviepy.editor
from glob import glob
import matplotlib as mp
import numpy as np
 



def CreateGIF(ForecastArray):
    
    image_list = []
    
    for i in range(0,11):
        
        df = gpd.read_file('..\CountyShapes\County.shp')
        
        za_points = df.copy()
        df['Name'] = df['Name'].str.replace(" ","")
        
        
        df['VCI3M'] = np.array(ForecastArray[:,1,i],dtype=float)
        
        
        bounds = [0,0.0001, 10, 20, 35,50,100]
        fig2 = plt.figure(figsize=(16,24))
        cmap = mp.colors.ListedColormap(['white','r', 'darkorange', 'yellow', 'limegreen','darkgreen'])
        spec2 = gridspec.GridSpec(ncols=15, nrows=15, figure=fig2)
        norm = mp.colors.BoundaryNorm(bounds, cmap.N)
        ax1 = fig2.add_subplot(spec2[0, :])
        ax2 = fig2.add_subplot(spec2[0:, 0:12])
        ax3 = fig2.add_subplot(spec2[3:5, 14])
        ax2.axis('off')
        ax3.axis('off')
    
        plt.subplots_adjust(hspace = -.175)
        plt.subplots_adjust(wspace = +1.5)
    
        ax2=df.plot(ax=ax2,column ='VCI3M',cmap = cmap,norm=norm,legend= False, edgecolor='Black',label= df['Name'])
        
        mp.colorbar.ColorbarBase(ax1, cmap=cmap,norm=norm,orientation='horizontal')
        
        
        ax1.set_title('VCI3M for week commencing ' + str(ForecastArray[0,0,i]),fontsize=20)
        ax1.tick_params(labelsize=20)
    
        labels = [item.get_text() for item in ax1.get_xticklabels()]
        labels[0] = 'No Data'
    
        ax1.set_xticklabels(labels)
  
        
        df['geometry'] = df.buffer(0.01)
        df["center"] = df["geometry"].representative_point()
        za_points = df.copy()
        za_points['ID'] = za_points['ID'].astype(int)
        za_points.set_geometry("center", inplace = True)
        texts = []
        fig2.patch.set_facecolor('lightblue')
        
        
        for x, y, label in zip(za_points.geometry.x, za_points.geometry.y, za_points['ID']):
            texts.append(ax2.text(x-0.1, y-0.06, label, fontsize = 12,color='black'))
    
        for x,(name,ID) in enumerate(zip(za_points['Name'],za_points['ID'])):
            ax3.text(0.1,1-((x*4.75)/49),str(ID)+'.'+name,verticalalignment='center', horizontalalignment='right',
                   transform=ax3.transAxes, fontsize=15)
            
      
        
        
            
        plt.savefig('..\GIF\\GIF_Images\\'+str(i)+'Dated' + str(ForecastArray[0,0,i]) + '.png',facecolor=fig2.get_facecolor(),dpi = 300)
        plt.show()
        image_list.append('..\GIF\\GIF_Images\\'+str(i)+'Dated' + str(ForecastArray[0,0,i]) + '.png')
        
  
    
    
    my_clip = moviepy.editor.ImageSequenceClip(image_list, fps=1.5)
    my_clip.write_gif("..\GIF\\10WeekForecast Dated" +str(ForecastArray[0,0,0]) + ".gif")
    










