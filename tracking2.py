import numpy as np 
import dish
import time
import threading
import takespec
import dish_synth
import sys
import ephem
import gzip 

#generate lists of pointings in terms of galactic coords 

#b_list = [-20., -18., -16., -14., -12., -10., -8., -6., -4., -2., 0., 2., 4., 6., 8., 10., 12., 14., 16., 20.]
#b_coord = [] 
#l_coord = []    

#for i in range(20, 170, 4): 
#    l = i 
#    for k in range(0, len(b_list), 1):
#        b = b_list[k] 
#        b_coord.extend([b]) 
#        l_coord.extend([l]) 
#
#
#for n in range(190, 230, 4): 
#    m = n    
#    for j in range(0, len(b_list), 1):
#        b = b_list[j]
#        b_coord.extend([b])
#        l_coord.extend([m])   
       
#np.savetxt('gal_lat_b_Apr_29_2.gz', b_coord) 
#np.savetxt('gal_long_l_Apr_29_2.gz', l_coord) 


#determining alt,az for pointing 

def gal_to_eq(b_lat, l_long):
    open('alt_list.txt', 'w')  
    open('az_list.txt', 'w') 

    R = np.zeros([3,3])
    R[0] = [-0.054876, -0.873437, -0.483835]
    R[1] = [0.494109, -0.444830, 0.746982]
    R[2] = [-0.867666, -0.198076, 0.455984]
    trans_R = np.transpose(R)

    x = np.zeros([3,960])
    x[0] = np.cos(b_lat)*np.cos(l_long)
    x[1] = np.cos(b_lat)*np.sin(l_long)
    x[2] = np.sin(b_lat)

    A = np.dot(trans_R, x) 

    obs = ephem.Observer()
    obs.lat = 37.8732*np.pi/180
    obs.long = -122.2573*np.pi/180
    lst = obs.sidereal_time()

    R_1 = np.zeros([3,3])
    R_1[0] = [np.cos(lst), np.sin(lst), 0]
    R_1[1] = [np.sin(lst), -1*np.cos(lst), 0]
    R_1[2] = [0,0,1]

    B = np.dot(R_1, A)

    lat = 37.8732*np.pi/180

    R_2 = np.zeros([3,3]) 
    R_2[0] = [-1*np.sin(lat), 0, np.cos(lat)]
    R_2[1] = [0, -1, 0]
    R_2[2] = [np.cos(lat), 0, np.sin(lat)] 

    C = np.dot(R_2, B) 

    alt = np.arctan2(C[1], C[0])
    az = np.arcsin(C[2])
    alt_list = alt*(180/np.pi)
    az_list = az*(180/np.pi)

    np.savetxt('alt_list.txt', alt_list)
    np.savetxt('az_list.txt', az_list) 
     

       
def data_taker():
    #clear all files where data will be recorded 
    gzip.open('pointing_az_low_freq_noise_on_Apr_29.gz', 'wt')
    gzip.open('pointing_alt_low_freq_noise_on_Apr_29.gz', 'wt')
#    gzip.open('LST_low_freq_noise_on_Apr_29.gz', 'wt')
    gzip.open('spec_low_freq_noise_on_Apr_29.gz', 'wb') 
    gzip.open('pointing_az_low_freq_noise_off_Apr_29.gz', 'wt')
    gzip.open('pointing_alt_low_freq_noise_off_Apr_29.gz', 'wt')
#    gzip.open('LST_low_freq_noise_off_Apr_29.gz', 'wt')
    gzip.open('spec_low_freq_noise_off_Apr_29.gz', 'wb')
    gzip.open('pointing_az_up_freq_noise_on_Apr_29.gz', 'wt')
    gzip.open('pointing_alt_up_freq_noise_on_Apr_29.gz', 'wt')
#    gzip.open('LST_up_freq_noise_on_Apr_29.gz', 'wt')
    gzip.open('spec_up_freq_noise_on_Apr_29.gz', 'wb')
    gzip.open('pointing_az_up_freq_noise_off_Apr_29.gz', 'wt')
    gzip.open('pointing_alt_up_freq_noise_off_Apr_29.gz', 'wt')
#    gzip.open('LST_up_freq_noise_off_Apr_29.gz', 'wt')
    gzip.open('spec_up_freq_noise_off_Apr_29.gz', 'wb')
    #let's create a dish first
    d = dish.Dish(verbose=True)
    s = dish_synth.Synth()
    obs = ephem.Observer()
    obs.lat = 37.832*np.pi/180 
    obs.long = -122.2573*np.pi/180
    #d.home() 
    s.set_amp(10.0) 
    b_lat = np.loadtxt('gal_lat_b_Apr_29_1.gz') 
    l_long = np.loadtxt('gal_long_l_Apr_29_1.gz')     
    for i in range (0, len(l_long), 1):
        #update pointing                
        gal_to_eq(b_lat, l_long)
        az_list = np.loadtxt('az_list.txt')
        alt_list = np.loadtxt('alt_list.txt') 
        #noise on, lower center frequency
        #s.set_freq(1422.4)
        s.set_freq(1272.4)
        s.set_amp(10.0)
        d.noise_on()
        try:         
            d.point(az_list[i], alt_list[i])
            np.savetxt('pointing_alt_low_freq_noise_on_Apr_29.gz', alt_list[i])
            np.savetxt('pointing_az_low_freq_noise_on_Apr_29.gz', az_list[i])
        except ValueError:
            print "invalid pointing, skipping point"
            pass
        try:
            takespec.takeSpec('spec_low_freq_noise_on_Apr_29.gz', numSpec=80)
            LST = obs.sidereal_time() 
            np.savez('LST_low_freq_noise_on_Apr_29.npz', LST)
        except ValueError:
            print "Could not take spectra, skipping point"
            pass
        time.sleep(5)
              
        #No noise, lower center frequency
        d.noise_off()
        try:
            d.point(az_list[i], alt_list[i])
            np.savetxt('pointing_alt_low_freq_noise_off_Apr_29.gz', alt_list[i])
            np.savetxt('pointing_az_low_freq_noise_off_Apr_29.gz', az_list[i])
        except ValueError:
            print "invalid pointing, skipping point"
            pass
        
        try:
            takespec.takeSpec('spec_low_freq_noise_off_Apr_29.gz', numSpec=180)
            LST = obs.sidereal_time()
            np.savez('LST_low_freq_noise_off_Apr_29.npz', LST)
        except ValueError:
            print "Could not take spectra, skipping point"
            pass
        time.sleep(5)
                
        #no noise, upper center frequency
        #s.set_freq(1418.4)
        s.set_amp(10.0)
        s.set_freq(1268.4)
        d.noise_off()                    
        try:
            d.point(az_list[i], alt_list[i])
            np.savetxt('pointing_alt_up_freq_noise_off_Apr_29.gz', alt_list[i])
            np.savetxt('pointing_az_up_freq_noise_off_Apr_29.gz', az_list[i])
        except ValueError:
            print "invalid pointing, skipping point"
            pass
        try:
            takespec.takeSpec('spec_up_freq_noise_off_Apr_29.gz', numSpec=180)
            LST = obs.sidereal_time()
            np.savez('LST_up_freq_no_noise_Apr_29.npz', LST)
        except ValueError:
            print "Could not take spectra, skipping point"
            pass
        time.sleep(5)

        #noise, upper center frequency                       
        d.noise_on()
        try:
            d.point(az_list[i], alt_list[i])
            np.savetxt('pointing_alt_up_freq_noise_on_Apr_29.gz', az_list[i])
            np.savetxt('pointing_az_up_freq_noise_on_Apr_29.gz', alt_list[i])
        except ValueError:
            print "invalid pointing, skipping point"
            pass
        try:
            takespec.takeSpec('spec_up_freq_noise_on_Apr_29.gz', numSpec=80)
            LST = obs.sidereal_time()
            np.savez('LST_up_freq_noise_on_Apr_29.npz', LST)
        except ValueError:
            print "Could not take spectra, skipping point"
            pass
        time.sleep(5)

###### 


 
time.sleep(5) 
data_taker()


              

#now that everything has been defined, call functions
#record all outputs to a text file  
 
#with  open('obs_log_Apr_24.txt', 'w') as out: 
 #   sys.stdout = out
#data_taker()
#log_file.close() 
                

                
                
                
                
                
                
                
                
