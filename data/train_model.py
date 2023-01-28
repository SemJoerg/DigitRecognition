import tensorflow as tf
from tensorflow import keras
from data_handler import DataHandler

class_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

train_data = DataHandler("train_data.npz")
test_data = DataHandler("test_data.npz")

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(24, 24)),  # input layer (1)
    keras.layers.Dense(256, activation='relu'),  # hidden layer (2)
    keras.layers.Dense(128, activation='relu'),  # hidden layer (2)
    tf.keras.layers.Dropout(0.1),
    keras.layers.Dense(10, activation='softmax') # output layer (3)
])

model.compile("adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

model.fit(train_data.image_data, train_data.label_data, epochs=400)

test_loss, test_acc = model.evaluate(test_data.image_data, test_data.label_data)

print("Test accuracy: ", test_acc)
model.save("../main5_model")