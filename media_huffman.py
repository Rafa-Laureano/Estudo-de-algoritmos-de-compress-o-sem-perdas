import os
import subprocess
import random
import time

SF12_MAX_SIZE = 51
SF7_MAX_SIZE = 222

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_temp_file(lines, temp_file_path):
    with open(temp_file_path, 'w') as file:
        file.writelines(lines)

def get_file_size(file_path):
    return os.path.getsize(file_path)

def compress_file(input_file, output_file):
    start_time = time.time()
    subprocess.run(['./compressor', input_file, output_file])
    end_time = time.time()
    compression_time = end_time - start_time
    return round(compression_time, 6)

def log_results(log_file_path, n, original_size, compressed_size, avg_compression_ratio, avg_compression_time, sf12_max_messages, sf7_max_messages):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{n},{original_size},{compressed_size},{avg_compression_ratio:.2f},{avg_compression_time:.6f},{sf12_max_messages},{sf7_max_messages}\n')

def perform_multiple_compressions(lines, temp_input_file_path, output_file_path, n, iterations=100):
    total_compression_ratio = 0
    total_compression_time = 0

    for _ in range(iterations):
        sampled_lines = random.sample(lines, n)
        write_temp_file(sampled_lines, temp_input_file_path)

        original_size = get_file_size(temp_input_file_path)
        compression_time = compress_file(temp_input_file_path, output_file_path)
        compressed_size = get_file_size(output_file_path)

        if original_size > 0:
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
        else:
            compression_ratio = 0

        total_compression_ratio += compression_ratio
        total_compression_time += compression_time

    avg_compression_ratio = total_compression_ratio / iterations
    avg_compression_time = total_compression_time / iterations
    return avg_compression_ratio, avg_compression_time

def main():
    input_file_path = 'input.txt'
    log_file_path = 'compression_log.txt'
    temp_input_file_path = 'temp_input.txt'
    output_file_path = 'output'

    lines = read_file(input_file_path)
    total_lines = len(lines)

    with open(log_file_path, 'w') as log_file:
        log_file.write('n,original_size,compressed_size,avg_compression_ratio,avg_compression_time,sf12_max_messages,sf7_max_messages\n')

    sf12_max_messages = 0
    sf7_max_messages = 0

    for n in range(1, 40):
        avg_compression_ratio, avg_compression_time = perform_multiple_compressions(lines, temp_input_file_path, output_file_path, n)

        sampled_lines = random.sample(lines, min(n, total_lines))
        write_temp_file(sampled_lines, temp_input_file_path)
        original_size = get_file_size(temp_input_file_path)
        compressed_size = get_file_size(output_file_path)

        if compressed_size <= SF12_MAX_SIZE:
            sf12_max_messages = n
        if compressed_size <= SF7_MAX_SIZE:
            sf7_max_messages = n

        log_results(log_file_path, n, original_size, compressed_size, avg_compression_ratio, avg_compression_time, sf12_max_messages, sf7_max_messages)

        print(f'Completed compression with {n} messages.')

if __name__ == '__main__':
    main()
