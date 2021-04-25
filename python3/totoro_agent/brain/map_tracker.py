"""
Used to track all information about the ores (their HP, etc)
"""
from abc import abstractmethod
from ..utils.constants import ENTITIES
from ..utils import util_functions

from collections import defaultdict 
    
# adjacent list in this scenerio
class Graph: 
	
    def __init__(self,vertices): 
        self.V= vertices #No. of vertices in the graph
        self.graph = defaultdict(list) # default dictionary to store graph 
        self.Time = 0

    def new_method(self):
        children = 0
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
        self.graph[v].append(u) 
   
    def Articulation_Points_Util(self,u, visited, ap, parent, low, disc): 
        #Count of children in current node  
        self.new_method()
        visited[u]= True
        disc[u] = self.Time 
        low[u] = self.Time 
        self.Time += 1
  
        for v in self.graph[u]: 
            if visited[v] == False : 
                parent[v] = u 
                children += 1
                self.Articulation_Points_Util(v, visited, ap, parent, low, disc) 

                low[u] = min(low[u], low[v]) 

                if parent[u] == -1 and children > 1: 
                    ap[u] = True
  
                if parent[u] != -1 and low[v] >= disc[u]: 
                    ap[u] = True    
                      
                # Update low value of u for parent function calls     
            elif v != parent[u]:  
                low[u] = min(low[u], disc[v]) 

  
    #The function to do DFS traversal using Articulation_Points_Util()
    def Articulation_Points(self): 

        visited = [False] * (self.V) 
        disc = [float("Inf")] * (self.V) 
        low = [float("Inf")] * (self.V) 
        parent = [-1] * (self.V) 
        ap = [False] * (self.V) #To store articulation points 
  
        for i in range(self.V): 
            if visited[i] == False: 
				# recursive function to traverse all the leef nodes to find the node that has more than 1 edge
                self.Articulation_Points_Util(i, visited, ap, parent, low, disc)
  
        for index, value in enumerate (ap): 
            if value == True: print(index), 
		
class MapTracker:

	
	# Convert list into graph
	def get_surrounding_empty_tiles(position , world, entities):
		# do something here
		return 0
		
		
	def get_articulation_points(current_position, game_state):

		position = current_position
		world = game_state['world']
		entities = game_state['entities']	

		# get the graph
		# working on recursive function to retrieve all †he possible walkable tiles
		empty_tiles_graph = util_functions.get_surrounding_empty_tiles(position , world, entities)
		
		# find articulation points from graph
		#Graph.Articulation_Points()
	
		# return array of (x,y) tuples
		
		return 0
	

	def update(self, game_state):
		blast_blocks = []
		ore_blocks = []
		wood_blocks = []
		metal_blocks = []

		for entity in game_state.get("entities"):
			if entity.get("type") == ENTITIES.get("blast"):
				blast_blocks.append(entity)
			elif entity.get("type") == ENTITIES.get("ore"):
				ore_blocks.append(entity)
			elif entity.get("type") == ENTITIES.get("wood"):
				wood_blocks.append(entity)
			elif entity.get("type") == ENTITIES.get("metal"):
				metal_blocks.append(entity)

		game_state["blast_blocks"] = blast_blocks
		game_state["ore_blocks"] = ore_blocks
		game_state["wood_blocks"] = wood_blocks
		game_state["metal_blocks"] = metal_blocks

		# TODO me and tony
		# pinch points of map - floyd warshall (research)
