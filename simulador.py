# Este programa simula o funcionamento básico de uma CPU, reproduzindo
# as 6 etapas do ciclo de instrução: Fetch, Decode, Busca de Operandos,
# Execução, Armazenamento e Atualização do PC.

# MEMÓRIA DE INSTRUÇÕES
# Cada instrução é representada como uma lista:
# [OPERAÇÃO, operando1, operando2, ...]
# Esta é a "RAM" que a CPU irá percorrer sequencialmente usando o PC.

memoria = [
    ["ADD", 10, 20],         # Soma simples: 10 + 20
    ["SUB", 50, 15],         # Subtração: 50 - 15
    ["MUL", 8, 7],           # Multiplicação: 8 × 7
    ["DIV", 100, 4],         # Divisão: 100 ÷ 4
    ["DIV", 10, 0],          # Divisão por zero (teste de erro)
    ["MOV", 42],             # Armazena o valor 42 no registrador
    ["ADD", "X", 30, 12],    # ADD com 3 operandos: 30 + 12, resultado em X
    ["MUL", "Y", 5, 6],      # MUL com 3 operandos: 5 × 6, resultado em Y
    ["SUB", "Z", 20, 8],     # SUB com 3 operandos: 20 - 8, resultado em Z
    ["AVG", 10, 20, 30],     # Média de 10, 20 e 30
    ["JUMP", 12],            # Pula para a instrução na posição 12
    ["ADD", 99, 1],          # Esta instrução será pulada pelo JUMP
    ["MUL", 3, 3],           # Execução retoma aqui após o JUMP
    ["END"],                 # Encerra a execução
]

# REGISTRADORES DA CPU
# PC  → Program Counter: aponta para a próxima instrução a ser buscada
# IR  → Instruction Register: armazena a instrução atualmente em execução
# resultado → Registrador de resultado: guarda o resultado da ULA
# registradores → Dicionário que simula registradores nomeados (ex: X, Y, Z)

PC = 0
IR = None
resultado = None
registradores = {} 

# FUNÇÕES DO CICLO DE INSTRUÇÃO

def separador():
    print("=" * 50)


def etapa1_fetch(pc):
    #ETAPA 1 - BUSCA DA INSTRUÇÃO (FETCH)
    print(f"\nPC = {pc}")
    separador()
    print("[1] BUSCA DA INSTRUÇÃO (FETCH)")
    instrucao = memoria[pc]          # Acessa a memória usando o PC
    print(f"    Instrução encontrada: {' '.join(str(x) for x in instrucao)}")
    return instrucao                 # Retorna a instrução carregada no IR


def etapa2_decode(ir):
    """
    ETAPA 2 - DECODIFICAÇÃO DA INSTRUÇÃO (DECODE)
    A Unidade de Controle interpreta o código de operação (opcode)
    contido no IR e identifica qual ação deve ser realizada.
    """
    print("\n[2] DECODIFICAÇÃO")
    operacao = ir[0]                 # O primeiro elemento é sempre o opcode

    # Tabela de decodificação: mapeia opcode → descrição legível
    descricoes = {
        "ADD": "Soma",
        "SUB": "Subtração",
        "MUL": "Multiplicação",
        "DIV": "Divisão",
        "MOV": "Mover valor para registrador",
        "AVG": "Média aritmética",
        "JUMP": "Desvio de execução (JUMP)",
        "END": "Encerrar programa",
    }

    # Verifica se há 3 operandos numéricos (formato com destino registrador)
    if operacao in ("ADD", "MUL", "SUB") and len(ir) == 4:
        descricao = descricoes[operacao] + " com três operandos"
    else:
        descricao = descricoes.get(operacao, "Operação desconhecida")

    print(f"    Operação identificada: {descricao}")
    return operacao


def etapa3_operandos(ir, operacao):
    """
    ETAPA 3 - BUSCA DOS OPERANDOS
    Os valores necessários para a operação são carregados
    (nesta simulação, diretamente da instrução).
    Em uma CPU real, poderiam vir de registradores ou memória de dados.
    """
    print("\n[3] BUSCA DOS OPERANDOS")

    if operacao == "END":
        # END não possui operandos
        return None, None, None

    if operacao == "JUMP":
        # JUMP possui apenas o endereço de destino
        destino = ir[1]
        print(f"    Endereço de destino = {destino}")
        return destino, None, None

    if operacao == "MOV":
        # MOV possui apenas um valor a ser armazenado
        valor = ir[1]
        print(f"    Valor = {valor}")
        return valor, None, None

    if operacao == "AVG":
        # AVG recebe três valores para calcular a média
        a, b, c = ir[1], ir[2], ir[3]
        print(f"    A = {a}")
        print(f"    B = {b}")
        print(f"    C = {c}")
        return a, b, c

    # ADD / SUB / MUL / DIV com 3 operandos (destino + dois valores)
    if len(ir) == 4:
        destino = ir[1]
        b = ir[2]
        c = ir[3]
        print(f"    Destino = {destino}")
        print(f"    B = {b}")
        print(f"    C = {c}")
        return destino, b, c

    # ADD / SUB / MUL / DIV com 2 operandos (formato padrão)
    a = ir[1]
    b = ir[2]
    print(f"    A = {a}")
    print(f"    B = {b}")
    return a, b, None


def etapa4_execucao(operacao, a, b, c):
    """
    ETAPA 4 - EXECUÇÃO (ULA - Unidade Lógica e Aritmética)
    A ULA realiza o cálculo correspondente à operação decodificada.
    Retorna o resultado e, em caso de JUMP, o novo endereço do PC.
    """
    print("\n[4] EXECUÇÃO")
    novo_pc = None  # Usado apenas pela instrução JUMP

    if operacao == "END":
        print("    Instrução END encontrada. Encerrando.")
        return None, None

    if operacao == "JUMP":
        print(f"    Desviando execução para a posição {a}")
        return None, a  # Retorna o novo PC diretamente

    if operacao == "MOV":
        print(f"    Valor {a} será armazenado no registrador")
        return a, novo_pc

    if operacao == "AVG":
        res = (a + b + c) / 3
        print(f"    ({a} + {b} + {c}) / 3 = {res}")
        return res, novo_pc

    # Operações com 3 operandos (destino + dois valores)
    if c is not None:
        if operacao == "ADD":
            res = b + c
            print(f"    {b} + {c} = {res}")
        elif operacao == "MUL":
            res = b * c
            print(f"    {b} × {c} = {res}")
        elif operacao == "SUB":
            res = b - c
            print(f"    {b} - {c} = {res}")
        return res, novo_pc

    # Operações com 2 operandos (formato padrão)
    if operacao == "ADD":
        res = a + b
        print(f"    {a} + {b} = {res}")
    elif operacao == "SUB":
        res = a - b
        print(f"    {a} - {b} = {res}")
    elif operacao == "MUL":
        res = a * b
        print(f"    {a} × {b} = {res}")
    elif operacao == "DIV":
        # Tratamento de erro: divisão por zero
        if b == 0:
            print(f"    ERRO: Divisão por zero! ({a} / {b})")
            return "ERRO_DIV_ZERO", novo_pc
        res = a / b
        print(f"    {a} / {b} = {res}")

    return res, novo_pc


def etapa5_armazenamento(operacao, resultado, ir):
    """
    ETAPA 5 - ARMAZENAMENTO DO RESULTADO
    O resultado produzido pela ULA é salvo no registrador de resultado
    ou em um registrador nomeado (ex: X, Y, Z) no caso de 3 operandos.
    """
    print("\n[5] ARMAZENAMENTO")

    if operacao in ("END", "JUMP") or resultado is None:
        print("    Nenhum resultado a armazenar.")
        return

    if resultado == "ERRO_DIV_ZERO":
        print("    Resultado não armazenado (erro de divisão por zero).")
        return

    # Se a instrução tem destino nomeado (ex: ADD X 30 12), salva em registrador
    if len(ir) == 4 and operacao in ("ADD", "MUL", "SUB"):
        destino = ir[1]
        registradores[destino] = resultado
        print(f"    {destino} = {resultado}")
    elif operacao == "MOV":
        registradores["ACC"] = resultado  # Armazena no acumulador
        print(f"    ACC = {resultado}")
    else:
        print(f"    Resultado armazenado = {resultado}")


def etapa6_atualiza_pc(pc, novo_pc=None):
    """
    ETAPA 6 - ATUALIZAÇÃO DO PROGRAM COUNTER
    Incrementa o PC para apontar para a próxima instrução.
    Se houver um JUMP, o PC recebe o endereço de destino diretamente.
    """
    print("\n[6] ATUALIZAÇÃO DO PC")
    if novo_pc is not None:
        print(f"    JUMP: PC = {novo_pc}")
        return novo_pc
    pc += 1
    print(f"    PC = {pc}")
    return pc

# LOOP PRINCIPAL DA CPU
# Simula o ciclo fetch-decode-execute continuamente até encontrar END.

def executar_cpu():
    global PC, IR, resultado

    print("\n" + "=" * 50)
    print("        CPU INICIADA - IFSULDEMINAS")
    print("=" * 50)

    while PC < len(memoria):

        # --- ETAPA 1: FETCH ---
        IR = etapa1_fetch(PC)

        # --- ETAPA 2: DECODE ---
        operacao = etapa2_decode(IR)

        # Tratamento especial para END (encerra o loop)
        if operacao == "END":
            print("\n[2] DECODIFICAÇÃO")
            print("    Operação identificada: Encerrar programa")
            print("\n[3..5] Instrução END não possui operandos ou resultado.")
            print("\nCPU DESLIGADA.")
            separador()
            break

        # --- ETAPA 3: BUSCA DE OPERANDOS ---
        a, b, c = etapa3_operandos(IR, operacao)

        # --- ETAPA 4: EXECUÇÃO ---
        resultado, novo_pc = etapa4_execucao(operacao, a, b, c)

        # --- ETAPA 5: ARMAZENAMENTO ---
        etapa5_armazenamento(operacao, resultado, IR)

        # --- ETAPA 6: ATUALIZAÇÃO DO PC ---
        PC = etapa6_atualiza_pc(PC, novo_pc)

        separador()

    # Exibe estado final dos registradores nomeados
    if registradores:
        print("\nESTADO FINAL DOS REGISTRADORES:")
        for reg, val in registradores.items():
            print(f"    {reg} = {val}")


# Ponto de entrada do programa
if __name__ == "__main__":
    executar_cpu()