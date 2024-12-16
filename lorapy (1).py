from pyLoraRFM9x import LoRa, ModemConfig
import random
import time


def start_lora(SF):
    sf_mapping = {
        7: ModemConfig.Bw125Cr45Sf128,
        12: ModemConfig.Bw125Cr48Sf4096
    }

    if SF not in sf_mapping:
        raise ValueError("Invalid SF value")

    SF = sf_mapping[SF]
    
    #print(f"Configurando LoRa com Spreading Factor: {SF}")

    try:
        lora = LoRa(
            spi_channel=0,
            interrupt_pin=27,
            my_address=1,
            spi_port=0,
            reset_pin=17,
            freq=915,
            modem_config=SF,
            tx_power=23,
            receive_all=True
            
        )
        
        if SF == ModemConfig.Bw125Cr48Sf4096:
            
            lora.wait_packet_sent_timeout = 1.0  # Aumenta o timeout para SF 12
            lora.retry_timeout = 1.0  # Aumenta o tempo de espera entre tentativas de envio

        return lora
        
    except Exception as e:
        raise e


def send_packet(lora, packet):

    try:
        lora.set_mode_tx()
        lora.send(packet, 0)
    except Exception as e:
        raise e
        
def send_packet_with_retries(lora, packet, retries=5):
    try:
        for _ in range(retries):
            success = send_packet(lora, packet)
            if success:
                print("Pacote enviado com sucesso!")
                return
            print("Tentativa de envio falhou. Tentando novamente...")
            time.sleep(1)
    except Exception as e:
        raise e


def receive_packet(lora):

    try:
        lora.set_mode_rx()
        


        if not lora._last_payload:
            return None
            
        packet = lora._last_payload.message
        rssi = lora._last_payload.rssi
        snr = lora._last_payload.snr
        
        try:
            message = packet.decode('utf-8')
        except UnicodeDecodeError:
            message = packet.decode('latin-1')

        return {
            'message': message,
            'rssi': rssi,
            'snr': snr,
            'timestamp': time.time()
        }

    except Exception as e:
        raise e


def stop_lora(lora):

    try:
        lora.close()
    except Exception as e:
        raise e
