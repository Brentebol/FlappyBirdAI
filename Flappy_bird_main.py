# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 21:48:43 2019

@author: brent
"""
import numpy as np
import pygame as pg
import time as time
import torch
import matplotlib.pyplot as plt

from Neural_network_flappy import *
from Genetic_algoritm import *
from Classes import *
from Screen_fb import *


#genetic algortihm paratmers
ga_population = 200
num_immigrants = 10
mutation_rate = 0.05
#game paramters
reso = (400,600)
show = 100
timestep = 0.1 #in seconds

#pygame stuff
display = screen(reso)
surface = display.show()

#neural network stuff
use_gpu = torch.cuda.is_available()
if use_gpu:
    device = torch.device('cuda:0' if use_gpu else 'cpu')

#looping stuff
main_loop = True
game_loop = True
debug = False

#
try:
    first_run  == False
except:
    generation = 0
    ga_scores = []
    birds = Get_Amount(Bird(), ga_population)
    saved_birds = []
    pipes = [Pipe(reso)]

while main_loop == True:
    count = 0
    max_score = 0
    generation += 1
    game_loop = True
    pipes_passed = 0
    passed = False
    
    while game_loop == True :
        if count % 1 == 0:
            pg.event.pump()
            display.Draw_Window(surface, birds, pipes)
            display.RedrawText(surface, generation, len(birds), pipes_passed)
            display.Draw()
        
        time.sleep(0.005)
        count += 1
        
        tst = pg.key.get_pressed()
        
        #game controls
        if tst[pg.K_ESCAPE]:
            game_loop = False
            main_loop = False
            debug= True
            break
        
        if tst[pg.K_q] or pipes_passed == 25:
            for bird in birds:
                bird.is_alive = False
        
        if tst[pg.K_w]:
            main_loop = False
            first_run = False
        
        #section for game
        for pipe in pipes:
            if pipe.remove():
                pipes.remove(pipe)
            if pipe.make_new():
                pipes.append(Pipe(reso))
                
        next_pipe = Get_Next(pipes)
        if Pipes_passed(pipes):
            pipes_passed += 1
            
        for bird in birds:
            if bird.check_collision(pipes[0], reso):
                bird.is_alive = False
            if bird.is_alive == False:
                saved_birds.append(bird)
                birds[birds.index(bird)] = 0
                birds.remove(0)
                del bird
            elif bird.is_alive == True:
                bird.score += 1
                max_score = max(bird.score, max_score)
        
                
                NN_input = bird.Get_NN_Input(next_pipe,reso)
                NN_input = torch.Tensor(NN_input).view(-1, len(NN_input)).to(device)
                NN_output = float(bird.nn(NN_input))
                if NN_output > 0.5 and bird.velocity >= 0:
                    bird.jump()
        
        #check if there are any bird left
        if birds == []:
            break
            
        #Move birds and pipes
        for bird in birds:
            if bird.is_alive:
                bird.update()
            else:
                saved_birds.append(bird)
                birds[birds.index(bird)] = 0
                birds.remove(0)
                del bird
        for pipe in pipes:
            pipe.move()
                

                
    #continue from main_loop while
    if debug == True:
        break
    #rest pipes
    pipes = [Pipe(reso)]
    
    fit = []
    for bird in saved_birds:
        bird.score += np.random.randn() / (10**10)
        bird.fit = bird.score / max_score 
        fit.append(bird.score)
    mean_score = np.average(fit)
    sorted_fit = list(np.sort(fit)/max_score)
    ga_scores.append([max_score, mean_score])
    
    print('gen: '+str(generation), '  max score: ' + str(round(max_score,3)), '  mean score: ' + str(mean_score))
    
    elites = saved_birds[-5:]
    
    birds, parent_fit = breed(saved_birds, num_immigrants = 10)
    saved_birds = []    
    idx = [sorted_fit.index(a) for a in parent_fit]
    
    #put elites back in
    rnd_var = np.random.randint(0,len(birds),len(elites))
    for i, elite in zip(rnd_var, elites):
        birds[i] = Bird(elite.nn)
        birds[i].color = (0,255,0)
        
    
    plt.clf() #clear the current plot
    plt.subplot(211)
    plt.plot(ga_scores)
    plt.draw()
    
    plt.subplot(212)
    plt.plot(sorted_fit, 'bo')
    plt.plot(idx, parent_fit, 'rs')
    plt.draw()
            
#display.close()