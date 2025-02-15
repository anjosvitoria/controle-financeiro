from models import Conta, engine, Bancos, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date, timedelta
import matplotlib.pyplot as plt


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
        
def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement= select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        #todo validar para ver se a conta esta ativa
        if historico.tipo ==Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError("saldo insuficiente")
            conta.valor -=historico.valor
            
        session.add(historico)
        session.commit()
        return historico

def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
    
    total = 0 
    for conta in contas:
        total += conta.valor
    return float(total)
    
#todo descrição do que o usuario comprou 
        
        
def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        resultados = session.exec(statement).all()
        return resultados

def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status == Status.ATIVO)
        contas = session.exec(statement).all()
        bancos= [i.banco.value for i in contas]
        total=[i.valor for i in contas]
        plt.bar(bancos, total)
        plt.show()
           
            
#criar_grafico_por_conta()
#x =buscar_historico_entre_datas(date.today() - timedelta(days=1), date.today() + timedelta(days=1))
#print(x)

#conta = Conta(valor=10, banco=Bancos.NUBANK)
#criar_conta(conta)
#desativar_conta(1)
#transferir_saldo(2, 3, 1)
#historico = Historico(conta_id=1, tipos=Tipos.ENTRADA,valor=10, data= date.today())
#movimentar_dinheiro(historico)
#print(total_contas())
