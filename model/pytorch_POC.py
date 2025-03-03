import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter

# remove previous runs' logs 
# rm -rf ./logs/

# Transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# INPUTS: LOAD DATASET
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True)
print(trainloader)
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=32, shuffle=False)


class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(64 * 8 * 8, 128)  # Assuming 32x32 input size
        self.fc2 = nn.Linear(128, 10)  # 10 output classes (CIFAR-10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)  # Flatten before feeding into FC layers
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    

## SET UP THE MODEL: 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SimpleCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
test_optimizer = optim.Adam(model.parameters(), lr=0.001)
writer = SummaryWriter('runs/fashion_mnist_experiment_1')
dataiter = iter(trainloader)
images, labels = next(dataiter)

# Training loop
# 10 epochs 
num_epochs = 10

def get_accuracy(pred, actual):
  assert len(pred) == len(actual)

  total = len(actual)
  _, predicted = torch.max(pred.data, 1)
  correct = (predicted == actual).sum().item()
  return correct / total


for epoch in range(num_epochs):
    running_training_loss = 0.0
    running_test_loss = 0.0
    for training_inputs, training_labels in trainloader:
        training_inputs, training_labels = training_inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        training_outputs = model(training_inputs)
        training_loss = criterion(training_outputs, training_labels)
        training_loss.backward()
        optimizer.step()
        training_accuracy = get_accuracy(training_outputs, training_labels)
        running_training_loss += training_loss.item()

    for test_inputs, test_labels in testloader: 
        test_inputs, test_labes = test_inputs.to(device), test_labels.to(device)
        test_optimizer.zero_grad()
        test_outputs = model(test_inputs)
        test_loss = criterion(test_outputs, test_labels)
        test_loss.backward()
        test_optimizer.step()

        running_test_loss += test_loss.item()
    
    print(f"Epoch {epoch+1}, Training Loss: {running_training_loss/len(trainloader)}, Test Loss: {running_test_loss/len(testloader)}")

# Evaluate the model 
correct = 0
total = 0
model.eval()

with torch.no_grad():
    for inputs, labels in testloader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Test Accuracy: {100 * correct / total:.2f}%")


# Add-ons from tutorial: Save model- 
torch.save(model, 'cifar10_test_model.pth')