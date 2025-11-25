from pygame import Rect

ground = Rect(10,350,500,30)
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
    falling = False
    jumpSpeed = 0
    jumpInitial = 0      # força inicial
    jumpMax = 30

    running = False
    leftR = False
    rightR = False


class Physics:
    gravity = 5
    collisionVertical = False
    collisionHorizontal = False
    left = False
    right = False    
    

class Animation:
    leftRunningImages = ['leftrunningshaolin', '1.5leftrunningshaolin', '2leftrunningshaolin']
    rightRunningImages = ['rightrunningshaolin','1.5rightrunningshaolin', '2rightrunningshaolin']
    frame = 0
    frameCounter = 0
    frameSpeed = 5


animate = Animation()
move = Moveset()
phys = Physics()
world1 = World()

for x in range(300, 600,300):
    block = Rect(x, 300, world1.block_larg, world1.block_alt)
    blocks.append(block)

def draw():
    screen.clear()
    shaolin.draw()
    screen.draw.rect(ground, (255, 255, 255))
    screen.draw.rect(wall, (255,255,255))
#    screen.draw.rect(wall, (255,255,255))
    block_image = Actor('block')  # Carregue a imagem do bloco
    
    for block in blocks:
        block_image.pos = block.x, block.y
        block_image.draw()  # Desenha a imagem do bloco



def update():

    normal_stance()
    # ===== APLICA GRAVIDADE =====
    if not phys.collisionVertical and not move.jumping:
        shaolin.y += phys.gravity
        move.falling = True

    # ===== PULO =====
    if keyboard.w and not move.falling and not move.jumping:
        move.jumping = True
        move.jumpSpeed = 15
    
    if move.jumping:
        shaolin.y -= move.jumpSpeed
        move.jumpSpeed -= 1
        if move.jumpSpeed <= 0:
            move.jumping = False
            move.falling = True

    # ===== MOVIMENTO HORIZONTAL =====
    if keyboard.d:
        shaolin_right()
        move.leftR = False
        if phys.right == False:       
            shaolin.x += 5
            move.rightR = True 

      #  animate.frame = 0
    if keyboard.a:
        shaolin_left()
        move.rightR = False
        if not phys.left:
            shaolin.x -= 5
            move.leftR = True

    # ===== VERIFICA COLISÃO APÓS MOVER =====
    colisao()
    


def shaolin_right():  
    #animate.frame = 0
    animate.frameCounter += 1
    if animate.frameCounter >= animate.frameSpeed:     
        animate.frameCounter = 0
        animate.frame = (animate.frame + 1) % len(animate.rightRunningImages)
    
    shaolin.image = (animate.rightRunningImages[animate.frame])

def shaolin_left():       
    #shaolin.image = ('leftrunningshaolin')
    #animate.frame = 0     
    animate.frameCounter += 1
    if animate.frameCounter >= animate.frameSpeed:     
        animate.frameCounter = 0
        animate.frame = (animate.frame + 1) % len(animate.leftRunningImages)
    
    shaolin.image = (animate.leftRunningImages[animate.frame])

def normal_stance():
    if move.rightR == True:
        shaolin.image = ('shaolin')
    elif move.leftR == True:
        shaolin.image = ('lshaolin')


def colisao():

    print(f'shaolin em {shaolin.x}, {shaolin.y}')
    phys.collisionVertical = False
    phys.collisionHorizontal = False
    
    # Chão
    if shaolin.colliderect(ground):
        if shaolin.bottom >= ground.top:
            shaolin.bottom = ground.top
            move.falling = False
            phys.collisionVertical = True
            return

    # Blocos
    for block in blocks:
        if shaolin.colliderect(block):
            # Está vindo de cima
            if shaolin.bottom >= block.top and shaolin.y < block.top:
                shaolin.bottom = block.top
                move.falling = False
                phys.collisionVertical = True
                return
    
    #horizontal
    if shaolin.colliderect(wall):
        if shaolin.right >= wall.left and shaolin.left < wall.left:
            phys.right = True            
            move.running = False
            phys.collisionHorizontal = True
            #print('bateu na direita')
            return
        
        elif shaolin.left <= wall.right and shaolin.right > wall.right:
            phys.left = True
            move.running = False
            phys.collisionHorizontal = True
            print('bateu esquerda')
            return
        
    phys.left = False
    phys.right = False
    
