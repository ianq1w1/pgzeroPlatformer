from pygame import Rect

ground = Rect(10,350,500,30)

alien = Actor('alienzitos')
alien.pos = 100, 56

WIDTH = 800
HEIGHT = 500

class Moveset:
    buttonPressed = False
    jumping = False
    falling = False
    jumpSpeed = 0
    jumpInitial = 0      # força inicial
    jumpMax = 70
    jumpHoldBoost = 4   # quanto continua subindo se segurar
    jumpMaxHoldTime = 16   # limite de "segurar para pular mais"
    holdCounter = 0

class Physics:
    gravity = 5
    collisionVertical = False

move = Moveset()
phys = Physics()


def draw():
    screen.clear()
    alien.draw()
    screen.draw.rect(ground, (255, 255, 255))


def update():
    colisao()
    if phys.collisionVertical == False:
        alien.y += phys.gravity
        
        #print('caindo')
#    if phys.collisionVertical == True:
        #print('no chao')
    if keyboard.w and move.falling == False:
        print('w pressionado')
        move.jumpSpeed = move.jumpSpeed + 2
        print(move.jumpSpeed)
        move.buttonPressed = True
        
        if move.jumpSpeed != move.jumpMax and move.buttonPressed == True and move.falling == False:
            alien.y -= 10
            #move.jumping = True
            #print('parou')
    elif not keyboard.w:
        move.buttonPressed = False
        print('deixou de pressionar')

    if move.jumpSpeed == move.jumpMax and phys.collisionVertical == False or move.buttonPressed == False and phys.collisionVertical == False:
        move.jumpSpeed = 0
        move.falling = True

        #move.jumping = False
        #alien.y += phys.gravity
        print('caindo')

        print('queda terminada')
        #if move.jumping == False:
        #    move.jumpSpeed = 0
        #    print('resetado')
                    
    

    # movimentação básica
    if keyboard.d:
        alien.x += 5
    if keyboard.a:
        alien.x -= 5


def colisao():
    if alien.colliderect(ground):
        #alien.bottom = ground.top
        phys.collisionVertical = True
       #move.jumping = False
        move.falling = False
        print('tocou no chao')

        #move.jumpSpeed = 0
    elif not alien.colliderect(ground):
        phys.collisionVertical = False
