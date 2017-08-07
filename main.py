import pygame
import os
import math

os.system("clear")

print('Room Triangulation System')
print('Scale: 1m = 100px')
print()
roomWidth		= int(input('Width of the room in meters: '))
roomHeight		= int(input('Height of the room in meters: '))
screenWidth		= roomWidth*100+50
screenHeight	= roomHeight*100+50
beaconDistance	= screenWidth-100

white			= (255,		255,	255)
black			= (0,		0,		0)
blue			= (0,		63,		255)
green			= (0,		255,	63)
red				= (255,		0,		0)

angleLeft		= 20
angleRight		= 20

robotX			= 0
robotY			= 0

pygame.init()
pygame.font.init()
pixel			= pygame.font.Font('pixel.ttf', 8)
os.system('clear')

print('Room Triangulation System')

screen			= pygame.display.set_mode((screenWidth, screenHeight))
pygame.mouse.set_visible(1)
pygame.key.set_repeat(500, 1)

frame			= pygame.Surface((screenWidth, screenHeight))
pygame.draw.rect(frame, white, pygame.rect.Rect(25, 25, screenWidth-50, screenHeight-50), 1)
pygame.draw.circle(frame, green, (50, screenHeight-50), 15, 1)
pygame.draw.circle(frame, green, (screenWidth-50, screenHeight-50), 15, 1)
pygame.draw.line(frame, green, (50, screenHeight-50), (screenWidth-50, screenHeight-50), 1)

clock			= pygame.time.Clock()
running			= 1
checked			= 1
count			= 1

while(running):
	clock.tick(60)
	screen.fill((10,10,10))
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			running = 0
		if(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_ESCAPE):
				pygame.event.post(pygame.event.Event(pygame.QUIT))
			if(event.key == pygame.K_DOWN):
				if(checked == 1 and angleLeft > 10):
					angleLeft -= 1
				if(checked == 2 and angleRight > 10):
					angleRight -=1
			if(event.key == pygame.K_UP and angleLeft < 80):
				if(checked == 1):
					angleLeft += 1
				if(checked == 2 and angleRight < 80):
					angleRight +=1
		if(event.type == pygame.KEYUP):
			if(event.key == pygame.K_TAB):
				if(checked == 1):
					checked = 2
				elif(checked == 2):
					checked = 1

	screen.blit(frame, (0,0))
	# Calculate Robot Coordinates
	angleTop	= 180 - angleLeft - angleRight
	robotX		= ( math.cos(math.radians(angleLeft)) * math.sin(math.radians(angleRight)) * beaconDistance) / math.sin(math.radians(angleTop))
	robotY		= ( math.sin(math.radians(angleLeft)) * math.sin(math.radians(angleRight)) * beaconDistance) / math.sin(math.radians(angleTop))
	# Beacon Signals
	pygame.draw.line(screen, green, (robotX+50, screenHeight-robotY-25), (50, screenHeight-50), 1)
	pygame.draw.line(screen, green, (robotX+50, screenHeight-robotY-25), (screenWidth-50, screenHeight-50), 1)
	# Cartesian Lines
	pygame.draw.line(screen, red, (robotX+50, screenHeight-robotY+30), (robotX+50, screenHeight-27), 1)
	pygame.draw.line(screen, red, (robotX+50, screenHeight-robotY-80), (robotX+50, 26), 1)
	pygame.draw.line(screen, red, (robotX-5, screenHeight-robotY-25), (26, screenHeight-robotY-25), 1)
	pygame.draw.line(screen, red, (robotX+105, screenHeight-robotY-25), (screenWidth-26, screenHeight-robotY-25), 1)
	# Robot
	pygame.draw.rect(screen, red, pygame.rect.Rect(robotX, screenHeight-robotY-75, 100, 100), 1)
	# Robot Circle
	pygame.draw.arc(screen, blue, pygame.rect.Rect(robotX-25, screenHeight-robotY-100, 150, 150), math.radians(count*8), math.radians(count*8+80), 4)
	pygame.draw.arc(screen, blue, pygame.rect.Rect(robotX-30, screenHeight-robotY-105, 160, 160), -math.radians(count*6+90), -math.radians(count*6+40), 4)
	pygame.draw.arc(screen, blue, pygame.rect.Rect(robotX-35, screenHeight-robotY-110, 170, 170), math.radians(count*16+40), math.radians(count*16+180), 4)
	# Beacon Circle
	if(checked == 1):
		pygame.draw.arc(screen, blue, pygame.rect.Rect(30, screenHeight-70, 40, 40), math.radians(count*8), math.radians(count*8+80), 1)
	if(checked == 2):
		pygame.draw.arc(screen, blue, pygame.rect.Rect(screenWidth-70, screenHeight-70, 40, 40), math.radians(count*8), math.radians(count*8+80), 1)
	# Text
	robotXY		= pixel.render(str(round(robotX))+' | '+str(round(robotY)), 1, blue)
	angleText1	= pixel.render(str(angleLeft)+'°', 1, blue)
	angleText2	= pixel.render(str(angleRight)+'°', 1, blue)
	screen.blit(robotXY, (robotX+2, screenHeight-robotY-75))
	screen.blit(angleText1, (70, screenHeight-50))
	screen.blit(angleText2, (screenWidth-90, screenHeight-50))

	#print(count)
	count += 1

	pygame.display.flip()
