import pygame
from pygame import mixer
import os
import csv
import button
import subprocess
import random
import ProyectoFinalCoso

import inspect

clases = inspect.getmembers(ProyectoFinalCoso, inspect.isclass)
nombres_clases = [nombre for nombre, _ in clases]
print(nombres_clases)


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

mixer.init()
pygame.init()

#set cuadros por segundodw
clock = pygame.time.Clock()
FPS = 60

#variables de ventana
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

#variables de juego
GRAVEDAD = 0.65
Rows = 16
Columns = 150
NMAX_NIV = 3
TILE_SZ = SCREEN_HEIGHT // Rows
Tyle_types = 67
Level = 0
screen_scroll = 0
SCROLL_THRESH = 200
bg_scroll = 0
start_game = False
start_intro = False

#variables de jugador
munin = 0
granadin = 0
salin = 0




#ventana
ventana = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

degustadores = ['Kevin' , 'Walther' , 'Emiliano', 'Alberth' , 'Wilmer']
#numero random de 0 a 3
randoms = random.randint(0, 3)
pygame.display.set_caption('La aventura de ' + degustadores[randoms])

#variables de accion
moviendose_izq = False
moviendose_der = False
disparando = False
grenade = False
Gran_Lanzada = False

#musica y sonidos
pygame.mixer.music.load('./Audio/music.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1, 0.0, 5000)
daño_fx = pygame.mixer.Sound('./Audio/Auch.mp3')
daño_fx.set_volume(0.05)

granada_fx = pygame.mixer.Sound('./Audio/Boom.mp3')
granada_fx.set_volume(0.2)

disparo_fx = pygame.mixer.Sound('./Audio/Pew.mp3')
disparo_fx.set_volume(0.15)

muerte_fx = pygame.mixer.Sound('./Audio/Muerte.mp3')
muerte_fx.set_volume(0.05)

cuchillo_fx = pygame.mixer.Sound('./Audio/Cuchillo.mp3')
cuchillo_fx.set_volume(0.1)


#imagenes botones
boton_start = pygame.image.load('./img/start_btn.png').convert_alpha()
boton_start = pygame.transform.scale(boton_start, (200, 100))
boton_editor = pygame.image.load('./img/lvled_btn.png').convert_alpha()
boton_editor = pygame.transform.scale(boton_editor, (200, 100))
boton_exit = pygame.image.load('./img/exit_btn.png').convert_alpha()
boton_exit = pygame.transform.scale(boton_exit, (200, 100))
boton_restart = pygame.image.load('./img/restart_btn.png').convert_alpha()
boton_restart = pygame.transform.scale(boton_restart, (200, 100))
#cargar imagenes
bg_one = pygame.image.load('./img/Background/plx-1.png').convert_alpha()
bg_two = pygame.image.load('./img/Background/plx-2.png').convert_alpha()
bg_three = pygame.image.load('./img/Background/plx-3.png').convert_alpha()
bg_four = pygame.image.load('./img/Background/plx-4.png').convert_alpha()
bg_five = pygame.image.load('./img/Background/plx-5.png').convert_alpha()
#tiles en una lista
img_list = []
for x in range(Tyle_types):
    img = pygame.image.load(f'./img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SZ, TILE_SZ))
    img_list.append(img)
#balas
bullet_img = pygame.image.load('./img/icons/bullet.png').convert_alpha()  #cambiar por la imagen de la bala
cuchillo_imgg = pygame.image.load('./img/icons/knife.png').convert_alpha()
#granadas
grenade_img = pygame.image.load('./img/icons/grenade.png').convert_alpha()  
#items
salud_img = pygame.image.load('./img/icons/health_box.png').convert_alpha() 
municion_img = pygame.image.load('./img/icons/ammo_box.png').convert_alpha() 
granadas_img = pygame.image.load('./img/icons/grenade_box.png').convert_alpha() 
cuchillo_img = pygame.image.load('./img/icons/knife (2).png').convert_alpha()

item_list = {
    'Salud'    : salud_img,
    'Municion'  : municion_img,
    'Granada'  : granadas_img,
    'Cuchillo' : cuchillo_img
}



def draw_txt(text,font,tect_col,x,y):
    img = font.render(text, True,tect_col)
    ventana.blit(img, (x,y)) 

def draw_bg():
    ventana.fill((146, 244, 255))
    width = ventana.get_width()  # Obtener el ancho de la ventana
    height = ventana.get_height()  # Obtener el alto de la ventana

    # Escalar las imágenes a la altura de la pantalla
    bg_one_scaled = pygame.transform.scale(bg_one, (width, height))
    bg_two_scaled = pygame.transform.scale(bg_two, (width, height))
    bg_three_scaled = pygame.transform.scale(bg_three, (width, height))
    bg_four_scaled = pygame.transform.scale(bg_four, (width, height))
    bg_five_scaled = pygame.transform.scale(bg_five, (width, height))

    for x in range(4):
        ventana.blit(bg_one_scaled, ((x * width) - bg_scroll * 0.5, 0))
        ventana.blit(bg_two_scaled, ((x * width) - bg_scroll * 0.6, 0))
        ventana.blit(bg_three_scaled, ((x * width) - bg_scroll * 0.7, 0))
        ventana.blit(bg_four_scaled, ((x * width) - bg_scroll * 0.8, 0))
        ventana.blit(bg_five_scaled, ((x * width) - bg_scroll * 0.9, 0))

#hacer reset del nivel
def reset_level():
    grupo_balas.empty()
    grupo_granadas.empty()
    grupo_explosiones.empty()
    grupo_enemigos.empty()
    grupo_item_list.empty()
    grupo_deco.empty()
    grupo_agua.empty()
    grupo_salida.empty()
    grupo_spikes.empty()
    grupo_lava.empty()

    #CREAR NIVEL VACIO
    Data = []
    for row in range(Rows):
        r = [-1] * Columns
        Data.append(r)

    return Data





#fuente
font = pygame.font.SysFont('Futura', 30)

WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
PINK = (255,200,200)
GREEN = (0,255,0)

#botones centrados segun screen heigh y width
start_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200, boton_start, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, boton_exit, 1)
editor_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, boton_editor, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, boton_restart, 1)
#grupos de sprite
grupo_balas = pygame.sprite.Group()
grupo_granadas = pygame.sprite.Group()
grupo_explosiones = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_item_list = pygame.sprite.Group() 
grupo_deco = pygame.sprite.Group()
grupo_agua = pygame.sprite.Group()
grupo_salida = pygame.sprite.Group()
grupo_spikes = pygame.sprite.Group()
grupo_lava = pygame.sprite.Group()

#clase item
class item(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_list[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SZ//2 , y + (TILE_SZ - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        #colisiones (pick box)
        if pygame.sprite.collide_rect(self, J1):
            if self.item_type == 'Salud':
                J1.salud += 30
                if J1.salud > J1.sal_max:
                    J1.salud = J1.sal_max
            elif self.item_type == 'Municion':
                J1.mun += 10
            elif self.item_type == 'Granada':
                J1.granad += 2
            elif self.item_type == 'Cuchillo':
                J1.cuchillo = True
                cuchillo_fx.play()

            #borrar
            self.kill()

#Clase barra vida
class BarraVida():
    def __init__(self, x, y,  salud, salud_max):
        self.x = x
        self.y = y
        self.salud = salud
        self.salud_max = salud_max

    def draw(self, salud):
        #actualizar con nueva salud
        self.salud = salud
        #calcular radio de vida
        radio_vida = (self.salud / self.salud_max)

        #dibujar barra de vida
        pygame.draw.rect(ventana, BLACK, (self.x - 2 , self.y - 2 , 154, 24))
        pygame.draw.rect(ventana, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(ventana, GREEN, (self.x, self.y, 150 * radio_vida, 20))

class Agua(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SZ // 2, y + (TILE_SZ - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(J1, self):
            if J1.rect.bottom >= (self.rect.top + (self.rect.height / 2)):
                J1.vel = 2
            else:
                J1.vel = 5
        


class Lava(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SZ // 2, y + (TILE_SZ - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll
        #hacer daño luego de cierto tiempo
        if pygame.sprite.collide_rect(J1, self):
            J1.salud -= 0.5
            if J1.rect.bottom >= self.rect.top + (self.rect.height / 2):
                J1.vel = 0.6
                J1.salud -= 0.7
            else:
                J1.vel = 5

class spikes(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SZ // 2, y + (TILE_SZ - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        #hacer daño si se toca
        if pygame.sprite.collide_rect(self, J1):
            J1.salud -= 0.5
            daño_fx.play()




class Salida(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SZ // 2, y + (TILE_SZ - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll




#clase balas
class balas(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #mover la bala
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #chequear si la bala sale de la pantalla
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #colision con nivel
        for tile in mundo.list_obstacl:
            if tile[1].colliderect(self.rect):
                self.kill()

        #colisiones con personajes 
        if pygame.sprite.spritecollide(J1, grupo_balas, False):
            if J1.vive:
                J1.salud -= 25
                daño_fx.play()
                self.kill()

        for enemig in grupo_enemigos:
            if pygame.sprite.spritecollide(enemig, grupo_balas, False):
                if enemig.vive:
                    enemig.salud -= 25
                    self.kill()


class Cuchillo(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12
        self.image = cuchillo_imgg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #mover la bala
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #chequear si la bala sale de la pantalla
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #colision con nivel
        for tile in mundo.list_obstacl:
            if tile[1].colliderect(self.rect):
                self.kill()

        for enemig in grupo_enemigos:
            if pygame.sprite.spritecollide(enemig, grupo_balas, False):
                if enemig.vive:
                    enemig.salud -= 100
                    self.kill()

        



#clase granadas
class BOOMgran(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.tiempo = 100
        self.vel = -10
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #mover la granada
        self.vel += GRAVEDAD
        dx = self.direction * self.speed
        dy = self.vel
        #colisiones con nivel
        for tile in mundo.list_obstacl:
            #colisiones en x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                self.direction *= -1
                dx = self.direction * self.speed
            #colisiones en y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                self.speed = 0
                #chequear si esta debajo del suelo
                if self.vel < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel = 0
                #chequear si esta arriba del suelo
                elif self.vel >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel = 0
                
        #actualizar posixion de la granada
        self.rect.x += dx + screen_scroll
        self.rect.y += dy
        #chequear si la granada sale de la pantalla
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed
        #tiempo de explosion
        self.tiempo -= 1
        if self.tiempo <= 0:
            self.kill()
            explosion = Explosiones(self.rect.x, self.rect.y, 3)
            grupo_explosiones.add(explosion)
            granada_fx.play()
            #daño por explosion
            if abs(self.rect.centerx - J1.rect.centerx) < TILE_SZ * 2 and\
                abs(self.rect.centery - J1.rect.centery) < TILE_SZ * 2:
                J1.salud -= 50
            for enemig in grupo_enemigos:
                if abs(self.rect.centerx - enemig.rect.centerx) < TILE_SZ * 2 and\
                    abs(self.rect.centery - enemig.rect.centery) < TILE_SZ * 2:
                    enemig.salud -= 50




#clase explosiones
class Explosiones(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'./img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.contador = 0   

    def update(self):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        #update explosion anim
        self.contador += 1
        if self.contador >= EXPLOSION_SPEED:
            self.contador = 0
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]


#clase jugador
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, escala ,char_type , vel, mun, granad):
        super().__init__()
        self.vive = True
        self.vel = vel
        self.mun = mun
        self.mun_inicial = mun
        self.espera = 0
        self.granad = granad
        self.granad_inc = granad
        self.cuchillo = False
        self.salud = 100
        self.sal_max = self.salud
        self.char_type = char_type
        self.direccion = 1
        self.vel_y = 0
        self.salto = False
        self.saltando = True
        self.flip = False
        self.animation_list = []
        self.accion=0
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        list_temp = []

        self.move_counter = 0
        self.endescanso = False
        self.endescanso_counter = 0
        self.campo_vision = pygame.Rect(0, 0, 150, 20)

        self.munin = 0
        self.granadin = 0
        self.salin = 0


        #recargar imagenes
        tiposAnimaciones = ['Idle', 'Run', 'Jump', 'Death']
        for tipo in tiposAnimaciones:
            #resetear la lista de imagenes
            list_temp = []
            #numero de archivos en la carpeta
            framesencarpeta = len(os.listdir(f'./img/{self.char_type}/{tipo}'))
            for i in range(framesencarpeta):
                img = pygame.image.load(f'./img/{self.char_type}/{tipo}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (36, img.get_height() * escala -10))
                list_temp.append(img)
            self.animation_list.append(list_temp)

        self.image = self.animation_list[self.accion][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self):
        #hacer update a la anim
        self.update_animation()
        self.verif_vivo()
        self.verif_caido()
        #espera
        if self.espera > 0:
            self.espera -= 1

    def move(self, moviendose_izq, moviendose_der):
        #variables de movimiento
        Screen_scroll = 0
        dx = 0
        dy = 0

        #asignar variables de movimiento
        if moviendose_izq:
            dx = -self.vel
            self.flip = True
            self.direccion = -1
        if moviendose_der:
            dx = self.vel
            self.flip = False
            self.direccion = 1
        
        #salto
        if self.salto == True and self.saltando == False:
            self.vel_y = -13
            self.salto = False 
            self.saltando = True


        #gravedad
        self.vel_y += GRAVEDAD
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y  

        
        #chequear colisiones
        for tile in mundo.list_obstacl:
            #colisiones en x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direccion *= -1
                    self.move_counter = 0
            #colisiones en y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                #chequear si esta debajo del suelo
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #chequear si esta arriba del suelo
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.saltando = False
                    dy = tile[1].top - self.rect.bottom
                    
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0  
        

        #actualizar la posicion
        self.rect.x += dx
        self.rect.y += dy

        
        #actualizar scroll
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (mundo.leveL_LNG * TILE_SZ) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                Screen_scroll = -dx

        #colision con salida
        level_complete = False
        if pygame.sprite.spritecollide(self, grupo_salida, False):
            level_complete = True

            
        return Screen_scroll, level_complete


    def disparar(self):
        if self.espera == 0 and self.mun > 0:
            self.espera = 20
            balaa = balas(self.rect.centerx + (0.75 * self.rect.size[0] * self.direccion), self.rect.centery, self.direccion)
            grupo_balas.add(balaa)  
            self.mun -= 1
            disparo_fx.play()

    def lanzar_cuchillo(self):  
        if self.cuchillo == True:
            cuchillo = Cuchillo(self.rect.centerx + (0.75 * self.rect.size[0] * self.direccion), self.rect.centery, self.direccion)
            grupo_balas.add(cuchillo)
            self.cuchillo = False

    #verificar si cayo del suelo del mundo
    def verif_caido(self):
        if self.rect.bottom > SCREEN_HEIGHT + 5:
            self.vive = False
            self.update_accion(3)
            
      
        
    
    def update_animation(self):
        COOLDOWN_ANIMACION = 100
        #hacer update a la anim
        self.image = self.animation_list[self.accion][self.index]
        #ver el tiempo pasado desde la ultima actualizacion
        if pygame.time.get_ticks() - self.update_time > COOLDOWN_ANIMACION:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        #si la animacion se acaba, resetearla
        if self.index >= len(self.animation_list[self.accion]):
            if self.accion == 3:
                self.index = len(self.animation_list[self.accion]) - 1
            else:
                self.index = 0
        

    def update_accion(self, nueva_accion):
        #chequear si la nueva accion es diferente a la anterior
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            #actualizar el frame de la animacion y el tiempo
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def verif_vivo(self):
        if self.salud <= 0:
            self.salud = 0
            self.vel = 0
            self.vive = False
            self.update_accion(3)#muerte

    def controlenemigos(self):
        if self.vive and J1.vive:
            if random.randint(1, 200) == 1 and self.endescanso == False:
                self.update_accion(0)
                self.endescanso = True
                self.endescanso_counter = 50
            if self.campo_vision.colliderect(J1.rect):
                self.update_accion(0)
                self.disparar()
            else:
                if self.endescanso == False:
                    if self.direccion == 1:
                        ai_moviendose_der = True
                    else:
                        ai_moviendose_der = False
                    ai_moviendose_izq = not ai_moviendose_der
                    self.move(ai_moviendose_izq, ai_moviendose_der)
                    self.update_accion(1)

                    self.move_counter += 1
                    self.campo_vision.center = (self.rect.centerx + 75 * self.direccion, self.rect.centery)
                    #dibujar campo de vision

                    if self.move_counter > TILE_SZ:
                        self.direccion *= -1
                        self.move_counter *= -1
                else:
                    self.endescanso_counter -= 1
                    if self.endescanso_counter <= 0:
                        self.endescanso = False

        #scroll
        self.rect.x += screen_scroll
        

    
    def draw(self):
        ventana.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 

class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0


	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:#whole screen fade
			pygame.draw.rect(ventana, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(ventana, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(ventana, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(ventana, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
		if self.direction == 2:#vertical screen fade down
			pygame.draw.rect(ventana, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= SCREEN_WIDTH:
			fade_complete = True

		return fade_complete


#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)



class Decoracion(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SZ // 2, y + (TILE_SZ - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll
        


class Mundo():
    def __init__(self):
        self.list_obstacl = []

    def procesar_mundo(self, datos):
        self.leveL_LNG = len(datos[0])
        for y, row in enumerate(datos):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SZ
                    img_rect.y = y * TILE_SZ
                    tile_data = (img, img_rect)

                    if (tile >= 0 and tile <= 8) or (tile >= 57 and tile <= 61) or (tile == 12 or tile == 13):
                        self.list_obstacl.append(tile_data)

                    elif tile >= 9 and tile <= 10:#agua
                        agua = Agua(img, x * TILE_SZ, y * TILE_SZ)
                        grupo_agua.add(agua)
                        #crear un rectangulo con colision debajo del tile del rectangulo del agua para que se pueda nadar 
                        img = img_list[Tyle_types-1]
                        tile_data = ((img), pygame.Rect(x * TILE_SZ, (y+1) * TILE_SZ, TILE_SZ, TILE_SZ))  
                        self.list_obstacl.append(tile_data)

                    elif (tile >= 14 and tile <= 18) or (tile >= 27 and tile <= 35) or (tile >= 62 and tile <= 64) or (tile >= 40 and tile <= 56) or (tile == 26 or tile == 39) or (tile >=62 and tile <= 64) or (tile == 11):#decoraciones
                        decoracion = Decoracion(img, x * TILE_SZ, y * TILE_SZ)
                        grupo_deco.add(decoracion)
                    elif tile == 21:#crear caja de municion
                        item_box = item('Municion', x * TILE_SZ, y * TILE_SZ)
                        grupo_item_list.add(item_box)
                    elif tile == 22:#crear caja de granadas
                        item_box = item('Granada', x * TILE_SZ, y * TILE_SZ)
                        grupo_item_list.add(item_box)
                    elif tile == 23:#crear caja de salud
                        item_box = item('Salud', x * TILE_SZ, y * TILE_SZ)
                        grupo_item_list.add(item_box)
                    elif tile == 66:#crear cuchillo
                        item_box = item('Cuchillo', x * TILE_SZ, y * TILE_SZ)
                        grupo_item_list.add(item_box)
                    elif tile == 24:#crear salida
                        salida = Salida(img, x * TILE_SZ, y * TILE_SZ)
                        grupo_salida.add(salida)
                    elif tile == 25:#crear spikes
                        spike = spikes(img, x * TILE_SZ, y * TILE_SZ)
                        grupo_spikes.add(spike)
                    elif tile == 36 or tile == 37:#crear lava
                        lava = Lava(img, x * TILE_SZ, y * TILE_SZ)
                        grupo_lava.add(lava)

                        #crear un rectangulo con colision abajo del rectangulo del agua para que se pueda nadar 
                        img = img_list[Tyle_types-1]
                        tile_data = ((img), pygame.Rect(x * TILE_SZ, (y+1) * TILE_SZ, TILE_SZ, TILE_SZ))  
                        self.list_obstacl.append(tile_data)

                    elif tile == 19:#crear jugador    
                        if Level > 0:
                            J1 = Entity(x * TILE_SZ, y * TILE_SZ, 1.65, 'player', 10, munin, granadin)
                            J1.salud = salin
                            BarraVid = BarraVida(10, 10, J1.salud, J1.sal_max)
                        else:
                            J1 = Entity(x * TILE_SZ, y * TILE_SZ, 1.65, 'player', 10, 30, 5)
                            BarraVid = BarraVida(10, 10, J1.salud, J1.sal_max)
                    elif tile == 20:#crear enemigos
                        enemig = Entity(x * TILE_SZ, y * TILE_SZ, 1.65, 'enemy', 2, 20, 0)
                        grupo_enemigos.add(enemig)
        
        return J1, BarraVid

    def draw(self):
        for tile in self.list_obstacl:
            tile[1][0] += screen_scroll
            ventana.blit(tile[0], tile[1])

    
    

    



#CREAR NIVEL VACIO
mundo_DTA = []
for row in range(Rows):
    r = [-1] * Columns
    mundo_DTA.append(r)

#cargar nivel y crear mundo
with open(f'./levels/level{Level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            mundo_DTA[x][y] = int(tile)

mundo = Mundo()
J1 , BarraVid = mundo.procesar_mundo(mundo_DTA)





#gameloop
running = True
while running:

    clock.tick(FPS)
    if start_game == False:
        ventana.fill((18, 55, 42))
        #botones
        if start_button.draw(ventana):
            start_game = True
            start_intro = True

        if exit_button.draw(ventana):
            running = False

        if editor_button.draw(ventana):
            #iniciar el level editor
            subprocess.call('python LevelEditor.py', shell=True)
    else:
        draw_bg()

        #dibujar barra de vida
        BarraVid.draw(J1.salud)

        #municion
        draw_txt('Municion: ', font, WHITE, 10,35)
        for x in range(J1.mun):
            ventana.blit(bullet_img, (110 + (x *10), 40))
        draw_txt('Granadas: ', font, WHITE, 10,60)
        for x in range(J1.granad):
            ventana.blit(grenade_img, (120 + (x *15), 65))

        #actualizar y dibujar mundo
        mundo.draw()

        #actualizar y dibujar los grupos
        # Updates
        grupo_balas.update()
        grupo_granadas.update()
        grupo_explosiones.update()
        grupo_item_list.update()
        grupo_deco.update()
        grupo_salida.update()
        grupo_agua.update()
        grupo_spikes.update()        
        grupo_lava.update()

        #Draws que van detrás del Jugador
        grupo_deco.draw(ventana)
        grupo_balas.draw(ventana)
        grupo_granadas.draw(ventana)
        grupo_explosiones.draw(ventana)
        grupo_item_list.draw(ventana)
        grupo_salida.draw(ventana)

        #Dibujar Jugador
        for enemig in grupo_enemigos:
            enemig.controlenemigos()
            enemig.draw()
            enemig.update()
        J1.draw()
        J1.update()

        #Draws que van en frente del Jugador
        grupo_agua.draw(ventana)
        grupo_spikes.draw(ventana)
        grupo_lava.draw(ventana)

        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        #actualizar acciones jugador 
        if J1.vive:
            if disparando:
                J1.disparar()  
            elif grenade and Gran_Lanzada == False and J1.granad > 0:
                granada = BOOMgran(J1.rect.centerx + (0.6 * J1.rect.size[0] * J1.direccion),\
                                J1.rect.top , J1.direccion)
                grupo_granadas.add(granada)
                Gran_Lanzada = True
                J1.granad -= 1
            if J1.saltando:
                J1.update_accion(2)  # 2 is for jumping.
            elif moviendose_izq or moviendose_der:
                J1.update_accion(1)  # 1 is for running.
            else:
                J1.update_accion(0)

            screen_scroll, level_complete = J1.move(moviendose_izq, moviendose_der)
            bg_scroll -= screen_scroll
            J1.update_animation()  # Update animation.

            if level_complete:
                start_intro = True
                munin = J1.mun
                granadin = J1.granad
                salin = J1.salud

                Level += 1
                bg_scroll = 0
                mundo_DTA = reset_level()
                if Level <= NMAX_NIV:
                    #cargar nivel y crear mundo
                    with open(f'./levels/level{Level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                mundo_DTA[x][y] = int(tile)

                    mundo = Mundo()
                    J1 , BarraVid = mundo.procesar_mundo(mundo_DTA)
        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(ventana):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    mundo_DTA = reset_level()
                    #cargar nivel y crear mundo
                    with open(f'./levels/level{Level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                mundo_DTA[x][y] = int(tile)

                    mundo = Mundo()
                    J1 , BarraVid = mundo.procesar_mundo(mundo_DTA)








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #presses de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moviendose_izq = True
            if event.key == pygame.K_d:
                moviendose_der = True
            if event.key == pygame.K_SPACE:
                disparando = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and J1.vive == True:
                J1.salto = True
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_e:
                J1.lanzar_cuchillo()

        #releases de teclado
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moviendose_izq = False
            if event.key == pygame.K_d:
                moviendose_der = False
            if event.key == pygame.K_SPACE:
                disparando = False
            if event.key == pygame.K_q:
                grenade = False
                Gran_Lanzada = False
            if event.key == pygame.K_e:
                J1.cuchillo = False
             
            

    pygame.display.update()



