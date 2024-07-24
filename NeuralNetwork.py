
import torch
import torch.nn as nn # All neural network modules, nn.Linear, nn.Conv2d, BatchNorm, Loss functions
import torch.optim as optim # For all Optimization algorithms, SGD, Adam, etc.
import torch.nn.functional as F # All functions that don't have any parameters
from torch.utils.data import DataLoader # Gives easier dataset managment and creates mini batches
import torchvision.datasets as datasets # Has standard datasets we can import in a nice and easy way
import torchvision.transforms as transforms # Transformations we can perform on our dataset


class proplay_prediction(nn.Module):


    def __init__(self, input_size, output_size = 2):
        super(proplay_prediction,self).__init__()
        self.layer1 = nn.Linear(input_size,15)
        self.layer2  = nn.Linear(15, 10)
        self.layer3 = nn.Linear(10,5)
        self.layer4 = nn.Linear(5,output_size)

    def forward(self, input): #forward propogation
        #first layer
        result = self.layer1(input)
        result = F.relu(result)

        #second layer
        result = self.layer2(result)
        result = F.relu(result)

        #third layer
        result = self.layer3(result)
        result = F.relu(result)

        #final layer (output)
        result = self.layer4(result)

        return result
    



#time to train NN