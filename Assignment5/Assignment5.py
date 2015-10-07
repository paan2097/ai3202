#Patrick Andresen paan2097 Assignment 5 October 7, 2015
#References: Stackoverflow.com & github.com

from sys import argv
import math
script, world, E = argv

class Node():

	def __init__ (self):
		
		self.Type=None
		self.parent=None
		self.reward=0.0
		self.utility=0.0
		self.delta=100
		self.x_val=0
		self.y_val=0
		
def getUtility(matrix,i,j):
	
	maze=[]
	x_grid=len(matrix)
	y_grid=len(matrix[:][1])
	maze.append("("+str(i)+","+str(j)+")"+", "+str(matrix[i][j].utility))
	
	while(matrix[i][j].reward != 50):
		
		if(j+1 < y_grid and matrix[i][j+1].Type != '2'):  #calculates moving up one, not a wall
			util_1=matrix[i][j+1].utility
			
		else:
			util_1=-100000000
			
		if(j-1 >=0 and matrix[i][j-1].Type != '2'): #calculates moving down one, not a wall
			util_2=matrix[i][j-1].utility
			
		else:
			util_2=-100000000
			
		if(i+1 < x_grid and matrix[i+1][j].Type != '2'): #calculates moving right one, not a wall
			util_3=matrix[i+1][j].utility
			
		else:
			util_3=-100000000
			
		if(i-1 >=0 and matrix[i-1][j].Type != '2'): #calculates moving left one, not a wall
			util_4=matrix[i-1][j].utility
			
		else:
			util_4=-100000000
			
		large_util=max(util_1,util_2,util_3,util_4) #takes the best utility 
		
		if large_util == util_1:
			maze.append("("+str(i)+","+str(j+1)+"), "+str(matrix[i][j+1].utility)) #chooses move up
			matrix[i][j+1].parent=matrix[i][j]
			j=j+1
			
		elif large_util == util_2:
			maze.append("("+str(i)+","+str(j-1)+"), "+str(matrix[i][j-1].utility)) #chooses move down
			matrix[i][j-1].parent=matrix[i][j]
			j=j-1
			
		elif large_util == util_3:
			maze.append("("+str(i+1)+","+str(j)+"), "+str(matrix[i+1][j].utility)) #chooses move right
			matrix[i+1][j].parent=matrix[i][j]
			i = i + 1
			
		else:
			maze.append("("+str(i-1)+","+str(j)+"), "+str(matrix[i-1][j].utility)) #chooses move left
			matrix[i-1][j].parent=matrix[i][j]
			i = i - 1
			
	return maze
		
def markovDecision(matrix,err):
	
	x_grid=len(matrix)
	y_grid=len(matrix[:][1])
	delta_max=100
	
	while delta_max > err:
		
		delta_max=0
		
		for i in range(0,x_grid):			
			for j in range(y_grid-1,-1,-1):
				util_curr=matrix[i][j].utility
				
				if matrix[i][j].reward==50: #Made it to the apple
					matrix[i][j].utility=50
					matrix[i][j].delta=0
					
				else:
					util_1=0
					util_2=0
					util_3=0
					util_4=0
					
					if(j+1 < y_grid and matrix[i][j+1].Type != '2'):
						util_1=util_1 + 0.8*matrix[i][j+1].utility    #moves in intended direction
						util_3=util_3 + 0.1*matrix[i][j+1].utility
						util_4=util_4 + 0.1*matrix[i][j+1].utility	#moves in incorrect direction
						
					else:
						util_1=util_1 - 100000
						
						if(i+1 < x_grid and matrix[i+1][j].Type != '2'):
							util_3=util_3 + 0.1*matrix[i+1][j].utility     #unintended direction
							
						if(i-1 < x_grid and matrix[i-1][j].Type != '2'):
							util_4=util_4 + 0.1*matrix[i-1][j].utility     #unintended direction
							
					if(j-1 >=0 and matrix[i][j-1].Type != '2'):
						util_2=util_2 + 0.8*matrix[i][j-1].utility
						util_3=util_3 + 0.1*matrix[i][j-1].utility         #calcuates 3 moves
						util_4=util_4 + 0.1*matrix[i][j-1].utility
						
					else:
						util_2=util_2 - 100000
						
						if(i+1 < x_grid and matrix[i+1][j].Type != '2'):
							util_3=util_3 + 0.1*matrix[i+1][j].utility
							
						if(i-1 < x_grid and matrix[i-1][j].Type != '2'):
							util_4=util_4 + 0.1*matrix[i-1][j].utility
							
					if(i+1 < x_grid and matrix[i+1][j].Type != '2'):
						util_3=util_3 + 0.8*matrix[i+1][j].utility
						util_1=util_1 + 0.1*matrix[i+1][j].utility    #3 moves
						util_2=util_2 + 0.1*matrix[i+1][j].utility
						
					else:
						util_3=util_3 - 100000
						
						if(j+1 < y_grid and matrix[i][j+1].Type != '2'):
							util_1=util_1 + 0.1*matrix[i][j+1].utility
							
						if(j-1 < y_grid and matrix[i][j-1].Type != '2'):
							util_2=util_2 + 0.1*matrix[i][j-1].utility
							
					if(i-1 >=0 and matrix[i-1][j].Type != '2'):
						util_4=util_4 + 0.8*matrix[i-1][j].utility
						util_1=util_1 + 0.1*matrix[i-1][j].utility
						util_2=util_2 + 0.1*matrix[i-1][j].utility
						
					else:
						util_4=util_4 - 100000
						
						if(j+1 < y_grid and matrix[i][j+1].Type != '2'):
							util_1=util_1 + 0.1*matrix[i][j+1].utility
							
						if(j-1 < y_grid and matrix[i][j-1].Type != '2'):
							util_2=util_2 + 0.1*matrix[i][j-1].utility
							
					matrix[i][j].utility=(matrix[i][j]).reward + 0.9*max(util_1,util_2,util_3,util_4)
					util_new=(matrix[i][j]).utility
					
					if(abs(util_new - util_curr) < matrix[i][j].delta):
						matrix[i][j].delta = abs(util_new - util_curr)
						
					if matrix[i][j].delta > delta_max:
						delta_max=matrix[i][j].delta
	
def getMaze(world,E):
	
	matrix=[[0 for i in range(10)] for j in range(8)]
	row=0
	column=0
	
	with open (world, 'r') as data:        #read in text file/matrix
		for line in data:
			line=line.strip()
			items=line.split(" ")
			column=0
			
			for item in items:
				if column <=9 and row<=7:
					node = Node()			#set each item in matrix as a node
					node.Type=item
					
					if item == '0':
						node.reward=0
						
					elif item == '1':
						node.reward = (-1)
						
					elif item == '2':
						node.reward=-100000000
						
					elif item == '3':
						node.reward = (-2)
						
					elif item == '4':
						node.reward = 1
						
					elif item == '50':
						node.reward = 50
						
					node.x_val = column
					node.y_val = row
					matrix[row][column]=node
					column=column + 1
					
			row = row+1
			
	markovDecision(matrix,(float(E)/9))
	good_path=getUtility(matrix,7,0)
	
	print("The path found is shown as (location),utility " +str(good_path))

if __name__ == '__main__':
	getMaze(world,E)
