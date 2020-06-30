# IMPORTS

import pygame
import random
import sys

# PYGAME INITIALIZATION

pygame.init()

# WINDOW SETTINGS

win = pygame.display.set_mode((650, 650), 0, 32)
pygame.display.set_caption("Snake | Score: 0")

# VARIABLES

clock = pygame.time.Clock()
fps = 60
score = 0
foodOnScreen = False
snakeHeadAlive = pygame.image.load("snakeHead.png")
gameLoop = True


def renderText(text, fontSize, pos, width, height, color=(0, 0, 0)):
    # LOAD FONT
    font = pygame.font.SysFont('Arial', fontSize)

    # SET TEXT
    textSurface = font.render(str(text), True, color)

    # CENTER TEXT
    textRect = textSurface.get_rect()
    textRect.center = ((pos[0] + (width / 2)), (pos[1] + (height / 2)))

    # DRAW TEXT TO WINDOW
    win.blit(textSurface, textRect)


class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(win, (168, 0, 0), (self.x, self.y, 25, 25))

    def getCollision(self):
        global foodOnScreen, snake, score

        if snake.x == self.x and snake.y == self.y:

            snake.bodySize += 1

            if snake.bodySize == 1:
                snake.body.append(SnakeBody(snake.x, snake.y, snake.bodySize, snake.snakeDist, snake.previousDist))
                snake.bodySize += 1
                snake.body.append(SnakeBody(snake.body[-1].x, snake.body[-1].y, snake.bodySize,
                                            snake.body[-1].bodyDist, snake.body[snake.bodySize - 2].previousDist))
            else:
                snake.body.append(SnakeBody(snake.body[-1].x, snake.body[-1].y, snake.bodySize,
                                            snake.body[-1].bodyDist, snake.body[snake.bodySize - 2].previousDist))
                snake.bodySize += 1
                snake.body.append(SnakeBody(snake.body[-1].x, snake.body[-1].y, snake.bodySize,
                                            snake.body[-1].bodyDist, snake.body[snake.bodySize - 2].previousDist))

            foodOnScreen = False
            score += 1
            pygame.display.set_caption(f"Snake | Score: {str(score)}")


class SnakeBody(object):
    def __init__(self, x, y, bodySize, dist, previousDist):
        self.x = x
        self.y = y
        self.bodyDist = dist
        self.previousDist = previousDist
        self.posInBody = bodySize

        if self.bodyDist == "up":
            self.y += 25
        if self.bodyDist == "down":
            self.y -= 25
        if self.bodyDist == "right":
            self.x -= 25
        if self.bodyDist == "left":
            self.x += 25

    def draw(self):
        pygame.draw.rect(win, (0, 128, 0), (self.x, self.y, 25, 25))

    def updateDir(self):
        if self.posInBody <= 1:
            self.bodyDist = snake.previousDist
        else:
            self.bodyDist = snake.body[(self.posInBody - 2)].previousDist

    def moveBody(self):

        if self.bodyDist == "up":
            self.y -= 25
        elif self.bodyDist == "down":
            self.y += 25
        elif self.bodyDist == "right":
            self.x += 25
        elif self.bodyDist == "left":
            self.x -= 25

        self.previousDist = self.bodyDist


class Snake(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.snakeDist = "up"
        self.body = []
        self.bodySize = 0
        self.previousDist = None

        self.countdownToMove = 0
        self.delayToMove = 9

    def moveSnake(self):
        self.countdownToMove += 1

        if self.countdownToMove == self.delayToMove:

            if self.snakeDist == "up":
                self.y -= 25
            elif self.snakeDist == "down":
                self.y += 25
            elif self.snakeDist == "right":
                self.x += 25
            elif self.snakeDist == "left":
                self.x -= 25

            for body in self.body:
                body.moveBody()
                if self.x == body.x and self.y == body.y:
                    gameOver()

            self.countdownToMove = 0
            self.previousDist = self.snakeDist

    def drawSnake(self):
        win.blit(snakeHeadAlive, (self.x, self.y))
        for body in self.body:
            body.draw()


snake = Snake(13 * 25, 13 * 25)


def gameOver():
    global gameLoop, score, foodOnScreen

    button0Rect = pygame.Rect(225, 250, 200, 50)
    button1Rect = pygame.Rect(225, 450, 200, 50)

    pygame.display.set_caption(f"Game Over | Score: {str(score)}")

    score = 0
    foodOnScreen = False
    gameLoop = False

    while not gameLoop:

        clock.tick(fps)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        mouseX, mouseY = pygame.mouse.get_pos()

        if button0Rect.collidepoint(mouseX, mouseY):
            if clicked:
                gameLoop = True
                pygame.display.set_caption("Snake | Score: 0")
                run()

        elif button1Rect.collidepoint(mouseX, mouseY):
            if clicked:
                sys.exit()

        renderText("Game Over", 54, (0, 0), 650, 250, (255, 255, 255))

        pygame.draw.rect(win, (255, 255, 255), button0Rect)
        renderText("Play Again", 25, (button0Rect[0], button0Rect[1]), 200, 50)

        pygame.draw.rect(win, (255, 255, 255), button1Rect)
        renderText("Quit", 25, (button1Rect[0], button1Rect[1]), 200, 50)

        pygame.display.update()


def run():
    global snake, foodOnScreen

    food = Food(0, 0)

    while gameLoop:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()

        win.fill((0, 0, 0))

        if not foodOnScreen:
            food.x = random.randint(1, 25) * 25
            food.y = random.randint(1, 25) * 25
            foodOnScreen = True

        # SNAKE MOVEMENT

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            snake.snakeDist = "right"
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            snake.snakeDist = "left"
        elif keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN]:
            snake.snakeDist = "up"
        elif keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            snake.snakeDist = "down"

        for body in snake.body:
            body.updateDir()

        food.draw()
        snake.moveSnake()
        snake.drawSnake()
        food.getCollision()

        # CHECKS IF SNAKE TOUCH THE BORDER
        if snake.x == 650 or snake.x == -25 or snake.y == 650 or snake.y == -25:
            gameOver()

        pygame.display.update()


run()
