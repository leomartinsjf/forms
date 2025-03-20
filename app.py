import streamlit as st
import json
import os
import base64
import requests
from datetime import datetime
import time

# GitHub API configuration
GITHUB_REPO = "leomartinsjf/FORMS"  # Replace with your actual GitHub username/repo
GITHUB_TOKEN = st.secrets["github_token"] if "github_token" in st.secrets else None
GITHUB_FILE_PATH = "dados_insercao.json"

# Function to check if running on Streamlit Cloud
def is_streamlit_cloud():
    return "STREAMLIT_SHARING_MODE" in os.environ or "STREAMLIT_RUN_PATH" in os.environ

# Function to load data from GitHub
def load_data_from_github():
    if not GITHUB_TOKEN:
        st.warning("GitHub token not found in secrets. Using local file storage.")
        return None
        
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Get the file content from GitHub
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Decode the content
            content = response.json()
            file_content = base64.b64decode(content["content"]).decode("utf-8")
            # Get the current SHA (needed for updating the file later)
            sha = content["sha"]
            
            # Parse the JSON content
            data = json.loads(file_content)
            return data, sha
        else:
            if response.status_code == 404:
                # File doesn't exist yet
                return [], None
            else:
                st.error(f"Failed to load data from GitHub: {response.status_code}")
                st.json(response.json())
                return None
                
    except Exception as e:
        st.error(f"Error loading data from GitHub: {str(e)}")
        return None
        
# Function to save data to GitHub
def save_data_to_github(data, sha=None):
    if not GITHUB_TOKEN:
        st.warning("GitHub token not found in secrets. Using local file storage.")
        return False
        
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Convert data to JSON and encode for GitHub
    json_data = json.dumps(data, indent=4)
    encoded_content = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")
    
    # Prepare the request payload
    payload = {
        "message": f"Update data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": encoded_content
    }
    
    # If updating an existing file, include the SHA
    if sha:
        payload["sha"] = sha
        
    try:
        # Update the file on GitHub
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            return True
        else:
            st.error(f"Failed to save data to GitHub: {response.status_code}")
            st.json(response.json())
            return False
            
    except Exception as e:
        st.error(f"Error saving data to GitHub: {str(e)}")
        return False

# Function to load existing data
def load_data():
    # First, check if we're on Streamlit Cloud and should use GitHub
    if is_streamlit_cloud() and GITHUB_TOKEN:
        github_data = load_data_from_github()
        if github_data:
            data, _ = github_data
            return data
    
    # Fall back to local file if not on Streamlit Cloud or GitHub failed
    try:
        with open("dados_insercao.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save data
def save_data(data_list):
    # If on Streamlit Cloud, try to save to GitHub
    if is_streamlit_cloud() and GITHUB_TOKEN:
        # Get the current SHA
        _, sha = load_data_from_github() or (None, None)
        # Save to GitHub
        if save_data_to_github(data_list, sha):
            return
    
    # Fall back to local file
    with open("dados_insercao.json", "w") as file:
        json.dump(data_list, indent=4)

# Initialize session state for tracking form submission
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Load existing data
existing_data = load_data()

# Display GitHub status if applicable
if is_streamlit_cloud():
    if GITHUB_TOKEN:
        st.sidebar.success("GitHub storage is configured")
    else:
        st.sidebar.warning("GitHub token not found in secrets. Data will not persist.")

st.title("Formulário de Inserção Social - Quadriênio 2021-2024")

# -------------------------------
# Seção 1: Dados do Programa e do Respondente
# -------------------------------
st.header("Seção 1: Dados do Programa e do Respondente")

sigla = st.text_input("Sigla do Programa", "Ex.: PPGPC")
nome_completo = st.text_input("Nome Completo do Programa", "Ex.: Programa de Pós-Graduação em Psicologia Clínica")
instituicao = st.text_input("Instituição", "Ex.: Pontifícia Universidade Católica do Rio de Janeiro")
modalidade = st.selectbox("Modalidade", options=["Apenas Mestrado", "Mestrado e Doutorado"])
dp = st.number_input("Número médio de docentes (DP)", min_value=1, value=18, key="dp_input")
st.markdown("**Observação:** O número de ações a serem relatadas deve ser igual a DP/2 (máximo de 10 ações).")

# -------------------------------
# Seção 2: Relato Detalhado das Atividades
# -------------------------------
st.header("Seção 2: Relato Detalhado das Atividades")

# A. Cursos de Especialização (Lato Sensu)
st.subheader("A. Cursos de Especialização (Lato Sensu)")
oferta_especializacao = st.checkbox("Ofertou curso(s) de especialização (lato sensu) durante 2021-2024?")
if oferta_especializacao:
    cursos_especializacao = st.text_area("Liste os nomes dos cursos de especialização ofertados durante o período.")
    descricao_especializacao = st.text_area("Descreva os objetivos, tópicos abordados e a metodologia de cada curso.")
    alunos_especializacao = st.text_area("Informe o número de alunos matriculados em cada curso (separar por vírgula se houver mais de um).")
    duracao_especializacao = st.text_input("Informe a duração dos cursos (em meses ou períodos).")
    docentes_especializacao = st.number_input("Número de docentes envolvidos", min_value=0, value=0, key="docentes_especializacao")
    impacto_especializacao = st.text_area("Descreva os principais resultados e impactos (ex.: desempenho, publicações, projetos de seguimento).")

# B. Cursos de Extensão e Atividades de Divulgação
st.subheader("B. Cursos de Extensão e Atividades de Divulgação")
oferta_extensao = st.checkbox("Ministrou cursos de extensão ou atividades de divulgação durante 2021-2024?")
if oferta_extensao:
    cursos_extensao = st.text_area("Liste os nomes e descreva brevemente os cursos de extensão/atividades de divulgação realizadas.")
    participantes_extensao = st.text_area("Informe o número de participantes de cada atividade (separar por vírgula, se aplicável).")
    duracao_extensao = st.text_input("Informe a duração de cada atividade (em meses ou períodos).")
    docentes_extensao = st.number_input("Número de docentes envolvidos", min_value=0, value=0, key="docentes_extensao")
    impacto_extensao = st.text_area("Descreva os principais resultados ou impactos (ex.: capacitação, feedback da comunidade).")

# C. Consultorias e Atividades de Assessoria
st.subheader("C. Consultorias e Atividades de Assessoria")
oferta_consultoria = st.checkbox("Atuou em consultorias ou assessorias (sem emissão de relatórios formais) durante 2021-2024?")
if oferta_consultoria:
    detalhes_consultoria = st.text_area("Detalhe o nome da agência/organização e a atividade realizada em cada consultoria.")
    duracao_consultoria = st.text_input("Informe a duração de cada consultoria (em meses).")
    docentes_consultoria = st.number_input("Número de docentes envolvidos", min_value=0, value=0, key="docentes_consultoria")
    impacto_consultoria = st.text_area("Descreva os resultados ou impactos (ex.: mudanças de política, capacitação).")

# D. Participação e Coordenação de Redes de Pesquisa
st.subheader("D. Participação e Coordenação de Redes de Pesquisa")
oferta_redes = st.checkbox("Participou ou coordenou redes de pesquisa (nacionais/internacionais) durante 2021-2024?")
if oferta_redes:
    redes = st.text_area("Liste os nomes das redes ou consórcios de pesquisa que você participou ou coordenou.")
    papel_redes = st.text_area("Descreva seu papel em cada rede (ex.: participante, coordenador, assessor).")
    duracao_redes = st.text_input("Informe a duração da participação em cada rede.")
    resultados_redes = st.text_area("Liste os principais resultados colaborativos (ex.: publicações, eventos, propostas).")

# E. Organização e Participação em Eventos Científicos
st.subheader("E. Organização e Participação em Eventos Científicos")
oferta_eventos = st.checkbox("Organizou ou participou de eventos científicos (congressos, simpósios, webinars) durante 2021-2024?")
if oferta_eventos:
    eventos = st.text_area("Informe o título e o tipo de cada evento realizado.")
    publico_eventos = st.text_area("Informe o número de participantes e descreva o público-alvo de cada evento.")
    duracao_eventos = st.text_input("Informe a duração e a frequência dos eventos.")
    impacto_eventos = st.text_area("Descreva os impactos ou resultados dos eventos (ex.: colaborações, cobertura de mídia).")

# F. Intervenções para Populações Vulneráveis e Comunidades
st.subheader("F. Intervenções para Populações Vulneráveis e Comunidades")
oferta_interv = st.checkbox("Implementou intervenções ou projetos para comunidades vulneráveis durante 2021-2024?")
if oferta_interv:
    interv = st.text_area("Descreva a intervenção: qual comunidade foi atendida, objetivos e principais atividades.")
    beneficiados = st.number_input("Número de beneficiados", min_value=0, value=0)
    duracao_interv = st.text_input("Informe a duração da intervenção (em meses).")
    docentes_interv = st.number_input("Número de docentes envolvidos", min_value=0, value=0, key="docentes_interv")
    metricas_interv = st.text_area("Descreva as métricas de avaliação utilizadas (ex.: feedback, indicadores de bem-estar).")

# G. Atividades em Educação Básica (Escolas)
st.subheader("G. Atividades em Educação Básica (Escolas)")
oferta_escolas = st.checkbox("Realizou atividades em escolas (públicas ou privadas) durante 2021-2024?")
if oferta_escolas:
    atividade_escolas = st.text_area("Descreva a atividade realizada (ex.: palestras, workshops, sessões interativas) e o público-alvo (alunos, professores ou ambos).")
    sessoes_escolas = st.number_input("Número de sessões", min_value=0, value=0, key="sessoes_escolas")
    participantes_escolas = st.number_input("Número total de participantes", min_value=0, value=0, key="participantes_escolas")
    duracao_escolas = st.text_input("Informe a duração total das atividades (em meses ou períodos).")
    avaliacao_escolas = st.text_area("Descreva como foi avaliado o impacto da atividade (ex.: feedback, mudanças no ambiente escolar).")

# -------------------------------
# Seção 3: Reflexões Gerais e Métricas Adicionais
# -------------------------------
st.header("Seção 3: Reflexões Gerais e Métricas Adicionais")
reflexoes = st.text_area("Forneça comentários ou insights adicionais sobre desafios, sucessos e lições aprendidas durante o período.")
impacto_total = st.text_area("Informe dados agregados ou métricas quantitativas adicionais (ex.: total de eventos, matrículas, beneficiários).")
recomendacoes = st.text_area("Liste suas recomendações para melhorar o planejamento e a execução das ações futuras.")

# -------------------------------
# Botão de Envio
# -------------------------------
if st.button("Enviar"):
    dados = {
        "Programa": {
            "Sigla": sigla,
            "Nome Completo": nome_completo,
            "Instituição": instituicao,
            "Modalidade": modalidade,
            "Número médio de docentes (DP)": dp
        },
        "Cursos de Especialização": {
            "Ofertou curso?": oferta_especializacao,
            "Cursos": cursos_especializacao if oferta_especializacao else "",
            "Descrição": descricao_especializacao if oferta_especializacao else "",
            "Alunos": alunos_especializacao if oferta_especializacao else "",
            "Duração": duracao_especializacao if oferta_especializacao else "",
            "Docentes Envolvidos": docentes_especializacao if oferta_especializacao else "",
            "Impacto": impacto_especializacao if oferta_especializacao else ""
        },
        "Cursos de Extensão": {
            "Ministrou cursos/atividades?": oferta_extensao,
            "Cursos/Atividades": cursos_extensao if oferta_extensao else "",
            "Participantes": participantes_extensao if oferta_extensao else "",
            "Duração": duracao_extensao if oferta_extensao else "",
            "Docentes Envolvidos": docentes_extensao if oferta_extensao else "",
            "Impacto": impacto_extensao if oferta_extensao else ""
        },
        "Consultorias": {
            "Atuou em consultorias?": oferta_consultoria,
            "Detalhes": detalhes_consultoria if oferta_consultoria else "",
            "Duração": duracao_consultoria if oferta_consultoria else "",
            "Docentes Envolvidos": docentes_consultoria if oferta_consultoria else "",
            "Impacto": impacto_consultoria if oferta_consultoria else ""
        },
        "Redes de Pesquisa": {
            "Participou ou coordenou?": oferta_redes,
            "Redes": redes if oferta_redes else "",
            "Papel": papel_redes if oferta_redes else "",
            "Duração": duracao_redes if oferta_redes else "",
            "Resultados": resultados_redes if oferta_redes else ""
        },
        "Eventos Científicos": {
            "Organizou ou participou?": oferta_eventos,
            "Eventos": eventos if oferta_eventos else "",
            "Público": publico_eventos if oferta_eventos else "",
            "Duração": duracao_eventos if oferta_eventos else "",
            "Impacto": impacto_eventos if oferta_eventos else ""
        },
        "Intervenções Comunitárias": {
            "Implementou intervenções?": oferta_interv,
            "Intervenção": interv if oferta_interv else "",
            "Beneficiados": beneficiados if oferta_interv else "",
            "Duração": duracao_interv if oferta_interv else "",
            "Docentes Envolvidos": docentes_interv if oferta_interv else "",
            "Métricas": metricas_interv if oferta_interv else ""
        },
        "Atividades em Escolas": {
            "Realizou atividades?": oferta_escolas,
            "Atividade": atividade_escolas if oferta_escolas else "",
            "Número de Sessões": sessoes_escolas if oferta_escolas else "",
            "Participantes": participantes_escolas if oferta_escolas else "",
            "Duração": duracao_escolas if oferta_escolas else "",
            "Avaliação": avaliacao_escolas if oferta_escolas else ""
        },
        "Reflexões e Métricas Adicionais": {
            "Reflexões": reflexoes,
            "Impacto Total": impacto_total,
            "Recomendações": recomendacoes
        },
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add data to existing data
    existing_data.append(dados)
    
    # Show a spinner while saving data
    with st.spinner("Salvando dados..."):
        # Save to JSON file (local or GitHub)
        save_data(existing_data)
        
        # Add a small delay for better UX
        time.sleep(1)
    
    st.session_state.form_submitted = True
    st.success("Dados coletados e salvos com sucesso!")
    st.write(dados)

# Add a section to view submitted data
st.header("Submissões Anteriores")
if existing_data:
    if st.checkbox("Mostrar dados anteriores"):
        for i, submission in enumerate(existing_data):
            with st.expander(f"Submissão {i+1} - {submission.get('Timestamp', 'Data não disponível')}"):
                st.json(submission)
else:
    st.info("Nenhuma submissão encontrada.")