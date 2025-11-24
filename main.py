from pygame import Rect

ground = Rect(10,350,500,30)

shaolin = Actor('shaolin')
shaolin.pos = 100, 56

#leftRunningImages = ['leftrunnningshaolin', '2leftrunningshaolin']
#rightRunningImages = ['rightrunningshaolin', '2rightrunningshaolin']

WIDTH = 800
HEIGHT = 500

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

class Animation:
    leftRunningImages = ['leftrunningshaolin', '1.5leftrunningshaolin', '2leftrunningshaolin']
    rightRunningImages = ['rightrunningshaolin','1.5rightrunningshaolin', '2rightrunningshaolin']
    frame = 0


animate = Animation()
move = Moveset()
phys = Physics()


def draw():
    screen.clear()
    shaolin.draw()
    screen.draw.rect(ground, (255, 255, 255))


def update():
    colisao()
    normal_stance()
    if phys.collisionVertical == False:
        shaolin.y += phys.gravity
        
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
    animate.frame = (animate.frame + 1) % len(animate.rightRunningImages)
    shaolin.image = (animate.rightRunningImages[animate.frame])

def shaolin_left():       
    #shaolin.image = ('leftrunningshaolin')
    #animate.frame = 0     
    animate.frame = (animate.frame + 1) % len(animate.leftRunningImages)
    shaolin.image = (animate.leftRunningImages[animate.frame])

def normal_stance():
    if move.rightR == True:
        shaolin.image = ('shaolin')
    elif move.leftR == True:
        shaolin.image = ('lshaolin')

def colisao():
    if shaolin.colliderect(ground):
        #shaolin.bottom = ground.top
        phys.collisionVertical = True
       #move.jumping = False
        move.falling = False
        print('tocou no chao')

        #move.jumpSpeed = 0
    elif not shaolin.colliderect(ground):
        phys.collisionVertical = False
