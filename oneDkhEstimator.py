#Parameter Estimation Code. This code uses the flux adiabatic model. To run the code. Set the file directiories,
#adjust for material and tests to run, and then execute the code.
#
# This code is copyrighted by the authors, but released under the MIT
# license:
#
# Copyright (c) 2020 -- oneDkhEstimator.py
#
# S&T and the University of Missouri Board of Curators
# license to you the right to use, modify, copy, and distribute this
# code subject to the MIT license:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
import sys
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import time #to allow time stamp on output
import numpy as np
from numpy import array
from xlwt import Workbook # Writing to an excel
import array as arr
cur_version = sys.version_info # Test for Python version:
wb = Workbook() # Workbook is created

#select files to run. Files must be a .txt format with time, temperature
filefolder="S:\\Parameter Estimation\\research\\data\\datamarch\\" #location of data
excelsaveloc="S:\\Parameter Estimation\\research\\results\\datamarch\\" #location to save excel file of results
plotsaveloc="S:\\Parameter Estimation\\research\\results\\datamarch\\" #location to save plots

filesave='sstest'  #Excel filename

# Select Wind or Temperature Test

#Wind = True
Temp = True

# Select material:

#Al = True
#SS = True
Cu = True

try:
    SS
except NameError:
    try:
        Al
    except NameError:
        try:
            Cu
        except NameError:
            print("Incorrect Material Definition")
        else:
            Al = False
            SS = False
    else:
        Cu = False
        SS = False
else:
    Al = False
    Cu = False

try:
    Wind
except NameError:
    try:
        Temp
    except NameError:
        print("Incorrect Test Definition")
    else:
        Wind = False
else:
    Temp = False

if Cu == True:
#material properties and files to run
#copper
#X=[0,0.02013,0.02966,0.03982,0.05019,0.0607]
    X=[0.000,0.015,0.030,0.045,0.060,0.075] #thermocouple locations in meters
    if Temp == True:
        filenames=['50cu1','50cu2','50cu3','75cu1','75cu2','75cu3','100cu1','100cu2','100cu3'] #list of files to run
        VV=[5,5,5,5,5,5,5,5,5]  #wind speed guess
        ymax=[60,60,60,90,90,90,120,120,120] #yaxis maximum temperature
        Tinf=20.5
    if Wind == True:
        filenames=['cu1','cu2','cu3','cu4','cu5','cu6','cu7','cu8','cu9','cu10'] #list of files to run
        VV=[1,2,3,4,5,6,7,8,9,10]  #wind speed guess
        ymax=[90,90,90,90,90,90,90,90,90,90] #yaxis maximum temperature
        Tinf=20.6
    #filenames=['100cu3']
    #ymax=[120]
    rho=8912.93 #density
    D=0.003175 #rod diameter
    L=0.150 #length
    c=384.93 # specific heat
    pT=300 #plot time seconds

if Al == True:
    #aluminum
    X=[0,0.01,0.02,0.03,0.04,0.05]
    if Temp == True:
        filenames=['50al1','50al2','50al3','75al1','75al2','75al3','100al1','100al2','100al3'] #list of files to run
        VV=[5,5,5,5,5,5,5,5,5]  #wind speed guess
        ymax=[60,60,60,90,90,90,120,120,120] #yaxis maximum temperature
        Tinf=20.5
    if Wind == True:
        filenames=['al1','al2','al3','al4','al5','al6','al7','al8','al9','al10'] #list of files to run
        VV=[1,2,3,4,5,6,7,8,9,10]  #wind speed guess
        ymax=[90,90,90,90,90,90,90,90,90,90] #yaxis maximum temperature
        Tinf=20.6
    #filenames=['100al3']
    #ymax=[120]
    rho=2767.99 #density
    D=0.003175 #rod diameter
    L=0.150 #length
    c=896 # specific heat
    pT=300 #plot time seconds

if SS == True:
#stainless steel
    X=[0,0.007,0.014,0.021,0.028,0.035]
    if Temp == True:
        filenames=['50ss1','50ss2','50ss3','75ss1','75ss2','75ss3','100ss1','100ss2','100ss3'] #list of files to run
        VV=[5,5,5,5,5,5,5,5,5]  #wind speed guess
        ymax=[60,60,60,90,90,90,120,120,120] #yaxis maximum temperature
        Tinf=20.5
    if Wind == True:
        filenames=['ss1','ss2','ss3','ss4','ss5','ss6','ss7','ss8','ss9','ss10'] #list of files to run
        VV=[1,2,3,4,5,6,7,8,9,10]  #wind speed guess
        ymax=[90,90,90,90,90,90,90,90,90,90] #yaxis maximum temperature
        Tinf=21.2
    #filenames=['100ss1']
    #ymax=[120]
    rho=8030 #density
    D=0.003175 #rod diameter
    L=0.150 #length
    c=502 # specific heat
    pT=800 #plot time seconds

# Define the model:
A=np.pi*D**2/4
s=np.pi*D
N=100 #Number of terms in Fourier Series
#adding labels to excel document
labels=['Transient model','h','k','Pss','standard_error','h error','k error','Pss error'] #labels for results
sheet1 = wb.add_sheet(filesave)
labels2=['N']
labels0=['Finite difference boundary model','Power','alpha','tau','sig','Power error','alpha error','tau error']
labels01=['Steady state model','Pss','j','sig','Pss error','j error']
labels2.extend(labels0)
labels2.append(' ')
labels2.extend(labels01)
labels2.append(' ')
labels2.extend(labels)
sheet1.write(0, 0, 'Variable')
for i in range(0,len(labels2)):
    sheet1.write(i+1, 0, labels2[i])
for mm in range(0,len(filenames)): #cycles through array of filenames
    v=VV[mm] #windspeed
    filename=filenames[mm]
    sheet1.write(0, mm+1, filenames[mm])
    # Create empty lists:
    TT = [[],[],[],[],[],[]]
    xx = [[],[],[],[],[],[]]
    t = []
    T=[]
    x=[]
    Tss=[]
    xss=[]

    # Set the desired resolution:
    res = 5000# Dpi.  Fine for EPS, but should use higher for PNG.

    infile=filefolder+filename+".txt"
    #plotname = ("S:\\Parameter Estimation\\research\\results\\datamarch\\"+filename+"5")
    plotname = (plotsaveloc+filename) #plot save location
    try:
        data = open(infile, "r")# get array out of input file
    except:
        print ("Cannot find input file; Please try again.")
        sys.exit(0)

    data.seek(0) # Reset file pointer to the beginning
    linecount = 0

    # Read the data from the input file:
    if cur_version[0]==3:# This is necesary due to the change in the type
        for line in data:# returned by the map function in Python 3.x.x.
            linedat = list(map(float, line.split()))
            t.append(linedat[0])
            for i in range(0, 6):
                TT[i].append(linedat[i+1])
            for i in range(6, 12):
                xx[i-6]=([X[i-6]]*len(t))
            linecount += 1
    else:
        for line in data:
            t.append(map(float, line.split())[0])
            for i in range(0, 6):
                TT[i].append(map(float, line.split())[i+1])
            for i in range(6, 12):
                xx[i-6]=([X[i-6]]*len(t))
            linecount += 1
    # Close the input file:
    data.close()

    #Arranging data into three column matrices
    sheet1.write(1, mm+1, N)
    T=array(TT[0])
    x=array(xx[0])
    tt = np.concatenate((array(t),array(t),array(t),array(t),array(t),array(t)),axis=0)
    for i in range(1,6):
        T=np.concatenate((T,array(TT[i])),axis=0)
    for i in range(1,6):
        x=np.concatenate((x,array(xx[i])),axis=0)

    #h initial guess
    rhoair=1.23
    muair=1.789*10**(-5)
    Re=rhoair*v*D/muair
    Pr=0.71
    kair=0.02602
    h0=kair/D*(0.3+0.62*Re**(0.5)*Pr**(1.0/3)/(1+(0.4/Pr)**(2.0/3))**(0.25)*(1+(Re/282000)**(5.0/8))**(-4.0/5))


    #Finite difference of boundary
    #B=(array(TT[0])-array(TT[1]))/X[1] #first order accurate
    Boundrymodel=(3*array(TT[0])-4*array(TT[1])+array(TT[2]))/(2*X[1]) #second order accurate
    def f0(V): #variables are scaled so that they are on the same order of magnitude
        return V[0]*(1-np.exp(-V[1]/10000*(array(t)+V[2]/10)))-Boundrymodel
    output0 = leastsq(f0,[1000,0.05,10], args=(), full_output=1)
    err20 = np.sqrt(output0[2]['fvec']*output0[2]['fvec']) #Squared deviations
    sig0 = np.sqrt(sum(err20)/(len(err20)-3)) # Unbiased uncertainty estimate
    cov0 = output0[1]
    errors0=1.96*sig0*np.sqrt(cov0)
    values0 = arr.array('d',output0[0]) # Optimal parameters
    values0.append(sig0)
    values0.extend([errors0[0,0],errors0[1,1],errors0[2,2]])
    scales=[1,10000,10,1,1,10000,10] #scales for the parameters
    print(labels0[0])
    for j in range(0,len(values0)):
        print(labels0[j+1]+' = {}'.format(values0[j]/scales[j]))
        sheet1.write(j+3, mm+1, values0[j]/scales[j])

    ap=values0[1]/scales[1]   #alpha
    tau=values0[2]/scales[2]  #tau

        #steadystatedata
    T0=sum(TT[0][-20:])/len(TT[0][-20:])
    Tss=array(TT[0][-20:])
    xss=array(xx[0][-20:])
    for i in range(1,6):
        Tss=np.concatenate((Tss,array(TT[i][-20:])),axis=0)
    for i in range(1,6):
        xss=np.concatenate((xss,array(xx[i][-20:])),axis=0)

    #steady state model
    def f01(V):
        m=np.sqrt(4*V[1]/D)
        return V[0]/m*np.cosh(m*(L-xss))/np.sinh(m*L)-Tss
    output01 = leastsq(f01, [50,10], args=(), full_output=1)
    err201 = np.sqrt(output01[2]['fvec']*output01[2]['fvec']) #Squared deviations
    sig01 = np.sqrt(sum(err201)/(len(err201)-2)) # Unbiased uncertainty estimate
    cov01 = output01[1]
    errors01=1.96*sig0*np.sqrt(cov01)
    values01 = arr.array('d',output01[0]) # Optimal parameters
    values01.append(sig01)
    values01.extend([errors01[0,0],errors01[1,1]])
    print(labels01[0])
    for j in range(0,len(values01)):
        print(labels01[j+1]+' = {}'.format(values01[j]))
        sheet1.write(j+5+len(values0), mm+1, values01[j])

    k0=h0/values01[1] #initial guess thermal conductivity
    Pguess=values01[0]*k0*A #power initial guess

    #transient model
    def f(V,tT,XX,TTT):
        nu=(V[0]*s)/(rho*A*c)
        K=V[1]/(rho*c)
        Pss=V[2]
        total=np.zeros(np.size(tT))
        for n in range(1,N+1):
            beta = n*np.pi*np.sqrt(K)/(L)
            total=total+np.multiply(2*K*Pss*((-beta**2 - nu)*np.exp((-beta**2 - nu)*tT - ap*tau)
            + (beta**2 - ap + nu)*np.exp(-tT*(beta**2 + nu)) + (beta**2 + nu)*np.exp(-ap*(tT + tau)) - beta**2 + ap - nu)
            /(V[1]*L*A*(-beta**2 + ap - nu)*(beta**2 + nu)),np.cos(beta/np.sqrt(K)*XX))
        return -(np.exp(-ap*tau - nu*tT)*nu - np.exp(-ap*(tT + tau))*nu + (ap - nu)*(np.exp(-nu*tT) - 1))*Pss*K/(V[1]*L*A*nu*(ap - nu))+total-TTT
    x0=[h0,k0,Pguess] #x0=[h,k,Pss]
    # Find the best values
    output = leastsq(f, x0, args=(tt,x,T), full_output=1)
    err2 = np.sqrt(output[2]['fvec']*output[2]['fvec']) #Squared deviations
    sig = np.sqrt(sum(err2)/(len(err2)-len(x0))) # Unbiased uncertainty estimate
    cov = output[1]
    errors=1.96*sig*np.sqrt(cov)
    values = arr.array('d',output[0]) # Optimal parameters
    values.append(sig)
    values.extend([errors[0,0],errors[1,1],errors[2,2]])
    print(labels[0])
    for j in range(0,len(values)):
        print(labels[j+1]+' = {}'.format(values[j]))
        sheet1.write(j+len(values0)+7+len(values01), mm+1, values[j])

    # Plot the model and the data for comparision:
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_size(12)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(array(t), array(TT[0])+Tinf, 'k.', label='Experimental Data',markersize=3)
    ax.plot(array(t), f([values[0],values[1],values[2]],array(t),array(xx[0]),np.zeros(np.size(array(t))))+Tinf, '-r', label='Model',linewidth=2)
    ax.set_xlim(0, pT)
    ax.set_ylim(20, ymax[mm])
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    for tick in ax.get_xticklabels():
        tick.set_fontname('Times New Roman')
    for tick in ax.get_yticklabels():
        tick.set_fontname('Times New Roman')

#Locations for TC labels
    for i in range(0, 6): #locations for TC# labels
        ax.plot(array(t), array(TT[i])+Tinf, 'k.',markersize=4)
        ax.plot(array(t), f([values[0],values[1],values[2]],array(t),array(xx[i]),np.zeros(np.size(array(t))))+Tinf, '-r',linewidth=2)
        ax.text(pT, TT[i][-1]-4+Tinf, 'TC '+ str(i+1), verticalalignment='bottom', horizontalalignment='right', fontproperties=font)

#individually adjust TC labels
    """
    for i in range(0, 6):
        ax.plot(array(t), array(TT[i])+Tinf, 'k.',markersize=4)
        ax.plot(array(t), f2([values[0],values[1],values[2]],array(t),array(xx[i]),np.zeros(np.size(array(t))))+Tinf, '-r',linewidth=2)
    #locations for TC# labels
    ax.text(pT, TT[0][-1]-1.7+Tinf, 'TC '+ str(1), verticalalignment='top', horizontalalignment='right', fontproperties=font)
    ax.text(pT, TT[1][-1]-1.4+Tinf, 'TC '+ str(2), verticalalignment='top', horizontalalignment='right', fontproperties=font)
    ax.text(pT, TT[2][-1]-1.2+Tinf, 'TC '+ str(3), verticalalignment='top', horizontalalignment='right', fontproperties=font)
    ax.text(pT, TT[3][-1]-1.5+Tinf, 'TC '+ str(4), verticalalignment='top', horizontalalignment='right', fontproperties=font)
    ax.text(pT, TT[4][-1]-0.4+Tinf, 'TC '+ str(5), verticalalignment='top', horizontalalignment='right', fontproperties=font)
    ax.text(pT, TT[5][-1]-1.2+Tinf, 'TC '+ str(6), verticalalignment='top', horizontalalignment='right', fontproperties=font)
    """

    plt.legend(loc='upper left', shadow=False, prop=font,frameon=False)
    plt.xlabel('Time (s)', fontproperties=font)
    plt.ylabel('Temperature ($^o$C)', fontproperties=font)
    ax.grid(False)
    # Put a nice background color on the legend:
    #legend.get_frame().set_facecolor('#00FFCC')
    # Add date and time in plot title:
    loctime = time.asctime(time.localtime(time.time()))
    plotname = plotname+".EPS"
    plt.savefig(plotname,format='eps', dpi=res)   #save plot
    plt.show()# Show the plot
#save excel file
wb.save(excelsaveloc+filesave+".xls")
