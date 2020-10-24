import os
from shutil import copy2
import tensorflow as tf 
import numpy as np 

# code based on this tutorial:
# https://towardsdatascience.com/implementing-a-fully-convolutional-network-fcn-in-tensorflow-2-3c46fb61de3b

# define number of classes based on number of folders in image directory
path = './data/images'
number_classes = sum(os.path.isdir(os.path.join(path, i)) for i in os.listdir(path))

# prepare data for ingestion into model
# data will come into data/images/{classname}, so we need to shuffle and split into train 
# and validation sets. we set it up to get 350 images per class, so we'll use 300 train,
# 50 validate
def prepare_data(path, train_images=300, val_images=50):
    print(f"Preprocessing data from images folder, {number_classes} classes found")
    # list classes in the folder
    classes = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

    # create dir for shuffled and split data
    shuffled_path = path + '_split'
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
    return True

# define the model
def fcn_model(dropout_rate=0.2):
    try:
        # input layer set to (None,None) to allow for variable inputs
        input_layer = tf.keras.layers.Input(shape=(None, None, 3))

        x = tf.keras.layers.Conv2D(filters=32, kernel_size=3, strides=1)(input_layer)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)

        x = tf.keras.layers.Conv2D(filters=64, kernel_size=3, strides=1)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)

        x = tf.keras.layers.Conv2D(filters=128, kernel_size=3, strides=2)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)

        x = tf.keras.layers.Conv2D(filters=256, kernel_size=3, strides=2)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)

        x = tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=2)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)

        # Fully connected layer 1
        x = tf.keras.layers.Conv2D(filters=64, kernel_size=1, strides=1)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)

        # Fully connected layer 2
        x = tf.keras.layers.Conv2D(filters=number_classes, kernel_size=1, strides=1)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.GlobalMaxPooling2D()(x)
        predictions = tf.keras.layers.Activation('softmax')(x)

        model = tf.keras.Model(inputs=input_layer, outputs=predictions)
        
        print(model.summary())
        print(f'Total number of layers: {len(model.layers)}')

        return model
    
    except Exception as e: 
        print(f"an error occured in function 'fcn_model': {e}")

if __name__ == '__main__':
    prepare_data('data/images')
    #fcn_model()