import numpy as np
import os
import time
import threading
import dish
import takespec
import dish_synth


class tracking:
    #create a dish
    def _init_(self, ra= None, dec = None, lo_amp = None, lo_freq = None):
        self.dish = dish.Dish()
        self.dish.noise_off()
      #set the LO  
    def set_lo(self, amp = None, freq = None):
        self.synth = dish_synth.Synth()
        self.synth.set_amp(amp)
       self.synth.set_freq(freq)
      #point the telescope. need to convert from radec to azalt
    def point():
        alt = convert(ra)
        az = convert(dec)
        self.dish.point(alt, az)
    #begin 
    def track(self):
        self.dish.home()
        self.set_lo(lo_amp, lo_freq)
        self.point()
        takespec.takeSpec(args)
        
        
        
    
        