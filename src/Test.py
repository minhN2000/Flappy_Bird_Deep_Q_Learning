import argparse
import torch
from Model import DeepQNetwork
from PreProcessing import preProcessing
from FlappyBird import FlappyBird

def get_args():
    parser = argparse.ArgumentParser(
        """Implementation of Deep Q Network to play Flappy Bird""")
    parser.add_argument("--imageSize", type=int, default=84, help="The common width and height for all images")
    parser.add_argument("--savedPath", type=str, default="trainedModels")

    args = parser.parse_args()
    return args

def test(opt):
    if torch.cuda.is_available():
        torch.cuda.manual_seed(123)
    else:
        torch.manual_seed(123)
    if torch.cuda.is_available():
        model = torch.load("{}/flappyBirdModel1000000".format(opt.savedPath))
    else:
        model = torch.load("{}/flappyBirdModel1000000".format(opt.savedPath), map_location=lambda storage, loc: storage)
    model.eval()
    game = FlappyBird()
    image, reward, done = game.play(0)
    image = preProcessing(image[:game.SCREEN_WIDTH, :int(game.SCREEN_HEIGHT*0.90)], opt.imageSize, opt.imageSize)
    image = torch.from_numpy(image)
    if torch.cuda.is_available():
        model.cuda()
        image = image.cuda()
    state = torch.cat(tuple(image for _ in range(4)))[None, :, :, :]

    while True:
        prediction = model(state)[0]
        action = torch.argmax(prediction).item()

        nextImage, reward, terminal = game.play(action)
        nextImage = preProcessing(nextImage[:game.SCREEN_WIDTH, :int(game.SCREEN_HEIGHT*0.90)], opt.imageSize, opt.imageSize)
        nextImage = torch.from_numpy(nextImage)
        if torch.cuda.is_available():
            nextImage = nextImage.cuda()
        nextState = torch.cat((state[0, 1:, :, :], nextImage))[None, :, :, :]

        state = nextState

if __name__ == "__main__":
    opt = get_args()
    test(opt)