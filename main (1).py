# ============================================================
# SPRINT 3 - Controle Inteligente de Sessão de Recarga
# Prototipo inspirado no conceito do GoodWe Smart Energy Controller
# Plataforma: Raspberry Pi Pico (MicroPython)
# ============================================================
#
# CONCEITOS DE ARQUITETURA DE COMPUTADORES DEMONSTRADOS:
#  - ENTRADA (input):  valores de geracao e consumo de energia
#                       (aqui simulados, mas representam sensores reais)
#  - PROCESSAMENTO:    o Pico (CPU) executa o algoritmo que calcula a
#                       energia disponivel e decide o estado da recarga
#  - MEMORIA:          as variaveis (geracao, consumo, disponivel,
#                       estado) ficam armazenadas na RAM do Pico
#                       enquanto o programa roda
#  - SAIDA (output):   os LEDs (verde/amarelo/vermelho) e o texto
#                       impresso no Monitor Serial
#
# ============================================================

from machine import Pin
import time

# ------------------------------------------------------------
# 1) CONFIGURACAO DE HARDWARE (E/S)
# ------------------------------------------------------------
# Pinos escolhidos para o Wokwi / Pico fisico.
# Se for montar fisicamente, ligue cada LED em serie com um
# resistor de 220-330 ohm entre o pino e o GND.

LED_VERDE    = Pin(16, Pin.OUT)   # GP16 -> Recarga autorizada
LED_AMARELO  = Pin(17, Pin.OUT)   # GP17 -> Recarga reduzida
LED_VERMELHO = Pin(18, Pin.OUT)   # GP18 -> Recarga bloqueada

def apagar_leds():
    LED_VERDE.off()
    LED_AMARELO.off()
    LED_VERMELHO.off()

# ------------------------------------------------------------
# 2) LIMIAR (THRESHOLD) DE DECISAO
# ------------------------------------------------------------
# Se a energia disponivel for maior que este limiar, a recarga
# e considerada totalmente autorizada. Entre 0 e o limiar, a
# recarga e apenas parcial (reduzida). Abaixo de 0, bloqueada.
LIMIAR_RECARGA_TOTAL = 500  # em Watts

# ------------------------------------------------------------
# 3) PROCESSAMENTO: calculo do estado da sessao de recarga
# ------------------------------------------------------------
def calcular_estado(geracao, consumo):
    """
    Recebe geracao e consumo (em Watts) e retorna:
    (energia_disponivel, status_texto)
    """
    disponivel = geracao - consumo

    if disponivel <= 0:
        status = "RECARGA BLOQUEADA"
    elif disponivel < LIMIAR_RECARGA_TOTAL:
        status = "RECARGA REDUZIDA"
    else:
        status = "RECARGA AUTORIZADA"

    return disponivel, status

# ------------------------------------------------------------
# 4) SAIDA: acionamento do LED correspondente
# ------------------------------------------------------------
def acionar_led(status):
    apagar_leds()
    if status == "RECARGA AUTORIZADA":
        LED_VERDE.on()
    elif status == "RECARGA REDUZIDA":
        LED_AMARELO.on()
    elif status == "RECARGA BLOQUEADA":
        LED_VERMELHO.on()

# ------------------------------------------------------------
# 5) REPRESENTACAO DE DADOS: decimal, binario e hexadecimal
# ------------------------------------------------------------
def mostrar_representacao(valor, nome="Potencia disponivel"):
    """
    Mostra um valor em Decimal, Binario e Hexadecimal,
    conforme pedido no item 5 do enunciado.
    Trata valores negativos mostrando o sinal separadamente,
    já que o Pico nao usa complemento de dois em bin()/hex()
    por padrao.
    """
    sinal = "-" if valor < 0 else ""
    modulo = abs(valor)

    print("----- Representacao de dados: {} -----".format(nome))
    print("Decimal:      {}{}".format(sinal, modulo))
    print("Binario:      {}{}".format(sinal, bin(modulo)[2:]))   # remove '0b'
    print("Hexadecimal:  {}{}".format(sinal, hex(modulo)[2:].upper()))  # remove '0x'
    print("-" * 45)

# ------------------------------------------------------------
# 6) EXIBICAO DOS DADOS DA SESSAO NO MONITOR SERIAL
# ------------------------------------------------------------
def exibir_dados(geracao, consumo, disponivel, status):
    print("GERACAO: {} W   CONSUMO: {} W   DISPONIVEL: {} W   STATUS: {}".format(
        geracao, consumo, disponivel, status
    ))

# ------------------------------------------------------------
# 7) ENTRADA: cenarios simulados de geracao/consumo
# ------------------------------------------------------------
# Os 3 cenarios exigidos pelo enunciado (situacoes 1, 2 e 3).
# Em uma aplicacao real, esses valores viriam de sensores de
# energia (entrada de dados via hardware).
CENARIOS = [
    {"nome": "Situacao 1 - Energia suficiente", "geracao": 4000, "consumo": 1500},
    {"nome": "Situacao 2 - Energia limitada",    "geracao": 1800, "consumo": 1500},
    {"nome": "Situacao 3 - Energia insuficiente","geracao": 1000, "consumo": 1800},
]

# ------------------------------------------------------------
# 8) PROGRAMA PRINCIPAL
# ------------------------------------------------------------
def main():
    print("=" * 60)
    print(" SISTEMA DE CONTROLE INTELIGENTE DE SESSAO DE RECARGA")
    print(" Prototipo educacional - Raspberry Pi Pico / MicroPython")
    print("=" * 60)

    apagar_leds()
    time.sleep(1)

    # Demonstra, em loop continuo, os 3 estados exigidos.
    while True:
        for cenario in CENARIOS:
            print("\n>> {}".format(cenario["nome"]))

            geracao = cenario["geracao"]
            consumo = cenario["consumo"]

            disponivel, status = calcular_estado(geracao, consumo)
            acionar_led(status)
            exibir_dados(geracao, consumo, disponivel, status)
            mostrar_representacao(disponivel, "Energia disponivel")

            # Tempo em que o LED fica aceso, para dar tempo de
            # filmar cada situacao no video de demonstracao.
            time.sleep(4)

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
