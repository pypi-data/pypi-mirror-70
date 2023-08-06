# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 13:28:19 2018

@author: alex
"""
# Array math
import numpy as np
#Citation: Uncertainties: a Python package for calculations with uncertainties,
#    Eric O. LEBIGOT, http://pythonhosted.org/uncertainties/
from uncertainties import unumpy as unp
# Nonlinear fitting
import lmfit
from lmfit import Minimizer, Parameters, report_fit
print(lmfit.__version__)
import emcee
print(emcee.__version__)
# Plotting
import permittivitycalc as pc
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import corner
import os
import datetime
import warnings
            

# GLOBAL VARIABLES
E_0 = 8.854187817620*10**-12 #Permittivity of vacuum (F/m) 
U_0 = 4*np.pi*10**-7 #Permeability of vacuum (V*s/A*m) 
C = (1)*1/np.sqrt(E_0*U_0) #Speed of light (m/s)
LAM_C = float('inf') #Cut-off wavelength = infinity


class AirlineIter():
    """
    Iterative fit to measured S-parameters using a Cole-Cole model. Can fit 
    both 2-port and 2-port + shorted measurements. A flat model can also be 
    used for samples with no measurable frequency dispersion.
        
    To determine an initial guess for the fit, first fit a Cole-Cole
    model to analytical results: either New Non-iterative, NRW, or both. This 
    provides an initial guess for the Cole-Cole model parameters. Then use the 
    emcee package with lmfit to perform a Bayesian fit to the S-Parameters. 
    This finds the Cole-Cole model which produces the best fit model 
    S-parameters.  
        
    Parameters
    ----------
    data_instance : permittivitycalc.AirlineData 
        AirlineData class instance  containing raw S-parameters to be 
        iterated over. If data_instance contains corrected data, it will be 
        automatically used.
        
    trial_run : bool
        If True only fit Cole-Cole model to analytical results and plot the 
        results. Useful for determining the number of poles to be used
        in the Cole-Cole model before perfoming the more time consuming
        final fit to the S-parameters (Default: True).
            
    number_of_poles : int
        Number of poles to be used in the Cole-Cole model for epsilon. When
        number_of_poles is 0, a flat model will be used instead of a Cole-Cole
        model (epsilon* = epsilon_real - 1j*epsilon_imag) (Default: 1).
        
    fit_mu : bool
        If True, fit both permittivity and permeability (Default: False).
        
    number_of_poles_mu : int
        Number of poles to be used in the Cole-Cole model for mu. When
        number_of_poles_mu is 0, a flat model will be used instead of a 
        Cole-Cole model (mu* = mu_real - 1j*mu_imag) (Default: 1).
        
    fit_conductivity : bool
        If True, include a seperate real conductivity term in the Cole-Cole 
        model for epsilon. Can be ignored for materials with very low 
        conductivity (Default: False).
        
    number_of_fits : int
        Number of default emcee fits to perform beofre final fit. Subsequent 
        fits will use the results from the pervious iteration as initial 
        values. Generally, using more steps is preferable to initializing a 
        new fit (Default: 1).
        
    start_freq : float or int, optional
        Start frequency in Hz for iteration. If None, will use the starting 
        frequency of the data instance (Default: None).
    
    end_freq : float or int, optional
        End frequency in Hz for iteration (Default: None).
        
    initial_parameters : dict, optional
        A dictionary containing custom initial values for the iteration. 
        Default values will be automatically generated if none are provided.
        The dictionary must contain initial values for all parameters in the
        iteration and each parameter much have the exact name as the ones used
        in the iteration. See documnetation for the _colecole and 
        _iteration_parameters for parameter naming conventions.
        
    nsteps : int, optional
        Number of steps to be used by emcee for iteration when trial_run is 
        False. See lmfit and emcee documentation for details (Default: 1000).
        
    nwalkwers: int, optional
        Number of walkers to be used by emcee for iteration when trial_run is 
        False. See lmfit and emcee documentation for details (Default: 100).
        
    nburn : int, optional
        Number of steps for burn-in phase to be used by emcee for iteration 
        when trial_run is False. See lmfit and emcee documentation for details 
        (Default: 500).
        
    nthin : int, optional
        Only accept every nthin samples in emcee for iteration when trial_run 
        is False. See lmfit and emcee documentation for details (Default: 1).
        
    nworkers : int or pool, optional
        Number of workers or pool object for paralelization (Default: 1).
        
    epsilon_iter : array
        Complex array containing the results of the iterrative fit for epsilon.
        trail_run must be set to False.
        
    mu_iter : array
        Complex array containing the results of the iterative fit for mu.
        trial_run must be set to False and fit_mu must be set to True.
        
    param_results : dict
        Model parameters for epsilon and mu (if fit_mu is True).
        
    lmfit_results : lmfit.minimizer.MinimizerResult object
        Results from lmfit. See lmfit documentation.
        
    publish : bool, optional
        If True save figure as .eps file. Default: False.
        
    name : str, optional
        Required when publish=True. Used in file name of saved figure. 
        
    """
    def __init__(self,data_instance,trial_run=True,number_of_poles=1,\
                 fit_mu=False,number_of_poles_mu=1,fit_conductivity=False,\
                 number_of_fits=1,start_freq=None,end_freq=None,\
                 initial_parameters=None,nsteps=1000,nwalkers=100,nburn=500,\
                 nthin=1,nworkers=1,publish=False,name=None):
        self.meas = data_instance
        # Get s params (corrected if they exist)
        if self.meas.corr:
            self.s11 = self.meas.corr_s11
            self.s21 = self.meas.corr_s21
            self.s22 = self.meas.corr_s22
            self.s12 = self.meas.corr_s12
            print('Using corrected S-Parameter data.')
        else:
            self.s11 = self.meas.s11
#            print(self.s11)
            self.s21 = self.meas.s21
            self.s22 = self.meas.s22
            self.s12 = self.meas.s12
        # Check if shorted
        if self.meas.shorted:
            self.shorted = True
            self.s11_short = self.meas.s11_short
            print('Using shorted data.')
        else:
            self.shorted = False
        # Get permittivity data
        self.freq = self.meas.freq
        if self.meas.corr:
            self.avg_dielec = self.meas.corr_avg_dielec
            self.avg_lossfac = self.meas.corr_avg_lossfac
            self.avg_losstan = self.meas.corr_avg_losstan
        else:
            self.avg_dielec = self.meas.avg_dielec
            self.avg_lossfac = self.meas.avg_lossfac
            self.avg_losstan = self.meas.avg_losstan
        if self.meas.nrw:
            if self.meas.corr:
                self.avg_mu_real = self.meas.corr_avg_mu_real
                self.avg_mu_imag = self.meas.corr_avg_mu_imag
            else:
                self.avg_mu_real = self.meas.avg_mu_real
                self.avg_mu_imag = self.meas.avg_mu_imag
        self.trial = trial_run
        # self.water_pole = water_pole
        self.fit_mu = fit_mu
        self.fit_sigma = fit_conductivity
        self.poles = number_of_poles
        self.poles_mu = number_of_poles_mu
        self.fits = number_of_fits
        if start_freq:
            self.start_freq = start_freq
        else:
            self.start_freq = self.meas.freq_cutoff
        self.end_freq = end_freq
        self.initial_parameters = initial_parameters
        self.nsteps = nsteps
        self.nwalkers = nwalkers
        self.nburn = nburn
        self.nthin = nthin
        self.nworkers = nworkers
        self.publish = publish
        self.name = name
        
        # Data cutoff
        if self.end_freq:
            self.s11 = np.array((self.s11[0][self.freq<=self.end_freq],self.s11[1][self.freq<=self.end_freq]))
            self.s21 = np.array((self.s21[0][self.freq<=self.end_freq],self.s21[1][self.freq<=self.end_freq]))
            self.s22 = np.array((self.s22[0][self.freq<=self.end_freq],self.s22[1][self.freq<=self.end_freq]))
            self.s12 = np.array((self.s12[0][self.freq<=self.end_freq],self.s12[1][self.freq<=self.end_freq]))
            self.avg_dielec = self.avg_dielec[self.freq<=self.end_freq]
            self.avg_lossfac = self.avg_lossfac[self.freq<=self.end_freq]
            self.avg_losstan = self.avg_losstan[self.freq<=self.end_freq]
            if self.meas.nrw:
                self.avg_mu_real = self.avg_mu_real[self.freq<=self.end_freq]
                self.avg_mu_imag = self.avg_mu_imag[self.freq<=self.end_freq]
            if self.shorted:
                self.s11_short = np.array((self.s11_short[0][self.freq<=self.end_freq],self.s11_short[1][self.freq<=self.end_freq]))
            self.freq = self.freq[self.freq<=self.end_freq]
        
        # Calc real and imag unc
        #calc real and imag s-params
        self.s11r = (self.s11[0]*unp.cos(unp.radians(self.s11[1])))[self.freq>=self.start_freq]
        self.s11i = (self.s11[0]*unp.sin(unp.radians(self.s11[1])))[self.freq>=self.start_freq]
        self.s22r = (self.s22[0]*unp.cos(unp.radians(self.s22[1])))[self.freq>=self.start_freq]
        self.s22i = (self.s22[0]*unp.sin(unp.radians(self.s22[1])))[self.freq>=self.start_freq]
        self.s21r = (self.s21[0]*unp.cos(unp.radians(self.s21[1])))[self.freq>=self.start_freq]
        self.s21i = (self.s21[0]*unp.sin(unp.radians(self.s21[1])))[self.freq>=self.start_freq]
        self.s12r = (self.s12[0]*unp.cos(unp.radians(self.s12[1])))[self.freq>=self.start_freq]
        self.s12i = (self.s12[0]*unp.sin(unp.radians(self.s12[1])))[self.freq>=self.start_freq]
        #calc diff
        self.diff_sRr = np.abs(unp.nominal_values(self.s11r) - unp.nominal_values(self.s22r))
        self.diff_sRi = np.abs(unp.nominal_values(self.s11i) - unp.nominal_values(self.s22i))
        self.diff_sTr = np.abs(unp.nominal_values(self.s21r) - unp.nominal_values(self.s12r))
        self.diff_sTi = np.abs(unp.nominal_values(self.s21i) - unp.nominal_values(self.s12i))
        if self.shorted:
            self.s11r_unc = unp.std_devs(self.s11_short[0]*unp.cos(unp.radians(self.s11_short[1])))[self.freq>=self.start_freq]
            self.s11i_unc = unp.std_devs(self.s11_short[0]*unp.sin(unp.radians(self.s11_short[1])))[self.freq>=self.start_freq]
        else:
            self.s11r_unc = unp.std_devs(self.s11r)
            self.s11i_unc = unp.std_devs(self.s11i)
        self.s21r_unc = unp.std_devs(self.s21r)
        self.s21i_unc = unp.std_devs(self.s21i)
        self.s22r_unc = unp.std_devs(self.s22r)
        self.s22i_unc = unp.std_devs(self.s22i)
        self.s12r_unc = unp.std_devs(self.s12r)
        self.s12i_unc = unp.std_devs(self.s12i)
        #calc total unc
        self.s11r_unc = np.sqrt(self.s11r_unc**2 + self.diff_sRr**2)
        self.s11i_unc = np.sqrt(self.s11i_unc**2 + self.diff_sRi**2)
        self.s22r_unc = np.sqrt(self.s22r_unc**2 + self.diff_sRr**2)
        self.s22i_unc = np.sqrt(self.s22i_unc**2 + self.diff_sRi**2)
        self.s21r_unc = np.sqrt(self.s21r_unc**2 + self.diff_sTr**2)
        self.s21i_unc = np.sqrt(self.s21i_unc**2 + self.diff_sTi**2)
        self.s12r_unc = np.sqrt(self.s12r_unc**2 + self.diff_sTr**2)
        self.s12i_unc = np.sqrt(self.s12i_unc**2 + self.diff_sTi**2)
        
#        self.s11r_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
#        self.s11i_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
#        self.s22r_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
#        self.s22i_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
#        self.s21r_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
#        self.s21i_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
#        self.s12r_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
#        self.s12i_unc = 0.2*np.ones(len(self.freq[self.freq>=self.start_freq]))
        # Seperate uncertainty
        #unc
        self.s11_unc = unp.std_devs(self.s11)
#        print(self.s11_unc)
        self.s21_unc = unp.std_devs(self.s21)
        self.s22_unc = unp.std_devs(self.s22)
        self.s12_unc = unp.std_devs(self.s12)
        self.avg_dielec_unc = unp.std_devs(self.avg_dielec)
        self.avg_lossfac_unc = unp.std_devs(self.avg_lossfac)
        self.avg_losstan_unc = unp.std_devs(self.avg_losstan)
        #nominal values
        self.s11 = unp.nominal_values(self.s11)
#        print(self.s11)
        self.s21 = unp.nominal_values(self.s21)
        self.s22 = unp.nominal_values(self.s22)
        self.s12 = unp.nominal_values(self.s12)
        self.avg_dielec = unp.nominal_values(self.avg_dielec)
        self.avg_lossfac = unp.nominal_values(self.avg_lossfac)
        self.avg_losstan = unp.nominal_values(self.avg_losstan)
        if self.meas.nrw:
            #unc
            self.avg_mu_real_unc = unp.std_devs(self.avg_mu_real)
            self.avg_mu_imag_unc = unp.std_devs(self.avg_mu_imag)
            #nominal valiues
            self.avg_mu_real = unp.nominal_values(self.avg_mu_real)
            self.avg_mu_imag = unp.nominal_values(self.avg_mu_imag)
        if self.shorted:
            #unc
            self.s11_short_unc = unp.std_devs(self.s11_short)
            #nominal
            self.s11_short = unp.nominal_values(self.s11_short)
            
        # Get mag and phase uncertainties cutoff at start_freq
        if self.shorted:
            self.s11m_unc = self.s11_short_unc[0][self.freq>=self.start_freq]
            self.s11p_unc = np.radians(self.s11_short_unc[1][self.freq>=self.start_freq])
            self.s11p_unc_deg = self.s11_short_unc[1][self.freq>=self.start_freq]
        else:
            self.s11m_unc = self.s11_unc[0][self.freq>=self.start_freq]
            self.s11p_unc = np.radians(self.s11_unc[1][self.freq>=self.start_freq])
            self.s11p_unc_deg = self.s11_unc[1][self.freq>=self.start_freq]
        self.s21m_unc = self.s21_unc[0][self.freq>=self.start_freq]
        self.s21p_unc = np.radians(self.s21_unc[1][self.freq>=self.start_freq])
        self.s21p_unc_deg = self.s21_unc[1][self.freq>=self.start_freq]
        self.s22m_unc = self.s22_unc[0][self.freq>=self.start_freq]
        self.s22p_unc = np.radians(self.s22_unc[1][self.freq>=self.start_freq])
        self.s22p_unc_deg = self.s22_unc[1][self.freq>=self.start_freq]
        self.s12m_unc = self.s12_unc[0][self.freq>=self.start_freq]
        self.s12p_unc = np.radians(self.s12_unc[1][self.freq>=self.start_freq])
        self.s12p_unc_deg = self.s12_unc[1][self.freq>=self.start_freq]
        
        if self.trial:
            self._permittivity_iterate()
        elif self.fit_mu:
            self.epsilon_iter, self.mu_iter, self.param_results, self.lmfit_results = self._permittivity_iterate()
        else:
            self.epsilon_iter, self.param_results, self.lmfit_results = self._permittivity_iterate()
        if not self.trial:
            print('Reduced Chi Squared: ' + str(self.red_chi_sq))
            print('Bayesian Information Criterion: ' + str(self.bic))
            
    def _colecole(self,number_of_poles,freq,v,mu=False):
        """
        Unpack Cole-Cole paramaterd and retuns Cole-Cole model based on 
        number of poles.
        
        Parameters
        ----------
        number_of_poles : int 
            Number of poles in the Cole-Cole model 
            
        freq : numpy array 
            Frequency vector for model
        
        v : dict 
            Cole-Cole parameters to be used in model. v must be a dictionary 
            with the following values:
                - k_inf
                - sigma
                - k_dc_n
                - tau_n
                - alpha_n
            
            Where n is the pole number in the Cole-Cole model from 1 to inf.
                
        mu : bool
            If True use mu parameters in v:
                - mu_inf
                - mu_dc_n
                - mutau_n
                - mualpha_n
            
            Where n is the pole number in the Cole-Cole model from 1 to inf.
                
        Return
        ------
        k : array
            Cole-Cole model.
        """
        if mu:
            if number_of_poles == 0:
                k = (v['mu_real'] - 1j*v['mu_imag'])
                # Make k the length of freq if using 0 poles
                freq_vector = np.ones(len(freq))
                k = k * freq_vector
            else:
                k = (v['mu_inf'])
        elif number_of_poles == 0:
            k = (v['k_real'] - 1j*v['k_imag'])
            # Make k the length of freq if using 0 poles
            freq_vector = np.ones(len(freq))
            k = k * freq_vector
        elif self.fit_sigma:
            k = (v['k_inf']) - 1j*v['sigma']/(2*np.pi*freq*E_0)
        else:
            k = (v['k_inf'])
        
        if number_of_poles != 0:
            for n in range(number_of_poles):
                n+=1    # Start names at 1 intead of 0
                if mu and self.poles_mu != 0:
                    k += (v['mu_dc_{}'.format(n)])/(1 + (1j*2*np.pi*freq*v['mutau_{}'.format(n)])**v['mualpha_{}'.format(n)])
                # elif self.water_pole and n == 1:
                #     k += (v['k_dc_{}'.format(n)])/(1 + (1j*2*np.pi*freq*v['tau_{}'.format(n)]))
                else:
                    k += (v['k_dc_{}'.format(n)])/(1 + (1j*2*np.pi*freq*v['tau_{}'.format(n)])**v['alpha_{}'.format(n)])
        
        return k
    
    def _model_sparams(self,freq,L,epsilon,mu):
        # Calculate predicted sparams
        lam_0 = (C/freq)
        
        small_gam = (1j*2*np.pi/lam_0)*np.sqrt(epsilon*mu - \
                    (lam_0/LAM_C)**2)
        
        small_gam_0 = (1j*2*np.pi/lam_0)*np.sqrt(1- (lam_0/LAM_C)**2)
        
        t = np.exp(-small_gam*L)
        
        big_gam = (small_gam_0*mu - small_gam) / (small_gam_0*mu + \
                  small_gam)
        
        # Use shorted S11 data if present
        if self.shorted:
            # Modified S11
            s11_predicted = big_gam - ( ( (1-big_gam**2)*t**2 ) / (1 - (big_gam*t**2) ) )
        else:
            # Baker-Jarvis S11
            s11_predicted = (big_gam*(1-t**2))/(1-(big_gam**2)*(t**2))
        
        # S21
        s21_predicted = t*(1-big_gam**2) / (1-(big_gam**2)*(t**2))
        
        s12_predicted = s21_predicted
        
        return s11_predicted, s21_predicted, s12_predicted
    
    def _iteration_parameters(self,pole_num,initial_values=None,mu=False):
        """
        Creates Parameter object to be used in _permittivity_iterate
        
        Parameters
        ----------
        number_of_poles : int or list of ints
            Number if poles in the Cole-Cole model.
            
        initial_values : dict (optional)
            Initial guess interation parameters for the Cole-Cole model. If 
                none given, will generate default parameters.
            
            initial_values must be a dictionary with the following values:
                - k_inf
                - sigma
                - k_dc_n
                - tau_n
                - alpha_n
                
                Where n is the pole number in the Cole-Cole model from 1 to inf.
                
            If mu = True then initial_values also must contain:
                - mu_inf
                - mu_dc_n
                - mutau_n
                - mualpha_n
                
        mu : bool
            If True, create seperate parameters for mu (Default: False).
                
        Return
        ------
        params : lmfit.Parameter object
            paramaters for iteration
        """
        if isinstance(pole_num,int):
            pole_num = [pole_num]           
        # Get default initial values if none given
        if not initial_values:
            initial_values = self._default_initial_values(pole_num[0])
            if mu:
                initial_values_mu = self._default_initial_values_mu(pole_num[1])
                initial_values = {**initial_values,**initial_values_mu}
                
        # Flat model if number of poles is 0
        if pole_num[0] == 0:
            eps_flag = True
        else:
            eps_flag = False
        if mu and pole_num[1] == 0:
            mu_flag = True
        else:
            mu_flag = False
        
        # Create parameters
        params = Parameters()
#        params.add('ST_deg_err',value=0.1)
#        params.add('ST_db_err',value=0.01)
#        params.add('ST_del_err',value=1e-12,min=0)
#        params.add('SR_deg_err',value=-0.2)
#        params.add('SR_db_err',value=0.05,min=0)
#        params.add('SR_del_err',value=1e-12,min=0)
        if mu:
            if mu_flag:
                params.add('mu_real',value=initial_values['mu_real'],min=1)
                params.add('mu_imag',value=initial_values['mu_imag'],min=0)
            else:
                params.add('mu_inf',value=initial_values['mu_inf'],min=1)
        if eps_flag:
            params.add('k_real',value=initial_values['k_real'],min=1)
            params.add('k_imag',value=initial_values['k_imag'],min=0)
        else:
            params.add('k_inf',value=initial_values['k_inf'],min=1)
        # if self.water_pole:
        #     params.add('k_w_inf',value=4.9,vary=False) # k_inf for water
        #     params.add('c_w',value=0.9,min=0,max=1) # water pole strength factor
        if self.fit_sigma:
            params.add('sigma',value=initial_values['sigma'],min=0)
        
        if mu:
            if not mu_flag:
                for m in range(pole_num[1]):
                    m+=1
                    params.add('mu_dc_{}'.format(m),value=initial_values['mu_dc_{}'.format(m)],min=0)#,min=1)
                    params.add('mutau_{}'.format(m),value=initial_values['mutau_{}'.format(m)],min=0)
                    params.add('mualpha_{}'.format(m),value=initial_values['mualpha_{}'.format(m)],min=0,max=1)
        if not eps_flag:
            for n in range(pole_num[0]):
                n+=1 # start variable names at 1 instead of 0
                params.add('k_dc_{}'.format(n),value=initial_values['k_dc_{}'.format(n)],min=0)#,min=1)
                params.add('tau_{}'.format(n),value=initial_values['tau_{}'.format(n)],min=0,max=0.001)
                params.add('alpha_{}'.format(n),value=initial_values['alpha_{}'.format(n)],min=0,max=1)
                # if self.water_pole and n == 1:
                #     tau_w = self._calc_water_pole_params()
                #     params.add('tau_{}'.format(n),value=tau_w,vary=False)
                #     params.add('k_dc_{}'.format(n),value=initial_values['k_dc_{}'.format(n)],min=0)#,min=1)
                # else:
                #     params.add('k_dc_{}'.format(n),value=initial_values['k_dc_{}'.format(n)],min=0)#,min=1)
                #     params.add('tau_{}'.format(n),value=initial_values['tau_{}'.format(n)],min=0,max=0.001)
                #     params.add('alpha_{}'.format(n),value=initial_values['alpha_{}'.format(n)],min=0,max=1)
            
        return params
    
    # def _calc_water_pole_params(self):
    #     if not self.meas.temperature:
    #         raise Exception('AirlineData class instance must be given a temperature if using a Debye water pole')
    #     else:
    #         temp = self.meas.temperature
        
    #     tau_w = (1.1109e-10 - 3.824e-12*temp + 6.938e-14*temp**2 - \
    #            5.096e-16*temp**3)/(2*np.pi)
        
    #     return tau_w
    
    def _fix_parameters(self,params,pole_num,unfix=False,mu=False):
        # Check if fixing or unfixing parameters
        fix_bool = unfix
        # Check for flat k
        if pole_num == 0:
            flat_flag = True
        else:
            flat_flag = False
            
        if mu and flat_flag:
            params['mu_real'].vary = fix_bool
            params['mu_imag'].vary = fix_bool
        elif mu:
            params['mu_inf'].vary = fix_bool
            for m in range(pole_num):
                m+=1    #start counting at 1
                params['mu_dc_{}'.format(m)].vary = fix_bool
                params['mutau_{}'.format(m)].vary = fix_bool
                params['mualpha_{}'.format(m)].vary = fix_bool
        elif not mu and flat_flag:
            params['k_real'].vary = fix_bool
            params['k_imag'].vary = fix_bool
        else:
            params['k_inf'].vary = fix_bool
            if self.fit_sigma:
                params['sigma'].vary = fix_bool
            for n in range(pole_num):
                n+=1    #start counting at 1
                params['k_dc_{}'.format(n)].vary = fix_bool
                params['tau_{}'.format(n)].vary = fix_bool
                params['alpha_{}'.format(n)].vary = fix_bool
        
        return params
    
    def _default_initial_values(self,number_of_poles):
        """
        Creates default initial values for iteration parameters
        """
        if number_of_poles == 0:
            initial_values = {'k_real':2.01,'k_imag':0.0001}
        else:
            initial_values = {'k_inf':2.01,'sigma':0.0001}
            for n in range(number_of_poles):
                n+=1 # start variable names at 1 instead of 0
                initial_values['k_dc_{}'.format(n)] = 5/n
                initial_values['tau_{}'.format(n)] = 1e-9 * 10**-(2*(n-1))
                initial_values['alpha_{}'.format(n)] = 0.5
            
        return initial_values
    
    def _default_initial_values_mu(self,number_of_poles):
        """
        Creates default initial values for iteration parameters
        """
        if number_of_poles == 0:
            initial_values = {'mu_real':1.01,'mu_imag':0.0001}
        else:
            initial_values = {'mu_inf':1.001}
            for n in range(number_of_poles):
                n+=1 # start variable names at 1 instead of 0
                initial_values['mu_dc_{}'.format(n)] = 0.001 + 10**(n-1)
                initial_values['mutau_{}'.format(n)] = 1e-9 * 10**-(2*(n-1))
                initial_values['mualpha_{}'.format(n)] = 0.5
            
        return initial_values
    
    def _colecole_residuals(self,params,number_of_poles,freq,k,mu=False):
        """
        Cole-Cole model objective function
        """
        v = params.valuesdict()
        
        if mu:
            k_predicted = self._colecole(number_of_poles,freq,v,mu=True)
        else:
            k_predicted = self._colecole(number_of_poles,freq,v)
        
        # Residuals
        resid1 = k_predicted.real - k.real
        resid2 = k_predicted.imag - k.imag
        
        return np.concatenate((resid1,resid2))
    
    def _iterate_model(self,params,L,freq_0):
        """
        Objective funtion to minimize from modified Baker-Jarvis (NIST) 
            iterative method (Houtz et al. 2016).
        """
        
        freq = self.freq[self.freq>=freq_0]
        L = L/100 #L in m

        # Unpack parameters
        v = params.valuesdict()
        
        # Calculate predicted mu and epsilon
        if self.fit_mu:    #check if fitting mu
            mu = self._colecole(self.poles_mu,freq,v,mu=True)
        else:   #set mu=1 if not fitting mu
            mu = 1
        epsilon = self._colecole(self.poles,freq,v)
        
        s11_predicted, s21_predicted, s12_predicted = self._model_sparams(freq,L,epsilon,mu)
        
#        degree_omegas = 360*freq
#        S12_magnitude = np.abs(s12_predicted)*10**(v['ST_db_err']/20)
#        S12_phase = np.angle(s12_predicted,deg=True) + v['ST_deg_err'] #+ degree_omegas*v['ST_del_err']  
#        S11_magnitude = np.abs(s11_predicted)#*10**(v['SR_db_err']/20)
#        S11_phase = np.angle(s11_predicted,deg=True)# + v['SR_deg_err'] #+ degree_omegas*v['SR_del_err']
#        S21_magnitude = np.abs(s21_predicted)*10**(v['ST_db_err']/20)
#        S21_phase = np.angle(s21_predicted,deg=True) + v['ST_deg_err'] #+ degree_omegas*v['ST_del_err']
#        
#        s21_predicted = 1j*S21_magnitude*np.sin(np.radians(S21_phase));
#        s21_predicted += S21_magnitude*np.cos(np.radians(S21_phase))
#        s11_predicted = 1j*S11_magnitude*np.sin(np.radians(S11_phase));
#        s11_predicted += S11_magnitude*np.cos(np.radians(S11_phase))
#        s12_predicted = 1j*S12_magnitude*np.sin(np.radians(S12_phase));
#        s12_predicted += S12_magnitude*np.cos(np.radians(S12_phase))

#        # Get uncertainty (weights)
#        if self.shorted:
#            s11m_unc = unp.std_devs(self.s11_short[0][self.freq>=freq[0]])
#            s11p_unc = unp.std_devs(unp.radians(self.s11_short[1][self.freq>=freq[0]]))
#        else:   #NOTE: Update to use S22 for non-shorted case
#            s11m_unc = unp.std_devs(self.s11[0][self.freq>=freq[0]])
#            s11p_unc = unp.std_devs(unp.radians(self.s11[1][self.freq>=freq[0]]))
#        s21m_unc = unp.std_devs(self.s21[0][self.freq>=freq[0]])
#        s21p_unc = unp.std_devs(unp.radians(self.s21[1][self.freq>=freq[0]]))
#        s12m_unc = unp.std_devs(self.s12[0][self.freq>=freq[0]])
#        s12p_unc = unp.std_devs(unp.radians(self.s12[1][self.freq>=freq[0]]))
        
        return s11_predicted, s21_predicted, s12_predicted#, s11m_unc, \
#            s11p_unc, s21m_unc, s21p_unc, s12m_unc, s12p_unc
    
    def _iterate_objective_function(self,params,L,freq_0,s11c,s21c,s12c,s22c=None):
        """
        Objective funtion to minimize from modified Baker-Jarvis (NIST) 
            iterative method (Houtz et al. 2016).
        """
        
#        s11_predicted, s21_predicted, s12_predicted, s11m_unc, s11p_unc, \
#            s21m_unc, s21p_unc, s12m_unc, s12p_unc = \
#            self._iterate_model(params,L,freq_0)
        
        s11_predicted, s21_predicted, s12_predicted = \
            self._iterate_model(params,L,freq_0)
        
        # Create weighted objective functions for magnitute and phase seperately
        obj_func_real = ((np.absolute(s21c) - np.absolute(s21_predicted))/self.s21m_unc + \
                         (np.absolute(s12c) - np.absolute(s12_predicted))/self.s12m_unc + \
                         (np.absolute(s11c) - np.absolute(s11_predicted))/self.s11m_unc)
        obj_func_imag = ((np.unwrap(np.angle(s21c)) - np.unwrap(np.angle(s21_predicted)))/self.s21p_unc + \
                         (np.unwrap(np.angle(s12c)) - np.unwrap(np.angle(s12_predicted)))/self.s12p_unc + \
                         (np.unwrap(np.angle(s11c)) - np.unwrap(np.angle(s11_predicted)))/self.s11p_unc)
        
        return np.concatenate((obj_func_real,obj_func_imag))
    
    def _log_likelihood(self,params,L,freq_0,s11c,s21c,s12c):
#        s11_predicted, s21_predicted, s12_predicted, s11m_unc, s11p_unc, \
#            s21m_unc, s21p_unc, s12m_unc, s12p_unc = \
#            self._iterate_model(params,L,freq_0)
        s11_predicted, s21_predicted, s12_predicted = \
            self._iterate_model(params,L,freq_0)
        # create s-parameter row matrix
#        large_x = np.array([\
#                  np.abs(np.absolute(s11c) - np.absolute(s11_predicted)),\
#                  np.abs(np.unwrap(np.angle(s11c)) - np.unwrap(np.angle(s11_predicted))),\
#                  np.abs(np.absolute(s21c) - np.absolute(s21_predicted)),\
#                  np.abs(np.unwrap(np.angle(s21c)) - np.unwrap(np.angle(s21_predicted))),
#                  np.abs(np.absolute(s12c) - np.absolute(s12_predicted)),\
#                  np.abs(np.unwrap(np.angle(s12c)) - np.unwrap(np.angle(s12_predicted)))])
#        large_x = np.concatenate([\
#                  np.abs(np.absolute(s11c) - np.absolute(s11_predicted)),\
#                  np.abs(np.unwrap(np.angle(s11c)) - np.unwrap(np.angle(s11_predicted))),\
#                  np.abs(np.absolute(s21c) - np.absolute(s21_predicted)),\
#                  np.abs(np.unwrap(np.angle(s21c)) - np.unwrap(np.angle(s21_predicted))),
#                  np.abs(np.absolute(s12c) - np.absolute(s12_predicted)),\
#                  np.abs(np.unwrap(np.angle(s12c)) - np.unwrap(np.angle(s12_predicted)))])
        large_x = np.concatenate([\
                  np.abs(s11c.real - s11_predicted.real),\
                  np.abs(s11c.imag - s11_predicted.imag),\
                  np.abs(s21c.real - s21_predicted.real),\
                  np.abs(s21c.imag - s21_predicted.imag),
                  np.abs(s12c.real - s12_predicted.real),\
                  np.abs(s12c.imag - s12_predicted.imag)])
        # create s_parameter arrays with uncertainty
#        s_mat = np.array([np.absolute(s11c),np.unwrap(np.angle(s11c)),np.absolute(s21c),np.unwrap(np.angle(s21c)),np.absolute(s12c),np.unwrap(np.angle(s12c))])
#        c = np.cov(s_mat)
#        loglik = np.sum(-3*np.log(2*np.pi) - 0.5*np.log(np.linalg.det(c)) -0.5*np.dot(np.dot(large_x.T,np.linalg.inv(c)),large_x))
        # global s_mat
#        s_mat = np.concatenate([self.s11m_unc,self.s11p_unc_deg,self.s21m_unc,self.s21p_unc_deg,self.s12m_unc,self.s12p_unc_deg])
        s_mat = np.concatenate([self.s11r_unc,self.s11i_unc,self.s21r_unc,self.s21i_unc,self.s12r_unc,self.s12i_unc])
        #loglik = -0.5*len(s_mat)*np.log(2*np.pi) - 0.5*np.log(1/np.prod(s_mat)) -0.5*np.sum(large_x**2 / s_mat**2)
        loglik = -0.5*np.sum(large_x**2 / s_mat**2)
        # loglik = -np.sum(large_x**2 / s_mat**2)
        # global red_chi_sq
        self.red_chi_sq = np.sum(large_x**2 / s_mat**2) / len(s_mat)
        # global bic
        self.bic = np.log(len(s_mat))*2 - 2*loglik
        return loglik
    
    def _sparam_iterator(self,params,L,freq_0,s11,s21,s12,s22):
        """
        Perform the s-parameter fit using lmfit and emcee and produce the fit 
            report.
        """
        # Fit data
        minner = Minimizer(self._log_likelihood,\
                   params,fcn_args=(L,freq_0,s11,s21,s12),\
                   nan_policy='omit')
        
        from timeit import default_timer as timer
        start = timer()
        result = minner.emcee(steps=self.nsteps,nwalkers=self.nwalkers,burn=self.nburn,thin=self.nthin,workers=self.nworkers)
        end = timer()
        m, s = divmod(end - start, 60)
        h, m = divmod(m, 60)
        time_str = "emcee took: %02d:%02d:%02d" % (h, m, s)
        print(time_str)
        
        report_fit(result)
        
        highest_prob = np.argmax(result.lnprob)
        hp_loc = np.unravel_index(highest_prob, result.lnprob.shape)
        mle_soln = result.chain[hp_loc]
        for i, par in enumerate(params):
            params[par].value = mle_soln[i]


        # print('\nMaximum Likelihood Estimation from emcee       ')
        # print('-------------------------------------------------')
        # print('Parameter  MLE Value   Median Value   Uncertainty')
        # fmt = '  {:5s}  {:11.5f} {:11.5f}   {:11.5f}'.format
        # for name, param in params.items():
        #     print(fmt(name, param.value, result.params[name].value,
        #       result.params[name].stderr))
        
        return result, time_str
    
    def _permittivity_iterate(self,corr=False):
        """
        Set up iteration and plot results. Corrected data currently only supported for un-shorted measurements.
        """
        number_of_fits = self.fits
        # Get electromagnetic properties
        # Note: does not currently check if using corrected data
        if self.start_freq:     #start iteration from self.start_freq
            freq = self.freq[self.freq>=self.start_freq]
        else:   #use full frequency range
            freq = self.freq
        # Get epsilon
        epsilon = -1j*self.avg_lossfac;
        epsilon += self.avg_dielec
        epsilon = epsilon[self.freq>=freq[0]]
        # Uarrays fot plotting
        epsilon_plot_real = self.avg_dielec[self.freq>=freq[0]]
        epsilon_plot_imag = self.avg_lossfac[self.freq>=freq[0]]
        # If ierating for mu, get mu
        if self.fit_mu:
            if self.meas.nrw:   #get epsilon and mu
                mu = -1j*self.avg_mu_real;
                mu += self.avg_mu_imag
                mu = mu[self.freq>=freq[0]]
            else:   #raise exception if nrw not used
                raise Exception('permittivitycalc needs to be run with nrw=True if fit_mu=True')
            # Uarrays for plotting
            mu_plot_real = self.avg_mu_real[self.freq>=freq[0]]
            mu_plot_imag = self.avg_mu_imag[self.freq>=freq[0]]
            
        ## First, fit Cole-Cole model(s) to analytical results to get initial guess
        # If in Trial mode and number_of_poles is a list, fit for each 
        # number_of_poles (and number_of_poles_mu) in the list(s) and report statistics
        # If not in trial mode, only one value for the number of poles may be 
        # given for each of epsilon and mu
        if isinstance(self.poles,list) and not self.trial and len(self.poles) != 1:
            raise Exception('Can only have one value for number_of_poles when trial_run=False.')
        # if trail_run=False and number_of_poles is a list of length 1, make int
        elif isinstance(self.poles,list) and not self.trial and len(self.poles) == 1:
            self.poles = self.poles[0]
        if self.fit_mu and isinstance(self.poles_mu,list) and not self.trial and len(self.poles_mu) != 1:
            raise Exception('Can only have one value for number_of_poles_mu when trial_run=False.')
        elif self.fit_mu and isinstance(self.poles_mu,list) and not self.trial and len(self.poles_mu) == 1:
            self.poles_mu = self.poles_mu[0]
        
        # When trial_run is False, then self.poles should be an int while number_of_poles should be a list (of length 1)
        number_of_poles = self.poles
        if self.fit_mu:
            number_of_mu_poles = self.poles_mu
        if not isinstance(self.poles,list): # make sure number_of_poles is a list
            number_of_poles = [number_of_poles]
        if self.fit_mu and not isinstance(self.poles_mu,list):
            number_of_mu_poles = [number_of_mu_poles]
        if self.fit_mu and len(number_of_poles) != len(number_of_mu_poles):
                raise Exception('Number of poles must be the same for epsilon and mu (len(number_of_poles) == len(number_of_poles_mu))')
        
        # Create a set of Parameters to the Cole-Cole model
        params = []
        if self.fit_mu:
            for m in range(len(number_of_mu_poles)):
                params.append(self._iteration_parameters([number_of_poles[m],number_of_mu_poles[m]],initial_values=self.initial_parameters,mu=True))
        else:
            for n in range(len(number_of_poles)):
                params.append(self._iteration_parameters(number_of_poles[n],initial_values=self.initial_parameters))
            
        # Iterate to find parameters
        result = []
        for n in range(len(number_of_poles)):
            # if fit_mu, fix mu parameters
            if self.fit_mu:
                params[n] = self._fix_parameters(params[n],number_of_mu_poles[n],mu=True)
            miner = Minimizer(self._colecole_residuals,params[n],\
                              fcn_args=(number_of_poles[n],freq,epsilon))
            result.append(miner.minimize(method='least_squares'))
        if self.fit_mu:
            result_mu = []
            for m in range(len(number_of_mu_poles)):
                # unfix mu parameters and fix epsilon parameters
                params[m] = self._fix_parameters(params[m],number_of_mu_poles[m],unfix=True,mu=True)
                params[m] = self._fix_parameters(params[m],number_of_poles[m],unfix=False,mu=False)
                # iterate
                miner_mu = Minimizer(self._colecole_residuals,params[m],\
                              fcn_args=(number_of_mu_poles[m],freq,mu,True))
                result_mu.append(miner_mu.minimize(method='least_squares'))
    
        # Write fit report
        for n in range(len(number_of_poles)):
            print('Results for epsilon with {} poles:'.format(str(number_of_poles[n])))
            report_fit(result[n])
        if self.fit_mu:
            for m in range(len(number_of_mu_poles)):
                print('Results for mu with {} poles:'.format(str(number_of_mu_poles[m])))
                report_fit(result_mu[m])
        
        # Get parameter values
        values = []
        for n in range(len(number_of_poles)):
            values_temp = result[n].params
            values.append(values_temp.valuesdict())
        if self.fit_mu:
            values_mu = []
            for m in range(len(number_of_mu_poles)):
                values_mu_temp = result_mu[m].params
                values_mu.append(values_mu_temp.valuesdict())
            if not self.trial:    
                # Merge results into single object for initial guess of Bayesian fit
                if self.poles_mu == 0:
                    values[0]['mu_real'] = values_mu[0]['mu_real']
                    values[0]['mu_imag'] = values_mu[0]['mu_imag']
                else:
                    values[0]['mu_inf'] = values_mu[0]['mu_inf']
                    for m in range(self.poles_mu):
                        m+=1
                        values[0]['mu_dc_{}'.format(m)] = values_mu[0]['mu_dc_{}'.format(m)]
                        values[0]['mutau_{}'.format(m)] = values_mu[0]['mutau_{}'.format(m)]
                        values[0]['mualpha_{}'.format(m)] = values_mu[0]['mualpha_{}'.format(m)]
            
        # Calculate model EM parameters
        for n in range(len(number_of_poles)):
            epsilon_iter = self._colecole(number_of_poles[n],freq,values[n])
            # Plot                    
            pc.pplot.make_plot([freq,freq],[epsilon_plot_real,epsilon_iter.real],legend_label=['Analytical','Iterative ({} poles)'.format(str(number_of_poles[n]))])
            pc.pplot.make_plot([freq,freq],[epsilon_plot_imag,-epsilon_iter.imag],plot_type='lf',legend_label=['Analytical','Iterative ({} poles)'.format(str(number_of_poles[n]))])
            # Find values at 8.5 GHz by finding index where freq is closest to 8.5 GHz
#            ep_real = epsilon_iter.real[np.where(freq == freq[np.abs(freq - 8.5e9).argmin()])][0]
#            ep_imag = epsilon_iter.imag[np.where(freq == freq[np.abs(freq - 8.5e9).argmin()])][0]
#            print(ep_real)
#            print(ep_imag)
        if self.fit_mu:
            for m in range(len(number_of_mu_poles)):
                mu_iter = self._colecole(number_of_mu_poles[m],freq,values_mu[m],mu=True)
                if number_of_mu_poles[m] == 0:
                    mu_iter =  mu_iter*np.ones(len(freq))
                pc.pplot.make_plot([freq,freq],[mu_plot_real,mu_iter.real],plot_type='ur',legend_label=['Analytical mu','Iterative mu ({} poles)'.format(str(number_of_mu_poles[m]))])
                pc.pplot.make_plot([freq,freq],[mu_plot_imag,-mu_iter.imag],plot_type='ui',legend_label=['Analytical mu','Iterative mu ({} poles)'.format(str(number_of_mu_poles[m]))])
#                mu_real = mu_iter.real[np.where(freq == freq[np.abs(freq - 8.5e9).argmin()])][0]
#                mu_imag = mu_iter.imag[np.where(freq == freq[np.abs(freq - 8.5e9).argmin()])][0]
#                print(mu_real)
#                print(mu_imag)
        
        # If not in trial mode (no iterative fitting of sparams), perform iteration
        if not self.trial:
            # Check if using corrected S-params
            if corr:
                s11 = self.s11
                L = self.meas.Lcorr
            else:
                # Use shorted S11 if available
                if self.shorted:
                    s11 = self.s11_short
                else:
                    s11 = self.s11
                L = self.meas.L
            s21 = self.s21
            s12 = self.s12
            s22 = self.s22
            
            # Start arrays at start_freq
            s11 = np.array((s11[0][self.freq>=freq[0]],s11[1][self.freq>=freq[0]]))
            s21 = np.array((s21[0][self.freq>=freq[0]],s21[1][self.freq>=freq[0]]))
            s12 = np.array((s12[0][self.freq>=freq[0]],s12[1][self.freq>=freq[0]]))
            s22 = np.array((s22[0][self.freq>=freq[0]],s22[1][self.freq>=freq[0]]))
            # Cast measured sparams to complex
            s11c = 1j*s11[0]*np.sin(np.radians(s11[1]));
            s11c += s11[0]*np.cos(np.radians(s11[1]))
            s22c = 1j*s22[0]*np.sin(np.radians(s22[1]));
            s22c += s22[0]*np.cos(np.radians(s22[1]))
            s21c = 1j*s21[0]*np.sin(np.radians(s21[1]));
            s21c += s21[0]*np.cos(np.radians(s21[1]))
            s12c = 1j*s12[0]*np.sin(np.radians(s12[1]));
            s12c += s12[0]*np.cos(np.radians(s12[1]))
            
            ## Perform the fits acording to number_of_fits
            values_sp = values[0] # Use Cole-Cole fit for intial values
            for n in range(number_of_fits):
                # Create a set of Parameters
                if self.initial_parameters: # Use given initial values instead of generated ones
                    initial_values = self.initial_parameters
                else:
                    initial_values = values_sp
                if self.fit_mu:
                    params = self._iteration_parameters([number_of_poles[0],number_of_mu_poles[0]],initial_values,mu=True)
                else:
                    params = self._iteration_parameters(number_of_poles,initial_values)
                # Fit data
                result_sp, time_str = self._sparam_iterator(params,L,freq[0],s11c,s21c,s12c,s22c)
                # Update initial values for next run
                values_sp = result_sp.params
                values_sp = values_sp.valuesdict()
            
            # Get final parameter values
            values_sp = result_sp.params
            values_sp = values_sp.valuesdict()
            
            # Calculate model EM parameters
            epsilon_iter_sp = self._colecole(number_of_poles[0],freq,values_sp)
            if self.fit_mu:
                mu_iter_sp = self._colecole(number_of_mu_poles[0],freq,values_sp,mu=True)
            else:
                mu_iter_sp = 1
            
            # Plot
            try:                 
                pc.pplot.make_plot([freq,freq],[epsilon_plot_real,epsilon_iter_sp.real],legend_label=['Analytical','Iterative'],publish=self.publish,name=self.name)
                pc.pplot.make_plot([freq,freq],[epsilon_plot_imag,-epsilon_iter_sp.imag],plot_type='lf',legend_label=['Analytical','Iterative'],publish=self.publish,name=self.name)
                if self.fit_mu:
                    pc.pplot.make_plot([freq,freq],[mu_plot_real,mu_iter_sp.real],plot_type='ur',legend_label=['Analytical mu','Iterative mu'],publish=self.publish,name=self.name)
                    pc.pplot.make_plot([freq,freq],[mu_plot_imag,-mu_iter_sp.imag],plot_type='ui',legend_label=['Analytical mu','Iterative mu'],publish=self.publish,name=self.name)
            except:
                print('Plot(s) failed')
                pass
        
            # Plot s-params
            s11_predicted, s21_predicted, s12_predicted = self._model_sparams(freq,L/100,epsilon_iter_sp,mu_iter_sp)
            # Plot
            try:
                f,ax = plt.subplots(3, 2, sharex=True, figsize=(18, 15))
                ax[0,0].plot(freq,np.absolute(s11c),label='Measured') #s11mag
                ax[0,0].plot(freq,np.absolute(s11_predicted),label='Predicted')
                ax[0,0].set_title('Magnitude of S11')
                ax[0,1].plot(freq,np.angle(s11c),label='Measured') #s11phase
                ax[0,1].plot(freq,np.angle(s11_predicted),label='Predicted')
                ax[0,1].set_title('Phase of S11')
                ax[1,0].plot(freq,np.absolute(s21c),label='Measured') #s21mag
                ax[1,0].plot(freq,np.absolute(s21_predicted),label='Predicted')
                ax[1,0].set_title('Magnitude of S21')
                ax[1,1].plot(freq,np.angle(s21c),label='Measured') #s21phase
                ax[1,1].plot(freq,np.angle(s21_predicted),label='Predicted')
                ax[1,1].set_title('Phase of S21')
                ax[2,0].plot(freq,np.absolute(s12c),label='Measured') #s12mag
                ax[2,0].plot(freq,np.absolute(s12_predicted),label='Predicted')
                ax[2,0].set_title('Magnitude of S12')
                ax[2,1].plot(freq,np.angle(s12c),label='Measured') #s12phase
                ax[2,1].plot(freq,np.angle(s12_predicted),label='Predicted')
                ax[2,1].set_title('Phase of S12')
                # Hide redundant x-axis tick marks
                plt.setp([a.get_xticklabels() for a in ax[0, :]], visible=False)
                ax[0,0].legend(loc=1)
                plt.show()
            except:
                pass
            
            #Corner plot
            try:
                default_font = matplotlib.rcParams["font.size"]
                matplotlib.rcParams["font.size"] = 16
                figure = corner.corner(result_sp.flatchain, labels=result_sp.var_names, \
                              truths=list(result_sp.params.valuesdict().values()))
                figure.subplots_adjust(right=1.5,top=1.5)
                if self.publish:
                    DATE = str(datetime.date.today())
                    try:
                        datapath = pc.pplot.save_path_for_plots
                    except:
                        print('Save path is not in globals')
                    savename = self.name.replace(' ','-') + '_corner_ ' + DATE + '.pdf'
                    filepath = os.path.join(datapath,savename)
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        figure.savefig(filepath,dpi=300,format='pdf',pad_inches=0.3,bbox_inches='tight')
            except:
                pass
            
            #Plot traces
            try:
                nplots = len(result_sp.var_names)
                fig, axes = plt.subplots(nplots, 1, sharex=True, figsize=(8,nplots*1.6))
                for n in range(nplots):
                    axes[n].plot(result_sp.chain[:, :, n].T, color="k", alpha=0.4)
                    axes[n].yaxis.set_major_locator(MaxNLocator(4))
                    axes[n].set_ylabel(result_sp.var_names[n])
                axes[nplots-1].set_xlabel("step number")
                fig.tight_layout(h_pad=0.1)
                plt.show()
                if self.publish:
                    DATE = str(datetime.date.today())
                    try:
                        datapath = pc.pplot.save_path_for_plots
                    except:
                        print('Save path is not in globals')
                    savename = self.name.replace(' ','-') + '_traces_ ' + DATE + '.pdf'
                    filepath = os.path.join(datapath,savename)
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        fig.savefig(filepath,dpi=300,format='pdf',pad_inches=0)
                matplotlib.rcParams["font.size"] = default_font
            except:
                pass
            
            
            print(time_str)
            
            # Return results
            if self.fit_mu:
                return epsilon_iter_sp, mu_iter_sp, values_sp, result_sp
            else:
                return epsilon_iter_sp, values_sp, result_sp
