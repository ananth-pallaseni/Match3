""" Canvas """

import tkinter as tk
import sys
import random
import math

class CustomCanvas(object):
	"""A basic canvas object that contains basic drawing functions. Extend for custom functionality"""
	def __init__(self, parent, width, height):
		# Attributes:
		self.parent = parent
		self.width = width
		self.height = height

		# Root window:
		self.tk = tk.Tk()
		self.tk.title("Match 3")

		# Canvas:
		self.canvas = tk.Canvas(self.tk, width=width, height=height, bg="White")
		self.canvas.pack()

	def drawCircle(self, centerX, centerY, radius, lineColor='White', lineWidth=1, filled=1, fillColor="Black", tag=""):
		""" Draw a circle with specified radius at center. Returns its tkinter id"""
		if filled == 0:
			fillColor = ""

		x0 = centerX - radius
		y0 = centerY - radius
		x1 = centerX + radius
		y1 = centerY + radius
		return self.canvas.create_oval(x0, y0, x1, y1, outline=lineColor, fill=fillColor, width=lineWidth, tags=tag)

	def drawLine(self, startx, starty, endx, endy, lineColor='White', lineWidth=1, tag=""):
		""" Draw a line from (startx, starty) to (endx, endy). Returns its tkinter id"""

		return self.canvas.create_line(startx, starty, endx, endy, fill=lineColor, width=lineWidth, tags=tag)




