import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

path = os.path.dirname(__file__)

class MyException(Exception):
    pass

raise MyException(path)

# CSS - Estilos #######
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css(path + '/styles.css')
#######################

# Botão URL #######
from streamlit.components.v1 import html
def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)
#######################

# Sidebar #############
with st.sidebar:
   st.image(Image.open('img/eu.jpg'), width=200)
   st.markdown('### João Gabriel Wendling Alves')
   st.markdown('![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn: [linkedin.com/in/joaowendling](https://www.linkedin.com/in/joaowendling/)')
   st.markdown(':email: E-mail: [joaogabriel.alves11@gmail.com](mailto:joaogabriel.alves11@gmail.com)')
   st.markdown(':telephone_receiver: +55 (51) 99357-0403')

   with open('CV_JoaoGabrielWendlingAlves.pdf', "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button('Download CV', PDFbyte, file_name="CV_JoaoGabrielWendlingAlves.pdf",  mime='application/octet-stream')
#######################


# Início ##############
st.markdown('# João Wendling')
st.markdown('Data Analyst and Industrial Engineer. ')

st.markdown('### Summary')
st.markdown(''':chart_with_upwards_trend: Work experience in Data Analytics and Business Intelligence projects, automating, collecting, cleaning, exploring, analyzing, and visualizing data using tools such as `SQL`, `Power BI`, `Python` and `Excel`.''')
st.markdown(''':brain: Passionate about using data as a decision-making and problem-solving tool. I am curious, collaborative and result oriented. ''')          
st.markdown(''':mortar_board: Degree in Industrial Engineering''')
st.markdown(''':beginner: Certifications: Power BI Data Analyst Associate (Microsoft) and C1 English (Cambridge CAE)''')

st.markdown('### Projects')
########################

# Ler tabelas projetos #
df = pd.read_excel('projetos.xlsx')
df = df.sort_values(by='Ordem')
########################

# Botões tags #########

tags = df['Tag'].unique().tolist()
skills = tags + ['All']
skill_col_size = 5

colunas_botoes = st.columns(skill_col_size)
def skill_tab():
    rows = len(skills)//skill_col_size
    skills2 = iter(skills)
    if len(skills)%skill_col_size!=0:
        rows+=1
    for x in range(rows):
        columns = st.columns(skill_col_size)
        for index_ in range(skill_col_size):
            skill = next(skills2)
            try:
                columns[index_].button(skill, key=skill)
            except:
                break
with st.spinner(text="Loading section..."):
    skill_tab()

#######################

# Quais projetos mostrar #######

# Qual tag está selecionada
tag = ''
for key in st.session_state.keys():
    if st.session_state[key]:
        tag = key

df_projetos_visualizados = df.copy()

if tag in tags:
    # se for alguma das tags, filtra o df
    df_projetos_visualizados = df_projetos_visualizados[df_projetos_visualizados['Tag'] == tag]
else:
    # mostra todos
    df_projetos_visualizados = df.copy()

# Divide o df
n_columns_projects = 2
dfs = { }

for i in range(n_columns_projects):
    dfs[i] = pd.DataFrame()

# Popula os dfs divididos
for i_proj in range(len(df_projetos_visualizados)):
    coluna = i_proj %  n_columns_projects
    dfs[coluna] = pd.concat([dfs[coluna], df_projetos_visualizados.iloc[i_proj,:]], axis=1, ignore_index=True) 
# transpose pq ele fica com as linhas como colunas
for i in range(n_columns_projects):
    dfs[i] = dfs[i].transpose()

#######################


# Display colunas #####
colunas = st.columns(n_columns_projects, gap='medium')

for i,coluna in enumerate(colunas):
    with coluna:
        df = dfs[i]
        for j, row in df.iterrows():
            with st.expander('**' + row['Título'] + '**', expanded=True):
                st.image(Image.open(row['Imagem']), use_column_width=True)
                st.markdown(row['Descrição'])
              #  if row['EscritoBotao'] != 'n':
              #      st.button(row['EscritoBotao'], key=j, on_click=open_page, args=(row['LinkBotao'],), kwargs=None, disabled=False)
 
#######################

