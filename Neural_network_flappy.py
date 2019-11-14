# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:18:44 2019

@author: brent
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

global device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Brain(nn.Module):
    def __init__(self, num_input=6, num_output = 1):
        super(Brain, self).__init__()
        self.fc1 = nn.Linear(num_input, 8)
        self.fc2 = nn.Linear(8, num_output)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.sigmoid(self.fc2(x))
        return x

def Get_FCNet(number):
    lst = [0] * number
    for i in range(number):
        lst[i] = FCNet().__class__().cuda()
    return lst


        
    


















