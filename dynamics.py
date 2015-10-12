import numpy as np
import math

class Vector(object):

	def __init__(self,x_coord,y_coord):
		
		self.x = x_coord
		self.y = y_coord
		
		self.vec = np.array([self.x,self.y])
		self.mag = math.sqrt(self.x**2+self.y**2)
		self.dir = self.vec/self.mag
		self.ang = math.atan(self.x/self.y)
			
	def __add__(self,other):
	
		xcomp = self.x + other.x
		ycomp = self.y + other.y
		
		return Vector(xcomp,ycomp)
		
	def __sub__(self,other):
		
		xcomp = self.x - other.x
		ycomp = self.x - other.y
		
		return Vector(xcomp,ycomp)
		


class Dynamics(object):

	def __init__(self,x1,y1,x2,y2,frame,image):

		# frame = range of x and y allowed = rect object
		# x1,y1 = top left position of the prey/predator
		# x2,y2 = top left position of the player

		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.frame = frame
		self.slope = self.calc_slope(x1,y1,x2,y2)
		self.dist  = self.distance(x1,y1,x2,y2)
		self.dimn  = image

	def quadrant(self,x,y):

		w = self.frame.width/2.0
		h = self.frame.height/2.0

    	#  ________________
		# |       |        |
		# |   Q1  |    Q2  |
		# |-------|--------|
		# |   Q4  |    Q3  |
		# |_______|________|

		if x>w:
			if y>h:
				return "Q3"
			else:
				return "Q2"
		else:
			if y>h:
				return "Q4"
			else:
				return "Q1"


	def max_distance(self):

		# Returns the maximum distance possible 
		# within the frame

		frame = self.frame
		y2 = self.y2
		x2 = self.x2

		d1 = self.distance(x2,y2,frame.left,frame.top)
		d2 = self.distance(x2,y2,frame.width,frame.top)
		d3 = self.distance(x2,y2,frame.left,frame.height)
		d4 = self.distance(x2,y2,frame.width,frame.height)

		return max([d1,d2,d3,d4])


	def distance(self,x1,y1,x2,y2):

		x1 = self.x1
		x2 = self.x2
		y1 = self.y1
		y2 = self.y2

		a = (x1-x2)**2
		b = (y1-y2)**2

		return math.sqrt(a+b)

	def calc_slope(self,x1,y1,x2,y2):

		if x1 == x2:
			return 'inf'
		else:
			return float((y2-y1))/float((x2-x1))
	
	def direction_change(self,x1,y1,x2,y2):

		# Returns True if a direction change is required
		# to get away or near an object after crossing the
		# screen boundaries

		W = self.frame.width/2
		H = self.frame.height/2
		quad1 = self.quadrant(x1,y1)
		quad2 = self.quadrant(x2,y2)
		dist = self.distance(x1,y1,x2,y2)


		TD = {('Q1','Q1'):(False,False),
				('Q1','Q2'):(True,False),
				('Q1','Q3'):(True,True),
				('Q1','Q4'):(False,True),
				('Q2','Q1'):(True,False),
				('Q2','Q2'):(False,False),
				('Q2','Q3'):(False,True),
				('Q2','Q4'):(True,True),
				('Q3','Q1'):(True,True),
				('Q3','Q2'):(False,True),
				('Q3','Q3'):(False,False),
				('Q3','Q4'):(True,False),
				('Q4','Q1'):(False,True),
				('Q4','Q2'):(True,True),
				('Q4','Q3'):(True,False),
				('Q4','Q4'):(False,False)}
		
		if abs(y2-y1) > H or abs(x2-x1) > W:
			return TD[(quad1,quad2)]
		else:
			return (False,False)

	def direction(self,x1p,y1p,x2p,y2p):

		# Direction of (x2,y2) w.r.t (x1,y1)
		# Top left of screen is (0,0) and X,Y increase
		# when going towards bottom right
		dir_change = self.direction_change(x1p,y1p,x2p,y2p)

		x1,y1,x2,y2 = x1p,y1p,x2p,y2p
		if dir_change[0]:
			x1 = x2p
			x2 = x1p
		if dir_change[1]:
			y1 = y2p
			y2 = y1p

		m = self.slope

		if m > 0:
			if y2  < y1:
				return 'top_left'
			else:
				return 'bottom_right'
		elif m < 0:
			if y2 < y1:
				return 'top_right'
			else: 
				return 'bottom_left'
		elif m == 0:
			if x2>x1:
				return 'right'
			else:
				return 'left'
		else:
			if y2 < y1:
				return 'top'
			else:
				return 'bottom'


	def in_frame(self,x,y):
		
		frame = self.frame
		dimn   = self.dimn
		# x,y - top left coordinates of the image
		if x < frame.left or x > (frame.width-dimn.width) or y < frame.top or y > (frame.height-dimn.height):
			return False
		else: 
			return True

	def visible(self,x1,y1,x2,y2,r):
		
		if (x1**2 + y1**2 -(2*(x1*x2+y1*y2)) + x2**2 + y2**2) < r**2:
			return True
		else:
			return False
	
	def far_move(self,max_step):

		frame = self.frame
		x1 = self.x1
		x2 = self.x2
		y1 = self.y1
		y2 = self.y2

		v1 = Vector(x1,y1)  # Prey
		v2 = Vector(x2,y2)  # Player
		
		## Player + Move Vector = Prey
		
		move_vector = v1-v2
		
		#print move_vector.vec
		dx,dy = max_step*(move_vector.dir)
		new_x,new_y = x1+dx,y1+dy
		
		return new_x, new_y

	def sphere_move(self,newX,newY):

		frame = self.frame
		width = frame.width
		height = frame.height

		new_x = newX%width
		new_y = newY%height

		return new_x,new_y


	def near_move(self,max_step):

		frame = self.frame
		x1 = self.x1
		x2 = self.x2
		y1 = self.y1
		y2 = self.y2
		m = self.slope
		direc = self.direction(x1,y1,x2,y2)

		if m != 'inf':
			x_move = math.sqrt(float(max_step)/(1+m**2))
			y_move = math.sqrt((float(max_step)*(m**2))/(1+m**2))
		else:
			x_move = 0.0
			y_move = max_step

		new_x,new_y = x1,y1
		if 'right' in direc:
			new_x = x1 + x_move
		if 'left' in direc:
			new_x = x1 - x_move
		if 'top' in direc:	
			new_y = y1 - y_move
		if 'bottom' in direc:
			new_y = y1 + y_move

		#if self.visible(x1,y1,x2,y2,300):
		return new_x,new_y
		#else:
		#	return x1,y1

if __name__ == '__main__':
	
	v1 = Vector(3,4)
	v2 = Vector(4,5)
	
	v3 = v1-v2
	print v3.vec