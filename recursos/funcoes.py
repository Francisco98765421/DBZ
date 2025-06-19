import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    try:
        with open("base.atitus", "r") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dados[nome] = {
        "pontos": pontos,
        "data_hora": agora
    }

    with open("base.atitus", "w") as arquivo:
        json.dump(dados, arquivo, indent=4)