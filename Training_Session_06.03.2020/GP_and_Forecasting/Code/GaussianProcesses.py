# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:32:54 2019

@author: Andrew

INPUT

Module that takes and input of two numpy arrays. 

X : Days since the first measurement. Eg (0,7,14). 
Y : VCI Values. Eg (10.1,20.3,34.5).

PROCESS

Using an RBF kernel GP is performed on the time series creating a distribution at each time step.

This is then use to forecast values at the next 10 weeks.

OUTPUT 

Returns two numpy arrays. 

Mean : Days since first measurement + Additional forecasted days

Xtest_use : VCI Values inputted + Additional forecasted values

"""

#Importing modules used


import numpy as np

# Pyro has been used in this instance. It is a powerful machine learning tool. 

import torch
import pyro
import pyro.contrib.gp as gp
from pyro.optim import Adam
from pyro.infer import SVI, Trace_ELBO




torch.set_default_tensor_type(torch.DoubleTensor)
torch.set_default_dtype(torch.double)

# The main forecast function

def forecast(X,y):
    
    # Creating the RBF kernel with the desired lengthscale and variance using pyro.
    
    k1 = gp.kernels.RBF(input_dim=2, lengthscale=torch.tensor(50.0),\
                   variance = torch.tensor(0.5))
    pyro.enable_validation(True)       
    optim = Adam({"lr": 0.01}) 
    pyro.clear_param_store()
    
    # Creating an array with the last value entered and the 7 weeks ahead (in days).
    
    plus_arr = np.max(X)+np.array([7.,14.,21.,28.,35.,42.,49.,56.,63.,70.])
    
    # Changing numpy arrays into pytorch tensors (Faster for machine learning).

    X2 = (torch.from_numpy(X))
    y2 = (torch.from_numpy(y-np.mean(y)))
    
    # Adding the new prediction dates into the array and then transforming into pytorch tensor.
    
    Xtest_use = np.append(X,plus_arr)
    Xtest_use2 = (torch.from_numpy(Xtest_use))


    # Running the GP RBF kernel model on the known data
    
    gpr = gp.models.GPRegression(X2, y2,k1, noise=torch.tensor(0.01))
    
    # Stochastic variational inference to optimise the loss function
    # Esentially minimising the errors on the model

    svi = SVI(gpr.model, gpr.guide, optim, loss=Trace_ELBO())
    losses = []
    
    # Choosing how many times to iterate over the optimisiation

    num_steps = 10

    for k in range(num_steps):
        losses.append(svi.step())

    # Putting the results into numpy arrays to be outputted.

    with torch.no_grad():
      if type(gpr) == gp.models.VariationalSparseGP:
        mean, cov = gpr(Xtest_use2, full_cov=True)
      else:
        mean, cov = gpr(Xtest_use2, full_cov=False, noiseless=False) 

    mean = mean.detach().numpy()+np.mean(y)
    
    return mean, Xtest_use 
