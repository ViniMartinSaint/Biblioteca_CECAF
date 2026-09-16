# Sistema Web para Gestão de Biblioteca Escolar
# Projeto Extensionista - CECAF Centro Educacional Casinha Feliz
# Desenvolvido em Python com Dash e Plotly

import os
from datetime import date, timedelta

import dash
from dash import dcc, html, dash_table, Input, Output, State, no_update
import plotly.express as px
import pandas as pd

# ============================================================
# ARQUIVOS CSV PARA SALVAR OS DADOS
# ============================================================

# Usa sempre a pasta onde este arquivo está localizado.
# Isso evita problemas no Windows quando o programa é iniciado por atalho,
# arquivo .bat ou duplo clique em outro diretório.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARQUIVO_LIVROS = os.path.join(BASE_DIR, "livros_biblioteca.csv")
ARQUIVO_EMPRESTIMOS = os.path.join(BASE_DIR, "emprestimos_biblioteca.csv")

# ============================================================
# FUNÇÕES DE CARREGAMENTO E SALVAMENTO
# ============================================================

def carregar_livros():
    if os.path.exists(ARQUIVO_LIVROS):
        return pd.read_csv(ARQUIVO_LIVROS)

    livros_iniciais = pd.DataFrame([
        {"id": 1, "titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "categoria": "Literatura Infantil", "quantidade_total": 5, "quantidade_disponivel": 3},
        {"id": 2, "titulo": "A Bolsa Amarela", "autor": "Lygia Bojunga", "categoria": "Literatura Infantil", "quantidade_total": 4, "quantidade_disponivel": 2},
        {"id": 3, "titulo": "Menina Bonita do Laço de Fita", "autor": "Ana Maria Machado", "categoria": "Literatura Infantil", "quantidade_total": 6, "quantidade_disponivel": 5},
        {"id": 4, "titulo": "Marcelo, Marmelo, Martelo", "autor": "Ruth Rocha", "categoria": "Literatura Infantil", "quantidade_total": 3, "quantidade_disponivel": 1},
        {"id": 5, "titulo": "O Menino Maluquinho", "autor": "Ziraldo", "categoria": "Literatura Infantil", "quantidade_total": 5, "quantidade_disponivel": 4},
        {"id": 6, "titulo": "Fábulas de Esopo", "autor": "Esopo", "categoria": "Fábulas", "quantidade_total": 4, "quantidade_disponivel": 2},
        {"id": 7, "titulo": "Reinações de Narizinho", "autor": "Monteiro Lobato", "categoria": "Literatura Brasileira", "quantidade_total": 3, "quantidade_disponivel": 2},
        {"id": 8, "titulo": "Chapeuzinho Vermelho", "autor": "Irmãos Grimm", "categoria": "Contos Clássicos", "quantidade_total": 6, "quantidade_disponivel": 3},
    ])
    salvar_livros(livros_iniciais)
    return livros_iniciais


def carregar_emprestimos():
    if os.path.exists(ARQUIVO_EMPRESTIMOS):
        return pd.read_csv(ARQUIVO_EMPRESTIMOS)

    emprestimos_iniciais = pd.DataFrame([
        {"id": 1, "aluno": "Ana Clara", "turma": "2º ano", "livro": "O Pequeno Príncipe", "data_emprestimo": "2025-04-01", "data_prevista_devolucao": "2025-04-08", "data_devolucao_real": "2025-04-08", "status": "Devolvido"},
        {"id": 2, "aluno": "João Miguel", "turma": "3º ano", "livro": "A Bolsa Amarela", "data_emprestimo": "2025-04-03", "data_prevista_devolucao": "2025-04-10", "data_devolucao_real": "", "status": "Emprestado"},
        {"id": 3, "aluno": "Maria Eduarda", "turma": "1º ano", "livro": "Menina Bonita do Laço de Fita", "data_emprestimo": "2025-04-05", "data_prevista_devolucao": "2025-04-12", "data_devolucao_real": "2025-04-12", "status": "Devolvido"},
        {"id": 4, "aluno": "Pedro Henrique", "turma": "4º ano", "livro": "Marcelo, Marmelo, Martelo", "data_emprestimo": "2025-04-06", "data_prevista_devolucao": "2025-04-13", "data_devolucao_real": "", "status": "Emprestado"},
        {"id": 5, "aluno": "Laura Vitória", "turma": "5º ano", "livro": "O Menino Maluquinho", "data_emprestimo": "2025-04-07", "data_prevista_devolucao": "2025-04-14", "data_devolucao_real": "2025-04-14", "status": "Devolvido"},
        {"id": 6, "aluno": "Lucas Gabriel", "turma": "3º ano", "livro": "Fábulas de Esopo", "data_emprestimo": "2025-04-09", "data_prevista_devolucao": "2025-04-16", "data_devolucao_real": "", "status": "Emprestado"},
        {"id": 7, "aluno": "Sofia Beatriz", "turma": "2º ano", "livro": "Chapeuzinho Vermelho", "data_emprestimo": "2025-04-10", "data_prevista_devolucao": "2025-04-17", "data_devolucao_real": "2025-04-17", "status": "Devolvido"},
    ])
    salvar_emprestimos(emprestimos_iniciais)
    return emprestimos_iniciais


def salvar_livros(df):
    df.to_csv(ARQUIVO_LIVROS, index=False)


def salvar_emprestimos(df):
    df.to_csv(ARQUIVO_EMPRESTIMOS, index=False)


livros_df = carregar_livros()
emprestimos_df = carregar_emprestimos()

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def criar_cards(livros, emprestimos):
    total_livros = int(livros["quantidade_total"].sum()) if not livros.empty else 0
    disponiveis = int(livros["quantidade_disponivel"].sum()) if not livros.empty else 0
    emprestados = total_livros - disponiveis
    total_emprestimos = len(emprestimos)
    return total_livros, disponiveis, emprestados, total_emprestimos


def card_indicador(titulo, valor):
    return html.Div([
        html.H4(titulo, style={"margin": "0", "fontSize": "16px", "color": "#555"}),
        html.H2(valor, style={"margin": "10px 0 0 0", "color": "#1f4e79"})
    ], style={
        "backgroundColor": "white",
        "padding": "20px",
        "borderRadius": "12px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.12)",
        "textAlign": "center",
        "width": "23%"
    })


def filtrar_emprestimos(emprestimos, aluno, turma, livro, status, data_inicio, data_fim):
    df = emprestimos.copy()

    if df.empty:
        return df

    df["data_emprestimo_dt"] = pd.to_datetime(df["data_emprestimo"], errors="coerce")

    if aluno:
        df = df[df["aluno"].astype(str).str.lower().str.contains(aluno.lower(), na=False)]

    if turma and turma != "Todas":
        df = df[df["turma"] == turma]

    if livro and livro != "Todos":
        df = df[df["livro"] == livro]

    if status and status != "Todos":
        df = df[df["status"] == status]

    if data_inicio:
        df = df[df["data_emprestimo_dt"] >= pd.to_datetime(data_inicio)]

    if data_fim:
        df = df[df["data_emprestimo_dt"] <= pd.to_datetime(data_fim)]

    return df.drop(columns=["data_emprestimo_dt"], errors="ignore")

# ============================================================
# INICIALIZAÇÃO DO DASH
# ============================================================

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Biblioteca CECAF"

# ============================================================
# LAYOUT
# ============================================================

def servir_layout():
    # Toda vez que a página for carregada ou atualizada no navegador,
    # o sistema lê novamente os arquivos CSV. Assim, as alterações salvas
    # continuam aparecendo mesmo após dar refresh na página.
    livros_atualizados = carregar_livros()
    emprestimos_atualizados = carregar_emprestimos()

    return html.Div([
        dcc.Store(id="store-livros", data=livros_atualizados.to_dict("records")),
        dcc.Store(id="store-emprestimos", data=emprestimos_atualizados.to_dict("records")),

    html.Div([
        html.H1("Sistema de Gestão da Biblioteca Escolar", style={"marginBottom": "5px"}),
        html.H3("CECAF - Centro Educacional Casinha Feliz", style={"marginTop": "0", "fontWeight": "normal"}),
        html.P("Protótipo desenvolvido para atividade extensionista utilizando Python, Dash e Plotly.")
    ], style={
        "backgroundColor": "#1f4e79",
        "color": "white",
        "padding": "25px",
        "borderRadius": "0 0 16px 16px",
        "textAlign": "center"
    }),

    html.Div(id="cards-indicadores", style={
        "display": "flex",
        "justifyContent": "space-between",
        "margin": "25px 40px"
    }),

    html.Div([
        html.H2("Acervo de livros"),
        html.Div([
            dcc.Input(id="input-titulo", placeholder="Título do livro", type="text", style={"flex": "2"}),
            dcc.Input(id="input-autor", placeholder="Autor", type="text", style={"flex": "1.6"}),
            dcc.Input(id="input-categoria", placeholder="Categoria", type="text", style={"flex": "1.6"}),
            dcc.Input(id="input-quantidade", placeholder="Quantidade", type="number", min=1, style={"flex": "1.1"}),
            html.Button(
                children=html.Span(
                    "Cadrastrar Livro",
                    style={ 
                        "display": "inline-block",
                        "width": "100%",
                        "whiteSpace": "nowrap",
                        "textAlign": "center"
                    }
                ),
                id="btn-adicionar-livro",
                n_clicks=0,
                style={
                    "width": "200px",
                    "minWidth": "200px",
                    "height": "36px",
                    "cursor": "pointer",
                    "fontWeight": "bold",
                    "fontSize": "14px",
                    "overflow": "visible"
                }
            )
        ], style={"display": "flex", "gap": "12px", "alignItems": "center", "marginBottom": "20px"}),

        dash_table.DataTable(
            id="tabela-livros",
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "Título", "id": "titulo"},
                {"name": "Autor", "id": "autor"},
                {"name": "Categoria", "id": "categoria"},
                {"name": "Total", "id": "quantidade_total"},
                {"name": "Disponível", "id": "quantidade_disponivel"},
            ],
            page_size=8,
            filter_action="native",
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "8px"},
            style_header={"backgroundColor": "#1f4e79", "color": "white", "fontWeight": "bold"},
        )
    ], style={"backgroundColor": "white", "padding": "25px", "margin": "25px 40px", "borderRadius": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.12)"}),

    html.Div([
        html.H2("Filtros Gerais dos Empréstimos"),
        html.Div([
            html.Div([
                html.Label("Buscar por aluno", style={"fontWeight": "bold", "fontSize": "13px"}),
                dcc.Input(id="filtro-aluno", placeholder="", type="text", style={"width": "100%"}),
            ], style={"width": "22%"}),

            html.Div([
                html.Label("Buscar por turma", style={"fontWeight": "bold", "fontSize": "13px"}),
                dcc.Dropdown(id="filtro-turma", placeholder="", clearable=True, style={"width": "100%"}),
            ], style={"width": "18%"}),

            html.Div([
                html.Label("Buscar por livro", style={"fontWeight": "bold", "fontSize": "13px"}),
                dcc.Dropdown(id="filtro-livro", placeholder="", clearable=True, style={"width": "100%"}),
            ], style={"width": "24%"}),

            html.Div([
                html.Label("Status", style={"fontWeight": "bold", "fontSize": "13px"}),
                dcc.Dropdown(
                    id="filtro-status",
                    options=[
                        {"label": "Todos", "value": "Todos"},
                        {"label": "Emprestado", "value": "Emprestado"},
                        {"label": "Devolvido", "value": "Devolvido"},
                    ],
                    value="Todos",
                    clearable=False,
                    style={"width": "100%"}
                ),
            ], style={"width": "16%"}),

            html.Div([
                html.Label("Espaço de tempo", style={"fontWeight": "bold", "fontSize": "13px"}),
                dcc.DatePickerRange(
                    id="filtro-data",
                    start_date=None,
                    end_date=None,
                    display_format="DD/MM/YYYY",
                    start_date_placeholder_text="Início",
                    end_date_placeholder_text="Fim",
                    style={"width": "100%"}
                ),
            ], style={"width": "20%"}),
        ], style={"display": "flex", "alignItems": "end", "gap": "12px"})
    ], style={"backgroundColor": "white", "padding": "25px", "margin": "25px 40px", "borderRadius": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.12)"}),

    html.Div([
        html.H2("Registro de Empréstimos"),
        html.Div([
            dcc.Input(id="input-aluno", placeholder="Nome do aluno", type="text", style={"width": "24%", "marginRight": "1%"}),
            dcc.Input(id="input-turma", placeholder="Turma", type="text", style={"width": "15%", "marginRight": "1%"}),
            dcc.Dropdown(id="dropdown-livro", placeholder="Selecione o livro", style={"width": "28%", "marginRight": "1%"}),
            dcc.DatePickerSingle(id="input-data", date=date.today(), display_format="DD/MM/YYYY", style={"width": "94%", "marginRight": "1%"}),
            html.Button(
                children=html.Span(
                    "Registrar Empréstimo",
                    style={
                        "display": "inline-block",
                        "width": "100%",
                        "whiteSpace": "nowrap",
                        "textAlign": "center"
                    }
                ),
                id="btn-registrar-emprestimo",
                n_clicks=0,
                style={
                    "width": "200px",
                    "minWidth": "200px",
                    "height": "36px",
                    "cursor": "pointer",
                    "fontWeight": "bold",
                    "fontSize": "14px",
                    "overflow": "visible"
                }
            )
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "20px"}),

        dash_table.DataTable(
            id="tabela-emprestimos",
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "Aluno", "id": "aluno"},
                {"name": "Turma", "id": "turma"},
                {"name": "Livro", "id": "livro"},
                {"name": "Data Empréstimo", "id": "data_emprestimo"},
                {"name": "Data Prevista", "id": "data_prevista_devolucao"},
                {"name": "Data Devolução", "id": "data_devolucao_real"},
                {"name": "Status", "id": "status"},
            ],
            page_size=8,
            row_selectable="single",
            selected_rows=[],
            filter_action="native",
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "8px"},
            style_header={"backgroundColor": "#1f4e79", "color": "white", "fontWeight": "bold"},
            style_data_conditional=[
                {"if": {"filter_query": "{status} = 'Emprestado'"}, "backgroundColor": "#fff3cd"},
                {"if": {"filter_query": "{status} = 'Devolvido'"}, "backgroundColor": "#d4edda"},
            ]
        ),

        html.Div([
            html.Button(
                children=html.Span(
                    "Registrar Devolução Selecionada",
                    style={
                        "display": "inline-block",
                        "width": "100%",
                        "whiteSpace": "nowrap",
                        "textAlign": "center"
                    }
                ),
                id="btn-devolver",
                n_clicks=0,
                style={
                    "width": "250px",
                    "minWidth": "200px",
                    "height": "36px",
                    "cursor": "pointer",
                    "fontWeight": "bold",
                    "fontSize": "14px",
                    "overflow": "visible",
                    "marginTop": "15px"
                }
            ),
            html.Span(id="mensagem-devolucao", style={"fontWeight": "bold", "color": "#1f4e79", "marginLeft": "15px", "marginTop": "15px"})
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "flex-start"})
    ], style={"backgroundColor": "white", "padding": "25px", "margin": "25px 40px", "borderRadius": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.12)"}),

    html.Div([
        html.H2("Dashboard da Biblioteca"),
        html.Div([
            dcc.Graph(id="grafico-categorias", style={"width": "50%"}),
            dcc.Graph(id="grafico-livros-emprestados", style={"width": "50%"}),
        ], style={"display": "flex"})
    ], style={"backgroundColor": "white", "padding": "25px", "margin": "25px 40px", "borderRadius": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.12)"}),

    html.Footer("Projeto Extensionista - Sistema simulado para apoio à biblioteca escolar", style={
        "textAlign": "center",
        "padding": "20px",
        "color": "#666"
    })

    ], style={"backgroundColor": "#f2f5f7", "fontFamily": "Arial, sans-serif", "minHeight": "100vh"})


app.layout = servir_layout

# ============================================================
# CALLBACKS
# ============================================================

@app.callback(
    Output("cards-indicadores", "children"),
    Input("store-livros", "data"),
    Input("store-emprestimos", "data")
)
def atualizar_cards(livros_data, emprestimos_data):
    livros = pd.DataFrame(livros_data)
    emprestimos = pd.DataFrame(emprestimos_data)
    total_livros, disponiveis, emprestados, total_emprestimos = criar_cards(livros, emprestimos)

    return [
        card_indicador("Total de Exemplares", total_livros),
        card_indicador("Livros Disponíveis", disponiveis),
        card_indicador("Livros Emprestados", emprestados),
        card_indicador("Total de Empréstimos", total_emprestimos),
    ]


@app.callback(
    Output("tabela-livros", "data"),
    Input("store-livros", "data")
)
def atualizar_tabela_livros(livros_data):
    return livros_data


@app.callback(
    Output("tabela-emprestimos", "data"),
    Input("store-emprestimos", "data"),
    Input("filtro-aluno", "value"),
    Input("filtro-turma", "value"),
    Input("filtro-livro", "value"),
    Input("filtro-status", "value"),
    Input("filtro-data", "start_date"),
    Input("filtro-data", "end_date")
)
def atualizar_tabela_emprestimos(emprestimos_data, aluno, turma, livro, status, data_inicio, data_fim):
    emprestimos = pd.DataFrame(emprestimos_data)
    emprestimos_filtrados = filtrar_emprestimos(emprestimos, aluno, turma, livro, status, data_inicio, data_fim)
    return emprestimos_filtrados.to_dict("records")


@app.callback(
    Output("dropdown-livro", "options"),
    Input("store-livros", "data")
)
def atualizar_dropdown_livros(livros_data):
    livros = pd.DataFrame(livros_data)
    livros_disponiveis = livros[livros["quantidade_disponivel"] > 0]
    return [{"label": row["titulo"], "value": row["titulo"]} for _, row in livros_disponiveis.iterrows()]


@app.callback(
    Output("filtro-turma", "options"),
    Output("filtro-livro", "options"),
    Input("store-emprestimos", "data")
)
def atualizar_opcoes_filtros(emprestimos_data):
    emprestimos = pd.DataFrame(emprestimos_data)

    if emprestimos.empty:
        return [], []

    turmas = sorted(emprestimos["turma"].dropna().unique())
    livros = sorted(emprestimos["livro"].dropna().unique())

    opcoes_turma = [{"label": turma, "value": turma} for turma in turmas]
    opcoes_livro = [{"label": livro, "value": livro} for livro in livros]

    return opcoes_turma, opcoes_livro


@app.callback(
    Output("store-livros", "data"),
    Input("btn-adicionar-livro", "n_clicks"),
    State("input-titulo", "value"),
    State("input-autor", "value"),
    State("input-categoria", "value"),
    State("input-quantidade", "value"),
    State("store-livros", "data"),
    prevent_initial_call=True
)
def adicionar_livro(n_clicks, titulo, autor, categoria, quantidade, livros_data):
    if not titulo or not autor or not categoria or not quantidade:
        return livros_data

    livros = pd.DataFrame(livros_data)
    novo_id = int(livros["id"].max()) + 1 if not livros.empty else 1

    novo_livro = {
        "id": novo_id,
        "titulo": titulo,
        "autor": autor,
        "categoria": categoria,
        "quantidade_total": int(quantidade),
        "quantidade_disponivel": int(quantidade),
    }

    livros = pd.concat([livros, pd.DataFrame([novo_livro])], ignore_index=True)
    salvar_livros(livros)
    return livros.to_dict("records")


@app.callback(
    Output("store-emprestimos", "data"),
    Output("store-livros", "data", allow_duplicate=True),
    Input("btn-registrar-emprestimo", "n_clicks"),
    State("input-aluno", "value"),
    State("input-turma", "value"),
    State("dropdown-livro", "value"),
    State("input-data", "date"),
    State("store-emprestimos", "data"),
    State("store-livros", "data"),
    prevent_initial_call=True
)
def registrar_emprestimo(n_clicks, aluno, turma, livro, data_emprestimo, emprestimos_data, livros_data):
    if not aluno or not turma or not livro or not data_emprestimo:
        return emprestimos_data, livros_data

    emprestimos = pd.DataFrame(emprestimos_data)
    livros = pd.DataFrame(livros_data)

    linha_livro = livros[livros["titulo"] == livro]
    if linha_livro.empty:
        return emprestimos_data, livros_data

    idx = linha_livro.index[0]
    if livros.loc[idx, "quantidade_disponivel"] <= 0:
        return emprestimos_data, livros_data

    livros.loc[idx, "quantidade_disponivel"] -= 1

    novo_id = int(emprestimos["id"].max()) + 1 if not emprestimos.empty else 1
    data_emp = pd.to_datetime(data_emprestimo)
    data_dev = data_emp + pd.Timedelta(days=7)

    novo_emprestimo = {
        "id": novo_id,
        "aluno": aluno,
        "turma": turma,
        "livro": livro,
        "data_emprestimo": data_emp.strftime("%Y-%m-%d"),
        "data_prevista_devolucao": data_dev.strftime("%Y-%m-%d"),
        "data_devolucao_real": "",
        "status": "Emprestado",
    }

    emprestimos = pd.concat([emprestimos, pd.DataFrame([novo_emprestimo])], ignore_index=True)

    salvar_emprestimos(emprestimos)
    salvar_livros(livros)

    return emprestimos.to_dict("records"), livros.to_dict("records")


@app.callback(
    Output("store-emprestimos", "data", allow_duplicate=True),
    Output("store-livros", "data", allow_duplicate=True),
    Output("mensagem-devolucao", "children"),
    Input("btn-devolver", "n_clicks"),
    State("tabela-emprestimos", "selected_rows"),
    State("tabela-emprestimos", "data"),
    State("store-emprestimos", "data"),
    State("store-livros", "data"),
    prevent_initial_call=True
)
def registrar_devolucao(n_clicks, selected_rows, tabela_filtrada_data, emprestimos_data, livros_data):
    if not selected_rows:
        return no_update, no_update, "Selecione um empréstimo na tabela para registrar a devolução."

    linha_selecionada = tabela_filtrada_data[selected_rows[0]]
    id_emprestimo = linha_selecionada["id"]

    emprestimos = pd.DataFrame(emprestimos_data)
    livros = pd.DataFrame(livros_data)

    idx_emprestimo = emprestimos[emprestimos["id"] == id_emprestimo].index
    if len(idx_emprestimo) == 0:
        return no_update, no_update, "Empréstimo não encontrado."

    idx_emprestimo = idx_emprestimo[0]

    if emprestimos.loc[idx_emprestimo, "status"] == "Devolvido":
        return no_update, no_update, "Este livro já foi devolvido."

    livro_devolvido = emprestimos.loc[idx_emprestimo, "livro"]
    emprestimos.loc[idx_emprestimo, "status"] = "Devolvido"
    emprestimos.loc[idx_emprestimo, "data_devolucao_real"] = date.today().strftime("%Y-%m-%d")

    idx_livro = livros[livros["titulo"] == livro_devolvido].index
    if len(idx_livro) > 0:
        idx_livro = idx_livro[0]
        if livros.loc[idx_livro, "quantidade_disponivel"] < livros.loc[idx_livro, "quantidade_total"]:
            livros.loc[idx_livro, "quantidade_disponivel"] += 1

    salvar_emprestimos(emprestimos)
    salvar_livros(livros)

    return emprestimos.to_dict("records"), livros.to_dict("records"), "Devolução registrada com sucesso."


@app.callback(
    Output("grafico-categorias", "figure"),
    Output("grafico-livros-emprestados", "figure"),
    Input("store-livros", "data"),
    Input("store-emprestimos", "data"),
    Input("filtro-aluno", "value"),
    Input("filtro-turma", "value"),
    Input("filtro-livro", "value"),
    Input("filtro-status", "value"),
    Input("filtro-data", "start_date"),
    Input("filtro-data", "end_date")
)
def atualizar_graficos(livros_data, emprestimos_data, aluno, turma, livro, status, data_inicio, data_fim):
    livros = pd.DataFrame(livros_data)
    emprestimos = pd.DataFrame(emprestimos_data)
    emprestimos_filtrados = filtrar_emprestimos(emprestimos, aluno, turma, livro, status, data_inicio, data_fim)

    categoria_df = livros.groupby("categoria", as_index=False)["quantidade_total"].sum()
    fig_categoria = px.pie(
        categoria_df,
        names="categoria",
        values="quantidade_total",
        title="Distribuição do acervo por categoria",
        hole=0.35
    )

    fig_categoria.update_traces(
    textposition="inside",
    textinfo="percent+label"
    )

    if emprestimos_filtrados.empty:
        livros_mais_emprestados = pd.DataFrame({"livro": [], "quantidade": []})
    else:
        livros_mais_emprestados = emprestimos_filtrados.groupby("livro", as_index=False).size()
        livros_mais_emprestados = livros_mais_emprestados.rename(columns={"size": "quantidade"}).sort_values("quantidade", ascending=False)

    # ordenar decrescente
    livros_mais_emprestados = livros_mais_emprestados.sort_values("quantidade", ascending=False)

    fig_emprestados = px.bar(
        livros_mais_emprestados,
        y="livro",
        x="quantidade",
        orientation='h',
        title="Ranking de livros mais emprestados",
        labels={"livro": "Livro", "quantidade": "Quantidade de empréstimos"}
    )

    # deixar inteiros no eixo X
    fig_emprestados.update_xaxes(dtick=1)

    # inverter eixo Y para maior ficar em cima
    fig_emprestados.update_layout(yaxis={'categoryorder':'total ascending'})

    return fig_categoria, fig_emprestados

# ============================================================
# EXECUÇÃO DO SISTEMA
# ============================================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=False)
