'''This Model is for which city? (Cambridge, MA or Lancaster,CA?)'''
city = 'Lancaster'
#to determine the capacity factor
if city == 'Cambridge': cap_fac=.15 
else: cap_fac=.20 # The city is Lancaster,CA
#this part is to calibrate the model parameters:
ticks_to_run =20
RunsPerScenario=50
#electricity_price_list=[.15] 
#solar_PV_cost_list=[4000] #  the total up-front (initial) investment cost 
#neighborhood_effect_list=[0.15]
electricity_price_list=[.12, .13,.14,.15,.16,.17,.18,.19,.20,.21] 
solar_PV_cost_list=[3000, 3500, 4000, 4500] #  the total up-front (initial) investment cost 
neighborhood_effect_list=[0.1, 0.12, 0.15, 0.18, 0.2]
k=0.3
l_scale=1
#%%
import os
os.chdir('%s'%city) # to set the dirctory following the name of the city.
import numpy as np
import xlsxwriter
import time
import pickle
import solar_pv_init
import solar_pv
runData = pickle.load(open('pickles/buildingData.p','rb'))
Run=0
for current_price in electricity_price_list:
    for neighborhood_effect in neighborhood_effect_list:
        for solar_PV_cost in solar_PV_cost_list:
             for loop in range(RunsPerScenario):   #To perform multiple runs for each scenario        
                Run+=1
                prosumers = pickle.load(open('pickles/prosumers.p','rb')) #to reset prosumers in each run
                #To call doit function and run the model
                (per_yr_stat,installed_solar_building_Type_dic, prosumers_updated)=solar_pv.doit(
                        ticks_to_run, prosumers, runData, current_price, solar_PV_cost, cap_fac, neighborhood_effect, k, l_scale)
                # Write the results to a pickle file
                #pickle.dump(prosumers_updated,open('results/pickles/prosumers_%s.p'%time.strftime("%m%d%y_%H%M%S"),'wb'),protocol=1)
#%%
#This part generates the first output Excel file
                timestr = time.strftime("%m%d%y_%H%M%S") #to insert time and date in the file name
                wb=xlsxwriter.Workbook('results/Results_%s.xlsx'%timestr) 
#To create the first worksheet "Summary"
                sheet0= wb.add_worksheet('Summary')
                parameters =['Ticks to run', 'Current price', 'Solar PV cost', 'Capacity factor', 'neighborhood effect', 'k', 'L-scale']
                parameter_values =[ticks_to_run, current_price, solar_PV_cost, cap_fac, neighborhood_effect, k, l_scale]
                for i in range(len(parameters)): 
                    sheet0.write(i,0,parameters[i]); sheet0.write(i,1,parameter_values[i])
#to creat the second sheet "Total"
                sheet1= wb.add_worksheet('Total')
                colnames=["Year","Installed Units","New Installations", "Installed Capacity",
                          "New Installed capacity", "Demand","Supply","Demand/Supply", "Net Demand"]
                for i in range(len(colnames)): sheet1.write(0,i,colnames[i]) 
                for row, row_data in enumerate(per_yr_stat): sheet1.write_row(row+1,0,row_data)
#to report per year statistics with a new sheet for every year
                #first builbing the columns and rows with totals included
                buildTypes=[0]*(len(solar_pv_init.buildingCategories)+3)
                for i, category in enumerate(solar_pv_init.buildingCategories): 
                    buildTypes[i]=category.encode('ascii','ignore')
                buildTypes[-3], buildTypes[-2], buildTypes[-1] = 'Total Units', 'Total Capacity', 'Total Supply'#to copy the dictionary keys from the original file
                newsolarTypes=solar_pv_init.solarTypes+['Total Units', 'Total Capacity','Total Supply']
#this part is to do the calulation of capcity in the next worksheets 2kw*4 orientations, 4kw, 6kw, 25kw, and 75 kw
                capacity_matrix=np.concatenate(([[2]*len(buildTypes)]*4,[[4]*len(buildTypes)]*4,[[6]*len(buildTypes)]*4,
                                                 [[25]*len(buildTypes)]*2,[[75]*len(buildTypes)]*2,[[0]*len(buildTypes)]*3), axis=0)
                supply_matrix=(np.concatenate(([[runData.annualSolarProduction[j]]*len(buildTypes) for j in 
                                                range(len(solar_pv_init.solarTypes))],[[0]*len(buildTypes)]*3), axis=0))/1000
#Start adding yearly statistics as sperate worksheets
                for tick in range(ticks_to_run):
                    sheet= wb.add_worksheet('Yr_%s'%tick)#seprate sheet for every year
                    solarType_buildingType_matrix=np.array([[0 for j in range(len(buildTypes))] for j in range (len(newsolarTypes))],dtype=np.float)    
                    item=installed_solar_building_Type_dic[tick]
                    for i in range(len(item)):
                            solarType_buildingType_matrix[item[i][0],item[i][1]]+=1# filling the matrix
                    solarType_buildingType_matrix[:,-3] = solarType_buildingType_matrix.sum(axis=1)#calculates TotalUnits column
                    matrix2=solarType_buildingType_matrix * capacity_matrix
                    matrix3=solarType_buildingType_matrix * supply_matrix     
                    solarType_buildingType_matrix[-3,:] = solarType_buildingType_matrix.sum(axis=0)#calculates TotalUnits row
                    solarType_buildingType_matrix[-2,:] = matrix2.sum(axis=0)#calculates TotalCapacity row
                    solarType_buildingType_matrix[-1,:] = matrix3.sum(axis=0)#calculates TotalSupply row
                    solarType_buildingType_matrix[:,-2] = matrix2[:,-3]
                    solarType_buildingType_matrix[:,-1] = matrix3[:,-3]
                    solarType_buildingType_matrix[-1,-1] = sum(solarType_buildingType_matrix[:,-1])
                    solarType_buildingType_matrix[-2,-2] = sum(solarType_buildingType_matrix[:,-2])
                    solarType_buildingType_matrix[-1,-3] , solarType_buildingType_matrix[-2,-3] = 0,0
                    for i in range(len(buildTypes)): sheet.write(0,i+1,buildTypes[i])#builds cols names
                    for i in range(len(newsolarTypes)): sheet.write(i+1,0,newsolarTypes[i])#builds rows names
                    for row, row_data in enumerate(solarType_buildingType_matrix):
                        sheet.write_row(row+1,1,row_data)      
## Create chart objects. In this case 4 embedded charts n the sheet "Total"
                chart1 = wb.add_chart({'type': 'line'}); chart2 = wb.add_chart({'type': 'line'})
                chart3 = wb.add_chart({'type': 'line'}); chart4 = wb.add_chart({'type': 'line'})
#adding the series
                chart1.add_series({'name':'=Total!$G$1','categories':'=Total!$A$2:$A$21','values':'=Total!$G$2:$G$21',})
                chart2.add_series({'name':'=Total!$C$1','categories':'=Total!$A$2:$A$21','values':'=Total!$C$2:$C$21',})
                chart3.add_series({'name':'=Total!$D$1','categories':'=Total!$A$2:$A$21','values':'=Total!$D$2:$D$21',})
                chart4.add_series({'name':'=Total!$E$1','categories':'=Total!$A$2:$A$21','values':'=Total!$E$2:$E$21',})
#Adding labels
                chart1.set_x_axis({'name': 'Year'}); chart2.set_x_axis({'name': 'Year'})
                chart3.set_x_axis({'name': 'Year'}); chart4.set_x_axis({'name': 'Year'})
#Inserting the charts into the worksheet
                sheet1.insert_chart('K2', chart1, {'x_offset': 25, 'y_offset': 10})
                sheet1.insert_chart('K18', chart2, {'x_offset': 25, 'y_offset': 10})
                sheet1.insert_chart('S2', chart3, {'x_offset': 25, 'y_offset': 10})
                sheet1.insert_chart('S18', chart4, {'x_offset': 25, 'y_offset': 10})
                wb.close()
#The end of generating the first Excel file
#the folowing variables are used to generate the second Excel file
                parameter_2_values =[Run, current_price, solar_PV_cost, cap_fac, neighborhood_effect]+ per_yr_stat[-1][1:6:2]+per_yr_stat[-1][6:]
                if Run==1: 
                    parameters_2 =[['Run', 'Current price', 'Solar PV cost', 'Capacity factor', 'neighborhood effect', 
                             "Installed Units","Installed Capacity","Demand","Supply","fraction of demand met by solar", "Net Demand"]]
                    parameters_2. append(parameter_2_values)
                else: parameters_2. append(parameter_2_values)
#End of the runs        
#%%
#This part generates the second output Excel file
wb2=xlsxwriter.Workbook('results/Totals_%s.xlsx'%timestr) 
sheetA= wb2.add_worksheet('Totals')
for row, row_data in enumerate(parameters_2): sheetA.write_row(row,0,row_data)
wb2.close()
#The end of generating the second Excel file
