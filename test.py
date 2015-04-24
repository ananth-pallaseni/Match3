# Test

import tkinter as tk
import sys
import random
import math
import os
from custom_canvas import CustomCanvas

# ALL GEMS ARE 3000x3000
GEM_SIDE = 3000
GEM_DIR = "gems"

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
		return ((posX - self.radius) / self.boxWidth, (posY - self.radius) / self.boxHeight)

	def circle(self, posX, posY, color):
		return self.drawCircle(posX, posY, self.radius, lineColor='White', lineWidth=1, filled=1, fillColor=color, tag=color)

	def bind(self, item, func):
		self.canvas.tag_bind(item, '<ButtonPress-1>', func)

	def move(self, m):
		pos = self.indexToPos(m.final[0], m.final[1])
		self.canvas.coords(m.item, pos[0] - self.radius, pos[1] - self.radius, pos[0] + self.radius, pos[1] + self.radius)

	def createGems(self):
		gems = {}
		for gem_name in os.listdir(GEM_DIR):
			color = gem_name[4:len(gem_name)-4].upper()
			path = GEM_DIR + "/" + gem_name
			p = tk.PhotoImage(file=path)
			scale = int(GEM_SIDE // (self.boxWidth - 2))	
			print(scale)
			gems[color] = p.subsample(scale, scale)
		return gems


	def gem(self, indexX, indexY, color):
		pos = self.indexToPos(indexX, indexY)
		return self.canvas.create_image(pos[0], pos[1], image=self.gems[color.upper()])


if __name__ == '__main__':
	c = MatchCanvas(None, 400, 400, 10, 10)
	c.gem(4, 4, "blue")



