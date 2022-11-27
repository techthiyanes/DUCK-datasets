import os
from torchvision.io import read_image

file_paths = os.listdir()[0]
im = read_image(os.path.join(os.getcwd(), file_paths + "/png/" + "out1"))
print(im.shape)


