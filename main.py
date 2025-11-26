from pygame import Rect

music.set_volume(0.5)   # opcional
music.play("theme")

estado_do_jogo = "menu"


button_play = Actor("play")
button_exit = Actor("exit")
button_sound = Actor("soundon")   # começa ligado
logo = Actor("title")

#wall = Rect(350,300, 30,30)

WIDTH = 800
HEIGHT = 500

button_play.pos = (WIDTH // 2, 250)
button_exit.pos = (WIDTH // 2, 330)
logo.pos = (WIDTH // 2, 120)
button_sound.pos = (50, 50)


scenario = images.scenario1  # carrega imagem
map_width = scenario.get_width()

GROUND_Y = 330

class World:
    block_larg = 10
    block_alt = 30
    camera_x = 0

class MenuGame:
    Play = False
    Exit = False
    SoundOn = True
    SoundOff = False
    

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
            else:
                 self.actor = None
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
                



def start_new_game():
    global move, robots, world1, phys, blocks, ground

    move = Player(100, 56)
    phys = Physics()
    world1 = World()

    robots = []
    robots.append(Robot(500, 300))
    robots.append(Robot(600,300))
    robots.append(Robot(800, 300))
    robots.append(Robot(750, 300))
    robots.append(Robot(1000, 300))

    # reconstruir blocos
    blocks = []
    ground = Rect(10,350,150,30)
    for x in range(300, map_width, 30):
        blocks.append(Rect(x, GROUND_Y, 30, 30))

    world1.camera_x = 0

    if MenuGame.SoundOn:
        music.play("theme")

def draw_menu():

    screen.clear()
    screen.blit("menubg", (0, 0))  # se tiver um fundo

    logo.draw()

    button_play.draw()
    button_exit.draw()
    button_sound.draw()

def update_menu():
    global estado_do_jogo
    if keyboard.RETURN:
        start_new_game()
        estado_do_jogo = "jogo"


def on_mouse_down(pos):
    global estado_do_jogo

    if estado_do_jogo == "menu":

        # BOTÃO PLAY
        if button_play.collidepoint(pos):
            start_new_game()
            estado_do_jogo = "jogo"
            return

        # BOTÃO EXIT
        if button_exit.collidepoint(pos):
            exit()

        # BOTÃO SOUND
        if button_sound.collidepoint(pos):
            if MenuGame.SoundOn:
                MenuGame.SoundOn = False
                MenuGame.SoundOff = True
                button_sound.image = "soundoff"
                music.stop()
            else:
                MenuGame.SoundOn = True
                MenuGame.SoundOff = False
                button_sound.image = "soundon"
                music.play("theme")

#for x in range(300, 600, 300):
#    block = Rect(x, 300, world1.block_larg, world1.block_alt)
#    blocks.append(block)


def draw():
    if estado_do_jogo == "menu":
        draw_menu()
        return
    elif estado_do_jogo == "jogo":
        screen.clear()
        # background rolando com a câmera
        screen.blit("scenario1", (-world1.camera_x, 0))

        # player
        if move.actor:
            screen.blit(move.actor.image, (move.actor.x - world1.camera_x - move.actor.width/2,
                                        move.actor.y - move.actor.height/2))

        # chão
        screen.draw.filled_rect(Rect(ground.x - world1.camera_x, ground.y, ground.width, ground.height), (255,255,255))

        # blocos
        for block in blocks:
            screen.blit("block", (block.x - world1.camera_x, block.y))

        # robôs
        for r in robots:
            screen.blit(r.actor.image,
                        (r.actor.x - world1.camera_x - r.actor.width/2,
                        r.actor.y - r.actor.height/2))



def update():
    global estado_do_jogo

    if estado_do_jogo == "menu":
        update_menu()
        return

    # ======= ESTAMOS NO JOGO ========

    move.update()
    colisao()

    if move.actor and move.actor.y > HEIGHT + 100:
        move.playerDead = True

    # se o player morreu → volta para menu
    if move.playerDead and move.actor == None:
        estado_do_jogo = "menu"
        return
    


    world1.camera_x = move.actor.x - WIDTH//2

    for r in robots:
        r.update()


def colisao():

    phys.collisionVertical = False
    phys.collisionHorizontal = False

    # ===== COLISÃO COM CHÃO =====
    if move.actor:
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
        """if move.actor.colliderect(wall):

            # bate no lado direito do personagem
            if move.actor.right >= wall.left  and move.actor.left < wall.left:
                phys.right = True
                phys.collisionHorizontal = True
                return
            
            # bate no lado esquerdo
            if move.actor.left <= wall.right and move.actor.right > wall.right:
                phys.left = True
                phys.collisionHorizontal = True
                return"""     
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
