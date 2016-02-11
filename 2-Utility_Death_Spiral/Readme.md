
####Purpose 

The purpose of the model is to describe the adoption over time of  solar PV under the assumption of residence, size of PV installation, and contagion effects of existing installations. It is assumed that customers adopt probabilistically, depending upon these various conditions

####Basic Story 
Time proceeds discretely. At the start of each episode a price schedule for electric power is announced. Also, a cost schedule for solar PV is announced. Eligible (to install PV) customers are those who do not already have solar PV installed. During the episode eligible customers adopt solar PV with a probability depending upon the price of electric power from the utility, the cost of solar power, and the prevalence of solar adopters in the neighborhood. Depending upon the number of adoptions, and possibly external factors, the utility updates its price schedule for electric power, effective at the start of the next period. 

####Using the model

The model comes in two versions: a dynamic price model "Main_Dynamic.py" and a static price model "Main_Static.py".  and which are intended to run as stand-alone analysis programs. The first one is 

To run the model, simply do the following:

The former file is intended to use the Cambridge data but to run as a stand-alone analysis program. 

Two other files come with the Python implementation: solar_pv_cambridge_init.py initializes the datasets used directly by solar_pv_cambridge.py and solar_pv_cambridge_gis.py, and solarpvlib.py, which contains class definitions and function definitions used by the three other programs.


1- open the main.py file. "The main file calls the folder Cambridge or Lancaster depending on the city typed in Main.py file. Each of folders contains 3 Pytnon files: (1) defining_classes.py to define prosumer and RunData classes, (2) solar_pv_init.py to create the prosumer and buildingData pickles, and (3) solar_pv.py is to run the model."
2- calibrate the parameters located at the very begining of the code
3- click Run 
4- the results will be created as an Excel file in the folder "results"
5- the name of the Excel file will be  Results_mdy_HMS.xlsx, where "mdy_HMS" is the date and time at which the file was created.

#### Data Input Files
Key inputs for the model are the number of buildings, their corresponding rooftop areas, and their locations. The sizes of buildings are used to determine both their electricity demand profiles and their ability to install PV panels. Their locations are used to determine contagion effects: agents with neighbors having PV are more likely to adopt PV. PV adoption in the model is a function of the economics of PV investments, and a neighborhood effect instrumented to be converted to PV cost reductions. 
The model treats each building as a single agent, with the logistic curve providing the probability that the building owner chooses to add solar (given electricity price, solar system cost, and neighborhood effect). Thus, the model is a stochastic simulation with specific real buildings randomly adding PV. The model increments time in discrete, annual steps over the course of a 20-year time horizon.  We chose this horizon because that is the lifespan of a solar panel. A consumer makes a choice of adding solar or not in each year. (We assume that once a building has installed rooftop PV it remains in place for the duration of the simulation, and no new installation is possible.) Other model outputs include hourly electricity demand, the number of rooftop PV installations, PV capacity, and PV electricity generation and net electricity demand. 
Adoption decisions proceed in two stages. First, buildings adopt PV panels depending on the payback period for a PV investment. (The payback period incorporates both installation cost and an imputed benefit from the neighborhood effect.) 



#### Initialization

Initialization is accomplished by execution of a stand-alone Python program, solar_py_init.py.  It imports defining_classes.py for some class and function definitions and processes the files in data folder. Its output consists of two Python pickle files: prosumers.p and BuildingData.p stored in the data folder. BuildingData.p is a pickling/serialization of a single object of class dataForRun. prosumers.p is a pickled list of prosumer objects (of the prosumer class), one for each building in the model.


#### Main Program


There are two versions of the main program, as noted above. The solar_pv_.py version is for modeling and exploration in Python alone,

```
 Copyright © KAPSARC. Open source MIT License.
```