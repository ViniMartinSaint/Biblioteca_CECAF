# 📚 Biblioteca CECAF

## Sistema de Gestão da Biblioteca Escolar

Projeto desenvolvido para o **CECAF --- Centro Educacional Casinha
Feliz** com o objetivo de facilitar a organização e o controle da
biblioteca escolar.

O sistema foi criado como parte de uma **atividade extensionista** e
utiliza **Python, Dash, Plotly e Pandas** para oferecer uma interface
web simples para cadastro do acervo, registro de empréstimos e
devoluções, pesquisa de movimentações e visualização de indicadores da
biblioteca.

> **Objetivo:** tornar o controle do acervo e dos empréstimos mais
> simples, organizado e visual, auxiliando a equipe escolar no
> acompanhamento da utilização da biblioteca.

------------------------------------------------------------------------

## 🖼️ Visão geral do sistema

<img width="1353" height="763" alt="image" src="https://github.com/user-attachments/assets/5d1a8534-ce63-41c0-bf4c-fabb987af852" />

A página inicial reúne os principais indicadores da biblioteca e permite
acessar as funções de controle do acervo e dos empréstimos em uma única
interface.

------------------------------------------------------------------------

## ✨ Funcionalidades

### 📊 1. Painel de indicadores

Na parte superior do sistema são apresentados indicadores atualizados
automaticamente a partir dos dados cadastrados:

-   **Total de Exemplares**
-   **Livros Disponíveis**
-   **Livros Emprestados**
-   **Total de Empréstimos**

Esses dados permitem visualizar rapidamente a situação atual do acervo.

<img width="1277" height="119" alt="image" src="https://github.com/user-attachments/assets/d8fedf9e-7669-488a-8792-c22ca3cfcf26" />


------------------------------------------------------------------------
### 📚 2. Cadastro e controle do acervo

Novos livros podem ser adicionados diretamente pelo sistema. Para cada
obra são registrados:

-   título;
-   autor;
-   categoria;
-   quantidade de exemplares.

O sistema gera um identificador para o livro e controla separadamente a
**quantidade total** e a **quantidade disponível**.

A tabela do acervo permite visualizar:

  Campo        Descrição
  ------------ ---------------------------------------
  ID           Identificador do livro
  Título       Nome da obra
  Autor        Autor do livro
  Categoria    Classificação da obra
  Total        Quantidade total de exemplares
  Disponível   Quantidade disponível para empréstimo

A própria tabela também possui recursos de **filtro e ordenação**.

<img width="1278" height="440" alt="image" src="https://github.com/user-attachments/assets/d4459628-1f2d-49b7-8864-5cda42f0bd0c" />


------------------------------------------------------------------------

### 🔎 3. Pesquisa e filtros

O sistema possui uma área de **Filtros Gerais** que permite localizar
movimentações da biblioteca de forma rápida.

É possível pesquisar por:

-   nome do aluno;
-   turma;
-   título do livro;
-   status do empréstimo (**Emprestado** ou **Devolvido**);
-   intervalo de datas.

Os filtros também são utilizados para atualizar os dados apresentados na
tabela de empréstimos e no relatório gráfico de livros mais emprestados.

------------------------------------------------------------------------

### 🤝 4. Registro de empréstimos

A área de empréstimos permite registrar a retirada de um livro por um
aluno.

São informados:

-   nome do aluno;
-   turma;
-   livro;
-   data do empréstimo.

Somente livros que possuem exemplares disponíveis são apresentados para
seleção. Ao registrar um empréstimo, o sistema reduz automaticamente a
quantidade disponível daquele livro.

O sistema também calcula uma **data prevista de devolução de 7 dias após
o empréstimo**.

<img width="1274" height="566" alt="image" src="https://github.com/user-attachments/assets/4190cc59-d55f-4aaa-a866-3aa05e1ebf35" />

------------------------------------------------------------------------

### ↩️ 5. Registro de devoluções

Para registrar uma devolução, basta selecionar o empréstimo
correspondente na tabela e utilizar a opção:

**Registrar Devolução do Empréstimo Selecionado**

Quando a devolução é registrada, o sistema:

1.  altera o status de **Emprestado** para **Devolvido**;
2.  registra a data real da devolução;
3.  devolve automaticamente uma unidade ao estoque disponível do livro;
4.  impede que o mesmo empréstimo seja devolvido novamente.

------------------------------------------------------------------------

### 📋 6. Histórico de empréstimos

A tabela de movimentações mantém o histórico dos empréstimos
registrados.

Ela apresenta:

  Informação        Descrição
  ----------------- -----------------------------------
  ID                Identificação do empréstimo
  Aluno             Aluno responsável pelo empréstimo
  Turma             Turma do aluno
  Livro             Livro emprestado
  Data Empréstimo   Data de retirada
  Data Prevista     Previsão de devolução
  Data Devolução    Data em que o livro foi devolvido
  Status            Emprestado ou Devolvido

Os registros também possuem identificação visual para facilitar a
leitura dos livros que ainda estão emprestados e dos que já foram
devolvidos.

<img width="1280" height="449" alt="image" src="https://github.com/user-attachments/assets/662ddaae-edb3-4e7a-bd7f-fcbf51a5c988" />

------------------------------------------------------------------------

### 📈 7. Dashboard da biblioteca

O projeto utiliza **Plotly** para transformar os dados da biblioteca em
informações visuais.

Atualmente o dashboard possui dois gráficos principais:

#### Quantidade de livros por categoria

Apresenta a distribuição dos exemplares do acervo de acordo com suas
categorias.

#### Ranking de livros mais emprestados

Mostra quais livros tiveram o maior número de empréstimos registrados. O
ranking também acompanha os filtros utilizados no sistema.

<img width="1280" height="449" alt="image" src="https://github.com/user-attachments/assets/d2b494cb-a9e2-4652-a12f-b5d28a706cfe" />

------------------------------------------------------------------------

## 💾 Armazenamento dos dados

Para manter o projeto simples e adequado ao ambiente escolar proposto,
os dados são armazenados em arquivos **CSV**.

Os principais arquivos são:

``` text
livros_biblioteca.csv
emprestimos_biblioteca.csv
```

O arquivo de livros mantém os dados do acervo e a quantidade disponível
de cada obra. O arquivo de empréstimos registra as movimentações,
alunos, turmas, datas e status.

As alterações feitas pela aplicação são salvas nesses arquivos e, ao
recarregar a página, o sistema realiza uma nova leitura dos CSVs.

------------------------------------------------------------------------

## 🛠️ Tecnologias utilizadas

  Tecnologia              Utilização
  ----------------------- --------------------------------------------------
  **Python**              Desenvolvimento da aplicação e regras do sistema
  **Dash**                Construção da interface web
  **Plotly**              Criação dos gráficos e dashboard
  **Pandas**              Leitura, tratamento e gravação dos dados
  **CSV**                 Persistência dos dados do acervo e empréstimos
  **HTML/CSS via Dash**   Estrutura e apresentação visual da aplicação

------------------------------------------------------------------------

## 📂 Estrutura do projeto

A estrutura pode variar entre as versões para Linux e Windows, mas o
projeto utiliza arquivos semelhantes aos seguintes:

``` text
Biblioteca_CECAF/
│
│
├── Estoque-biblioteca-Windows/
│   ├── main_windows.py
│   ├── iniciar_biblioteca_windows.bat
│   ├── livros_biblioteca.csv
│   ├── emprestimos_biblioteca.csv
│   └── requirements_windows.txt
│
└── README.md
```

------------------------------------------------------------------------

## 🚀 Como executar

### Linux

Entre na pasta correspondente ao sistema e instale as dependências:

``` bash
pip install -r requirements.txt
```

Depois execute:

``` bash
python3 main.py
```

### Windows

Na versão para Windows, instale as dependências:

``` bash
pip install -r requirements_windows.txt
```

Depois execute:

``` bash
python main_windows.py
```

A versão do projeto também pode incluir o arquivo:

``` text
iniciar_biblioteca_windows.bat
```

para facilitar a inicialização do sistema no computador da escola.

Após iniciar a aplicação, abra no navegador o endereço exibido pelo
terminal. Em uma execução local padrão do Dash, normalmente será:

``` text
http://127.0.0.1:8050
```

------------------------------------------------------------------------

## 🧪 Metodologia do projeto

O desenvolvimento foi organizado nas seguintes etapas:

1.  levantamento das necessidades da biblioteca escolar;
2.  identificação dos dados necessários;
3.  planejamento das funcionalidades;
4.  desenvolvimento do sistema em Python com Dash e Plotly;
5.  criação de uma base de dados simulada;
6.  testes com dados fictícios;
7.  simulação de uso no ambiente escolar;
8.  análise dos resultados;
9.  ajustes e melhorias.

O projeto foi desenvolvido ao longo de aproximadamente **1,5 mês**,
passando da identificação do problema até os testes e refinamentos
finais.

------------------------------------------------------------------------

## 🎯 Aplicação no CECAF

O sistema foi pensado para a biblioteca do **Centro Educacional Casinha
Feliz (CECAF)** como uma ferramenta de apoio à organização do acervo
escolar.

A proposta demonstra como uma solução simples pode substituir controles
manuais e centralizar informações importantes, como disponibilidade de
livros, histórico de empréstimos, devoluções e indicadores de utilização
da biblioteca.

O protótipo também permite que novas funcionalidades sejam incorporadas
futuramente conforme as necessidades da instituição.

------------------------------------------------------------------------

## 🔮 Possíveis evoluções

Como continuidade do projeto, a aplicação pode futuramente receber
recursos como autenticação de usuários, banco de dados relacional,
cadastro individual de alunos, alertas de atraso, geração de relatórios
em PDF e rotinas de backup.

------------------------------------------------------------------------

## 👨‍💻 Autor

**Vinícius Martins dos Santos**

Projeto desenvolvido para atividade extensionista aplicada ao **CECAF
--- Centro Educacional Casinha Feliz**.

------------------------------------------------------------------------

## 📄 Observação

Este repositório apresenta um projeto educacional de gestão de
biblioteca escolar. Durante o desenvolvimento e os testes foram
utilizados dados simulados/fictícios.
