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

# %% Load images
DATA_DIR = "data/download/"
ids_downloaded = sorted(
    [int(i.split(".")[0]) for i in os.listdir(DATA_DIR) if i.endswith(".jpg")]
)

img_list = []
for img_file in os.listdir(DATA_DIR):
    img = image.load_img("data/download/" + img_file, target_size=(224, 224))
    x = image.img_to_array(img)
    x = preprocess_input(x)
    img_list.append(x)

x = np.concatenate([img_list], axis=0)

# %% load target vector
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

# %% create model for transfer learning
base_model = InceptionV3(include_top=False, weights="imagenet")
# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation="relu")(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(len(y_labels), activation="softmax")(x)
# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)
# freeze layers from base model
for layer in base_model.layers:
    layer.trainable = False
# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer="adam", loss="categorical_crossentropy")

# %% validation
datagen = image.ImageDataGenerator(validation_split=0.1)
datagen.fit(x)
datagen.flow(x, y, batch_size=32)

# %% training
model.fit_generator(
    datagen.flow(x, y, batch_size=32), steps_per_epoch=len(x) / 32, epochs=2, verbose=1
)

# %% predict with model
img_path = "data/download/446.jpg"
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
preds = model.predict(x)
print(f"most likely prediction: {y_labels[np.argmax(preds)]}")

# %%
