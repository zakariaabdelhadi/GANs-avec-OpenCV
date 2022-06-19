#imports for cropping
import sys
import os
from os import listdir
from os.path import isfile, join
import  time
import cv2
import numpy
#END

from importlib.metadata import files

import tensorflow as tf

from keras import layers
from keras.layers import Input, Reshape, Dropout, Dense
from keras.layers import Flatten, BatchNormalization
from keras.layers import Activation, ZeroPadding2D
from keras.layers import LeakyReLU
from keras.layers import UpSampling2D, Conv2D
from keras.models import Sequential, Model, load_model
from keras.optimizers import nadam_v2  # Adam adam adam
import numpy as np
from PIL import Image
from tqdm import tqdm
import os
import time
import matplotlib.pyplot as plt
 #from colab import locale
# drive.mount('/content/drive')

import detect_gender as dg

#--------------- code korregiert von Tom ----------------------------------------
import cv2
import os
import sys
from os import listdir
from os.path import isfile, join
import time
import cv2
import numpy

# CODE TO MAKE THE CROPPING
p = 10
mypath = 'C:\\Users\\ZAKARIA\\Desktop\\New folder\\CFD Version 3.0\\Images\\tiri'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
images = numpy.empty(len(onlyfiles), dtype=object)

outputpath = os.path.join(mypath, 'cropped_resized_images')
outputpath2 = os.path.join(mypath, 'ohne_fehlerhafte_detection')

if not os.path.exists(outputpath):
        os.makedirs(outputpath)

if not os.path.exists(outputpath2):
        os.makedirs(outputpath2)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
for n in range(0, len(onlyfiles)):
        images[n] = cv2.imread(join(mypath, onlyfiles[n]))
        # hier entdecken wir Gesichter im Bild und schneiden wir sie aus (uns ist egal was das Bild nebenbei enthält )
        faces_detected = face_cascade.detectMultiScale(images[n], scaleFactor=1.1, minNeighbors=5)
        (x, y, w, h) = faces_detected[0]
        # cv2.rectangle(images[n], (x, y), (x + w, y + h), (0, 255, 0), 1)
        # hier schneiden wir das Gesicht genau aus
        face = images[n][y:y + h, x:x + w]

        dim = (300, 300)
        # resize image . hier verarbeiten wir die Größe der Bilder
        face = cv2.resize(face, dim, interpolation=cv2.INTER_AREA)
        # cv2.resize(face, dim, interpolation=cv2.INTER_LINEAR) # alternativ
        face = face[50:265, 50:250] # hart cropping
        face = cv2.resize(face, dim, interpolation=cv2.INTER_AREA)

        #hier anwenden wir den Filter "median Filter", um Noise im Bild zu entfernen
        face_median = cv2.medianBlur(src=face, ksize=5)     # Median filter "blur"
        # # image sharpening

        """
        It is very similar to the process of blurring, except that now, 
        instead of creating a kernel to average each pixel intensity, we are creating
         a kernel that will cause the pixel intensities to be higher and therefore 
         more prominent to the human eye.
         """

        # kernel = np.array([[0, -1, 0],
        #                    [-1, 5, -1],
        #                    [0, -1, 0]])
        # image_sharp = cv2.filter2D(src=face_median, ddepth=-1, kernel=kernel)
        # cv2.imshow('AV CV- Winter Wonder Sharpened', image_sharp)
        # cv2.waitKey()
        # hier machen wir alle Bilder im Gray scale d.h. ohne Farben außer mischung scala von Schwarz und weiß
        face_gray = cv2.cvtColor(face_median, cv2.COLOR_BGR2GRAY) # machen alle Bilder schwarz & Weiß

        cv2.imwrite(outputpath + "/Bild_bearbeitet_" + str(n) + ".png", face_gray)
        # in der Variable "accept" findet man 1 oder 100
        # 1: das Bild enthält kein Gesicht
        # 100: das Bild hat wirklich ein Gesicht entdeckt
        accept=dg.predict_gender(outputpath + "/Bild_bearbeitet_" + str(n) + ".png")
        print("der Wert von accept ist: "+str(accept))

        # wir speichern nur Bilder, die wirklich Gesichter beinhalten
        if (accept==100):
                print('Gesicht erfolgreich entdeckt')
                cv2.imwrite(outputpath2 + "/Bild_bearbeitet_" + str(n) + ".png",     face_gray)

# # --------------------------Geschlechterkennung-----------------------------------------------
#
# # das finden Sie in der Datei 'detect_gender.p'
#
#
#
# #-------------------------- END Preprocessing endet hier --------------------------
#

#--------------------------  BEGIN Preprocessing mit der ersten Methode _ hart cropping --------------------------

#     print('original dimension :', images[n].shape)  # Print image shape
#     scale_percent = 25  # percent of original size
#     width = int(images[n].shape[1] * scale_percent / 100)
#     height = int(images[n].shape[0] * scale_percent / 100)
#     dim = (width, height)
#     # resize image
#     resized = cv2.resize(images[n], dim, interpolation=cv2.INTER_AREA)
#     cropped_image = resized[150:350, 220:380] # hart cropping
#     cv2.imwrite('C:\\Users\\ZAKARIA\\Desktop\\New folder\\CFD Version 3.0\\Images\\cropped\\img' + str(n) + '.jpg',cropped_image)
#
# time.sleep(30)
#     #print('resized dimension :', resized.shape)  # Print image shape
#
# #cv2.waitKey(0)
#
# #cv2.destroyAllWindows()
# #END

# --------------------------  END Preprocessing mit der ersten Methode _ hart cropping --------------------------


# ------------------ BEGIN Generierung der Gesichter ---------------
GENERATE_RES = 3  # Generation resolution factor
# (1=32, 2=64, 3=96, 4=128, etc.)
GENERATE_SQUARE = 32 * GENERATE_RES  # rows/cols (should be square)
IMAGE_CHANNELS = 3

# Preview image
PREVIEW_ROWS = 4
PREVIEW_COLS = 7
PREVIEW_MARGIN = 16

# Size vector to generate images from
SEED_SIZE = 100

# Configuration
DATA_PATH = outputpath2
EPOCHS = 50
BATCH_SIZE = 32
BUFFER_SIZE = 60000

print(f"Will generate {GENERATE_SQUARE}px square images.")


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


training_binary_path = os.path.join(DATA_PATH,
                                    f'training_data_{GENERATE_SQUARE}_{GENERATE_SQUARE}.npy')

print(f"Looking for file: {training_binary_path}")

if not os.path.isfile(training_binary_path):
    start = time.time()
    print("Loading training images...")

    training_data = []
    faces_path = os.path.join(DATA_PATH)
    for filename in tqdm(os.listdir(faces_path)):

        path = os.path.join(faces_path, filename)
        image = Image.open(path).resize((GENERATE_SQUARE,
                                         GENERATE_SQUARE), Image.ANTIALIAS) # Image.ANTIALIAS
        training_data.append(np.asarray(image))
    training_data = np.reshape(training_data, (-1, GENERATE_SQUARE,
                                               GENERATE_SQUARE, IMAGE_CHANNELS))
    training_data = training_data.astype(np.float32)
    training_data = training_data / 127.5 - 1.

    print("Saving training image binary...")
    np.save(training_binary_path, training_data)
    elapsed = time.time() - start
    print(f'Image preprocess time: {hms_string(elapsed)}')
else:
    print("Loading previous training pickle...")
    training_data = np.load(training_binary_path)

# shuffle the data
train_dataset = tf.data.Dataset.from_tensor_slices(training_data) \
    .shuffle(BUFFER_SIZE).batch(BATCH_SIZE)


def build_generator(seed_size, channels):
    model = Sequential()

    model.add(Dense(4 * 4 * 256, activation="relu", input_dim=seed_size))
    model.add(Reshape((4, 4, 256)))

    model.add(UpSampling2D())
    model.add(Conv2D(256, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Activation("relu"))

    model.add(UpSampling2D())
    model.add(Conv2D(256, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Activation("relu"))

    # Output resolution, additional upsampling
    model.add(UpSampling2D())
    model.add(Conv2D(128, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Activation("relu"))

    if GENERATE_RES > 1:
        model.add(UpSampling2D(size=(GENERATE_RES, GENERATE_RES)))
        model.add(Conv2D(128, kernel_size=3, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))

    # Final CNN layer
    model.add(Conv2D(channels, kernel_size=3, padding="same"))
    model.add(Activation("tanh"))

    return model


def build_discriminator(image_shape):
    model = Sequential()

    model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=image_shape,
                     padding="same"))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
    model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(512, kernel_size=3, strides=1, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    return model


def save_images(cnt, noise):
    image_array = np.full((
        PREVIEW_MARGIN + (PREVIEW_ROWS * (GENERATE_SQUARE + PREVIEW_MARGIN)),
        PREVIEW_MARGIN + (PREVIEW_COLS * (GENERATE_SQUARE + PREVIEW_MARGIN)), 3),
        255, dtype=np.uint8)

    generated_images = generator.predict(noise)



    #cv2.imshow('rak hna zaki',generated_images)
   # cv2.waitKey()

    generated_images = 0.5 * generated_images + 0.5

    image_count = 0
    for row in range(PREVIEW_ROWS):
        for col in range(PREVIEW_COLS):
            r = row * (GENERATE_SQUARE + 16) + PREVIEW_MARGIN
            c = col * (GENERATE_SQUARE + 16) + PREVIEW_MARGIN
            image_array[r:r + GENERATE_SQUARE, c:c + GENERATE_SQUARE] \
                = generated_images[image_count] * 255
            if cnt == EPOCHS-1:
                cv2.imshow("Bild"+str(image_count)+" von 28",generated_images[image_count])
                cv2.waitKey(0)

            image_count += 1

    output_path = os.path.join(DATA_PATH, 'output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = os.path.join(output_path, f"train-{cnt}.png")
    im = Image.fromarray(image_array)
 #   im_median= cv2.medianBlur(src=im, ksize=5)  # Median filter "blur"

    im.save(filename)


generator = build_generator(SEED_SIZE, IMAGE_CHANNELS)

noise = tf.random.normal([1, SEED_SIZE])
generated_image = generator(noise, training=False)

plt.imshow(generated_image[0, :, :, 0])

image_shape = (GENERATE_SQUARE, GENERATE_SQUARE, IMAGE_CHANNELS)

discriminator = build_discriminator(image_shape)
decision = discriminator(generated_image)
print(decision)

cross_entropy = tf.keras.losses.BinaryCrossentropy()


def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)


generator_optimizer = tf.keras.optimizers.Adam(1.5e-4, 0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(1.5e-4, 0.5)


@tf.function
def train_step(images):
    seed = tf.random.normal([BATCH_SIZE, SEED_SIZE])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(seed, training=True)
        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

        gradients_of_generator = gen_tape.gradient( \
            gen_loss, generator.trainable_variables)
        gradients_of_discriminator = disc_tape.gradient( \
            disc_loss, discriminator.trainable_variables)

        generator_optimizer.apply_gradients(zip(
            gradients_of_generator, generator.trainable_variables))
        discriminator_optimizer.apply_gradients(zip(
            gradients_of_discriminator,
            discriminator.trainable_variables))
    return gen_loss, disc_loss


def train(dataset, epochs):
    fixed_seed = np.random.normal(0, 1, (PREVIEW_ROWS * PREVIEW_COLS,
                                         SEED_SIZE))
    start = time.time()

    for epoch in range(epochs):
        epoch_start = time.time()

        gen_loss_list = []
        disc_loss_list = []

        for image_batch in dataset:
            t = train_step(image_batch)
            gen_loss_list.append(t[0])
            disc_loss_list.append(t[1])

        g_loss = sum(gen_loss_list) / len(gen_loss_list)
        d_loss = sum(disc_loss_list) / len(disc_loss_list)

        epoch_elapsed = time.time() - epoch_start
        print(f'Epoch {epoch + 1}, gen loss={g_loss},disc loss={d_loss},' \
              ' {hms_string(epoch_elapsed)}')
        save_images(epoch, fixed_seed)

    elapsed = time.time() - start
    print(f'Training time: {hms_string(elapsed)}')


train(train_dataset, EPOCHS)
