import os
import subprocess
import random
import time

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_temp_file(lines, temp_file):
    with open(temp_file, 'w') as file:
        file.writelines(lines)

def compress_file(executable, mem_size, input_file, output_file):
    command = [executable, f"-{mem_size}", input_file, output_file]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def extract_compression_info(output):
    lines = output.splitlines()
    
    total_input_size = None
    total_archive_size = None
    time_seconds = None

    for line in lines:
        if 'Total input size' in line:
            total_input_size = int(line.split(":")[-1].strip())
        elif 'Total archive size' in line:
            total_archive_size = int(line.split(":")[-1].strip())
        elif 'Time' in line:
            time_seconds = float(line.split(" ")[1].strip())
    
    if total_input_size is None or total_archive_size is None or time_seconds is None:
        print("Output format:")
        print(output)
        raise RuntimeError("Unexpected output format from paq8px")

    return total_input_size, total_archive_size, time_seconds

def calculate_compression_rate(original_size, compressed_size):
    return 100 - (compressed_size / original_size * 100)

def perform_multiple_compressions(lines, executable_path, mem_size, num_messages, iterations=100):
    total_compression_rate = 0
    total_compression_time = 0
    total_original_size = 0
    total_compressed_size = 0

    for _ in range(iterations):
        selected_lines = random.sample(lines, num_messages)
        temp_input_file = f"temp_input_{num_messages}.txt"
        temp_output_file = f"teste_{num_messages}"

        try:
            write_temp_file(selected_lines, temp_input_file)
            output = compress_file(executable_path, mem_size, temp_input_file, temp_output_file)
            original_size, compressed_size, compression_time = extract_compression_info(output)
            
            compression_rate = calculate_compression_rate(original_size, compressed_size)
            
            total_compression_rate += compression_rate
            total_compression_time += compression_time
            total_original_size += original_size
            total_compressed_size += compressed_size
        finally:
            if os.path.exists(temp_input_file):
                os.remove(temp_input_file)

    avg_compression_rate = total_compression_rate / iterations
    avg_compression_time = total_compression_time / iterations
    avg_original_size = total_original_size / iterations
    avg_compressed_size = total_compressed_size / iterations
    
    return avg_original_size, avg_compressed_size, avg_compression_rate, avg_compression_time

def main():
    input_file_path = 'input.txt'
    executable_path = './paq8px'
    mem_size = 8
    log_file_path = 'compression_results.txt'

    lines = read_input_file(input_file_path)
    
    with open(log_file_path, 'w') as log_file:
        log_file.write('num_messages,avg_original_size,avg_compressed_size,avg_compression_rate,avg_compression_time\n')
    
    for num_messages in range(1, 40):
        avg_original_size, avg_compressed_size, avg_compression_rate, avg_compression_time = perform_multiple_compressions(lines, executable_path, mem_size, num_messages)

        with open(log_file_path, 'a') as log_file:
            log_file.write(f'{num_messages},{avg_original_size},{avg_compressed_size},{avg_compression_rate:.2f},{avg_compression_time:.2f}\n')
        
        print(f'Completed 100 compressions for {num_messages} messages.')

if __name__ == "__main__":
    main()
