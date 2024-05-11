import matplotlib.pyplot as plt
import csv
import numpy as np

# 'data_test-15sec-ramp.csv'
def plot_data(file):
    x=[]
    y=[]
    z=[]
    r=[]

   

    with open(file, 'r' ) as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        next(csvfile)

        for row in plots:
            x.append(float(row[0]))  # Time
            y.append(float(row[3]))  #LIA component
            z.append(float(row[1]))  #LD Current
            r.append(float(row[2]))  #LD Temp
           




    # Throw away early values to stabilize LIA
    limit=100  

    x=x[limit:]
    y=y[limit:]
    z=z[limit:]
    r=r[limit:]


    #fit_ramp,fit_LIA,fit_timestamp,fit_temp=filter_ramp(x,y,z,r)
    x,y,z,r=filter_ramp(x,y,z,r,limit=1)


    fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(5)
    fig.subplots_adjust(hspace=1) 


    ax1.plot(x, y,'r-')
    ax1.set_ylabel('LIA - 12bit')
    ax1.set_xlabel('Time(Sec)')

    ax2.plot(x,z,'g.')
    ax2.set_ylabel('LD Current(mA)')
    ax2.set_xlabel('Time(Sec)')

    ax3.plot(x,r,'b')
    ax3.set_ylabel('Temp(°C)')
    ax3.set_xlabel('Time(Sec)')

   

    ax4.plot(z,y,'b,')    # plot RAMP-LIA
    X_out,Y_out=per_point_midvalue(z,y)
    ax4.plot(X_out,Y_out,'r.')


    #Point to select linear regression range
    fit_ramp=z
    fit_LIA=y

    
    #fit_ramp,fit_LIA=fit_select(X_out,Y_out,165,210,2)

    a, b = best_fit(fit_ramp,fit_LIA)  # Coefficients

    d = np.linspace(min(z),max(z),2)
    f = b*d+a       #line check


    ax4.plot(d, f, '-g.') # coefficient line check
    #ax4.plot(np.unique(fit_ramp), np.poly1d(np.polyfit(fit_ramp, fit_LIA, 1))(np.unique(fit_ramp)),'r') #regression line


    ax4.set_ylabel('LIA')
    ax4.set_xlabel('LD Current(mA) y='+''+"{0:.2f}".format(b)+'x+'+"{0:.2f}".format(a))




    
    ## DATA HANDLING
    line2x=[min(z),max(z)]
    line2y=[1,1]

    ax5.plot(line2x, line2y, '-c') # coefficient line check  - 1 straight


    processed=[]
    #for value in range(len(z)):
        #processed.append(y[value]/(b*z[value]+a))

    for value in range(len(X_out)):
        processed.append(Y_out[value]/(b*X_out[value]+a))

    ax5.plot(z,processed,'r.')  # Value substraction plot



    plt.show()

  
    
def fit_select(x,y,lim_min,lim_max,range_lim):  # select values on specific points +- range
    fit_x=[]
    fit_y=[]
    for i in range(len(x)):      
        if lim_min-range_lim<=x[i]<=lim_min+range_lim or lim_max-range_lim<=x[i]<=lim_max+range_lim:
            fit_x.append(x[i])
            fit_y.append(y[i])
    return  fit_x,fit_y


def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    return a, b


def per_point_midvalue(X,Y):
    X_out=[]
    Y_out=[]
    for value in X:
        meanlist=list_duplicates_of(X, value)
        #print(value)
        valuelist=[]
        for ind in range(len(meanlist)):
            valuelist.append(Y[meanlist[ind]])
        #print(meanlist)
        X_out.append(value)
        Y_out.append(np.mean(valuelist))
    return X_out,Y_out


def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def filter_ramp(x,y,z,r,limit):
    fit_ramp=[]
    fit_LIA=[]
    fit_timestamp=[]
    fit_temp=[]
    limited=[]
    for value in range(len(z)):
        if z[value]>min(z)+limit and z[value]<max(z)-limit:
            fit_ramp.append(z[value])
            fit_LIA.append(y[value])
            fit_timestamp.append(x[value]-x[1])
            fit_temp.append(r[value])
    return fit_timestamp,fit_LIA,fit_ramp,fit_temp



if __name__ == '__main__':
 

    #plot_data('co2_16-36-35.csv')
    #plot_data('test.csv')
    #plot_data('n2o_13-14-49.csv')

    #plot_data('ch4_14-07-13.csv')  #ch4 10 ramp

    #plot_data('co2_15-36-48.csv')
    #plot_data('ch4_16-12-19 - 1200.csv') #huge
    #plot_data('co2_12-15-24.csv')

    #plot_data('ch4_13-31-43.csv')  

    #plot_data('ch4_14-31-22.csv') 
    
    #plot_data('ch4_16-39-54.csv')  # Ramp visible

   #plot_data('ch4_11-16-07.csv')  #100 step
    
    #plot_data('ch4_11-29-00.csv') #50 step

    #plot_data('co2_11-57-13.csv') #50 step C02


    #plot_data('ch4_12-14-51.csv') #10 step CH4,600sec
   
    #plot_data('ch4_12-40-21.csv') #25 step CH4 ,1200sec
    
    #plot_data('ch4_13-14-19.csv') 
    
    #plot_data('ch4_14-20-44.csv')   
    #plot_data('co2_14-41-41.csv')   

    #plot_data('ch4_14-23-54.csv')   
    

    plot_data('ch4_p14.01_22-36-41.csv')
    

    #plot_data('n2o_12-55-06 - No LD output - Clear sig check.csv')

