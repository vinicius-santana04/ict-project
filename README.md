## 🇧🇷 Português

# ICT Project - Análise de Métricas de Futebol

### Descrição Detalhada

Este projeto representa a fase fundamental de uma iniciativa maior, focada na análise avançada de partidas de futebol através de Visão Computacional. O objetivo principal desta etapa foi a transcrição e adaptação de um conjunto de métricas de desempenho, originalmente implementadas em MATLAB, para a linguagem de programação Python.

A migração para Python é um passo estratégico, pois permitirá a integração fluida com bibliotecas de ponta em Visão Computacional e aprendizado de máquina. No futuro, um sistema automatizado irá capturar dados brutos de vídeos de jogos de futebol (como posicionamento de jogadores, posse de bola, etc.). Esses dados serão então processados pelas métricas implementadas neste repositório para gerar análises táticas e de desempenho aprofundadas, tanto individuais quanto coletivas.

As métricas aqui contidas são a base para a extração de insights valiosos que podem ser utilizados por comissões técnicas, analistas de desempenho e entusiastas do esporte para entender melhor as dinâmicas de um jogo.

### Estrutura do Projeto

O projeto está organizado da seguinte forma, com cada componente tendo um propósito específico:

```
├── .idea/              # Pasta com configurações específicas do ambiente de desenvolvimento (IDE).
│
├── data/               # Diretório destinado ao armazenamento de conjuntos de dados, como arquivos CSV,
│                       # JSON ou outros formatos que possam ser usados para testar e validar as métricas.
│
├── metrics/            # Contém os scripts Python com a implementação das métricas de análise.
│                       # Cada arquivo pode representar uma métrica ou um conjunto de métricas relacionadas.
│
├── README.md           # Este arquivo, contendo a documentação completa do projeto.
│
└── main.py             # Ponto de entrada principal do projeto. Este script é responsável por orquestrar
                        # a execução, carregar os dados, aplicar as métricas e exibir os resultados.
```

### Tecnologias Utilizadas

A escolha das tecnologias foi pautada pela eficiência, compatibilidade e pelo ecossistema robusto disponível para análise de dados e computação científica.

  * **Python (94.2%):** A linguagem principal do projeto, escolhida por sua simplicidade, vasta quantidade de bibliotecas para análise de dados (Pandas, NumPy, etc.) e por ser o padrão da indústria para projetos de Visão Computacional e Inteligência Artificial.
  * **Cython (3.4%):** Utilizado para otimizar partes críticas do código que exigem maior desempenho, permitindo a compilação de código Python para C.
  * **C (1.2%) e C++ (1.0%):** Empregadas em módulos de baixo nível para acelerar cálculos computacionalmente intensivos.
  * **Fortran (0.1%):** Usado para integrar bibliotecas legadas ou rotinas numéricas de alta performance.
  * **JavaScript (0.1%):** Potencialmente utilizado para futuras visualizações de dados interativas.

### Como Executar o Projeto

Para configurar e executar este projeto em seu ambiente local, siga os passos detalhados abaixo:

1.  **Clonar o Repositório:** Abra um terminal e execute o seguinte comando para baixar os arquivos do projeto.
    ```bash
    git clone https://github.com/vinicius-santana04/ict-project.git
    ```
2.  **Navegar para o Diretório:** Entre na pasta do projeto que você acabou de clonar.
    ```bash
    cd ict-project
    ```
3.  **Instalar as Dependências:** É altamente recomendável criar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    # Crie um ambiente virtual (opcional, mas recomendado)
    python -m venv venv

    # Ative o ambiente virtual
    # No Windows:
    # venv\Scripts\activate
    # No macOS/Linux:
    # source venv/bin/activate
    ```
4.  **Executar o Script Principal:** Com as dependências instaladas, você pode executar o projeto.
    ```bash
    python main.py
    ```
    Certifique-se de que os dados necessários estejam na pasta `/data` para que o script funcione corretamente.

-----

## 🇬🇧 English

# ICT Project - Soccer Metrics Analysis

### Detailed Description

This project represents the foundational phase of a larger initiative focused on the advanced analysis of soccer matches using Computer Vision. The primary goal of this stage was to transcribe and adapt a set of performance metrics, originally implemented in MATLAB, into the Python programming language.

Migrating to Python is a strategic move, as it will allow for seamless integration with cutting-edge libraries in Computer Vision and Machine Learning. In the future, an automated system will capture raw data from soccer game videos (such as player positioning, ball possession, etc.). This data will then be processed by the metrics implemented in this repository to generate in-depth tactical and performance analyses, for both individuals and teams.

The metrics contained herein are the basis for extracting valuable insights that can be used by coaching staff, performance analysts, and sports enthusiasts to better understand game dynamics.

### Project Structure

The project is organized as follows, with each component serving a specific purpose:

```
├── .idea/              # Folder with specific settings for the development environment (IDE).
│
├── data/               # Directory for storing datasets, such as CSV, JSON, or other formats
│                       # that can be used to test and validate the metrics.
│
├── metrics/            # Contains the Python scripts with the implementation of the analysis metrics.
│                       # Each file may represent a single metric or a set of related metrics.
│
├── README.md           # This file, containing the complete project documentation.
│
└── main.py             # The main entry point of the project. This script is responsible for orchestrating
                        # the execution, loading data, applying metrics, and displaying the results.
```

### Technologies Used

The choice of technologies was guided by efficiency, compatibility, and the robust ecosystem available for data analysis and scientific computing.

  * **Python (94.2%):** The main language of the project, chosen for its simplicity, vast number of libraries for data analysis (Pandas, NumPy, etc.), and for being the industry standard for Computer Vision and Artificial Intelligence projects.
  * **Cython (3.4%):** Used to optimize critical parts of the code that require higher performance, allowing Python code to be compiled to C.
  * **C (1.2%) & C++ (1.0%):** Employed in low-level modules to accelerate computationally intensive calculations.
  * **Fortran (0.1%):** Used to integrate legacy libraries or high-performance numerical routines.
  * **JavaScript (0.1%):** Potentially used for future interactive data visualizations.

### How to Run the Project

To set up and run this project in your local environment, follow the detailed steps below:

1.  **Clone the Repository:** Open a terminal and run the following command to download the project files.
    ```bash
    git clone https://github.com/vinicius-santana04/ict-project.git
    ```
2.  **Navigate to the Directory:** Enter the project folder you just cloned.
    ```bash
    cd ict-project
    ```
3.  **Install Dependencies:** It is highly recommended to create a virtual environment to isolate the project's dependencies.
    ```bash
    # Create a virtual environment (optional, but recommended)
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
4.  **Run the Main Script:** With the dependencies installed, you can run the project.
    ```bash
    python main.py
    ```
    Ensure that the necessary data is in the `/data` folder for the script to work correctly.
