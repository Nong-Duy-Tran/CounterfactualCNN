import tensorflow as tf
import keras
from keras import layers
from FrameGenerator import Modified_Frame_Generator
from MainClass import Conv2Plus1D, ResidualMain, ResizeVideo, add_residual_block
import numpy as np

# Define the dimensions of one frame in the set of frames created
HEIGHT = 224
WIDTH = 224

n_frames = 10
batch_size = 8
output_signature = (tf.TensorSpec(shape = (None, None, None, 3), dtype = tf.float32),
                    tf.TensorSpec(shape = (), dtype = tf.int16))


dataset_path = r"D:\Dataset\archive\UCF101TrainTestSplits-RecognitionTask\ucfTrainTestlist\trainlist03.txt"
index_path = r"D:\Dataset\archive\UCF101TrainTestSplits-RecognitionTask\ucfTrainTestlist\classIndFull.txt"


generator = Modified_Frame_Generator(dataset_path, index_path, n_frames, training =True)

modified_train_ds = tf.data.Dataset.from_generator(generator,
                                          output_signature = output_signature)

modified_train_ds = modified_train_ds.batch(batch_size)



input_shape = (None, 10, HEIGHT, WIDTH, 3)
input = layers.Input(shape=(input_shape[1:]))
x = input

x = Conv2Plus1D(filters=16, kernel_size=(3, 7, 7), padding='same')(x)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)
x = ResizeVideo(HEIGHT // 2, WIDTH // 2)(x)

# Block 1
x = add_residual_block(x, 16, (3, 3, 3))
x = ResizeVideo(HEIGHT // 4, WIDTH // 4)(x)

# Block 2
x = add_residual_block(x, 32, (3, 3, 3))
x = ResizeVideo(HEIGHT // 8, WIDTH // 8)(x)

# Block 3
x = add_residual_block(x, 64, (3, 3, 3))
x = ResizeVideo(HEIGHT // 16, WIDTH // 16)(x)

# Block 4
x = add_residual_block(x, 128, (3, 3, 3))

x = layers.GlobalAveragePooling3D()(x)
x = layers.Flatten()(x)
x = layers.Dense(10)(x)

model = keras.Model(input, x)


frames, label = next(iter(modified_train_ds))
print(np.array(frames).size)
model.build(frames)

model.compile(loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              optimizer = keras.optimizers.Adam(learning_rate = 0.0001), 
              metrics = ['accuracy'])

model.fit(x=modified_train_ds, epochs=50)