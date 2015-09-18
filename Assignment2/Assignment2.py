#Assignment 2 Patrick Andresen paan2097

import math
from sys import argv
script, world, Heuristic = argv

class Node():

	def __init__ (self):
		self.location=[]
		self.distToStart=None
		self.heurDistance=None
		self.f=None
		self.parent=None
		
	def heuristic(self,heuristic,x_final,y_final):
		x_now=self.location[0]
		y_now=self.location[1]
		
		if (heuristic == "euclidian"):
			return (10 * math.sqrt(((x_final-x_now)**2)+((y_final-y_now)**2)))
			#distance using pythagorean theorem
			
		elif (heuristic == "manhattan"):
			return (10*(abs(x_final-x_now)+abs(y_final-y_now)))
			#straight line distance
						
		else:
			print("Invalid Heuristic")
		
	def getAdj(self,heur,matrix,visited,passed):
		x_val=self.location[0]
		y_val=self.location[1]
		x_grid=len(matrix)
		y_grid=len(matrix[:][1])
		adj_nodes=[]
		
		for i in range(-1,2): #checks adj nodes in i
			
			if(0<=(x_val+i)<x_grid):	
				
				for j in range(-1,2): #checks adj nodes in j
					
					if(0<=(y_val+j)<y_grid):
						temp=matrix[x_val+i][y_val+j]
						maze=[]
						exists=False
						opened=False
						maze.append(x_val+i) #adds i to maze
						maze.append(y_val+j) #adds j to maze
						
						for nodes in visited:
							
							if maze[0]==nodes[0] and maze[1]==nodes[1]:
								exists=True
								
						for nodes in passed:
							
							if maze[0]==nodes.location[0] and maze[1]==nodes.location[1]:
								opened=True
								
						if((exists==False) and (temp != "2")):
							node=Node()
							node.location.append(x_val+i)
							node.location.append(y_val+j)
							node.heurDistance=node.heuristic(heur,x_grid,0)
							node.parent=self
							
							if((abs(i)+abs(j))<2):
								
								if(temp=="1"):
									node.distToStart=20+self.distToStart #mountain sqaure
									
								else:
									node.distToStart=10+self.distToStart #horizontal/vertical regular square
									
							else:
								if(temp=="1"):
									node.distToStart=24 + self.distToStart #diagonal into mountain square
									
								else:
									node.distToStart=14 + self.distToStart #diagonal into regular square 
							node.f=(node.heurDistance + node.distToStart)
							
							if(node.location != self.location and opened==False):
								adj_nodes.append(node)
								
		return adj_nodes

def getPath(world, Heuristic):
	num=1
	matrix=[[0 for i in range(10)] for j in range(8)]
	col=0
	row=0
	
	with open (world, 'r') as data:
		
		for line in data:
			line=line.strip()
			items=line.split(" ") #read in data from worldtxt
			col=0
			
			for item in items:
				
				if col <=9 and row<=7:
					matrix[row][col]=item  #creates matrix from data
					col=col + 1
					
			row = row+1
			
	y_dest=row
	x_dest=0
	visited_node=[]
	open_node=[]
	node=Node()
	node.location.append(7)
	node.location.append(0)
	node.heurDistance=node.heuristic(Heuristic,row,0)
	node.distToStart=0
	node.f=node.heurDistance
	node.parent=None
	open_node.append(node)
	final_dist=0
	good_path=[]
	goal=False
	
	while(len(open_node)!=0) and goal==False:
		near_node=None
		
		for nodes in open_node:
			
			if near_node == None:
				near_node= nodes
				
			else:
				if(near_node.f > nodes.f):  #picks node with lowest f
					near_node=nodes	
					
		adj=near_node.getAdj(Heuristic,matrix, visited_node,open_node)
		num=num+1
		visited_node.append(near_node.location)
		open_node.remove(near_node)
		
		for nodes in adj:
			
			if nodes.location[0] == x_dest and nodes.location[1]==y_dest:
				final_dist=nodes.distToStart
				
				while(nodes.parent != None):
					good_path.append(nodes.location)
					nodes=nodes.parent   #sets parent node 
					
				good_path.append(nodes.location)
				goal=True
				
			else:
				open_node.append(nodes)
				
	good_pathinOrder=good_path.reverse
	print("The total distance is",final_dist,"for the path:",good_path[::-1],"and visits", num, "locations")
	return
getPath(world,Heuristic)
