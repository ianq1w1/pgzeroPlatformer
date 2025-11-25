from pygame import Rect

ground = Rect(10,350,500,30)
#wall = Rect(550,400, 30,30)

shaolin = Actor('shaolin')
shaolin.pos = 100, 56

#leftRunningImages = ['leftrunnningshaolin', '2leftrunningshaolin']
#rightRunningImages = ['rightrunningshaolin', '2rightrunningshaolin']

WIDTH = 800
HEIGHT = 500

blocks = []

class World:

    block_larg = 10
    block_alt = 0


class Moveset:
    buttonPressed = False
    jumping = False
    falling = False
    jumpSpeed = 0
    jumpInitial = 0      # força inicial
    jumpMax = 30
    #jumpHoldBoost = 4   # quanto continua subindo se segurar
    #jumpMaxHoldTime = 16   # limite de "segurar para pular mais"
    #holdCounter = 0

    leftR = False
    rightR = False

class Physics:
    gravity = 5
    collisionVertical = False
    collisionHorizontal = False

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

for x in range(300, 600,100):
    block = Rect(x, 300, world1.block_larg, world1.block_alt)
    blocks.append(block)

def draw():
    screen.clear()
    shaolin.draw()
    screen.draw.rect(ground, (255, 255, 255))
#    screen.draw.rect(wall, (255,255,255))
    block_image = Actor('block')  # Carregue a imagem do bloco
    
    for block in blocks:
        block_image.pos = block.x, block.y
        block_image.draw()  # Desenha a imagem do bloco



def update():
    colisao()
    normal_stance()
    if phys.collisionVertical == False:
        shaolin.y += phys.gravity
    if phys.collisionVertical == True:
        shaolin.x 
        #print('caindo')
#    if phys.collisionVertical == True:
        #print('no chao')
    if keyboard.w and move.falling == False:
        print('w pressionado')
        move.jumpSpeed = move.jumpSpeed + 2
        print(move.jumpSpeed)
        move.buttonPressed = True
        
        if move.jumpSpeed != move.jumpMax  and move.falling == False:
            shaolin.y -= 15

    elif not keyboard.w:
        move.buttonPressed = False
        print('deixou de pressionar')

    if move.jumpSpeed == move.jumpMax and phys.collisionVertical == False or move.buttonPressed == False and phys.collisionVertical == False:
        move.jumpSpeed = 0
        move.falling = True
        print('caindo')
        print('queda terminada')
 
    # movimentação básica
    if keyboard.d:
        shaolin_right()
        move.rightR = True 
        move.leftR = False       
        shaolin.x += 5
      #  animate.frame = 0
    if keyboard.a:
        shaolin_left()
        shaolin.x -= 5
        move.leftR = True
        move.rightR = False
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
    if shaolin.colliderect(ground) and shaolin.y <= ground.top :

        phys.collisionVertical = True
        move.falling = False
        print('tocou no chao')

        #move.jumpSpeed = 0
    elif not shaolin.colliderect(ground):
        phys.collisionVertical = False

    for block in blocks:
        if shaolin.colliderect(block) and shaolin.y <= block.y :
            
            phys.collisionVertical = True
            move.falling = False
           # shaolin.bottom = block.top
            print(f'Tocou no bloco em {block.x}, {block.y}')
            break  # Interrompe a verificação após detectar colisão        
