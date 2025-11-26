from pygame import Rect

ground = Rect(10,350,700,30)
wall = Rect(350,300, 30,30)

shaolin = Actor('shaolin')
shaolin.pos = 100, 56

WIDTH = 800
HEIGHT = 500

blocks = []

class World:
    block_larg = 10
    block_alt = 30

class Moveset:
    buttonPressed = False
    jumping = False
    falling = True
    jumpSpeed = 0
    jumpInitial = 0
    jumpMax = 30
    running = False
    leftR = False
    rightR = False

    punch = False

class Physics:
    gravity = 5
    collisionVertical = False
    collisionHorizontal = False
    left = False
    right = False    

class Animation:
    state = 'idle'
    leftRunningImages = ['leftrunningshaolin', '1.5leftrunningshaolin', '2leftrunningshaolin']
    rightRunningImages = ['rightrunningshaolin','1.5rightrunningshaolin', '2rightrunningshaolin']
    jumpleftImages = ['jumplshaolin', '2jumplshaolin']
    jumprightImages = ['jumprshaolin', '2jumprshaolin']
    punchleftImages = ['2leftpunchshaolin']
    punchrightImages = [ '2rightpunchshaolin']
    frame = 0
    frameCounter = 0
    frameSpeed = 8

class Robot:
    def __init__(self, x, y):
        self.actor = Actor('lrobot')
        self.actor.pos = x, y
        self.speed = 1
        self.direction = 1
        self.origin_x = x
        self.limit = 20
        self.gravity = 5
        self.falling = True
        self.right = False
        self.left = False

        self.robotLeftFrames = ['lrobot', '2lrobot']
        self.robotRightFrames = ['rrobot', '2rrobot']
        self.frame = 0
        self.frameCounter = 0
        self.frameSpeed = 8

    def update(self):
        # lógica de andar, limite e gravidade
        self.actor.x += self.speed * self.direction
        if self.actor.x >= self.origin_x + self.limit:
            self.right = False
            self.left = True
            self.direction = -1
        if self.actor.x <= self.origin_x - self.limit:
            self.right = True
            self.left = False
            self.direction = 1
        
        if self.left == True:
            self.frameCounter += 1
            if self.frameCounter >= self.frameSpeed:
                self.frameCounter = 0
                self.frame = (self.frame + 1) % len(self.robotLeftFrames)
        
            self.actor.image = self.robotLeftFrames[self.frame]
        elif self.right == True:
            self.frameCounter += 1
            if self.frameCounter >= self.frameSpeed:
                self.frameCounter = 0
                self.frame = (self.frame + 1) % len(self.robotRightFrames)
        
            self.actor.image = self.robotRightFrames[self.frame]


        if self.falling:
            self.actor.y += self.gravity

        if self.actor.colliderect(ground):
            if self.actor.bottom >= ground.top:
                self.actor.bottom = ground.top
                self.falling = False
        else:
            self.falling = True

        for block in blocks:
            if self.actor.colliderect(block):
                if self.actor.bottom >= block.top and self.actor.y < block.top:
                    self.actor.bottom = block.top
                    self.falling = False
                    return
                

robots = []               

robots.append(Robot(500, 300))


animate = Animation()
move = Moveset()
phys = Physics()
world1 = World()

for x in range(300, 600, 300):
    block = Rect(x, 300, world1.block_larg, world1.block_alt)
    blocks.append(block)

def draw():
    screen.clear()
    shaolin.draw()
    screen.draw.rect(ground, (255, 255, 255))
    screen.draw.rect(wall, (255,255,255))
    block_image = Actor('block')
    
    for block in blocks:
        block_image.pos = block.x, block.y
        block_image.draw()
    for r in robots:
        r.actor.draw()

def update():

    # ===== GRAVIDADE =====
    if not move.jumping and not phys.collisionVertical:
        shaolin.y += phys.gravity
        move.falling = True

    # ===== PULO =====
    if keyboard.w and not move.falling and not move.jumping:
        move.jumping = True
        move.jumpSpeed = 15

    if move.jumping:
        shaolin.y -= move.jumpSpeed
        move.jumpSpeed -= 1
        
        animate.state = "jump_left" if move.leftR else "jump_right"

        if move.jumpSpeed <= 0:
            move.jumping = False
            move.falling = True

    # ===== MOVIMENTO HORIZONTAL =====
    if keyboard.d:
        shaolin_right()
        animate.state = "run_right"
        move.leftR = False
        if not phys.right:
            shaolin.x += 5
            move.rightR = True

    elif keyboard.a:
        shaolin_left()
        animate.state = "run_left"
        move.rightR = False
        if not phys.left:
            shaolin.x -= 5
            move.leftR = True

    else:
        animate.state = "idle"


    if keyboard.h and not move.punch:
        move.punch = True
        


    colisao()
    update_animation()
    for r in robots:
       r.update()

def update_animation():

    if move.jumping:
        shaolin.image = "2jumplshaolin" if move.leftR else "2jumprshaolin"
        return
    
    if animate.state == "run_right":
        shaolin_right()
        return

    if animate.state == "run_left":
        shaolin_left()
        return
    
    if move.punch:
        if move.leftR:
            frames = animate.punchleftImages
        else:
            frames = animate.punchrightImages

        # Atualiza frame da animação de soco
        animate.frameCounter += 1
        if animate.frameCounter >= animate.frameSpeed:
            animate.frameCounter = 0
            animate.frame += 1

        # Checa se acabou a animação
        if animate.frame >= len(frames):
            animate.frame = 0
            move.punch = False  # termina o soco
            normal_stance()     # volta para a stance normal
        else:
            shaolin.image = frames[animate.frame]
        return

    normal_stance()

def shaolin_right():  
    animate.frameCounter += 1
    if animate.frameCounter >= animate.frameSpeed:
        animate.frameCounter = 0
        animate.frame = (animate.frame + 1) % len(animate.rightRunningImages)
    shaolin.image = animate.rightRunningImages[animate.frame]

def shaolin_left():       
    animate.frameCounter += 1
    if animate.frameCounter >= animate.frameSpeed:
        animate.frameCounter = 0
        animate.frame = (animate.frame + 1) % len(animate.leftRunningImages)
    shaolin.image = animate.leftRunningImages[animate.frame]

def normal_stance():
    if move.jumping or move.falling:
        return
    if move.rightR:
        shaolin.image = 'shaolin'
    elif move.leftR:
        shaolin.image = 'lshaolin'

def colisao():

    phys.collisionVertical = False
    phys.collisionHorizontal = False

    # ===== COLISÃO COM CHÃO =====
    if shaolin.colliderect(ground):
        if move.falling and shaolin.bottom >= ground.top:
            shaolin.bottom = ground.top
            move.falling = False
            phys.collisionVertical = True
            return

    # ===== COLISÃO COM BLOCOS =====
    for block in blocks:
        if shaolin.colliderect(block):

            # Veio de cima (CAINDO)
            if move.falling and shaolin.bottom >= block.top and shaolin.y < block.top:
                shaolin.bottom = block.top
                move.falling = False
                phys.collisionVertical = True
                return

            # Veio de baixo (SUBINDO — bateu a cabeça)
            if move.jumping and shaolin.top <= block.bottom and shaolin.y > block.bottom:
                shaolin.top = block.bottom
                move.jumping = False
                move.falling = True
                phys.collisionVertical = True
                return

    # ===== COLISÃO HORIZONTAL (PAREDE) =====
    if shaolin.colliderect(wall):

        # bate no lado direito do personagem
        if shaolin.right >= wall.left and shaolin.left < wall.left:
            phys.right = True
            phys.collisionHorizontal = True
            return
        
        # bate no lado esquerdo
        if shaolin.left <= wall.right and shaolin.right > wall.right:
            phys.left = True
            phys.collisionHorizontal = True
            return

    phys.left = False
    phys.right = False
