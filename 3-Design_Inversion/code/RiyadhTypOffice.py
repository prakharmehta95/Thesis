# -*- coding: utf-8 -*-
"""
Created on Mon May 23 15:18:01 2016

@author: stevenkimbrough
"""

import pandas as pd
import numpy as np
from collections import OrderedDict
import datetime

#%%

def getExcelData():
    '''
    This reads in John's version 3 Excel file, or rather the key
    data from it. I'll input the parameter values directly.
    '''
    xlsxDf = pd.read_excel('../data/Riyadh_Typ_Office_clculator_rev03.xlsx',
                       sheetname='Data',header=5, skiprows=[6],
                       parse_cols=[1,2,3,4,5,10,11], #,7,9,10,11,12,14,15,
                                   #16,17,18],
                    skip_footer=6)
    return xlsxDf

#### Old, mutilated code for reading the original workbook:
#def getExcelData():
#    xlsxDf = pd.read_excel('../data/Riyadh_Typ_Office_clculator_rev03.xlsx',
#                       sheetname='Inputs and Outputs',header=5, skiprows=[6],
#                       parse_cols=[1,2,3,4,5,7,9,10,11,12,14,15,
#                                   16,17,18],
#                    skip_footer=6)
#    return xlsxDf    
#########################

#%%
# Parameter values taken from '../data/Riyadh_Typ_Office_clculator_rev03.xlsx'

# PV collector efficiency	ratio	0.15
pVCollectorEfficiency = 0.15
# Area of PV	m**2	2000
areaOfPV = 2000
#	Expensive battery storage efficiency	0.95
ExpensiveBatteryStorageEfficiency	 = 0.95
#	Expensive battery extract efficiency	0.99
ExpensiveBatteryDischargeEfficiency = 0.99
#	Battery capacity (kWh)	 500
ExpensiveBatteryCapacity = 500.0

#	Cheap battery storage efficiency	0.30
CheapBatteryStorageEfficiency = 0.30
#	Cheap battery extract efficiency	0.99
CheapBatteryDischargeEfficiency = 0.99
#	Battery capacity (kWh)	1000
CheapBatteryCapacity = 1000.0
####################################

##

class Initialization():
    '''
    Use this class to initialize parameter values needed in the 
    simulation.
    '''
    def __init__(self,timeSteps=8760):
        # Set the number of time steps in the simulation. 
        # It's 8760 for one year of hours.
        self.timeSteps = timeSteps

settings = Initialization()

def makePVPower():
    '''
    Returns a DataFrame corresponding to columns N:S of John's
    worksheet, 'PV Power', neglecting column Q,
    'Need met  by PV (%)', which it seems isn't needed.
    '''
    definingDict = OrderedDict()
    pVEnergyGenerated = getPVEnergyGenerated()
    definingDict[pVEnergyGenerated.name] = pVEnergyGenerated
    energySupply = getEnergySupply(pVEnergyGenerated)
    definingDict[energySupply.name] = energySupply
    energyDemand = getEnergyDemand()
    definingDict[energyDemand.name] = energyDemand
    deficit,overSupply = getDeficitAndOverSupply()
    definingDict[deficit.name] = deficit
    definingDict[overSupply.name] = overSupply
    return pd.DataFrame(definingDict)
    
#%%
def makeExpensiveBatteryDF(steps=settings.timeSteps,
            capacity=ExpensiveBatteryCapacity,
            dischargeEfficiency=ExpensiveBatteryDischargeEfficiency):
    '''
    Creates, initializes, and returns a pandas DataFrame 
    corresponding to columns U:AJ in John Sullivan's v3 
    spreadsheet. That is, this holds the data for the
    model about using expensive storage first. The DataFrame
    retains columns that correspond to parameters,
    such as DischargeEfficiency, but seeks to generalize them.--NOT!!!
    '''
    definingDict = OrderedDict()
    U = 'Electricity Stored at Last Timestep'
    Uinit = np.ones((steps))*capacity
    definingDict[U] = Uinit
    V = 'Post-PV demand from building'
    #energyDemand = getEnergyDemand()
    deficit = PVPower['Deficit']
    definingDict[V] = deficit #energyDemand
    # Parameter W = 'Discharge efficiency'
    X = 'Is there 100% capacity in battery?'
    definingDict[X] = np.zeros(steps)
    Y = 'Transferred out of battery'
    definingDict[Y] = np.zeros(steps)
    Z = 'Supplied to building'
    definingDict[Z] = np.zeros(steps)
    AA = 'Electricity stored after supplying building'
    definingDict[AA] = np.zeros(steps)
    AB = 'Is there excess eletricity from PV?'
    definingDict[AB] = np.zeros(steps)
    AC = 'Electricity needed to refill battery'
    definingDict[AC] = np.zeros(steps)
    AD = 'Excess eletricity from PV'
    definingDict[AD] = np.zeros(steps)
    AF = '(Excess eletricity * efficiency)'
    definingDict[AF] = np.zeros(steps)
    
    AH = 'Supplied to Battery from PV'
    definingDict[AH] = np.zeros(steps)
    AG = 'Transferred from PV'
    definingDict[AG] = np.zeros(steps)
    AI = 'Electricity stored at end of timestep'
    definingDict[AI] = np.zeros(steps)
    AJ = 'Excess PV eletricity after charging'
    definingDict[AJ] = np.zeros(steps)
    
    return pd.DataFrame(definingDict)

def makeCheapBatteryDF(steps=settings.timeSteps,
            capacity=CheapBatteryCapacity,
            dischargeEfficiency=CheapBatteryDischargeEfficiency):
    '''
    Creates, initializes, and returns a pandas DataFrame 
    corresponding to columns U:AJ in John Sullivan's v3 
    spreadsheet. That is, this holds the data for the
    model about using expensive storage first. The DataFrame
    retains columns that correspond to parameters,
    such as DischargeEfficiency, but seeks to generalize them.--NOT!!!
    '''
    definingDict = OrderedDict()  
    AL = 'Electricity Stored at Last Timestep'
    definingDict[AL] = np.ones(steps)*capacity  
    AM = 'Unmet Demand'
    definingDict[AM] = np.ones(steps)*-1.0
    AO = 'Can the battery meet the demand?'
    definingDict[AO] = np.ones(steps)*-1.0
    AQ = 'Supplied to Building'
    definingDict[AQ] = np.ones(steps)*-1.0
    AP = 'Transferred out of battery'
    definingDict[AP] = np.ones(steps)*-1.0
    AR = 'Electricity stored after supplying building'
    definingDict[AR] = np.ones(steps)*-1.0
    AS = 'Is there excess eletricity from PV?'
    definingDict[AS] = np.ones(steps)*-1.0
    AT = 'Electricity needed to refill battery'
    definingDict[AT] = np.ones(steps)*-1.0
#    AU = 'Excess eletricity from PV'
#    definingDict[AU] = np.ones(steps)*-1.0
    AW = '(Excess eletricity * efficiency)'
    definingDict[AW] = np.ones(steps)*-1.0
    AY = 'Supplied to Battery from PV'
    definingDict[AY] = np.ones(steps)*-1.0
    AX = 'Transferred from PV'
    definingDict[AX] = np.ones(steps)*-1.0
    AZ = 'Electricity stored at end of timestep'
    definingDict[AZ] = np.ones(steps)*-1.0
    BA = 'Excess PV eletricity after charging'
    definingDict[BA] = np.ones(steps)*-1.0
    BB = 'Unmet demand'
    definingDict[BB] = np.ones(steps)*-1.0
    return pd.DataFrame(definingDict)




#%%
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
    return (x.max(),x.idxmax(),x.min(),x.idxmin())
    #return (x.values.max(axis=0),x.values.min(axis=0))

#%%

def getMaxMinMany(x):
    '''
    Given a pandas DataFrame object
    with possibly many columns, x, return
    the maximum and minimum values as a 
    tuple: (maxa,mina) in which maxa (mina) 
    are arrays of columns.
    '''
    return (x.values.max(axis=0),x.values.min(axis=0))
    
#%%
    
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
    Both demand and solarSupply should be Series objects.
    '''
    reducedDemand = demand - extSupply #demand.iloc[:,0] - extSupply
    netDemand = reducedDemand - solarSupply #solarSupply.iloc[:,0]
    netDemandCumSum = netDemand.cumsum()
    return (netDemandCumSum.max(), netDemandCumSum.min())
    
#%%
    
def getPVEnergyGenerated():
    return pd.Series(data=df['Riyadh global horizontal radiation (W)'].values* \
    0.001*pVCollectorEfficiency,name='PV Energy Generated (kW/m**2)')
    
def getEnergySupply(pVEnergyGenerated):
    theDATA=pVEnergyGenerated * areaOfPV
    return pd.Series(data=theDATA,
                     name='Energy Supply (kW)')
def getEnergyDemand():
    return pd.Series(data=df['KSA Office typ rev01 net electricity demand (kW)'],
                             name='Energy Demand (kW)')
def getDeficitAndOverSupply():
    pVEnergyGenerated = getPVEnergyGenerated()
    rawDeficit = pd.Series(data=getEnergyDemand() - getEnergySupply(pVEnergyGenerated),
                           name='Raw Deficit')
    shortageIndicators = rawDeficit >= 0
    deficit = pd.Series(data=abs(rawDeficit*shortageIndicators.astype('int32')),
                        name='Deficit')
    surplusIndicators = 1 - shortageIndicators
    overSupply = pd.Series(data=abs(rawDeficit*surplusIndicators),
                           name='Over Supply')
    return (deficit,overSupply)

#%%

def calculateExpensiveBattery(dischargeEfficiency=ExpensiveBatteryDischargeEfficiency):
    '''
    Given the ExpensiveBattery DataFrame, as initialized,
    replicates the calculations in John's worksheet, columns
    U:AJ and returns a DataFrame. Sees to be correct. Takes
    about 32 seconds on my MacBook Air.
    '''
    EB = ExpensiveBattery.copy()
    for i in range(settings.timeSteps): # settings.timeSteps
        U = EB.iloc[i,0]
        V = PVPower.loc[i,'Deficit']
        W = dischargeEfficiency #ExpensiveBatteryDischargeEfficiency
        if U >= V/W:
            EB.loc[i,'Is there 100% capacity in battery?'] = 1.0
        else:
            EB.loc[i,'Is there 100% capacity in battery?'] = 0.0
        X = EB.loc[i,'Is there 100% capacity in battery?']
        #print(U,V,W,X)
        if X == 1.0:
            EB.loc[i,'Transferred out of battery'] = V/W
        else:
            EB.loc[i,'Transferred out of battery'] = U
        Y = EB.loc[i,'Transferred out of battery']
        EB.loc[i,'Supplied to building'] = Y * W
        #Z = EB.loc[i,'Supplied to building']
        EB.loc[i,'Electricity stored after supplying building'] = U-Y
        AA = EB.loc[i,'Electricity stored after supplying building']
        if PVPower.loc[i,'Over Supply'] > 0:
            EB.loc[i,'Is there excess eletricity from PV?'] = 1.0
        else:
            EB.loc[i,'Is there excess eletricity from PV?'] = 0.0
        #AB = EB.loc[i,'Is there excess eletricity from PV']
        EB.loc[i,'Electricity needed to refill battery'] = \
            ExpensiveBatteryCapacity - AA
        AC = EB.loc[i,'Electricity needed to refill battery']
        EB.loc[i,'(Excess eletricity * efficiency)'] = \
        PVPower.loc[i,'Over Supply'] * ExpensiveBatteryStorageEfficiency
        AF = EB.loc[i,'(Excess eletricity * efficiency)']


        if AF - AC > 0:
            EB.loc[i,'Supplied to Battery from PV'] = AC
        else:
            EB.loc[i,'Supplied to Battery from PV'] = AF
        AH = EB.loc[i,'Supplied to Battery from PV']
        EB.loc[i,'Transferred from PV'] = AH/ExpensiveBatteryStorageEfficiency
        AG = EB.loc[i,'Transferred from PV']
        EB.loc[i,'Electricity stored at end of timestep'] = AA + AH
        AI = EB.loc[i,'Electricity stored at end of timestep']
        if i < settings.timeSteps - 1:
            EB.iloc[i+1,0] = AI
        EB.loc[i,'Excess PV eletricity after charging'] = \
            PVPower.loc[i,'Over Supply'] - AG
        

    return EB

#%%

def calculateCheapBattery(previousBattery,
        dischargeEfficiency=CheapBatteryDischargeEfficiency,
        capacity=CheapBatteryCapacity,
        chargingEfficiency=CheapBatteryStorageEfficiency):
    '''
    Given the CheapBattery DataFrame, as initialized,
    replicates the calculations in John's worksheet, columns
    AL:BB and returns a DataFrame. Sees to be correct. Takes
    about XXX seconds on my MacBook Air.
    '''
    CB = CheapBattery.copy()
    for i in range(settings.timeSteps): # settings.timeSteps
        AL  = CB.iloc[i,0]
        CB.loc[i,'Unmet Demand'] = \
            previousBattery.loc[i,'Post-PV demand from building'] - \
            previousBattery.loc[i,'Supplied to building']
        AM = CB.loc[i,'Unmet Demand']
        if AL * dischargeEfficiency >= AM:
            CB.loc[i,'Can the battery meet the demand?'] = 1.0
        else:
            CB.loc[i,'Can the battery meet the demand?'] = 0.0
        AO = CB.loc[i,'Can the battery meet the demand?'] 
        if AO == 1.0:
            CB.loc[i,'Supplied to Building'] = AM
        else:
            CB.loc[i,'Supplied to Building'] = AL*dischargeEfficiency
        AQ = CB.loc[i,'Supplied to Building']
        
        CB.loc[i,'Transferred out of battery'] = AQ/dischargeEfficiency
        AP = CB.loc[i,'Transferred out of battery']
        CB.loc[i,'Electricity stored after supplying building'] = AL-AP
        AR = CB.loc[i,'Electricity stored after supplying building']
        
        if previousBattery.loc[i,'Excess PV eletricity after charging'] > 0:
            CB.loc[i,'Is there excess eletricity from PV?'] = 1.0
        else:
            CB.loc[i,'Is there excess eletricity from PV?'] = 0.0
        CB.loc[i,'Electricity needed to refill battery'] = \
            CheapBatteryCapacity - AR
        AT = CB.loc[i,'Electricity needed to refill battery']
        CB.loc[i,'(Excess eletricity * efficiency)'] = \
            previousBattery.loc[i,'Excess PV eletricity after charging'] * \
            chargingEfficiency
        AW = CB.loc[i,'(Excess eletricity * efficiency)']
        if AW >= AT:
            CB.loc[i,'Supplied to Battery from PV'] = AT
        else:
            CB.loc[i,'Supplied to Battery from PV'] = AW
        AY = CB.loc[i,'Supplied to Battery from PV']
        CB.loc[i,'Transferred from PV'] = AY/chargingEfficiency
        AX = CB.loc[i,'Transferred from PV']
        CB.loc[i,'Electricity stored at end of timestep'] = AR+AY
        AZ = CB.loc[i,'Electricity stored at end of timestep']
        if i < settings.timeSteps - 1:
            CB.iloc[i+1,0] = AZ
        CB.loc[i,'Excess PV eletricity after charging'] = \
          previousBattery.loc[i,'Excess PV eletricity after charging'] - AX
        CB.loc[i,'Unmet demand'] = AM - AQ

    return CB  


#%%        
if __name__ == '__main__':
    xlsxDf = getExcelData()
    df = xlsxDf.copy()
    printColumnIndexes()
#    pVEnergyGenerated = getPVEnergyGenerated()
#    energySupply = getEnergySupply(pVEnergyGenerated)
#    # energyDemand just copies a column from df, but here we get a 
#    # series and a shorted name.
#    energyDemand = getEnergyDemand()
#    (deficit,overSupply) = getDeficitAndOverSupply()
    PVPower = makePVPower()
    ExpensiveBattery = makeExpensiveBatteryDF()
    print(datetime.datetime.now())
    EB = calculateExpensiveBattery()
    print(datetime.datetime.now())
#    U = ExpensiveBattery['Electricity Stored at Last Timestep']
#    V = ExpensiveBattery['Post-PV demand from building']
#    W = ExpensiveBatteryDischargeEfficiency
    CheapBattery = makeCheapBatteryDF()
    print(datetime.datetime.now())
    CB = calculateCheapBattery(EB)
    print(datetime.datetime.now())    
    
#%%
#print(EB.shape)
#print(CB.shape)
#CB2 = calculateCheapBattery(EB)
