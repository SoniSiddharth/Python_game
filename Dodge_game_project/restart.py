# to run the game, run this python file
import pygame
import numpy as np
import matplotlib
pygame.init()

# creating a function to restart the game and executing the main game file "Dodge_game.py" in this file
def restart_game():
	execfile(r"C:\Users\HP\Desktop\Dodge_game_project\Dodge_game.py")
	# exec(compile(open('Dodge_game.py', "rb").read(), 'Dodge_game.py', 'exec'))
r = True
screen = pygame.display.set_mode((100, 100))

# for restarting the game and defining the event of the space key
restart_game()
while r:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				restart_game()
		if event.type == pygame.QUIT:
			r = False
pygame.quit()


