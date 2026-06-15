import streamlit as st
from dados_per import PERGAMINHOS
from calculos import calcular_custo
from tabelas import DESTREZA, COMBATIVIDADE, OUTROS
import os
import re

st.set_page_config(layout="wide")
st.title("🧙 Calculadora de Pergaminhos")

def limpar_nome_pergaminho(nome):
    return re.sub(r'\s*LV\(\d+\)', '', nome)

def carregar_imagem_pergaminho(nome_pergaminho):
    pasta_imagens = "imagens/pergaminhos"
    
    if not os.path.exists(pasta_imagens):
        return None
    
    for arquivo in os.listdir(pasta_imagens):
        nome_arquivo = os.path.splitext(arquivo)[0]
        nome_normalizado = nome_pergaminho.replace(" ", "").lower()
        arquivo_normalizado = nome_arquivo.replace(" ", "").lower()
        
        if arquivo_normalizado == nome_normalizado:
            caminho = os.path.join(pasta_imagens, arquivo)
            return caminho
    
    return None

if "pergaminhos_selecionados" not in st.session_state:
    st.session_state.pergaminhos_selecionados = set()

if "calcular" not in st.session_state:
    st.session_state.calcular = False

categoria = st.selectbox(
    "Escolha a categoria",
    ["Destreza", "Combatividade", "Maestria"]
)

st.divider()
lista_pergaminhos = list(PERGAMINHOS.keys())

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("✓ Selecionar Todos", use_container_width=True):
        st.session_state.pergaminhos_selecionados = set(lista_pergaminhos)
        st.rerun()
    
    if st.button("✗ Desselecionar Todos", use_container_width=True):
        st.session_state.pergaminhos_selecionados = set()
        st.rerun()

st.divider()

cols = st.columns(5)
for idx, pergaminho in enumerate(lista_pergaminhos):
    with cols[idx % 5]:
        is_selected = pergaminho in st.session_state.pergaminhos_selecionados
        caminho_imagem = carregar_imagem_pergaminho(pergaminho)
        
        with st.container():
            if caminho_imagem:
                st.image(caminho_imagem, use_column_width=True)
            else:
                st.empty()
            
            nome_limpo = limpar_nome_pergaminho(pergaminho)
            st.markdown(f"<p style='text-align: center; font-weight: bold; margin: 8px 0;'>{nome_limpo}</p>", unsafe_allow_html=True)
            
            btn_color = "🟢" if is_selected else "⚪"
            
            if st.button(f"{btn_color}", key=f"btn_{pergaminho}", use_container_width=True):
                if is_selected:
                    st.session_state.pergaminhos_selecionados.discard(pergaminho)
                else:
                    st.session_state.pergaminhos_selecionados.add(pergaminho)
                st.rerun()

st.divider()

if st.session_state.pergaminhos_selecionados:
    st.success(f"✓ {len(st.session_state.pergaminhos_selecionados)} pergaminho(s) selecionado(s)")
    
    st.write("**Selecionados:**")
    
    cols = st.columns(4)
    
    for i, pergaminho in enumerate(st.session_state.pergaminhos_selecionados):
        col_idx = i % 4
        with cols[col_idx]:
            caminho_imagem = carregar_imagem_pergaminho(pergaminho)
            
            if caminho_imagem:
                st.image(caminho_imagem, use_column_width=True)
            
            nome_limpo = limpar_nome_pergaminho(pergaminho)
            st.markdown(f"<p style='text-align: center; font-weight: bold;'>{i + 1}. {nome_limpo}</p>", unsafe_allow_html=True)

st.divider()
st.header("📊 Calcular Custo")

tabelas_disponiveis = {
    "Destreza": DESTREZA,
    "Combatividade": COMBATIVIDADE,
    "Outros": OUTROS
}

tabela_selecionada = tabelas_disponiveis.get(categoria, DESTREZA)

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
        if st.button("🧮 Calcular Custo", use_container_width=True):
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
                resultado = calcular_custo(
                    tabela_selecionada,
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
                    "Ryos": resultado["ryos"]
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
                        caminho_imagem = carregar_imagem_pergaminho(pergaminho)
                        if caminho_imagem:
                            st.image(caminho_imagem, use_column_width=True)
                        st.write(f"**{item['Pergaminho']}**")
                    
                    with col2:
                        st.write("")
                        st.write(f"🔵 Segredo: {item['Segredo']}")
                    
                    with col3:
                        st.write("")
                        st.write(f"🔴 Soro: {item['Soro']}")
                    
                    with col4:
                        st.write("")
                        st.write(f"💰 Ryos: {item['Ryos']:,}")
                    
                    st.divider()
            
            st.divider()
            st.success("✅ TOTAL PARA TODOS OS PERGAMINHOS")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🔵 Segredo Total", total_geral_segredo)
            col2.metric("🔴 Soro Total", total_geral_soro)
            col3.metric("💰 Ryos Total", f"{total_geral_ryos:,}")
