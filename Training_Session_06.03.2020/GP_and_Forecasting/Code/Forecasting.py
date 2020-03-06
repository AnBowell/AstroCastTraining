# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:30:33 2019

@author: Andrew

This function is the mediator between the main body of code and the GP code.


INPUT

Three numpy arrays of daily frequency.

Dates : Dates of data points E.g. (12-12-12,13-12-12) 
VCI1W : The 7-Day VCI average (10.4,15.4)
VCI3M : The 3-Month VCI Average (30.3,40.6)

PROCESS
Converts input dates into single figure days since values then runs the GP function. 
Once output from GP function has been recieved, it converts days since back to dates.

OUTPUT

Four numpy arrays of weekly frequency.

PredictedTimeStamps : Dates of predicted data points E.g. (14-12-12,21-12-12)
Dates : Dates of all previous data E.g.(12-12-12,13-12-12)
VCI3M : Previous VCI3M values E.g. (30.3,40.6)
PredictedVCI3M : Predicted VCI3M at weekly intervals E.g. (45.5,46.3)

"""

#Importing modules

import numpy as np
import julian
from datetime import datetime,timedelta

# Importing the bespoke GP module

import GaussianProcesses

#~~~~~~~~~~~~~~~~~~~~~Forecasting code using GP for VCI~~~~~~~~~~~~~~~~~~~~~~#

def GetForecastVCI(Dates,VCI1W,VCI3M):
    
       
    # Computational speed up. Removing start data so that we can divide by 7.
    
    ToRemove = (len(VCI1W) % 7)
    
    # We now take every 7th value, essentially taking weekly data points
    
    VCI1W,VCI3M,Dates = VCI1W[ToRemove-1:][::7],VCI3M[ToRemove-1:][::7],Dates[ToRemove-1:][::7]
    
    # Take the last 3 months of VCI1W so VCI3M can be computed
    
    PastVCI = VCI1W[-14:-1]
 

    # Empty list for day numbers since 2000 to be stored in
    
    Days = []

    # This function here takes a date and turns it into a day since 2000
    
    for item in Dates:
        
        Newitem = item.split('-')[2]
        Year = Newitem.split('20')[1]
        if Newitem == '2020':
            Year = int(20)
        day_of_year = datetime.strptime(item, '%d-%m-%Y').timetuple().tm_yday
        Days.append((int(day_of_year+(int(Year)*(365.25)))))

    # The list of days is then turned into an array, and any nan values from VCI removed.
    VCI = VCI1W
    Days = np.array(Days)
    Mask = np.isnan(VCI1W)
    VCI = VCI[~Mask]
    
    # The data is then fed into the GP module
    
    mean,Xtest_use = GaussianProcesses.forecast(Days,VCI)
    
    # The output of the module is then seperated into past and future data.
    
    use = Xtest_use >= np.max(Days)
    fc = Xtest_use - np.max(Days)
    
    use = fc > 0
    fc = fc[use]
    
    PredictedDates = Xtest_use[use]
    PredictedValues= mean[use]
    
    
    # The last value from the known VCI is then entered into the predicton (Easier to plot later)
    PredictedDates=np.insert(PredictedDates,0,Days[-1])
    PredictedVCI=np.insert(PredictedValues,0,VCI[-1])

    # The predicted days ahead are then converted back into dates.
    # Two chunks of code. One for the predicted time stamps, one for rest of the previous data

    PredictedTimeStamps = []
    for PredictedTimeStamp in PredictedDates:
        mjd =51543+PredictedTimeStamp 
        dt = julian.from_jd(mjd, fmt='mjd')
        PredictedTimeStamps.append(dt.date())
        
        
    Dates = []

    for Day in Days:
        mjd =51543+Day
        dt = julian.from_jd(mjd, fmt='mjd')
        Dates.append(dt)
        
    # Empty array made to store the VCI3M in    
    VCI3MfromVCI1W = np.empty((11))
    
    # The following loops over the weeks of known VCI1W data and our predicted VCI1W data to create
    # A VCI3M running average.

    for WeekCounter,item in enumerate(PredictedVCI):
    
        if WeekCounter < 14:
            NewVCI3M = np.append(PastVCI[WeekCounter:-1], PredictedVCI[:WeekCounter+1])
            VCI3MfromVCI1W[WeekCounter] = np.mean(NewVCI3M)
        else:
            NewVCI3M = np.append(PastVCI[WeekCounter:-1], PredictedVCI[WeekCounter-13:WeekCounter+1])
            VCI3MfromVCI1W[WeekCounter] = np.mean(NewVCI3M)



    # Slight correction due to averging
            
    PredictedVCI3M = VCI3MfromVCI1W-(VCI3MfromVCI1W[0]-VCI3M[-1])    
        
        
        

    return PredictedTimeStamps,Dates,VCI3M,PredictedVCI3M


        
