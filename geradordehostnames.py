import json
import os

ARQUIVO = "base.json"

def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {"fornecedores": {}, "setores": {}, "tipos": {}, "locais": {}, "maquinas": {}}

def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

# ----------- Consulta setores/maquinas -----------
def consultar_setores():
    dados = carregar_dados()
    if not dados["maquinas"]:
        print("Nenhum setor cadastrado ainda.")
        return
    for setor, maquinas in dados["maquinas"].items():
        qtd = len(maquinas)
        print(f"Setor: {setor} - {qtd} máquinas")

# ----------- Adicionar fornecedor/setor/tipo/local -----------
def adicionar_fornecedor():
    dados = carregar_dados()
    nome = input("Nome do fornecedor: ").lower()
    codigo = input("Código do fornecedor: ")
    dados["fornecedores"][nome] = codigo
    salvar_dados(dados)
    print(f"Fornecedor {nome} adicionado.")

def adicionar_setor():
    dados = carregar_dados()
    nome = input("Nome do setor: ").lower()
    codigo = input("Código do setor (ex: 01): ")
    dados["setores"][nome] = codigo
    salvar_dados(dados)
    print(f"Setor {nome} adicionado.")

def adicionar_tipo():
    dados = carregar_dados()
    nome = input("Nome do tipo (ex: laptop/desktop): ").lower()
    codigo = input("Código do tipo (ex: L/D/S): ").upper()
    dados["tipos"][nome] = codigo
    salvar_dados(dados)
    print(f"Tipo {nome} adicionado.")

def adicionar_local():
    dados = carregar_dados()
    nome = input("Nome do local (ex: fabrica/escritorio): ").lower()
    codigo = input("Código do local (ex: 1/2): ")
    dados["locais"][nome] = codigo
    salvar_dados(dados)
    print(f"Local {nome} adicionado.")

# ----------- Gerar hostname -----------
def gerar_hostname():
    dados = carregar_dados()

    fornecedor_nome = input("Fornecedor: ").lower()
    if fornecedor_nome not in dados["fornecedores"]:
        print("Fornecedor não encontrado.")
        return
    fornecedor = dados["fornecedores"][fornecedor_nome]

    tipo_nome = input("Tipo de máquina: ").lower()
    if tipo_nome not in dados["tipos"]:
        print("Tipo não encontrado.")
        return
    tipo = dados["tipos"][tipo_nome]

    setor_nome = input("Setor: ").lower()
    if setor_nome not in dados["setores"]:
        print("Setor não encontrado.")
        return
    setor = dados["setores"][setor_nome]

    local_nome = input("Local: ").lower()
    if local_nome not in dados["locais"]:
        print("Local não encontrado.")
        return
    local = dados["locais"][local_nome]

    # Inicializa setor no JSON se não existir
    if setor_nome not in dados["maquinas"]:
        dados["maquinas"][setor_nome] = {}

    maquinas = dados["maquinas"][setor_nome]

    # Descobrir próximo número disponível
    usados = sorted(int(num) for num in maquinas.keys())
    numero = None
    for i in range(1, max(usados, default=0) + 2):
        if i not in usados:
            numero = i
            break

    hostname = f"CNL-{fornecedor}{tipo}{setor}{local}-{numero:03d}"

    maquinas[f"{numero:03d}"] = hostname
    salvar_dados(dados)

    print(f"✅ Hostname gerado: {hostname}")

# ----------- Excluir hostname -----------
def excluir_hostname():
    dados = carregar_dados()
    hostname = input("Digite o hostname para excluir: ")
    for setor, maquinas in dados["maquinas"].items():
        for numero, nome in list(maquinas.items()):
            if nome == hostname:
                del maquinas[numero]
                salvar_dados(dados)
                print(f"Hostname {hostname} excluído com sucesso.")
                return
    print("Hostname não encontrado.")

# ----------- Menu principal -----------
def menu():
    while True:
        print("\n######## MENU ########")
        print("1 - Consultar setores")
        print("2 - Adicionar máquina")
        print("3 - Excluir hostname")
        print("4 - Adicionar fornecedor")
        print("5 - Adicionar setor")
        print("6 - Adicionar tipo")
        print("7 - Adicionar local")
        print("8 - Sair")
        escolha = input("Escolha: ")

        if escolha == "1":
            consultar_setores()
        elif escolha == "2":
            gerar_hostname()
        elif escolha == "3":
            excluir_hostname()
        elif escolha == "4":
            adicionar_fornecedor()
        elif escolha == "5":
            adicionar_setor()
        elif escolha == "6":
            adicionar_tipo()
        elif escolha == "7":
            adicionar_local()
        elif escolha == "8":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# ----------- Executar programa -----------
menu()
