# Controle Inteligente de Sessão de Recarga — Sprint 3

Protótipo educacional inspirado no conceito do **GoodWe Smart Energy
Controller**, desenvolvido para a disciplina de **Arquitetura de
Computadores**. Simula, com um Raspberry Pi Pico rodando MicroPython, a
decisão automática entre autorizar, reduzir ou bloquear uma sessão de
recarga com base na energia disponível (geração − consumo).

## Integrantes

| Nome | RM |
|---|---|
| _Bryan_ | _rm571350_ |
| _Beckman_ | _rm573442_ |
| _Guilherme_ | _rm571350_ |

## Como funciona

1. **Entrada**: o sistema recebe (aqui, simula) três cenários de geração e
   consumo de energia residencial.
2. **Processamento**: a CPU do Pico calcula `energia_disponivel =
   geracao - consumo` e decide o estado da sessão comparando esse valor
   com um limiar (`LIMIAR_RECARGA_TOTAL = 500 W`).
3. **Memória**: os valores de geração, consumo, energia disponível e
   status ficam armazenados nas variáveis do programa em RAM durante a
   execução.
4. **Saída**: um LED (verde, amarelo ou vermelho) é aceso conforme o
   estado, e os dados completos da sessão são impressos no Monitor
   Serial.

## Estados do sistema

| Estado | Condição | LED | Exemplo do enunciado |
|---|---|---|---|
| Recarga autorizada | disponível ≥ 500 W | 🟢 Verde | Geração 4000 W, Consumo 1500 W → 2500 W |
| Recarga reduzida | 0 < disponível < 500 W | 🟡 Amarelo | Geração 1800 W, Consumo 1500 W → 300 W |
| Recarga bloqueada | disponível ≤ 0 W | 🔴 Vermelho | Geração 1000 W, Consumo 1800 W → -800 W |

## Representação de dados

O sistema também exibe a **energia disponível** de cada cenário em
decimal, binário e hexadecimal (item 5 do enunciado), por exemplo:

```
Decimal:      2500
Binario:      100111000100
Hexadecimal:  9C4
```

## Como rodar (simulador Wokwi — recomendado, sem hardware físico)

1. Acesse **https://wokwi.com** e crie uma conta gratuita (ou faça login).
2. Clique em **"New Project" → "Raspberry Pi Pico (MicroPython)"**.
3. No editor que abrir, apague o conteúdo padrão de `main.py` e cole o
   conteúdo do arquivo [`main.py`](./main.py) deste repositório.
4. Clique na aba **"diagram.json"** do projeto Wokwi, apague o conteúdo
   e cole o conteúdo do arquivo [`diagram.json`](./diagram.json) deste
   repositório (ele já posiciona os 3 LEDs com resistores ligados nos
   pinos GP16, GP17 e GP18 do Pico).
5. Clique no botão verde **▶ (Play/Start Simulation)**.
6. Abra o **Monitor Serial** (ícone de terminal na parte inferior) para
   ver os dados de cada sessão sendo impressos.
7. Observe os LEDs alternando entre verde, amarelo e vermelho a cada
   ~4 segundos, um para cada cenário do enunciado — use essa tela para
   gravar o vídeo de demonstração.

## Como rodar em um Raspberry Pi Pico físico (opcional)

1. Instale o firmware MicroPython no Pico (documentação oficial:
   micropython.org/download/RPI_PICO).
2. Ligue 3 LEDs aos pinos **GP16 (verde)**, **GP17 (amarelo)** e
   **GP18 (vermelho)**, cada um em série com um resistor de 220–330 Ω
   até o GND.
3. Copie `main.py` para o Pico (via Thonny IDE, por exemplo) e execute.
4. Acompanhe a saída pelo Monitor Serial do Thonny.

## Relação com Arquitetura de Computadores

- **Sistemas de E/S**: os LEDs são dispositivos de saída digital
  controlados via GPIO; os dados simulados representam a entrada que,
  numa aplicação real, viria de sensores de energia.
- **Processamento**: o microcontrolador (CPU do Pico) executa o
  algoritmo de decisão em tempo real, comparando valores e ramificando
  a lógica (`if/elif/else`).
- **Memória**: as variáveis do programa (geração, consumo, energia
  disponível, status) residem na memória RAM do dispositivo durante a
  execução do laço principal.
- **Sistemas numéricos**: o projeto demonstra explicitamente a
  conversão de um valor entre as bases decimal, binária e hexadecimal,
  ilustrando como os dados são representados internamente pelo
  hardware.

## Estrutura do repositório

```
.
├── main.py          # Código MicroPython do protótipo
├── diagram.json      # Circuito para simulação no Wokwi
└── README.md          # Esta documentação
```
