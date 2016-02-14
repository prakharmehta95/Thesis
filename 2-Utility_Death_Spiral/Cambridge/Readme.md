
Recall that we have two models: A dynamic model in which prices change annually to reflect solar PV adoption and recovery of fixed costs, **solar_pv_dynamic.py** which is called by the main file **Main_Dynamic.py** and a static model in which prices remain constant but the utility company sees reduced profits from the reduced revenues,**solar_pv_static.py** which is called by the main file **Main_Static.py**. Calling these files are done after the intitalization process.


The Initialization process is accomplished by execution of a stand-alone Python program, **solar_py_init.py** which imports **defining_classes.py** for some class and function definitions. The file also the data files located in the **data** folder. It generates two output Python pickle files stored in the **pickles** folder: prosumers.p and BuildingData.p. BuildingData.p is a pickling/serialization of a single object of class dataForRun. prosumers.p is a pickled list of prosumer objects (of the prosumer class), one for each building in the model.


```
 Copyright © KAPSARC. Open source MIT License.
```