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
    PLAYGROUND = False
    
    def __init__(self):
        self.groundPlan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)
        self.plan = self.developGroundplan()
        self.frame = GroundplanFrame(self.groundPlan)
        self.frame.setPlan()
        self.lastPlacedObject = ''
        
        """your code""" 
        
        self.frame.root.mainloop()


    def developGroundplan(self):


        # place playground

        # add Homes Randomly
        self.addHomes()

        if(self.groundPlan.isValid()): 
            print "groundPlan is valid"

        else: 
            print "groundPlan is invalid"
        
        print "Value of groundPlan is:", self.groundPlan.getPlanValue()
        
        return

    def addHomes(self):

        while self.groundPlan.numberOfHouses() <= self.NUMBER_OF_HOUSES:
            if (self.groundPlan.number_of_mansions < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_MANSION_PERCENTAGE)):
                self.addToGroundPlan('mansion')
            elif (self.groundPlan.number_of_bungalows < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_BUNGALOW_PERCENTAGE)):
                self.addToGroundPlan('bungalow')
            elif (self.groundPlan.number_of_familyhomes < (self.NUMBER_OF_HOUSES * self.groundPlan.MINIMUM_FAMILYHOMES_PERCENTAGE)):
                self.addToGroundPlan('family_home')
            else:
                break

        return


    # Add object to map (type)
    def addToGroundPlan(self, type):
        if (type == 'mansion'):
            x = 10 + random() * (self.groundPlan.WIDTH - 50)
            y = 10 + random() * (self.groundPlan.HEIGHT - 50)  

            mansion = Mansion(x,y)
            if (self.groundPlan.correctlyPlaced(mansion)):
                self.groundPlan.addResidence(mansion)
                print "Placing a mansion at location:", x, ",", y            

        elif (type == 'bungalow'):
            x = 10 + random() * (self.groundPlan.WIDTH - 50)
            y = 10 + random() * (self.groundPlan.HEIGHT - 50)

            bungalow = Bungalow(x, y).flip()
            if (self.groundPlan.correctlyPlaced(bungalow)):
                self.groundPlan.addResidence(bungalow) 
                print "Placing a bungalow at location:", x, ",", y

        elif (type == 'family_home'):
            x = 10 + random() * (self.groundPlan.WIDTH - 50)
            y = 10 + random() * (self.groundPlan.HEIGHT - 50)

            familyHome = FamilyHome(x, y)
            if (self.groundPlan.correctlyPlaced(familyHome)):
                self.groundPlan.addResidence(familyHome) 
                print "Placing a family home at location:", x, ",", y     

        elif (type == 'playground'):
            x = 50 + random() * (self.groundPlan.WIDTH - 100)
            y = 50 + random() * (self.groundPlan.HEIGHT - 100)


            playground = Playground(x, y)
            if (self.groundPlan.correctlyPlaced(playground)):
                self.groundPlan.addPlayground(playground)
                print "Placing a playground at location: ", x, ",", y

        elif (type == 'waterbody'):    
            width = random() * 20 + 20
            height = random() * 30 + 30
            x = 10 + random() * (self.groundPlan.WIDTH - width - 10)
            y = 10 + random() * (self.groundPlan.HEIGHT - height - 10)

            waterbody = Waterbody(x, y, width, height)
            if (self.groundPlan.correctlyPlaced(waterbody)):
                self.groundPlan.addWaterbody(waterbody)  
                print "Placing a waterbody at location: ", x, ",", y, "of size", width, "x", height                            

        return


    # Remove object from map (type)

    # Remove object from map (type)    


    
DistrictPlanner()