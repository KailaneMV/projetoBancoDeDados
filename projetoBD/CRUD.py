import sqlite3
conn = sqlite3.connect('baseDeDados.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS contas (
    numero_conta TEXT PRIMARY KEY,
    nome_cliente TEXT NOT NULL,
    saldo REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_conta TEXT NOT NULL,
    tipo TEXT NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (numero_conta) REFERENCES contas (numero_conta)
)
''')

conn.commit()


def criar_conta():
    nome_cliente = input("Digite o nome do cliente: ")
    numero_conta = input("Digite o número da conta: ")
    saldo_inicial = float(input("Digite o saldo inicial: "))
    try:
        cursor.execute("INSERT INTO contas (numero_conta, nome_cliente, saldo) VALUES (?, ?, ?)",
                       (numero_conta, nome_cliente, saldo_inicial))
        conn.commit()
        print("Conta criada com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro: Número de conta já existe.")

def consultar_saldo():
    numero_conta = input("Digite o número da conta: ")
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    resultado = cursor.fetchone()
    if resultado:
        print(f"Saldo atual: R$ {resultado[0]:.2f}")
    else:
        print("Erro: Conta não encontrada.")

def depositar():
    numero_conta = input("Digite o número da conta: ")
    valor = float(input("Digite o valor do depósito: "))
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    resultado = cursor.fetchone()
    if not resultado:
        print("Erro: Conta não encontrada.")
        return
    if valor <= 0:
        print("Erro: Valor de depósito inválido.")
        return
    novo_saldo = resultado[0] + valor
    cursor.execute("UPDATE contas SET saldo = ? WHERE numero_conta = ?", (novo_saldo, numero_conta))
    cursor.execute("INSERT INTO historico (numero_conta, tipo, valor) VALUES (?, ?, ?)", (numero_conta, "depósito", valor))
    conn.commit()
    print(f"Depósito realizado. Novo saldo: R$ {novo_saldo:.2f}")

def sacar():
    numero_conta = input("Digite o número da conta: ")
    valor = float(input("Digite o valor do saque: "))
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    resultado = cursor.fetchone()
    if not resultado:
        print("Erro: Conta não encontrada.")
        return
    if valor <= 0:
        print("Erro: Valor de saque inválido.")
        return
    if resultado[0] < valor:
        print("Erro: Saldo insuficiente.")
        return
    novo_saldo = resultado[0] - valor
    cursor.execute("UPDATE contas SET saldo = ? WHERE numero_conta = ?", (novo_saldo, numero_conta))
    cursor.execute("INSERT INTO historico (numero_conta, tipo, valor) VALUES (?, ?, ?)", (numero_conta, "saque", valor))
    conn.commit()
    print(f"Saque realizado. Novo saldo: R$ {novo_saldo:.2f}")

def encerrar_conta():
    numero_conta = input("Digite o número da conta: ")
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    resultado = cursor.fetchone()
    if not resultado:
        print("Erro: Conta não encontrada.")
        return
    if resultado[0] != 0:
        print("Erro: A conta só pode ser encerrada com saldo zero.")
        return
    cursor.execute("DELETE FROM contas WHERE numero_conta = ?", (numero_conta,))
    conn.commit()
    print("Conta encerrada com sucesso.")

def mostrar_historico():
    numero_conta = input("Digite o número da conta: ")
    cursor.execute("SELECT tipo, valor FROM historico WHERE numero_conta = ?", (numero_conta,))
    historico = cursor.fetchall()
    if not historico:
        print("Sem movimentações no histórico.")
    else:
        print("Histórico de movimentações:")
        for tipo, valor in historico:
            print(f"- {tipo}: R$ {valor:.2f}")

def menu():
    while True:
        print("\nMenu Principal")
        print("1. Criar conta")
        print("2. Consultar saldo")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Encerrar conta")
        print("6. Mostrar histórico")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            consultar_saldo()
        elif opcao == "3":
            depositar()
        elif opcao == "4":
            sacar()
        elif opcao == "5":
            encerrar_conta()
        elif opcao == "6":
            mostrar_historico()
        elif opcao == "7":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()

conn.close()
