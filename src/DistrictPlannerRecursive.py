from Groundplan import Groundplan
from GroundplanFrame import GroundplanFrame
from districtobjects.Mansion import Mansion
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from random import random

class DistrictPlannerRecursive(object):
    NUMBER_OF_HOUSES = 150
    PLAYGROUND       = True

    FIRST_HOME_X     = 0
    FIRST_HOME_Y     = 0

    SHOW_RESULTS     = False;


    def __init__(self, x, y, showResult):
        self.FIRST_HOME_X = x
        self.FIRST_HOME_Y = y
        self.SHOW_RESULTS = showResult

        self.groundPlan = Groundplan(self.NUMBER_OF_HOUSES, True)


    def developGroundplan(self):

        # place playground & water
        self.addPlaygrounds()
        self.addWaterbodies()

        firstResidence = self.initFirstHome()

        if (firstResidence != False):
            self.addHomes(firstResidence)

        if (self.SHOW_RESULTS) :
            if(self.groundPlan.isValid()): 
                print ("groundPlan is valid")
            else: 
                print ("groundPlan is invalid")
        
            print ("Value of groundPlan is:", self.groundPlan.getPlanValue())
        
            self.printResults()

        planValue = self.groundPlan.getPlanValue()

        if (self.SHOW_RESULTS) :
            self.frame = GroundplanFrame(self.groundPlan)
            self.frame.setPlan()
            self.frame.root.mainloop()

        return planValue


    def initFirstHome(self):
        return self.addToGroundPlan('FamilyHome', self.FIRST_HOME_X, self.FIRST_HOME_Y)


    # Add homes recursively based on initial first placed home
    def addHomes(self, residence):

        # PLACE RESIDENCE UP
        x,y = self.getCoordinatesUp(residence)
        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)


        # PLACE RESIDENCE UP - RIGHT
        x,y = self.getCoordinatesUpRight(residence)
        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)


        # PLACE RESIDENCE RIGHT
        x,y = self.getCoordinatesRight(residence)

        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)        


        # PLACE RESIDENCE DOWN - RIGHT
        x,y = self.getCoordinatesDownRight(residence)
        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)        


        # PLACE RESIDENCE DOWN
        x,y = self.getCoordinatesDown(residence)
        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)        


        # PLACE RESIDENCE DOWN - LEFT
        x,y = self.getCoordinatesDownLeft(residence)
        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)        


        # PLACE RESIDENCE LEFT
        x,y = self.getCoordinatesLeft(residence)
        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)        


        # PLACE RESIDENCE UP - LEFT
        x,y = self.getCoordinatesUpLeft(residence)
        newResidence = self.addToGroundPlan('FamilyHome', x, y)

        if (newResidence):
            self.addHomes(newResidence)                    


    def checkEnd(self):
        if (self.groundPlan.numberOfHouses() >= self.NUMBER_OF_HOUSES):
            return True    
        return False

    # UP - LEFT
    def getCoordinatesUpLeft(self, residence):
        x = residence.getX() - residence.getminimumClearance() - residence.getminimumClearance() - residence.getWidth()
        y = residence.getY() - residence.getminimumClearance() - residence.getminimumClearance() - residence.getHeight()
        return x,y        

    # UP
    def getCoordinatesUp(self, residence):
        x = residence.getX()
        y = residence.getY() - residence.getminimumClearance() - residence.getminimumClearance() - residence.getHeight()
        return x,y

    # UP - RIGHT
    def getCoordinatesUpRight(self, residence):
        x = residence.getX() + residence.getWidth() + residence.getminimumClearance() + residence.getminimumClearance()
        y = residence.getY() - residence.getminimumClearance() - residence.getminimumClearance() - residence.getHeight()
        return x,y        

    # RIGHT
    def getCoordinatesRight(self, residence):
        x = residence.getX() + residence.getWidth() + residence.getminimumClearance() + residence.getminimumClearance()
        y = residence.getY()
        return x,y

    # DOWN - RIGHT
    def getCoordinatesDownRight(self, residence):
        x = residence.getX() + residence.getWidth() + residence.getminimumClearance() + residence.getminimumClearance()
        y = residence.getY() + residence.getminimumClearance() + residence.getminimumClearance() + residence.getHeight()
        return x,y

    # DOWN
    def getCoordinatesDown(self, residence):
        x = residence.getX()
        y = residence.getY() + residence.getminimumClearance() + residence.getminimumClearance() + residence.getHeight()
        return x,y        

    # DOWN - LEFT
    def getCoordinatesDownLeft(self, residence):
        x = residence.getX() - residence.getminimumClearance() - residence.getminimumClearance() - residence.getWidth()
        y = residence.getY() + residence.getminimumClearance() + residence.getminimumClearance() + residence.getHeight()
        return x,y

    # LEFT
    def getCoordinatesLeft(self, residence):
        x = residence.getX() - residence.getminimumClearance() - residence.getminimumClearance() - residence.getWidth()
        y = residence.getY()
        return x,y


    # Add object to map (type)
    def addToGroundPlan(self, type, x_coordinate, y_coordinate):
        if (self.checkEnd()) :
            return False

        if (type == 'Mansion'):
            mansion = Mansion(x_coordinate,y_coordinate)
            if (self.groundPlan.correctlyPlaced(mansion)):
                self.groundPlan.addResidence(mansion)
                return mansion
        elif (type == 'Bungalow'):
            bungalow = Bungalow(x_coordinate,y_coordinate)
            if (self.groundPlan.correctlyPlaced(bungalow)):
                self.groundPlan.addResidence(bungalow)
                return bungalow
            if (self.groundPlan.correctlyPlaced(bungalow.flip())):
                self.groundPlan.addResidence(bungalow)
                return bungalow

        elif (type == 'FamilyHome'):
            familyHome = FamilyHome(x_coordinate,y_coordinate)        
            if (self.groundPlan.correctlyPlaced(familyHome)):
                self.groundPlan.addResidence(familyHome)
                return familyHome

        # residence cant be placed                
        return False


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
        # print("Minimal clearance Bungalows: ", min(bungalows))
        # print("Minimal clearance Mansions: ", min(mansions))

        # print(mansions)
        # print(bungalows)
        print(familyHomes)


###
 #
 #  Bereken voor een initiele begincoordinaten van het eerste huisje hoe de huisjes het
 #  beste verdeeld kunnen worden over de beschikbare grond
 #
###  
X_COR_HOUSE = 140
Y_COR_HOUSE = 100

planner = DistrictPlannerRecursive(X_COR_HOUSE, Y_COR_HOUSE, True)
value = planner.developGroundplan()
print "De waarde van de verdeling bedraagt: ", value;

exit()
###
 #
 #  Ga voor alle mogelijke beginposities (afhankelijk van de grote van het eerste huisje)
 #  na wat de positie is waarbij de hoogst mogelijke waarde behaald kan worden
 #
###  
LENGTH_AREA  = 170
WIDTH_AREA   = 200

LENGTH_HOME  = 10
WIDTH_HOME   = 10

results = []
highest = [0,0,0]

for i in range(0, WIDTH_AREA, WIDTH_HOME):
    for j in range(0, LENGTH_AREA, LENGTH_HOME):
        planner = DistrictPlannerRecursive(i,j, False)
        value = planner.developGroundplan()
        res = [i,j,value]
        if (res[2] > 0) :
            if (res[2] >= highest[2]) :
                highest = res
            results.append(res)

print "alle resultaten:" , results
print "beste resultaat:" , highest
