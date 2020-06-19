import pygame
import random

pygame.init()

# FPS
FPS = 120
clock = pygame.time.Clock()

#Разрешение экрана
D_Width = 1000
D_Height = 600
land = pygame.image.load("Fils\Img\Land.png")
display = pygame.display.set_mode((D_Width, D_Height))

pygame.mixer.music.load("Fils\Sound\BackGround.mp3")
RIP = pygame.mixer.Sound("Fils\Sound\Jump_RIP.wav")
Button_sound = pygame.mixer.Sound("Fils\Sound\Button.wav")

#Название
pygame.display.set_caption('Run dino, run!')

#Иконка
icon = pygame.image.load('Fils\Img\icon.jpg')
pygame.display.set_icon(icon)

#Dino
dino_Width = 80
dino_Height = 140
dino_x = D_Width // 6
dino_y = D_Height - dino_Height - 100

score = 0
img_counter = 3
Dino_image = [pygame.image.load('Fils\Img\Dino_1.png'), pygame.image.load('Fils\Img\Dino_2.png'), pygame.image.load('Fils\Img\Dino_3.png')]


def draw_dino():
    global img_counter
    if img_counter == 9:
        img_counter = 0
    display.blit(Dino_image[int(img_counter // 3)], (dino_x, dino_y))
    img_counter += 1


#Objeck
cactus_image = [pygame.image.load('Fils\Img\Cac_1.png'), pygame.image.load('Fils\Img\Cac_2.png'), pygame.image.load('Fils\Img\Cac_3.png')]
cactus_op = [40, 420, 50, 415, 45, 405]
radius = 0
class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed


    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False


    def return_cactus(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


def create_cactus(array):
    choice = random.randrange(0, 3)
    img = cactus_image[choice]
    width = cactus_op[choice * 2]
    height = cactus_op[choice * 2 + 1]
    array.append(Object(D_Width + 50, height, width, img, 5))

    choice = random.randrange(0, 3)
    img = cactus_image[choice]
    width = cactus_op[choice * 2]
    height = cactus_op[choice * 2 + 1]
    array.append(Object(D_Width + 700, height, width, img, 5))

    choice = random.randrange(0, 3)
    img = cactus_image[choice]
    width = cactus_op[choice * 2]
    height = cactus_op[choice * 2 + 1]
    array.append(Object(D_Width + 1450, height, width, img, 5))


def find_radius(array):
    maximum =  max(array[0].x, array[1].x, array[2].x)
    if maximum < D_Width:
        radius = D_Width
        if radius - maximum < 100:
            radius += 350
    else:
        radius = maximum
    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(40, 50)
    else:
        radius += random.randrange(350, 450)

    return radius


def draw_cactus(array):
    for Object in array:
        check = Object.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_image[choice]
            width = cactus_op[choice * 2]
            height = cactus_op[choice * 2 + 1]

            Object.return_cactus(radius, height, width, img)


cloud_img = [pygame.image.load('Fils\Img\oblaco_1.png'), pygame.image.load('Fils\Img\oblaco_2.png')]
stone_img = [pygame.image.load('Fils\Img\camen_1.png'), pygame.image.load('Fils\Img\camen_2.png')]


def open_obj():
    choice = random.randrange(0, 2)
    img_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_cloud = cloud_img[choice]

    stone = Object(D_Width, D_Height - 70, 7, img_stone, 5)
    cloud = Object(D_Width, 100, 230, img_cloud, 2)

    return stone, cloud


def move_obj(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_stone = stone_img[choice]
        stone.return_cactus(D_Width, 500 + random.randrange(10, 80), stone.width, img_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_cloud = cloud_img[choice]
        cloud.return_cactus(D_Width, random.randrange(0, 200), cloud.width, img_cloud)


#Прыжок
mate_jump = False
jump_counter = 30

def jamp():
   global dino_y, jump_counter, mate_jump
   if jump_counter >= -30:
       dino_y -= jump_counter / 3
       jump_counter -= 1
   else:
       jump_counter = 30
       mate_jump = False


#Text
def Print_text(message, x, y, font_color = (0, 0, 0), font_type = ('Fils\Other\8930.ttf'), font_size = 30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
  pause = True
  pygame.mixer.music.pause()
  while pause:
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
              pause = False


      Print_text("Пауза, нажмите ESC, чтобы продолжить", 295, 275)

      pygame.display.update()
      clock.tick(15)
  pygame.mixer.music.play()


# Collision
def check_collision(barriers):
    for barrier in barriers:
        if not mate_jump:
            if barrier.x <= dino_x + dino_Width - 15 <= barrier.x + barrier.width:
                return True
        if mate_jump:
            if jump_counter >= 0:
                if dino_y + dino_Height - 35 >= barrier.y:
                    if barrier.x <= dino_x + dino_Width - 40 <= barrier.x + barrier.width:
                        return True
            elif jump_counter <= -1:
                if dino_y + dino_Height - 10 >= barrier.y:
                    if barrier.x <= dino_x + dino_Width -35 <= barrier.x + barrier.width:
                        return True
            elif jump_counter <= -15:
                if dino_y + dino_Height - 35 >= barrier.y:
                    if barrier.x <= dino_x + dino_Width - 40 <= barrier.x + barrier.width:
                        return True
    return False


def game_over():
    global score
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                score = 0
                return True

            if keys[pygame.K_ESCAPE]:
                return False

        Print_text("GAME OVER, нажми Enter чтобы начать заново или ESC чтобы выйти", 205, 275)
        Print_text("Ваш счет: " + str(int(score)), 450, 305)

        pygame.display.update()
        clock.tick(15)


def RunGame():
   global mate_jump, score

   pygame.mixer.music.play(-1)

   game = True

   cactus_arr = []
   create_cactus(cactus_arr)

   stone, cloud = open_obj()
   while game:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               quit()
           keys = pygame.key.get_pressed()
           if keys[pygame.K_ESCAPE]:
               pause()
            
       keys = pygame.key.get_pressed()
       if keys[pygame.K_SPACE]:
           mate_jump = True

       if mate_jump:
           jamp()

       display.blit(land, (0, 0))

       score += 0.1
       Print_text("Очки: " + str(int(score)), 20, 10)

       draw_cactus(cactus_arr)
       draw_dino()
       move_obj(stone, cloud)

       if check_collision(cactus_arr):
          pygame.mixer.music.pause()
          pygame.mixer.Sound.play(RIP, 0)
          game = False
           

       #FPS
       pygame.display.update()
       clock.tick(FPS)


   return game_over()

while RunGame():
    pass
pygame.quit()
quit()
