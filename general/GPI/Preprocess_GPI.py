# Author: Sudarshan Ragunathan
# Date: 03may2021

import numpy as np
import gpi


class ExternalNode(gpi.NodeAPI):
    """This is a GPI node to preprocess the spiral header file 

    INPUT:
        hdr_in - dictionary of header
        spparams_in - dictionary with spiral parameters
    OUTPUT:
        hdr_out - pre-processed header as dictionary
        spparams_out - dictionary with modified spiral parameters
    WIDGETS:
        Spiral in/out select - Select if preprocessing is for spiral-in or spiral-out trajectory
        Compute - Toggle compute 
    """

    # initialize the UI - add widgets and input/output ports
    def initUI(self):
        # Widgets
        self.addWidget('PushButton', 'Compute', toggle=True, val=0)
        self.addWidget('ExclusivePushButtons', 'Spiral in/out select',
                     buttons=['spiral-in', 'spiral-out'], val=1)

        # IO Ports
        self.addInPort('hdr_in', 'DICT')
        self.addInPort('spparams_in', 'DICT', obligation=gpi.OPTIONAL)
        self.addOutPort('hdr_out', 'DICT')
        self.addOutPort('spparams_out', 'DICT', obligation=gpi.OPTIONAL)

    # validate the data - runs immediately before compute
    # your last chance to show/hide/edit widgets
    # return 1 if the data is not valid - compute will not run
    # return 0 if the data is valid - compute will run
    def validate(self):
        hdr_in = self.getData('hdr_in')

        # TODO: make sure the input data is valid
        # [your code here]

        return 0

    # process the input data, send it to the output port
    # return 1 if the computation failed
    # return 0 if the computation was successful 
    def compute(self):
        hdr_in = self.getData('hdr_in')
        spparams_in = self.getData('spparams_in')
        inout_select = self.getVal('Spiral in/out select')

        if self.getVal('Compute'):
            if inout_select:
                hdr_out = hdr_in['BNIspiral']
            else:
                hdr_out = hdr_in['BNIspiral']
                hdr_out['spINOUT_ON'][0] = 1
            spparams_out = spparams_in
            spparams_out['RES_CM'] = [0.3157894, 0.3157894, 0.]

            self.setData('hdr_out', hdr_out)
            self.setData('spparams_out', spparams_out)

        return 0
