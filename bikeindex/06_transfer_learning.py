""" Training networks with transfer learning. """
# %%
import os
from ast import literal_eval

import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

# %% LOAD IAMGES
DATA_DIR = "data/download/"
ids_downloaded = sorted(
    [int(i.split(".")[0]) for i in os.listdir(DATA_DIR) if i.endswith(".jpg")]
)

img_list = []
for img_file in os.listdir(DATA_DIR):
    img = image.load_img("data/download/" + img_file, target_size=(224, 224))
    img_arr = image.img_to_array(img)
    img_prep = preprocess_input(img_arr)
    img_list.append(img_prep)

x = np.concatenate([img_list], axis=0)

# %% LOAD TARGET
df = pd.read_csv("data/df_merged.csv", quotechar="'", sep=";")
df_filtered = df[df["thumbnail_id"].isin(ids_downloaded)].sort_values(by="thumbnail_id")
# check properties of result
assert not df_filtered.thumbnail_id.duplicated().any(), "duplicated ids for images!"
assert df_filtered.thumbnail_id.is_monotonic_increasing, "thumbnails not sorted!"
# label column to vector
y_list = [literal_eval(i) for i in df_filtered.frame_colors.values]
mlb = MultiLabelBinarizer()
y_encoded = pd.DataFrame(mlb.fit_transform(y_list), columns=mlb.classes_)
# to array and column names
y = y_encoded.values
y_labels = list(y_encoded.columns)

# %% CREATE MODEL
base_model = InceptionV3(include_top=False, weights="imagenet")
# add a global spatial average pooling layer
x1 = base_model.output
x2 = GlobalAveragePooling2D()(x1)
# let's add a fully-connected layer
x3 = Dense(1024, activation="relu")(x2)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(len(y_labels), activation="softmax")(x3)
# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)
# freeze layers from base model
for layer in base_model.layers:
    layer.trainable = False
# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer="adam", loss="categorical_crossentropy")

# %% DATA AUGMENTATION
datagen = image.ImageDataGenerator(validation_split=0.1)
datagen.fit(x)

# %% TRAINING
model.fit_generator(
    datagen.flow(x, y, batch_size=32), steps_per_epoch=len(x) / 32, epochs=2, verbose=1
)

# %% PREDICTION
img_path = "data/download/446.jpg"
img = image.load_img(img_path, target_size=(224, 224))
img_arr = image.img_to_array(img)
img_arr = np.expand_dims(img_arr, axis=0)
img_arr = preprocess_input(img_arr)
preds = model.predict(img_arr)
print(f"most likely prediction: {y_labels[np.argmax(preds)]}")

# %%
