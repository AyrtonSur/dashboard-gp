# Dashboard - Processo Seletivo IN Junior 📊

Dashboard interativo desenvolvido com Streamlit para análise dinâmica dos dados do processo seletivo.

## 🚀 Funcionalidades

### Filtros Interativos
- **Fase Atual**: Filtre por fase do processo seletivo
- **Curso**: Visualize dados por curso específico
- **Período**: Analise por período acadêmico
- **Raça/Cor**: Filtre por autodeclaração racial

### Abas de Análise

#### 📈 Visão Geral
- Distribuição de candidatos por fase
- Candidatos por curso
- Análise cruzada: fase × curso

#### 👥 Diversidade
- Distribuição racial
- Identidade de gênero e pronomes
- Comunidade LGBTQIAPN+
- Necessidades de acessibilidade
- Análise de diversidade nas diferentes fases

#### 🎓 Acadêmico
- Distribuição por período
- Taxa de aprovação por curso
- Desempenho por período

#### 📢 Divulgação
- Canais de divulgação mais efetivos
- Taxa de conversão por canal
- Análise de efetividade para alcançar entrevistas

#### 📋 Dados Detalhados
- Tabela completa com filtros personalizados
- Estatísticas resumidas
- Export de dados filtrados em CSV

## 📦 Instalação

### 1. Criar ambiente virtual

```bash
python3 -m venv venv
```

### 2. Ativar o ambiente virtual

```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Executar o dashboard

**Opção A - Com script automatizado:**
```bash
chmod +x run.sh
./run.sh
```

**Opção B - Manualmente:**
```bash
source venv/bin/activate
streamlit run dashboard.py
```

O dashboard abrirá automaticamente no seu navegador em `http://localhost:8501`

### 5. Desativar o ambiente virtual (quando terminar)

```bash
deactivate
```

## 📊 Tecnologias Utilizadas

- **Streamlit**: Framework para criar dashboards interativos
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Gráficos interativos e responsivos

## 💡 Como Usar

1. Use os filtros na barra lateral esquerda para segmentar os dados
2. Navegue entre as abas para diferentes tipos de análise
3. Interaja com os gráficos (hover, zoom, download)
4. Exporte dados filtrados na aba "Dados Detalhados"

## 📈 Métricas Principais

O dashboard apresenta métricas principais no topo:
- Total de candidatos (filtrados)
- Candidatos que chegaram à entrevista
- Taxa de conversão para entrevista
- Candidatos LGBTQIAPN+

## 🎨 Visualizações Incluídas

- Gráficos de pizza (distribuição percentual)
- Gráficos de barras (comparações)
- Gráficos empilhados (análises cruzadas)
- Tabelas interativas (dados detalhados)

## 📝 Observações

- Todos os gráficos são interativos (zoom, pan, hover)
- Os filtros se aplicam a todas as visualizações
- Use Ctrl+F5 se precisar recarregar os dados
