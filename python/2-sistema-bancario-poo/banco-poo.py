from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.conta.append(conta)
    
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falho! Você não tem saldo suficiente.")

        elif valor > 0:
            self.saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Operação valhor! Valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósido realzado com sucesso!")
        else:
            print("Operação falhou! Valor informado e inválido.")
            return False
        return True

    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transcao):
        self._transacoes.append(
            {
                "tipo": transcao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta:Conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta: Conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    cpf = input("Informe CPF do cliente: ")
    cliente : Cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def depositar(clientes):
    cpf = input("Informe CPF do cliente: ")
    cliente : Cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

    
def retirar_extrato(clientes):
    cpf = input("Informe CPF do cliente: ")
    cliente : Cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("=========== Extrato ==========")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n {transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=====================================")

def criar_usuario(usuarios):
    cpf = input("Informe CPF (somente número): ")
    
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario: 
        print("Usuário já existe")
        return

    nome = input("Informe o nome completo: ") 
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append({ "nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco })
    
    print("Usuário criado com sucesso!")
    
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print(" Usuário não encontrado, fluxo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta["agencia"]}
            C/C:\t\t{conta["numero_conta"]}
            Titular:\t{conta["usuario"]["nome"]}
        """
        print("*" * 100)
        print(linha)

def filtrar_usuario(cpf, clientes):
    usuarios_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_cliente(cliente):
    pass

def main():

    clientes = []
    contas = []

    menu = """

    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nu] Novo usuario
    [nc] Nova conta
    [lc] Listar contas
    [q]  Sair

    => """

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    contas = []
    usuarios = []

    while True:

        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Valor: "))
            saldo, extrato, numero_saques = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Valor para saque: "))
            saldo, extrato = sacar(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            retirar_extrato(saldo, extrato=extrato)
        
        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)
                
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
    
main()