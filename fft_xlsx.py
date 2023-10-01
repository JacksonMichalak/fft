import numpy as np
from scipy.fft import fft
import pandas as pd
import zipfile

# Caminho para o arquivo ZIP
zip_file_path = 'D:/Downloads/full_data_accelerometer.csv.zip'

# Nome do arquivo dentro do ZIP
csv_file_name = 'full_data_carla.csv'

# Função para calcular a Transformada de Fourier e encontrar os 100 maiores valores de amplitude


def top_100_amplitudes(data):
    # Calcula a Transformada de Fourier
    fft_result = fft(data)

    # Calcula a amplitude (módulo) dos valores da FFT
    amplitude = np.abs(fft_result)

    # Encontra os índices dos 100 maiores valores de amplitude
    top_100_indices = np.argsort(amplitude)[-100:][::-1]

    # Obtém as frequências correspondentes aos índices
    frequencies = np.fft.fftfreq(len(data))
    top_100_frequencies = frequencies[top_100_indices]

    # Obtém os 100 maiores valores de amplitude
    top_100_values = amplitude[top_100_indices]

    return top_100_frequencies, top_100_values


# Extrai o arquivo CSV do ZIP e lê os dados
with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    zip_file.extractall()
    data = pd.read_csv(csv_file_name)

# Seleção dos dados de aceleração nos eixos X, Y e Z
accelX = data['accelX'].values
accelY = data['accelY'].values
accelZ = data['accelZ'].values

# Calcula as 100 maiores amplitudes para cada eixo
top_100_freqX, top_100_ampX = top_100_amplitudes(accelX)
top_100_freqY, top_100_ampY = top_100_amplitudes(accelY)
top_100_freqZ, top_100_ampZ = top_100_amplitudes(accelZ)

# Criar DataFrames para cada eixo
df_x = pd.DataFrame(
    {'Frequência (Hz)': top_100_freqX, 'Amplitude': top_100_ampX})
df_y = pd.DataFrame(
    {'Frequência (Hz)': top_100_freqY, 'Amplitude': top_100_ampY})
df_z = pd.DataFrame(
    {'Frequência (Hz)': top_100_freqZ, 'Amplitude': top_100_ampZ})

# Criar um arquivo Excel com cada eixo em uma aba separada
with pd.ExcelWriter('resultados_amplitudes.xlsx') as writer:
    df_x.to_excel(writer, sheet_name='Eixo X', index=False)
    df_y.to_excel(writer, sheet_name='Eixo Y', index=False)
    df_z.to_excel(writer, sheet_name='Eixo Z', index=False)

print("Resultados salvos em resultados_amplitudes.xlsx")
