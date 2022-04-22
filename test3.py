#!/usr/bin/env python

"""
This Python code is based on Java code by Lee Jacobson found in an article
entitled "Applying a genetic algorithm to the travelling salesman problem"
that can be found at: http://goo.gl/cJEY1
"""

# 시작점 고정하기,
    # 지금 값이 optimal하지 않은데.... \
    # 이유가 시작점 고정이 안되어서 그런걸까?
# 출력은 좌표 + city 번호도 같이 출력하기....
# 이동한대로 그래프로 출력하기.


import math
import random


class City:
   def __init__(self, x=None, y=None):
      self.x = None
      self.y = None
      if x is not None:
         self.x = x
      else:
         self.x = int(random.random() * 200)
      if y is not None:
         self.y = y
      else:
         self.y = int(random.random() * 200)
   
   def getX(self):
      return self.x
   
   def getY(self):
      return self.y
   
   def distanceTo(self, city):
      xDistance = abs(self.getX() - city.getX())
      yDistance = abs(self.getY() - city.getY())
      distance = math.sqrt( (xDistance*xDistance) + (yDistance*yDistance) )
      return distance
   
   def __repr__(self):
      return str(self.getX()) + ", " + str(self.getY())


class TourManager:
   destinationCities = []
   
   def addCity(self, city):
      self.destinationCities.append(city)
   
   def getCity(self, index):
      return self.destinationCities[index]
   
   def numberOfCities(self):
      return len(self.destinationCities)


class Tour:
   def __init__(self, tourmanager, tour=None):
      self.tourmanager = tourmanager
      self.tour = []
      self.fitness = 0.0
      self.distance = 0
      if tour is not None:
         self.tour = tour
      else:
         for i in range(0, self.tourmanager.numberOfCities()):
            self.tour.append(None)
   
   def __len__(self):
      return len(self.tour)
   
   def __getitem__(self, index):
      return self.tour[index]
   
   def __setitem__(self, key, value):
      self.tour[key] = value
   
   def __repr__(self):
      geneString = "|"
      for i in range(0, self.tourSize()):
         geneString += str(self.getCity(i)) + "|"
      return geneString
   
   def generateIndividual(self):
      for cityIndex in range(0, self.tourmanager.numberOfCities()):
         self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
      random.shuffle(self.tour)
   
   def getCity(self, tourPosition):
      return self.tour[tourPosition]
   
   def setCity(self, tourPosition, city):
      self.tour[tourPosition] = city
      self.fitness = 0.0
      self.distance = 0
   
   def getFitness(self):
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance())
      return self.fitness
   
   def getDistance(self):
      if self.distance == 0:
         tourDistance = 0
         for cityIndex in range(0, self.tourSize()):
            fromCity = self.getCity(cityIndex)
            destinationCity = None
            if cityIndex+1 < self.tourSize():
               destinationCity = self.getCity(cityIndex+1)
            else:
               destinationCity = self.getCity(0)
            tourDistance += fromCity.distanceTo(destinationCity)
         self.distance = tourDistance
      return self.distance
   
   def tourSize(self):
      return len(self.tour)
   
   def containsCity(self, city):
      return city in self.tour


class Population:
   def __init__(self, tourmanager, populationSize, initialise):
      self.tours = []
      for i in range(0, populationSize):
         self.tours.append(None)
      
      if initialise:
         for i in range(0, populationSize):
            newTour = Tour(tourmanager)
            newTour.generateIndividual()
            self.saveTour(i, newTour)
      
   def __setitem__(self, key, value):
      self.tours[key] = value
   
   def __getitem__(self, index):
      return self.tours[index]
   
   def saveTour(self, index, tour):
      self.tours[index] = tour
   
   def getTour(self, index):
      return self.tours[index]
   
   def getFittest(self):
      fittest = self.tours[0]
      for i in range(0, self.populationSize()):
         if fittest.getFitness() <= self.getTour(i).getFitness():
            fittest = self.getTour(i)
      return fittest
   
   def populationSize(self):
      return len(self.tours)


class GA:
   def __init__(self, tourmanager):
      self.tourmanager = tourmanager
      self.mutationRate = 0.015
      self.tournamentSize = 5
      self.elitism = True
   
   def evolvePopulation(self, pop):
      newPopulation = Population(self.tourmanager, pop.populationSize(), False)
      elitismOffset = 0
      if self.elitism:
         newPopulation.saveTour(0, pop.getFittest())
         elitismOffset = 1
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         parent1 = self.tournamentSelection(pop)
         parent2 = self.tournamentSelection(pop)
         child = self.crossover(parent1, parent2)
         newPopulation.saveTour(i, child)
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         self.mutate(newPopulation.getTour(i))
      
      return newPopulation
   
   def crossover(self, parent1, parent2):
      child = Tour(self.tourmanager)
      
      startPos = int(random.random() * parent1.tourSize())
      endPos = int(random.random() * parent1.tourSize())
      
      for i in range(0, child.tourSize()):
         if startPos < endPos and i > startPos and i < endPos:
            child.setCity(i, parent1.getCity(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               child.setCity(i, parent1.getCity(i))
      
      for i in range(0, parent2.tourSize()):
         if not child.containsCity(parent2.getCity(i)):
            for ii in range(0, child.tourSize()):
               if child.getCity(ii) == None:
                  child.setCity(ii, parent2.getCity(i))
                  break
      
      return child
   
   def mutate(self, tour):
      for tourPos1 in range(0, tour.tourSize()):
         if random.random() < self.mutationRate:
            tourPos2 = int(tour.tourSize() * random.random())
            
            city1 = tour.getCity(tourPos1)
            city2 = tour.getCity(tourPos2)
            
            tour.setCity(tourPos2, city1)
            tour.setCity(tourPos1, city2)
   
   def tournamentSelection(self, pop):
      tournament = Population(self.tourmanager, self.tournamentSize, False)
      for i in range(0, self.tournamentSize):
         randomId = int(random.random() * pop.populationSize())
         tournament.saveTour(i, pop.getTour(randomId))
      fittest = tournament.getFittest()
      return fittest



if __name__ == '__main__':
   
   tourmanager = TourManager()
   
   # Create and add our cities
   city1 = City(0, 13)
   tourmanager.addCity(city1)
   city2 = City(0, 26)
   tourmanager.addCity(city2)
   city3 = City(0, 27)
   tourmanager.addCity(city3)
   city4 = City(0, 39)
   tourmanager.addCity(city4)
   city5 = City(2, 0)
   tourmanager.addCity(city5)
   city6 = City(5, 13)
   tourmanager.addCity(city6)
   city7 = City(5, 19)
   tourmanager.addCity(city7)
   city8 = City(5, 25)
   tourmanager.addCity(city8)
   city9 = City(5, 31)
   tourmanager.addCity(city9)
   city10 = City(5, 37)
   tourmanager.addCity(city10)
   city11 = City(5, 43)
   tourmanager.addCity(city11)
   city12 = City(5, 8)
   tourmanager.addCity(city12)
   city13 = City(8, 0)
   tourmanager.addCity(city13)
   city14 = City(9, 10)
   tourmanager.addCity(city14)
   city15 = City(10, 10)
   tourmanager.addCity(city15)
   city16 = City(11, 10)
   tourmanager.addCity(city16)
   city17 = City(12, 10)
   tourmanager.addCity(city17)
   city18 = City(12, 5)
   tourmanager.addCity(city18)
   city19 = City(15, 13)
   tourmanager.addCity(city19)
   city20 = City(15, 19)
   tourmanager.addCity(city20)
   city21 = City(15, 25)
   tourmanager.addCity(city21)
   city22 = City(15, 31)
   tourmanager.addCity(city22)
   city23 = City(15, 37)
   tourmanager.addCity(city23)
   city24 = City(15, 43)
   tourmanager.addCity(city24)
   city25 = City(15, 8)
   tourmanager.addCity(city25)
   city26 = City(18, 11)
   tourmanager.addCity(city26)
   city27 = City(18, 13)
   tourmanager.addCity(city27)
   city28 = City(18, 15)
   tourmanager.addCity(city28)
   city29 = City(18, 17)
   tourmanager.addCity(city29)
   city30 = City(18, 19)
   tourmanager.addCity(city30)
   city31 = City(18, 21)
   tourmanager.addCity(city31)
   city32 = City(18, 23)
   tourmanager.addCity(city32)
   city33 = City(18, 25)
   tourmanager.addCity(city33)
   city34 = City(18, 27)
   tourmanager.addCity(city34)
   city35 = City(18, 29)
   tourmanager.addCity(city35)
   city36 = City(18, 31)
   tourmanager.addCity(city36)
   city37 = City(18, 33)
   tourmanager.addCity(city37)
   city38 = City(18, 35)
   tourmanager.addCity(city38)
   city39 = City(18, 37)
   tourmanager.addCity(city39)
   city40 = City(18, 39)
   tourmanager.addCity(city40)
   city41 = City(18, 41)
   tourmanager.addCity(city41)
   city42 = City(18, 42)
   tourmanager.addCity(city42)
   city43 = City(18, 44)
   tourmanager.addCity(city43)
   city44 = City(18, 45)
   tourmanager.addCity(city44)
   city45 = City(25, 11)
   tourmanager.addCity(city45)
   city46 = City(25, 15)
   tourmanager.addCity(city46)
   city47 = City(25, 22)
   tourmanager.addCity(city47)
   city48 = City(25, 23)
   tourmanager.addCity(city48)
   city49 = City(25, 24)
   tourmanager.addCity(city49)
   city50 = City(25, 26)
   tourmanager.addCity(city50)
   city51 = City(25, 28)
   tourmanager.addCity(city51)
   city52 = City(25, 29)
   tourmanager.addCity(city52)
   city53 = City(25, 9)
   tourmanager.addCity(city53)
   city54 = City(28, 16)
   tourmanager.addCity(city54)
   city55 = City(28, 20)
   tourmanager.addCity(city55)
   city56 = City(28, 28)
   tourmanager.addCity(city56)
   city57 = City(28, 30)
   tourmanager.addCity(city57)
   city58 = City(28, 34)
   tourmanager.addCity(city58)
   city59 = City(28, 40)
   tourmanager.addCity(city59)
   city60 = City(28, 43)
   tourmanager.addCity(city60)
   city61 = City(28, 47)
   tourmanager.addCity(city61)
   city62 = City(32, 26)
   tourmanager.addCity(city62)
   city63 = City(32, 31)
   tourmanager.addCity(city63)
   city64 = City(33, 15)
   tourmanager.addCity(city64)
   city65 = City(33, 26)
   tourmanager.addCity(city65)
   city66 = City(33, 29)
   tourmanager.addCity(city66)
   city67 = City(33, 31)
   tourmanager.addCity(city67)
   city68 = City(34, 15)
   tourmanager.addCity(city68)
   city69 = City(34, 26)
   tourmanager.addCity(city69)
   city70 = City(34, 29)
   tourmanager.addCity(city70)
   city71 = City(34, 31)
   tourmanager.addCity(city71)
   city72 = City(34, 38)
   tourmanager.addCity(city72)
   city73 = City(34, 41)
   tourmanager.addCity(city73)
   city74 = City(34, 5)
   tourmanager.addCity(city74)
   city75 = City(35, 17)
   tourmanager.addCity(city75)
   city76 = City(35, 31)
   tourmanager.addCity(city76)
   city77 = City(38, 16)
   tourmanager.addCity(city77)
   city78 = City(38, 20)
   tourmanager.addCity(city78)
   city79 = City(38, 30)
   tourmanager.addCity(city79)
   city80 = City(38, 34)
   tourmanager.addCity(city80)
   city81 = City(40, 22)
   tourmanager.addCity(city81)
   city82 = City(41, 23)
   tourmanager.addCity(city82)
   city83 = City(41, 32)
   tourmanager.addCity(city83)
   city84 = City(41, 34)
   tourmanager.addCity(city84)
   city85 = City(41, 35)
   tourmanager.addCity(city85)
   city86 = City(41, 36)
   tourmanager.addCity(city86)
   city87 = City(48, 22)
   tourmanager.addCity(city87)
   city88 = City(48, 27)
   tourmanager.addCity(city88)
   city89 = City(48, 6)
   tourmanager.addCity(city89)
   city90 = City(51, 45)
   tourmanager.addCity(city90)
   city91 = City(51, 47)
   tourmanager.addCity(city91)
   city92 = City(56, 25)
   tourmanager.addCity(city92)
   city93 = City(57, 12)
   tourmanager.addCity(city93)
   city94 = City(57, 25)
   tourmanager.addCity(city94)
   city95 = City(57, 44)
   tourmanager.addCity(city95)
   city96 = City(61, 45)
   tourmanager.addCity(city96)
   city97 = City(61, 47)
   tourmanager.addCity(city97)
   city98 = City(63, 6)
   tourmanager.addCity(city98)
   city99 = City(64, 22)
   tourmanager.addCity(city99)
   city100 = City(71, 11)
   tourmanager.addCity(city100)
   city101 = City(71, 13)
   tourmanager.addCity(city101)
   city102 = City(71, 16)
   tourmanager.addCity(city102)
   city103 = City(71, 45)
   tourmanager.addCity(city103)
   city104 = City(71, 47)
   tourmanager.addCity(city104)
   city105 = City(74, 12)
   tourmanager.addCity(city105)
   city106 = City(74, 16)
   tourmanager.addCity(city106)
   city107 = City(74, 20)
   tourmanager.addCity(city107)
   city108 = City(74, 24)
   tourmanager.addCity(city108)
   city109 = City(74, 29)
   tourmanager.addCity(city109)
   city110 = City(74, 35)
   tourmanager.addCity(city110)
   city111 = City(74, 39)
   tourmanager.addCity(city111)
   city112 = City(74, 6)
   tourmanager.addCity(city112)
   city113 = City(77, 21)
   tourmanager.addCity(city113)
   city114 = City(78, 10)
   tourmanager.addCity(city114)
   city115 = City(78, 32)
   tourmanager.addCity(city115)
   city116 = City(78, 35)
   tourmanager.addCity(city116)
   city117 = City(78, 39)
   tourmanager.addCity(city117)
   city118 = City(79, 10)
   tourmanager.addCity(city118)
   city119 = City(79, 33)
   tourmanager.addCity(city119)
   city120 = City(79, 37)
   tourmanager.addCity(city120)
   city121 = City(80, 10)
   tourmanager.addCity(city121)
   city122 = City(80, 41)
   tourmanager.addCity(city122)
   city123 = City(80, 5)
   tourmanager.addCity(city123)
   city124 = City(81, 17)
   tourmanager.addCity(city124)
   city125 = City(84, 20)
   tourmanager.addCity(city125)
   city126 = City(84, 24)
   tourmanager.addCity(city126)
   city127 = City(84, 29)
   tourmanager.addCity(city127)
   city128 = City(84, 34)
   tourmanager.addCity(city128)
   city129 = City(84, 38)
   tourmanager.addCity(city129)
   city130 = City(84, 6)
   tourmanager.addCity(city130)
   city131 = City(107, 27)
   tourmanager.addCity(city131)

   # Initialize population
   pop = Population(tourmanager, 50, True);
   print ("Initial distance: " + str(pop.getFittest().getDistance()))
   
   # Evolve population for 50 generations
   ga = GA(tourmanager)
   pop = ga.evolvePopulation(pop)
   for i in range(0, 100):
      pop = ga.evolvePopulation(pop)
   
   # Print final results
   print ("Finished")
   print ("Final distance: " + str(pop.getFittest().getDistance()))
   print ("Solution:")
   print (pop.getFittest())
   