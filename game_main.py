import pygame, os, sys, random, math
from dynamics import Dynamics


class Predator(pygame.sprite.Sprite):

	# Makes the predator sprite, stay away from it

	def __init__(self,screen,level):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image, self.rect = Game().load_image('predator.png',-1)

		# Randomly place the object on the screen
		self.frame = screen.get_rect()
		xposition  = math.floor(random.random()*(self.frame.width-self.rect.width))
		yposition  = math.floor(random.random()*(self.frame.height-self.rect.height))
		self.rect.topleft = xposition,yposition


		self.maxstep = 10*level

	def position(self):

		center_x = self.rect.x + (self.rect.width/2.0)
		center_y = self.rect.y + (self.rect.height/2.0)

		return center_x,center_y

	def update(self,player_pos):

		# player_pos = positionof player = x,y
		player_x, player_y= player_pos[0] , player_pos[1]
		
		x1,y1 = self.position()		

		new_pos = Dynamics(x1,y1,player_x,player_y,self.frame,self.rect)
		new_cen_x,new_cen_y = new_pos.near_move(self.maxstep)
		new_cen_x,new_cen_y = new_pos.sphere_move(new_cen_x,new_cen_y)
		new_x,new_y = new_cen_x - (self.rect.width/2.0) , new_cen_y - (self.rect.height/2.0)
		
		self.rect.topleft = new_x,new_y

class Prey(pygame.sprite.Sprite):

	# Makes the prey sprite, catch it to win

	def __init__(self,screen,level):
		
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image, self.rect = Game().load_image('prey.png',-1)

		# Randomly place the object on the screen

		self.frame = screen.get_rect()
		xposition  = math.floor(random.random()*(self.frame.width-self.rect.width))
		yposition  = math.floor(random.random()*(self.frame.height-self.rect.height))
		self.rect.topleft = xposition,yposition
		
		self.maxstep = 10*level
		print self.maxstep

	def position(self):

		center_x = self.rect.x + (self.rect.width/2.0)
		center_y = self.rect.y + (self.rect.height/2.0)

		return center_x,center_y

	def update(self,player_pos):

		# player_pos = positionof player = x,y
		player_x = player_pos[0]
		player_y = player_pos[1]
		
		x1,y1 = self.position()

		new_pos = Dynamics(x1,y1,player_x,player_y,self.frame,self.rect)
		new_cen_x,new_cen_y = new_pos.far_move(self.maxstep)
		new_cen_x,new_cen_y = new_pos.sphere_move(new_cen_x,new_cen_y)
		new_x,new_y = new_cen_x - (self.rect.width/2.0) , new_cen_y - (self.rect.height/2.0)

		self.rect.topleft = new_x,new_y
		
		
class Player(pygame.sprite.Sprite):

	# Makes the player sprite, this is you

	def __init__(self,screen,level):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image, self.rect = Game().load_image('player.png',-1)

		# Randomly place the object on the screen
		self.dimensions = screen.get_rect()
		xposition  = math.floor(random.random()*(self.dimensions.width-self.rect.width))
		yposition  = math.floor(random.random()*(self.dimensions.height-self.rect.height))
		self.rect.topleft = xposition,yposition

		self.maxstep = 10*(level/2.0)


	def update(self,key):

		# key = a tuple 
		# 1 = positive movement, -1 = negative movement, 0 = no movement
		
		y_move = key[0]
		x_move = key[1]

		x1,y1 = self.position()

		new_x_cen = x1 + (self.maxstep*x_move)
		new_y_cen = y1 + (self.maxstep*y_move)
		new_pos = Dynamics(new_x_cen,new_y_cen,x1,y1,self.dimensions,self.rect)
	
	
		new_x,new_y = new_x_cen - (self.rect.width/2.0) , new_y_cen - (self.rect.height/2.0)
		self.rect.topleft = new_pos.sphere_move(new_x,new_y)


	def position(self):

		center_x = self.rect.x + (self.rect.width/2.0)
		center_y = self.rect.y + (self.rect.height/2.0)

		return center_x,center_y

class Game(object):

	def load_image(self, name, colorkey=None):

	    fullname = os.path.join('media', name)
	    try:
	        image = pygame.image.load(fullname)
	    except pygame.error, message:
	        print 'Cannot load image:', fullname
	        raise SystemExit, message

	    image = image.convert()
	    
	    if colorkey is not None:
	        if colorkey is -1:
	        	colorkey = image.get_at((0,0))
	    		
	        image.set_colorkey(colorkey, pygame.RLEACCEL)
	    
	    return image, image.get_rect()


	def Initialize_Level(self,level):
		
		# Initializing Stuff
		pygame.init()
		screen = pygame.display.set_mode((640,480))
		rect = screen.get_rect()
					
		# Making the background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((200, 200, 200))

		# Initializing game objects
		clock     = pygame.time.Clock()
		predator  = Predator(screen,level)
		prey      = Prey(screen,level)	
		player    = Player(screen,level)

		allsprites = pygame.sprite.Group((predator,prey,player))

		while 1:

			clock.tick(30)
			player_move = [0,0]

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					return
	
			keys = pygame.key.get_pressed()

			if keys[pygame.K_UP]:
				player_move[0] = -1
			if keys[pygame.K_DOWN]:
				player_move[0] = 1
			if keys[pygame.K_LEFT]:
				player_move[1] = -1
			if keys[pygame.K_RIGHT]:
				player_move[1] = 1
				

			player.update(player_move)
			playerPos = player.position()
			prey.update(playerPos)
			predator.update(playerPos)

			screen.blit(background, (0, 0))
			allsprites.draw(screen)
			pygame.display.flip()
			
			if player.rect.colliderect(prey.rect):
				return True

			if player.rect.colliderect(predator.rect):
				return False
		
	def main(self):
	
		level = 1

		instance = self.Initialize_Level(level)
		while instance:
			level += 1
			instance = self.Initialize_Level(level)

		raise SystemExit, "Game Over, you reached Level "+ str(level)

if __name__ == "__main__":
	
	Game().main()

