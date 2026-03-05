#!/bin/bash

# Script para executar o dashboard com o ambiente virtual

# Ativar o ambiente virtual
source venv/bin/activate

# Executar o dashboard
streamlit run dashboard.py

# Desativar o ambiente virtual ao fechar
deactivate
