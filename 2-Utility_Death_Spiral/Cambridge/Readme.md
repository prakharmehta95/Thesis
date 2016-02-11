
Initialization is accomplished by execution of a stand-alone Python program, **solar_py_init.py**.  It imports **defining_classes.py** for some class and function definitions and processes the files in data folder. Its output consists of two Python pickle files: prosumers.p and BuildingData.p stored in the data folder. BuildingData.p is a pickling/serialization of a single object of class dataForRun. prosumers.p is a pickled list of prosumer objects (of the prosumer class), one for each building in the model.




```
 Copyright KAPSARC. Open source MIT License.
```