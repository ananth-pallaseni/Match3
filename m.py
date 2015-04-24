""" Match 3"""

import tkinter as tk
import sys
import random
import math
from custom_canvas import CustomCanvas

TYPES = ["RED", "BLUE", "GREEN", "PURPLE"]
WIDTH = 400
HEIGHT = 400
BOXES_PER_SIDE = 10

class Match(object):
	"""docstring for Match"""
	def __init__(self):
		self.canvas = MatchCanvas(self, WIDTH, HEIGHT, BOXES_PER_SIDE, BOXES_PER_SIDE)
		self.grid = [[-1 for i in range(BOXES_PER_SIDE)] for j in range(BOXES_PER_SIDE)]

		self.selected = None

	def fillGridRandom(self):
		for i in range(BOXES_PER_SIDE):
			for j in range(BOXES_PER_SIDE):
				color = random.choice(TYPES)
				pos = self.canvas.indexToPos(i, j)
				self.grid[i][j] = self.canvas.circle(pos[0], pos[1], color)
				self..canvas.canvas.tag_bind(self.grid[i][j], '<ButtonPress-1>', self.canvas_onclick)

	def colorOf(self, item):
		return self.canvas.canvas.gettags(item)[0]

	def posOf(self, item):
		coords = self.canvas.canvas.coords(item)
		return (coords[0] + coords[2] / 2, coords[1] + coords[3] / 2)

	def findCurrentItem(self):
		return self.canvas.canvas.find_withtag("current")[0]
