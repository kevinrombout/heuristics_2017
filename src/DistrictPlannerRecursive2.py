from Groundplan import Groundplan
from GroundplanFrame import GroundplanFrame
from districtobjects.Mansion import Mansion
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from random import random
import time
import numpy


class DistrictPlanner(object):
    clearanceFamDict = {}
    clearanceBunDict = {}
    clearanceManDict = {}
    clearanceFam = []
    clearanceBun = []
    clearanceMan = []
    times = []
    works = []
    areaUsed = []

    PRINT_STEP              = False
    
    NUMBER_OF_HOUSES        = 0
    PLAYGROUND              = False
    NUMBER_OF_PLAYGROUNDS   = 0
    NUMBER_OF_WATERBODIES   = 4

    FAMILY_HOME_CLEARANCE   = 2
    BUNGALOW_CLEARANCE      = 3
    MANSION_CLEARANCE       = 6

    familyHomesClearance    = 0
    bungalowClearance       = 0
    mansionClearance        = 0

    stats                   = {}
    bestGroundPlan          = Groundplan(40,1)
    groundPlan              = Groundplan(40,1)
    time                    = 0

    house_type              = 'FamilyHome'
    Advanced                = True
    
    def __init__(self, x = 0, y = -1, numberOfHouses = 40, 
                 numberOfPlaygrounds = 1, printStatistics = True, printPlan=True, printResult = False, numberOfGroundplans=1):
        self.NUMBER_OF_HOUSES       = numberOfHouses
        self.PLAYGROUND             = numberOfPlaygrounds > 0
        self.NUMBER_OF_PLAYGROUNDS  = numberOfPlaygrounds
        
        self.printPlan              = printPlan
        self.printResult            = printResult
        self.printStatistics        = printStatistics
        self.printClearances        = printResult
        
        self.saveResultsOfArea      = True 
        self.resetClearanceInfo()        
        self.iterative              = False
        
        self.stats = {
                'revenue_valid' :[],
                'revenue'       :[],
                'min_cl_f'      :[],
                'min_cl_b'      :[],
                'min_cl_m'      :[],
                'avg_cl_f'      :[],
                'avg_cl_b'      :[],
                'avg_cl_m'      :[],
                'runtime'       :[],
                'valid'         :[],
                'used_area'     :[],
                'unused_area'   :[]
            }

        for i in range(numberOfGroundplans):
            self.first_x = x
            self.first_y = y
            self.startExperiment()
            print(i+1, 'valid' if self.bestGroundPlan.isValid() else 'invalid')
        print()
        print("STATS")

        self.printPlan              = True
        self.printClearances        = False
        self.printStatistics        = True
        
        self.printResults(self.bestGroundPlan)
    
    
    #################################################
    #               START EXPERIMENT                #
    #################################################

    def startExperiment(self):
        self.time = time.time()
        self.bestGroundPlan         = Groundplan(40,1)
        self.groundPlan             = Groundplan(40,1)
        if(self.iterative):
            self.iterativeUpgratingClearance()
        elif(self.Advanced):
            self.developGroundPlanAdvanced()
        else:
            self.hillClimbing()
        self.saveStats(self.bestGroundPlan)
        # self.printResults(self.bestGroundPlan)
        
    ####################################
    #System With upgrading clearances iterative
    def iterativeUpgratingClearance(self):
        delta = 1
        self.mansionClearance       = self.MANSION_CLEARANCE
        self.bungalowClearance      = self.BUNGALOW_CLEARANCE
        self.familyHomesClearance   = self.FAMILY_HOME_CLEARANCE

        while(self.doesFitOnGroundPlan()):
            #self.mansionClearance       += delta
            #self.bungalowClearance      += delta
            self.familyHomesClearance   += delta
        self.returnToNormalClearance(self.bestGroundPlan)

    def doesFitOnGroundPlan(self):
        self.developGroundPlan()
        if self.PRINT_STEP:
            self.frame = GroundplanFrame(self.groundPlan)
            self.frame.setPlan()
            self.frame.root.mainloop()
        if self.numberOfHousesReached():
            self.loadClearances(self.groundPlan)
            if not (min(self.clearanceFam) == self.familyHomesClearance):
                return False
            if self.bestGroundPlan.getPlanValue() <= self.groundPlan.getPlanValue():
                self.bestGroundPlan = self.groundPlan
            return True
        return False
     
    def returnToNormalClearance(self, groundPlan):
        residences = groundPlan.getResidences()
        for residence in residences:
            groundPlan.removeResidence(residence)
            if(residence.getType() == "FamilyHome"):
                residence.minmalClearance = self.FAMILY_HOME_CLEARANCE
            elif(residence.getType() == "Bungalow"):
                residence.minmalClearance = self.BUNGALOW_CLEARANCE
            elif(residence.getType() == "Mansion"):
                residence.minmalClearance = self.MANSION_CLEARANCE
            groundPlan.addResidence(residence)
            

    #################################################
    #               HILLCLIMBING ALGORITHM         #
    #################################################


    def hillClimbing(self):
        self.mansionClearance       = self.MANSION_CLEARANCE
        self.bungalowClearance      = self.BUNGALOW_CLEARANCE
        self.familyHomesClearance   = self.FAMILY_HOME_CLEARANCE
        self.developGroundPlan()
        while(not self.numberOfHousesReached()):
            self.developGroundPlan()
       # self.printPlan = True
       # self.printResults(self.groundPlan)
       # self.printPlan = False
        improvement = True
        numberOfHousess = self.groundPlan.numberOfHouses()
       # residences = self.groundPlan.getResidences()
        starttijd = time.time()
        noImprovements = 0
        while (improvement): 
            newGroundPlanValue = self.groundPlan.getPlanValue()
            improvement = False
            for i in range(numberOfHousess):
                # j = numberOfHousess - i - 1
                 #Residence = residences[j]
                 Residence = self.groundPlan.getResidence(i)
                 improvement = self.checkAvailability(Residence)
                 if(improvement):
                     #residences = self.groundPlan.getResidences()
                     break
            
            newGroundPlanValue2 = self.groundPlan.getPlanValue()
           # print(newGroundPlanValue)
           # print(newGroundPlanValue2)
            if(newGroundPlanValue == newGroundPlanValue2):
                noImprovements += 1
            else:
                noImprovements = 0
            if(noImprovements >=10):
                improvement = False    
            else:
                improvement = True
            end = time.time()
            if(end-starttijd >60.0):
                 print("ed")
                 improvement = False
         #   print(end-starttijd)
        self.bestGroundPlan = self.groundPlan
  
    def checkAvailability(self, residence):
        #if(residence.getType() != "Mansion"):
         #   return False
        oldX = residence.x
        oldY = residence.y
        newGroundPlanValue = self.groundPlan.getPlanValue()
       # print(newGroundPlanValue)
        self.groundPlan.removeResidence(residence)
        x = None
        y = None
        if(residence.getType() == "FamilyHome"):
            distance = 5
        elif(residence.getType() == "Bungalow"):
            distance = 10
        else:
            distance = 80
        for i in range(-distance,distance):
             for j in range(-distance,distance):
                 if(i != 0 and j!=0 and (i == j or i == -j or i ==0 or j ==0)):
                     residence.x = oldX + i*0.5
                     residence.y = oldY + j*0.5
                     if(self.groundPlan.correctlyPlaced(residence)):
                         self.groundPlan.addResidence(residence)
                         if(newGroundPlanValue <= self.groundPlan.getPlanValue()):
                             newGroundPlanValue = self.groundPlan.getPlanValue()
                             x = oldX + i*0.5
                             y = oldY + j*0.5
                         self.groundPlan.removeResidence(residence)
        if(x is not None):
            #print("improvement")
            residence.x = x
            residence.y = y
            self.groundPlan.addResidence(residence)
            return True
        else:
            # print("No improvement")
             residence.x = oldX
             residence.y = oldY
             self.groundPlan.addResidence(residence)
             return False


    #################################################
    #               EXECUTE PLACING METHODS         #
    #################################################

    def developGroundPlan(self):
        self.groundPlan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)
        self.addWaterbodies()
        self.addPlayground() 
        self.initFirstHome()
        self.recursivePlacingMethod(False)


    def addPlayground(self):
        if(self.NUMBER_OF_PLAYGROUNDS == 1):
            x = [90]
            y = [70]
        elif(self.NUMBER_OF_PLAYGROUNDS == 2):
            x = [40, self.groundPlan.WIDTH - 60]
            y = [self.groundPlan.HEIGHT - 50 - 30, 50]
        for i in range(self.NUMBER_OF_PLAYGROUNDS):
            self.groundPlan.addPlayground(Playground(x[i], y[i]).flip())
        return


    def addWaterbodies(self):
        if(self.NUMBER_OF_PLAYGROUNDS < 2):
            width = [21,21,21,21]
            height = [83.5,83.5,83.5,83.5]
            x = [0,0,179,179]
            y = [0, 86.5, 0, 86.5]        
        elif(self.NUMBER_OF_PLAYGROUNDS == 2):
            width = [80, 14.2, 14.2, 80]
            height = [40,14.2, 14.2, 40]
            x = [0, self.groundPlan.WIDTH - 14.2, 0, self.groundPlan.WIDTH - 80]
            y = [0, 0, self.groundPlan.HEIGHT - 14.2, self.groundPlan.HEIGHT - 40]
            
        for i in range(self.NUMBER_OF_WATERBODIES):
            self.groundPlan.addWaterbody(Waterbody(x[i], y[i], width[i], height[i]))
        return
    

    def initFirstHome(self):
        initHome = self.defineNextResidence()
       # initHome.x = self.first_x
        #initHome.y = self.first_y
        while not self.groundPlan.correctlyPlaced(initHome):
            initHome.x = random() * 200
            initHome.y = random() * 170
            self.first_x = initHome.x
            self.first_y = initHome.y
        self.groundPlan.addResidence(initHome)
        return      
    

    def recursivePlacingMethod(self, stop):
        if(self.numberOfHousesReached()):
            return True
        oldResidence = self.findLastAddedResidence()
        for direction in range(8):
            for flip in [0,1]:
                newResidence = self.defineNextResidence()
                if(flip == 1):
                    newResidence = newResidence.flip()
                newX, newY = self.getCoordinatesBasedOnDirection(direction, oldResidence, newResidence)
                newResidence.x = newX
                newResidence.y = newY
                if(self.groundPlan.correctlyPlaced(newResidence)):
                    self.groundPlan.addResidence(newResidence)
                    stop = self.recursivePlacingMethod(stop)
                if(stop):
                    return stop
        return stop

        
    def numberOfHousesReached(self):
        return self.groundPlan.numberOfHouses() == self.groundPlan.number_of_houses


    def findLastAddedResidence(self):
        return self.groundPlan.getResidence(self.groundPlan.numberOfHouses()-1)
        

    def defineNextResidence(self):
        familyHomes = self.groundPlan.number_of_familyhomes
        bungalows = self.groundPlan.number_of_bungalows
        mansions = self.groundPlan.number_of_mansions    
        requiredHouses = self.groundPlan.number_of_houses
        percFamily = self.groundPlan.MINIMUM_FAMILYHOMES_PERCENTAGE
        percBungalow = self.groundPlan.MINIMUM_BUNGALOW_PERCENTAGE
        percMansions = self.groundPlan.MINIMUM_MANSION_PERCENTAGE   
        if(familyHomes < requiredHouses*percFamily):
            family = FamilyHome(1,1)
            family.minimumClearance = self.familyHomesClearance
            return family
        elif(bungalows < requiredHouses*percBungalow):
            bungalow = Bungalow(1,1)
            bungalow.minimumClearance = self.bungalowClearance
            return bungalow
        elif(mansions< requiredHouses*percMansions):
            mansion = Mansion(1,1)
            mansion.minimumClearance = self.mansionClearance
            return mansion


    def getCoordinatesBasedOnDirection(self, direction, oldResidence, newResidence):
        clearance = max(oldResidence.getminimumClearance(),newResidence.getminimumClearance())
        x_directions = [ 0 , 1 , 0 , -1, 1 , 1,-1, -1]
        y_directions = [-1 , 0 , 1 , 0 , 1 ,-1, 1, -1]        
        x_dir = x_directions[direction]
        y_dir = y_directions[direction]
        return self.getNewCoordinates(oldResidence, newResidence, clearance, x_dir, y_dir)        


    def getNewCoordinates(self, oldResidence, newResidence, clearance, x_dir, y_dir):
        x = oldResidence.getX() + x_dir * (oldResidence.getWidth() + clearance) 
        y = oldResidence.getY() + y_dir * (newResidence.getHeight() + clearance)
        return x,y


    #################################################
    #               ADVANCED FUNCTIONS              #
    #################################################               


    def developGroundPlanAdvanced(self):
        self.groundPlan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)
        self.addWaterbodies()
        self.addPlayground() 
        # homes = ['FamilyHome','Bungalow','Mansion']
        # homes = ['FamilyHome','Mansion','Bungalow']
        # homes = ['Bungalow','FamilyHome','Mansion']
        # homes = ['Bungalow','Mansion','FamilyHome'] 
        # homes = ['Mansion','Bungalow','FamilyHome']
        # homes = ['Mansion','FamilyHome','Bungalow'] 
        homes = ['Mansion','Bungalow','FamilyHome']                                
        for home in homes:
            self.house_type = home
            self.initFirstHomeAdvanced()
            self.recursivePlacingMethodAdvanced(False)
            if (self.numberOfHousesReached()):
                break
        self.bestGroundPlan = self.groundPlan


    def defineNextResidenceAdvanced(self): 
        if (self.house_type == 'FamilyHome'):
            family = FamilyHome(1,1)
            # family.minimumClearance = self.familyHomesClearance
            return family
        elif (self.house_type == 'Bungalow'):
            bungalow = Bungalow(1,1)
            # bungalow.minimumClearance = self.bungalowClearance
            return bungalow
        elif (self.house_type == 'Mansion'):
            mansion = Mansion(1,1)
            # mansion.minimumClearance = self.mansionClearance
            return mansion    


    def recursivePlacingMethodAdvanced(self, stop):
        if(self.numberOfHousesReached()):
            return True
        oldResidence = self.findLastAddedResidence()
        for direction in range(8):
            for flip in [0,1]:
                if(self.numberOfHousesReached()):
                    return True                
                newResidence = self.defineNextResidenceAdvanced()
                if(flip == 1):
                    newResidence = newResidence.flip()                    
                newX, newY = self.getCoordinatesBasedOnDirection(direction, oldResidence, newResidence)
                newResidence.x = newX
                newResidence.y = newY
                if(self.groundPlan.correctlyPlaced(newResidence)):
                    self.groundPlan.addResidence(newResidence)
                    stop = self.recursivePlacingMethodAdvanced(stop)
                if(stop):
                    return stop
        return stop     


    def initFirstHomeAdvanced(self):
        initHome = self.defineNextResidenceAdvanced()
       # initHome.x = self.first_x
        #initHome.y = self.first_y
        while not self.groundPlan.correctlyPlaced(initHome):
            initHome.x = random() * 200
            initHome.y = random() * 170
            self.first_x = initHome.x
            self.first_y = initHome.y
        self.groundPlan.addResidence(initHome)
        return                   
        
    #################################################
    #               STATISTICS                      #
    #################################################               
   
    def saveStats(self, groundPlan):
        if(groundPlan.isValid()):
            self.saveRevenueIfValid(groundPlan)
            if(self.saveResultsOfArea):
                self.loadClearances(groundPlan) 
                self.saveResultsArea(groundPlan)
                self.saveClearance(groundPlan)
        self.stats['revenue'].append(self.bestGroundPlan.getPlanValue()) 
        self.stats['runtime'].append(time.time() - self.time)
        self.stats['valid'].append(self.bestGroundPlan.isValid()*1)
    
    def saveRevenueIfValid(self, groundPlan): 
       self.stats['revenue_valid'].append(groundPlan.getPlanValue())
    
    def saveResultsArea(self, groundPlan):
        usedArea = self.computeUsedArea(groundPlan)
        self.stats['used_area'].append(usedArea),
        self.stats['unused_area'].append(100-usedArea)
    
    def saveClearance(self, groundPlan):
        f = self.clearanceFam
        b = self.clearanceBun
        m = self.clearanceMan
        if len(f)>0:
            self.stats['min_cl_f'].append(min(f))
            self.stats['avg_cl_f'].append(sum(f)/len(f))
        if len(b)>0:
            self.stats['min_cl_b'].append(min(b))
            self.stats['avg_cl_b'].append(sum(b)/len(b))
        if len(m)>0:
            self.stats['min_cl_m'].append(min(m))
            self.stats['avg_cl_m'].append(sum(m)/len(m))

    def loadClearances(self, groundPlan):
        self.resetClearanceInfo()
        for residence in groundPlan.getResidences():
            minDist = groundPlan.getMinimumDistance(residence)
            if(residence.getType() == "FamilyHome"):
                self.clearanceFamDict[residence] = minDist
                self.clearanceFam.append(minDist)
            elif(residence.getType() == "Bungalow"):
                self.clearanceBunDict[residence] = minDist
                self.clearanceBun.append(minDist)
            else:
                self.clearanceManDict[residence] = minDist
                self.clearanceMan.append(minDist)
    
    def resetClearanceInfo(self):
        self.clearanceFamDict = {}
        self.clearanceBunDict = {}
        self.clearanceManDict = {}
        self.clearanceFam = []
        self.clearanceBun = []
        self.clearanceMan = []
    

    #################################################
    #               COMPUTE USED AREA               #
    #################################################  

    def computeUsedArea(self, groundPlan):
        total = 0
        usedArea = 0
        for i in range(0, int(groundPlan.getWidth()/2)):
            for j in range(0, int(groundPlan.getHeight()/2)):
                total += 1
                if (not self.checkIfPointIsInFreeArea(groundPlan, i*2,j*2)):
                    usedArea += 1
        return (float(usedArea) / total) * 100
        
    def checkIfPointIsInFreeArea(self, groundPlan, i, j):
        point = self.makePoint(i,j)
        if(not self.checkIfPointIsNotInWater(groundPlan, point)):
            return False
        if(not self.checkIfPointIsNotInPlayground(groundPlan, point)):
            return False
        if(not self.checkIfPointIsNotInResidenceOrClearance(groundPlan, point)):
            return False
        return True
        
    def makePoint(self, i, j):
        tmpHome = FamilyHome(i,j)
        tmpHome.height = 0
        tmpHome.width = 0
        return tmpHome        
     
    def checkIfPointIsNotInWater(self, groundPlan, point):
        for waterbody in groundPlan.getWaterbodies():
            if (groundPlan.getDistance(point, waterbody) == 0):
                return False
        return True
        
    def checkIfPointIsNotInPlayground(self, groundPlan, point):
        for playground in groundPlan.getPlaygrounds():
            if (groundPlan.getDistance(point, playground) == 0):
                return False
        return True
      
    def checkIfPointIsNotInResidenceOrClearance(self, groundPlan, point):
        for residence in groundPlan.getResidences():
            res = groundPlan.getDistance(residence, point)
            if (res < residence.getminimumClearance()):
                return False
            if(residence.getType() == "FamilyHome" and res < max(self.clearanceFam)):
                minimumClearance = self.clearanceFamDict[residence]
                if (res < minimumClearance):
                    return False
            elif(residence.getType() == "Bungalow" and res < max(self.clearanceBun)):
                minimumClearance = self.clearanceBunDict[residence]
                if (res < minimumClearance):
                    return False
            elif(residence.getType() == "Mansion" and res < max(self.clearanceMan)):
                minimumClearance = self.clearanceManDict[residence]
                if (res < minimumClearance):
                    return False
        return True
     
    #################################################
    #               PRINT RESULTS                   #
    #################################################  
    
    def printResults(self, groundPlan):
        if(self.printStatistics):
            self.printStats(groundPlan)
            
        if(self.printClearances):
            self.printClearance(groundPlan)
        
        if(self.printPlan):
            self.printGroundPlan(groundPlan)
            
    def printStats(self, groundPlan):
        print("print stats")
        for key, value in sorted(self.stats.items(), key = lambda x: x[0]):
            if (len(value) > 0):
                print(key, "=", sum(value)/len(value))
                print(key+"_std", "=", numpy.std(value))
        
    def printGroundPlan(self, groundPlan):
        frame = GroundplanFrame(groundPlan)
        frame.setPlan()
        frame.root.mainloop()
        
    def printClearance(self, groundPlan):
        print("FamilyHomes: ", self.clearanceFam)
        print("Bungalows: ", self.clearanceBun)
        print("Mansions: ", self.clearanceMan)
        print("Value: ", groundPlan.getPlanValue())
        print()


    #################################################
    #               MAIN LOOP                       #
    #################################################  


normal = True
if normal:
    DistrictPlanner(0,-1,100,2,True,False,False,10)
else:
    runtimes = 10
    xyValues = []
    planValues = []
    for i in range(runtimes):
        x = random()*200
        y = random()*170
        plan = DistrictPlanner(x,y,False)
        xyValues.append([plan.x,plan.y])
        print(i + 1,plan.value)
        print()
        planValues.append(plan.value)
    xy = xyValues[planValues.index(max(planValues))]
    print(xy)
    DistrictPlanner(xy[0],xy[1], 40, 1, True, True, True)