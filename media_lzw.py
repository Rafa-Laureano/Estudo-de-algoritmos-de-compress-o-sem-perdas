# -*- coding: utf-8 -*-

import subprocess
import random
import time
import os
import json

# Função para ler as linhas do arquivo
def ler_arquivo(input_file):
    with open(input_file, 'r') as file:
        linhas = file.readlines()
    return linhas

# Função para escrever linhas selecionadas em um arquivo temporário
def escrever_arquivo(temp_file, linhas):
    with open(temp_file, 'w') as file:
        file.writelines(linhas)

# Função para executar o comando de compressão e retornar os resultados
def executar_compressao(input_file, output_file):
    inicio_tempo = time.time()
    result = subprocess.run(['./compressao', input_file, output_file], capture_output=True, text=True)
    fim_tempo = time.time()
    duracao = fim_tempo - inicio_tempo
    return result.stdout, duracao

# Função para extrair informações do resultado da compressão
def extrair_informacoes(resultado):
    linhas = resultado.split('\n')
    tamanho_original = int(linhas[1].split(': ')[1].split(' ')[0])
    tamanho_comprimido = int(linhas[2].split(': ')[1].split(' ')[0])
    taxa_compressao = float(linhas[3].split(': ')[1].split('%')[0])
    return tamanho_original, tamanho_comprimido, taxa_compressao

# Função para realizar múltiplas compressões e calcular médias
def realizar_compressao_multiplas_vezes(linhas, num_mensagens, num_compressao, output_file):
    tamanhos_originais = []
    tamanhos_comprimidos = []
    taxas_compressao = []
    tempos_compressao = []

    for _ in range(num_compressao):
        linhas_aleatorias = random.sample(linhas, num_mensagens)
        temp_file = 'temp_input.txt'
        escrever_arquivo(temp_file, linhas_aleatorias)

        resultado, duracao = executar_compressao(temp_file, output_file)
        tamanho_original, tamanho_comprimido, taxa_compressao = extrair_informacoes(resultado)

        tamanhos_originais.append(tamanho_original)
        tamanhos_comprimidos.append(tamanho_comprimido)
        taxas_compressao.append(taxa_compressao)
        tempos_compressao.append(duracao)

        os.remove(temp_file)

    media_tamanho_original = sum(tamanhos_originais) / num_compressao
    media_tamanho_comprimido = sum(tamanhos_comprimidos) / num_compressao
    media_taxa_compressao = sum(taxas_compressao) / num_compressao
    media_tempo_compressao = sum(tempos_compressao) / num_compressao

    return media_tamanho_original, media_tamanho_comprimido, media_taxa_compressao, media_tempo_compressao

# Função principal
def main(input_file, output_file, max_mensagens, num_compressao, sf12_max_bytes, sf7_max_bytes):
    linhas = ler_arquivo(input_file)
    resultados = []
    max_sf12 = 0
    max_sf7 = 0

    random.seed(42)  # Fixa a semente do gerador de números aleatórios

    for i in range(1, max_mensagens + 1):
        media_tamanho_original, media_tamanho_comprimido, media_taxa_compressao, media_tempo_compressao = realizar_compressao_multiplas_vezes(linhas, i, num_compressao, output_file)

        resultados.append({
            'mensagens': i,
            'tamanho_original': media_tamanho_original,
            'tamanho_comprimido': media_tamanho_comprimido,
            'taxa_compressao': media_taxa_compressao,
            'tempo': media_tempo_compressao
        })

        if media_tamanho_comprimido <= sf12_max_bytes:
            max_sf12 = i

        if media_tamanho_comprimido <= sf7_max_bytes:
            max_sf7 = i

    return resultados, max_sf12, max_sf7

# Executa o script
if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'output'
    max_mensagens = 39
    num_compressao = 100
    sf12_max_bytes = 51
    sf7_max_bytes = 222

    resultados, max_sf12, max_sf7 = main(input_file, output_file, max_mensagens, num_compressao, sf12_max_bytes, sf7_max_bytes)

    # Salva os resultados em um arquivo TXT
    with open('resultados_compressao.txt', 'w') as file:
        file.write('mensagens,tamanho_original,tamanho_comprimido,taxa_compressao,tempo\n')
        for resultado in resultados:
            file.write(f"{resultado['mensagens']},{resultado['tamanho_original']},{resultado['tamanho_comprimido']},{resultado['taxa_compressao']},{resultado['tempo']}\n")

    # Salva o resumo em um arquivo JSON
    resumo = {
        'max_sf12_mensagens': max_sf12,
        'max_sf7_mensagens': max_sf7
    }

    with open('resumo_compressao.json', 'w') as file:
        json.dump(resumo, file, indent=4)

    print("Compressao concluida e resultados salvos em 'resultados_compressao.txt' e 'resumo_compressao.json'")
    print(f"Maximo de mensagens que cabem em SF12 (51 bytes): {max_sf12}")
    print(f"Maximo de mensagens que cabem em SF7 (222 bytes): {max_sf7}")
