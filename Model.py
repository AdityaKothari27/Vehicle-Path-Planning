from math import *
from random import randint

class World:

	def __init__(self, width, scoutAntsNumber, workerAntsNumber, decreaseRate): 	
		self.pheromones = [[0 for i in range(width)] for j in range(width)] 	
		self.width = width 	

		self.decreaseRate = decreaseRate 		

		self.workerAntsNumber = workerAntsNumber
		self.scoutAntsNumber = scoutAntsNumber 	

		self.anthill = [0, 0]
		self.food = [0, 0] 	
		

		self.broughtFood = 0 			

		self.letGoWorkerAnts = False 	

		self.pathFound = False 			
		self.lastFoundPath = [] 		
		self.commonPathsNumber = 0 		

		while (abs(self.anthill[0] - self.food[0]) + (abs(self.anthill[1] - self.food[1]))) < self.width:

			
			self.anthill = (randint(0, self.width-1), randint(0, self.width-1))
			self.food = (randint(0, self.width-1), randint(0, self.width-1))

		self.ants = [] 	

		
		for i in range(self.workerAntsNumber):
			newAnt = Ant(1, self.anthill)
			self.ants.append(newAnt)

		for i in range(self.scoutAntsNumber):
			newAnt = Ant(0, self.anthill)
			self.ants.append(newAnt)

	def realOptimalDistance(self):
		lengthRealOptimalDistance = 0 						
		position = [self.food[0], self.food[1]] 			
		finalPosition = [self.anthill[0], self.anthill[1]] 	

		
		
		
		while position != finalPosition:

			if position[0] != finalPosition[0]:
				if position[0] < finalPosition[0]:
					position[0] = position[0] + 1
				else:
					position[0] = position[0] - 1

			if position[1] != finalPosition[1]:
				if position[1] < finalPosition[1]:
					position[1] = position[1] + 1
				else:
					position[1] = position[1] - 1

			lengthRealOptimalDistance = lengthRealOptimalDistance + 1

		return lengthRealOptimalDistance

	def returningAntsNumberPerCell(self):

		antsNumber = [[0 for i in range(self.width)] for j in range(self.width)] 								

		for i in range(len(self.ants)): 																		
			if self.ants[i].returning: 																			
				antsNumber[self.ants[i].X][self.ants[i].Y] = antsNumber[self.ants[i].X][self.ants[i].Y] + 1 	

		return antsNumber

	def antsNumberPerCell(self):

		antsNumber = [[0 for i in range(self.width)] for j in range(self.width)] 							

		for i in range(len(self.ants)): 																	
			antsNumber[self.ants[i].X][self.ants[i].Y] = antsNumber[self.ants[i].X][self.ants[i].Y] + 1 	

		return antsNumber

	def listAuthorizedCellsAround(self, ant):
		
		Ax = ant.X 	
		Ay = ant.Y

		returning = ant.returning 	

		cellsList = [] 	

		for i in range(-1, 2): 						
			newX = Ax + i 							
			if newX >= 0 and newX < self.width: 	
				for j in range(-1, 2): 				
					newY = Ay + j
					if newY >= 0 and newY < self.width:
						if i != 0 or j != 0: 		
							if (not returning and not (newX == self.anthill[0] and newY == self.anthill[1])) or (returning and not (newX == self.food[0] and newY == self.food[1])):
								
								if not ([newX, newY] in ant.visitedCells): 	
									cellsList.append([newX, newY]) 			

		return cellsList


	def chooseInterestingCellAround(self, antNumber):

		ant = self.ants[antNumber] 	

		decision = None 	
		pheromoneSum = 0 	

		possibleDecisions = self.listAuthorizedCellsAround(ant) 		
		if len(possibleDecisions) == 0: 								
			self.ants[antNumber].visitedCells = [] 						
			possibleDecisions = self.listAuthorizedCellsAround(ant) 	

		for i in range(len(possibleDecisions)): 	
			X = possibleDecisions[i][0] 	
			Y = possibleDecisions[i][1]
			if (X == self.anthill[0] and Y == self.anthill[1] and ant.returning) or (X == self.food[0] and Y == self.food[1] and not ant.returning):
			
			
			
				decision = [X, Y] 	
				break 				
			else: 														
				pheromoneSum = pheromoneSum + self.pheromones[X][Y] 	

		if decision != None: 	
			return decision 	

		probabilitiesList = [None for i in range(len(possibleDecisions))] 
		if pheromoneSum == 0: 	
			decisionNumber = randint(0, len(possibleDecisions)-1) 	
			decision = possibleDecisions[decisionNumber] 			

		else: 	
			probability = 0 	
			choosenProbability = randint(0, 99) / 100 	
			for i in range(0, len(possibleDecisions)): 	
				X = possibleDecisions[i][0] 	
				Y = possibleDecisions[i][1]
				pheromones = self.pheromones[X][Y] 	
				probability += (pheromones/pheromoneSum) 	
				if probability > choosenProbability: 	
					decision = possibleDecisions[i] 	
					break 	
		return decision



	def moveAnts(self):

		for i in range(len(self.ants)): 	
			
			if self.ants[i].antType == 1: 	
				
				if self.letGoWorkerAnts: 	
					newPosition = self.chooseInterestingCellAround(i) 	
					
					self.ants[i].visitedCells.append([self.ants[i].X, self.ants[i].Y]) 	
					self.ants[i].X = newPosition[0] 	
					self.ants[i].Y = newPosition[1]

			
			elif self.ants[i].antType == 0 and not (self.ants[i].X == self.anthill[0] and self.ants[i].Y == self.anthill[1] and self.ants[i].returning == True):

				moveX = 0 	
				moveY = 0

				for j in range(-1, 2): 			
					newX = self.ants[i].X + j 	
					for k in range(-1, 2): 		
						newY = self.ants[i].Y + k
						if (self.ants[i].returning and newX == self.anthill[0] and newY == self.anthill[1]) or (not self.ants[i].returning and newX == self.food[0] and newY == self.food[1]):
						
						
							moveX = j
							moveY = k

				while (moveX == 0 and moveY == 0) or (self.ants[i].X + moveX) < 0 or (self.ants[i].Y + moveY) < 0 or (self.ants[i].X + moveX) >= self.width or (self.ants[i].Y + moveY) >= self.width:
				
				
				
					moveX = randint(-1, 1) 	
					moveY = randint(-1, 1)

				self.ants[i].visitedCells.append([self.ants[i].X, self.ants[i].Y]) 	
				self.ants[i].X = self.ants[i].X + moveX 	
				self.ants[i].Y = self.ants[i].Y + moveY

			self.changeAntState(i) 	

	def changeAntState(self, antNumber):

		if self.ants[antNumber].X == self.food[0] and self.ants[antNumber].Y == self.food[1]: 	
			self.ants[antNumber].returning = True 	
			self.ants[antNumber].visitedCells = [] 	

		elif self.ants[antNumber].X == self.anthill[0] and self.ants[antNumber].Y == self.anthill[1]: 	
			
			if self.ants[antNumber].returning: 	
				
				if self.ants[antNumber].antType == 0 and self.letGoWorkerAnts == False: 	
					self.letGoWorkerAnts = True 	
				
				elif self.ants[antNumber].antType == 1: 	
					
					self.broughtFood = self.broughtFood + 1 	
					
					if self.ants[antNumber].visitedCells == self.lastFoundPath: 	
						self.commonPathsNumber = self.commonPathsNumber + 1 	
					else: 	
						self.commonPathsNumber = 1 	
						self.lastFoundPath = self.ants[antNumber].visitedCells 	
				
				self.ants[antNumber].returning = False 	
				self.ants[antNumber].visitedCells = [] 	

	def leaveAllPheromones3(self):
		

		antsNumber = self.returningAntsNumberPerCell() 	

		for i in range(self.width): 	
			for j in range(self.width): 	
				
				
				
				
				
				self.pheromones[i][j] = ((1-self.decreaseRate)*self.pheromones[i][j]) + antsNumber[i][j]**(self.width)

	def leaveAllPheromones4(self):

		addedPheromones = [[0 for i in range(self.width)] for j in range(self.width)]

		for i in range(len(self.ants)):
			
			if 1:
				addedPheromones[self.ants[i].X][self.ants[i].Y] = addedPheromones[self.ants[i].X][self.ants[i].Y] + (1/(len(self.ants[i].visitedCells)+1))**(self.width)

		for i in range(self.width):
			for j in range(self.width):
				self.pheromones[i][j] = ((1-self.decreaseRate)*self.pheromones[i][j]) + addedPheromones[i][j]**(self.width)


	def checkConvergence(self):
		
		if self.commonPathsNumber > self.workerAntsNumber/4: 	
			self.pathFound = True

	def loop(self):
		
		self.moveAnts()
		self.leaveAllPheromones3()
		self.checkConvergence()


class Ant:

	def __init__(self, antType, anthillCoordinates):
		self.antType = antType

		if self.antType == 0:
			self.antName = "Scout"
		elif self.antType == 1:
			self.antName = "Worker"

		self.X = anthillCoordinates[0]
		self.Y = anthillCoordinates[1]

		self.returning = False 	

		self.visitedCells = [] 	
