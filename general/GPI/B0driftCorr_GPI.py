# Author: Sudarshan Ragunathan
# Date: 02May2021

import numpy as np
import gpi


class ExternalNode(gpi.NodeAPI):
    """This is a GPI node to perform B0 drift correction for a single shot spiral dynamic scan
    using a linear drift model.

    INPUT:
        B0 - The B0 map as a numpy array
    OUTPUT:
        B0corr - The B0 map after correcting for B0 drift as a numpy array
    WIDGETS:
        f0_min - Lower bound value of f0
        f0_max - upper bound value of f0
        Total Dynamics - Number of dynamics
        correction dynamic - Dynamic that needs drift correction
    """

    # initialize the UI - add widgets and input/output ports
    def initUI(self):
        # Widgets
        self.addWidget('DoubleSpinBox', 'f0_min', val=0., min=0., max=100.)
        self.addWidget('DoubleSpinBox', 'f0_max', val=32., min=0., max=100.)
        self.addWidget('SpinBox', 'Total Dynamics', val=200, min=0, max=1000)
        self.addWidget('SpinBox', 'correction dynamic', val=0, min=0, max=1000)
        self.addWidget('PushButton', 'Compute', toggle=True, visibility=True, val=0)

        # IO Ports
        self.addInPort('B0', 'NPYarray', dtype=[np.double, np.float32])
        self.addOutPort('B0corr', 'NPYarray', dtype=[np.double, np.float32])


    def validate(self):
        b0_data = self.getData('B0')
        total_dyns = self.getVal('Total Dynamics')
        corr_dyn = self.getVal('correction dynamic')

        if corr_dyn > total_dyns:
            self.log.warn('Dynamic to be corrected exceeds the total dynamics in the series')
            return 1

        # TODO: make sure the input data is valid
        # [your code here]

        return 0

    def compute(self):
        b0_data = self.getData('B0')
        f0_min = self.getVal('f0_min')
        f0_max = self.getVal('f0_max')
        total_dyns = self.getVal('Total Dynamics')
        corr_dyn = self.getVal('correction dynamic')
        b0corr_data = np.zeros(b0_data.shape)

        if self.getVal('Compute'):
            # Generate linear f0 drift series
            f0_series = np.zeros(total_dyns)
            f0_series = np.linspace(f0_min,f0_max,total_dyns)

            # Select the appropriate drift value based on the dynamic and perform drift correction
            f0_drift = np.double(f0_series[np.int(corr_dyn-1)])
            b0corr_data = b0_data - f0_drift
            
        
            self.setData('B0corr', b0corr_data)

        return 0
