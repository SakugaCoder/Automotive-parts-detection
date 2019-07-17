#from __future__ import absolute_import, division, print_function

#Importar libreria de tensor flow
import tensorflow as tf

#Importar libreria de keras de la libreria tensorflow
from tensorflow import keras


#librerias adicionales
import numpy as np
import matplotlib.pyplot as plt


#Creación de objeto keras.datasets.fashion_mnist
fashion_minist = keras.datasets.fashion_mnist

#Carga de imagenes y etiquetas de entrenameinto respectivamente (Devuelve cuatro 'numpy array')
(imagenes_entrenamiento,etiquetas_entrenamiento) , (imagenes_prueba,etiquetas_prueba) = fashion_minist.load_data()

#Creación de una lista con las clases del clasificador
clases = ['T-Shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt',
         'Sneaker','Bag','Ankle boot']


#Escalamiento de todas las imagenes (Entrenamiento y prueba) las valores de entre 0 a 1
#por convención para alimentar la red nuronal
imagenes_entrenamiento = imagenes_entrenamiento / 255.0
imagenes_prueba = imagenes_prueba / 255.0

#Construcción del modelo clasificador
modelo = keras.Sequential()

#Capa para convertir la imagen 2d en 1d
modelo.add(keras.layers.Flatten(input_shape = (28,28)))
#Capa prufunda de 128 neuronas
modelo.add(keras.layers.Dense(128,activation=tf.nn.relu))
#Capa profunda final de 10 neuronas (Las diez clases de ropa)
modelo.add(keras.layers.Dense(10,activation=tf.nn.softmax))


#Compilar el modelo
modelo.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#Entrenar el modelo
modelo.fit(imagenes_entrenamiento,etiquetas_entrenamiento,epochs=5)

#Evaluar efectividad
prueba_perdida, effectividad_prueba = modelo.evaluate(imagenes_prueba,etiquetas_prueba)
print("Efectividad de la prueba : {}".format(effectividad_prueba))

#Predecir valores de una sola imagen:
img = imagenes_prueba[100]
imagen = np.expand_dims(img,0)
predicciones = modelo.predict(imagen)

print("Predicciones para la imagen 100: {}".format(predicciones))
