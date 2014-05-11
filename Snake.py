#!/usr/bin/python

import os
import pickle
import pygame
import sys
import time

from pygame.locals import *
from itertools import cycle
from random import randint

###############################################################################
Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
Rainbow = cycle([Red,Green,Blue, (255,255,0),(255,0,255),(0,255,255)])
###############################################################################

###############################################################################
###############################################################################
class Snake():
  def __init__(self):
    pygame.init()
    self.mFrameRate = 20
    self.mLineThickness = 10
    self.mWindowWidth = 800
    self.mWindowHeight = 700
    self.mFont = pygame.font.Font('freesansbold.ttf',20)
    self.mBigFont = pygame.font.Font('freesansbold.ttf',40)
    self.mDisplay = \
      pygame.display.set_mode((self.mWindowWidth,self.mWindowHeight))
    self.mClock = pygame.time.Clock()
    pygame.display.set_caption('Snake')
    self.mGameOver = True

  #############################################################################
  def StartGame(self):
    MiddleX, MiddleY = self.mWindowWidth/2, self.mWindowHeight/2
    self.mSnakeLength = 3
    self.mSnake = [(MiddleX, MiddleY), \
      (MiddleX-self.mLineThickness,MiddleY), \
      (MiddleX-2*self.mLineThickness,MiddleY)]
    self.mSnakeXDirection = 1
    self.mSnakeYDirection = 0
    self.mFoodPosition = self.GetNextFoodPosition()
    self.mTimeSinceLastIncrease = time.time()
    self.mTimeSinceLastFood = time.time()
    self.mScore = 0

  #############################################################################
  def IsInsideOfSnake(self, x, y):
    for SnakeX, SnakeY in self.mSnake:
      SnakeXRange = range(SnakeX,SnakeX + self.mLineThickness)
      SnakeYRange = range(SnakeY,SnakeY + self.mLineThickness)
      if x in SnakeXRange and y in SnakeYRange:
        return True
    return False

  #############################################################################
  def GetHighScoreList(self):
    try:
      return pickle.load(\
        open(os.path.expanduser('~/') + '.SnakeHighScore.pickle','rb'))
    except IOError:
      return [0,0,0,0,0]

  #############################################################################
  def SaveHighScores(self):
    NewHighScoreList = []
    OldHighScores = self.GetHighScoreList()
    for HighScore in OldHighScores:
      if self.mScore > HighScore:
        NewHighScoreList.append(self.mScore)
        self.mScore = HighScore
      else:
        NewHighScoreList.append(HighScore)
    pickle.dump( \
      NewHighScoreList, \
      open(os.path.expanduser('~/') + '.SnakeHighScore.pickle','wb'))

  #############################################################################
  def GetNextFoodPosition(self):
    while True:
      x = randint( \
        self.mLineThickness, \
        (self.mWindowWidth-2*self.mLineThickness)/self.mLineThickness)*self.mLineThickness
      y = randint( \
        self.mLineThickness, \
        (self.mWindowHeight-2*self.mLineThickness)/self.mLineThickness)*self.mLineThickness
      self.mFoodColor = self.GetRandomColor()
      if not self.IsInsideOfSnake(x, y):
        return x, y

  #############################################################################
  def DrawMenu(self):
    NewGameSurface = \
      self.mBigFont.render('Press s to start a new game!', True, Red)
    NewGameRectangle = NewGameSurface.get_rect()
    NewGameRectangle.midbottom = (self.mWindowWidth/2,(self.mWindowHeight/4))

    HighScoreSurface = \
      self.mBigFont.render('Pess h to see high scores!', True, Blue)
    HighScoreRectangle = HighScoreSurface.get_rect()
    HighScoreRectangle.midtop = NewGameRectangle.midbottom

    EscapeSurface = \
      self.mBigFont.render('Pess Esc or Q to exit!', True, Green)
    EscapeRectangle = EscapeSurface.get_rect()
    EscapeRectangle.midtop = HighScoreRectangle.midbottom

    self.mDisplay.blit(NewGameSurface, NewGameRectangle)
    self.mDisplay.blit(HighScoreSurface, HighScoreRectangle)
    self.mDisplay.blit(EscapeSurface, EscapeRectangle)

  #############################################################################
  def DrawColorBorder(self):
    for xPos in range(self.mWindowWidth/10, 9*self.mWindowWidth/10, self.mLineThickness):
      TopRectangle = pygame.Rect(xPos,self.mWindowHeight/10, self.mLineThickness, self.mLineThickness)
      BottomRectangle = pygame.Rect(xPos,9*self.mWindowHeight/10, self.mLineThickness, self.mLineThickness)
      pygame.draw.rect(self.mDisplay, self.GetRandomColor(),TopRectangle)
      pygame.draw.rect(self.mDisplay, self.GetRandomColor(),BottomRectangle)
    for yPos in range(self.mWindowHeight/10, 9*self.mWindowHeight/10+self.mLineThickness,self.mLineThickness):
      LeftRectangle = pygame.Rect(self.mWindowWidth/10,yPos, self.mLineThickness, self.mLineThickness)
      RightRectangle = pygame.Rect(9*self.mWindowWidth/10,yPos, self.mLineThickness, self.mLineThickness)
      pygame.draw.rect(self.mDisplay, self.GetRandomColor(),LeftRectangle)
      pygame.draw.rect(self.mDisplay, self.GetRandomColor(),RightRectangle)


  #############################################################################
  def DrawStartScreen(self):
    self.DrawBorder()
    self.DrawMenu()
    self.DrawColorBorder()
    pygame.display.update()

  #############################################################################
  def DrawGame(self):
    self.DrawBorder()
    self.DrawFood()
    self.DrawSnake()
    self.DrawScore()
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
      pygame.draw.rect(self.mDisplay, next(Rainbow), Rect)

  ##############################################################################
  def GetRandomColor(self):
    return randint(0,255),randint(0,255),randint(0,255)
  ##############################################################################
  def DrawFood(self):
    x,y = self.mFoodPosition
    Food = pygame.Rect(x,y, self.mLineThickness, self.mLineThickness)
    pygame.draw.rect(self.mDisplay, self.mFoodColor, Food)

  ##############################################################################
  def GetNextHead(self):
    x,y = self.mSnake[0]
    x = x + self.mSnakeXDirection * self.mLineThickness
    y = y + self.mSnakeYDirection * self.mLineThickness
    return x, y
  ##############################################################################
  def MoveSnake(self):
    if time.time() - self.mTimeSinceLastIncrease > 5:
      self.mTimeSinceLastIncrease = time.time()
      self.mSnake = [self.GetNextHead()] + self.mSnake
    else:
      self.mSnake = [self.GetNextHead()] + self.mSnake[:-1]

  ##############################################################################
  def CheckForFoodCollision(self):
    if self.IsInsideOfSnake(self.mFoodPosition[0], self.mFoodPosition[1]):
      self.mScore += 100 * len(self.mSnake)
      self.mTimeSinceLastIncrease =-100
      self.mFoodPosition = self.GetNextFoodPosition()

  ##############################################################################
  def DisplayGameOver(self):
    GameOverSurface = self.mBigFont.render('GAME OVER', True, Red)
    GameOverRectangle = GameOverSurface.get_rect()
    GameOverRectangle.midbottom = (self.mWindowWidth/2,self.mWindowHeight/2)
    self.mDisplay.blit(GameOverSurface, GameOverRectangle)

    ScoreSurface = self.mBigFont.render('Score = %s' %(self.mScore), True, Red)
    ScoreRectangle = ScoreSurface.get_rect()
    ScoreRectangle.midtop = GameOverRectangle.midbottom
    self.mDisplay.blit(ScoreSurface, ScoreRectangle)

    pygame.display.update()
    time.sleep(3)

  ##############################################################################
  def Fail(self):
    self.DisplayGameOver()
    self.SaveHighScores()
    self.mGameOver = True

  ##############################################################################
  def CheckForSnakeCollision(self):
    if len(set(self.mSnake)) < len(self.mSnake):
      self.Fail()

  ##############################################################################
  def CheckForWallCollision(self):
    x, y = self.mSnake[0]
    if x <= 0 or x + self.mLineThickness >= self.mWindowWidth:
      self.Fail()
    elif y <= self.mLineThickness or y + 2*self.mLineThickness >= self.mWindowHeight:
      self.Fail()

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
    elif Event.key == K_ESCAPE or Event.key == 113:
      pygame.quit()
      exit()
    elif Event.key == 115:
      self.StartGame()
      self.mGameOver = False
    elif Event.key == 104:
      self.DrawHighScoreScreen()

  ##############################################################################
  def DrawHighScore(self, Place, Score):
    ScoreSurface = self.mFont.render('%s.  %s' %(Place +1, Score), True, next(Rainbow))
    ScoreRectangle = ScoreSurface.get_rect()
    ScoreRectangle.midbottom = \
      (self.mWindowWidth/2,self.mWindowHeight/4+ Place*self.mWindowHeight/8)
    self.mDisplay.blit(ScoreSurface,ScoreRectangle)
    pygame.display.update()

  ##############################################################################
  def DrawHighScoreScreen(self):
    self.DrawBorder()
    for Place, Score in enumerate(self.GetHighScoreList()):
      delay = time.time()
      while time.time() -delay < 1:
        self.DrawColorBorder()
        self.DrawHighScore(Place,Score)

    delay = time.time()
    while time.time() -delay < 3:
      self.DrawColorBorder()
      pygame.display.update()

  ##############################################################################
  def DrawScore(self):
    Surface = self.mFont.render('Score = %s' %(self.mScore), True, Green)
    Rectangle = Surface.get_rect()
    Rectangle.topleft = (self.mLineThickness*3, self.mLineThickness*2)
    self.mDisplay.blit(Surface,Rectangle)

  ##############################################################################
  def CheckIfStuck(self):
    if time.time() - self.mTimeSinceLastIncrease > 10:
      self.mFoodPosition = self.GetNextFoodPosition()

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

        if self.mGameOver:
          self.DrawStartScreen()
        else:
          self.DrawGame()
          self.mClock.tick(self.mFrameRate)
          self.MoveSnake()
          self.CheckForFoodCollision()
          self.CheckForWallCollision()
          self.CheckForSnakeCollision()
          self.CheckIfStuck()
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

