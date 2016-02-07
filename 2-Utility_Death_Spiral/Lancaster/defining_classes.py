
#%%
class dataForRun():
    def __init__(self,solarProduction,buildingCategories,
                 hourlyDemands,hourlyDemandsLabels,neighborsDict,
                 roofCategoriesDict,roofCategoryBuildingType):
        self.solarProduction = solarProduction
        self.buildingCategories = buildingCategories
        self.annualSolarProduction = sum(self.solarProduction)
        self.hourlyDemands = hourlyDemands
        self.hourlyDemandsLabels = hourlyDemandsLabels
        self.annualHourlyDemands = sum(self.hourlyDemands)
        self.neighborsDict = neighborsDict
        self.roofCategoriesDict = roofCategoriesDict
        self.roofCategoryBuildingType = roofCategoryBuildingType
#%%
class prosumer():
    '''
    Contains all key prosumer data for the Solar PV model:
    0. ID: ID of the building/prosumer. 
    1. objInfo: documentation text from the object's creation.
    2. prosumerType: text, not yet really used.
    3. hasSolar: boolean; True if the building/prosumer has solar; 
       else False. 
    4. buildingType: an integer, indicating the column in the demands array,
       which will normally be 8760 by N where N is the demand_type. So,
       buildingType indicates a column in this array.
    5. solarType: the type of solar, an integer indicating a column in
       the solarProduction array, which will normally be 8760 by M for
       M types of solarProduction. (Remember: we always count from 0.). Its default value is 99.
    6. gettingSolar: boolean; True if the building/prosumer is scheduled
       to get solar PV during the current tick.
    7. year_adopted: the year in which the prosumer adopted solar. 
    '''
    def __init__(self,ID,objInfo='Not yet',prosumerType='greedy',
                 hasSolar=False,buildingType=0,solarType=99,
                 gettingSolar=False,roof_area=-1,year_adopted=0):
        self.ID = ID
        self.objInfo = objInfo
        self.prosumerType = prosumerType
        self.hasSolar = hasSolar
        self.buildingType = buildingType
        self.solarType = solarType
        self.gettingSolar = gettingSolar
        self.roof_area = roof_area
        self.year_adopted= year_adopted