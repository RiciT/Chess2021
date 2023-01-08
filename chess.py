import time
import os
import random
import pygame
import math
import copy

pygame.init()

		###			TO BE PATCHED 		###

#KING CAN WALK IN CHECK GIVING THE WIN TO THE OTHER

		###################################

#CONSTs
WIN_WIDTH = 400
WIN_HEIGHT = 400
BOARDLENGTH = 8
IMAGE_SCALE = 0.35
BLACK, WHITE, SELECTBLACK, SELECTWHITE, RED = (181, 136, 99), (240, 217, 181), (166, 121, 84), (225, 202, 166), (221, 0, 0)
BLACK_ROCK = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blackrock.png")), 0, IMAGE_SCALE)
BLACK_KNIGHT = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blackknight.png")), 0, IMAGE_SCALE)
BLACK_BISHOP = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blackbishop.png")), 0, IMAGE_SCALE)
BLACK_QUEEN = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blackqueen.png")), 0, IMAGE_SCALE)
BLACK_KING = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blackking.png")), 0, IMAGE_SCALE)
BLACK_PAWN = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blackpawn.png")), 0, IMAGE_SCALE)

WHITE_ROCK = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "whiterock.png")), 0, IMAGE_SCALE)
WHITE_KNIGHT = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "whiteknight.png")), 0, IMAGE_SCALE)
WHITE_BISHOP = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "whitebishop.png")), 0, IMAGE_SCALE)
WHITE_QUEEN = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "whitequeen.png")), 0, IMAGE_SCALE)
WHITE_KING = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "whiteking.png")), 0, IMAGE_SCALE)
WHITE_PAWN = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "whitepawn.png")), 0, IMAGE_SCALE)

#piece_classes
class Rock:

	class_id = "Rock"

	def __init__(self, color):
		self.color = color
		self.pickuppoint = [0, 0]
		self.goalpoint = [0, 0]

	def __eq__(self, other):
		if other is None:
			return False
		return (self.class_id, self.color) == (other.class_id, other.color)
	
	def draw(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_ROCK.get_height()
			width = WHITE_ROCK.get_width()
			win.blit(WHITE_ROCK, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))
		if self.color == "black":
			height = BLACK_ROCK.get_height()
			width = BLACK_ROCK.get_width()
			win.blit(BLACK_ROCK, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))

	def drawOnWindow(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_ROCK.get_height()
			width = WHITE_ROCK.get_width()
			win.blit(WHITE_ROCK, (x - width / 2, y - height / 2))
		if self.color == "black":
			height = BLACK_ROCK.get_height()
			width = BLACK_ROCK.get_width()
			win.blit(BLACK_ROCK, (x - width / 2, y - height / 2))

	def setPickupPoint(self, x, y):
		self.pickuppoint = [y, x]

	def validate(self, x, y):
		goalpoint = [y, x]
		valid = False
		for i in range(1, 8):
			#print(self.pickuppoint[0], self.pickuppoint[1])
			#print(goalpoint[0], goalpoint[1])
			#print(i)
			#print("\n")
			if (abs(goalpoint[0] - self.pickuppoint[0]) == i and goalpoint[1] == self.pickuppoint[1]) or (abs(goalpoint[1] - self.pickuppoint[1]) == i and goalpoint[0] == self.pickuppoint[0]):
				valid = True
				for j in range(1, i + 1):
					if goalpoint[0] > self.pickuppoint[0]:
						if current_board[goalpoint[1]][goalpoint[0] - j] != None:
							valid = False
							break
					if goalpoint[0] < self.pickuppoint[0]:
						if current_board[goalpoint[1]][goalpoint[0] + j] != None:
							valid = False
							break
					if goalpoint[1] > self.pickuppoint[1]:
						if current_board[goalpoint[1] - j][goalpoint[0]] != None:
							valid = False
							break
					if goalpoint[1] < self.pickuppoint[1]:
						if current_board[goalpoint[1] + j][goalpoint[0]] != None:
							valid = False
							break

		if current_board[goalpoint[1]][goalpoint[0]] != None:
			if self.color == current_board[goalpoint[1]][goalpoint[0]].color:
				valid = False

		return valid

	def canCapture(self, pivot, test = False):
		defendedTiles = [[None]*64 for i in range(64)]
		index = 0
		if test:
			for i in range(8):
				for j in range(8):
					if j == pivot[1] or i == pivot[0]:
						if i > pivot[0]:
							for z in range(1, i - pivot[0] + 1): 
								if checkmatetest_board[pivot[0] + z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if i < pivot[0]:
							for z in range(1, pivot[0] - i + 1):
								if checkmatetest_board[pivot[0] - z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if j > pivot[1]:
							for z in range(1, j - pivot[1] + 1):
								if checkmatetest_board[pivot[0]][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if j < pivot[1]:
							for z in range(1, pivot[1] - j + 1):
								if checkmatetest_board[pivot[0]][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
		else:
			for i in range(8):
				for j in range(8):
					if j == pivot[1] or i == pivot[0]:
						if i > pivot[0]:
							for z in range(1, i - pivot[0] + 1): 
								if current_board[pivot[0] + z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if i < pivot[0]:
							for z in range(1, pivot[0] - i + 1):
								if current_board[pivot[0] - z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if j > pivot[1]:
							for z in range(1, j - pivot[1] + 1):
								if current_board[pivot[0]][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if j < pivot[1]:
							for z in range(1, pivot[1] - j + 1):
								if current_board[pivot[0]][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
							
		return defendedTiles

class Knight:

	class_id = "Knight"

	def __init__(self, color):
		self.color = color
		self.pickuppoint = [0, 0]
		self.goalpoint = [0, 0]

	def __eq__(self, other):
		if other is None:
			return False
		return (self.class_id, self.color) == (other.class_id, other.color)
	
	def draw(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_KNIGHT.get_height()
			width = WHITE_KNIGHT.get_width()
			win.blit(WHITE_KNIGHT, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))
		if self.color == "black":
			height = BLACK_KNIGHT.get_height()
			width = BLACK_KNIGHT.get_width()
			win.blit(BLACK_KNIGHT, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))

	def drawOnWindow(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_KNIGHT.get_height()
			width = WHITE_KNIGHT.get_width()
			win.blit(WHITE_KNIGHT, (x - width / 2, y - height / 2))
		if self.color == "black":
			height = BLACK_KNIGHT.get_height()
			width = BLACK_KNIGHT.get_width()
			win.blit(BLACK_KNIGHT, (x - width / 2, y - height / 2))

	def setPickupPoint(self, x, y):
		self.pickuppoint = [y, x]

	def validate(self, x, y):
		goalpoint = [y, x]
		valid = False
		if (abs(goalpoint[0] - self.pickuppoint[0]) == 2 and abs(goalpoint[1] - self.pickuppoint[1]) == 1) or (abs(goalpoint[0] - self.pickuppoint[0]) == 1 and abs(goalpoint[1] - self.pickuppoint[1]) == 2):
			valid = True

		if current_board[goalpoint[1]][goalpoint[0]] != None:
			if self.color == current_board[goalpoint[1]][goalpoint[0]].color:
				valid = False

		return valid

	def canCapture(self, pivot, test = False):
		defendedTiles = [[None]*64 for i in range(64)]
		index = 0
		for i in range(8):
			for j in range(8):
				if (abs(i - pivot[0]) == 2 and abs(j - pivot[1]) == 1) or (abs(i - pivot[0]) == 1 and abs(j - pivot[1]) == 2):
					defendedTiles[index][0] = i
					defendedTiles[index][1] = j
					index += 1

		return defendedTiles

class Bishop:

	class_id = "Bishop"

	def __init__(self, color):
		self.color = color
		self.pickuppoint = [0, 0]
		self.goalpoint = [0, 0]

	def __eq__(self, other):
		if other is None:
			return False
		return (self.class_id, self.color) == (other.class_id, other.color)
	
	def draw(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_BISHOP.get_height()
			width = WHITE_BISHOP.get_width()
			win.blit(WHITE_BISHOP, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))
		if self.color == "black":
			height = BLACK_BISHOP.get_height()
			width = BLACK_BISHOP.get_width()
			win.blit(BLACK_BISHOP, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))

	def drawOnWindow(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_BISHOP.get_height()
			width = WHITE_BISHOP.get_width()
			win.blit(WHITE_BISHOP, (x - width / 2, y - height / 2))
		if self.color == "black":
			height = BLACK_BISHOP.get_height()
			width = BLACK_BISHOP.get_width()
			win.blit(BLACK_BISHOP, (x - width / 2, y - height / 2))

	def setPickupPoint(self, x, y):
		self.pickuppoint = [y, x]

	def validate(self, x, y):
		goalpoint = [y, x]
		valid = False
		for i in range(1, 8):
			#for j in range(abs(goalpoint[0] - pickuppoint[0])):
			if (abs(goalpoint[1] - self.pickuppoint[1]) == i and abs(goalpoint[0] - self.pickuppoint[0]) == i):
				valid = True
				for j in range(1, i + 1):
					#print(self.pickuppoint[0], self.pickuppoint[1])
					#print(goalpoint[0], goalpoint[1])
					#print(j, i)
					#print("\n")
					if goalpoint[0] > self.pickuppoint[0] and goalpoint[1] > self.pickuppoint[1]:
						if current_board[goalpoint[1] - j][goalpoint[0] - j] != None:
							valid = False
							break
					if goalpoint[0] < self.pickuppoint[0] and goalpoint[1] > self.pickuppoint[1]:
						if current_board[goalpoint[1] - j][goalpoint[0] + j] != None:
							valid = False
							break
					if goalpoint[0] > self.pickuppoint[0] and goalpoint[1] < self.pickuppoint[1]:
						if current_board[goalpoint[1] + j][goalpoint[0] - j] != None:
							valid = False
							break
					if goalpoint[0] < self.pickuppoint[0] and goalpoint[1] < self.pickuppoint[1]:
						if current_board[goalpoint[1] + j][goalpoint[0] + j] != None:
							valid = False
							break

		if current_board[goalpoint[1]][goalpoint[0]] != None:
			if self.color == current_board[goalpoint[1]][goalpoint[0]].color:
				valid = False

		return valid

	def canCapture(self, pivot, test = False):
		defendedTiles = [[None]*64 for i in range(64)]
		index = 0
		if test:
			for i in range(8):
				for j in range(8):
					if (abs(j - pivot[1]) == abs(i - pivot[0])):
						if i > pivot[0] and j > pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if checkmatetest_board[pivot[0] + z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i > pivot[0] and j < pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if checkmatetest_board[pivot[0] + z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
						if i < pivot[0] and j > pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if checkmatetest_board[pivot[0] - z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i < pivot[0] and j < pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if checkmatetest_board[pivot[0] - z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
		else:
			for i in range(8):
				for j in range(8):
					if (abs(j - pivot[1]) == abs(i - pivot[0])):
						if i > pivot[0] and j > pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if current_board[pivot[0] + z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i > pivot[0] and j < pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if current_board[pivot[0] + z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
						if i < pivot[0] and j > pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if current_board[pivot[0] - z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i < pivot[0] and j < pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if current_board[pivot[0] - z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
							
		return defendedTiles

class Queen:

	class_id = "Queen"

	def __init__(self, color):
		self.color = color
		self.pickuppoint = [0, 0]
		self.goalpoint = [0, 0]

	def __eq__(self, other):
		if other is None:
			return False
		return (self.class_id, self.color) == (other.class_id, other.color)
	
	def draw(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_QUEEN.get_height()
			width = WHITE_QUEEN.get_width()
			win.blit(WHITE_QUEEN, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))
		if self.color == "black":
			height = BLACK_QUEEN.get_height()
			width = BLACK_QUEEN.get_width()
			win.blit(BLACK_QUEEN, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))

	def drawOnWindow(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_QUEEN.get_height()
			width = WHITE_QUEEN.get_width()
			win.blit(WHITE_QUEEN, (x - width / 2, y - height / 2))
		if self.color == "black":
			height = BLACK_QUEEN.get_height()
			width = BLACK_QUEEN.get_width()
			win.blit(BLACK_QUEEN, (x - width / 2, y - height / 2))

	def setPickupPoint(self, x, y):
		self.pickuppoint = [y, x]

	def validate(self, x, y):
		goalpoint = [y, x]
		valid = False
		for i in range(1, 8):
			#for j in range(abs(goalpoint[0] - pickuppoint[0])):
			if (abs(goalpoint[1] - self.pickuppoint[1]) == i and abs(goalpoint[0] - self.pickuppoint[0]) == i):
				valid = True
				for j in range(1, i + 1):
					#print(self.pickuppoint[0], self.pickuppoint[1])
					#print(goalpoint[0], goalpoint[1])
					#print(j, i)
					#print("\n")
					if goalpoint[0] - self.pickuppoint[0] > 0 and goalpoint[1] - self.pickuppoint[1] > 0:
						if current_board[goalpoint[1] - j][goalpoint[0] - j] != None:
							valid = False
							break
					if goalpoint[0] - self.pickuppoint[0] < 0 and goalpoint[1] - self.pickuppoint[1] > 0:
						if current_board[goalpoint[1] - j][goalpoint[0] + j] != None:
							valid = False
							break
					if goalpoint[0] - self.pickuppoint[0] > 0 and goalpoint[1] - self.pickuppoint[1] < 0:
						if current_board[goalpoint[1] + j][goalpoint[0] - j] != None:
							valid = False
							break
					if goalpoint[0] - self.pickuppoint[0] < 0 and goalpoint[1] - self.pickuppoint[1] < 0:
						if current_board[goalpoint[1] + j][goalpoint[0] + j] != None:
							valid = False
							break
			if (abs(goalpoint[0] - self.pickuppoint[0]) == i and goalpoint[1] == self.pickuppoint[1]) or (abs(goalpoint[1] - self.pickuppoint[1]) == i and goalpoint[0] == self.pickuppoint[0]):
				valid = True
				for j in range(1, i + 1):
					if goalpoint[0] > self.pickuppoint[0]:
						if current_board[goalpoint[1]][goalpoint[0] - j] != None:
							valid = False
							break
					if goalpoint[0] < self.pickuppoint[0]:
						if current_board[goalpoint[1]][goalpoint[0] + j] != None:
							valid = False
							break
					if goalpoint[1] > self.pickuppoint[1]:
						if current_board[goalpoint[1] - j][goalpoint[0]] != None:
							valid = False
							break
					if goalpoint[1] < self.pickuppoint[1]:
						if current_board[goalpoint[1] + j][goalpoint[0]] != None:
							valid = False
							break

		if current_board[goalpoint[1]][goalpoint[0]] != None:
			if self.color == current_board[goalpoint[1]][goalpoint[0]].color:
				valid = False

		return valid

	def canCapture(self, pivot, test = False):
		defendedTiles = [[None]*64 for i in range(64)]
		index = 0
		if test:
			for i in range(8):
				for j in range(8):
					if j == pivot[1] or i == pivot[0]:
						if i > pivot[0]:
							for z in range(1, i - pivot[0] + 1):
								if checkmatetest_board[pivot[0] + z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if i < pivot[0]:
							for z in range(1, pivot[0] - i + 1):
								if checkmatetest_board[pivot[0] - z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if j > pivot[1]:
							for z in range(1, j - pivot[1] + 1):
								if checkmatetest_board[pivot[0]][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if j < pivot[1]:
							for z in range(1, pivot[1] - j + 1):
								if checkmatetest_board[pivot[0]][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
					if (abs(j - pivot[1]) == abs(i - pivot[0])):
						if i > pivot[0] and j > pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if checkmatetest_board[pivot[0] + z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i > pivot[0] and j < pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if checkmatetest_board[pivot[0] + z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
						if i < pivot[0] and j > pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if checkmatetest_board[pivot[0] - z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i < pivot[0] and j < pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if checkmatetest_board[pivot[0] - z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
		else:
			for i in range(8):
				for j in range(8):
					if j == pivot[1] or i == pivot[0]:
						if i > pivot[0]:
							for z in range(1, i - pivot[0] + 1):
								if current_board[pivot[0] + z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if i < pivot[0]:
							for z in range(1, pivot[0] - i + 1):
								if current_board[pivot[0] - z][pivot[1]] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1]
									index += 1
						if j > pivot[1]:
							for z in range(1, j - pivot[1] + 1):
								if current_board[pivot[0]][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if j < pivot[1]:
							for z in range(1, pivot[1] - j + 1):
								if current_board[pivot[0]][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0]
									defendedTiles[index][1] = pivot[1] - z
									index += 1
					if (abs(j - pivot[1]) == abs(i - pivot[0])):
						if i > pivot[0] and j > pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if current_board[pivot[0] + z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i > pivot[0] and j < pivot[1]:
							for z in range(1, i - pivot[0] + 1):
								if current_board[pivot[0] + z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] + z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
						if i < pivot[0] and j > pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if current_board[pivot[0] - z][pivot[1] + z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] + z
									index += 1
						if i < pivot[0] and j < pivot[1]:
							for z in range(1, pivot[0] - i + 1):
								if current_board[pivot[0] - z][pivot[1] - z] != None:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1
									break
								else:
									defendedTiles[index][0] = pivot[0] - z
									defendedTiles[index][1] = pivot[1] - z
									index += 1		
		return defendedTiles

class King:

	class_id = "King"

	def __init__(self, color):
		self.color = color
		self.pickuppoint = [0, 0]
		self.goalpoint = [0, 0]

	def __eq__(self, other):
		#print(other)
		if other is None:
			return False
		return (self.class_id, self.color) == (other.class_id, other.color)
	
	def draw(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_KING.get_height()
			width = WHITE_KING.get_width()
			win.blit(WHITE_KING, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))
		if self.color == "black":
			height = BLACK_KING.get_height()
			width = BLACK_KING.get_width()
			win.blit(BLACK_KING, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))

	def drawOnWindow(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_KING.get_height()
			width = WHITE_KING.get_width()
			win.blit(WHITE_KING, (x - width / 2, y - height / 2))
		if self.color == "black":
			height = BLACK_KING.get_height()
			width = BLACK_KING.get_width()
			win.blit(BLACK_KING, (x - width / 2, y - height / 2))

	def setPickupPoint(self, x, y):
		self.pickuppoint = [y, x]

	def validate(self, x, y):
		goalpoint = [y, x]
		valid = False
		if (goalpoint[1] == self.pickuppoint[1] or abs(goalpoint[1] - self.pickuppoint[1]) == 1) and (goalpoint[0] == self.pickuppoint[0] or abs(goalpoint[0] - self.pickuppoint[0]) == 1):
			valid = True
		
		if current_board[goalpoint[1]][goalpoint[0]] != None:
			if self.color == current_board[goalpoint[1]][goalpoint[0]].color:
				valid = False

		return valid

	def canCapture(self, pivot, test = False):
		defendedTiles = [[None]*64 for i in range(64)]
		index = 0
		for i in range(8):
			for j in range(8):
				if (j == pivot[1] or abs(j - pivot[1]) == 1) and (i == pivot[0] or abs(i - pivot[0]) == 1):
					defendedTiles[index][0] = i
					defendedTiles[index][1] = j
					index += 1

		return defendedTiles

class Pawn:
	
	class_id = "Pawn"
	
	def __init__(self, color, test = False):
		self.color = color
		self.pickuppoint = [0, 0]
		self.goalpoint = [0, 0]

	def __eq__(self, other):
		if other is None:
			return False
		return (self.class_id, self.color) == (other.class_id, other.color)
	
	def draw(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_PAWN.get_height()
			width = WHITE_PAWN.get_width()
			win.blit(WHITE_PAWN, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))
		if self.color == "black":
			height = BLACK_PAWN.get_height()
			width = BLACK_PAWN.get_width()
			win.blit(BLACK_PAWN, (25 + x * 50 - width / 2, 25 + y * 50 - height / 2))

	def drawOnWindow(self, win, x = 0, y = 0):
		if self.color == "white":
			height = WHITE_PAWN.get_height()
			width = WHITE_PAWN.get_width()
			win.blit(WHITE_PAWN, (x - width / 2, y - height / 2))
		if self.color == "black":
			height = BLACK_PAWN.get_height()
			width = BLACK_PAWN.get_width()
			win.blit(BLACK_PAWN, (x - width / 2, y - height / 2))

	def setPickupPoint(self, x, y):
		self.pickuppoint = [y, x]

	def validate(self, x, y):
		goalpoint = [y, x]
		valid = False
		if self.color == "black":
			if goalpoint[1] - self.pickuppoint[1] == 1 and goalpoint[0] == self.pickuppoint[0] and current_board[goalpoint[1]][goalpoint[0]] == None:
				valid = True
			if goalpoint[1] - self.pickuppoint[1] == 1 and abs(goalpoint[0] - self.pickuppoint[0]) == 1 and current_board[goalpoint[1]][goalpoint[0]] != None:
				valid = True
			if self.pickuppoint[1] == 1 and goalpoint[1] - self.pickuppoint[1] == 2 and goalpoint[0] == self.pickuppoint[0] and current_board[goalpoint[1]][goalpoint[0]] == None:
				valid = True
		if self.color == "white":
			if goalpoint[1] - self.pickuppoint[1] == -1 and goalpoint[0] == self.pickuppoint[0] and current_board[goalpoint[1]][goalpoint[0]] == None:
				valid = True
			if goalpoint[1] - self.pickuppoint[1] == -1 and abs(goalpoint[0] - self.pickuppoint[0]) == 1 and current_board[goalpoint[1]][goalpoint[0]] != None:
				valid = True
			if self.pickuppoint[1] == 6 and goalpoint[1] - self.pickuppoint[1] == -2 and goalpoint[0] == self.pickuppoint[0] and current_board[goalpoint[1]][goalpoint[0]] == None:
				valid = True

		if current_board[goalpoint[1]][goalpoint[0]] != None:
			if self.color == current_board[goalpoint[1]][goalpoint[0]].color:
				valid = False

		return valid

	def canCapture(self, pivot, test = False):
		defendedTiles = [[None]*64 for i in range(64)]
		if self.color == "black":
			defendedTiles[0][0] = pivot[0] + 1
			defendedTiles[0][1] = pivot[1] - 1
			defendedTiles[1][0] = pivot[0] + 1
			defendedTiles[1][1] = pivot[1] + 1
		if self.color == "white":
			defendedTiles[0][0] = pivot[0] - 1
			defendedTiles[0][1] = pivot[1] + 1
			defendedTiles[1][0] = pivot[0] - 1
			defendedTiles[1][1] = pivot[1] - 1

		return defendedTiles

#board_variables
current_board = [[Rock("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rock("black")],
				[Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black")],
				[None, None, None, None, None, None, None, None],
				[None, None, None, None, None, None, None, None],
				[None, None, None, None, None, None, None, None],
				[None, None, None, None, None, None, None, None],
				[Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white")],
				[Rock("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rock("white")]]
current_black_attack = [[None for y in range(8)] for x in range(8)]
current_white_attack = [[None for y in range(8)] for x in range(8)]
checkmatetest_board = current_board
checkmatetest_black_attack = current_black_attack
checkmatetest_white_attack = current_white_attack

#draw
def setupWindow(win, size, selectedPiece, king = None):
	pygame.display.set_caption("ChessBoard")
	win.fill(WHITE)

	#print(current_board[7][0] == current_board[7][7])
	cnt = 0
	for i in range(BOARDLENGTH):
		for z in range(BOARDLENGTH):
			#check if current loop value is even
			if cnt % 2 == 0:
				pygame.draw.rect(win, WHITE, [size * z, size * i, size, size])
				if selectedPiece != None and selectedPiece.pickuppoint[1] == i and selectedPiece.pickuppoint[0] == z:
					pygame.draw.rect(win, SELECTWHITE, [size * z, size * i, size, size])
			else:
				pygame.draw.rect(win, BLACK, [size * z, size * i, size, size])
				if selectedPiece != None and selectedPiece.pickuppoint[1] == i and selectedPiece.pickuppoint[0] == z:
					pygame.draw.rect(win, SELECTBLACK, [size * z, size * i, size, size])
			if king:
				if king.pickuppoint == [i, z]:
					pygame.draw.rect(win, RED, [size * z, size * i, size, size])
			cnt += 1
			#since theres an even number of squares go back one value
		cnt -= 1
	#Add a nice boarder
	pygame.draw.rect(win, BLACK, [size, size, WIN_WIDTH, WIN_HEIGHT], 1)

def drawWin(win, selectedPiece, selectedPieceCoords):
	for i in range(BOARDLENGTH):
		for j in range(BOARDLENGTH):
			if current_board[j][i] != None:
				current_board[j][i].draw(win, i, j)

	if selectedPiece != None:
		selectedPiece.draw(win, int(selectedPieceCoords[0] / 50), int(selectedPieceCoords[1] / 50))

def drawWinWin(win, color):
	if color == "white":
		pygame.draw.rect(win, WHITE, [0, 0, WIN_WIDTH, WIN_HEIGHT])
	if color == "black":
		pygame.draw.rect(win, BLACK, [0, 0, WIN_WIDTH, WIN_HEIGHT])
	
#mechanics
def getAttackedTiles(color, test = False):
	global current_black_attack
	global current_white_attack
	global checkmatetest_black_attack
	global checkmatetest_white_attack
	for i in range(8):
		for j in range(8):
			if color == "black":
				current_black_attack[j][i] = None
				checkmatetest_black_attack[j][i] = None
			if color == "white":
				current_white_attack[j][i] = None
				checkmatetest_white_attack[j][i] = None
	if test:
		for i in range(8):
			for j in range(8):
				if checkmatetest_board[j][i] != None:
					if checkmatetest_board[j][i].color == color:
						for e in checkmatetest_board[j][i].canCapture([j, i], True):
							if color == "black" and e[0] != None and e[1] != None and e[0] >= 0 and e[1] >= 0 and e[0] <= 7 and e[1] <= 7:
								checkmatetest_black_attack[e[0]][e[1]] = "cb"
							if color == "white" and e[0] != None and e[1] != None and e[0] >= 0 and e[1] >= 0 and e[0] <= 7 and e[1] <= 7:
								checkmatetest_white_attack[e[0]][e[1]] = "cb"
								

	else:
		for i in range(8):
			for j in range(8):
				if current_board[j][i] != None:
					if current_board[j][i].color == color:
						for e in current_board[j][i].canCapture([j, i]):
							if color == "black" and e[0] != None and e[1] != None and e[0] >= 0 and e[1] >= 0 and e[0] <= 7 and e[1] <= 7:
								current_black_attack[e[0]][e[1]] = "cb"
							if color == "white" and e[0] != None and e[1] != None and e[0] >= 0 and e[1] >= 0 and e[0] <= 7 and e[1] <= 7:
								current_white_attack[e[0]][e[1]] = "cb"

def checkForCheckmate(attackedKingPos, color):
	global checkmatetest_board
	current_piece = None
	for b_j in range(8):
		for b_i in range(8):
			if current_board[b_j][b_i] != None:
				if color == current_board[b_j][b_i].color:
					current_piece = current_board[b_j][b_i]
					for i in range(8):
						for j in range(8):
							checkmatetest_board = copy.deepcopy(current_board)
							current_piece.setPickupPoint(b_j, b_i)
							if current_piece.validate(j, i):
								checkmatetest_board[b_j][b_i] = None
								checkmatetest_board[j][i] = current_piece
								getAttackedTiles("white", True)
								getAttackedTiles("black", True)
								
								#print(b_j, b_i, j, i, checkmatetest_black_attack[attackedKingPos[0]][attackedKingPos[1]], checkmatetest_white_attack[attackedKingPos[0]][attackedKingPos[1]])

								if color == "white":
									if checkmatetest_black_attack[attackedKingPos[0]][attackedKingPos[1]] != "cb":
										return False
								else:
									if checkmatetest_white_attack[attackedKingPos[0]][attackedKingPos[1]] != "cb":
										return False
	return True

#mains
def main():
	run = True
	gameExit = False
	clock = pygame.time.Clock()
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	size = WIN_HEIGHT / BOARDLENGTH
	selected = False
	selectedPiece = None
	attackedPiece = None
	king = None
	checkmateIsPossible = 0
	current_round = "white"
	selectedPieceCoords = [0, 0]
	global current_board

	while run:
		clock.tick(30)
		ev = pygame.event.get()
		for event in ev:
			setupWindow(win, size, selectedPiece)
			drawWin(win, selectedPiece, selectedPieceCoords)
			pygame.display.update()
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if selected:
					x,y = pygame.mouse.get_pos()
					attackedPiece = None
					if selectedPiece.validate(math.floor(y / 50), math.floor(x / 50)):
						if selectedPiece.__eq__(Pawn("white")):
							if math.floor(y / 50) == 0:
								selectedPiece = Queen("white")
						if selectedPiece.__eq__(Pawn("black")):
							if math.floor(y / 50) == 7:
								selectedPiece = Queen("black")
						if current_board[math.floor(y / 50)][math.floor(x / 50)] != None:
							attackedPiece = current_board[math.floor(y / 50)][math.floor(x / 50)]
						selected = False
						current_board[math.floor(y / 50)][math.floor(x / 50)] = selectedPiece
						if current_round == "white":
							current_round = "black"
							getAttackedTiles("black")
							getAttackedTiles("white")
							for i in range(8):
								for j in range(8):
									if current_board[i][j].__eq__(King("white")) == True:
										king = [i, j]
										break
								else:
									continue
								break
							if current_black_attack[king[0]][king[1]] == "cb":
								if checkForCheckmate(king, "white"):
									print("checkmate")
									run = False #THIS IS BAD WE NEED A PROPER WAY TO STOP THE GAME
									drawWinWin(win, "black") #black wins
									pygame.display.update()
									loseScreen()
									return
								current_board[selectedPiece.pickuppoint[1]][selectedPiece.pickuppoint[0]] = selectedPiece
								current_board[math.floor(y / 50)][math.floor(x / 50)] = attackedPiece
								selectedPiece = None
								current_round = "white"
								getAttackedTiles("black")
								getAttackedTiles("white")
								
						else:
							current_round = "white"
							getAttackedTiles("black")
							getAttackedTiles("white")
							for i in range(8):
								for j in range(8):
									if current_board[i][j].__eq__(King("black")) == True:
										king = [i, j]
										break
								else:
									continue
								break
							if current_white_attack[king[0]][king[1]] == "cb":
								if checkForCheckmate(king, "black"):
									print("checkmate")
									run = False #THIS IS BAD WE NEED A PROPER WAY TO STOP THE GAME
									drawWinWin(win, "white") #white wins
									pygame.display.update()
									loseScreen()
									return
								current_board[selectedPiece.pickuppoint[1]][selectedPiece.pickuppoint[0]] = selectedPiece
								current_board[math.floor(y / 50)][math.floor(x / 50)] = attackedPiece
								selectedPiece = None
								current_round = "black"
								getAttackedTiles("white")
								getAttackedTiles("black")
						selectedPiece = None
								
				else:
					x,y = pygame.mouse.get_pos()
					selectedPiece = current_board[math.floor(y / 50)][math.floor(x / 50)]
					if selectedPiece != None and selectedPiece.color == current_round:
						selectedPiece.setPickupPoint(math.floor(y / 50), math.floor(x / 50))
						current_board[math.floor(y / 50)][math.floor(x / 50)] = None
						selected = True
					else:
						selectedPiece = None
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if selectedPiece != None:
						current_board[selectedPiece.pickuppoint[1]][selectedPiece.pickuppoint[0]] = selectedPiece
						selectedPiece = None
						selected = False
		if selectedPiece:
			x,y = pygame.mouse.get_pos()
			selectedPieceCoords = [x, y]

def loseScreen():
	while True:
		ev = pygame.event.get()
		for event in ev:
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				restart()
				main()

def restart():
	global current_board
	global current_black_attack
	global current_white_attack
	global checkmatetest_board
	global checkmatetest_black_attack
	global checkmatetest_white_attack
	current_board = [[Rock("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rock("black")],
					[Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black")],
					[None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None],
					[Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white")],
					[Rock("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rock("white")]]
	current_black_attack = [[None for y in range(8)] for x in range(8)]
	current_white_attack = [[None for y in range(8)] for x in range(8)]
	checkmatetest_board = current_board
	checkmatetest_black_attack = current_black_attack
	checkmatetest_white_attack = current_white_attack

if __name__ == "__main__":
	main()