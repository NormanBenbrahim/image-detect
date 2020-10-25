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
    
    return shuffled_path


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


# generate image batches for variable image sizes. find the max height and width in all 
# images and then zero pad all other images to that size
def construct_generator(image_group, batch_size):
    # get max image shape
    max_shape = tuple(max(image.shape[x] for image in image_group) for x in range(3))

    # construct an image batch object
    image_batch = np.zeros((batch_size,) + max_shape, dtype='float32')

    # copy all images to the upper left part of the image batch object
    for image_index, image in enumerate(image_group):
        image_batch[image_index, :image.shape[0], :image.shape[1], :image.shape[2]] = image

    return image_batch


# model training
def train(model, train_generator, val_generator, epochs = 50):
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.0001),
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

    checkpoint_path = './snapshots'
    os.makedirs(checkpoint_path, exist_ok=True)
    model_path = os.path.join(checkpoint_path, 'model_epoch_{epoch:02d}_loss_{loss:.2f}_acc_{acc:.2f}_val_loss_{val_loss:.2f}_val_acc_{val_acc:.2f}.h5')
    
    history = model.fit_generator(generator=train_generator,
                                    steps_per_epoch=len(train_generator),
                                    epochs=epochs,
                                    callbacks=[tf.keras.callbacks.ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1)],
                                    validation_data=val_generator,
                                    validation_steps=len(val_generator))

    return history

# finally, a run function that does all of the above in sequence
def run(path):
    # prepare data
    data = prepare_data(path)
    model = fcn_model()
    


if __name__ == '__main__':
    prepare_data('data/images')
    #fcn_model()