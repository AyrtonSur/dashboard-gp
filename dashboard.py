import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(page_title="Dashboard PS - IN Junior",
                   page_icon="📊",
                   layout="wide")

# Título
st.title("📊 Dashboard - Processo Seletivo IN Junior")
st.markdown("---")


# Carregar dados
@st.cache_data
def load_data():
  df = pd.read_csv("Cópia de Dados PS - Report.csv")
  return df


df = load_data()

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")

# Filtro de Fase
fases = ["Todas"] + sorted(df["Fase atual"].unique().tolist())
fase_selecionada = st.sidebar.multiselect("Fase Atual",
                                          options=fases,
                                          default=["Todas"])

# Filtro de Curso
cursos = ["Todos"] + sorted(df["Curso"].unique().tolist())
curso_selecionado = st.sidebar.multiselect("Curso",
                                           options=cursos,
                                           default=["Todos"])

# Filtro de Período
periodos = ["Todos"] + sorted(df["Qual o seu período?"].unique().tolist())
periodo_selecionado = st.sidebar.multiselect("Período",
                                             options=periodos,
                                             default=["Todos"])

# Filtro de Raça/Cor
racas = ["Todas"] + sorted(
    df["Como você se autodeclara em relação à sua cor ou raça?  "].unique(
    ).tolist())
raca_selecionada = st.sidebar.multiselect("Raça/Cor",
                                          options=racas,
                                          default=["Todas"])

# Aplicar filtros
df_filtrado = df.copy()

if "Todas" not in fase_selecionada and len(fase_selecionada) > 0:
  df_filtrado = df_filtrado[df_filtrado["Fase atual"].isin(fase_selecionada)]

if "Todos" not in curso_selecionado and len(curso_selecionado) > 0:
  df_filtrado = df_filtrado[df_filtrado["Curso"].isin(curso_selecionado)]

if "Todos" not in periodo_selecionado and len(periodo_selecionado) > 0:
  df_filtrado = df_filtrado[df_filtrado["Qual o seu período?"].isin(
      periodo_selecionado)]

if "Todas" not in raca_selecionada and len(raca_selecionada) > 0:
  df_filtrado = df_filtrado[
      df_filtrado["Como você se autodeclara em relação à sua cor ou raça?  "].
      isin(raca_selecionada)]

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric("Total de Candidatos", len(df_filtrado))

with col2:
  entrevistas = len(df_filtrado[df_filtrado["Fase atual"] == "Entrevista"])
  st.metric("Chegaram à Entrevista", entrevistas)

with col3:
  taxa_entrevista = ((entrevistas / len(df_filtrado) *
                      100) if len(df_filtrado) > 0 else 0)
  st.metric("Taxa de Entrevista", f"{taxa_entrevista:.1f}%")

with col4:
  lgbtq = len(df_filtrado[
      df_filtrado["Você se identifica como parte da comunidade LGBTQIAPN+?  "]
      == "Sim"])
  st.metric("Candidatos LGBTQIAPN+", lgbtq)

st.markdown("---")

# Abas para organizar as visualizações
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Visão Geral",
    "👥 Diversidade",
    "🎓 Acadêmico",
    "📢 Divulgação",
    "📋 Dados Detalhados",
])

# TAB 1: VISÃO GERAL
with tab1:
  # Funil do Processo Seletivo - Destaque principal
  st.subheader("Funil do Processo Seletivo")

  # Calcular as etapas do funil na ordem correta do processo
  total_candidatos = len(df_filtrado)

  # Fase 1: Responderam (excluindo eliminados por falta de resposta)
  responderam = len(df_filtrado[~df_filtrado["Fase atual"].str.
                                contains("Falta de Resposta", na=False)])

  # Fase 2: Passaram Fit Cultural (excluindo eliminados do fit cultural)
  passaram_fit_cultural = len(
      df_filtrado[~df_filtrado["Fase atual"].str.contains(
          "Falta de Resposta|Fit Cultural", na=False, regex=True)])

  # Fase 3: Compareceram à Dinâmica (excluindo falta na dinâmica)
  compareceram_dinamica = len(
      df_filtrado[~df_filtrado["Fase atual"].str.
                  contains("Falta de Resposta|Fit Cultural|Falta na Dinâmica",
                           na=False,
                           regex=True)])

  # Fase 4: Aprovados na Dinâmica (excluindo eliminados da dinâmica)
  aprovados_dinamica = len(df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica|Eliminados da Dinâmica",
      na=False,
      regex=True,
  )])

  # Fase 5: Entrevista (fase final)
  entrevista = len(df_filtrado[df_filtrado["Fase atual"] == "Entrevista"])

  # Criar o gráfico de funil
  fig1 = go.Figure(
      go.Funnel(
          y=[
              "Inscritos",
              "Responderam",
              "Aprovados<br>Fit Cultural",
              "Compareceram<br>Dinâmica",
              "Aprovados<br>Dinâmica",
              "Entrevista",
          ],
          x=[
              total_candidatos,
              responderam,
              passaram_fit_cultural,
              compareceram_dinamica,
              aprovados_dinamica,
              entrevista,
          ],
          textposition="inside",
          textinfo="value+percent initial",
          marker=dict(
              color=[
                  "#3498DB",
                  "#5DADE2",
                  "#85C1E9",
                  "#7DCEA0",
                  "#52BE80",
                  "#2ECC71",
              ],
              line=dict(width=2, color="white"),
          ),
          connector=dict(line=dict(color="lightgray", width=2)),
      ))

  fig1.update_layout(title="Funil de Conversão do Processo Seletivo",
                     height=500,
                     showlegend=False)
  st.plotly_chart(fig1, use_container_width=True)

  # Distribuição por Curso
  st.markdown("---")
  st.subheader("Distribuição por Curso")
  curso_counts = df_filtrado["Curso"].value_counts()
  fig2 = px.bar(
      x=curso_counts.values,
      y=curso_counts.index,
      orientation="h",
      title="Candidatos por Curso",
      labels={
          "x": "Quantidade",
          "y": "Curso"
      },
  )
  fig2.update_layout(showlegend=False)
  fig2.update_xaxes(showgrid=False)
  fig2.update_yaxes(showgrid=False)
  st.plotly_chart(fig2, use_container_width=True)

  # Detalhamento das fases
  st.markdown("---")
  st.subheader("Detalhamento por Fase")

  col3, col4 = st.columns([2, 1])

  with col3:
    # Ordem correta das fases do processo
    ordem_fases = [
        "Eliminados Falta de Resposta",
        "Eliminados do Fit Cultural e Vídeo de Apresentação",
        "Falta na Dinâmica",
        "Eliminados da Dinâmica",
        "Entrevista",
    ]

    fase_counts = df_filtrado["Fase atual"].value_counts()

    # Reordenar conforme o processo
    fase_counts_ordenado = pd.Series({
        fase: fase_counts.get(fase, 0)
        for fase in ordem_fases if fase in fase_counts.index
    })

    # Cores personalizadas para cada tipo de fase
    cores_fase = {
        "Eliminados Falta de Resposta": "#E74C3C",  # Vermelho
        "Eliminados do Fit Cultural e Vídeo de Apresentação":
        "#C0392B",  # Vermelho escuro
        "Falta na Dinâmica": "#F39C12",  # Amarelo
        "Eliminados da Dinâmica": "#E67E22",  # Laranja
        "Entrevista": "#2ECC71",  # Verde para sucesso
    }

    cores = [
        cores_fase.get(fase, "#95A5A6") for fase in fase_counts_ordenado.index
    ]

    fig_detalhe = px.bar(
        y=fase_counts_ordenado.index,
        x=fase_counts_ordenado.values,
        orientation="h",
        title="Candidatos por Fase Detalhado",
        labels={
            "x": "Quantidade de Candidatos",
            "y": "Fase"
        },
        text=fase_counts_ordenado.values,
    )
    fig_detalhe.update_traces(marker_color=cores, textposition="outside")
    fig_detalhe.update_layout(showlegend=False, height=350)
    fig_detalhe.update_xaxes(showgrid=False)
    fig_detalhe.update_yaxes(showgrid=False)
    st.plotly_chart(fig_detalhe, use_container_width=True)

  with col4:
    st.markdown("### Estatísticas")
    total = len(df_filtrado)

    st.metric("Taxa de Resposta", f"{(responderam/total*100):.1f}%")
    st.metric(
        "Taxa Fit Cultural",
        f"{(passaram_fit_cultural/responderam*100 if responderam > 0 else 0):.1f}%",
    )
    st.metric(
        "Taxa Comparecimento",
        f"{(compareceram_dinamica/passaram_fit_cultural*100 if passaram_fit_cultural > 0 else 0):.1f}%",
    )
    st.metric(
        "Taxa Aprovação Dinâmica",
        f"{(aprovados_dinamica/compareceram_dinamica*100 if compareceram_dinamica > 0 else 0):.1f}%",
    )
    st.metric("Taxa Final (Entrevista)", f"{(entrevista/total*100):.1f}%")

  st.markdown("---")
  st.subheader("Distribuição de Cursos ao Longo do Funil")
  st.info(
      "Mostra como cada curso se comporta em cada etapa do processo seletivo")

  # Criar datasets para cada fase do funil por curso
  fases_curso_analise = []

  # Fase 1: Todos inscritos
  df_inscritos_curso = df_filtrado.copy()
  df_inscritos_curso["Fase_Funil"] = "1. Inscritos"
  fases_curso_analise.append(df_inscritos_curso)

  # Fase 2: Responderam
  df_responderam_curso = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta", na=False)].copy()
  df_responderam_curso["Fase_Funil"] = "2. Responderam"
  fases_curso_analise.append(df_responderam_curso)

  # Fase 3: Aprovados Fit Cultural
  df_fit_curso = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural", na=False, regex=True)].copy()
  df_fit_curso["Fase_Funil"] = "3. Aprovados Fit"
  fases_curso_analise.append(df_fit_curso)

  # Fase 4: Compareceram Dinâmica
  df_compareceram_curso = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica", na=False, regex=True
  )].copy()
  df_compareceram_curso["Fase_Funil"] = "4. Compareceram"
  fases_curso_analise.append(df_compareceram_curso)

  # Fase 5: Aprovados Dinâmica
  df_aprovados_curso = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica|Eliminados da Dinâmica",
      na=False,
      regex=True,
  )].copy()
  df_aprovados_curso["Fase_Funil"] = "5. Aprovados Din."
  fases_curso_analise.append(df_aprovados_curso)

  # Fase 6: Entrevista
  df_entrevista_curso = df_filtrado[df_filtrado["Fase atual"] ==
                                    "Entrevista"].copy()
  df_entrevista_curso["Fase_Funil"] = "6. Entrevista"
  fases_curso_analise.append(df_entrevista_curso)

  # Combinar todos os dados
  df_funil_curso = pd.concat(fases_curso_analise, ignore_index=True)

  col_curso1, col_curso2 = st.columns(2)

  with col_curso1:
    fase_curso_abs = pd.crosstab(df_funil_curso["Fase_Funil"],
                                 df_funil_curso["Curso"]).reset_index()

    fig3 = px.bar(
        fase_curso_abs,
        x="Fase_Funil",
        y=fase_curso_abs.columns[1:],
        barmode="stack",
        title="Distribuição de Cursos por Fase (Valores Absolutos)",
        labels={
            "value": "Quantidade",
            "variable": "Curso",
            "Fase_Funil": "Fase"
        },
    )
    fig3.update_xaxes(showgrid=False, tickangle=-45)
    fig3.update_yaxes(showgrid=False)
    st.plotly_chart(fig3, use_container_width=True)

  with col_curso2:
    fase_curso_pct = pd.crosstab(df_funil_curso["Fase_Funil"],
                                 df_funil_curso["Curso"],
                                 normalize="index").reset_index()

    fig3b = px.bar(
        fase_curso_pct,
        x="Fase_Funil",
        y=fase_curso_pct.columns[1:],
        barmode="stack",
        title="Distribuição de Cursos por Fase (Percentual)",
        labels={
            "value": "Proporção",
            "variable": "Curso",
            "Fase_Funil": "Fase"
        },
    )
    fig3b.update_xaxes(showgrid=False, tickangle=-45)
    fig3b.update_yaxes(showgrid=False)
    fig3b.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig3b, use_container_width=True)

# TAB 2: DIVERSIDADE
with tab2:
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Distribuição por Raça/Cor")
    raca_counts = (
        df_filtrado["Como você se autodeclara em relação à sua cor ou raça?  "]
        .value_counts().sort_values(ascending=True))

    total = raca_counts.sum()
    percentuais = (raca_counts / total * 100).round(1)

    fig4 = px.bar(
        y=raca_counts.index,
        x=raca_counts.values,
        orientation="h",
        title="Autodeclaração de Raça/Cor",
        labels={
            "x": "Quantidade",
            "y": "Raça/Cor"
        },
        text=[
            f"{val} ({pct}%)"
            for val, pct in zip(raca_counts.values, percentuais)
        ],
        color=raca_counts.values,
        color_continuous_scale="Teal",
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(showlegend=False, height=350)
    fig4.update_xaxes(showgrid=False)
    fig4.update_yaxes(showgrid=False)
    st.plotly_chart(fig4, use_container_width=True)

  with col2:
    st.subheader("Identidade de Gênero")
    pronome_counts = df_filtrado[
        "Quais pronomes você utiliza?  "].value_counts()
    fig5 = px.bar(
        x=pronome_counts.index,
        y=pronome_counts.values,
        title="Pronomes Utilizados",
        labels={
            "x": "Pronomes",
            "y": "Quantidade"
        },
        color=pronome_counts.values,
        color_continuous_scale="Blues",
    )
    fig5.update_layout(height=350)
    fig5.update_xaxes(showgrid=False)
    fig5.update_yaxes(showgrid=False)
    st.plotly_chart(fig5, use_container_width=True)

  col3, col4 = st.columns(2)

  with col3:
    st.subheader("Comunidade LGBTQIAPN+")
    lgbtq_counts = df_filtrado[
        "Você se identifica como parte da comunidade LGBTQIAPN+?  "].value_counts(
        )

    cores_lgbtq = {
        "Sim": "#FF6B9D",
        "Não": "#4ECDC4",
        "Prefiro não responder": "#95E1D3",
    }
    cores = [cores_lgbtq.get(cat, "#BDC3C7") for cat in lgbtq_counts.index]

    total = lgbtq_counts.sum()
    percentuais = (lgbtq_counts / total * 100).round(1)

    fig6 = px.bar(
        x=lgbtq_counts.index,
        y=lgbtq_counts.values,
        title="Identificação LGBTQIAPN+",
        labels={
            "x": "Resposta",
            "y": "Quantidade"
        },
        text=[
            f"{val}<br>({pct}%)"
            for val, pct in zip(lgbtq_counts.values, percentuais)
        ],
    )
    fig6.update_traces(marker_color=cores, textposition="outside")
    fig6.update_layout(showlegend=False, height=350)
    fig6.update_xaxes(showgrid=False)
    fig6.update_yaxes(showgrid=False)
    st.plotly_chart(fig6, use_container_width=True)

  with col4:
    st.subheader("Acessibilidade")
    def_counts = df_filtrado[
        "Você possui alguma deficiência, condição ou necessidade específica que a IN Junior deveria considerar para garantir acessibilidade e inclusão?  "].value_counts(
        )
    fig7 = px.bar(
        x=def_counts.index,
        y=def_counts.values,
        title="Necessidades de Acessibilidade",
        labels={
            "x": "Resposta",
            "y": "Quantidade"
        },
        color=def_counts.values,
        color_continuous_scale="Oranges",
    )
    fig7.update_layout(height=350)
    fig7.update_xaxes(showgrid=False)
    fig7.update_yaxes(showgrid=False)
    st.plotly_chart(fig7, use_container_width=True)

  # Análise cruzada: Diversidade dos Aprovados
  st.markdown("---")
  st.subheader("Perfil dos Candidatos Aprovados (Entrevista)")

  df_entrevista = df_filtrado[df_filtrado["Fase atual"] == "Entrevista"]

  if len(df_entrevista) > 0:
    col5, col6 = st.columns(2)

    with col5:
      raca_entrevista = df_entrevista[
          "Como você se autodeclara em relação à sua cor ou raça?  "].value_counts(
          )
      fig8 = px.bar(
          x=raca_entrevista.values,
          y=raca_entrevista.index,
          orientation="h",
          title="Distribuição Racial - Aprovados",
          labels={
              "x": "Quantidade",
              "y": "Raça/Cor"
          },
          text=raca_entrevista.values,
          color=raca_entrevista.values,
          color_continuous_scale="Greens",
      )
      fig8.update_traces(textposition="outside")
      fig8.update_xaxes(showgrid=False)
      fig8.update_yaxes(showgrid=False)
      st.plotly_chart(fig8, use_container_width=True)

    with col6:
      # Análise adicional dos aprovados
      lgbtq_entrevista = df_entrevista[
          "Você se identifica como parte da comunidade LGBTQIAPN+?  "].value_counts(
          )
      pronome_entrevista = df_entrevista[
          "Quais pronomes você utiliza?  "].value_counts()

      fig8b = px.bar(
          x=pronome_entrevista.values,
          y=pronome_entrevista.index,
          orientation="h",
          title="Pronomes - Aprovados",
          labels={
              "x": "Quantidade",
              "y": "Pronomes"
          },
          text=pronome_entrevista.values,
          color=pronome_entrevista.values,
          color_continuous_scale="Greens",
      )
      fig8b.update_traces(textposition="outside")
      fig8b.update_xaxes(showgrid=False)
      fig8b.update_yaxes(showgrid=False)
      st.plotly_chart(fig8b, use_container_width=True)
  else:
    st.info("Nenhum candidato aprovado com os filtros selecionados.")

  # Análise dos Eliminados
  st.markdown("---")
  st.subheader("Perfil dos Candidatos Eliminados")

  df_eliminados = df_filtrado[df_filtrado["Fase atual"] != "Entrevista"]

  if len(df_eliminados) > 0:
    col7, col8 = st.columns(2)

    with col7:
      raca_eliminados = df_eliminados[
          "Como você se autodeclara em relação à sua cor ou raça?  "].value_counts(
          )
      fig9 = px.bar(
          x=raca_eliminados.values,
          y=raca_eliminados.index,
          orientation="h",
          title="Distribuição Racial - Eliminados",
          labels={
              "x": "Quantidade",
              "y": "Raça/Cor"
          },
          text=raca_eliminados.values,
          color=raca_eliminados.values,
          color_continuous_scale="Reds",
      )
      fig9.update_traces(textposition="outside")
      fig9.update_xaxes(showgrid=False)
      fig9.update_yaxes(showgrid=False)
      st.plotly_chart(fig9, use_container_width=True)

    with col8:
      pronome_eliminados = df_eliminados[
          "Quais pronomes você utiliza?  "].value_counts()
      fig9b = px.bar(
          x=pronome_eliminados.values,
          y=pronome_eliminados.index,
          orientation="h",
          title="Pronomes - Eliminados",
          labels={
              "x": "Quantidade",
              "y": "Pronomes"
          },
          text=pronome_eliminados.values,
          color=pronome_eliminados.values,
          color_continuous_scale="Reds",
      )
      fig9b.update_traces(textposition="outside")
      fig9b.update_xaxes(showgrid=False)
      fig9b.update_yaxes(showgrid=False)
      st.plotly_chart(fig9b, use_container_width=True)

  else:
    st.info("Nenhum candidato eliminado com os filtros selecionados.")

  # Diversidade por Fase do Processo (cumulativo - quem chegou até cada fase)
  st.markdown("---")
  st.subheader("Diversidade por Fase do Processo")
  st.info(
      "Mostra a composição de todos os candidatos que chegaram até cada etapa do funil"
  )

  # Criar datasets para cada fase do funil
  fases_analise = []

  # Fase 1: Todos inscritos
  df_inscritos = df_filtrado.copy()
  df_inscritos["Fase_Funil"] = "1. Inscritos"
  fases_analise.append(df_inscritos)

  # Fase 2: Responderam (excluindo falta de resposta)
  df_responderam = df_filtrado[~df_filtrado["Fase atual"].str.
                               contains("Falta de Resposta", na=False)].copy()
  df_responderam["Fase_Funil"] = "2. Responderam"
  fases_analise.append(df_responderam)

  # Fase 3: Aprovados Fit Cultural
  df_fit = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural", na=False, regex=True)].copy()
  df_fit["Fase_Funil"] = "3. Aprovados Fit Cultural"
  fases_analise.append(df_fit)

  # Fase 4: Compareceram Dinâmica
  df_compareceram = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica", na=False, regex=True
  )].copy()
  df_compareceram["Fase_Funil"] = "4. Compareceram Dinâmica"
  fases_analise.append(df_compareceram)

  # Fase 5: Aprovados Dinâmica
  df_aprovados = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica|Eliminados da Dinâmica",
      na=False,
      regex=True,
  )].copy()
  df_aprovados["Fase_Funil"] = "5. Aprovados Dinâmica"
  fases_analise.append(df_aprovados)

  # Fase 6: Entrevista
  df_entrevista_funil = df_filtrado[df_filtrado["Fase atual"] ==
                                    "Entrevista"].copy()
  df_entrevista_funil["Fase_Funil"] = "6. Entrevista"
  fases_analise.append(df_entrevista_funil)

  # Combinar todos os dados
  df_funil_completo = pd.concat(fases_analise, ignore_index=True)

  # Análise racial por fase
  col9, col10 = st.columns(2)

  with col9:
    fase_raca_processo = pd.crosstab(
        df_funil_completo["Fase_Funil"],
        df_funil_completo[
            "Como você se autodeclara em relação à sua cor ou raça?  "],
    ).reset_index()

    fig10 = px.bar(
        fase_raca_processo,
        x="Fase_Funil",
        y=fase_raca_processo.columns[1:],
        barmode="stack",
        title="Distribuição Racial por Fase (Valores Absolutos)",
        labels={
            "value": "Quantidade",
            "variable": "Raça/Cor",
            "Fase_Funil": "Fase",
        },
    )
    fig10.update_xaxes(showgrid=False, tickangle=-45)
    fig10.update_yaxes(showgrid=False)
    st.plotly_chart(fig10, use_container_width=True)

  with col10:
    # Percentual por fase
    fase_raca_pct = pd.crosstab(
        df_funil_completo["Fase_Funil"],
        df_funil_completo[
            "Como você se autodeclara em relação à sua cor ou raça?  "],
        normalize="index",
    ).reset_index()

    fig10b = px.bar(
        fase_raca_pct,
        x="Fase_Funil",
        y=fase_raca_pct.columns[1:],
        barmode="stack",
        title="Distribuição Racial por Fase (Percentual)",
        labels={
            "value": "Proporção",
            "variable": "Raça/Cor",
            "Fase_Funil": "Fase"
        },
    )
    fig10b.update_xaxes(showgrid=False, tickangle=-45)
    fig10b.update_yaxes(showgrid=False)
    fig10b.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig10b, use_container_width=True)

  # Análise LGBTQIAPN+ por fase
  st.markdown("---")
  col11, col12 = st.columns(2)

  with col11:
    fase_lgbtq_processo = pd.crosstab(
        df_funil_completo["Fase_Funil"],
        df_funil_completo[
            "Você se identifica como parte da comunidade LGBTQIAPN+?  "],
    ).reset_index()

    fig11_lgbtq = px.bar(
        fase_lgbtq_processo,
        x="Fase_Funil",
        y=fase_lgbtq_processo.columns[1:],
        barmode="stack",
        title="Distribuição LGBTQIAPN+ por Fase (Valores Absolutos)",
        labels={
            "value": "Quantidade",
            "variable": "LGBTQIAPN+",
            "Fase_Funil": "Fase",
        },
        color_discrete_sequence=["#FF6B9D", "#4ECDC4", "#95E1D3"],
    )
    fig11_lgbtq.update_xaxes(showgrid=False, tickangle=-45)
    fig11_lgbtq.update_yaxes(showgrid=False)
    st.plotly_chart(fig11_lgbtq, use_container_width=True)

  with col12:
    fase_lgbtq_pct = pd.crosstab(
        df_funil_completo["Fase_Funil"],
        df_funil_completo[
            "Você se identifica como parte da comunidade LGBTQIAPN+?  "],
        normalize="index",
    ).reset_index()

    fig11b_lgbtq = px.bar(
        fase_lgbtq_pct,
        x="Fase_Funil",
        y=fase_lgbtq_pct.columns[1:],
        barmode="stack",
        title="Distribuição LGBTQIAPN+ por Fase (Percentual)",
        labels={
            "value": "Proporção",
            "variable": "LGBTQIAPN+",
            "Fase_Funil": "Fase",
        },
        color_discrete_sequence=["#FF6B9D", "#4ECDC4", "#95E1D3"],
    )
    fig11b_lgbtq.update_xaxes(showgrid=False, tickangle=-45)
    fig11b_lgbtq.update_yaxes(showgrid=False)
    fig11b_lgbtq.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig11b_lgbtq, use_container_width=True)

  # Análise de Identidade de Gênero (Pronomes) por fase
  st.markdown("---")
  col13, col14 = st.columns(2)

  with col13:
    fase_pronome_processo = pd.crosstab(
        df_funil_completo["Fase_Funil"],
        df_funil_completo["Quais pronomes você utiliza?  "],
    ).reset_index()

    fig12_pronome = px.bar(
        fase_pronome_processo,
        x="Fase_Funil",
        y=fase_pronome_processo.columns[1:],
        barmode="stack",
        title=
        "Distribuição de Identidade de Gênero por Fase (Valores Absolutos)",
        labels={
            "value": "Quantidade",
            "variable": "Pronomes",
            "Fase_Funil": "Fase",
        },
    )
    fig12_pronome.update_xaxes(showgrid=False, tickangle=-45)
    fig12_pronome.update_yaxes(showgrid=False)
    st.plotly_chart(fig12_pronome, use_container_width=True)

  with col14:
    fase_pronome_pct = pd.crosstab(
        df_funil_completo["Fase_Funil"],
        df_funil_completo["Quais pronomes você utiliza?  "],
        normalize="index",
    ).reset_index()

    fig12b_pronome = px.bar(
        fase_pronome_pct,
        x="Fase_Funil",
        y=fase_pronome_pct.columns[1:],
        barmode="stack",
        title="Distribuição de Identidade de Gênero por Fase (Percentual)",
        labels={
            "value": "Proporção",
            "variable": "Pronomes",
            "Fase_Funil": "Fase"
        },
    )
    fig12b_pronome.update_xaxes(showgrid=False, tickangle=-45)
    fig12b_pronome.update_yaxes(showgrid=False)
    fig12b_pronome.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig12b_pronome, use_container_width=True)

# TAB 3: ACADÊMICO
with tab3:
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Distribuição por Período")
    periodo_counts = df_filtrado["Qual o seu período?"].value_counts(
    ).sort_index()
    fig11 = px.bar(
        x=periodo_counts.index,
        y=periodo_counts.values,
        title="Candidatos por Período",
        labels={
            "x": "Período",
            "y": "Quantidade"
        },
        color=periodo_counts.values,
        color_continuous_scale="Viridis",
    )
    fig11.update_xaxes(showgrid=False)
    fig11.update_yaxes(showgrid=False)
    st.plotly_chart(fig11, use_container_width=True)

  with col2:
    st.subheader("Taxa de Aprovação por Curso")
    aprovacao_curso = (df_filtrado.groupby("Curso")["Fase atual"].apply(
        lambda x: (x == "Entrevista").sum() / len(x) * 100
        if len(x) > 0 else 0).sort_values(ascending=False))
    fig12 = px.bar(
        x=aprovacao_curso.values,
        y=aprovacao_curso.index,
        orientation="h",
        title="Taxa de Aprovação para Entrevista (%)",
        labels={
            "x": "Taxa (%)",
            "y": "Curso"
        },
        color=aprovacao_curso.values,
        color_continuous_scale="RdYlGn",
    )
    fig12.update_xaxes(showgrid=False)
    fig12.update_yaxes(showgrid=False)
    st.plotly_chart(fig12, use_container_width=True)

  # Análise de Períodos ao longo do Funil
  st.markdown("---")
  st.subheader("Distribuição de Períodos ao Longo do Funil")
  st.info(
      "Mostra como a composição de períodos evolui em cada etapa do processo seletivo"
  )

  # Criar datasets para cada fase do funil (reutilizando a lógica)
  fases_periodo = []

  # Fase 1: Todos inscritos
  df_inscritos_p = df_filtrado.copy()
  df_inscritos_p["Fase_Funil"] = "1. Inscritos"
  fases_periodo.append(df_inscritos_p)

  # Fase 2: Responderam
  df_responderam_p = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta", na=False)].copy()
  df_responderam_p["Fase_Funil"] = "2. Responderam"
  fases_periodo.append(df_responderam_p)

  # Fase 3: Aprovados Fit Cultural
  df_fit_p = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural", na=False, regex=True)].copy()
  df_fit_p["Fase_Funil"] = "3. Aprovados Fit"
  fases_periodo.append(df_fit_p)

  # Fase 4: Compareceram Dinâmica
  df_compareceram_p = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica", na=False, regex=True
  )].copy()
  df_compareceram_p["Fase_Funil"] = "4. Compareceram"
  fases_periodo.append(df_compareceram_p)

  # Fase 5: Aprovados Dinâmica
  df_aprovados_p = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica|Eliminados da Dinâmica",
      na=False,
      regex=True,
  )].copy()
  df_aprovados_p["Fase_Funil"] = "5. Aprovados Din."
  fases_periodo.append(df_aprovados_p)

  # Fase 6: Entrevista
  df_entrevista_p = df_filtrado[df_filtrado["Fase atual"] ==
                                "Entrevista"].copy()
  df_entrevista_p["Fase_Funil"] = "6. Entrevista"
  fases_periodo.append(df_entrevista_p)

  # Combinar todos os dados
  df_funil_periodo = pd.concat(fases_periodo, ignore_index=True)

  col_p1, col_p2 = st.columns(2)

  with col_p1:
    fase_periodo_abs = pd.crosstab(
        df_funil_periodo["Fase_Funil"],
        df_funil_periodo["Qual o seu período?"]).reset_index()

    fig_periodo1 = px.bar(
        fase_periodo_abs,
        x="Fase_Funil",
        y=fase_periodo_abs.columns[1:],
        barmode="stack",
        title="Distribuição de Períodos por Fase (Valores Absolutos)",
        labels={
            "value": "Quantidade",
            "variable": "Período",
            "Fase_Funil": "Fase"
        },
    )
    fig_periodo1.update_xaxes(showgrid=False, tickangle=-45)
    fig_periodo1.update_yaxes(showgrid=False)
    st.plotly_chart(fig_periodo1, use_container_width=True)

  with col_p2:
    fase_periodo_pct = pd.crosstab(
        df_funil_periodo["Fase_Funil"],
        df_funil_periodo["Qual o seu período?"],
        normalize="index",
    ).reset_index()

    fig_periodo2 = px.bar(
        fase_periodo_pct,
        x="Fase_Funil",
        y=fase_periodo_pct.columns[1:],
        barmode="stack",
        title="Distribuição de Períodos por Fase (Percentual)",
        labels={
            "value": "Proporção",
            "variable": "Período",
            "Fase_Funil": "Fase"
        },
    )
    fig_periodo2.update_xaxes(showgrid=False, tickangle=-45)
    fig_periodo2.update_yaxes(showgrid=False)
    fig_periodo2.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig_periodo2, use_container_width=True)

# TAB 4: DIVULGAÇÃO
with tab4:
  st.subheader("Como os candidatos ficaram sabendo do PS?")

  divulgacao_counts = (
      df_filtrado["Como você ficou sabendo do processo seletivo?"].
      value_counts().sort_values(ascending=True))

  total = divulgacao_counts.sum()
  percentuais = (divulgacao_counts / total * 100).round(1)

  # Gráfico principal com percentuais
  fig14 = px.bar(
      y=divulgacao_counts.index,
      x=divulgacao_counts.values,
      orientation="h",
      title="Canais de Divulgação - Volume de Candidatos",
      labels={
          "x": "Número de Candidatos",
          "y": "Canal"
      },
      text=[
          f"{val} ({pct}%)"
          for val, pct in zip(divulgacao_counts.values, percentuais)
      ],
      color=divulgacao_counts.values,
      color_continuous_scale="Viridis",
  )
  fig14.update_traces(textposition="outside")
  fig14.update_layout(showlegend=False, height=400)
  fig14.update_xaxes(showgrid=False)
  fig14.update_yaxes(showgrid=False)
  st.plotly_chart(fig14, use_container_width=True)

  st.markdown("---")

  # Análise: Canais ao longo do Funil
  st.subheader("Distribuição dos Canais de Divulgação ao Longo do Funil")
  st.info(
      "Mostra como cada canal de divulgação se comporta em cada etapa do processo seletivo"
  )

  # Criar datasets para cada fase do funil
  fases_canal = []

  # Fase 1: Todos inscritos
  df_inscritos_c = df_filtrado.copy()
  df_inscritos_c["Fase_Funil"] = "1. Inscritos"
  fases_canal.append(df_inscritos_c)

  # Fase 2: Responderam
  df_responderam_c = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta", na=False)].copy()
  df_responderam_c["Fase_Funil"] = "2. Responderam"
  fases_canal.append(df_responderam_c)

  # Fase 3: Aprovados Fit Cultural
  df_fit_c = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural", na=False, regex=True)].copy()
  df_fit_c["Fase_Funil"] = "3. Aprovados Fit"
  fases_canal.append(df_fit_c)

  # Fase 4: Compareceram Dinâmica
  df_compareceram_c = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica", na=False, regex=True
  )].copy()
  df_compareceram_c["Fase_Funil"] = "4. Compareceram"
  fases_canal.append(df_compareceram_c)

  # Fase 5: Aprovados Dinâmica
  df_aprovados_c = df_filtrado[~df_filtrado["Fase atual"].str.contains(
      "Falta de Resposta|Fit Cultural|Falta na Dinâmica|Eliminados da Dinâmica",
      na=False,
      regex=True,
  )].copy()
  df_aprovados_c["Fase_Funil"] = "5. Aprovados Din."
  fases_canal.append(df_aprovados_c)

  # Fase 6: Entrevista
  df_entrevista_c = df_filtrado[df_filtrado["Fase atual"] ==
                                "Entrevista"].copy()
  df_entrevista_c["Fase_Funil"] = "6. Entrevista"
  fases_canal.append(df_entrevista_c)

  # Combinar todos os dados
  df_funil_canal = pd.concat(fases_canal, ignore_index=True)

  col_c1, col_c2 = st.columns(2)

  with col_c1:
    fase_canal_abs = pd.crosstab(
        df_funil_canal["Fase_Funil"],
        df_funil_canal["Como você ficou sabendo do processo seletivo?"],
    ).reset_index()

    fig15 = px.bar(
        fase_canal_abs,
        x="Fase_Funil",
        y=fase_canal_abs.columns[1:],
        barmode="stack",
        title="Distribuição de Canais por Fase (Valores Absolutos)",
        labels={
            "value": "Quantidade",
            "variable": "Canal",
            "Fase_Funil": "Fase"
        },
    )
    fig15.update_xaxes(showgrid=False, tickangle=-45)
    fig15.update_yaxes(showgrid=False)
    st.plotly_chart(fig15, use_container_width=True)

  with col_c2:
    fase_canal_pct = pd.crosstab(
        df_funil_canal["Fase_Funil"],
        df_funil_canal["Como você ficou sabendo do processo seletivo?"],
        normalize="index",
    ).reset_index()

    fig16 = px.bar(
        fase_canal_pct,
        x="Fase_Funil",
        y=fase_canal_pct.columns[1:],
        barmode="stack",
        title="Distribuição de Canais por Fase (Percentual)",
        labels={
            "value": "Proporção",
            "variable": "Canal",
            "Fase_Funil": "Fase"
        },
    )
    fig16.update_xaxes(showgrid=False, tickangle=-45)
    fig16.update_yaxes(showgrid=False)
    fig16.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig16, use_container_width=True)

  # Taxa de conversão por canal
  st.markdown("---")
  st.subheader("Taxa de Conversão Final por Canal")
  taxa_conversao = (
      df_filtrado.groupby("Como você ficou sabendo do processo seletivo?")
      ["Fase atual"].apply(lambda x: (x == "Entrevista").sum() / len(x) * 100
                           if len(x) > 0 else 0).sort_values(ascending=False))

  fig17 = px.bar(
      x=taxa_conversao.values,
      y=taxa_conversao.index,
      orientation="h",
      title="Taxa de Conversão Final para Entrevista (%)",
      labels={
          "x": "Taxa de Conversão (%)",
          "y": "Canal"
      },
      text=[f"{val:.1f}%" for val in taxa_conversao.values],
      color=taxa_conversao.values,
      color_continuous_scale="RdYlGn",
  )
  fig17.update_traces(textposition="outside")
  fig17.update_xaxes(showgrid=False)
  fig17.update_yaxes(showgrid=False)
  st.plotly_chart(fig17, use_container_width=True)

# TAB 5: DADOS DETALHADOS
with tab5:
  st.subheader("Tabela de Dados Filtrados")

  # Opções de colunas para exibir
  colunas_disponiveis = df_filtrado.columns.tolist()
  colunas_selecionadas = st.multiselect(
      "Selecione as colunas para exibir:",
      options=colunas_disponiveis,
      default=colunas_disponiveis[:5],
  )

  if colunas_selecionadas:
    st.dataframe(df_filtrado[colunas_selecionadas], use_container_width=True)
  else:
    st.dataframe(df_filtrado, use_container_width=True)

  # Estatísticas descritivas
  st.subheader("Estatísticas Resumidas")

  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric("Total de Registros", len(df_filtrado))
    st.metric("Cursos Diferentes", df_filtrado["Curso"].nunique())

  with col2:
    st.metric("Fases Diferentes", df_filtrado["Fase atual"].nunique())
    st.metric("Períodos Diferentes",
              df_filtrado["Qual o seu período?"].nunique())

  with col3:
    candidatos_deficiencia = len(df_filtrado[df_filtrado[
        "Você possui alguma deficiência, condição ou necessidade específica que a IN Junior deveria considerar para garantir acessibilidade e inclusão?  "]
                                             == "Sim"])
    st.metric("Com Deficiência/Necessidades", candidatos_deficiencia)
    pct_feminino = (len(df_filtrado[
        df_filtrado["Quais pronomes você utiliza?  "] == "Ela/Dela"]) /
                    len(df_filtrado) * 100 if len(df_filtrado) > 0 else 0)
    st.metric("% Feminino", f"{pct_feminino:.1f}%")

  # Download dos dados filtrados
  st.subheader("Exportar Dados")
  csv = df_filtrado.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Download CSV Filtrado",
      data=csv,
      file_name="dados_filtrados_ps.csv",
      mime="text/csv",
  )

# Footer
st.markdown("---")
st.markdown(
    "*Dashboard desenvolvido para análise do Processo Seletivo da IN Junior*")
