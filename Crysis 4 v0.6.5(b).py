# -*- coding: UTF-8 -*-
import pygame, os
pygame.init ()

def load_image(name):
   fullname = os.path.join('pics',name)
   i=pygame.image.load(fullname)
   return i.convert_alpha()

def platform_func(x_speed):#Стены
   global level
   if x_speed > 0:
        if level.get_at(((x_cord+32)/32, (y_cord+16)/32)) <> (empty):
          return 0
        return 16
   if x_speed < 0:
        if level.get_at(((x_cord-16)/32, (y_cord+16)/32)) <> (empty):
          return 0
        return -16
   if x_speed == 0:return 0

def gravity_func(gravity):#Гравитация
   global level
   if gravity == 0:
      if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) <> i:
           return 0
      return 16
   if gravity > 0:
       if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) <> (empty) or level.get_at(((x_cord)/32, (y_cord+32)/32)) <> (empty):
          return 0
       return 16
   if gravity < 0:#Для прыжка
       if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) <> (empty) and level.get_at(((x_cord+16)/32, (y_cord-32)/32)) <> (empty):
          return 0
       if level.get_at(((x_cord)/32, (y_cord+32)/32)) <> (empty) and level.get_at(((x_cord)/32, (y_cord-32)/32)) <> (empty):
          return 0
       if level.get_at(((x_cord+16)/32, (y_cord-32)/32)) <> (empty) or level.get_at(((x_cord)/32, (y_cord-32)/32)) <> (empty):
          return 16
       return -32

def jump( gravity):#Прыжок
   global jump_height, jump_trigger
   if gravity > 0:
      jump_trigger = False
   if  gravity == 0:#Алгоритм неочень, 
      jump_height = 0#тормозит слегка, но работает
   if jump_trigger == True and jump_height < 3:
      jump_height += 1
      return -32
   return 16

def corner_stop(x_speed, gravity):#Исправляет баг с углом
   global level
   if gravity > 0:
     if x_speed > 0:
       if level.get_at(((x_cord+32)/32, (y_cord+32)/32)) <> (empty):
         return 0
       return x_speed
     if x_speed < 0:
       if level.get_at(((x_cord-16)/32, (y_cord+32)/32)) <> (empty):
         return 0
       return x_speed
   if gravity < 0:
     if x_speed > 0:
       if level.get_at(((x_cord+32)/32, (y_cord-32)/32)) <> (empty):
         return 0
       return x_speed
     if x_speed < 0:
       if level.get_at(((x_cord-16)/32, (y_cord-32)/32)) <> (empty):
         return 0
       return x_speed
   return x_speed

def draw_player( x, y):#Функция отрисовки перса
   if x_speed == 0:
      if gravity <= 0:
         player = p0
      if gravity > 0:
         player = p10
   global N
   if x_speed > 0:
      if N==1: player = p1
      elif N==2: player = p2
      elif N==3: player = p3
   if x_speed < 0:
      if N==1: player = p4
      elif N==2: player = p5
      elif N==3: player = p6
   screen.blit(player, (x, y))
   N += 1
   if N >3: N=1

def camera_move(x,y,speed, gravity):
   if speed <> 0:
     return (x-320,y-240,640,480)
   elif speed == 0:
      return (x-320,y-240,640,480)
   if gravity <> 0:
     return (x-320,y-240,640,480)

def Spike():
   global HP
   if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) == (255,0,0) or level.get_at(((x_cord-16)/32, (y_cord+32)/32)) == (255,0,0):
      HP -= 1


#def Portal():
#   if level.get_at(((x_cord+16)/32, (y_cord-32)/32)) == (200,170,8):
#      print "Fuck Yeah!"

def draw_stats():
     HPstat = Stats_font.render("%d" % HP,0, (255,255,255))
     Keystat = Stats_font.render("%d" % Keys,0, (255,255,255))
     screen.blit(Heart_image,(5, 448))
     screen.blit(HPstat,(25, 448))
     screen.blit(Key_image,(5, 424))
     screen.blit(Keystat,(25, 424))

def Dead():
   if HP <= 0:
     dead = Message_font.render("You die!",0, (255,255,255))
     screen.fill((0,0,0))
     screen.blit(dead,(230, 200))

def  Pick_key():
   global Keys, key_list
   for i in key_list:
     camera.blit(GameKey,i)
     if (x_cord, y_cord) == i:
        Keys += 1
        del key_list[key_list.index((x_cord, y_cord))] 
#        camera.fill((0, 0, 0))


def next_level(key_list):
   global lvl, camera, Keys, HP
   if key_list == [] and level.get_at(((x_cord+16)/32, (y_cord-32)/32)) == (200,170,8):
      print "Fuck Yeah!"
      lvl = 3
      camera = load_image("3background.png" )
      HP=100
      Keys = 0
      key_list =[(320,706),(352,706)]
#____________________________________
screen = pygame.display.set_mode([640, 480])
pygame.display.set_caption('Crysis 4')

camera = load_image("1background.png" )

key_list =[(320,706),(352,706)]
GameKey = load_image("GameKey.png" )
HP=100
Keys = 0
lvl=2
Stats_font = pygame.font.Font("JFRocSol.ttf", 18)
Message_font = pygame.font.Font("JFRocSol.ttf", 36)

clock = pygame.time.Clock()
level = load_image("lvl%d.png" % lvl)

Heart_image = load_image("Heart.png")
Key_image = load_image("key_stats.png")

empty = (0, 0, 0)
blue = (0,0,255)
green = (0,255,0)

#Скорость в пикселях за кадр
x_speed = 0
gravity = 16
#Начальные корды
x_cord = 704
y_cord = 258

jump_trigger = True
jump_height = 0

N=1
p10 = load_image("player10.png" )
p0 = load_image("player0.png" )
p1 = load_image("Rplayer1.png" )
p2 = load_image("Rplayer2.png" )
p3 = load_image("Rplayer3.png" )
p4 = load_image("Lplayer1.png" )
p5 = load_image("Lplayer2.png" )
p6 = load_image("Lplayer3.png" )

done=False
while done == False:
    for event in pygame.event.get():
     if event.type == pygame.QUIT:
      done = True

     if event.type == pygame.KEYDOWN:#Кнопка нажата, движение
         if event.key == pygame.K_LEFT: x_speed =-16
         if event.key == pygame.K_RIGHT: x_speed = 16
         if event.key == pygame.K_UP: jump_trigger = True
     if event.type == pygame.KEYUP:# Кнопка отпущена, движение прекращается
         if event.key == pygame.K_LEFT: x_speed = 0
         if event.key == pygame.K_RIGHT: x_speed = 0


    gravity =jump( gravity)
    x_speed = platform_func(x_speed)
    gravity = gravity_func(gravity)
    x_speed=corner_stop(x_speed, gravity)
    cam = camera_move( x_cord, y_cord, x_speed, gravity)
    Spike()
    next_level(key_list)
#    Dead()
#    Portal()
    print HP,key_list,lvl

    x_cord += x_speed
    y_cord += gravity

    screen.blit(camera,(0,0), cam)
    draw_player(320, 240)
    draw_stats()
    Dead()
    Pick_key()

    pygame.display.flip()
    clock.tick(20)