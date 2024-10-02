import tensorflow as tf

model = tf.keras.models.load_model('../cnn-model/malaria_lenet_model.keras')
model.summary()
