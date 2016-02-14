This folder includes the following three files:

> **Note:** The .p extension indicates that this is a Python pickle file. This is a binary format. 



1- **buildingData.p**

This is a Python pickle file that when loaded yields a list of building instances. The list contains an object instance for each buildings in our data set. This is the buildings as they are initialized, but without their neighbors listed. That information is contained in the **neighDict.p** file, which is also loaded by the program. Together, these two pickle files allow us to operate independently of **ArcGIS** for development purposes.

2- **neighDict.p**

**neighborhood dictionary**. The file holds a Python dictionary in which the keys are the building IDs in the
data set and the values are lists of neighbors, where a neighbor is indicated by a building ID.  The Python code loads this file and translates it into a usable dictionary during setup. Every building is considered to be a neighbor of itself, so the  key is in every list of neighbors. The data were produced by ArcGIS, saved  to a file, and processed by Python into neighDict.p.


3- **prosumers.p**

This file contains prosumer data created by **solar_pv_init.py** and is updated by **doit** function located in **solar_pv_static.py** (or **solar_pv_dynamic.py**) to include prosumers who adopt solar at every tick. 


----------
> Copyright © [KAPSARC](https://www.kapsarc.org/). Open source [MIT License](http://opensource.org/licenses/MIT).
