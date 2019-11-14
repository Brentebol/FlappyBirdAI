# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:42:41 2019

@author: brent
"""
import numpy as np
import pygame as pg
import random as rnd
import torch

from Neural_network_flappy import Brain

use_gpu = torch.cuda.is_available()
if use_gpu:
    device = torch.device('cuda:0' if use_gpu else 'cpu')


class Bird(): 
    def __init__(self, net = False):
        self.y = float(400)
        self.x = 100
        self.velocity = 0
        self.accel = 0.2
        self.is_alive = True
        
        self.score = 0
        self.fit = 0
        if net:
            self.nn = net
        else:
            self.nn = Brain().cuda()
        
        #pygame variables
        self.color = (255,255,255)
        self.size = 10
    
    def jump(self):
        self.velocity = -6
        
    def update(self):
        self.velocity += self.accel
        self.y += self.velocity
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        
    def check_collision(self, pipe, reso):
        if self.y >= reso[1]:
            return True
        if self.y >= pipe.h2 and (self.x <= pipe.x2 and self.x >= pipe.x1):
            return True
        elif self.y <= pipe.h1 and (self.x <= pipe.x2 and self.x >= pipe.x1):
            return True
    
    def Get_NN_Input(self, pipe, reso):
        #Make 5 inputs: X dist self-pipe_start, X dist self-pipe_end, Y distance self-pipe_top, Y dist self-pipe_bot, self.velocity:
        inputs = [0]*6
        inputs[0] = (pipe.x1 - self.x) / reso[0]
        inputs[1] = (pipe.x2 - self.x) / reso[0]
        inputs[2] = (pipe.h1 - self.y) / reso[1]
        inputs[3] = (pipe.h2 - self.y) / reso[1]
        inputs[4] = self.velocity / 100  #arbitrary
        inputs[5] = self.x / reso[0]
        return inputs
    
class Pipe():
    def __init__(self,reso):
        self.width = 15
        self.gap = 100
        self.speed = -1
        self.x1 = reso[0]
        self.x2 = self.x1 + self.width
        self.h1 = int(np.random.random() * (reso[1] - self.gap))
        self.h2 = self.h1 + self.gap
        
        self.new_possible = True
        
        #pygame variable
        self.color = (255,255,255)
        self.maxima = (0, reso[1])
        
    def move(self):
        self.x1 = self.x1 + self.speed
        self.x2 = self.x1 + self.width
        
    def remove(self):
        if self.x2 < 0:
            return True
        else:
            return False
        
    def make_new(self):
        if self.x2 < 125 and self.new_possible == True:
            self.new_possible = False
            return True
        else:
            return False
    
def Get_Amount(add_class ,number):
    lst = [0] * number
    for i in range(number):
        lst[i] = add_class.__class__()
    return lst
        
def Get_Next(pipes):
    if len(pipes) == 1:
        return pipes[0]
    elif pipes[0].x2 > 95:
        return pipes[0]
    else: 
        return pipes[1]
    
def Pipes_passed(pipes):
    if pipes[0].x2 == 100:
        return True
    else:
        return False
            
        
        