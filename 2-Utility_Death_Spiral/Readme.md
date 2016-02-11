
####Purpose 

The purpose of the Residential Solar PV Adoption model is to describe the adoption over time of residential solar PV under realistic assumptions regarding consumer behavior. In particular, the model takes into account type of residence, size of PV installation, and contagion effects of existing installations. It is assumed that customers adopt probabilistically, depending upon these various conditions
####Basic Story 
Time proceeds discretely. At the start of each episode a price schedule for electric power is announced. Also, a price schedule for solar PV is announced. Eligible (to install PV) customers are those who have appropriate residences and who do not already have solar PV installed. During the episode eligible customers adopt solar PV with a probability depending upon the cost of electric power from the utility, the cost of solar power, and the prevalence of solar adopters in the neighborhood. Depending upon the number of adoptions, and possibly external factors, the utility updates its price schedule for electric power, effective at the start of the next period. 
#### 

The former file is intended to use the Cambridge data but to run as a stand-alone analysis program.  Both files are intended to serve as templates, to be modified as appropriate for other locations and data sets.
Two other files come with the Python implementation: solar_pv_cambridge_init.py initializes the datasets used directly by solar_pv_cambridge.py and solar_pv_cambridge_gis.py, and solarpvlib.py, which contains class definitions and function definitions used by the three other programs.

####Using the model

To run the model, simply do the following:
1- open the main.py file. "The main file calls the folder Cambridge or Lancaster depending on the city typed in Main.py file. Each of folders contains 3 Pytnon files: (1) defining_classes.py to define prosumer and RunData classes, (2) solar_pv_init.py to create the prosumer and buildingData pickles, and (3) solar_pv.py is to run the model."
2- calibrate the parameters located at the very begining of the code
3- click Run 
4- the results will be created as an Excel file in the folder "results"
5- the name of the Excel file will be  Results_mdy_HMS.xlsx, where "mdy_HMS" is the date and time at which the file was created.

#### Data Input Files

The Solar PV Adoption model for Cambridge processes the following files at initialization:

Hourly_Demand_PB_20150616.xlsx
Hourly Solar Output.xlsx 
roof_distribution.xlsx 
roofCatDist.csv 
buildings_data.csv 
neighDict.p  

(1) Hourly_Demand_PB_20150616.xlsx gives the electric power demands in   kilowatts on an hourly basis for a representative year for 19 categories of   buildings as located in a Boston-like environment.  

(2) Hourly Solar Output.xlsx gives the solar output of a solar PV installation  in the Boston area in watts on an hourly basis for a representative year.  There are three tabs, for 2kW, 4kW, and 6kW installations.  

(3) roof_distribution.xlsx has two kinds of data. First, it specifies  7 categories of building, based on roof size:  
Group minimum roof size	Group maximum roof size 
0				1000 
1000			2000 
2000			4000 
4000			10000 
10000			25000 
25000			50000 
50000			1000000 

We ID these as types 0, 1, 2, 3, 4, 5, and 6.  

Second, the file specifies for each type/category (the 7 above) a probability  distribution over the 19 building types. Thus, for example, if a building’s  roof is type 1 and so ranges from 1000 to 2000 square feet, then the given  probability that the building has the demand profile of a small house is  0.25, a medium house, 0.37, and so on.  

(4) roofCatDist.csv is a CSV file for mapping from a building type (one of the  7 indicated in the roof_distribution.xlsx file, above) to a probability  distribution for adopting 2, 4, or 6 kW solar PV installations.  

(5) buildings_data.csv was derived from the Cambridge shapefile.  It is a CSV file  with two columns per row and 13454 rows, one for each building. The first  value in a row is the building ID and the second value is the building’s  roof area in square meters.  

(6) neighDict.p is a Python pickle file that when loaded produces a Python  dictionary in which the keys are building IDs and the values are lists of  building IDs, which lists constitute the neighbors of the building whose ID  is the key. Every building is considered to be a neighbor of itself, so the  key is in every list of neighbors. The data were produced by ArcGIS, saved  to a file, and processed by Python into neighDict.p.


#### Initialization

Initialization is accomplished by execution of a stand-alone Python program, solar_py_cambridge_init.py.  It imports solarpvlib.py for some class and function definitions and processes the 6 data files described in the previous section. Its output consists of two Python pickle files: prosumers.p and cambridgeData.p. cambridgeData.p is a pickling/serialization of a single object of class dataForRun. prosumers.p is a pickled list of prosumer objects (of the prosumer class), one for each building in the model.


#### Main Program


There are two versions of the main program, as noted above. The solar_pv_cambridge.py version is for modeling and exploration in Python alone, outside of ArcGIS. The solar_pv_cambridge_gis.py version is to be run from within ArcGIS. In general, it is probably easier to run outside of ArcGIS because (1) the user can write code that does multiple runs, (2) the user can otherwise modify the code and data, and (3) the user doesn’t need to be running on a Windows machine with an ArcGIS active license present.



```
 Copyright KAPSARC. Open source MIT License.
```