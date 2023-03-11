import sqlite3

def criar_conta(numero, nome, senha):
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()

    c.execute('INSERT INTO contas VALUES (?, ?, ?, 0)', (numero, nome, senha))
    
    conn.commit()
    conn.close()

def autenticar_conta(numero, senha):
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()

    c.execute('SELECT * FROM contas WHERE numero = ? AND senha = ?', (numero, senha))
    conta = c.fetchone()
    
    conn.close()
    
    return conta

def depositar(conta, valor):
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()

    c.execute('UPDATE contas SET saldo = saldo + ? WHERE numero = ?', (valor, conta[0]))
    c.execute('INSERT INTO transacoes (tipo, valor, data, conta) VALUES (?, ?, CURRENT_TIMESTAMP, ?)', ('depósito', valor, conta[0]))

    conn.commit()
    conn.close()

def sacar(conta, valor):
    if valor > 500:
        print('Limite máximo por saque é de R$ 500,00')
        return
    if valor > conta[3]:
        print('Saldo insuficiente')
        return
        
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()

    c.execute('UPDATE contas SET saldo = saldo - ? WHERE numero = ?', (valor, conta[0]))
    c.execute('INSERT INTO transacoes (tipo, valor, data, conta) VALUES (?, ?, CURRENT_TIMESTAMP, ?)', ('saque', valor, conta[0]))

    conn.commit()
    conn.close()

class Conta:
   def __init__(self, numero, titular, senha, saldo=0):
        self.numero = numero
        self.titular = titular
        self.senha = senha
        self.saldo = saldo
        self.transacoes = []
        

def extrato(conta):
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()

    c.execute('SELECT * FROM transacoes WHERE conta = ? ORDER BY data', (conta[0],))
    transacoes = c.fetchall()

    if isinstance(conta, tuple):
        conta = Conta(*conta)
        print(f'Extrato da conta {conta.numero} - {conta.titular}')
        saldo_atual = conta.saldo

    for transacao in conta.transacoes:
        if isinstance(transacao.valor, str):
            print(f'{transacao.data} - {transacao.tipo}: {transacao.valor}')
        else:
            print(f'{transacao.data} - {transacao.tipo}: R$ {transacao.valor:.2f}')

    print(f'Saldo atual: R$ {saldo_atual:.2f}')

def login():
    numero_conta = input('Digite o número da conta: ')
    senha_conta = input('Digite a senha: ')
    conta = autenticar_conta(numero_conta, senha_conta)
    if conta is not None:
        menu_principal(conta, numero_conta, senha_conta)
    else:
        print('Conta não encontrada ou senha incorreta.')

def criar_conta_menu():
    numero_conta = input('Digite o número da conta: ')
    senha_conta = input('Digite a senha: ')
    nome_conta = input('Digite o nome do titular: ')

    criar_conta(numero_conta, nome_conta, senha_conta)

    print('Conta criada com sucesso.')
    login()


def menu_principal(conta, numero_conta, senha_conta):
    while True:
        print('Selecione uma opção:')
        print('1 - Depósito')
        print('2 - Saque')
        print('3 - Extrato')
        print('4 - Sair')
        
        opcao = int(input())

        if opcao == 1:
            valor = float(input('Digite o valor a ser depositado: '))
            depositar(conta, valor)
            print('Depósito realizado com sucesso.')

        elif opcao == 2:
            valor = float(input('Digite o valor a ser sacado: '))
            sacar(conta, valor)

        elif opcao == 3:
            conta = autenticar_conta(numero_conta, senha_conta)
            extrato(conta)

        elif opcao == 4:
            break

        else:
            print('Opção inválida.')

def login_menu():
    while True:
        print('Selecione uma opção:')
        print('1 - Login')
        print('2 - Criar conta')
        print('3 - Sair')

        opcao = int(input())

        if opcao == 1:
            login()
            break

        elif opcao == 2:
            criar_conta_menu()
            continue

        elif opcao == 3:
            break

        else:
            print('Opção inválida.')
    
if __name__ == '__main__':
    login_menu()