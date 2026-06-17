import streamlit as st
from dados_per import PERGAMINHOS
from calculos import calcular_custo
from tabelas import DESTREZA, COMBATIVIDADE, PADRAO
import base64
import mimetypes
import os
import re
import unicodedata
from difflib import SequenceMatcher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
PASTA_PERGAMINHOS = os.path.join(ROOT_DIR, "imagens", "Pergaminhos")
PASTA_CATEGORIAS = os.path.join(ROOT_DIR, "imagens", "Categorias")
PASTA_RECURSOS = os.path.join(ROOT_DIR, "imagens", "Recursos")
IMAGEM_PRINCIPAL = os.path.join(PASTA_CATEGORIAS, "Categoria4k.png")

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 2rem; }
        .stTitle { margin-bottom: 0.2rem; }
        .subtitle { color: #8aa4d2; font-size: 1.02rem; margin-bottom: 1rem; }
        .card-box {
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 14px;
            padding: 0.6rem;
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
            height: 100%;
        }
        .stButton > button {
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.04);
            color: white;
        }
        .stButton > button:hover { background: rgba(138, 164, 210, 0.18); }
        .pill { color: #b7c7ef; font-size: 0.92rem; }
        .made-by {
            position: fixed;
            right: 12px;
            bottom: 8px;
            z-index: 9999;
            font-size: 0.78rem;
            color: rgba(255,255,255,0.72);
            opacity: 0.85;
            pointer-events: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def renderizar_imagem(caminho, largura=300):
    if not caminho or not os.path.exists(caminho):
        return

    with open(caminho, "rb") as arquivo:
        dados = base64.b64encode(arquivo.read()).decode("utf-8")

    tipo = mimetypes.guess_type(caminho)[0] or "image/png"
    st.markdown(
        f'<img src="data:{tipo};base64,{dados}" width="{largura}" style="display:block; margin:0 auto; border-radius:20px;" />',
        unsafe_allow_html=True,
    )


st.markdown("<div style='display:flex; justify-content:center; margin-bottom:0.2rem;'>", unsafe_allow_html=True)
if os.path.exists(IMAGEM_PRINCIPAL):
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    renderizar_imagem(IMAGEM_PRINCIPAL, 500)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>📜 Calculadora de Pergaminhos</h1>",
    unsafe_allow_html=True
    )
st.markdown("<div class='subtitle' style='text-align:center;'>Escolha os pergaminhos, informe os níveis e veja o custo em poucos cliques.</div>", unsafe_allow_html=True)


def limpar_nome_pergaminho(nome):
    return re.sub(r'\s*LV\(\d+\)', '', nome)


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    texto = re.sub(r'[^a-z0-9]', '', texto)
    return texto


def carregar_imagem_pergaminho(nome_pergaminho):
    nome_alvo = normalizar_texto(nome_pergaminho)
    pastas_imagens = [PASTA_PERGAMINHOS, PASTA_CATEGORIAS]

    melhor_caminho = None
    melhor_score = 0.0

    for pasta_imagens in pastas_imagens:
        if not os.path.exists(pasta_imagens):
            continue

        for arquivo in os.listdir(pasta_imagens):
            nome_arquivo = os.path.splitext(arquivo)[0]
            arquivo_normalizado = normalizar_texto(nome_arquivo)
            score = SequenceMatcher(None, nome_alvo, arquivo_normalizado).ratio()

            if score > melhor_score:
                melhor_score = score
                melhor_caminho = os.path.join(pasta_imagens, arquivo)

    if melhor_score >= 0.72:
        return melhor_caminho

    return None

if "pergaminhos_selecionados" not in st.session_state:
    st.session_state.pergaminhos_selecionados = set()

if "calcular" not in st.session_state:
    st.session_state.calcular = False
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.info("Passo 1: Selecione os pergaminhos.")
    st.info("Passo 2: Defina o nível atual e o desejado.")
    st.info("Passo 3: Calcule o custo.")
st.divider()
lista_pergaminhos = list(PERGAMINHOS.keys())

st.markdown("<div class='pill'>Seleção rápida</div>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Selecionar todos", width="stretch"):
        st.session_state.pergaminhos_selecionados = set(lista_pergaminhos)
        st.rerun()
    
    if st.button("Limpar seleção", width="stretch"):
        st.session_state.pergaminhos_selecionados = set()
        st.rerun()

st.divider()

cols = st.columns(5, gap="small")
for idx, pergaminho in enumerate(lista_pergaminhos):
    with cols[idx % 5]:
        is_selected = pergaminho in st.session_state.pergaminhos_selecionados
        caminho_imagem = carregar_imagem_pergaminho(pergaminho)
        
        with st.container():
            if caminho_imagem:
                renderizar_imagem(caminho_imagem, 110)
            else:
                st.empty()
            
            nome_limpo = limpar_nome_pergaminho(pergaminho)
            st.markdown(f"<p style='text-align: center; font-weight: 1000; margin: 10px 0 10px 0;'>{nome_limpo}</p>", unsafe_allow_html=True)
            
            btn_color = "🟢" if is_selected else "⚪"
            
            if st.button(f"{btn_color} {'Selecionado' if is_selected else 'Selecionar'}", key=f"btn_{pergaminho}", width="stretch"):
                if is_selected:
                    st.session_state.pergaminhos_selecionados.discard(pergaminho)
                else:
                    st.session_state.pergaminhos_selecionados.add(pergaminho)
                st.rerun()

st.divider()

if st.session_state.pergaminhos_selecionados:
    st.success(f"{len(st.session_state.pergaminhos_selecionados)} pergaminho(s) pronto(s) para calcular.")

    st.caption("Selecionados no momento:")
    
    cols = st.columns(4, gap="small")
    
    for i, pergaminho in enumerate(st.session_state.pergaminhos_selecionados):
        col_idx = i % 4
        with cols[col_idx]:
            caminho_imagem = carregar_imagem_pergaminho(pergaminho)
            
            if caminho_imagem:
                renderizar_imagem(caminho_imagem, 110)
            
            nome_limpo = limpar_nome_pergaminho(pergaminho)
            st.markdown(f"<p style='text-align: center; font-weight: bold;'>{i + 1}. {nome_limpo}</p>", unsafe_allow_html=True)

st.divider()
st.header("📊 Calcular custo")


def selecionar_tabela_pergaminho(nome_pergaminho):
    nome_limpo = limpar_nome_pergaminho(nome_pergaminho)

    if nome_limpo == "Destreza":
        return DESTREZA
    if nome_limpo == "Combatividade":
        return COMBATIVIDADE

    return PADRAO

col1, col2, col3 = st.columns(3)

with col1:
    nivel_atual = st.number_input(
        "Nível Atual",
        min_value=1,
        max_value=18,
        value=1
    )

with col2:
    nivel_desejado = st.number_input(
        "Nível Desejado",
        min_value=2,
        max_value=19,
        value=10
    )

with col3:
    st.write("")
    st.write("")
    if nivel_desejado <= nivel_atual:
        calcular_btn_disabled = True
    else:
        calcular_btn_disabled = False
        if st.button("🧮 Calcular Custo", width="stretch"):
            st.session_state.calcular = True

if st.session_state.pergaminhos_selecionados and st.session_state.get("calcular", False):
    if not calcular_btn_disabled:
        st.divider()
        st.subheader("📈 Resultado do Cálculo")
        
        total_geral_segredo = 0
        total_geral_soro = 0
        total_geral_ryos = 0
        
        resultados = []
        
        for pergaminho in st.session_state.pergaminhos_selecionados:
            try:
                tabela_pergaminho = selecionar_tabela_pergaminho(pergaminho)
                resultado = calcular_custo(
                    tabela_pergaminho,
                    nivel_atual,
                    nivel_desejado,
                    1
                )
                
                total_geral_segredo += resultado["segredo"]
                total_geral_soro += resultado["soro"]
                total_geral_ryos += resultado["ryos"]
                
                nome_limpo = limpar_nome_pergaminho(pergaminho)
                resultados.append({
                    "Pergaminho": nome_limpo,
                    "Segredo": resultado["segredo"],
                    "Soro": resultado["soro"],
                    "Ryos": resultado["ryos"],
                })
            except KeyError:
                pass
        
        if resultados:
            st.write("**Custo por Pergaminho:**")
            st.divider()
            
            for pergaminho in st.session_state.pergaminhos_selecionados:
                item = next((r for r in resultados if r['Pergaminho'] == limpar_nome_pergaminho(pergaminho)), None)
                if item:
                    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
                    
                    with col1:
                        st.markdown("<div style='display:flex; flex-direction:column; align-items:center; text-align:center; gap:6px;'>", unsafe_allow_html=True)
                        caminho_imagem = carregar_imagem_pergaminho(pergaminho)
                        if caminho_imagem:
                            renderizar_imagem(caminho_imagem, 140)
                        st.markdown(f"<strong>{item['Pergaminho']}</strong>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div style='display:flex; flex-direction:column; align-items:center; text-align:center; gap:4px;'>", unsafe_allow_html=True)
                        if os.path.exists(os.path.join(PASTA_RECURSOS, "PergaminhoSecreto4k.png")):
                            renderizar_imagem(os.path.join(PASTA_RECURSOS, "PergaminhoSecreto4k.png"), 78)
                        st.markdown(f"<span>Pergaminho Secreto: {item['Segredo']}</span>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("<div style='display:flex; flex-direction:column; align-items:center; text-align:center; gap:4px;'>", unsafe_allow_html=True)
                        if os.path.exists(os.path.join(PASTA_RECURSOS, "SorodaVerdade4k.png")):
                            renderizar_imagem(os.path.join(PASTA_RECURSOS, "SorodaVerdade4k.png"), 78)
                        st.markdown(f"<span>Soro: {item['Soro']}</span>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col4:
                        st.write("")
                        st.write(f"💰 Ryos: {item['Ryos']:,}")
                    
                    st.divider()
            
            st.divider()
            st.success("✅ TOTAL PARA TODOS OS PERGAMINHOS")

            cols = st.columns(3)
            with cols[0]:
                if os.path.exists(os.path.join(PASTA_RECURSOS, "PergaminhoSecreto4k.png")):
                    renderizar_imagem(os.path.join(PASTA_RECURSOS, "PergaminhoSecreto4k.png"), 90)
                st.metric("Pergaminho Total", total_geral_segredo)
            with cols[1]:
                if os.path.exists(os.path.join(PASTA_RECURSOS, "SorodaVerdade4k.png")):
                    renderizar_imagem(os.path.join(PASTA_RECURSOS, "SorodaVerdade4k.png"), 90)
                st.metric("Soro Total", total_geral_soro)
            with cols[2]:
                st.metric("💰 Ryos Total", f"{total_geral_ryos:,}")

            pacotes_fc = total_geral_segredo // 9

            st.metric("📦 Pacotes de Força Necessários", pacotes_fc)

st.markdown("<div class='made-by'>made by xSouza_Sad</div>", unsafe_allow_html=True)
