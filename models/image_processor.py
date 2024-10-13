import tensorflow as tf
from PIL import Image
import numpy as np

class ImageProcessor:
    @staticmethod
    def process_image(file_path):
        # Abre a imagem e converte para grayscale
        image = Image.open(file_path).convert('L')
        image = image.resize((28, 28))  # Redimensiona para 28x28 pixels
        image_array = np.array(image)

        # Converte a imagem para um array de float32
        image_array = image_array.astype('float32') / 255.0
        image_array = image_array.reshape(1, 28, 28, 1)  # Adiciona dimensões para o TensorFlow

        # Modelo simples para fazer uma previsão
        model = ImageProcessor.build_model()
        prediction = model.predict(image_array)

        # Retorna o grupo de imagem
        group = np.argmax(prediction, axis=1)[0]
        return f"Grupo {group}"

    @staticmethod
    def build_model():
        # Modelo simples para classificar imagens em 2 grupos
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(2, activation='softmax')  # 2 grupos: Grupo 0 e Grupo 1
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model
