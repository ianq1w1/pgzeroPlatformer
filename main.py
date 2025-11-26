from pygame import Rect

ground = Rect(10,350,700,30)
wall = Rect(350,300, 30,30)

WIDTH = 800
HEIGHT = 500

blocks = []

class World:
    block_larg = 10
    block_alt = 30

class Player:
    def __init__(self,x,y): 
        self.actor = Actor('shaolin')
        self.actor.pos = x,y      
        self.buttonPressed = False
        self.jumping = False
        self.falling = True
        self.jumpSpeed = 0
        self.jumpInitial = 0
        self.jumpMax = 30
        self.running = False
        self.leftR = False
        self.rightR = False

        self.punch = False
        self.playerDead = False

        self.state = 'idle'
        self.leftRunningImages = ['leftrunningshaolin', '1.5leftrunningshaolin', '2leftrunningshaolin']
        self.rightRunningImages = ['rightrunningshaolin','1.5rightrunningshaolin', '2rightrunningshaolin']
        self.jumpleftImages = ['jumplshaolin', '2jumplshaolin']
        self.jumprightImages = ['jumprshaolin', '2jumprshaolin']
        self.punchleftImages = ['leftpunchshaolin', '2leftpunchshaolin']
        self.punchrightImages = ['rightpunchshaolin', '2rightpunchshaolin']
        self.deadplayerImages = ['dead1shaolin', 'dead2shaolin', 'dead3shaolin', 'dead4shaolin']
        self.frameDEAD = 0
        self.frameSpeedDEAD = 20
        self.frameRUN = 0
        self.frameJUMP = 0
        self.framePUNCH = 0
        self.frame = 0
        self.frameCounter = 0
        self.frameSpeed = 8
    def update(self):
        if self.playerDead == True:
            print('jogador morto')
            if self.frameDEAD < len(self.deadplayerImages)-1:
                self.frameCounter += 1
                if self.frameCounter >= self.frameSpeed:
                    self.frameCounter = 0
                    self.frameDEAD += 1

                self.actor.image = self.deadplayerImages[self.frameDEAD]

        if self.playerDead == False:   
            if not self.jumping and not phys.collisionVertical:
                self.actor.y += phys.gravity
                self.falling = True

            # ===== PULO =====
            if keyboard.w and not self.falling and not self.jumping:
                self.jumping = True
                self.jumpSpeed = 15

            if self.jumping:
                self.actor.y -= self.jumpSpeed
                self.jumpSpeed -= 1
                
                self.state = "jump_left" if self.leftR else "jump_right"

                if self.jumpSpeed <= 0:
                    self.jumping = False
                    self.falling = True

            # ===== MOVIMENTO HORIZONTAL =====
            if keyboard.d:
                self.state = "run_right"
                self.leftR = False
                if not phys.right:
                    self.actor.x += 5
                    self.rightR = True

            elif keyboard.a:
                self.state = "run_left"
                self.rightR = False
                if not phys.left:
                    self.actor.x -= 5
                    self.leftR = True

            else:
                self.state = "idle"


            if keyboard.h and not self.punch:
                self.punch = True

            if self.jumping:
                frames = self.jumpleftImages if self.leftR else self.jumprightImages
                if self.state == "jump_left" or self.state == "jump_right":
                    self.frameJUMP = 0
                    self.frameCounter = 0
                self.frameCounter += 1
                if self.frameCounter >= self.frameSpeed:
                    self.frameCounter = 0
                    self.frameJUMP = (self.frameJUMP + 1) % len(frames)

                self.actor.image = frames[self.frameJUMP]
                return
        
            if self.state == "run_right":
                self.frameCounter += 1
                if self.frameCounter >= self.frameSpeed:
                    self.frameCounter = 0
                    self.frameRUN = (self.frameRUN + 1) % len(self.rightRunningImages)
                self.actor.image = self.rightRunningImages[self.frameRUN]
                return
            
            if self.state == "run_left":
                self.frameCounter += 1
                if self.frameCounter >= self.frameSpeed:
                    self.frameCounter = 0
                    self.frameRUN = (self.frameRUN + 1) % len(self.leftRunningImages)
                self.actor.image = self.leftRunningImages[self.frameRUN]
                return
        
            if self.punch:
                if self.leftR:
                    frames = self.punchleftImages
                else:
                    frames = self.punchrightImages

                # Atualiza frame da animação de soco
                self.frameCounter += 1
                if self.frameCounter >= self.frameSpeed:
                    self.frameCounter = 0
                    self.framePUNCH += 1

                # Checa se acabou a animação
                if self.framePUNCH >= len(frames):
                    self.framePUNCH = 0
                    self.punch = False  # termina o soco
                    #normal_stance()     # volta para a stance normal
                else:
                    self.actor.image = frames[self.framePUNCH]
                return    
            
            if self.jumping or self.falling:
                return
            if self.rightR:
                self.actor.image = 'shaolin'
            elif self.leftR:
                self.actor.image = 'lshaolin'
        


class Physics:
    gravity = 5
    collisionVertical = False
    collisionHorizontal = False
    left = False
    right = False    

class Robot:
    def __init__(self, x, y):
        self.actor = Actor('lrobot')
        self.actor.pos = x, y
        self.speed = 1
        self.direction = 1
        self.origin_x = x
        self.limit = 80
        self.gravity = 5
        self.falling = True
        self.right = False
        self.left = False
        self.dead = False

        self.robotLeftFrames = ['lrobot', '2lrobot']
        self.robotRightFrames = ['rrobot', '2rrobot']
        self.robotDeadFrames = ['robotdead1', 'robotdead2']
        self.frame = 0
        self.frameDEAD = 0
        self.frameCounter = 0
        self.frameSpeed = 15

    def update(self):
        if self.dead == True:
                # roda a animação apenas uma vez
            print('robot dead')
            if self.frameDEAD < len(self.robotDeadFrames)-1:
                self.frameCounter += 1
                if self.frameCounter >= self.frameSpeed:
                    self.frameCounter = 0
                    self.frameDEAD += 1

                self.actor.image = self.robotDeadFrames[self.frameDEAD]

            
            else:
                robots.remove(self)
            return 
        if self.dead == False:
            
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
            
            #animation
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
            
            #queda
            if self.falling:
                self.actor.y += self.gravity

            #colisao
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
robots.append(Robot(600,300))

move = Player(100, 56)
phys = Physics()
world1 = World()

for x in range(300, 600, 300):
    block = Rect(x, 300, world1.block_larg, world1.block_alt)
    blocks.append(block)

def draw():
    screen.clear()
    move.actor.draw()
    screen.draw.rect(ground, (255, 255, 255))
    screen.draw.rect(wall, (255,255,255))
    block_image = Actor('block')
    
    for block in blocks:
        block_image.pos = block.x, block.y
        block_image.draw()
    for r in robots:
        r.actor.draw()

def update():

    move.update()
    colisao()
    for r in robots:
       r.update()

def colisao():

    phys.collisionVertical = False
    phys.collisionHorizontal = False

    # ===== COLISÃO COM CHÃO =====
    if move.actor.colliderect(ground):
        if move.falling and move.actor.bottom >= ground.top:
            move.actor.bottom = ground.top
            move.falling = False
            phys.collisionVertical = True
            return

    # ===== COLISÃO COM BLOCOS =====
    for block in blocks:
        if move.actor.colliderect(block):

            # Veio de cima (CAINDO)
            if move.falling and move.actor.bottom >= block.top and move.actor.y < block.top:
                move.actor.bottom = block.top
                move.falling = False
                phys.collisionVertical = True
                return

            # Veio de baixo (SUBINDO — bateu a cabeça)
            if move.jumping and move.actor.top <= block.bottom and move.actor.y > block.bottom:
                move.actor.top = block.bottom
                move.jumping = False
                move.falling = True
                phys.collisionVertical = True
                return

    # ===== COLISÃO HORIZONTAL (PAREDE) =====
    if move.actor.colliderect(wall):

        # bate no lado direito do personagem
        if move.actor.right >= wall.left  and move.actor.left < wall.left:
            phys.right = True
            phys.collisionHorizontal = True
            return
        
        # bate no lado esquerdo
        if move.actor.left <= wall.right and move.actor.right > wall.right:
            phys.left = True
            phys.collisionHorizontal = True
            return
        
    if move.punch:

        # cria hitbox do soco
        if move.rightR:
            punchbox = Rect(move.actor.right, move.actor.y - 20, 25, 40)
        else:
            punchbox = Rect(move.actor.left - 25, move.actor.y - 20, 25, 40)

        # checa colisão com robôs
        for r in robots:
            robot_rect = Rect(r.actor.x - r.actor.width/2,
                            r.actor.y - r.actor.height/2,
                            r.actor.width,
                            r.actor.height)

            if punchbox.colliderect(robot_rect):
                r.dead = True

    if move.falling:

        # checa colisão com robôs
        for r in robots:
            robot_rect = Rect(r.actor.x - r.actor.width/2,
                            r.actor.y - r.actor.height/2,
                            r.actor.width,
                            r.actor.height)

            if move.actor.colliderect(robot_rect):
                if move.actor.bottom >= robot_rect.top and move.actor.y < robot_rect.top:
                    r.dead = True

    for r in robots:
        robot_rect = Rect(r.actor.x - r.actor.width/2,
                            r.actor.y - r.actor.height/2,
                            r.actor.width,
                            r.actor.height)
        
        if move.actor.colliderect(robot_rect):
                if r.dead == False and move.punch == False and move.actor.right >= robot_rect.left and move.actor.left < robot_rect.left:
                    move.playerDead = True  
                    print('tocou')
                    return
                if r.dead == False and move.punch == False and move.actor.left <= robot_rect.right and move.actor.right > robot_rect.right:
                    move.playerDead = True
                    print('tocou tambem')
                    return
                
    phys.left = False
    phys.right = False
