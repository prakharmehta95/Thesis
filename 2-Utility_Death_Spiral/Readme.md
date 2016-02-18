Can Adoption of Rooftop Solar PV Panels Trigger a Utility Death Spiral? A Tale of Two Cities
===================
#####by Iqbal Adjali, Patrick Bean, Rolando Fuentes, Steven Kimbrough, Mohammed Muaafa, Frederic Murphy, Michele Vittorio, Ben Wise, and Weinan Zheng

####Purpose 

Rooftop solar photovoltaic (PV for short) is a small-scale technology that can be adopted by a large portion of a power company’s customers. In this model, we examine the extent to which rooftop PV penetration can erode utilities’ revenues and undercut the traditional financial model of power companies, leading to a so-called **death spiral** of the utility business.
We developed an **agent-based** model (ABM) that simulates the **adoption of rooftop PV panels** by buildings depending on **perceived payback period** for their investment, given **PV costs** and **utility electricity prices**. The perceived payback period is influenced by a **contagion effect** that depends on the number of panels installed in their geographical vicinity. Our agent-based model allows us to estimate not only the size of the effect, but the rate at which customer adoption affects the revenues of the utilities. 

####Basic Story 
Time proceeds discretely. At the start of each episode a price schedule for electric power is announced. Also, a cost schedule for solar PV is announced. Eligible (to install PV) customers are those who do not already have solar PV installed. During the episode eligible customers adopt solar PV with a probability depending upon the price of electric power from the utility, the cost of solar power, and the prevalence of solar adopters in the neighborhood. Depending upon the number of adoptions, and possibly external factors, the utility updates its price schedule for electric power (only in the dynamic model), effective at the start of the next period. 

#### Data Input Files

Key inputs for the model (From **GIS**) are the **number of buildings**, their corresponding **rooftop sizes**, and their **locations**. The sizes of buildings are used to determine both their **electricity demand** profiles and their ability to install PV panels. Their locations are used to determine contagion effects: agents with neighbors having PV are more likely to adopt PV. PV adoption in the model is a function of the economics of PV investments, and a neighborhood effect instrumented to be converted to PV cost reductions. 

The model requires also inputting a retail **electricity price** ($/KWh), the **installed cost** for rooftop PV ($/watt), PV **capacity factor** (%), and a **neighborhood effect**. Each PV option has an hourly electricity generation profile based on its characteristics and a typical meteorological year in the analyzed location. The generation profiles come from the **NREL’s PVWatts** Calculator (NREL, 2015) as applied to the 19 different types of buildings represented in the model and matched to the buildings in **Cambridge** and **Lancaster**.


#### Main Program

The model treats each building as a single agent, with the logistic curve providing the probability that the building owner chooses to add solar (given electricity price, solar system cost, and neighborhood effect). The model increments time in discrete, annual steps over the course of a 20-year time horizon.  We chose this horizon because that is the lifespan of a solar panel. A consumer makes a choice of adding solar or not in each year depending on the payback period for a PV investment and a mirrored logistic function(refer to the main document for more details).We assume that once a building has installed rooftop PV it remains in place for the duration of the simulation, and no new installation is possible. Other model outputs include hourly electricity demand, the number of rooftop PV installations, PV capacity, and PV electricity generation and net electricity demand. 
The model is implemented in **Python** with **ArcGIS** visualization and is a template we designed to be modified as appropriate for other locations and data sets beyond Cambridge and Lancaster. The model comes in two versions: a **dynamic price** model "Main_Dynamic.py", in which the utility company updates the electricity price every year to recover the revenue lost from PV installations,  and a **static price** model "Main_Static.py" in which the electricity price is fixed throughout the simulation time. Both models are intended to run as stand-alone analysis programs. 

> **Note:** The dynamic model simulates the utility death spiral as follows. We assume the utility has an annual revenue requirement, F, for recovery of fixed costs and allowed profits. The electricity price in any single year is F + V, where V is the generation cost. We assume that in year 0, at initialization, F = total demand * $0.08 = F0 = total demand * PrF0. This constitutes the revenue requirement in each year for the utility to avoid a death spiral, i.e., for the utility to continue to be able to retire its investment costs and obtain its promised profits. The retail price in a given year is PrFt + PrV, with PrV set to be constant as PrV = initial price – PrF0. Solar additions decrease the sales of electricity by the amount they generate in each year. 

#### Initialization

Initialization is accomplished by execution of a stand-alone Python program in each city folder, solar_py_init.py. It imports, from the **pickles** folder, defining_classes.py for some class and function definitions and also processes the files in the **data** folder. Its output consists of two Python pickle files stored in the **pickles** folder: prosumers.p and BuildingData.p. The file BuildingData.p is a pickling/serialization of a single object of class dataForRun. The file prosumers.p is a pickled list of prosumer objects (of the prosumer class), one for each building in the model.

#### Running the model
To run the model, simply do the following:

- Open on of the main files "Main_Dynamic.py" or "Main_Static.py".
- Select the appropriate directory where this folder is located 
- Type the city you want to run the model for (Cambridge or Lancaster). The main file calls the corresponding city folder. Each folder contains 3 Pytnon files: (1) defining_classes.py to define prosumer and RunData classes, (2) solar_pv_init.py to create the prosumer and buildingData pickles, and (3) solar_pv.py is to simulate the adoption over 20 years.
- Calibrate the parameters located at the very begining of the code (time horizon, number of riblications per scenario, PV cost, Electricity price, neighbor effect, k, and L-scale).
- Click Run 
- The results will be created as Excel files inside the **results** folder. An Excl file for every replication of each scenario will be generated. So, if you select 50 Runs_Per_Scenario and a total of 100 scenarios, 5000 Excel file will be generated **plus** an Excel file that summarizes all the results will be also generated. The name of each Excel file will be Results_mdy_HMS.xlsx, where "mdy_HMS" is the date and time at which the file was created.



----------
> Copyright © [KAPSARC](https://www.kapsarc.org/). Open source [MIT License](http://opensource.org/licenses/MIT).
