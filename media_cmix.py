# -*- coding: utf-8 -*-

import os
import random
import subprocess
import time
import re

# Funcao para ler o arquivo input.txt e retornar as linhas
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

# Funcao para escrever um novo arquivo com as linhas selecionadas
def write_temp_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Funcao para executar o CMIX e capturar a saida
def run_cmix(cmix_path, input_file, output_file):
    start_time = time.time()
    result = subprocess.run([cmix_path, '-c', input_file, output_file], capture_output=True, text=True)
    end_time = time.time()
    elapsed_time = end_time - start_time

    output = result.stdout
    # Usar expressao regular para encontrar a linha com as informacoes de compressao
    match = re.search(r'(\d+) bytes -> (\d+) bytes', output)
    if match:
        size_before = int(match.group(1))
        size_after = int(match.group(2))
        compression_rate = (1 - (size_after / size_before)) * 100  # Calcular a taxa de compressao em porcentagem
        return size_before, size_after, compression_rate, elapsed_time

    # Caso nao encontre as informacoes, retornar None
    return None, None, None, elapsed_time

def perform_multiple_compressions(cmix_path, lines, num_messages, iterations=100):
    total_compression_rate = 0
    total_compression_time = 0
    total_size_before = 0
    total_size_after = 0

    for _ in range(iterations):
        random_lines = random.sample(lines, num_messages)
        write_temp_file(temp_file_path, random_lines)
        output_file_path = f'{output_file_base_path}_{num_messages}'

        size_before, size_after, compression_rate, elapsed_time = run_cmix(cmix_path, temp_file_path, output_file_path)

        if size_before is not None:
            total_compression_rate += compression_rate
            total_compression_time += elapsed_time
            total_size_before += size_before
            total_size_after += size_after

    avg_compression_rate = total_compression_rate / iterations
    avg_compression_time = total_compression_time / iterations
    avg_size_before = total_size_before / iterations
    avg_size_after = total_size_after / iterations

    return avg_size_before, avg_size_after, avg_compression_rate, avg_compression_time

# Caminhos dos arquivos e diretorios
input_file_path = '/home/rafaella/Desktop/experimento_um/cmix/cmix/input.txt'
temp_file_path = '/home/rafaella/Desktop/experimento_um/cmix/cmix/temp_input.txt'
cmix_path = '/home/rafaella/Desktop/experimento_um/cmix/cmix/cmix'
output_file_base_path = '/home/rafaella/Desktop/experimento_um/cmix/cmix/output'
log_file_path = '/home/rafaella/Desktop/experimento_um/cmix/cmix/compression_log.txt'

# Tamanhos dos pacotes SF12 e SF7
sf12_packet_size = 51
sf7_packet_size = 222

# Definir a semente para o gerador de numeros aleatorios
random.seed(42)

# Ler o arquivo input.txt
lines = read_input_file(input_file_path)

results = []

max_lines_sf12 = 0
max_lines_sf7 = 0

with open(log_file_path, 'w') as log_file:
    log_file.write("Num_Lines,Avg_Original_Size,Avg_Compressed_Size,Avg_Compression_Rate(%),Avg_Compression_Time,Max_SF12_Lines,Max_SF7_Lines\n")

for i in range(1, 40):
    avg_size_before, avg_size_after, avg_compression_rate, avg_compression_time = perform_multiple_compressions(cmix_path, lines, i)

    if avg_size_after <= sf12_packet_size:
        max_lines_sf12 = i
    if avg_size_after <= sf7_packet_size:
        max_lines_sf7 = i

    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{i},{avg_size_before},{avg_size_after},{avg_compression_rate:.2f},{avg_compression_time:.2f},{max_lines_sf12},{max_lines_sf7}\n")

    print(f"Linhas comprimidas: {i}: Tamanho medio antes = {avg_size_before} bytes, Tamanho medio depois = {avg_size_after} bytes, Taxa media de compressao = {avg_compression_rate:.2f}%, Tempo medio de compressao = {avg_compression_time:.2f} s")

print(f'Numero maximo de linhas comprimidas que cabem em um pacote SF12 ({sf12_packet_size} bytes): {max_lines_sf12}')
print(f'Numero maximo de linhas comprimidas que cabem em um pacote SF7 ({sf7_packet_size} bytes): {max_lines_sf7}')

# Exibir os resultados finais
with open(log_file_path, 'r') as log_file:
    for line in log_file:
        print(line.strip())
