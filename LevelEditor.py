import pygame
import os
import button
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Editor de Niveles')


#variables de juego 
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 67
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


#load images
one = pygame.image.load('./img/Background/plx-1.png').convert_alpha()
two = pygame.image.load('./img/Background/plx-2.png').convert_alpha()
three = pygame.image.load('./img/Background/plx-3.png').convert_alpha()
four = pygame.image.load('./img/Background/plx-4.png').convert_alpha()
five = pygame.image.load('./img/Background/plx-5.png').convert_alpha()

#almacenar imagenes en una lista
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'./img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('./img/save_btn.png').convert_alpha()
load_img = pygame.image.load('./img/load_btn.png').convert_alpha()


#Querido emiliano, si estas leyendo esto es porque sos grande, no se como se dice 
#te amo en aleman, pero supongo que se dice ich amech porque ich es yo 
#eniweis, ponete a hacer niveles a lo pendejo mi rey 
#animo
#lo amo, besitos

#Colorin colorado
FOREST_GREEN = (0, 92, 67)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)

#Matriz de nivel vacia
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

#Suelo
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0


#Texto en pantalla
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#fondito de bosque 
def draw_bg():
	screen.fill(FOREST_GREEN)
	width = one.get_width()
	scale = SCREEN_HEIGHT / width
	for x in range(5):
		screen.blit(pygame.transform.scale(one, (int(width * scale), SCREEN_HEIGHT)), (x * width * scale - scroll * 0.5, 0))
		screen.blit(pygame.transform.scale(two, (int(width * scale), SCREEN_HEIGHT)), (x * width * scale - scroll * 0.6, 0))
		screen.blit(pygame.transform.scale(three, (int(width * scale), SCREEN_HEIGHT)), (x * width * scale - scroll * 0.7, 0))
		screen.blit(pygame.transform.scale(four, (int(width * scale), SCREEN_HEIGHT)), (x * width * scale - scroll * 0.8, 0))
		screen.blit(pygame.transform.scale(five, (int(width * scale), SCREEN_HEIGHT)), (x * width * scale - scroll * 0.9, 0))


#grid 
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#dibujar el mundo
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))



#crear buttons
save_button = button.Button(SCREEN_WIDTH , SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH  + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
#lista de botones
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (50 * button_col) + 5, 50 * button_row + 5, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 6:
		button_row += 1
		button_col = 0


run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Nivel: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('ARRIBA o ABAJO para cambiar de nivel', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	#save and load data
	if save_button.draw(screen):
		#save level data
		with open(f'./levels/level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				writer.writerow(row)
		
	if load_button.draw(screen):
		#resetear al inicio del nivl
		scroll = 0
		with open(f'./levels/level{level}_data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)


	#dibujar 
	pygame.draw.rect(screen, FOREST_GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	#elegir tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#poner en rojo lo seleccionado
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	#scroll del mouse[ARREGLAR BUG CULERO]
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#agregar nuevos tiles a la pantalla
	#posicion del mouse
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	#revisazr si el mouse esta dentro de la pantalla
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#actualizar el valor de los tiles
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#inputs de teclado
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()

