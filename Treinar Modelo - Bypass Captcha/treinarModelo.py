import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Caminhos para os diretórios das imagens de treinamento e validação
diretorio_treinamento = 'Imagens Captcha/treinamento'
diretorio_validacao = 'Imagens Captcha/validacao'

# Definição do gerador de dados para pré-processamento
gerador_treinamento = ImageDataGenerator(rescale=1./255)
gerador_validacao = ImageDataGenerator(rescale=1./255)

gerador_treinamento = gerador_treinamento.flow_from_directory(
    diretorio_treinamento,
    target_size=(60, 120),  # Ajuste o tamanho conforme necessário
    batch_size=20,
    color_mode='grayscale',  # Indica que as imagens são em escala de cinza
    class_mode='categorical'  # Para múltiplas classes
)

gerador_validacao = gerador_validacao.flow_from_directory(
    diretorio_validacao,
    target_size=(60, 120),  # Ajuste o tamanho conforme necessário
    batch_size=20,
    color_mode='grayscale',  # Indica que as imagens são em escala de cinza
    class_mode='categorical'  # Para múltiplas classes
)

# Construção do modelo
modelo = tf.keras.models.Sequential([
    tf.keras.Input(shape=(60, 120, 1)),  # Utilize Input(shape) como a primeira camada para escala de cinza
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')  # 10 classes para os dígitos 0 a 9
])

modelo.compile(loss='categorical_crossentropy',
               optimizer='adam',
               metrics=['accuracy'])

# Treinamento do modelo
historico = modelo.fit(
    gerador_treinamento,
    steps_per_epoch=100,  # Número de batches por época
    epochs=50,
    validation_data=gerador_validacao,
    validation_steps=50  # Número de batches de validação por época
)

# Avaliação do modelo
acc = historico.history['accuracy']
val_acc = historico.history['val_accuracy']
loss = historico.history['loss']
val_loss = historico.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(epochs, acc, 'bo', label='Acurácia de Treinamento')
plt.plot(epochs, val_acc, 'b', label='Acurácia de Validação')
plt.title('Acurácia de treinamento e validação')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs, loss, 'bo', label='Perda de Treinamento')
plt.plot(epochs, val_loss, 'b', label='Perda de Validação')
plt.title('Perda de treinamento e validação')
plt.legend()

plt.show()

# Salvando o modelo
modelo.save('modelo.h5')

input()
