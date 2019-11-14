# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:41:54 2019

@author: brent
"""

import pygame as pg

class screen():
    def __init__(self, reso):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.grey = (100,100,100)
        
        self.resolution = reso
        
        pg.init()
        pg.font.init()
        self.font = pg.font.SysFont("monospace", 20)
        return
    
    def show(self):
        scr = pg.display.set_mode((self.resolution))
        return scr
    
    @staticmethod
    def close():
        pg.display.quit()
    
    @staticmethod
    def Draw():
        pg.display.flip()
    
    def RedrawText(self, disp, generation, amount, score):
        label = self.font.render("Generation: " + str(generation),1,(255,255,255))
        disp.blit(label,(10,6))
        label = self.font.render("Birds left: " + str(amount),1,(255,255,255))
        disp.blit(label,(10,24))
        label = self.font.render("Score: " + str(score),1,(255,255,255))
        disp.blit(label,(10,44))
        #print("printed")
    
    
    def Draw_Window(self, disp, birds, pipes):
        disp.fill(self.black)
        
        for bird in birds:
            pg.draw.circle(disp, bird.color, (bird.x, int(bird.y)), bird.size)
            
        for pipe in pipes:
            top = [(pipe.x1, pipe.maxima[0]), (pipe.x1, pipe.h1), (pipe.x2, pipe.h1), (pipe.x2,pipe.maxima[0])]
            bottom = [(pipe.x1, pipe.maxima[1]), (pipe.x1, pipe.h2), (pipe.x2, pipe.h2), (pipe.x2,pipe.maxima[1])]
            pg.draw.polygon(disp, pipe.color,(top))
            pg.draw.polygon(disp, pipe.color,(bottom))

