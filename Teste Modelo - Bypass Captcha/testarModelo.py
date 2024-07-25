import cv2
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.models import load_model

# Função para pré-processamento da imagem
def preprocess_image(image):
    # Aplicar thresholding binário para segmentar os dígitos brancos do fundo cinza
    _, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    return thresh

# Função para detectar e segmentar os dígitos
def detect_digits(image):
    # Pré-processar a imagem
    processed_img = preprocess_image(image)
    
    # Encontrar contornos na imagem
    contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Lista para armazenar os dígitos segmentados
    digits = []

    # Processar cada contorno encontrado
    for contour in contours:
        # Calcular o retângulo delimitador do contorno
        x, y, w, h = cv2.boundingRect(contour)
        
        # Verificar se o contorno é grande o suficiente para ser considerado um dígito
        if w > 10 and h > 10:
            # Extrair o dígito da imagem original usando o retângulo delimitador
            digit_img = image[y:y+h, x:x+w]
            
            # Adicionar padding à imagem do dígito para garantir que tenha o tamanho adequado
            target_size = (120, 60)  # Ajuste conforme o tamanho de entrada do modelo
            padded_digit = cv2.copyMakeBorder(digit_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            resized_digit = cv2.resize(padded_digit, target_size)
            
            # Armazenar o dígito identificado e suas coordenadas na lista
            digits.append((x, resized_digit))
    
    # Ordenar os dígitos pela posição x (da esquerda para a direita)
    sorted_digits = [digit for _, digit in sorted(digits, key=lambda x: x[0])]
    
    return sorted_digits

# Função para pré-processar cada dígito para o modelo
def preprocess_digit(digit_img):
    # Normalizar o pixel de 0 a 1
    normalized_digit = digit_img / 255.0
    # Adicionar uma dimensão extra para o batch size e a dimensão do canal (1, altura, largura, 1)
    expanded_digit = np.expand_dims(normalized_digit, axis=(0, -1))
    return expanded_digit

# Função para identificar o dígito usando o modelo
def identify_digits(model, digits):
    predictions = []
    for digit_img in digits:
        preprocessed_digit = preprocess_digit(digit_img)
        prediction = model.predict(preprocessed_digit)
        predicted_class = np.argmax(prediction, axis=1)[0]
        predictions.append(predicted_class)
    return predictions

# Diretório contendo as imagens de captchas
captchas_dir = 'captcha_imagens'

# Carregar o modelo treinado
model = load_model('modelo.h5')

# Processar cada imagem no diretório de captchas
for filename in os.listdir(captchas_dir):
    if filename.endswith('.png'):
        imagem_path = os.path.join(captchas_dir, filename)
        
        # Carregar a imagem em escala de cinza
        img = cv2.imread(imagem_path, cv2.IMREAD_GRAYSCALE)
        
        # Verificar se a imagem foi carregada corretamente
        if img is None:
            print(f"Erro: Não foi possível carregar a imagem em {imagem_path}")
        else:
            print(f"Processando imagem: {imagem_path}")
            print(f"Dimensões da imagem original: {img.shape}")

            # Detectar e segmentar os dígitos na imagem
            segmented_digits = detect_digits(img)

            # Identificar cada dígito segmentado
            predictions = identify_digits(model, segmented_digits)
            
            # Imprimir as previsões numa linha só
            print("Previsões:", " ".join(map(str, predictions)))

            cv2.waitKey(0)
            cv2.destroyAllWindows()
input()
