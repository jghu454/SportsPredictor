import torch
import torch.nn as nn # All neural network modules, nn.Linear, nn.Conv2d, BatchNorm, Loss functions
import torch.optim as optim # For all Optimization algorithms, SGD, Adam, etc.
import torch.nn.functional as F # All functions that don't have any parameters
from torch.utils.data import DataLoader # Gives easier dataset managment and creates mini batches
import torchvision.datasets as datasets # Has standard datasets we can import in a nice and easy way
import torchvision.transforms as transforms # Transformations we can perform on our dataset
from LeagueDataset import LeagueDataset
from torch.utils.data import DataLoader
from NeuralNetwork import proplay_prediction as network
from torch.optim.lr_scheduler import StepLR



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
input_size = 140
num_classes = 2
learning_rate = 0.001
num_epochs = 5000

data_loader = DataLoader(LeagueDataset('Summer24_LPL_Placements.csv'), batch_size=150, shuffle=True)

model = network(input_size).to(device)



# Assuming 'model' is your neural network, 'data_loader' is your DataLoader
optimizer = optim.Adam(model.parameters(), lr=learning_rate)  # Set up the optimizer
criterion = torch.nn.CrossEntropyLoss()  # Loss function


for epoch in range(num_epochs):  # Loop over the dataset multiple times
    for batch in data_loader:
        inputs = batch['features']
        labels = batch['label']
        optimizer.zero_grad()  # Clear the gradients, important for each backpropagation pass

        # Forward pass
        outputs = model(inputs)  # Get model outputs
        loss = criterion(outputs, labels)  # Calculate the loss

        # Backward pass
        loss.backward()  # Compute gradient of the loss with respect to model parameters
        optimizer.step()  # Update parameters
    
    print(f'Epoch {epoch + 1}, Loss: {loss.item()}')

# After the training loop
torch.save(model.state_dict(), 'model_weights.pth')


"""print(data_loader)
for batch in data_loader:
    print(batch['labels'])"""
    
    
    