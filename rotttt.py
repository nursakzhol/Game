
import pygame
import math
pygame.init()
pygame.mixer.music.load('c26baac1db252bd.mp3')

kuk = pygame.image.load('252.png')

class Screen(object):
    width = 640
    height = 480
    hw = width/2
    hh = height/2
    area = width*height
    fps = 60
win = pygame.display.set_mode((Screen.width, Screen.height))
class Bullet(pygame.sprite.Sprite):

    side = 3
    vel = 180
    mass = 50
    maxlifetime = 10.0

    def __init__(self, head):
        pygame.sprite.Sprite.__init__(self, self.groups)  # THE most important line !
        self.head = head
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.lifetime = 0.0
        self.color = self.head.color
        self.calculate_heading()
        self.dx += self.head.dx
        self.dy += self.head.dy
        self.pos = self.head.pos[:]
        self.calculate_origin()
        self.update()

    def calculate_heading(self):
        self.radius = Bullet.side
        self.angle += self.head.turretAngle
        self.mass = Bullet.mass
        self.vel = Bullet.vel
        image = pygame.Surface((Bullet.side * 2, Bullet.side))
        image.fill((128, 128, 128))
        pygame.draw.rect(image, (0, 0, 0), (0, 0, int(Bullet.side * 1.5), Bullet.side))
        pygame.draw.circle(image, (0, 0, 0), (int(self.side * 1.5), self.side // 2), self.side // 2)
        image.set_colorkey((128, 128, 128))
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        self.dx = math.cos(degrees_to_radians(self.head.turretAngle)) * self.vel
        self.dy = math.sin(degrees_to_radians(-self.head.turretAngle)) * self.vel

    def calculate_origin(self):
        self.pos[0] += math.cos(degrees_to_radians(self.head.turretAngle)) * (Tank.side - 20)
        self.pos[1] += math.sin(degrees_to_radians(-self.head.turretAngle)) * (Tank.side - 20)

    def update(self, seconds=0.0):

        self.lifetime += seconds
        if self.lifetime > Bullet.maxlifetime:
            self.kill()

        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds

        if self.pos[0] < 0 and self.pos[0] == self.pos:
            self.kill()
        elif self.pos[0] > Screen.width:
            self.kill()
        if self.pos[1] < 0:
            self.kill()
        elif self.pos[1] > Screen.height:
            self.kill()

        self.rect.centerx = round(self.pos[0], 0)
        self.rect.centery = round(self.pos[1], 0)





def radians_to_degrees(radians):
    return (radians / math.pi) * 180.0


def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)

class Tank(pygame.sprite.Sprite):
    side = 75
    turretTurnSpeed = 30
    tankTurnSpeed = 15
    movespeed = 25
    maxrotate = 360
    recoiltime = 0.5
    book = {}  # a book of tanks to store all tanks
    number = 0
    turretLeftkey = (pygame.K_j, pygame.K_6)
    turretRightkey = (pygame.K_l, pygame.K_4)
    fireKey = (pygame.K_SPACE, pygame.K_KP_ENTER)
    forwardkey = (pygame.K_w, pygame.K_UP)
    backwardkey = (pygame.K_s, pygame.K_DOWN)
    tankLeftkey = (pygame.K_a, pygame.K_LEFT)
    tankRightkey = (pygame.K_d, pygame.K_RIGHT)
    color = ((3, 94, 0), (190, 0, 0))

    def __init__(self, startpos=(150, 150), angle=0):
        self.number = Tank.number
        Tank.number += 1
        Tank.book[self.number] = self
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [startpos[0], startpos[1]]
        self.hitbox = (75, 75, 75 ,75)
        self.dx = 0
        self.dy = 0
        self.ammo = 30
        self.sound = pygame.mixer.music.load('tank-proezjaet-mimo_[Pro-Sound.org].mp3')
        self.color =  Tank.color[self.number]
        self.turretAngle = angle
        self.tankAngle = angle

        self.fireKey = Tank.fireKey[self.number]
        self.turretLeftkey = Tank.turretLeftkey[self.number]
        self.turretRightkey = Tank.turretRightkey[self.number]
        self.forwardkey = Tank.forwardkey[self.number]
        self.backwardkey = Tank.backwardkey[self.number]
        self.tankLeftkey = Tank.tankLeftkey[self.number]
        self.tankRightkey = Tank.tankRightkey[self.number]
        image = pygame.Surface((Tank.side, Tank.side))
        image.fill((0, 128, 0))
        if self.side > 10:
            pygame.draw.rect(image, self.color, (5, 5, self.side - 10, self.side - 10))
            pygame.draw.rect(image, (2, 47, 0), (0, 0, self.side // 6, self.side))
            pygame.draw.rect(image, (2, 47, 0), (self.side - self.side // 6, 0, self.side, self.side))

        image = pygame.transform.rotate(image, -90)
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        self.firestatus = 0.0
        self.turndirection = 0
        self.tankturndirection = 0
        self.movespeed = Tank.movespeed
        self.turretTurnSpeed = Tank.turretTurnSpeed
        self.tankTurnSpeed = Tank.tankTurnSpeed
        Turret(self)
        pygame.mixer.music.play(5)
    def update(self, seconds):

        if self.firestatus > 0:
            self.firestatus -= seconds
            if self.firestatus < 0:
                self.firestatus = 0
        pressedkeys = pygame.key.get_pressed()

        self.turndirection = 0
        if pressedkeys[self.turretLeftkey]:
            self.turndirection += 1
            print(self.pos)

        if pressedkeys[self.turretRightkey]:
            self.turndirection -= 1

        self.tankturndirection = 0
        if pressedkeys[self.tankLeftkey]:

            self.tankturndirection += 1
        if pressedkeys[self.tankRightkey]:
            self.tankturndirection -= 1


        self.tankAngle += self.tankturndirection * self.tankTurnSpeed * seconds #tank rotaion

        oldcenter = self.rect.center
        oldrect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

        self.turretAngle += self.tankturndirection * self.tankTurnSpeed * seconds + self.turndirection * self.turretTurnSpeed * seconds
        if (self.firestatus == 0) and (self.ammo > 0):
            if pressedkeys[self.fireKey]:

                self.firestatus = Tank.recoiltime
                Bullet(self)

                self.ammo -= 1

        self.dx = 0
        self.dy = 0

        self.forward = 1



        if pressedkeys[self.forwardkey]:
            self.forward = 1


        if pressedkeys[self.backwardkey]:

            self.forward = -1


        if self.forward == 1:
            self.dx += math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy += -math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed
        if self.forward == -1:
            self.dx = -math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy = math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed
        if self.pos[0] > Screen.width:
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = Screen.width
        if self.pos[1] > Screen.height:
            self.pos[1] = 0
        if self.pos[1] < 0:
            self.pos[1] = Screen.height
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds

        self.rect.centerx = round(self.pos[0], 0)
        self.rect.centery = round(self.pos[1], 0)

class Turret(pygame.sprite.Sprite):

    def __init__(self, head):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.head = head
        self.side = self.head.side
        self.images = {}
        self.images[0] = self.draw_cannon(0)  # idle position

    def update(self, seconds):
        self.image = self.images[0]

        oldrect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, self.head.turretAngle)
        self.rect = self.image.get_rect()

        self.rect = self.image.get_rect()
        self.rect.center = self.head.rect.center

    def draw_cannon(self, offset):
        image = pygame.Surface((self.head.side * 2, self.head.side * 2))  # created on the fly
        image.fill((128, 128, 128))  # fill grey
        pygame.draw.circle(image, (85, 60, 17), (self.side, self.side), 22, 0)  # red circle
        pygame.draw.circle(image, (43, 30, 9), (self.side, self.side), 18, 0)  # green circle
        pygame.draw.rect(image, (17, 11, 3), (self.side - 10, self.side + 10, 15, 2))  # turret mg rectangle
        pygame.draw.rect(image, (17, 11, 3),
                         (self.side - 20 - offset, self.side - 5, self.side - offset, 10))
        pygame.draw.rect(image, (0, 0, 0), (self.side - 20 - offset, self.side - 5, self.side - offset, 10), 1)
        image.set_colorkey((128, 128, 128))
        return image








def main():
    pygame.init()
    win = pygame.display.set_mode((Screen.width, Screen.height))


    clock = pygame.time.Clock()
    FPS = Screen.fps
    playtime = 0

    tankgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()

    Tank._layer = 4
    Bullet._layer = 7
    Turret._layer = 6
    Tank.groups = tankgroup, allgroup
    Turret.groups = allgroup
    Bullet.groups = bulletgroup, allgroup
    player1 = Tank((150, 250), 90)
    player2 = Tank((450, 250), -90)
    mainloop = True

    while mainloop:

        milliseconds = clock.tick(Screen.fps)
        seconds = milliseconds / 1000.0  # seconds passed since last frame (float)
        playtime += seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False  # exit game
        kuk = pygame.image.load('252.png').convert()


        win.blit(kuk, (0, 0))


        allgroup.update(seconds)
        allgroup.draw(win)
        pygame.display.flip()
    return 0



if __name__ == '__main__':
    main()


