import serial
import time

# Configuração da porta serial (ajuste conforme necessário)
ser = serial.Serial('COM11', 115200)  # Substitua 'COM3' pela porta serial correta no seu computador
time.sleep(2)  # Espera para a inicialização do Arduino

# Nome do arquivo de saída
output_file = "sf7_193_bytes.txt"

# Cabeçalho do arquivo

#header = "avg_power_mW,peakPower,peakAvgPower,peakCurrent \n"
ser.flush()
with open(output_file, 'w+') as file:
    #file.write(header)  # Escreve o cabeçalho no arquivo

    ser.flush()
    while True:
        try:
            ser.flush()
            file.flush()
            line = ser.readline().decode('latin-1').strip()
            #print(line)  # Mostra os dados no console
            file.write(line + "\n")  # Escreve os dados no arquivo
            file.flush()
            ser.flush()
        except KeyboardInterrupt:
            print("Interrompido pelo usuário")
            break

ser.close()
