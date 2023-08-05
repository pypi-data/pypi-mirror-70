# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 21:08:10 2018

@author: adutz

    TrussPy - Object Oriented Truss Solver for Python
    Copyright (C) 2018  Andreas Dutzler

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import sys
import os
import copy
import time
from subprocess import run as sp_run

# Numpy and Pandas
import numpy as np
import pandas as pd

# Handler Classes
from .handlers import SettingsHandler
from .handlers import NodeHandler
from .handlers import ElementHandler
from .handlers import BoundaryHandler
from .handlers import ExternalForceHandler
from .handlers import ResultHandler

# Analysis Class
from .core import Analysis

#from scipy.optimize import fsolve

# Material Definition
from .materials import umat_el, umat_elplast_iso

# Element Definition
from .elements import truss

# Solver and Tools
from .solvers import pathfollow
from .tools import (p_nodes,p_elements,p_extforces,
                    p_model,p_movie,p_history,p_path,p_show)

class Model:
    """Model Class with Nodes, Elements, Boundaries, etc.
    
    Attributes
    ----------
    stdout : sys.stdout
        get current stdout
        
    file : None or str
        name of input file (default is None)
        
    log : int
        Level of collecting logging informations during analysis.
        Higher numbers will collect more informations (default is 2).
        
    logfile : boolean
        flag for logfile creation (default is True)
        
    Nodes : NodeHandler
        Handles all nodes inside the model
        
    Elements : ElementHandler
        Handles all elements inside the model
        
    Boundaries : BoundaryHandler
        Handles all boundaries inside the model
        
    ExtForces : ExternalForceHandler
        Handles all external forces inside the model
        
    Analysis : AnalysisHandler
        Handles all data for one increment
        
    Results : ResultHandler
        Handles all result data inside the model.
        A collection of all converged analysis solutions.
        
    Settings : SettingsHandler
        Handles all model parameters inside the model
    
    Todo
    ----
    * move g(V), dgdV(V) from Model class to path_tracing function
    """
    def __init__(self,file=None,log=2,logfile=False,logfile_name='analysis'):
        """Init Model class with default values. If input file is specified,
        collect all data and create model.
        
        Parameter
        ---------
        file : None or str, optional
            name of input file (default is None)
            
        log : int
            Level of collecting logging informations during analysis.
            Higher numbers will collect more informations (default is 2).
            
        logfile : boolean, optional
            flag for logfile creation (default is True)
        """
        self.stdout = sys.stdout
        self.file = file
        self.logfile = logfile
        if file is None:
            pass
            #self.logfile = False
        
        if self.file is not None:
            self.logfile_name = '.'.join(self.file.split('.')[:-1])
        else:
            self.logfile_name = logfile_name
            #self.logfile = False
        if self.logfile:
            sys.stdout = open(self.logfile_name+'.md', 'w')
            print(r"<script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>")
            
        if log > 1: 
            print("""
         _____                  ______      
        |_   _|                 | ___ \     
          | |_ __ _   _ ___ ___ | |_/ /   _ 
          | | '__| | | / __/ __||  __/ | | |
          | | |  | |_| \__ \__ \| |  | |_| |
          \_/_|   \__,_|___/___/\_|   \__, |
                                       __/ |
                                      |___/ 
        
        TrussPy - Object Oriented Truss Solver for Python
                  Version 2018.08 (Build 20180829)

        Author: Dutzler A.
                Graz University of Technology, 2018
                
        TrussPy  Copyright (C) 2018  Andreas Dutzler
        This program comes with ABSOLUTELY NO WARRANTY; 
        for details type `trusspy.show_w()'.
        This is free software, and you are welcome to redistribute it
        under certain conditions; type `trusspy.show_c()' for details.
        """)

        if log > 1: print('')
        if log > 1: print('# Initialize Model')
        if log > 1: print('* loading Managers\n')
        
        self.Nodes = NodeHandler()
        self.Elements = ElementHandler()
        self.Boundaries = BoundaryHandler()
        self.ExtForces = ExternalForceHandler()
        self.Settings = SettingsHandler()
        #self.Results = ResultHandler()
        #self.Analysis = Analysis()
        
        self.Settings.log = log
        
        if log > 1: print('    - finished.\n')
        #if log > 1: print('-'*88+'\n')
        
        if file is not None:
            if log > 1: print('* loading INPUT-File: "'+file+'"\n')
            Nodes = pd.read_excel(file,sheet_name="Nodes",skiprows=2).values[:,:4].astype(float)
            Elements = pd.read_excel(file,sheet_name="Elements",skiprows=2).values[:,:10].astype(float)
            Material = pd.read_excel(file,sheet_name="Material",skiprows=2).values[:,:10].astype(float)
            Geometry = pd.read_excel(file,sheet_name="Geometry",skiprows=2).values[:,:10].astype(float)
            ExtForces = pd.read_excel(file,sheet_name="ExternalForces",skiprows=2).values[:,:1+5*3].astype(float)
            Boundary_U = pd.read_excel(file,sheet_name="BoundaryU",skiprows=2).values[:,:4].astype(float)
            Boundary_T = pd.read_excel(file,sheet_name="BoundaryT",skiprows=2).values[:,:2].astype(float)
            if log > 1: print('    - successful.\n')
            
            if log > 1: print('* Converting Data...\n')
            self.Nodes.add_node_matrix(Nodes)
            self.Elements.add_element_matrix(Elements,Material,Geometry,Boundary_T)
            self.ExtForces.add_force_matrix(ExtForces)
            self.Boundaries.add_bound_U_matrix(Boundary_U)

            if log > 1: print('    - Import finished.\n')
            #if log > 1: print('-'*88)
    
    def build(self):
        """build Model (r,U,K,...) with Model data and dimensions."""
        
        self.Results = ResultHandler()
        self.Analysis = Analysis()
        
        self.clock0_build = time.perf_counter()
        self.time0_build = time.process_time()
        
        # initialize numbers: #nodes, #elements, #dof
        self.nnodes = len(self.Nodes.labels)
        self.nelems = len(self.Elements.labels)
        self.ndim = self.Settings.ndim
        self.ndof = self.nnodes * self.ndim
        
        # fix node sorting, undefined boundaries and undefined external forces
        self.Nodes.fix_nodes()
        self.Boundaries.fix_bounds_U(self.Nodes.labels)
        self.ExtForces.fix_forces(self.Nodes.labels)
        
        if not(np.allclose(self.Nodes.labels,self.Boundaries.Unodes) and np.allclose(self.Nodes.labels,self.ExtForces.nodes)):
            raise IOError('Node sorting failed.')
        
        # init state variables for plasticity
        if 2 in self.Elements.mat_type:
            self.Settings.nstatev = 2
        
        # node properties
        # n----pro-------
        #
        #      active = free  = 1
        #    inactive = fixed = 0
        
        self.nproBC = self.Boundaries.Uvalues
        self.nproDOF = np.arange(self.ndof).reshape(self.nnodes,self.ndim)
        self.nproDOF0 = self.nproDOF.flatten()[np.where(self.nproBC.flatten() == 0)]
        self.nproDOF1 = self.nproDOF.flatten()[np.where(self.nproBC.flatten() == 1)]
        self.ndof0 = len(self.nproDOF0)
        self.ndof1 = len(self.nproDOF1)
        
        if self.Settings.log > 1: 
            print('')
            print('# Model Summary')

            print('    Analysis Dimension      "ndim":', self.Settings.ndim)
            print('    Number of Nodes       "nnodes":', self.nnodes)
            print('    Number of Elements    "nelems":', self.nelems)
            print(' ')
            print('    System DOF              "ndof":', self.ndof)
            print('    active DOF             "ndof1":', self.ndof1)
            print('    locked DOF             "ndof2":', self.ndof0)
            print(' ')
            print('    active DOF          "nproDOF1":', self.nproDOF1)
            print('    fixed  DOF          "nproDOF0":', self.nproDOF0)
            
        # init results, add empty increment
        self.Results.add_increment()
        self.Analysis.build(self.nnodes,self.nelems,self.ndim,
                            self.nproDOF0,self.nproDOF1,
                            self.Settings.nstatev)
        self.Results.R[-1] = copy.deepcopy(self.Analysis)
        
        self.clock1_build = time.perf_counter()
        self.time1_build = time.process_time()
            
    def run(self):
        """Run job."""
        
        if self.Settings.log > 1: 
            print(r'\pagebreak')
            print(' ')
            print('# Run Simulation')

            
        if self.Settings.log > 1:
            print('\n## Summary of Analysis Parameters')

            print('|Description                          |Parameter|Value|')
            print('|:------------------------------------|:--------|:--|')
            print('|Maximum increments                   |   `incs`|', self.Settings.incs,'|')
            print('|Maximum increment recycles           |   `cycl`|', self.Settings.cycl,'|')
            print('|Maximum Newton-Rhapson iterations    |   `nfev`|', self.Settings.nfev,'|')
            print('|Maximum incremental displacement     |     `du`|', self.Settings.du,'|')
            print('|Maximum incremental LPF              |   `dlpf`|', self.Settings.dlpf,'|')
            print('|Initial control component            |     `j0`|', 'LPF|' if self.Settings.j0==None else self.Settings.j0+'|')
            print('|Locked control component             |`j_fixed`|', self.Settings.j_fixed,'|')
            print('|Maximum incremental overshoot        |  `dxtol`|', self.Settings.dxtol,'|')
            print('|Tolerance for x                      |   `xtol`|', self.Settings.xtol,'|')
            print('|Tolerance for f                      |   `ftol`|', self.Settings.ftol,'|')
            
            
            if self.Settings.stepcontrol:
                print('\n### Adaptive control for incremental stepwidth')

                print('|Description                          |Parameter    |Value|')
                print('|:------------------------------------|:------------|:--|')
                print('|Adaptive control for inc. stepwidth  |`stepcontrol`|', self.Settings.stepcontrol,'|')
                print('|Minimum step size factor             |     `minfac`|', self.Settings.minfac,'|')
                print('|Maximum step size factor             |     `maxfac`|', self.Settings.maxfac,'|')
                print('|Reduce step size factor              |     `reduce`|', 1/self.Settings.reduce,'|')
                print('|Increase step size factor            |   `increase`|', self.Settings.increase,'|')
            print('')
            
        # measure time
        self.clock0_run = time.perf_counter()
        self.time0_run = time.process_time()
        
        
        
        # reduced modified displacement vector to active DOF and LPF
        self.Analysis.Vred = np.append(self.Analysis.Ured, 0)
        self.Analysis.lpf = 0
        
        # init LPF
        # self.Settings.lpf = self.Settings.dlpf
        #self.Analysis.lpf = self.Settings.dlpf
        
        for step in range(self.Settings.nsteps):
            
            # maximum number of increment and maximum value per step
            if type(self.Settings.incs) == tuple:
                incs = self.Settings.incs[step]
            else:
                incs = self.Settings.incs
            if type(self.Settings.xlimit[0]) == tuple:
                xlimit = self.Settings.xlimit[step]
            else:
                xlimit = self.Settings.xlimit
                
            if self.Settings.log > 0: print('\n## Step', step+1)
            if self.Settings.log > 1:
                print(r'* i(1) is index with 1st-biggest component in abs(Dx/Dx,max).')
                print(r'* i(2) is index with 2nd-biggest component in abs(Dx/Dx,max).')
                print(r'* i(3) is index with 3rd-biggest component in abs(Dx/Dx,max).')
                print(r'* i(4) is index with 4th-biggest component in abs(Dx/Dx,max).')
                print(r'* Value(i) is value of i-th component in abs(Dx/Dx,max).')
                
                print(r'$$\text{Value}_i = \left|\frac{D_x}{D_{x,max}}\right|_i$$')
            
            # get reduced external force vector
            #f0red = self.ExtForces.forces[:,3*(step):3*(step+1)].flatten()[self.Analysis.DOF1]
            #self.Analysis.f0red = f0red.reshape(len(f0red),1)
            self.Analysis.ExtForces = copy.deepcopy(self.ExtForces)
            
            f0_const = np.zeros_like(self.ExtForces.forces[:,3*(step):3*(step+1)])
            for s in range(step):
                f0_const += self.Results.step_lpf_end[s]*self.ExtForces.forces[:,3*(s):3*(s+1)]
            if len(range(step)) is not 0:
                print('\nconstant part of external forces due to previous step(s)')
                print('    ',f0_const,'\n')
                print('\ninitial values of active DOF due to previous step(s)')
                print('    ',self.Analysis.Vred,'\n')
            self.Analysis.ExtForces.forces_const = f0_const
            self.Analysis.ExtForces.forces = self.ExtForces.forces[:,3*(step):3*(step+1)]
            f0red = self.Analysis.ExtForces.forces.flatten()[self.Analysis.DOF1]
            self.Analysis.f0red = f0red.reshape(len(f0red),1)
            
            self.Analysis.step = 1+step
            
            res_V,res_a = pathfollow(self.equilibrium,self.stiffness, 
                                     self.Analysis.Ured, self.Analysis,
                                     dxmax=[self.Settings.du,self.Settings.dlpf],
                                     j=self.Settings.j0,
                                     j_fixed = self.Settings.j_fixed,
                                     j_pre = self.Settings.j_pre,
                                     xlimit = xlimit,
                                     incs=incs,
                                     nfev=self.Settings.nfev,
                                     cycl=self.Settings.cycl,
                                     ftol=10**-self.Settings.ftol,
                                     xtol=10**-self.Settings.xtol,
                                     stepcontrol=self.Settings.stepcontrol,
                                     maxfac=self.Settings.maxfac,
                                     minfac=self.Settings.minfac,
                                     reduce=self.Settings.reduce,
                                     increase=self.Settings.increase,
                                     dxtol=self.Settings.dxtol,
                                     verbose=self.Settings.log)
            
            if self.Settings.log > 1:
                print(r'\pagebreak')
                print(' ')
                print('\n### Create result object from analysis results for step {0:3d}\n'.format(1+step))
            
            for i,(r_V,r_a) in enumerate(zip(res_V[1:],res_a[1:])):
                if self.Settings.log > 1:
                    print('    write result {0:3d}/{1:3d} (LPF: {2:10.4g})'.format(1+i,len(res_V[1:]),r_a.lpf))
                self.Results.R[-1] = r_a
                self.Results.copy_increment()
                
            # copy initial U0
            self.Results.R[-1].U0 = np.copy(self.Results.R[-1].U)
            
            # append last lpf value
            self.Results.step_lpf_end.append(self.Results.R[-1].lpf)
            
            # reset LPF for new step
            if step+1 < self.Settings.nsteps:
                self.Analysis.Vred[-1] = 0.0
                self.Analysis.lpf = 0.0
            else:
                self.Results.remove_last_increment()
                
            if self.Settings.log > 0: print('\nEnd of Step', step+1)
            
        # duplicate first increment to get right indices
        self.Results.duplicate_first_increment()
            
        time_dclock_run   = time.perf_counter() - self.clock0_run
        time_dtime_run    = time.process_time()  - self.time0_run
        time_dclock_build = self.clock1_build - self.clock0_build
        time_dtime_build  = self.time1_build  - self.time0_build
        if self.Settings.log > 1:
            print(r'\pagebreak')
            print(' ')
            print('\n## Job duration')
            print('Time measurement for execution times of "Model.build()" and "Model.run()".\n')
            print('    total  cpu time "build": {:10.3f} seconds'.format(time_dclock_build))
            print('    total wall time "build": {:10.3f} seconds\n'.format(time_dtime_build))
            print('    total  cpu time "run":   {:10.3f} seconds'.format(time_dclock_run))
            print('    total wall time "run":   {:10.3f} seconds\n'.format(time_dtime_run))
            
        if self.logfile:
            sys.stdout = self.stdout
            sp_run(['pandoc', self.logfile_name+'.md', '-t', 'latex', '-o', self.logfile_name+'.pdf'])
            if self.Settings.logpdf: sp_run(['pandoc', self.logfile_name+'.md', '-t', 'html', '-s', '-o', self.logfile_name+'.html'])
        

    def stiffness(self,Ured,analysis=None):
        "Method for Stiffness Matrix."
        
        # In a future version this function should be implemented in Stiffness class part of the Model or Results
        # self.Stiffness(reduced=True)
        
        # it re-shapes stiffness matrix to
        # K(nnodes,nnodes,ndim,ndim) --> K(nnodes*ndim,nnodes*nim)
        # and returns a view on the reduced (active part of the) matrix
        # K(nnodes*ndim,nnodes*nim)[active DOF rows][:,active DOF columns]
        
        if analysis is not None:
                self.Analysis = analysis
        
        # generate stiffness
        self.equilibrium(Ured,Ured,stage='K')
        
        # init re-shaped output stiffness matrix
        K_out = np.zeros((self.nnodes*self.ndim, self.nnodes*self.ndim))

        # loop over nodes to reshape K
        for a in range(self.nnodes):
            for b in range(self.nnodes):
                K_out[a*self.ndim:a*self.ndim+self.ndim,
                      b*self.ndim:b*self.ndim+self.ndim] = self.Analysis.K[a,b]

        # select only active DOF1
        self.Analysis.Kred = K_out[self.Analysis.DOF1][:,self.Analysis.DOF1]
        
        return self.Analysis.Kred
            
        
    def equilibrium(self,Ured,U0red,stage='G',analysis=None,statev_write=False):
        """Method to generate equilibrium for given displacements and external forces."""
        
        if analysis is not None:
                self.Analysis = analysis

        # remove last entry in Vred to get only displacement DOFs
        if len(Ured) > self.ndof1:
            lpf   =  Ured[-1]
            lpf0  = U0red[-1]
            Ured  =  Ured[:self.ndof1]
            U0red = U0red[:self.ndof1]
        else:
            lpf = self.Analysis.lpf
            
        if stage=='G':
            self.Analysis.r.fill(0.0)
        else: #stage=='K'
            self.Analysis.K.fill(0.0)
            
            
        # copy input Ured to appropriate positions in full U-vector
        self.Analysis.U.reshape(len(self.Analysis.U.flatten(),))[self.Analysis.DOF1] = Ured
        self.Analysis.U0.reshape(len(self.Analysis.U0.flatten(),))[self.Analysis.DOF1] = U0red
        
        # loop over elements
        for e in self.Elements.labels:
            nodes = self.Elements.get_nodes(e) # connected nodes
            
            mat_prop = self.Elements.get_material_properties(e)  # material parameter
            geo_prop = self.Elements.get_geometric_properties(e) # geometric parameter
            
            # undeformed coordinates of begin and end nodes
            Xnodes = np.zeros((len(nodes),3))
            for n,node in enumerate(nodes):
                Xnodes[n] = self.Nodes.coords[np.where(self.Nodes.labels == node)][0]
            
            # displacements at begin and end nodes
            Unodes = np.zeros((len(nodes),3))
            for n,node in enumerate(nodes):
                Unodes[n] = self.Analysis.U[np.where(self.Nodes.labels == node)][0]
            
            # initial displacements at begin and end nodes
            U0nodes = np.zeros((len(nodes),3))
            for n,node in enumerate(nodes):
                U0nodes[n] = self.Analysis.U0[np.where(self.Nodes.labels == node)][0]
                
            # RESOLVE PROBLEM IN STATEV UPDATE
            if self.Settings.nstatev > 0:
                state_v = self.Analysis.state_v.copy()
            else:
                state_v = None

            # internal forces at begin and end nodes
            rnodes = np.zeros((len(nodes),3))
            for n,node in enumerate(nodes):
                rnodes[n] = self.Analysis.r[np.where(self.Nodes.labels == node)][0]
                
            mat_type = self.Elements.get_material_type(e)
            #elem_type = self.Elements.get_element_type(e)
            
            if mat_type == 1:
                umat = umat_el
            elif mat_type == 2:
                umat = umat_elplast_iso
            elif mat_type == 3:
                umat = umat_elplast_kiniso
            
            self.Analysis,state_v = truss(e,nodes,Xnodes,Unodes,U0nodes,rnodes,
                                       self.Nodes.labels,self.Elements.labels,stage,
                                       state_v,mat_prop,geo_prop,umat,
                                       self.Analysis)
            if statev_write and self.Settings.nstatev > 0:
                #print('write state-variable for element', int(e), state_v[0])
                self.Analysis.state_v = state_v
                self.Analysis.lpf = lpf
                self.Analysis.Vred = np.append(Ured,lpf)

        if stage == 'G':
            self.Analysis.g = -self.Analysis.r.flatten() \
                                  +       self.Analysis.ExtForces.forces_const.flatten() \
                                  + lpf * self.Analysis.ExtForces.forces.flatten()
            return self.Analysis.g[self.Analysis.DOF1]
        else:
            return
    
    # Plot Utilities from "trusspy/tools/plot_utitilies.py"
    def plt_nodes(self,config='undeformed'):
        p_nodes(self,config)
        
    def plt_elements(self,config='undeformed'):
        p_elements(self,config)

    def plt_extforces(self,config='undeformed'):
        p_extforces(self,config)

    def plot_model(self,config='both',view='xz',contour=None,lim_scale=1.2,force_scale=0.5,nodesize=10,cbar_limits='auto',inc=-1):
        fig, ax = p_model(self,config,view,contour,lim_scale,force_scale,nodesize,cbar_limits,inc)
        return fig, ax
           
    def plot_movie(self,config='both',view='xz',contour=None,lim_scale=1.2,force_scale=0.5,nodesize=10,cbar_limits='auto',incs='all'):
        p_movie(self,config,view,contour,lim_scale,force_scale,nodesize,cbar_limits,incs)
        
    def plot_history(self, nodes=[1, 1], increments=None, X='Displacement X', Y='LPF', fig=None, ax=None):
        fig, ax = p_history(self,nodes,increments,X,Y,fig,ax)
        return fig, ax
    
    def plot_path(self, nodepath=[1], increment=-1, Y='Displacement X', fig=None, ax=None):
        fig, ax = p_path(self,nodepath,increment,Y,fig,ax)
        return fig, ax
        
    def plot_show(self):
        p_show(self)

        