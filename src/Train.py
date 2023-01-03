import argparse
import os
import shutil
from random import random, randint, sample

import numpy as np
import torch
import torch.nn as nn
from tensorboardX import SummaryWriter

from Model import DeepQNetwork
from PreProcessing import preProcessing
from FlappyBird import FlappyBird

def _args():
    parser = argparse.ArgumentParser(
        """Implementation of Deep Q Network to play Flappy Bird""")
    parser.add_argument("--imageSize", type=int, default=84, help="The common width and height for all images")
    parser.add_argument("--batch", type=int, default=32, help="The number of images per batch")
    parser.add_argument("--optimizer", type=str, choices=["sgd", "adam"], default="adam")
    parser.add_argument("--learningRate", type=float, default=1e-6)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument("--epsilon0", type=float, default=0.1)
    parser.add_argument("--epsilon1", type=float, default=1e-4)
    parser.add_argument("--numberIters", type=int, default=3000000)
    parser.add_argument("--replayMemorySize", type=int, default=50000,
                        help="Number of epoches between testing phases")
    parser.add_argument("--logPath", type=str, default="tensorboard")
    parser.add_argument("--modelPath", type=str, default="trainedModels")

    args = parser.parse_args()
    return args

def train(opt):
    if(torch.cuda.is_available):
        #print("ok")
        torch.cuda.manual_seed(123)
    else:
        #print("ko ok")
        torch.manual_seed(123)

    model = DeepQNetwork()

    if os.path.isdir(opt.logPath):
        shutil.rmtree(opt.logPath)
    
    os.makedirs(opt.logPath)
    writer = SummaryWriter(opt.logPath)
    optimizer = torch.optim.Adam(model.parameters(), lr=opt.learningRate)
    criterion = nn.MSELoss()
    game = FlappyBird()
    image, reward, done = game.play(0) 
    image = preProcessing(image[:game.SCREEN_WIDTH, :int(game.SCREEN_HEIGHT*0.90)], opt.imageSize, opt.imageSize)
    image = torch.from_numpy(image)
    if torch.cuda.is_available():
        print("ok")
        model.cuda()
        image = image.cuda()
    state = torch.cat(tuple(image for _ in range(4)))[None, :, :, :]
    
    replayMemory = [] # Store all the [state, action, reward, nextState, done] at a specific size for long term train
    epoch = 0
    while epoch < opt.numberIters:
        predict = model(state)[0]
        # Exploration vs Exploitation
        epsilon = opt.epsilon1 + ((opt.numberIters - epoch) * (opt.epsilon0 - opt.epsilon1) / opt.numberIters)
        rand = random()
        randomAction = rand <= epsilon
        if randomAction: # Exploration
            print("Perform exploration")
            action = randint(0, 1)
        else: # Exploitation
            action = torch.argmax(predict).item()

        nextImage, reward, done = game.play(action)
        nextImage = preProcessing(nextImage[:game.SCREEN_WIDTH, :int(game.SCREEN_HEIGHT*0.90)], opt.imageSize, opt.imageSize)
        nextImage = torch.from_numpy(nextImage)
        
        if torch.cuda.is_available():
            nextImage = nextImage.cuda()
        nextState = torch.cat(tuple(nextImage for _ in range(4)))[None, :, :, :]

        replayMemory.append([state, action, reward, nextState, done])
        if len(replayMemory) > opt.replayMemorySize:
            del replayMemory[0]

        # Long-term train
        batch = sample(replayMemory, min(len(replayMemory), opt.batch))
        stateBatch, actionBatch, rewardBatch, nextStateBatch, doneBatch = zip(*batch)
        stateBatch = torch.cat(tuple(state for state in stateBatch))
        actionBatch = torch.from_numpy(np.array([[1, 0] if action == 0 else [0, 1] for action in actionBatch], dtype=np.float32))
        rewardBatch = torch.from_numpy(np.array(rewardBatch, dtype=np.float32)[:, None])
        nextStateBatch = torch.cat(tuple(state for state in nextStateBatch))

        if torch.cuda.is_available():
            stateBatch = stateBatch.cuda()
            actionBatch = actionBatch.cuda()
            rewardBatch = rewardBatch.cuda()
            nextStateBatch = nextStateBatch.cuda()

        currPredictBatch = model(stateBatch)
        nextPredictBatch = model(nextStateBatch)

        yBatch = torch.cat(tuple(reward if done else reward + opt.gamma * torch.max(predict)
                                 for reward, done, predict in zip(rewardBatch, doneBatch, nextPredictBatch)))
        qVal = torch.sum(currPredictBatch * actionBatch, dim=1)
        optimizer.zero_grad()

        loss = criterion(qVal, yBatch)
        loss.backward()
        optimizer.step()

        state = nextState
        epoch += 1

        print("Epoch: {}/{}, Action: {}, MSE Loss: {}, Epsilon: {}, Reward: {}, Q-value: {}". format(
              epoch + 1,
              opt.numberIters,
              action,
              loss,
              epsilon, 
              reward,
              torch.max(predict)))
        writer.add_scalar("Train/Loss", loss, epoch)
        writer.add_scalar("Train/Epsilon", epsilon, epoch)
        writer.add_scalar("Train/Reward", reward, epoch)
        writer.add_scalar("Train/Q-value", torch.max(predict), epoch)

        if (epoch + 1) % 1000000 == 0:
            torch.save(model, "{}/flappyBirdModel{}".format(opt.modelPath, epoch + 1))

    torch.save(model, "{}/flappyBirdModel".format(opt.modelPath))

if __name__ == "__main__":
    opt = _args()
    train(opt)