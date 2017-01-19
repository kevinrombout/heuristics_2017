from Groundplan import Groundplan
from GroundplanFrame import GroundplanFrame
from districtobjects.Mansion import Mansion
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody

class DistrictPlannerRecursive(object):
    NUMBER_OF_HOUSES = 100
    PLAYGROUND = True
    FIRST_HOME_X = 50
    FIRST_HOME_Y = 100
    directions = range(8) 
    housesss = 0
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

        firstResidence = self.initFirstHome()
       # print(firstResidence)
        #print(len(self.groundPlan.residences))
        self.recursivePlacingMethod(firstResidence, self.defineNextResidence(), True)
        
        if(self.groundPlan.isValid()): 
            print ("groundPlan is valid")
        else: 
            print ("groundPlan is invalid")
        
        print ("Value of groundPlan is:", self.groundPlan.getPlanValue())
        
        self.printResults()

        return
        

    
    def initFirstHome(self):
        initHome = FamilyHome(self.FIRST_HOME_X, self.FIRST_HOME_Y)
        if(self.checkAvailabilityResidence(initHome)):
            self.addResidenceToPlan(initHome)
        return initHome
    
    def addResidenceToPlan(self, whut):
        self.groundPlan.addResidence(whut)
        return
        
    def checkAvailabilityResidence(self, placeable):
        return self.groundPlan.correctlyPlaced(placeable)
        
     
    def checkEnd(self):
        if (self.housesss >= self.NUMBER_OF_HOUSES):
            return True    
        return False

       
    def recursivePlacingMethod(self, oldResidence, newResidence, full):
        if(self.checkEnd()):
            
            full = False
        print(self.housesss)   
        for direction in self.directions:
            #print(direction)
            newX, newY = self.switchDirection(direction, oldResidence, newResidence)
            newResidence.x = newX
            newResidence.y = (newY)   
            if(self.checkAvailabilityResidence(newResidence) and full is True):
                #print("number",self.housesss)
               # if(self.housesss <5 or self.housesss >45):
                  #  print(newX)
                  #  print(newY)
                print("succees",newX,newY)
                self.housesss +=1
                self.addResidenceToPlan(newResidence)
                oldResidence = newResidence
                newResidence = self.defineNextResidence()
                full = self.recursivePlacingMethod(oldResidence, newResidence, full)
                if(full == False):
                    return full
#            else:
#                newResidence = newResidence.flip()
#                newX, newY = self.switchDirection(direction, oldResidence, newResidence)
#                newResidence.setX(newX)
#                newResidence.setY(newY)
#                if(self.checkAvailabilityResidence(newResidence)):
#                    self.addResidenceToPlan(newResidence)
#                    oldResidence = newResidence
#                    newResidence = self.defineNextResidence()
#                self.recursivePlacingMethod(oldResidence, newResidence)
        return  full       
            
            
            
   
    def defineNextResidence(self):
        return FamilyHome(-1,-1)
   
    def switchDirection(self, argument, oldResidence, newResidence):
       clearance = max(oldResidence.getminimumClearance(),newResidence.getminimumClearance()) 
      
       if(argument == 0):
           return self.getCoordinatesUp(oldResidence, newResidence, clearance)
       elif(argument == 1):
           return self.getCoordinatesUpRight(oldResidence, newResidence, clearance)
       elif(argument == 2):
           return self.getCoordinatesRight(oldResidence, newResidence, clearance)
       elif(argument == 3):
           return self.getCoordinatesDownRight(oldResidence, newResidence, clearance)
       elif(argument == 4):
           return self.getCoordinatesDown(oldResidence, newResidence, clearance)
       elif(argument == 5):
           return self.getCoordinatesDownLeft(oldResidence, newResidence, clearance)
       elif(argument == 6):
           return self.getCoordinatesLeft(oldResidence, newResidence, clearance)
       elif(argument == 7):
           return self.getCoordinatesUpLeft(oldResidence, newResidence, clearance)
   
    def getCoordinatesUp(self, oldResidence, newResidence, clearance):   
       x = oldResidence.getX()
       y = oldResidence.getY()- clearance - newResidence.getHeight()
       return x,y
        
    def getCoordinatesUpRight(self, oldResidence, newResidence, clearance):
       x = oldResidence.getX() + oldResidence.getWidth() + clearance
       y = oldResidence.getY()- clearance - newResidence.getHeight()
       return x,y
       
    def getCoordinatesRight(self, oldResidence, newResidence, clearance):
       x = oldResidence.getX() + oldResidence.getWidth() + clearance
       y = oldResidence.getY()
       return x,y
       
    def getCoordinatesDownRight(self, oldResidence, newResidence, clearance):
       x = oldResidence.getX() + oldResidence.getWidth() + clearance
       y = oldResidence.getY() + oldResidence.getHeight() + clearance 
       return x,y

    def getCoordinatesDown(self, oldResidence, newResidence, clearance):
        x = oldResidence.getX()
        y = oldResidence.getY() + oldResidence.getHeight() + clearance 
        return x,y

    def getCoordinatesDownLeft(self, oldResidence, newResidence, clearance):
        x = oldResidence.getX() - clearance - newResidence.getWidth()
        y = oldResidence.getY() + oldResidence.getHeight() + clearance 
        return x,y
     
    def getCoordinatesLeft(self, oldResidence, newResidence, clearance):     
        x = oldResidence.getX() - clearance - newResidence.getWidth()
        y = oldResidence.getY()
        return x,y
        
    def getCoordinatesUpLeft(self, oldResidence, newResidence, clearance):    
        x = oldResidence.getX() - clearance - newResidence.getWidth()
        y = oldResidence.getY()- clearance - newResidence.getHeight()
        return x,y



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
        #print("Minimal clearance FamilyHomes: ", min(familyHomes))
        # print("Minimal clearance Bungalows: ", min(bungalows))
        # print("Minimal clearance Mansions: ", min(mansions))

        # print(mansions)
        # print(bungalows)
        print(familyHomes)

    
DistrictPlannerRecursive()