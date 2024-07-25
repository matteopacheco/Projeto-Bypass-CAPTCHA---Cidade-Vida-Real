import pyautogui
import keyboard
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageGrab
import sys  # Importar sys para encerrar o script

# Função para carregar coordenadas do arquivo
def carregar_coordenadas():
    with open('coordenadas.txt', 'r') as f:
        coordenadas = {}
        for linha in f:
            chave, valor = linha.strip().split('=')
            coordenadas[chave] = float(valor)
    return coordenadas

# Função para capturar tela com base nas coordenadas
def capturar_tela(x, y, w, h, nome_arquivo='captura.png'):
    imagem = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    imagem.save(nome_arquivo)
    return nome_arquivo

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
    contours_info = []

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
            
            # Adicionar à lista de dígitos segmentados com suas coordenadas X
            digits.append({'image': resized_digit, 'x': x})
    
    # Ordenar os dígitos pela posição X para garantir que estão na ordem correta
    digits.sort(key=lambda d: d['x'])
    
    return [d['image'] for d in digits]

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

# Função para escrever os dígitos preditos na tela
def escrever_digitos(predictions):
    for digit in predictions:
        # Escrever o dígito predito na posição atual do cursor
        pyautogui.typewrite(str(digit))

def main():
    print("Aguardando a tecla F12 para capturar e processar a tela...")
    
    coordenadas = carregar_coordenadas()
    
    x = coordenadas['x']
    y = coordenadas['y']
    w = coordenadas['w']
    h = coordenadas['h']
    
    while True:
        if keyboard.is_pressed('f12'):
            print("Capturando tela...")
            captura_path = capturar_tela(x, y, w, h)
            print(f"Captura de tela salva como '{captura_path}'")
            
            # Carregar a imagem em escala de cinza
            img = cv2.imread(captura_path, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                print(f"Erro: Não foi possível carregar a imagem em {captura_path}")
            else:
                print(f"Processando imagem: {captura_path}")
                print(f"Dimensões da imagem original: {img.shape}")

                # Detectar e segmentar os dígitos na imagem
                segmented_digits = detect_digits(img)

                # Carregar o modelo treinado
                model = load_model('modelo.h5')

                # Identificar cada dígito segmentado
                predictions = identify_digits(model, segmented_digits)

                # Imprimir as previsões numa linha só
                print("Previsões:", " ".join(map(str, predictions)))

                # Escrever os dígitos preditos na tela
                escrever_digitos(predictions)

                # Verificar se foram identificados 4 dígitos e encerrar se for o caso
                if len(predictions) == 4:
                    print("4 dígitos identificados. Encerrando o script.")
                    sys.exit()  # Encerra o script
                
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            # Espera até que a tecla F12 seja solta
            while keyboard.is_pressed('f12'):
                pass

if __name__ == "__main__":
    main()
