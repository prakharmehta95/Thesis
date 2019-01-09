# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 02:29:39 2015

@author: Steven Kimbrough edited by Mohmmed Muaafa

File: solar_pv_init.py

The purpose of this file is to create a pickle a prosumer object for the model.

See the documentation in Word, but here's some of it:

The Solar PV Adoption model processes the following files at initialization:
1.	Hourly_Demand_PB_20150616.xlsx
2.	Hourly Solar Output.xlsx
3.	roofCategory.xlsx
4.  roofCat_buildingType_Dist.xlsx
5.	roofCat_solarType_Dist.xlsx
6.	buildings_data.csv
7.	neighDict.p


(1) Hourly_Demand_PB_20150616.xlsx gives the electric power demands in  
kilowatts on an hourly basis for a representative year for 19 categories of  
buildings as located in a Boston-like environment.

(2) Hourly Solar Output.xlsx gives the solar output of a solar PV installation 
in the Boston area in watts on an hourly basis for a representative year. 
There are three tabs, for 2kW, 4kW, and 6kW installations.

(3) roofCategory.xlsx specifies 7 categories of building, based on roof size:

Group minimum roof size	Group maximum roof size
0	1000
1000	2000
2000	4000
4000	10000
10000	25000
25000	50000
50000	1000000
We ID these as types 0, 1, 2, 3, 4, 5, and 6.

(4) roofCat_buildingType_Dist.xlsx specifies for each type/category (the 7 above) a probability 
distribution over the 19 building types. Thus, for example, if a building’s 
roof is type 1 the given probability that the building has the demand profile of a small house is 
0.25, a medium house, 0.37, and so on.

(5) roofCat_solarType_Dist.xlsx is a file for mapping from a building type (one of the 
7 indicated in the roof_distribution.xlsx file, above) to a probability 
distribution for adopting different capacity for solar PV installations.

(6) buildings_data.csv was derived from the GIS shapefile. 
It is a CSV file with two columns per row and 13454 rows, one for each building. The first 
value in a row is the building ID and the second value is the building’s 
roof area in square meters.

(7) neighDict.p is a Python pickle file that when loaded produces a Python 
dictionary in which the keys are building IDs and the values are lists of 
building IDs, which lists constitute the neighbors of the building whose ID 
is the key. Every building is considered to be a neighbor of itself, so the 
key is in every list of neighbors. The data were produced by ArcGIS, saved 
to a file, and processed by Python into neighDict.p.
"""
'''
Model Version 0.2 Update (author: Patrick Bean)
The code was modified to expand the solar options to include orientation of the panels 
(SE, S, SW, W) and more sizes. Overall the amount of solar options increased from 3 to
16 different types.
'''

import pickle
import numpy as np
import pandas as pd
import defining_classes

#%%
''' These will indicate columns in the solarProduction array.
So, solarTypes['2kW'] is column 0 in the array, etc. These are just labels.'''
solarTypes = {}
solarTypes['2kW_S'] = 0
solarTypes['2kW_SE'] = 1
solarTypes['2kW_SW'] = 2
solarTypes['2kW_W'] = 3
solarTypes['4kW_S'] = 4
solarTypes['4kW_SE'] = 5
solarTypes['4kW_SW'] = 6
solarTypes['4kW_W'] = 7
solarTypes['6kW_S'] = 8
solarTypes['6kW_SE'] = 9
solarTypes['6kW_SW'] = 10
solarTypes['6kW_W'] = 11
solarTypes['25kW_S'] = 12
solarTypes['25kW_SW'] = 13
solarTypes['75kW_S'] = 14
solarTypes['75kW_SW'] = 15

#Sorting the dictionary
solarTypes=sorted(solarTypes, key=lambda x : solarTypes[x]) 
# Here and subsequently for all variables given values, check them out
# in the "Variable explorer" window of Anaconda.

#%%
# (1) File: 'Hourly_Demand_PB_20150616.xlsx'.
# Now get the hourly demands per building type (or demand type):
hourlyDemandsDF = pd.read_excel(open('data/Hourly_Demand_PB_20150616.xlsx','rb')) #edited by Mo,shortened
hourlyDemandsLabels = list(hourlyDemandsDF.columns)[2:]
hourlyDemands = np.array(hourlyDemandsDF.iloc[:,2:])
#%%
# Now we want to create the solarProduction array.
# So we initially create an array of the right size, containing only zeros.
solarProduction = np.zeros((8760,len(solarTypes))) #8769 hours in a year

#%% 
# (2) File: 'Hourly Solar Output %kW.csv'
# Get the hourly output from Hourly Solar Output.xlsx. 
# There are three tabs, for 2kW, 4kW, and 6kW nameplate capacity.
# This code has been modified to read CSV file but make sure there is a seperate file for
# each solar installation capacity with the name "Hourly Solar Output %.csv" where '%' the capacity (e.g. 2kW)
for i,j in enumerate(solarTypes):
    solarProduction[:,i]=np.genfromtxt("data/Hourly Solar Output %s.csv"%j,dtype=float,
        delimiter=',',skip_header=1,skip_footer=1,usecols = 10)
    #skip header because of the labels
    #skip footer because of the totals
    #usecols - reads the first eleven columns

#%%
# (3) File: 'roofCategory.xlsx'
# Now we are going to determine the roof categories.
# This in turn will tell us the probability of having 2, 4, or 6 kW solar PV.

roofCat = pd.read_excel(open("data/roofCategory.xlsx","rb"))
# Get the number of categories:
category_count = len(roofCat.iloc[0:,0])

# Make the category dictionary. Keys: category ID, an integer, 
# values: (low, hi) tuples.)
categoryDict = {}
for i in range(category_count):
    categoryDict[i] = (roofCat.iloc[i,0], roofCat.iloc[i,1])
    
#%%
    
# This information may not be necessary, but it's useful to have.   
#this is needed for my cae as well
roofCategoryDictInfo = '''The roof category dictionary has keys that are integers
and that start at 0. The categories are simply numbered and identified
that way. Their values are (low, high) tuples that represent roof areas in
square feel. A roof with an area at least low and at most high will be in
the category. Note that this might result in numerical errors, as a
roof with 2000.05 square feet will not be in (1001.0, 2000.0) or in
the next category, (2001.0, 4000.0). Will ignore this for now and see if
it causes problems. Here it is:
{0: (0.0, 1000.0),
 1: (1000.0, 2000.0),
 2: (2000.0, 4000.0),
 3: (4000.0, 10000.0),
 4: (10000.0, 25000.0),
 5: (25000.0, 50000.0),
 6: (50000.0, 1000000.0)}
'''
#%%
# (4) File: 'roofCat_buildingType_Dist.xlsx'
#Now get the building categories.
# Get their names from the roofCat_buildingType_Dist.xlsx file
#rc_bt denotes roof category with building type
rc_bt = pd.read_excel(open("data/roofCat_buildingType_Dist.xlsx","rb"))
buildingCategories = list(rc_bt.columns[1:])
buildingCategoryCount = len(buildingCategories)
roofCategoryBuildingType = np.array(rc_bt.iloc[:,1:])
# Again: you can inspect the variables in the "Variable explorer" in 
# Anaconda. Still, this is a check worth doing:
#print("Should be all 1.0s:",roofCategoryBuildingType.sum(axis=1))
#%%
#I have no clue what this section does
def in_range(value,range_tuple):
    '''
    Given a scalar value, value, and a tuple, range_tuple
    with low and high (left and right) values, returns
    True if x is in [low,high) and False otherwise.
    '''
    if range_tuple[1] <= range_tuple[0]:
        # We have an error condition
        return None
    if value >= range_tuple[0] and value < range_tuple[1]:
        return True
    else:
        return False
#%%
def getRoofCat(roofArea):
    '''Function to determine your roof category from your roof size.'''
    # ranges between 0-6
    category = None
    for i in categoryDict.keys():
        #print(i,flush=True)
        if in_range(roofArea,categoryDict[i]):
            category = i
            break
    if category is None:
        print("We have a None roof category.")
    return category
#%% 
def getBuildingType(roofArea):
    '''
    Given the roofArea of a building, gets the roof category (0-6 for
    the Cambrdige data), retrieves the distribution of building mixes
    for that category, and randomly draws a building mix, that is,
    picks according to to the distribution which type of building and
    load curve to use.
    '''
    roofCategory = getRoofCat(roofArea)
    buildingMix = roofCategoryBuildingType[roofCategory,:]
    #depending on the size of the roof, the roof category is defined which is used to define the building mix 
    #i.e. the probability of the demand of the building being a small house/medium house/commercial building etc
    #do not need to do this as we have definite information on the building type and it's demand
    
    return drawFromDistriubtionArray(buildingMix)
#%%
# (5) File: 'roofCat_solarType_Dist.xlsx'
# What this is is the table of probability distributions for solar size
# type (2, 4, 6 kW) given your roof category.
roofPVDistDF = pd.read_excel(open("data/roofCat_solarType_Dist.xlsx","rb"))
roofCat_pvSize_dist = np.array(roofPVDistDF.iloc[:,1:],dtype='float')
#these are the same arrays except for one column at the beginning
#%%
#returns cumulative values (probabilities) from whatever is passed through it
#don't clearly understand how it is used
def drawFromDistriubtionArray(distributionArray):
    '''
    Given distributionArray, which should be a vector, that is an m by 1 or
    1 by m array, of probability values that sum to 1: creates the 
    associated cumulative distribution and returns random draw from it.
    '''
    cumDist = distributionArray.cumsum()
    draw = np.random.random() #random number generator
    previous = -1.0
    for i in range(len(cumDist)):
        if draw > previous and draw <= cumDist[i]:
            return i
        else:
            previous = cumDist[i]
    print("Error in drawFromDistributionArray.")
#%%
def getSolarType(roofArea):
    '''
    Finds the solar type (2, 4, 6 kW coded as 0, 1, or 2) 
    of a building with roof area roofArea. Does this
    by getting the roof category of the building from its roofArea,
    then retrieving the PV size distribution vector from 
    roofCat_pvSize_dist, and drawing a random deviate (a size) from its
    cumulative.
    '''
    roofCategory = getRoofCat(roofArea)
    distVector = roofCat_pvSize_dist[roofCategory]
    return drawFromDistriubtionArray(distVector)
#%%
def explanationtomyself():
   '''
   we know the building type, rooftop size, demands --> we do not need to do this probabilistic distribution for
   getting building demands and PV system sizes
   We can make a probabilistic distribution only for the choice of the size of PV system as that will still depend on the decision
   Or rather that also depends on the decision making process - let it be defined by the variety of factors like cost, peer effects?
   '''

#%%
# (6) File: 'buildings_data.csv'
def makeProsumers():
    '''
    Creates the main agents, the prosumers, for the model. Begins by
    reading in the buildings_data.csv file and making it a dictionary.
    Returns a list of prosumer objects.
    '''
    prosumers = [] #list
    raDict = {} #dict
    f = open('data/buildings_data.csv','r')
    line = f.readline()
    while line:
        a,b = line.strip().split(',')
        raDict[int(a)] = float(b)
        line = f.readline()
    f.close()
    #The previous process is to convert building data into a dictionary (raDict)
    for buildingID in raDict.keys():
        roof = raDict[buildingID] 
        ID = buildingID
        solarTypeValue = getSolarType(roof)
        buildingTypeValue = getBuildingType(roof)
        prosumers.append(defining_classes.prosumer(ID,solarType=solarTypeValue,
                                             buildingType=buildingTypeValue,
                                             roof_area=roof))
    return prosumers
#%%        
prosumers = makeProsumers()
#%%
# Write the list of prosumers to a pickle file for use by the main program.
pickle.dump(prosumers,open('pickles/prosumers.p','wb'),protocol=1)
#%%
# (7) File: 'neighDict.p'
# Now create the dataForRun object, and populate it with the data.
neighborsDict = pickle.load(open('pickles/neighDict.p','rb'))       
buildingData = defining_classes.dataForRun(solarProduction,
                           buildingCategories,hourlyDemands,
                           hourlyDemandsLabels,neighborsDict,
                           categoryDict,roofCategoryBuildingType)
#this buildingData pickle is called as runData in the main code
#%%
# Conclude by writing the dataForRun object to a pickle file for use
# by the main program.
pickle.dump(buildingData,open('pickles/buildingData.p','wb'),protocol=1)
#%%
print("All done with initialization.")