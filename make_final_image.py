import numpy as np
import matplotlib.pyplot as pylab 
import math
import scipy.signal

#want to eventually graph vertical axis = b, horizontal axis = d, color = temperature 
#d has size (35, 2000)
#b has size (35)
#temp has size (35, 2000)



file = np.load('May_4_final_final.npz')

b_file = file['b'] 
b_list = []
d_file = file['Distance'] 
d_list = []
temp_file = file['Temp'] 
temp_list = []  
h_list=[]

for i in range(len(b_file)):
    b = b_file[i]
    d_array = d_file[i]
    temp = temp_file[i]
    for k in range(0, 2000): 
        b_list.extend([b*np.pi/180.])
        if math.isnan(d_array[k])==True:
            d_list.extend([0.]) 
        elif abs(d_array[k]) > 30.: 
            d_list.extend([0.]) 
        else:
            d_list.extend([d_array[k]])
        if math.isnan(temp[k])==True:
            temp_list.extend([0.])
        elif temp[k] < 0.0: 
            temp_list.extend([0.0])
        else:
            temp_list.extend([temp[k]]) 

for i in range(len(b_list)): 
    h = d_list[i]*np.tan(b_list[i]) 
    if math.isnan(h)==True:
        h_list.extend([0.]) 
    else: 
        h_list.extend([h]) 

#pylab.plot(d_file, h_list)
#pylab.xlabel('Distance from Earth (in kpc)')
#pylab.ylabel('Distance from $b$ = 0$^{\circ}$ (in kpc)')
#pylab.title('Observed Section of Galaxy at $l$ = 75$^{\circ}$')
#pylab.show()
 
#print h_list   




#create grid with 200 data points up and down (-10kpc to 10kpc for 0.1 kpc resolution)
img = np.zeros((201,251))
wt = np.zeros((201,251))

data = temp_list

#print np.shape(temp_list) 
#np.transpose(d_list)  

#print np.shape(d_list)
#print np.shape(h_list)




#print data 

#each data value is also an array - will need to account for that too 
for i in xrange(len(d_file)):
    d_vals = d_file[i] 
    #print d_vals
    b_vals = b_file[i]
    h_vals = d_vals*np.tan(b_vals*np.pi/180.) 
    temp_vals = temp_file[i] 
    for j in xrange(d_vals.size):
        if math.isnan(d_vals[j])==True: continue 
        if math.isnan(temp_vals[j])==True: continue 
        x_pos = np.rint(d_vals[j]/0.1)
        y_pos = np.rint(h_vals[j]/0.1) +100   #shifts the zero point to the 100th row in our image
        temp_1 = temp_vals[j] 
        x_pos_1 = 0
        y_pos_1 = 0 

        if abs(x_pos) > 250.: 
            x_pos_1 = 0.0
        else:
            x_pos_1 = x_pos
        
        if abs(y_pos) > 200.:
            y_pos_1 = 0.0
        else:
            y_pos_1 = y_pos

    #   print i, x_pos_1, y_pos_1, data_val
                                  #which corresponds to zero in H
        img[y_pos_1, x_pos_1] += temp_1 #record brightness temperature in appropriate location on 
                                 #image grid
        wt[y_pos_1, x_pos_1] += 1        #record that a data point was stored in that location
 

ker = np.zeros((41, 41)) 
sigma = 2.5 #.25 kpc at .1 kpc per pixel 


for i in xrange(-20, 21): 
    for j in xrange(-20, 21):
        ker[j+20, i+20] += np.exp((-(i**2/(2*sigma**2) + j**2/(2*sigma**2))))


print np.shape(img)
print np.shape(ker) 
    

image = scipy.signal.convolve2d(img, ker, mode='same')
print 'image done'


weight = scipy.signal.convolve2d(wt, ker, mode='same')

image[np.where(weight < 0.001)] = 0.0 
weight[np.where(weight < 0.001)] = 1.0 

print 'weight done'
fin_img = image/weight
print 'fin img done' 

np.savez('fin_img_data.npz', fin_img) 

#pylab.plot(d_list, h_list)

#pylab.imshow(image, cmap = 'hot') 

#pylab.imshow(weight, cmap = 'Greys')

pylab.imshow(fin_img, cmap='gist_gray', vmin = 0, extent = (0, 25, -10, 10))

pylab.colorbar()

pylab.xlabel('Distance from Earth (in kpc)')
pylab.ylabel('Height above/below Galactic Plane (in kpc)')
pylab.title('HI Emission at $l$ = 75$^{\circ}$')

#pylab.ylim(-40, 40)
#pylab.xlim(0, 30)

pylab.show() 




