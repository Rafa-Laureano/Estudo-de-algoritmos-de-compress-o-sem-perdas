import subprocess
import random
import time
import re
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def compress_file(input_file, output_file):
    start_time = time.time()
    result = subprocess.run(['./lstm-compress', '-c', input_file, output_file], capture_output=True, text=True)
    end_time = time.time()
    return result.stdout, end_time - start_time

def extract_compression_info(output):
    try:
        size_pattern = re.compile(r"(\d+) bytes -> (\d+) bytes")
        time_pattern = re.compile(r"in (\d+\.\d+) s")
        entropy_pattern = re.compile(r"cross entropy: (\d+\.\d+)")

        original_size, compressed_size = map(int, size_pattern.search(output).groups())
        compression_time = float(time_pattern.search(output).group(1))
        cross_entropy = float(entropy_pattern.search(output).group(1))

        return original_size, compressed_size, compression_time, cross_entropy
    except Exception as e:
        print(f"Error parsing compression output: {e}")
        return None, None, None, None

def log_results(log_file, i, original_size, compressed_size, avg_compression_rate, avg_compression_time, avg_cross_entropy, sf12_fit, sf7_fit):
    with open(log_file, 'a') as log:
        log.write(f"{i},{original_size},{compressed_size},{avg_compression_rate:.2f},{avg_compression_time},{avg_cross_entropy},{sf12_fit},{sf7_fit}\n")

def perform_multiple_compressions(lines, num_messages, iterations=100):
    total_compression_rate = 0
    total_compression_time = 0
    total_cross_entropy = 0
    total_original_size = 0
    total_compressed_size = 0

    for _ in range(iterations):
        selected_lines = random.sample(lines, num_messages)
        temp_input_file = 'temp_input.txt'
        temp_output_file = f'temp_output_{num_messages}'

        try:
            write_file(temp_input_file, selected_lines)
            output, elapsed_time = compress_file(temp_input_file, temp_output_file)
            original_size, compressed_size, compression_time, cross_entropy = extract_compression_info(output)

            if original_size is not None:
                compression_rate = (1 - (compressed_size / original_size)) * 100 if original_size != 0 else 0

                total_compression_rate += compression_rate
                total_compression_time += compression_time
                total_cross_entropy += cross_entropy
                total_original_size += original_size
                total_compressed_size += compressed_size
        finally:
            if os.path.exists(temp_input_file):
                os.remove(temp_input_file)

    avg_compression_rate = total_compression_rate / iterations
    avg_compression_time = total_compression_time / iterations
    avg_cross_entropy = total_cross_entropy / iterations
    avg_original_size = total_original_size / iterations
    avg_compressed_size = total_compressed_size / iterations

    return avg_original_size, avg_compressed_size, avg_compression_rate, avg_compression_time, avg_cross_entropy

def main():
    input_path = 'input.txt'
    log_path = 'compression_log.csv'

    # Write the log file header
    with open(log_path, 'w') as log:
        log.write("Num_Lines,Original_Size,Compressed_Size,Avg_Compression_Rate(%),Avg_Compression_Time,Avg_Cross_Entropy,SF12_Fit,SF7_Fit\n")

    lines = read_file(input_path)

    sf12_limit = 51
    sf7_limit = 222
    sf12_fit = 0
    sf7_fit = 0

    for i in range(1, 40):
        avg_original_size, avg_compressed_size, avg_compression_rate, avg_compression_time, avg_cross_entropy = perform_multiple_compressions(lines, i)

        if avg_compressed_size <= sf12_limit:
            sf12_fit = i
        if avg_compressed_size <= sf7_limit:
            sf7_fit = i

        log_results(log_path, i, avg_original_size, avg_compressed_size, avg_compression_rate, avg_compression_time, avg_cross_entropy, sf12_fit, sf7_fit)

        print(f'Completed 100 compressions for {i} messages.')

if __name__ == "__main__":
    main()
