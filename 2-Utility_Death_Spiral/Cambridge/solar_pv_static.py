"""
Created on Sun Jun 28 02:28:26 2015

@author: steve Kimbrough and edited by Mohammed Muaafa
"""
import numpy as np
#%%
def neighbors_with_solar(neighbor_list, prosumers):
    ''' This function checks if any of the neighbors of a givern prosomer has solar '''
    neighborsWithSolar = 0
    for neighbor in neighbor_list:
        if True == prosumers[neighbor].hasSolar:
             neighborsWithSolar += 1
    fractionOfNeighborsWithSolar= neighborsWithSolar*1.0 / len(neighbor_list)*1.0
    return fractionOfNeighborsWithSolar
#%%
def go(current_price, prosumers, runData, solar_cost, cap_fac, neighborhood_effect, k, l_scale):
    '''This function performs the PV adoption decision process for all prosumers'''
    for prosumer in prosumers:
        if not prosumer.hasSolar:        
            fractionOfNeighborsWithSolar = neighbors_with_solar(runData.neighborsDict[prosumer.ID], prosumers)
            ne = neighborhood_effect * fractionOfNeighborsWithSolar #adjust neighborhood effect as function of penetration level
            x = (solar_cost*(1-ne)) / (8760*cap_fac*current_price) #Payback period
            simple_mirrored_logistic = 1.0 - (l_scale / (1 + np.exp(-k*x)))
            if np.random.random() <= simple_mirrored_logistic:
                prosumer.gettingSolar = True
#%%
def getDemandForYear(prosumers, runData):
    '''This function adds up the hourly demand to get the yearly one '''    
    demand = 0
    for prosumer in prosumers:
        demand += runData.annualHourlyDemands[prosumer.buildingType]
    return demand
#%%
def getSolarSupplyForYear(prosumers, runData):
    ''' This function adds up the hourly production to get the yearly one '''  
    supply = 0
    for prosumer in prosumers:
        if prosumer.hasSolar:
            supply += runData.annualSolarProduction[prosumer.solarType]
    return supply / 1000.0
#%%
def getSolarCapacity(solarType):
    ''' This function finds the capcity of solar panel given its index (building.solarType) as defined 
        in solartypes dictionary so it is used to calculate the total capacity installed'''
    capacity=0    
    if 0<= solarType <=3:
        capacity =2
    elif 4<= solarType <=7:
        capacity =4
    elif 8<= solarType <=11:
        capacity =6
    elif 12<= solarType <=13:
        capacity =25
    else: capacity =75
    return capacity
#%%  Here is to calculate PV cost in every year given the decline is 5.9% to yr 6, 0.95% to yr 14, 0.675 to yr 20  
def SolarCost(solar_PV_cost,ticks_to_run,tick):
    cost= [solar_PV_cost for j in range (ticks_to_run)]    
    for year in range(ticks_to_run):
        if year<6 and year>0: 
            cost[year] = (1-0.059)*cost[year-1]
        elif year>5 and year<15:
            cost[year] = (1-0.0095)*cost[year-1]
        elif year>14:
            cost[year] = (1-0.0067)*cost[year-1]
    return cost[tick]
#%%
def doit(ticks_to_run, prosumers, runData, current_price, solar_PV_cost, cap_fac, neighborhood_effect, k, l_scale):
    ''' This is the main function that runs the model'''
    installed_solar_building_Type_dic=[[] for i in range(ticks_to_run)]
    per_yr_stat = [[0 for x in range(5)] for x in range(ticks_to_run)] 
    totalDemand = getDemandForYear(prosumers, runData)
    totalSupply = 0
    netDemand=totalDemand-totalSupply
    installed_units = 0 
    cum_installed_capacity =0
    for tick in range(ticks_to_run):
        go(current_price, prosumers, runData, SolarCost(solar_PV_cost,ticks_to_run,tick), cap_fac, neighborhood_effect, k, l_scale) #done with adoption 
        #here to do some statistics        
        new_installed_capacity = 0
        newinstallations = {}
        for building in prosumers:
            if building.gettingSolar:
                building.hasSolar = True
                building.gettingSolar = False
                building.year_adopted = tick+1 #to add entry year
                installed_units += 1
                newinstallations[building.ID] = (building.solarType,tick)
                new_installed_capacity += getSolarCapacity(building.solarType)
                cum_installed_capacity += getSolarCapacity(building.solarType)
            if building.hasSolar: 
                installed_solar_building_Type_dic[tick].append([building.solarType, building.buildingType])
        per_yr_stat[tick]=[tick, installed_units, len(newinstallations), cum_installed_capacity, new_installed_capacity, 
                            totalDemand, totalSupply, totalSupply/totalDemand, netDemand]
        totalSupply = getSolarSupplyForYear(prosumers, runData)
        netDemand=totalDemand-totalSupply
    return (per_yr_stat,installed_solar_building_Type_dic, prosumers)
#%%