""" Training networks with transfer learning. """

import os
from ast import literal_eval

import pandas as pd
import numpy as np
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

# Load data
DATA_DIR = "data/download/"
ids_downloaded = sorted(
    [int(i.split(".")[0]) for i in os.listdir(DATA_DIR) if i.endswith(".jpg")]
)
df = pd.read_csv("data/df_merged.csv", quotechar="'", sep=";")
df_filtered = df[df["thumbnail_id"].isin(ids_downloaded)].sort_values(by="thumbnail_id")
# check properties of result
assert not df_filtered.thumbnail_id.duplicated().any(), "duplicated ids for images!"
assert df_filtered.thumbnail_id.is_monotonic_increasing, "thumbnails not sorted!"

# target vector
# np.ndarray(literal_eval(df_filtered.frame_colors.values[-1]))
# TODO


# create model for transfer learning
base_model = InceptionV3(include_top=False, weights="imagenet")
# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation="relu")(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(200, activation="softmax")(x)
# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)
# freeze layers from base model
for layer in base_model.layers:
    layer.trainable = False
# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer="adam", loss="categorical_crossentropy")

# predict with model
img_path = "data/download/446.jpg"
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
preds = model.predict(x)
