from models import Conta, engine, Bancos, Status
from sqlmodel import Session, select


def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        results = session.exec(statement).all()

        if results:
            print('ja existe uma conta nesse banco')
            return
        
        session.add(conta)
        session.commit()    
        return conta
    
def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results

def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta = session.exec(statement).first()
        if conta.valor > 0:
            raise ValueError('essa conta ainda possui saldo')
        conta.status = Status.INATIVO
        session.commit()
        
def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id_conta_saida)
        conta_saida = session.exec(statement).first()
        if conta_saida.valor < valor:
            raise ValueError('saldo insuficiente')
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        conta_entrada = session.exec(statement).first()
    
        conta_saida.valor -= valor
        conta_entrada.valor += valor
        session.commit()
        
#conta = Conta(valor=10, banco=Bancos.NUBANK)
#criar_conta(conta)
#desativar_conta(1)
transferir_saldo(2, 3, 1)