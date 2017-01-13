from Groundplan import Groundplan
from GroundplanFrame import GroundplanFrame
from districtobjects.Mansion import Mansion
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from random import random

class DistrictPlanner(object):
    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True
    FIRST_HOME_X = 112
    FIRST_HOME_Y = 90
    
    def __init__(self):
        self.groundPlan = Groundplan(self.NUMBER_OF_HOUSES, True)

        
        self.developGroundplan()
        
        self.frame = GroundplanFrame(self.groundPlan)
        self.frame.setPlan()
        self.frame.root.mainloop()

    def developGroundplan(self):

        # place playground & water
        self.addPlaygrounds()
        self.addWaterbodies()
        self.initFirstHome()

        # add homes & move homes
        # self.addHomes()
        # self.moveHouses()

        if(self.groundPlan.isValid()): 
            print ("groundPlan is valid")
        else: 
            print ("groundPlan is invalid")
        
        print ("Value of groundPlan is:", self.groundPlan.getPlanValue())
        
        # self.printResults()

        return


    def initFirstHome(self):
        mansion = self.addToGroundPlan('FamilyHome', self.FIRST_HOME_X, self.FIRST_HOME_Y)
        return


    def addHomes(self, mansion):
        if (self.addToGroundPlan(type, x, y)):
            self.addHomes(mansion)
        else:
            return


    def checkSpotUp(self):
        pass

    def checkSpotRight(self):
        pass

    def checkSpotDown(self):
        pass

    def checkSpotLeft(self):
        pass


    def addPlaygrounds(self):
        x = 90
        y = 70
        self.groundPlan.addPlayground(Playground(x, y).flip())
        # x = self.groundPlan.WIDTH - 60
        # y = 50
        # self.groundPlan.addPlayground(Playground(x, y).flip())
        return

    def addWaterbodies(self):
        width = 21
        height = 83.5
        x = 0
        y = 0
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))

        x = 0
        y = 86.5
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))

        x = 179
        y = 0
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))

        x = 179
        y = 86.5
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))
        return


    # Add object to map (type)
    def addToGroundPlan(self, type, x_coordinate, y_coordinate):
        if (type == 'Mansion'):
            mansion = Mansion(x_coordinate,y_coordinate)
            if (self.groundPlan.correctlyPlaced(mansion)):
                self.groundPlan.addResidence(mansion)
                return mansion

        elif (type == 'Bungalow'):
            bungalow = Bungalow(x_coordinate,y_coordinate)
            if (self.groundPlan.correctlyPlaced(bungalow)):
                self.groundPlan.addResidence(bungalow)
                return True
            if (self.groundPlan.correctlyPlaced(bungalow.flip())):
                self.groundPlan.addResidence(bungalow)
                return bungalow

        elif (type == 'FamilyHome'):
            familyHome = FamilyHome(x_coordinate,y_coordinate)        
            if (self.groundPlan.correctlyPlaced(familyHome)):
                self.groundPlan.addResidence(familyHome)
                return True
            if (self.groundPlan.correctlyPlaced(familyHome.flip())):
                self.groundPlan.addResidence(familyHome)
                return familyHome

        return False

    def checkSecondMinDistance(self,groundPlan,minimumIndex,minimumValue, residences, clearanceList):
        clearanceList.pop(minimumIndex)
        firstHouse = residences[minimumIndex]
        if minimumValue not in clearanceList:
            return firstHouse
        scndMinimumIndex = clearanceList.index(minimumValue)
        scndHouse = residences[scndMinimumIndex]
        groundPlan.removeResidence(scndHouse)        
        firstMin = groundPlan.getMinimumDistance(firstHouse)
        groundPlan.addResidence(scndHouse)
        groundPlan.removeResidence(firstHouse)
        scndMin = groundPlan.getMinimumDistance(scndHouse)
        groundPlan.addResidence(firstHouse)
        if firstMin < scndMin:
            return firstHouse
        else :
            return scndHouse
           
    def moveHouses(self):
        busy = True        
        j = 0
        while busy:
            residences = self.groundPlan.getResidences()
            numberOfHouses = len(residences)
            if numberOfHouses == 0:
                return
            clearanceList = []
            for i in range(numberOfHouses):
                clearanceList.append(self.groundPlan.getMinimumDistance(residences[i]))
            minimumValue = min(clearanceList)
            minimumIndex = clearanceList.index(minimumValue)            
            remHouse = self.checkSecondMinDistance(self.groundPlan, minimumIndex, minimumValue, residences, clearanceList)
            self.groundPlan.removeResidence(remHouse) 
            if (j> 50 and remHouse.getType == "FamilyHome"):
                return
            elif j > 1000:
                return
            else:
                m = 0
                while not(self.addToGroundPlan(remHouse.getType())):
                   m = m+1
                # if m == 50:
                #     return
                j = j+1

    def printResults(self):
        residences = self.groundPlan.getResidences()
        numberOfHouses = len(residences)
        mansions = []
        bungalows = []
        familyHomes = []
        for i in range(numberOfHouses):
            if residences[i].getType() == "FamilyHome":
                familyHomes.append(self.groundPlan.getMinimumDistance(residences[i]))
            elif residences[i].getType() == "Bungalow":
                bungalows.append(self.groundPlan.getMinimumDistance(residences[i]))
            elif residences[i].getType() == "Mansion":
                mansions.append(self.groundPlan.getMinimumDistance(residences[i]))
        print("Minimal clearance FamilyHomes: ", min(familyHomes))
        print("Minimal clearance Bungalows: ", min(bungalows))
        print("Minimal clearance Mansions: ", min(mansions))

        print(mansions)
        print(bungalows)
        print(familyHomes)

    
DistrictPlanner()