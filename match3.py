""" Match 3"""

import tkinter as tk
import sys
import random
import math
import os
from collections import deque
from custom_canvas import CustomCanvas

TYPES = ["RED", "BLUE", "GREEN", "PURPLE"]
GEM_SIDE = 3000
GEM_DIR = "gems"
WIDTH = 400
HEIGHT = 400
BOXES_PER_SIDE = 10

FRAMES_PER_SECOND = 30
MILLISECONDS_PER_FRAME = 33

class MatchGame(object):
	"""Object to handle game state and rules"""

	def __init__(self):
		self.canvas = MatchCanvas(self, WIDTH, HEIGHT, BOXES_PER_SIDE, BOXES_PER_SIDE)
		self.grid = [[-1 for i in range(BOXES_PER_SIDE)] for j in range(BOXES_PER_SIDE)]
		self.moveQueue = deque([])
		self.investigateQueue = deque([])
		self.deleteQueue = deque([])
		self.selected = None

		self.fillGridRandom()
		self.update()

	def colorOf(self, item):
		""" Returns the color of the specified item """
		return self.canvas.canvas.gettags(item)[0]

	def posOf(self, item):
		""" Returns the canvas coordinates of the specified item """
		coords = self.canvas.canvas.coords(item)
		if len(coords) < 4:
			return coords
		return ((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)

	def indexOf(self, item):
		""" Returns the index of an item """
		pos = self.posOf(item)
		return self.canvas.posToIndex(int(pos[0]), int(pos[1]))

	def findCurrentItem(self):
		""" Returns the most recently clicked item """
		return self.canvas.canvas.find_withtag("current")[0]

	def bind(self, item, func):
		""" Binds func (which is a onclick function) to the specified item """
		self.canvas.bind(item, func)


	def swap(self, itemA, itemB):
		""" Swap the positions of two items. Adds two moves to the queue """
		self.moveQueue.append(Move(itemA, self.indexOf(itemA), self.indexOf(itemB)))
		self.moveQueue.append(Move(itemB, self.indexOf(itemB), self.indexOf(itemA)))

	def match(self, m):
		""" Processes Match objects. If m contains a match of 3 or more, add a series of delete-moves to the queue """

		# If m is not a match of 3 or more, do nothing
		if not m.isMatch():
			return

		# Create a delete-move for the center item
		#self.moveQueue.append(Move(self.grid[m.center[0]][m.center[1]], m.center, 0))
		self.highlight(m.center[0], m.center[1])

		# Move through all the indices in the UP direction:
		for x in range(1, m.up[1] - m.center[1] + 1):
			# Select the item x UP from center
			item = self.grid[m.center[0]][m.center[1] + x]

			# Create a delete-move for each such item:
			#self.moveQueue.append(Move(item, (m.center[0] , m.center[1] + x), 0))
			self.highlight(m.center[0] , m.center[1] + x)
		# Move through all the indices in the DOWN direction:
		for x in range(1, m.center[1] - m.down[1] + 1):
			# Select the item x DOWN from center
			item = self.grid[m.center[0]][m.center[1] - x]
			
			# Create a delete-move for each such item:
			#self.moveQueue.append(Move(item, (m.center[0], m.center[1] - x), 0))
			self.highlight(m.center[0], m.center[1] - x)
		# Move through all the indices in the RIGHT direction:
		for y in range(1, m.right[1] - m.center[0] + 1):
			# Select the item y RIGHT from center
			item = self.grid[m.center[0] + y][m.center[1]]
			
			# Create a delete-move for each such item:
			#self.moveQueue.append(Move(item, (m.center[0] + y, m.center[1]), 0))
			self.highlight(m.center[0] + y, m.center[1])
		# Move through all the indices in the LEFT direction:
		for y in range(1, m.center[0] - m.left[1] + 1):
			# Select the item y LEFT from center
			item = self.grid[m.center[0] - y][m.center[1]]
			
			# Create a delete-move for each such item:
			#self.moveQueue.append(Move(item, (m.center[0] - y, m.center[1]), 0))
			self.highlight(m.center[0] - y, m.center[1])
	def addItem(self, indexX, indexY, color):
		"""" Adds an item of the specified color at the specified index """
		pos = self.canvas.indexToPos(indexX, indexY)
		#self.grid[indexX][indexY] = self.canvas.circle(pos[0], pos[1], color) #Circles
		self.grid[indexX][indexY] = self.canvas.gem(pos[0], pos[1], color) # Gems
		self.bind(self.grid[indexX][indexY], self.canvas_onclick)

	def fillGridRandom(self):
		""" Fill the board with random gems """

		for i in range(BOXES_PER_SIDE):
			for j in range(BOXES_PER_SIDE):
				color = random.choice(TYPES)
				self.addItem(i, j, color)

	def findMatch(self, indexX, indexY, color):
		""" Searches around the specified index for chains of adjoining items with the same color.
			Returns a Match object """

		m = Match(indexX, indexY)
		c = color.upper()
		m.up = self.search(indexX, indexY, color, "UP")
		m.down = self.search(indexX, indexY, color, "DOWN")
		m.right = self.search(indexX, indexY, color, "RIGHT")
		m.left = self.search(indexX, indexY, color, "LEFT")
		return m

	def search(self, indexX, indexY, color, direction):
		""" Searches for items of the same color in a specified direction, starting from indexX, indexY. 
			Returns an index-tuple of the furthest object of the same color"""

		c = color.upper()
		i = 0
		j = 0
		print(direction)
		print(indexX, indexY)

		if direction == "UP" and indexY >= 0 and indexY < BOXES_PER_SIDE:
			j = 1
		elif direction == "DOWN" and indexY >= 0 and indexY < BOXES_PER_SIDE:
			j = -1
		elif direction == "RIGHT" and indexX >= 0 and indexX < BOXES_PER_SIDE:
			i = 1
		elif direction == "LEFT" and indexX >= 0 and indexX < BOXES_PER_SIDE:
			i = -1
		else:
			return 0

		if indexX == BOXES_PER_SIDE - 1 or indexY == BOXES_PER_SIDE - 1:
			pass
		elif self.colorOf(self.grid[indexX + i][indexY + j]) == c:
			result = self.search(indexX + i, indexY + j, color, direction)
			if result:
				return result
		
		return (indexX, indexY)


	def highlight(self, indexX, indexY):
		p = self.canvas.indexToPos(indexX, indexY)
		return self.canvas.highlight(p[0], p[1])

	def removeHighlight(self, h):
		self.canvas.removeHighlight(h)

	def canvas_onclick(self, event):
		""" Called whenever a click is made. Updates what has been clicked and calls appropriate functions to move objects"""
		if self.selected:
			newItem = self.findCurrentItem()
			firstIndex = self.indexOf(self.selected)
			secondIndex = self.indexOf(newItem)
			diff = (secondIndex[0] - firstIndex[0], secondIndex[1] - firstIndex[1])
			if diff[0] == 0 and abs(diff[1]) == 1:
				self.swap(self.selected, newItem)
				
			elif diff[1] == 0 and abs(diff[0]) == 1:
				self.swap(self.selected, newItem)

			else:
				print("NO HA")
				# do nothing
				pass

			self.selected = None
		else:
			self.selected = self.findCurrentItem()


	def update(self):
		""" Update function to be called at a reguar interval to update screen state. """
		# Check if the queue is empty
		if len(self.moveQueue) > 0:
			# Pop the first element of the queue
			move = self.moveQueue.popleft()

			# Perform the move 
			self.canvas.move(move)

			# If the move is a swap:
			if move.final:
				# Check if there exists a match starting from the moved item, returns a match object
				m = self.findMatch(move.final[0], move.final[1], self.colorOf(move.item))

				# Process the match object (may or may not add delete-moves to the queue)
				self.match(m)

		# Call this function again after MILLISECONDS_PER_FRAME:
		self.canvas.tk.after(MILLISECONDS_PER_FRAME, self.update)



class Match(object):
	def __init__(self, centerX, centerY):
		self.center = (centerX, centerY)
		self.up = (centerX, centerY)	# Placeholders for future values
		self.right = (centerX, centerY)	# Placeholders for future values
		self.left = (centerX, centerY)	# Placeholders for future values
		self.down = (centerX, centerY)	# Placeholders for future values

	def isMatch(self):
		if abs(self.up[1] - self.down[1]) >= 2:
			return True
		if abs(self.left[0] - self.right[0]) >= 2:
			return True
		return False

	def __str__(self):
		print(self.up)
		print(self.down)
		print(self.left)
		print(self.right)
		return ""

	def __repr__(self):
		print(self.up)
		print(self.down)
		print(self.left)
		print(self.right)
		return ""
		
		
class Move(object):
	def __init__(self, item, originalIndex, finalIndex):
		self.item = item
		self.origin = originalIndex
		self.final = finalIndex

	def __str__(self):
		return str((self.item, self.origin, self.final))

	def __repr__(self):
		return str((self.item, self.origin, self.final))

class MatchCanvas(CustomCanvas):
	"""docstring for Canvas"""


	def __init__(self, parent, width, height, numCols, numRows):
		super(MatchCanvas, self).__init__(parent, width, height)

		# Attributes:
		self.numCols = numCols
		self.numRows = numRows
		self.boxWidth = self.width / self.numCols
		self.boxHeight = self.height / self.numRows
		self.radius = min(self.boxHeight, self.boxWidth) / 2
		self.grid = {}
		self.gems = self.createGems()

		# Set Up Grid:
		self.drawGrid()


	
	def drawGrid(self):
		posX = self.boxWidth
		posY = self.boxHeight
		for r in range(self.numRows):
			self.drawLine(0, posY, self.width, posY, lineColor="Black")
			posY += self.boxHeight
		for c in range(self.numCols):
			self.drawLine(posX, 0, posX, self.height, lineColor="Black")
			posX += self.boxWidth

	def indexToPos(self, indexX, indexY):
		return (indexX * self.boxWidth + self.radius, indexY * self.boxHeight + self.radius)

	def posToIndex(self, posX, posY):
		return (int((posX - self.radius) / self.boxWidth), int((posY - self.radius) / self.boxHeight))

	def circle(self, posX, posY, color, radius=0):
		if not radius:
			radius = self.radius
		return self.drawCircle(posX, posY, radius, lineColor='White', lineWidth=1, filled=1, fillColor=color, tag=color)

	def bind(self, item, func):
		self.canvas.tag_bind(item, '<ButtonPress-1>', func)

	def move(self, m):
		if m.final:
			print(m.final)
			pos = self.indexToPos(m.final[0], m.final[1])
			#self.canvas.coords(m.item, pos[0] - self.radius, pos[1] - self.radius, pos[0] + self.radius, pos[1] + self.radius)
			self.canvas.coords(m.item, pos[0], pos[1])
		else:
			print("REMOVING")
			self.remove(m.item)


	def remove(self, item):
		self.canvas.delete(item)

	def createGems(self):
		gems = {}
		for gem_name in os.listdir(GEM_DIR):
			color = gem_name[4:len(gem_name)-4].upper()
			path = GEM_DIR + "/" + gem_name
			p = tk.PhotoImage(file=path)
			scale = int(GEM_SIDE // (self.boxWidth - 2))	
			gems[color] = p.subsample(scale, scale)
		return gems


	def gem(self, posX, posY, color):
		return self.canvas.create_image(posX, posY, image=self.gems[color.upper()], tag=color.upper())

	def highlight(self, posX, posY, color="BLACK"):
		h1 = self.circle(posX - self.radius, posY - self.radius, color, radius=int(self.radius/4))
		h2 = self.circle(posX - self.radius, posY + self.radius, color, radius=int(self.radius/4))
		h3 = self.circle(posX + self.radius, posY - self.radius, color, radius=int(self.radius/4))
		h4 = self.circle(posX + self.radius, posY + self.radius, color, radius=int(self.radius/4))
		return [h1, h2, h3, h4]

	def removeHighlight(self, h):
		for item in h:
			self.canvas.delete(item)


if __name__ == '__main__':
	c = MatchGame();


