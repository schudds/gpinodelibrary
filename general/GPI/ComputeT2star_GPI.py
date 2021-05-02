# Author: Sudarshan Ragunathan <sudarshan.ragunathan@barrowneuro.org>
# Date: 2019-10-03 11:25


import gpi
import numpy as np

class ExternalNode(gpi.NodeAPI):
    """Compute T2* map from mult-echo (MGE) data

    INPUT:
        mgedat - the MGE numpy array (#dims should be either 3 or 4 with last dim representing #echoes) [REQUIRED]
        mask - binary mask generated from reference T1 to mask out background noise [OPTIONAL]

    OUTPUT:
        T2star - the computed T2* map as a numpy array
        fitout - the curve fit metrics

    WIDGETS:
        TE1 - first echo time in ms (type: double/float)
        deltaTE - Echo spacing in ms (type: double/float)
        Compute - toggle node computation
    """

    def initUI(self):
        # Widgets
        self.addWidget('DoubleSpinBox', 'TE1', val=1.000, min=0.000, max=100.000)
        self.addWidget('DoubleSpinBox', 'deltaTE', val = 1.000, min=0.000, max=100.000)
        self.addWidget('DoubleSpinBox', 'Flip Angle (deg)', val = 90.0, min=0.0, max=180.0)
        self.addWidget('SpinBox', '# Echoes', val = 5, min=1, max=10)
        self.addWidget('PushButton', 'Compute', toggle=True, visible=True, val=0)

        # IO Ports
        self.addInPort('mgedat', 'NPYArray')
        self.addInPort('mask', 'NPYArray', obligation=gpi.OPTIONAL)
        self.addOutPort('T2star', 'NPYArray')
    
    def validate(self):

        data = self.getVal('mgedat')
        if data is not None:
            if data.ndim not in [3,4]:
                print("Error : # of dimensions must be 3 or 4")
                return 1

        return 0

    def compute(self):

        data = self.getVal('mgedat')
        te1 = self.getVal('TE1')
        deltaTE = self.getVal('deltaTE')
        flipangle = self.getVal('Flip Angle')
        echoes = self.getVal('# Echoes')
        
        e,z,y,x = data.shape
        TE_arr = np.zeros(echoes)
        TE_arr[0] = te1
        T2star = zeros([z,y,x])
        fitcov = np.zeros([z,y,x])


        def t2starfit(x,a,b):
            return a * sin(flipangle*np.pi/180.0) * np.exp((-x)/b)

        for i in (2,echoes):
            TE_arr[i] = TE_arr[i-1] + deltaTE
        
        if self.getVal('Compute'):

            from scipy.optimize import curve_fit
            import math

            for k in z:
                for j in y:
                    for i in x:
                        ydata = data[:,k,j,i]
                        # Initialize S0 and T2*
                        x0 = np.array([np.amax(ydata), 30.0])
                        T2star[k,j,i],fitcov[k,j,i] = curve_fit(t2starfit,np.transpose(ydata),TE_arr,p0=x0,method='lm')

            self.setData('T2star', T2star)
        
        return 0

    def execType(self):
        return gpi.GPI_PROCESS



