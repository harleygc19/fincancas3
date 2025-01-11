import streamlit as st
import pandas as pd
from github import Github
import base64

# Configurações do GitHub
GITHUB_TOKEN = "seu_token_github"
GITHUB_REPO = "usuario/repo"
ARQUIVO_PATH = "Contas.xlsx"

# Função para salvar arquivo no GitHub
def salvar_no_github(conteudo_arquivo, mensagem_commit="Atualização do arquivo Contas.xlsx"):
    try:
        # Conectando à API do GitHub
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)

        # Obtendo o conteúdo atual do arquivo no GitHub
        try:
            conteudo_atual = repo.get_contents(ARQUIVO_PATH)
            sha_atual = conteudo_atual.sha  # SHA do arquivo atual
        except:
            sha_atual = None  # Arquivo ainda não existe

        # Convertendo conteúdo para base64
        conteudo_b64 = base64.b64encode(conteudo_arquivo).decode()

        # Criando ou atualizando o arquivo no repositório
        if sha_atual:
            repo.update_file(
                path=ARQUIVO_PATH,
                message=mensagem_commit,
                content=conteudo_b64,
                sha=sha_atual
            )
        else:
            repo.create_file(
                path=ARQUIVO_PATH,
                message=mensagem_commit,
                content=conteudo_b64
            )
        st.success("Arquivo salvo no GitHub com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar arquivo no GitHub: {e}")

# Função para salvar uma nova entrada no arquivo Excel
def cadastrar1(Categoria, Conta, Forma_de_pagamento, Data_do_pagamento, Status_do_pagamento, Valor_pago, OBS):
    nova_linha = {
        'Categoria': Categoria,
        'Conta': Conta,
        'Forma_de_pagamento': Forma_de_pagamento,
        'Data_do_pagamento': Data_do_pagamento,
        'Status_do_pagamento': Status_do_pagamento,
        'Valor_pago': Valor_pago,
        'OBS': OBS
    }
    df_nova_linha = pd.DataFrame([nova_linha])

    try:
        # Carregando o Excel existente ou criando um novo DataFrame
        try:
            df = pd.read_excel("Contas.xlsx")
        except FileNotFoundError:
            df = pd.DataFrame(columns=[
                "Categoria", "Conta", "Forma_de_pagamento", "Data_do_pagamento", 
                "Status_do_pagamento", "Valor_pago", "OBS"
            ])

        # Adicionando a nova linha
        df = pd.concat([df, df_nova_linha], ignore_index=True)

        # Salvando localmente
        df.to_excel("Contas.xlsx", index=False)

        # Lendo o arquivo salvo para envio ao GitHub
        with open("Contas.xlsx", "rb") as f:
            conteudo_arquivo = f.read()

        # Salvando no GitHub
        salvar_no_github(conteudo_arquivo)

    except Exception as e:
        st.error(f"Erro ao salvar no arquivo local: {e}")

# Interface do Streamlit
def main():
    st.title("Gerenciador de Contas")

    # Campos do formulário
    with st.form(key="incluir_conta"):
        Categoria = st.text_input("Categoria:")
        Conta = st.text_input("Conta:")
        Forma_de_pagamento = st.selectbox("Forma de pagamento:", ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix", "Outro"])
        Data_do_pagamento = st.date_input("Data do pagamento:")
        Status_do_pagamento = st.selectbox("Status do pagamento:", ["Pago", "Pendente"])
        Valor_pago = st.number_input("Valor pago:", min_value=0.0, format="%.2f")
        OBS = st.text_area("Observações:")
        
        botao_submit = st.form_submit_button("Salvar")

    # Ação ao clicar no botão Salvar
    if botao_submit:
        cadastrar1(Categoria, Conta, Forma_de_pagamento, Data_do_pagamento, Status_do_pagamento, Valor_pago, OBS)

if __name__ == "__main__":
    main()
