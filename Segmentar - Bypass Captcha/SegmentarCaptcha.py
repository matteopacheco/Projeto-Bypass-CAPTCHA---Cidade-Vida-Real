import cv2
import numpy as np
import os

# Função para pré-processamento da imagem
def preprocess_image(image):
    # Aplicar thresholding adaptativo
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh

# Função para identificar o dígito em uma imagem
def detect_digit(image):
    # Pré-processar a imagem
    processed_img = preprocess_image(image)
    
    # Encontrar contornos na imagem
    contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Lista para armazenar os dígitos identificados
    identified_digits = []
    
    # Processar cada contorno encontrado
    for contour in contours:
        # Calcular o retângulo delimitador do contorno
        x, y, w, h = cv2.boundingRect(contour)
        
        # Verificar se o contorno é grande o suficiente para ser considerado um dígito
        if w > 10 and h > 10:
            # Extrair o dígito da imagem original usando o retângulo delimitador
            digit_img = image[y:y+h, x:x+w]
            
            # Armazenar o dígito identificado na lista
            identified_digits.append(digit_img)
    
    return identified_digits

# Diretório onde as imagens estão armazenadas
diretorio_imagens = 'captcha_images'

# Listar todas as imagens no diretório
imagens = os.listdir(diretorio_imagens)

# Iterar sobre cada imagem no diretório
for imagem_file in imagens:
    # Construir o caminho completo para a imagem
    imagem_path = os.path.join(diretorio_imagens, imagem_file)
    
    # Carregar a imagem em escala de cinza
    img = cv2.imread(imagem_path, cv2.IMREAD_GRAYSCALE)

    # Verificar se a imagem foi carregada corretamente
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em {imagem_path}")
        continue
    
    print(f"Processando imagem: {imagem_file}")
    print(f"Dimensões da imagem original: {img.shape}")

    # Limiarização para segmentar os dígitos brancos em um fundo cinza
    _, thresh = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)

    # Encontrar contornos dos dígitos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Desenhar contornos nos dígitos identificados
    digits_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Converter de volta para BGR para desenhar contornos coloridos
    identified_digits = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(digits_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        identified_digits.append(img[y:y+h, x:x+w])

    # Mostrar imagem com contornos dos dígitos identificados
    cv2.imshow("Identified Digits", digits_img)
    cv2.imwrite(os.path.join(diretorio_imagens, f"{os.path.splitext(imagem_file)[0]}_identified_digits.jpg"), digits_img)

    # Mostrar cada dígito identificado separadamente
    for i, digit_img in enumerate(identified_digits):
        cv2.imshow(f"Digit {i+1}", digit_img)
        cv2.imwrite(os.path.join(diretorio_imagens, f"{os.path.splitext(imagem_file)[0]}_digit_{i+1}.jpg"), digit_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
