import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

class ImageProcessor:
    model = None

    @staticmethod
    def load_model():
        if ImageProcessor.model is None:
            try:
                # Carregue o modelo de rede neural previamente treinado (substitua pelo caminho correto do modelo)
                ImageProcessor.model = tf.keras.models.load_model("caminho_do_modelo/model.h5")
            except Exception as e:
                raise RuntimeError(f"Erro ao carregar o modelo: {str(e)}")

    @staticmethod
    def process_image(img_path):
        try:
            # Carrega e pré-processa a imagem
            img = image.load_img(img_path, target_size=(224, 224))  # Altere o tamanho de entrada conforme necessário
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0  # Normaliza a imagem se necessário

            # Certifica-se de que o modelo está carregado
            ImageProcessor.load_model()

            # Faz a predição usando a rede neural
            predictions = ImageProcessor.model.predict(img_array)

            # Assumindo que a saída é binária, aplica um limiar de 0.5
            predicted_class = (predictions > 0.5).astype(int)  # Saída binária (0 ou 1)
            return f"Classe prevista: {predicted_class[0][0]}"
        except Exception as e:
            raise RuntimeError(f"Erro ao processar a imagem {img_path}: {str(e)}")
