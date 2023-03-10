# Flappy Bird with Deep Q-Learning

This repository contains code for training an AI agent to play Flappy Bird using deep Q-learning.


## Installation

You need to have [Python](https://www.python.org/downloads/) installed on your system. Please install the necessary dependencies by running:
> pip install -r requirements.txt

## Usage

To train the AI agent, run:
```python
train.py [--options]
```
| Option | Description | Default Value |
| --- | --- | --- |
| `--optimizer` | The optimizer for backpropagation | adam |
| `--learningRate` | Learning rate to train the model | `1e-6` |
| `--epsilon0` | Start epsilon for exploration vs exploitation setting | `0.1` |
| `--epsilon1` | End epsilon for exploration vs exploitation setting | `1e-4` |
| `--numberIters` | Training Epoch | `3000000` |
| `--replayMemorySize` | Max batch sizes to store states of the game for 60 fps | `50000` |
| `--imageSize` | Input image size to the model | `86` |
| `--batch` | Batch for each train epoch| `64` |
| `--modelPath` | Model path | `trainedModels` |
| `--logPath` | Log path | `tensorboard` |

## Results

Current results show that the Bird averagely score 15 per play. I will keep update the training. Stay tuned.

https://github.com/minhN2000/Flappy_Bird_Deep_Q_Learning/blob/main/result/Flappy%20Bird%20Res%20v1.mp4

## References
