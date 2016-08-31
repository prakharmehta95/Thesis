# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:02:59 2015

@author: stevekimbrough

File: pandasreadexcel.py from pandasexcel.py
"""
#%%
import pandas as pd
import matplotlib.pyplot as plt


#%%

xlsxDf = pd.read_excel('../../data/Riyadh_Typ_Office_net_zero.xlsx',
                       sheetname='Sheet1',header=3, 
                       parse_cols=[1,2,3,4,5,7,9,10,11,12,14,15,
                                   16,17,18],
                    skip_footer=6)
df = xlsxDf.copy()

def printColumnIndexes():
    for i in range(len(df.columns)):
        print('Column %d has header %s.' % (i,df.columns[i])) 
        
#%%        
def getMaxMinOne(x):
    '''
    Given a pandas Series object, or DataFrame
    object with one column, x, return
    its maximum and minimum values as a 
    tuple: (max,min).
    '''
    return (x.max()[0],x.min()[0])
    #return (x.values.max(axis=0),x.values.min(axis=0))
    
def getMaxMinMany(x):
    '''
    Given a pandas DataFrame object
    with possibly many columns, x, return
    the maximum and minimum values as a 
    tuple: (maxa,mina) in which maxa (mina) 
    are arrays of columns.
    '''
    return (x.values.max(axis=0),x.values.min(axis=0))
    
def batteryWithSupply(demand,solarSupply,extSupply):
    '''
    Given demand, the hourly demands for electric power,
    solarSupply, the hourly supply of solar power, and
    extSupply, a constant value of externally supplied
    electric power, returns a tuple: (maxover, maxunder)
    in which maxover is the maximum excess demand
    acumulating over the year, and maxunder is the 
    smallest overage (a negative number) occurring over
    the year, indicating excess power waiting to be used.
    '''
    reducedDemand = demand.iloc[:,0] - extSupply
    netDemand = reducedDemand - solarSupply.iloc[:,0]
    netDemandCumSum = netDemand.cumsum()
    return (netDemandCumSum.max(), netDemandCumSum.min())

def batteryWithPSupplyIdx(demand,solarSupply,extSupply,pSupply):
    '''
    Given demand, the hourly demands for electric power,
    solarSupply, the hourly supply of solar power, and
    extSupply, a constant value of externally supplied
    electric power, returns a 3-tuple: 
    ((maxover, maxunder),(maxoveridx, maxunderidx),
    netDemand, netDemandCumSum)
    in which maxover is the maximum excess demand
    acumulating over the year, maxoveridx is its index
    value, maxunder is the 
    smallest overage (a negative number) occurring over
    the year, indicating excess power waiting to be used,
    maxunderidx is its index value, netDemand is the
    net demand (by hour), and netDemandCumSum
    is the cumulative sum of the net demand.
    
    Very similar to batteryWithPSupplyIdx, but now in
    the calculations solarSupply is scaled by pSupply >= 0.
    '''
    reducedDemand = demand.iloc[:,0] - extSupply
    netDemand = reducedDemand - (solarSupply.iloc[:,0]*pSupply)
    netDemandCumSum = netDemand.cumsum()
    return ((netDemandCumSum.max(),netDemandCumSum.min()),
            (netDemandCumSum.idxmax(),netDemandCumSum.idxmin()),
            netDemand, netDemandCumSum)
            
#%%
        
def plotDemand(start,stop):
    # Begin a new figure:
    plt.figure()
    # Column 11 has header Energy Demand (kW).
    demand = df.ix[start:stop,11]
    plt.plot(demand)
    plt.title('Hourly demand for hours ' + str(start) + ' to ' + str(stop))
    plt.xlabel('Hours plus ' + str(start))
    plt.ylabel('Kilowatts demanded')
    plt.show()

def plotDemandInsolation(start,stop):
    '''
    Use e.g. plotDemandInsolation(24*300,24*302)
    '''
    # Begin a new figure:
    plt.figure()
    # Column 11 has header Energy Demand (kW).
    demand = df.ix[start:stop,11]
    plt.plot(demand,'r-+',label='Demand (kW)')
    # Column 4 has header Riyadh global horizontal radiation (W).
    insolation = df.ix[start:stop,4]  #/1000.0
    plt.plot(insolation,'g-+',label='Insolation (W)')
    plt.legend(loc=0)
    plt.title('Hourly demand and insolation for hours ' + str(start) + ' to ' + str(stop))
    plt.xlabel('Hours plus ' + str(start))
    plt.ylabel('Kilowatts/watts')
    plt.savefig('DemandInsolation'+str(start) + '-' + str(stop) + '.pdf')
    plt.show()
#%%           
if __name__ == '__main__':
    print("Yo!")
    print(df.columns)
            
#   fig, (ax1, ax2) = plt.subplots( nrows=2, ncols=1 )  # create figure & 1 axis
#    ax1.set_title("Lefties' confusion lags on top, Righties' on bottom.")
#    ax1.plot(bob,'k')
#    ax2.plot(carol,'k')
#    fig.savefig('confusions_lags_plot.pdf')   # save the figure to file path/to/save/image/
#    plt.close(fig)  
            
#plt.figure()
#p1 = plt.plot(df['signal_0_0'],'g',label='Green')
#p2 = plt.plot(df['signal_0_1'],'y',label='Yellow')
#p3 = plt.plot(df['signal_0_2'],'r',label='Red')
#plt.legend(loc=0)
#plt.title('Caste 0 (low aggression) signaling over time.')
#plt.ylim(-100,700)
#plt.savefig('Caste0SignalingOverTime.pdf')
#plt.show()