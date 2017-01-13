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

        # add homes & move homes
        self.addHomes()
        self.moveHouses()

        if(self.groundPlan.isValid()): 
            print ("groundPlan is valid")
        else: 
            print ("groundPlan is invalid")
        
        print ("Value of groundPlan is:", self.groundPlan.getPlanValue())
        
        self.printResults()

        return

    def addPlaygrounds(self):
        x = 40
        y = self.groundPlan.HEIGHT - 50 - 30
        self.groundPlan.addPlayground(Playground(x, y).flip())
        x = self.groundPlan.WIDTH - 60
        y = 50
        self.groundPlan.addPlayground(Playground(x, y).flip())
        return

    def addWaterbodies(self):
        width = 80
        height = 40
        x = 0
        y = 0
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))
        width = 15
        height = 15
        x = self.groundPlan.WIDTH - 15
        y = 0
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))
        width = 15
        height = 15
        x = 0
        y = self.groundPlan.HEIGHT - 15
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))
        width = 80
        height = 40
        x = self.groundPlan.WIDTH - 80
        y = self.groundPlan.HEIGHT - 40
        self.groundPlan.addWaterbody(Waterbody(x, y, width, height))
        return

    def addHomes(self):
        while self.groundPlan.numberOfHouses() <= self.NUMBER_OF_HOUSES:
            if (self.groundPlan.number_of_mansions < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_MANSION_PERCENTAGE)):
                self.addToGroundPlan('Mansion')
            elif (self.groundPlan.number_of_bungalows < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_BUNGALOW_PERCENTAGE)):
                self.addToGroundPlan('Bungalow')
            elif (self.groundPlan.number_of_familyhomes < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_FAMILYHOMES_PERCENTAGE) + 1):
                self.addToGroundPlan('FamilyHome')
            else:
                break
        return

    # Add object to map (type)
    def addToGroundPlan(self, type):
        if (type == 'Mansion'):
            x = random() * (self.groundPlan.WIDTH - 11)
            y = random() * (self.groundPlan.HEIGHT - 10.5)  

            mansion = Mansion(x,y)
            if (self.groundPlan.correctlyPlaced(mansion)):
                self.groundPlan.addResidence(mansion)
                return True

        elif (type == 'Bungalow'):
            x = random() * (self.groundPlan.WIDTH - 10)
            y = random() * (self.groundPlan.HEIGHT - 7.5)

            bungalow = Bungalow(x, y).flip()
            if (self.groundPlan.correctlyPlaced(bungalow)):
                self.groundPlan.addResidence(bungalow)
                return True

        elif (type == 'FamilyHome'):
            x = random() * (self.groundPlan.WIDTH - 8)
            y = random() * (self.groundPlan.HEIGHT - 8)

            familyHome = FamilyHome(x, y)
            if (self.groundPlan.correctlyPlaced(familyHome)):
                self.groundPlan.addResidence(familyHome)
                return True

        # elif (type == 'playground'):
        #     x = random() * (self.groundPlan.WIDTH - 100)
        #     y = random() * (self.groundPlan.HEIGHT - 100)


        #     playground = Playground(x, y)
        #     if (self.groundPlan.correctlyPlaced(playground)):
        #         self.groundPlan.addPlayground(playground)

        # elif (type == 'waterbody'):    
        #     width = random() * 20 + 20
        #     height = random() * 30 + 30
        #     x = 10 + random() * (self.groundPlan.WIDTH - width - 10)
        #     y = 10 + random() * (self.groundPlan.HEIGHT - height - 10)

        #     waterbody = Waterbody(x, y, width, height)
        #     if (self.groundPlan.correctlyPlaced(waterbody)):
        #         self.groundPlan.addWaterbody(waterbody)  

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