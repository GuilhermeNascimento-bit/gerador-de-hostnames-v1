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

# ----------- Listagem de categorias -----------
def listar_categorias(dados, chave, titulo):
    print(f"\n=== {titulo} cadastrados ===")
    if not dados[chave]:
        print("Nenhum cadastrado.")
        return
    for nome, codigo in dados[chave].items():
        print(f"{codigo}-{nome}")

# ----------- Consulta setores/maquinas -----------
def consultar_setores():
    dados = carregar_dados()
    if not dados["maquinas"]:
        print("Nenhum setor cadastrado ainda.")
        return
    
    setores = list(dados["maquinas"].keys())
    print("\n=== Setores disponíveis ===")
    for i, setor in enumerate(setores, start=1):
        qtd = len(dados["maquinas"][setor])
        print(f"{i} - {setor} ({qtd} máquinas)")

    try:
        opcao = int(input("\nQual setor gostaria de consultar? "))
        setor_escolhido = setores[opcao - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    maquinas = dados["maquinas"][setor_escolhido]

    # organiza por prefixos (fornecedor, tipo, local) para agrupar
    grupos = {}
    for hostname in maquinas.values():
        codigos = hostname.split("-")[1]  # CNL-<forn><tipo><setor><local>-<num>
        grupo = codigos
        grupos.setdefault(grupo, []).append(hostname)

    print(f"\n=== Máquinas do setor {setor_escolhido} ===")
    for grupo, hosts in grupos.items():
        print(f"\nGrupo {grupo}:")
        for h in sorted(hosts):
            print(f" - {h}")

# ----------- Adicionar fornecedor/setor/tipo/local -----------
def adicionar_fornecedor(nome_predefinido=None):
    dados = carregar_dados()
    if nome_predefinido:
        nome = nome_predefinido.lower()
        print(f"📥 Cadastrando fornecedor '{nome}'")
    else:
        nome = input("Nome do fornecedor: ").lower()

    while True:
        codigo = input("Código do fornecedor: ")
        if codigo in dados["fornecedores"].values():
            print(f"❌ Código {codigo} já está em uso! Escolha outro.")
        else:
            break

    dados["fornecedores"][nome] = codigo
    salvar_dados(dados)
    print(f"Fornecedor '{nome}' adicionado.")

def adicionar_setor(nome_predefinido=None):
    dados = carregar_dados()
    if nome_predefinido:
        nome = nome_predefinido.lower()
        print(f"📥 Cadastrando setor '{nome}'")
    else:
        nome = input("Nome do setor: ").lower()

    while True:
        codigo = input("Código do setor (ex: 01): ")
        if codigo in dados["setores"].values():
            print(f"❌ Código {codigo} já está em uso! Escolha outro.")
        else:
            break

    dados["setores"][nome] = codigo
    salvar_dados(dados)
    print(f"Setor '{nome}' adicionado.")

def adicionar_tipo(nome_predefinido=None):
    dados = carregar_dados()
    if nome_predefinido:
        nome = nome_predefinido.lower()
        print(f"📥 Cadastrando tipo '{nome}'")
    else:
        nome = input("Nome do tipo (ex: laptop/desktop): ").lower()

    while True:
        codigo = input("Código do tipo (ex: L/D/S): ").upper()
        if codigo in dados["tipos"].values():
            print(f"❌ Código {codigo} já está em uso! Escolha outro.")
        else:
            break

    dados["tipos"][nome] = codigo
    salvar_dados(dados)
    print(f"Tipo '{nome}' adicionado.")

def adicionar_local(nome_predefinido=None):
    dados = carregar_dados()
    if nome_predefinido:
        nome = nome_predefinido.lower()
        print(f"📥 Cadastrando local '{nome}'")
    else:
        nome = input("Nome do local (ex: fabrica/escritorio): ").lower()

    while True:
        codigo = input("Código do local (ex: 1/2): ")
        if codigo in dados["locais"].values():
            print(f"❌ Código {codigo} já está em uso! Escolha outro.")
        else:
            break

    dados["locais"][nome] = codigo
    salvar_dados(dados)
    print(f"Local '{nome}' adicionado.")


# ----------- Helper genérico p/ validar e cadastrar se faltar -----------
def obter_codigo(dados_iniciais, chave_dict, label, prompt, func_adicionar):
    dados_local = dados_iniciais
    houve_cadastro = False
    while True:
        listar_categorias(dados_local, chave_dict, label.capitalize())
        nome = input(prompt).strip().lower()
        if nome in dados_local[chave_dict]:
            return nome, dados_local[chave_dict][nome], houve_cadastro
        resp = input(f"{label.capitalize()} '{nome}' não encontrado. Deseja cadastrar? (sim/nao): ").strip().lower()
        if resp in ("sim", "s"):
            func_adicionar(nome)
            dados_local = carregar_dados()
            houve_cadastro = True
        elif resp in ("nao", "n", "não"):
            print(f"Digite outro {label}.")
        else:
            print("Resposta inválida. Digite 'sim' ou 'nao'.")

# ----------- Helper para número da máquina -----------
def obter_numero_disponivel(maquinas):
    usados = sorted(int(num) for num in maquinas.keys()) if maquinas else []
    max_num = max(usados) if usados else 0

    while True:
        escolha = input(f"Digite o número da máquina (1-{max_num + 1}) ou Enter para automático: ").strip()
        if escolha == "":
            # automático: pega o primeiro disponível
            for i in range(1, max_num + 2):
                if i not in usados:
                    return i
        else:
            try:
                num = int(escolha)
                if num in usados:
                    print(f"❌ Número {num:03d} já existe. Escolha outro.")
                elif num <= 0:
                    print("❌ Número inválido. Deve ser maior que zero.")
                else:
                    return num
            except ValueError:
                print("❌ Entrada inválida. Digite um número ou Enter.")

# ----------- Gerar hostname -----------
def gerar_hostname():
    dados = carregar_dados()

    forn_nome, fornecedor, add1 = obter_codigo(dados, "fornecedores", "fornecedor", "Fornecedor: ", adicionar_fornecedor)
    tipo_nome, tipo, add2 = obter_codigo(dados, "tipos", "tipo", "Tipo de máquina: ", adicionar_tipo)
    setor_nome, setor, add3 = obter_codigo(dados, "setores", "setor", "Setor: ", adicionar_setor)
    local_nome, local, add4 = obter_codigo(dados, "locais", "local", "Local: ", adicionar_local)

    if any([add1, add2, add3, add4]):
        dados = carregar_dados()

    if setor_nome not in dados["maquinas"]:
        dados["maquinas"][setor_nome] = {}

    maquinas = dados["maquinas"][setor_nome]

    numero = obter_numero_disponivel(maquinas)

    hostname = f"CNL-{fornecedor}{tipo}{setor}{local}-{numero:03d}"

    maquinas[f"{numero:03d}"] = hostname
    salvar_dados(dados)

    print(f"✅ Hostname gerado: {hostname}")

# ----------- Excluir hostname -----------
def excluir_hostname():
    dados = carregar_dados()
    hostname = input("Digite o hostname para excluir: ").strip()
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
        print("2 - Adicionar maquina")
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
