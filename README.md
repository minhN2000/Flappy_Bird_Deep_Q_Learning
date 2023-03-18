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

https://user-images.githubusercontent.com/71093113/224202462-3c351bea-25d8-4a3b-9e1f-53cbfcde22f3.mp4


## References
- [Flappy Bird with Pygame](https://www.youtube.com/watch?v=GiUGVOqqCKg&list=PLjcN1EyupaQkz5Olxzwvo1OzDNaNLGWoJ&ab_channel=CodingWithRuss) by Coding with Russ.
- [Deep Reinforcement Learning in Action](https://www.google.com/search?q=deep+reinforcement+learning+in+action&rlz=1C1RXQR_enUS979US979&oq=Deep+Reinforcement+Learning+in+Action&aqs=chrome.0.0i512j0i20i263i512l2j0i512j0i22i30l6.289j0j4&sourceid=chrome&ie=UTF-8&si=AEcPFx71Yi7YECiZ82vRWCw7NKNJZ9ALQCf9tGTuvAPobXXiAjWvB9O85LB0jABkF010LGls-BHl5YzswLEyR1YGLUuzntVbMXRz_0_HacVYtI48AFmt-hxu7lQXe71_nqaZZpz7F5VnorMEfVssoHZ_5zbUb-e1Lg%3D%3D&ictx=1&ved=2ahUKEwi9goCKoND9AhWolGoFHb6NCZ4QnZMFegQIaxAC) by Zai and Brown.
- [The Deep Reinforcement Learning Course](https://huggingface.co/deep-rl-course/unit0/introduction) by the Hugging Face team.
