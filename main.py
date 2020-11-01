import os
from shutil import copy2
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np 
from collections import Counter


class BuildPredictor:
    def __init__(self, batch_size, img_path):
        self.batch_size = batch_size
        self.img_path = img_path

    # data will come into data/images/{classname}, so we need to shuffle and split into train 
    # and validation sets
    def preprocess_data(self, train_images=300, val_images=50):
        print(f"Preprocessing data from images folder, {number_classes} classes found")
        # list classes in the folder
        classes = [x for x in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, x))]

        # create dir for shuffled and split data
        shuffled_path = self.path + '_split'
        os.makedirs(shuffled_path, exist_ok=True)

        # create train & validation dirs in the shuffled dir
        print(f'Shuffling and sampling data: {train_images} training and {val_images} validation images per class')
        train_dir = os.path.join(shuffled_path, 'train')
        val_dir = os.path.join(shuffled_path, 'validate')
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)

        # finally, shuffle the data then copy into shuffled dir
        for class_name in classes:
            # first create ourput dirs
            class_train_dir = os.path.join(train_dir, class_name)
            class_val_dir = os.path.join(val_dir, class_name)
            os.makedirs(class_train_dir, exist_ok=True)
            os.makedirs(class_val_dir, exist_ok=True)

            # shuffle the data
            class_path = os.path.join(path, class_name)
            class_images = os.listdir(class_path)
            np.random.shuffle(class_images)

            # now sample from shuffled imgs into folders
            for image in class_images[:train_images]:
                copy2(os.path.join(class_path, image), class_train_dir)
            for image in class_images[train_images:train_images+val_images]:
                copy2(os.path.join(class_path, image), class_val_dir)   
        print(f"Done, images in {shuffled_path}")
        
        return shuffled_path


        def get_sizes(self):
            """
            returns a counter object counting the image sizes in the self.path directory,
            this will include all classes in the path as well
            """
            sizes = {}
            img_classes = [x for x in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, x))]
            
            for img_class in img_classes:
                train_path = img_class + '_split' + '/train/'
                sizes[img_class] = [Image.open(train_path + f).size for f in os.listdir]



if __name__ == '__main__':
    # define number of classes based on number of folders in image directory
    path = './data/images'
    number_classes = sum(os.path.isdir(os.path.join(path, i)) for i in os.listdir(path))
    # preprocess_data('data/images')