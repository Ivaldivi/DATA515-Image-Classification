from glob import glob
import os
from PIL import Image

import numpy as np 
from sklearn.metrics import accuracy_score, roc_auc_score, average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms  # type: ignore

from landmarks_dataset import LandmarkData

## Tensorboard: 
tb_writer = SummaryWriter("logs/wa_landmarks")

## Load the data: 
data_directory = "../data/Images/"
im_list = []
lab_list = []
landmarks = sorted(os.listdir(data_directory))

# loop through landmarks folders and download the data
for landmark in landmarks: 
    landmark_folder = os.path.join(data_directory, landmark)
    if os.path.isdir(landmark_folder): 
        images = glob(os.path.join(landmark_folder, "*.jpg"))
        for image_option in images:
            try:
                # Open and convert image to RGB
                image = Image.open(image_option).convert("RGB")

                # Convert to NumPy array & normalize (0-1)
                image_array = np.asarray(image) / 255.0

                # Append data
                im_list.append(image_array)
                lab_list.append(landmark)  # Use folder name as the label
            except Exception as e:
                print(f"Error loading {image_option}: {e}")

washington_images_stack = np.stack(im_list, axis=0)  # Shape: (N, H, W, C)
labels = np.array(lab_list)

# Encodes string landmark names into integer labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Split dataset into test and train sets
x_train, x_test, y_train, y_test = train_test_split(
    washington_images_stack, encoded_labels, test_size=0.2, random_state=42
)

# Split training set into train and validation sets
x_train, x_val, y_train, y_val = train_test_split(
    x_train, y_train, test_size=0.2, random_state=42
) # 0.16 = validation set

transform = transforms.Compose([
    # transforms.ToPILImage(),
    # transforms.RandomHorizontalFlip(),  
    # transforms.RandomRotation(30), 
    transforms.ToTensor(),  
    transforms.Resize((225, 225)),
    transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])  
])

train_data = LandmarkData(x_train, y_train, transform=transform)
test_data = LandmarkData(x_test, y_test, transform=transform)
val_data = LandmarkData(x_val, y_val, transform=transform)
# print("Val data: ", val_data.labels)

trainloader = DataLoader(train_data, batch_size=32, shuffle=True,num_workers=0)
testloader = DataLoader(test_data, batch_size=32, shuffle=False, num_workers=0)
val_loader = DataLoader(val_data, batch_size=32, shuffle=False, num_workers=0)

# print("Val Loader: ", val_loader)
# SET UP THE CNN:
class SimpleCNN(nn.Module):  
    def __init__(self):        
        super(SimpleCNN, self).__init__()
        
        ### 1st convolutional layer
        # Doc: https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html#torch.nn.Conv2d
        # Input: 3x225x225, Output: 32x225x225
        # in-channels = 3 because we have 3 color channels (R, G, B)
        # out-channels = 32, # of channels the layer will produce
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)

        # Reduces size by half, Output: 32x112x112
        # Doc: https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html#torch.nn.MaxPool2d
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)       

        ### 2nd convolutional layer
        # Input: 32x112x112, Output: 64x112x112
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)  

        ### Third convolutional layer        
        # Input: 64x112x112, Output: 128x112x112
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)  

        ### Fully connected layers
        # Doc: https://pytorch.org/docs/stable/generated/torch.nn.Linear.html#torch.nn.Linear
        # The output size after pooling is 128x28x28
        self.fc1 = nn.Linear(128 * 28 * 28, 512)  
        # Output for 0-305 categories
        self.fc2 = nn.Linear(512, 306)            

       ### Activation layer
        # Doc: https://pytorch.org/docs/stable/generated/torch.nn.ReLU.html#torch.nn.ReLU
        # if input is negative, output is 0, otherwise input
        self.relu = nn.ReLU()

    def forward(self, input_tensor):
        """
        Forward pass of the CNN model
        :param x: input tensor
        :return: output tensor
        """
        ### Pooling layers
        # Doc: https://pytorch.org/docs/stable/generated/torch.nn.functional.relu.html#torch.nn.functional.relu
        # input: 32x225x225 -> output: 32x112x112
        input_tensor = self.pool(self.relu(self.conv1(input_tensor)))  
        # input: 32x112x112 -> output: 64x56x56
        input_tensor = self.pool(self.relu(self.conv2(input_tensor))) 
        # input: 64x56x56 -> output: 128x28x28 
        input_tensor = self.pool(self.relu(self.conv3(input_tensor)))  

        # Flatten the tensor before feeding it into the fully connected layer
        input_tensor = input_tensor.view(-1, 128 * 28 * 28)  # Flatten: (batch_size, 128*28*28)

        # Fully connected layers
        input_tensor = self.relu(self.fc1(input_tensor))      # 512 hidden units
        input_tensor = self.fc2(input_tensor)                 # Output layer with 305 categories

        return input_tensor
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SimpleCNN()
cross_ent_loss = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
val_optimizer = optim.Adam(model.parameters(), lr=0.001)

writer = SummaryWriter('runs/wa-Landmarks')
dataiter = iter(trainloader)
images, labels = next(dataiter)

for epoch in range(10):
    running_train_loss = 0.0
    running_val_loss = 0.0
    iteration_count = 0
    val_iter = 0
    model.train()

    for inputs, labels in trainloader:
        inputs, labels = inputs.to(torch.float32), labels.to(torch.long)

        # Zero gradients for every batch
        optimizer.zero_grad()

        # Forward pass - compute outputs on input data using the model
        outputs = model(inputs)

        # Calculate loss
        loss = cross_ent_loss(outputs, labels)

        # Backpropagation
        loss.backward()
        
        # Update weights
        optimizer.step()
        
        # Accumulate batch loss
        running_train_loss += loss.item()
        
        # Log batch loss
        tb_writer.add_scalar("Loss/train", loss.item(), epoch * len(trainloader) + iteration_count)
        iteration_count += 1
    
    epoch_train_loss = running_train_loss / len(trainloader)
    # Set model to evaluation mode    
    model.eval()  
    running_val_loss = 0.0
    all_val_labels = []
    all_val_probs = []
    with torch.no_grad():

        for val_inputs, val_labels in val_loader: 
            val_inputs, val_labels = val_inputs.to(torch.float32), val_labels.to(torch.long)

            # Forward pass only
            val_outputs = model(val_inputs)
            val_loss = cross_ent_loss(val_outputs, val_labels)

            # Calculate probabilities
            val_probs = F.softmax(val_outputs, dim=1)

            # # Doc: https://pytorch.org/docs/stable/generated/torch.nn.functional.one_hot.html#torch.nn.functional.one_hot
            # # Converts labels to one-hot encoding
            # Accumulate predictions and labels for epoch-level metrics
            all_val_labels.append(torch.nn.functional.one_hot(val_labels, num_classes=306).float().cpu().numpy())
            all_val_probs.append(val_probs.cpu().numpy())

            # Accumulate loss
            running_val_loss += val_loss.item()

            # Log batch validation loss
            tb_writer.add_scalar("Loss/val", val_loss.item(), epoch * len(val_loader) + val_iter)
            val_iter += 1

    model.train()
    
    # Calculate epoch-level validation metrics
    epoch_val_loss = running_val_loss / len(val_loader)
    
    # Combine all batches for metrics calculation
    all_val_labels = np.vstack(all_val_labels)
    all_val_probs = np.vstack(all_val_probs)
    
    # Calculate epoch-level ROC AUC and Average Precision
    epoch_roc_auc = roc_auc_score(all_val_labels, all_val_probs, multi_class="ovr")
    epoch_avg_precision = average_precision_score(all_val_labels, all_val_probs)
    
    # Log epoch-level metrics
    tb_writer.add_scalar("Epoch/train_loss", epoch_train_loss, epoch)
    tb_writer.add_scalar("Epoch/val_loss", epoch_val_loss, epoch)
    tb_writer.add_scalar("Epoch/roc_auc", epoch_roc_auc, epoch)
    tb_writer.add_scalar("Epoch/avg_precision", epoch_avg_precision, epoch)
    
    # Print epoch summary
    print(f"Epoch {epoch+1}/{10}, Train Loss: {epoch_train_loss:.4f}, Val Loss: {epoch_val_loss:.4f}, ROC AUC: {epoch_roc_auc:.4f}, Avg Precision: {epoch_avg_precision:.4f}")
    
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in testloader:
        inputs, labels = inputs.to(torch.float32), labels.to(torch.float32)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Test Accuracy: {100 * correct / total:.2f}%")
torch.save(model, 'wa_landmarks_1.pth')
tb_writer.flush()
