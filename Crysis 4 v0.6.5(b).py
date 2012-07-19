# -*- coding: UTF-8 -*-
import pygame, os
pygame.init ()

def load_image(name):
   fullname = os.path.join('pics',name)
   i=pygame.image.load(fullname)
   return i.convert_alpha()

def platform_func(x_speed):#Стены
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
   if gravity > 0:
       if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) <> (empty) or level.get_at(((x_cord)/32, (y_cord+32)/32)) <> (empty):
          return 0
       return 16
   if gravity < 0:#Для прыжка
       if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) <> (empty) and level.get_at(((x_cord+16)/32, (y_cord-32)/32)) <> (empty):
          return 0
       if level.get_at(((x_cord)/32, (y_cord+32)/32)) <> (empty) and level.get_at(((x_cord)/32, (y_cord-32)/32)) <> (empty):
          return 0
       if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) <> (empty) and level.get_at(((x_cord)/32, (y_cord-32)/32)) <> (empty):
          return 0
       if level.get_at(((x_cord)/32, (y_cord+32)/32)) <> (empty) and level.get_at(((x_cord+16)/32, (y_cord-32)/32)) <> (empty):
          return 0
       if level.get_at(((x_cord+16)/32, (y_cord-32)/32)) <> (empty) or level.get_at(((x_cord)/32, (y_cord-32)/32)) <> (empty):
          return 16
       return -32

def jump( gravity):#Прыжок
   global jump_height, jump_trigger
   if gravity > 0:
      jump_trigger = False
   if  gravity == 0:
      jump_height = 0
   if jump_trigger == True and jump_height < 3:
      jump_height += 1
      return -32
   return 16

def corner_stop(x_speed, gravity):#Исправляет баг с углом
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
         screen.blit(player, (x, y), (0,0,32,32))
      elif gravity > 0:
         screen.blit(player, (x, y), (0,33,32,32))
   global N
   if x_speed > 0:
      if gravity == 0:
         if N==1: screen.blit(player, (x, y), (33,0,32,32))
         elif N==2: screen.blit(player, (x, y), (65,0,32,32))
         elif N==3: screen.blit(player, (x, y), (93,0,32,32))
      elif gravity <> 0:
         screen.blit(player, (x, y), (33,0,32,32))
   if x_speed < 0:
      if gravity == 0:
         if N==1: screen.blit(player, (x, y), (33,33,32,32))
         elif N==2: screen.blit(player, (x, y), (65,33,32,32))
         elif N==3: screen.blit(player, (x, y), (93,33,32,32))
      elif gravity <> 0:
         screen.blit(player, (x, y), (33,33,32,32))
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
   if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) == (255,0,0):
      HP -= 5

def Lava():
   global HP
   if level.get_at(((x_cord+16)/32, (y_cord+32)/32)) == (255,128,0):
      HP -= 20
   if level.get_at(((x_cord+32)/32, (y_cord)/32)) == (255,128,0):
      HP -= 20
   if level.get_at(((x_cord-16)/32, (y_cord)/32)) == (255,128,0):
      HP -= 20

def draw_stats():
     HPstat = Stats_font.render("%d" % HP,0, (255,255,255))
     Keystat = Stats_font.render("%d" % Keys,0, (255,255,255))
     screen.blit(Heart_image,(10, 448))
     screen.blit(HPstat,(30, 448))
     screen.blit(Key_image,(10, 424))
     screen.blit(Keystat,(30, 424))

def Dead():
   if HP <= 0:
     dead = Message_font.render("You died!",0, (255,255,255))
     message = Stats_font.render("press x to restart" ,0, (255,255,255))
     screen.fill((0,0,0))
     screen.blit(dead,(210, 200))
     screen.blit(message,(205, 460))
     if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_x: 
            Load_level(lvl)

def  Pick_key():
   global Keys, key_list,camera
   for i in key_list:
     camera.blit(GameKey,i)
     if (x_cord, y_cord) == i:
        Keys += 1
        del key_list[key_list.index((x_cord, y_cord))]

def next_level(key_list):
   global lvl
   if key_list == [] and level.get_at(((x_cord+16)/32, (y_cord-16)/32)) == (200,170,8):
      lvl += 1
      Load_level(lvl)

def Load_level(lvl):
   global level, camera, Keys, HP,key_list, x_cord, y_cord 
   level = load_image("lvl%d.png" % lvl)
   camera = load_image("background%d.png" % lvl)
   HP=100
   Keys = 0
   key_list = list_of_lock[lvl]
   x_cord, y_cord = list_of_cords[lvl]



#____________________________________
screen = pygame.display.set_mode([640, 480])
pygame.display.set_caption('Crysis 4')

lvl=1
list_of_lock =[[],[(1248,1090),(384,1058),(1728,802),(1984,642)],[(1216,416),(960,1120),(1920,1056)]]
key_list = list_of_lock[lvl]
GameKey = load_image("GameKey.png" )
HP=100
Keys = 0
Stats_font = pygame.font.Font("JFRocSol.ttf", 18)
Message_font = pygame.font.Font("JFRocSol.ttf", 36)

clock = pygame.time.Clock()
camera = load_image("background%d.png" % lvl)
level = load_image("lvl%d.png" % lvl)

Heart_image = load_image("Heart.png")
Key_image = load_image("key_stats.png")

empty = (0, 0, 0)

#Скорость в пикселях за кадр
x_speed = 0
gravity = 16
#Начальные корды
x_cord, y_cord = 704, 258
list_of_cords = [(0,0),(704, 258),(320, 256)]

jump_trigger = True
jump_height = 0

N=1
player = load_image("player.png" )

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
    Lava()
    next_level(key_list)

    print key_list,x_cord, y_cord
    x_cord += x_speed
    y_cord += gravity

    screen.blit(camera,(0,0), cam)
    draw_player(320, 240)
    draw_stats()
    Dead()
    Pick_key()

    pygame.display.flip()
    clock.tick(20)