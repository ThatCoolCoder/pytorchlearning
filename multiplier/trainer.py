print('Importing pytorch...')

import matplotlib.pyplot as plt

# import libraries 
import torch
import torch.nn as nn
from torch.autograd import Variable

from model import Multiplier, MODEL_FILE_NAME

TRANING_DATA_SIZE = 11

Xs = []
Ys = []
for i in range(TRANING_DATA_SIZE):
    for j in range(TRANING_DATA_SIZE):
        Xs.append([float(i), float(j)])
        Ys.append(float(i * j))

Xs = torch.Tensor(Xs)

Ys = torch.Tensor(Ys).reshape(Xs.shape[0], 1)

print('Initialising model...')

model = Multiplier()

epochs = 3000
mseloss = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.03)
all_losses = []
current_loss = 0
plot_every = 50

print('Training...')

for epoch in range(epochs):
    # input training example and return the prediction
    yhat = model.forward(Xs)

    # calculate MSE loss
    loss = mseloss(yhat, Ys)
    
    # backpropogate through the loss gradiants
    loss.backward()

    # update model weights
    optimizer.step()

    # remove current gradients for next iteration
    optimizer.zero_grad()

    # append to loss
    current_loss += loss
    if epoch % plot_every == 0:
        all_losses.append(current_loss / plot_every)
        current_loss = 0
    
    # print progress
    if epoch % 500 == 0:
        print(f'Epoch {epoch} completed')

print('Saving model...')

torch.save(model.state_dict(), MODEL_FILE_NAME)

print('Done')

plt.plot(all_losses)
plt.ylabel('Loss')
plt.show()