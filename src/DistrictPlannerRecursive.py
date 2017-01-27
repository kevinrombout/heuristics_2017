from Groundplan import Groundplan
from GroundplanFrame import GroundplanFrame
from districtobjects.Mansion import Mansion
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from random import random

class DistrictPlannerRecursive(object):
    NUMBER_OF_HOUSES = 100
    PLAYGROUND       = True

    FIRST_HOME_X     = 0
    FIRST_HOME_Y     = 0

    SHOW_RESULTS     = False

    ADDITIONAL_CLEARANCE_OVERALL  = 0
    ADDITIONAL_CLEARANCE_FAMILY   = 0
    ADDITIONAL_CLEARANCE_BUNGALOW = 0
    ADDITIONAL_CLEARANCE_MANSION  = 5

    def __init__(self, x, y, showResults):
        self.FIRST_HOME_X = x
        self.FIRST_HOME_Y = y
        self.SHOW_RESULTS = showResults

        self.groundPlan = Groundplan(self.NUMBER_OF_HOUSES, True)


    def developGroundplan(self):

        # place playground & water
        self.addPlaygrounds()
        self.addWaterbodies()

        firstResidence = self.initFirstHome()

        if (firstResidence != False):
            self.addHomes(firstResidence)

        # print(self.groundPlan.number_of_familyhomes,
        #         self.groundPlan.number_of_bungalows,
        #         self.groundPlan.number_of_mansions)

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

        house = self.getHouse()

        if (house == False):
            return False


        x,y = self.getCoordinatesUp(residence, house)
        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        if (house == False):
            return False

        # PLACE RESIDENCE UP - RIGHT
        x,y = self.getCoordinatesUpRight(residence, house)
        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        if (house == False):
            return False

        # PLACE RESIDENCE RIGHT
        x,y = self.getCoordinatesRight(residence, house)

        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        if (house == False):
            return False

        # PLACE RESIDENCE DOWN - RIGHT
        x,y = self.getCoordinatesDownRight(residence, house)
        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        if (house == False):
            return False

        # PLACE RESIDENCE DOWN
        x,y = self.getCoordinatesDown(residence, house)
        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        if (house == False):
            return False

        # PLACE RESIDENCE DOWN - LEFT
        x,y = self.getCoordinatesDownLeft(residence, house)
        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        if (house == False):
            return False

        # PLACE RESIDENCE LEFT
        x,y = self.getCoordinatesLeft(residence, house)
        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        if (house == False):
            return False

        # PLACE RESIDENCE UP - LEFT
        x,y = self.getCoordinatesUpLeft(residence, house)
        newResidence = self.addToGroundPlan(house.getType(), x, y)

        if (newResidence):
            house = self.addHomes(newResidence)

        return house


    def getHouse(self):

        if (self.groundPlan.number_of_familyhomes < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_FAMILYHOMES_PERCENTAGE)):
            # print "Amount familyHomes: ", self.groundPlan.number_of_familyhomes, ' - ', self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_FAMILYHOMES_PERCENTAGE
            residence = FamilyHome(0,0)
            residence.minimumClearance = residence.getminimumClearance() + self.ADDITIONAL_CLEARANCE_FAMILY + self.ADDITIONAL_CLEARANCE_OVERALL
            return residence
        elif (self.groundPlan.number_of_bungalows < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_BUNGALOW_PERCENTAGE)):
            # print "Amount bungalows: ", self.groundPlan.number_of_bungalows, ' - ', self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_BUNGALOW_PERCENTAGE
            residence = Bungalow(0,0)
            residence.minimumClearance = residence.getminimumClearance() + self.ADDITIONAL_CLEARANCE_BUNGALOW + self.ADDITIONAL_CLEARANCE_OVERALL
            return residence
        elif (self.groundPlan.number_of_mansions < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_MANSION_PERCENTAGE)):
            # print "Amount mansions: ", self.groundPlan.number_of_mansions, ' - ', self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_MANSION_PERCENTAGE
            residence = Mansion(0,0)
            residence.minimumClearance = residence.getminimumClearance() + self.ADDITIONAL_CLEARANCE_MANSION + self.ADDITIONAL_CLEARANCE_OVERALL
            return residence

        return False


    def computeArea(self):

        area    = []
        nonArea = []
        count = 0
        for i in range(0, self.groundPlan.getWidth()):
            # print(count)
            for j in range(0, self.groundPlan.getWidth()):
                check = self.checkIsArea(i,j)
                if (check):
                    area.append([i,j])
                else:
                    nonArea.append([i,j])
            count = count+1

        return (float(len(area)) / (len(area) + len(nonArea))) * 100


    def checkIsArea(self, i, j):
        residences = self.groundPlan.getResidences()
        tmpHome = FamilyHome(i,j)
        tmpHome.height = 0
        tmpHome.width = 0

        waterbodies = self.groundPlan.getWaterbodies()
        playgrounds = self.groundPlan.getPlaygrounds()

        for waterbody in waterbodies:
            if (self.groundPlan.getDistance(tmpHome, waterbody) == 0):
                return False

        for playground in playgrounds:
            if (self.groundPlan.getDistance(tmpHome, playground) == 0):
                return False

        for residence in residences:
            res = self.groundPlan.getDistance(residence, tmpHome)
            if (res < residence.getminimumClearance()):
                return False
            if (res < 20):
                minimumClearance = self.groundPlan.getMinimumDistance(residence)
                if (res < minimumClearance):
                    return False
        return True

    def checkEnd(self):
        if (self.groundPlan.numberOfHouses() >= self.NUMBER_OF_HOUSES):
            return True
        return False


    # UP - LEFT
    def getCoordinatesUpLeft(self, oldResidence, newResidence):
        x = oldResidence.getX() - self.getMinimumClearance(oldResidence, newResidence) - newResidence.getWidth()
        y = oldResidence.getY() - self.getMinimumClearance(oldResidence, newResidence) - newResidence.getHeight()
        return x,y

    # UP
    def getCoordinatesUp(self, oldResidence, newResidence):
        x = oldResidence.getX()
        y = oldResidence.getY() - self.getMinimumClearance(oldResidence, newResidence) - newResidence.getHeight()
        return x,y

    # UP - RIGHT
    def getCoordinatesUpRight(self, oldResidence, newResidence):
        x = oldResidence.getX() + newResidence.getWidth() + self.getMinimumClearance(oldResidence, newResidence)
        y = oldResidence.getY() - self.getMinimumClearance(oldResidence, newResidence) - newResidence.getHeight()
        return x,y

    # RIGHT
    def getCoordinatesRight(self, oldResidence, newResidence):
        x = oldResidence.getX() + newResidence.getWidth() + self.getMinimumClearance(oldResidence, newResidence)
        y = oldResidence.getY()
        return x,y

    # DOWN - RIGHT
    def getCoordinatesDownRight(self, oldResidence, newResidence):
        x = oldResidence.getX() + newResidence.getWidth() + self.getMinimumClearance(oldResidence, newResidence)
        y = oldResidence.getY() + self.getMinimumClearance(oldResidence, newResidence) + newResidence.getHeight()
        return x,y

    # DOWN
    def getCoordinatesDown(self, oldResidence, newResidence):
        x = oldResidence.getX()
        y = oldResidence.getY() + self.getMinimumClearance(oldResidence, newResidence) + newResidence.getHeight()
        return x,y

    # DOWN - LEFT
    def getCoordinatesDownLeft(self, oldResidence, newResidence):
        x = oldResidence.getX() - self.getMinimumClearance(oldResidence, newResidence) - newResidence.getWidth()
        y = oldResidence.getY() + self.getMinimumClearance(oldResidence, newResidence) + newResidence.getHeight()
        return x,y

    # LEFT
    def getCoordinatesLeft(self, oldResidence, newResidence):
        x = oldResidence.getX() - self.getMinimumClearance(oldResidence, newResidence) - newResidence.getWidth()
        y = oldResidence.getY()
        return x,y


    #
    #   Compute the the highest minimum clearance between old and new house
    #
    def getMinimumClearance(self, oldResidence, newResidence):
        old = oldResidence.getminimumClearance()
        new = newResidence.getminimumClearance()
        return max(old,new)


    # Add object to map (type)
    def addToGroundPlan(self, type, x_coordinate, y_coordinate):
        if (self.checkEnd()) :
            return False

        if (type == 'Mansion'):
            mansion = Mansion(x_coordinate,y_coordinate)
            mansion.minimumClearance = mansion.getminimumClearance() + self.ADDITIONAL_CLEARANCE_FAMILY + self.ADDITIONAL_CLEARANCE_OVERALL
            if (self.groundPlan.correctlyPlaced(mansion)):
                self.groundPlan.addResidence(mansion)
                return mansion
        elif (type == 'Bungalow'):
            bungalow = Bungalow(x_coordinate,y_coordinate)
            bungalow.minimumClearance = bungalow.getminimumClearance() + self.ADDITIONAL_CLEARANCE_FAMILY + self.ADDITIONAL_CLEARANCE_OVERALL
            if (self.groundPlan.correctlyPlaced(bungalow)):
                self.groundPlan.addResidence(bungalow)
                return bungalow
            if (self.groundPlan.correctlyPlaced(bungalow.flip())):
                self.groundPlan.addResidence(bungalow)
                return bungalow

        elif (type == 'FamilyHome'):
            familyHome = FamilyHome(x_coordinate,y_coordinate)
            familyHome.minimumClearance = familyHome.getminimumClearance() + self.ADDITIONAL_CLEARANCE_FAMILY + self.ADDITIONAL_CLEARANCE_OVERALL
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
        # print("Minimal clearance FamilyHomes: ", min(familyHomes))
        # print("Minimal clearance Bungalows: ", min(bungalows))
        # print("Minimal clearance Mansions: ", min(mansions))

        usedArea = self.computeArea()
        print("free space: ",usedArea,"%")
        print("used space: ",100-usedArea,"%")


        print(mansions)
        print(bungalows)
        print(familyHomes)


###
 #
 #  Bereken voor een paar initiele begincoordinaten van het eerste huisje hoe de huisjes het
 #  beste verdeeld kunnen worden over de beschikbare grond
 #
###
def computeSpaceAllocation():
    X_COR_HOUSE = 117
    Y_COR_HOUSE = 91

    planner = DistrictPlannerRecursive(X_COR_HOUSE, Y_COR_HOUSE, True)
    value = planner.developGroundplan()
    print "De waarde van de verdeling bedraagt: ", value;

    return


###
 #
 #  Ga voor alle mogelijke beginposities (afhankelijk van de grote van het eerste huisje)
 #  na wat de positie is waarbij de hoogst mogelijke waarde behaald kan worden
 #
###
def computeInitialState():

    LENGTH_AREA  = 170
    WIDTH_AREA   = 200

    LENGTH_HOME  = 8
    WIDTH_HOME   = 8

    ADDITIONAL_SPACE = 5

    results = []
    highest = [0,0,0]

    for i in range(0, WIDTH_AREA, WIDTH_HOME + ADDITIONAL_SPACE):
        print((float(i) / WIDTH_AREA) * 100, '%')
        for j in range(0, LENGTH_AREA, LENGTH_HOME + ADDITIONAL_SPACE):
            planner = DistrictPlannerRecursive(i,j, False)
            value = planner.developGroundplan()
            res = [i,j,value]
            if (res[2] > 0) :
                if (res[2] >= highest[2]) :
                    highest = res
                results.append(res)

    print "alle resultaten:" , results
    print "beste resultaat:" , highest

    return


computeSpaceAllocation()
# computeInitialState()



