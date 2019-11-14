# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 21:04:19 2019

@author: brent
"""

import numpy as np
import torch
import random as rnd

from Neural_network_flappy import Brain
from Classes import Bird

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def Get_Fitness(score, max_score, min_score):
    x = score + abs(min_score) + 1
    x = x / (max_score + abs(min_score) + 1)
    return x

def New_Fitness(steps, apples):
    x = (steps) + ((2 ** apples) + (apples ** 2.1) * 15) - (((0.25 * steps) ** 1.3) * (apples**1.3))
    #y = (self._frames) + ((2**self.score) + (self.score**2.1)*500) - (((.25 * self._frames)**1.3) * (self.score**1.2))
    return x

#inputs the poulation, returns a new population of snakes.
def breed(population, mutation_rate = 0.05, num_immigrants = 0):
    #pop_size = len(population)
    new_population = [0] * len(population)
    parent_a = Select_Parent(population)
    parent_b = Select_Parent(population)
    parent_c = Select_Parent(population)
    
    while not(parent_a != parent_b != parent_c != parent_a):
        if parent_a == parent_b:
            parent_a = Select_Parent(population)
        elif parent_c == parent_b:
            parent_b = Select_Parent(population)
        elif parent_c == parent_a:
            parent_c = Select_Parent(population)
    
    for i in range(len(population)-num_immigrants):
        net = Brain().cuda()
        layer_count = 0
        for layer_a, layer_b, layer_c ,new_layer in zip(parent_a.nn.children(), parent_b.nn.children(),  parent_c.nn.children(), net.children()):
            layer_count += 1
            mask = torch.randint(0,3,layer_a.weight.shape, device = device)
            
            #crossover
            new_weight = torch.zeros(mask.shape).to(device)
            new_weight[mask == 0] = layer_a.weight[mask == 0]
            new_weight[mask == 1] = layer_b.weight[mask == 1]
            new_weight[mask == 2] = layer_c.weight[mask == 2]
             
            #mutation
            mask = torch.rand(layer_a.weight.shape)
            mutation = torch.randn(mask.shape, device = device)
            mutation = mutation * 0.25
            new_weight[mask < mutation_rate] = new_weight[mask < mutation_rate] + mutation[mask < mutation_rate]
            
            new_layer.weight = torch.nn.Parameter(new_weight)
            #new_layer = new_weight
        new_population[i] = Bird(net = net)
    
    for i in range(len(population)-num_immigrants, len(population)):
        new_population[i] = Bird()
        new_population[i].color = (0,150,255)
    
    parent_fit = [parent_a.fit, parent_b.fit, parent_c.fit]
    return new_population, parent_fit


#takes in the population and outputs a potential parent
def Select_Parent(population):
    for i in range(10000):        
        parent = rnd.choice(population)
        rnd_var = rnd.random()
        if rnd_var < parent.fit ** 3:
            return parent
            break