The Solar PV Adoption model for Cambridge processes the following files at initialization:

- Hourly Solar Output.xlsx (5 capacities and 4 orientations)
- Hourly_Demand_PB.xlsx
- roofCategory.xlsx
- roofCat_buildingType_Dist.xlsx
- roofCat_solarType_Dist.xlsx
- buildings_data.csv

(1) Hourly_Demand_PB.xlsx gives the electric power demands in  kilowatts on an hourly basis for a representative year for 19 categories of  buildings as located in a Boston-like environment.

(2) Hourly Solar Output.xlsx gives the solar output of a solar PV installation in the Boston area in watts on an hourly basis for a representative year. There are five tabs, for 2kW, 4kW, 6kW, 25 and 75 installations and there are 4 orientations (South, SouthWest, West, SouthEast)
Each PV option has an hourly electricity generation profile based on its characteristics and a typical meteorological year in the analyzed location. The generation profiles come from the NREL’s PVWatts Calculator (NREL, 2015) as applied to the 19 different types of buildings represented in the model and matched to the buildings in Cambridge and Lancaster.  


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

(4) roofCat_buildingType_Dist.xlsx specifies for each type/category (the 7 above) a probability distribution over the 19 building types. Thus, for example, if a building’s roof is type 1 the given probability that the building has the demand profile of a small house is 0.25, a medium house, 0.37, and so on.

(5) roofCat_solarType_Dist.xlsx is a file for mapping from a building type (one of the 7 indicated in the roof_distribution.xlsx file, above) to a probability distribution for adopting different capacity for solar PV installations.

(6) buildings_data.csv was derived from the GIS shapefile. 
It is a CSV file with two columns per row and 13454 rows, one for each building. The first value in a row is the building ID and the second value is the building’s roof area in square meters.

```
 Copyright KAPSARC. Open source MIT License.
```