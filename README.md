# Sistema de Gerência Orçamentária

Um **sistema de preenchimento e acompanhamento de processos de execução orçamentária** voltado para o âmbito da administração pública. Permite ao time técnico registrar cada processo, controlar limites de execução (total e percentuais) e fornece um painel interativo para gestores e secretários acompanharem indicadores em tempo real.

---

## 📝 Descrição

- **Objetivo**: Registrar, filtrar, agrupar e pivotar os processos orçamentários para monitorar o limite de execução do exercício corrente.  
- **Público‑alvo**: Técnicos de orçamento, gestores e secretários de órgãos públicos.  
- **Tecnologias**:  
  - [Streamlit](https://streamlit.io/) — interface web reativa  
  - [st‑aggrid](https://github.com/PablocFonseca/streamlit-aggrid) — tabelas interativas com filtros, agrupamentos e pivot  
  - [gspread](https://github.com/burnash/gspread) via `streamlit_gsheets` — backend de planilhas Google Sheets  
  - Python 3.8+ e bibliotecas auxiliares (pandas, etc.)

---

## 🚀 Funcionalidades Principais

1. **Cadastro e Edição de Processos**  
   - Formulários validados para inserir dados de cada processo (número, tipo de crédito, grupo de despesas, valores, datas etc.).  
   - Edição em tela única com salvamento direto em Google Sheets.

2. **Visualização e Filtros Avançados**  
   - Tabela AG‑Grid com:  
     - Filtros de texto, conjunto (checkbox) e data  
     - Ordenação, redimensionamento e wrap de textos  
     - Seleção de célula, cópia rápida (Ctrl +C) e duplo‑clique para copiar  
     - Pivot Mode e drag‑and‑drop para agrupamentos e agregações  

3. **Painel de Indicadores**  
   - Cartões com:  
     - Orçamento Aprovado  
     - Limite de Execução (10%)  
     - Limite Executado  
     - Percentual Executado do Total / do Limite  
   - Gráfico donut mostrando Executado × Disponível.

4. **Relatórios e Exportação**  
   - Geração de relatórios consolidados  
   - Download em PDF.

5. **Persistência de Estado**  
   - Configurações de filtros, colunas e pivot salvas na `session_state`.  
   - Usuário pode navegar entre páginas sem perder personalizações.

---

## 🛠 Dificuldades Encontradas

- **Adaptação a um novo sistema**: foi necessário moldar processos existentes, colher feedbacks constantes dos técnicos de orçamento e ajustar formulários e fluxos de trabalho conforme as demandas reais.  
- **Customização avançada do AG‑Grid**: filtros dinâmicos, pivot e persistência de estado exigiram entendimento profundo do módulo enterprise.  
- **Performance e caching**: equilibrar chamadas ao Google Sheets via `streamlit_gsheets` com `@st.experimental_memo` para manter o app responsivo.  
- **Gestão de credenciais e cotas**: lidar com erros da Google Sheets API e implementar retry/back‑off para garantir confiabilidade.  
- **Design responsivo**: personalizar a barra lateral e os componentes para diferentes resoluções e fluxos de uso.  

---

## 📂 Estrutura do Projeto

```plaintext
gerencia_orcamento/
├── .gitignore
├── .streamlit/
│   └── config.toml               ← configurações do Streamlit
├── Home.py                       ← ponto de entrada principal (layout & sidebar)
├── packages.txt                  ← lista de dependências congeladas (pip freeze)
├── requirements.txt              ← dependências do projeto
├── README.md                     ← documentação do projeto
├── image/                        ← imagens utilizadas no app
│   ├── 2.jpg
│   ├── default.png
│   └── SEPLAG.png
├── pages/                        ← páginas automáticas do Streamlit
│   ├── cadastro.py
│   ├── editar.py
│   ├── login.py
│   ├── relatorio.py
│   └── visualizar.py
├── sidebar/                      ← componentes da barra lateral
│   ├── customizacao.py
│   ├── page_cadastro.py
│   ├── page_editar.py
│   ├── page_home.py
│   ├── page_relatorio.py
│   ├── page_visualizar.py
│   └── sem_display.py
├── src/                          ← núcleo de conexão e carregamento de dados
│   ├── __pycache__/
│   └── base.py
└── utils/                        ← módulos utilitários
    ├── buscadores/              ← funções de busca e mapeamento
    │   ├── __pycache__/
    │   ├── contabilizar_limite.py
    │   ├── fonte_recurso.py
    │   ├── grupo_despesa.py
    │   ├── opcoes_colunas.py
    │   ├── orgao_uo.py
    │   ├── origem_recurso.py
    │   ├── situacao.py
    │   └── tipo_credito.py
    ├── calculo_limite/          ← regras de cálculo de limites orçamentários
    │   ├── __pycache__/
    │   └── limite.py
    ├── digitacao/               ← máscaras e validação de inputs
    │   ├── __pycache__/
    │   ├── digitacao.py
    │   └── gerar_relatorio.py
    ├── estilizacao/             ← customizações de estilo (CSS/JS para AG‑Grid)
    │   ├── __pycache__/
    │   ├── background.py
    │   └── dataframe.py
    ├── formatar/                ← formatação de moeda, datas, etc.
    │   ├── __pycache__/
    │   ├── formatar_numero_decreto.py
    │   └── formatar_valor.py
    ├── marca/                   ← helpers de branding e logos
    │   ├── __pycache__/
    │   └── creditos.py
    ├── processo/                ← lógica de processos orçamentários
    │   ├── __pycache__/
    │   ├── edicao_processo.py
    │   └── filtros_visualizar.py
    ├── relatorio/               ← geração de relatórios consolidados
    │   ├── __pycache__/
    │   ├── botao_cpof.py
    │   └── relatorio_cpof.py
    ├── sessao/                  ← gestão de estado da sessão (session_state)
    │   ├── __pycache__/
    │   └── login.py
    ├── validadores/             ← validações de formulários
    │   ├── __pycache__/
    │   ├── data.py
    │   ├── numero_decreto.py
    │   ├── numero_processo.py
    │   ├── objetivo.py
    │   ├── observacao.py
    │   ├── processo.py
    │   └── valor.py
    └── zBackup/                 ← backups de scripts antigos

```


## 🏆 Créditos
Desenvolvido por [Lucas Falcão](https://www.linkedin.com/in/falkzera/)  
Apoio técnico de [Felliphy Queiroz](https://www.linkedin.com/in/felliphyqueiroz/)
