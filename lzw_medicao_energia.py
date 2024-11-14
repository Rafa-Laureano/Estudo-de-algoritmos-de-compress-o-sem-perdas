# -*- coding: utf-8 -*-

import subprocess

# Função para retornar as mensagens baseadas em um índice
def get_message(idx):
    messages = [
        "-24.732765,-53.763553",
        "-24.730163,-53.761516",
        "-24.730245,-53.763401",
        "-24.732921,-53.763793",
        "-24.732990,-53.763832",
        "-24.733045,-53.763877",
        "-24.732973,-53.763870",
        "-24.732994,-53.763771",
        "-24.732923,-53.763736",
        "-24.733043,-53.763740",
        "-24.733104,-53.763561",
        "-24.732866,-53.763603",
        "-24.733190,-53.763797",
        "-24.732700,-53.763423",
        "-24.727039,-53.760662",
        "-24.729131,-53.754337",
        "-24.735008,-53.757503",
        "-24.742496,-53.759475",
        "-24.734609,-53.761112",
        "-24.732673,-53.763580",
        "-24.732740,-53.763565"
    ]
    return messages[idx]

# Função para concatenar mensagens até o índice especificado
def concatenate_messages(up_to_idx):
    concatenated = ""
    for i in range(up_to_idx):
        concatenated += get_message(i)
    return concatenated

# Função para escrever dados em um arquivo temporário
def write_temp_file(data, filename):
    with open(filename, "w") as f:
        f.write(data)

# Função para executar o compressao
def compress(input_filename, output_filename):
    subprocess.run(["./compressao", input_filename, output_filename], capture_output=True, text=True)

# Nome do arquivo temporário
temp_input_file = "temp_input.txt"

# Executa a compressão de 1 até 21 mensagens
for i in range(1, 22):
    data_to_compress = concatenate_messages(i)
    output_file = f"compressed_{i}.bin"

    # Escreve os dados a serem comprimidos no arquivo temporário
    write_temp_file(data_to_compress, temp_input_file)

    compress(temp_input_file, output_file)

print("Compressao de grupos de mensagens concluida com sucesso.")
