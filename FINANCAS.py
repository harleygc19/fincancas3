import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import plotly.express as px

st.set_page_config(page_title="Finanças HD",layout='wide',page_icon="logo2.png")

df = pd.read_excel('Contas.xlsx')

def verificar_credenciais(username, senha):
    try:
        df = pd.read_excel('senhas.xlsx')
    except FileNotFoundError:
        st.error('Arquivo senhas não encontrado')        
        return False
    except Exception as e:
        st.error(f'Erro ao ler o arquivo: {e}')
        return False

    if any((df["username"] == username) & (df["senha"] == senha)):
        return True
    return False





# Código para Página de login
def login_page():
    
    col1,col2,col3 = st.columns((0.5,1,0.5))
    with col2:

         imagem1 = st.image('logo1.png',use_column_width=True)
         imagem1 = st.sidebar.image('logo3.png',use_column_width=True)
   
    username = st.sidebar.text_input('login')
    
    senha = st.sidebar.text_input('senha',type='password')

    if st.sidebar.button('login'):
        if verificar_credenciais(username, senha):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else: 
            st.error('usuário ou senha incorretos, tente novamente')
    st.sidebar.text('Controle financeiro HD') 


def pag_inicial():
    st.subheader('Controle Financeiro HD',divider='gray')
    pag1, pag2, pag3 = st.tabs(['Cadastro de Gastros','Cadastro de Recebimentos','Tabela'])
    with pag1:
        tela_tabela()
        tela_formulario()

    with pag2:
        st.write ('Cadastro de recebimentos')

    with pag3:
        tela_tabela()



df = pd.read_excel('Contas.xlsx')


def formulario():

    try:
        df = pd.read_excel('Contas.xlsx')
        
        # Convertendo as colunas de datas para o formato dd/mm/aa
        colunas_de_data = ['Data_vencimento', 'Data_do_pagamento']  # Substitua pelos nomes corretos das suas colunas de data
        
        for coluna in colunas_de_data:
            df[coluna] = pd.to_datetime(df['coluna'], errors='coerce').dt.strftime('%d/%m/%y')
    
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Categoria', 'Conta', 'Data_vencimento', 'Data_do_pagamento', 'Status_do_pagamento', 'Valor_pago', 'OBS'])
    
    return df



def formulario_c_gastos1():
    @st.dialog('Cadastrar nova conta',width='big')
    def formulario_c_gastos():    
        
        lista_status = 'Pago','Pendente'
        
        dfcat = pd.read_excel('nome_categorias.xlsx')
        dfcat = dfcat[list]
        
        dfconta = pd.read_excel('nome_contas.xlsx')
        dfconta = dfconta[list]
        
        lista_categoria = dfcat
        lista_contas = dfconta


        if ' Categoria' not in st.session_state:
            st.session_state['Categoria'] = ''
        if 'Conta' not in st.session_state:
            st.session_state['Conta'] = ''
        if ' Data vencimento' not in st.session_state:
            st.session_state['Data_vencimento'] = ''
        if 'Data do pagamento' not in st.session_state:
            st.session_state['Data_do_pagamento'] = ''
        if 'Status do pagamento' not in st.session_state:
            st.session_state['Status_do_pagamento'] = ''
        if 'Valor_pago' not in st.session_state:
            st.session_state['Valor_pago'] = ''
        if 'OBS' not in st.session_state:
            st.session_state['OBS'] = ''
        
    
        st.session_state['Categoria'] = st.selectbox('Categoria',lista_categoria)
        st.session_state['Conta'] = st.selectbox('Conta', lista_contas)
        st.session_state['Data_vencimento']=st.date_input('Data vencimento')
        st.session_state['Data_do_pagamento']=st.date_input('Data do pagamento')
        st.session_state['Status_do_pagamento'] = st.selectbox('Status do Pagamento',lista_status)
        st.session_state['Valor_pago']=st.number_input('Valor pago')
        st.session_state['OBS'] = st.text_input('OBS')



        if st.button('Enviar'):
            cadastrar1(
            st.session_state['Categoria'],
            st.session_state['Conta'],
            st.session_state['Data_vencimento'],
            st.session_state['Data_do_pagamento'],
            st.session_state['Status_do_pagamento'],
            st.session_state['Valor_pago'],
            st.session_state['OBS'])
            st.rerun()
            
            st.success('Cadastro enviado com sucesso!')
        if st.button('Limpar'):
            st.session_state['Categoria']=''
            st.session_state['Conta']=''
            st.session_state['Data_vencimento']=''
            st.session_state['Data_do_pagamento']=''
            st.session_state['Status_do_pagamento']=''
            st.session_state['Valor_pago']=''
            st.session_state['OBS']
            st.rerun()

    if 'Novo gasto' not in st.session_state:
        if st.button('➕'):
            formulario_c_gastos()
    else:
        st.success('Novo gasto enviado com sucesso')
        
        

def cadastrar1(Categoria, Conta, Data_vencimento,  Data_do_pagamento, Status_do_pagamento, Valor_pago, OBS):

    nova_linha = {'Categoria': Categoria,
                  'Conta': Conta,
                  'Data_vencimento': Data_vencimento,
                  'Data_do_pagamento': Data_do_pagamento,
                  'Status_do_pagamento': Status_do_pagamento,
                  'Valor_pago': Valor_pago,
                  'OBS': OBS}
    df_nova_linha = pd.DataFrame([nova_linha])
    try:
        wb = load_workbook (filename="Contas.xlsx")
    except FileNotFoundError:
        df_nova_linha.to_excel("Contas.xlsx", index=False)
        wb = load_workbook(filename="Contas.xlsx")
    ws = wb.active
    proxima_linha = ws.max_row + 1

    for index, row in df_nova_linha.iterrows():
        for col, value in enumerate(row, start=1):
            ws.cell(row=proxima_linha, column=col, value=value)
    proxima_linha += 1

    wb.save(filename="Contas.xlsx")
    return df







def nova_categoria():

    @st.dialog("Cadastrar nova Categoria", width="big")  
    def cadastrar_categoria():
        
        if 'Nova_Categoria' not in st.session_state:
            st.session_state['Nova_Categoria'] = ''
        
        st.session_state['Nova_Categoria'] = st.text_input('Nova categoria', st.session_state['Nova_Categoria'])
        
        if st.button("Enviar"):
            cadastrar2(st.session_state['Nova_Categoria'])
            st.success('Cadastro enviado com sucesso!')
            st.rerun()  
        
        if st.button("Limpar"):
            st.session_state['Nova_Categoria'] = ''
            st.rerun()  
   
    if 'nova_categoria' not in st.session_state:
        if st.button("Abrir Formulário de Categoria"):
            cadastrar_categoria()  
    else:
        st.success("Categoria cadastrada com sucesso!")


def cadastrar2(Nova_Categoria):

    nova_linha2 = {'Nova_Categoria': Nova_Categoria}
    df_nova_linha2 = pd.DataFrame([nova_linha2])
    try:
        wb = load_workbook (filename="nome_categorias.xlsx")
    except FileNotFoundError:
        df_nova_linha2.to_excel("nome_categorias.xlsx", index=False)
        wb = load_workbook(filename="nome_categorias.xlsx")
    ws = wb.active
    proxima_linha = ws.max_row + 1

    for index, row in df_nova_linha2.iterrows():
        for col, value in enumerate(row, start=1):
            ws.cell(row=proxima_linha, column=col, value=value)
    proxima_linha += 1

    wb.save(filename="nome_categorias.xlsx")
    return df


def Nova_conta():
    
    # Controle do estado para abrir/fechar o formulário
    if 'form_aberto' not in st.session_state:
        st.session_state['form_aberto'] = False

    # Função para o formulário de cadastro de contas
    @st.dialog("Cadastrar nova conta", width="big")  
    def cadastrar_conta():
        
        # Verificar se a variável Nova_conta está no estado da sessão
        if 'Nova_conta' not in st.session_state:
            st.session_state['Nova_conta'] = ''
        
        # Campo de texto para inserir uma nova conta
        st.session_state['Nova_conta'] = st.text_input('Nova Conta', st.session_state['Nova_conta'])
        
        # Botão para enviar a nova conta
        if st.button("Enviar"):
            cadastrar3(st.session_state['Nova_conta'])
            st.success('Cadastro enviado com sucesso!')
            st.session_state['form_aberto'] = False  # Fechar o formulário
            st.rerun()  # Recarregar para exibir o botão novamente

        # Botão para limpar o formulário
        if st.button("Limpar"):
            st.session_state['Nova_conta'] = ''
            st.session_state['form_aberto'] = False  # Fechar o formulário
            st.rerun()  # Recarregar para exibir o botão novamente

    # Condição para exibir o botão "Abrir Formulário Conta"
    if not st.session_state['form_aberto']:
        if st.button("Abrir Formulário Conta"):
            st.session_state['form_aberto'] = True  # Abrir o formulário
            cadastrar_conta()  # Exibir o formulário

# Função que lida com o salvamento no arquivo Excel
def cadastrar3(Nova_conta):
    nova_linha3 = {'Nova_conta': Nova_conta}
    df_nova_linha3 = pd.DataFrame([nova_linha3])

    try:
        wb = load_workbook(filename="nome_contas.xlsx")
    except FileNotFoundError:
        df_nova_linha3.to_excel("nome_contas.xlsx", index=False)
        wb = load_workbook(filename="nome_contas.xlsx")

    ws = wb.active
    proxima_linha = ws.max_row + 1

    for index, row in df_nova_linha3.iterrows():
        for col, value in enumerate(row, start=1):
            ws.cell(row=proxima_linha, column=col, value=value)

    wb.save(filename="nome_contas.xlsx")



# Função principal para exibir os formulários
def tela_formulario():
    pos1, pos2, pos3, pos4, pos5 = st.columns([1,4,5,5,5])
    with pos1:
        formulario_c_gastos1()  # Sua função de gastos
    with pos2:
        nova_categoria()  # Sua função de categorias
    with pos3:
        Nova_conta()  # A função de nova conta
     

def tela_tabela():
    df = pd.read_excel('Contas.xlsx') 
    df = df.head(5)
    st.dataframe(df,hide_index=True)
    #graficos()








def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        pag_inicial()
    else:
        login_page()

if __name__ == "__main__":
    main()
