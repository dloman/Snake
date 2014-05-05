#!/usr/bin/python

import pygame
import sys
import random
from pygame.locals import *

###############################################################################
Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
###############################################################################

###############################################################################
class Snake():
  def __init__(self):
    pygame.init()
    self.mFrameRate = 20
    self.mLineThickness = 10
    self.mWindowWidth = 800
    self.mWindowHeight = 700
    self.mDisplay = \
      pygame.display.set_mode((self.mWindowWidth,self.mWindowHeight))
    self.mClock = pygame.time.Clock()
    pygame.display.set_caption('Snake')
    MiddleX, MiddleY = self.mWindowWidth/2, self.mWindowHeight/2
    self.mSnakeLength = 3
    self.mSnake = [(MiddleX, MiddleY), \
      (MiddleX-self.mLineThickness,MiddleY), \
      (MiddleX-2*self.mLineThickness,MiddleY)]
    self.mSnakeXDirection = 1
    self.mSnakeYDirection = 0
    self.mFoodPosition = self.GetFoodPosition()

  #############################################################################
  def IsInsideOfSnake(self, x, y):
    for SnakeX, SnakeY in self.mSnake:
      SnakeXRange = range(SnakeX,SnakeX + self.mLineThickness)
      SnakeYRange = range(SnakeY,SnakeY + self.mLineThickness)
      if x in SnakeXRange or y in SnakeYRange:
        return False
    return True


  #############################################################################
  def GetFoodPosition(self):
    while True:
      x = random.randint( \
        self.mLineThickness, \
        self.mWindowWidth/self.mLineThickness)*self.mLineThickness
      y = random.randint( \
        self.mLineThickness, \
        self.mWindowHeight/self.mLineThickness)*self.mLineThickness
      if not self.IsInsideOfSnake(x, y):
        return x, y

  #############################################################################

  #############################################################################
  def DrawGame(self):
    self.DrawBorder()
    self.DrawFood()
    self.DrawSnake()
    pygame.display.update()

  #############################################################################
  def DrawBorder(self):
    self.mDisplay.fill(Black)
    pygame.draw.rect( \
      self.mDisplay, \
      White,\
      ((0,0),(self.mWindowWidth,self.mWindowHeight)), \
      self.mLineThickness*2)

  #############################################################################
  def DrawSnake(self):
    for x,y in self.mSnake:
      Rect = pygame.Rect(x, y, self.mLineThickness, self.mLineThickness)
      pygame.draw.rect(self.mDisplay, White, Rect)

  ##############################################################################
  def DrawFood(self):
    x,y = self.mFoodPosition
    Food = pygame.Rect(x,y, self.mLineThickness, self.mLineThickness)
    pygame.draw.rect(self.mDisplay, White, Food)

  ##############################################################################
  def GetNextHead(self):
    x,y = self.mSnake[0]
    x = x + self.mSnakeXDirection * self.mLineThickness
    y = y + self.mSnakeYDirection * self.mLineThickness
    return x, y
  ##############################################################################
  def MoveSnake(self):
    self.mSnake = [self.GetNextHead()] + self.mSnake[:-1]

  ##############################################################################
  def CheckForFoodCollision(self):
    pass

  ##############################################################################
  def CheckForWallCollision(self):
    x, y = self.mSnake[0]
    if x <= 0 or x + self.mLineThickness >= self.mWindowWidth:
      print 'GAME OVER'
      pygame.quit()
      exit()
    elif y <= self.mLineThickness or y + 2*self.mLineThickness >= self.mWindowHeight:
      print 'GAME OVER'
      pygame.quit()
      exit()

  ##############################################################################
  def HandleKeyPress(self, Event):
    if Event.key == K_DOWN:
      if self.mSnakeYDirection == 0:
        self.mSnakeXDirection = 0
        self.mSnakeYDirection = 1
    elif Event.key == K_UP:
      if self.mSnakeYDirection == 0:
        self.mSnakeXDirection = 0
        self.mSnakeYDirection = -1
    elif Event.key == K_RIGHT:
      if self.mSnakeXDirection == 0:
        self.mSnakeXDirection = 1
        self.mSnakeYDirection = 0
    elif Event.key == K_LEFT:
      if self.mSnakeXDirection == 0:
        self.mSnakeXDirection = -1
        self.mSnakeYDirection = 0
    elif Event.key == K_ESCAPE:
      pygame.quit()
      exit()

  ##############################################################################
  def Run(self):
    while True:
      try:
        for Event in pygame.event.get():
          if Event.type == QUIT:
            pygame.quit()
            exit()
          elif Event.type == KEYDOWN:
            self.HandleKeyPress(Event)

        self.DrawGame()
        self.mClock.tick(self.mFrameRate)
        self.MoveSnake()
        self.CheckForFoodCollision()
        self.CheckForWallCollision()
      except KeyboardInterrupt:
        pygame.quit()
        exit()
    pygame.quit()
    exit()

################################################################################
################################################################################
if __name__ == '__main__':
  SnakeGame = Snake()
  SnakeGame.Run()

