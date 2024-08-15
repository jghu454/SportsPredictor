
import torch
import torch.nn as nn # All neural network modules, nn.Linear, nn.Conv2d, BatchNorm, Loss functions
import torch.optim as optim # For all Optimization algorithms, SGD, Adam, etc.
import torch.nn.functional as F # All functions that don't have any parameters
from torch.utils.data import DataLoader # Gives easier dataset managment and creates mini batches
import torchvision.datasets as datasets # Has standard datasets we can import in a nice and easy way
import torchvision.transforms as transforms # Transformations we can perform on our dataset

class Swish(nn.Module):
    def forward(self, x):
        return x * torch.sigmoid(x)

class proplay_prediction(nn.Module):


    
    def __init__(self, input_size, output_size=2):
        super(proplay_prediction, self).__init__()
        self.layer1 = nn.Linear(input_size, 15)
        self.prelu1 = nn.PReLU()  # PReLU after the first layer
        
        self.layer2 = nn.Linear(15, 10)
        self.prelu2 = nn.PReLU()  # PReLU after the second layer
        
        self.layer3 = nn.Linear(10, 5)
        self.prelu3 = nn.PReLU()  # PReLU after the third layer
        
        self.layer4 = nn.Linear(5, output_size)

    def forward(self, input):
        # First layer
        result = self.layer1(input)
        result = self.prelu1(result)  # Use PReLU activation

        # Second layer
        result = self.layer2(result)
        result = self.prelu2(result)  # Use PReLU activation

        # Third layer
        result = self.layer3(result)
        result = self.prelu3(result)  # Use PReLU activation

        # Final layer (output)
        result = self.layer4(result)

        return result
    



#time to train NN