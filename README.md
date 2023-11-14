# hackaton-2023

## 1. Introdução

Este documento descreve uma solução desenvolvida em Python para correção automática de testes e simulados de múltipla escolha. A própria utiliza solução de visão computacional e aprendizado de máquina para realizar a leitura do gabarito, analisar os cartões resposta dos alunos, comparar as respostas e gerar relatórios individuais. Além disso, inclui um sistema de gerenciamento de dados para armazenar os resultados de forma organizada.

## 2. Objetivo do Projeto

O objetivo principal deste projeto é automatizar o processo de correção de provas de múltipla escolha, proporcionando eficiência e precisão na avaliação dos resultados dos alunos.

## 3. Funcionalidades

### 3.1. Leitura do Gabarito

O webapp é capaz de ler e interpretar o gabarito da prova, identificando as respostas corretas para cada questão. Isso é feito por meio de técnicas de processamento de imagem e análise de padrões, são elas: o reconhecimento óptico de marcas (OMR), Python e a biblioteca OpenCV.

### 3.2. Leitura do Cartão Resposta

O webapp pode analisar os cartões resposta preenchidos pelos alunos, identificando as opções marcadas em cada questão. Utilizando técnicas avançadas de visão computacional, no qual se trata do reconhecimento óptico de marcas, que é descrito como o processo de análise automática de documentos marcados por humanos. Além disso, o sistema é capaz de extrair as marcações de forma precisa.

### 3.3. Comparação e Pontuação

Com base na leitura do gabarito e do cartão de resposta, a solução compara as respostas dos alunos com as respostas corretas, atribuindo uma pontuação a cada questão. A pontuação é calculada de acordo com a correspondência entre as escolhas dos alunos e as respostas corretas.

### 3.4. Relatórios Individuais

Gera uma solução de relatórios individuais para cada aluno, destacando as questões corretas e incorretas, além de fornecer a pontuação final. Esses relatórios são apresentados de maneira clara e compreensível para facilitar a compreensão do desempenho individual.

## 4. Gerenciamento de Dados

Os resultados da correção são armazenados de forma organizada em um sistema de gerenciamento de dados (SQLite). Isso permite o acesso fácil e rápido a informações passadas, possibilitando análises históricas, identificação de padrões e melhoria contínua do sistema.

## 5. Tecnologias utilizadas

- Flask
- Sqlite3
- Tailwindcss
- Flowbite
- JavaScript
- Cv2
- Numpy
- Imutils

## 6. Arquitetura do Sistema

### 6.3. Módulo de Interface Web

- Desenvolvimento de uma interface web para facilitar o carregamento de imagens e exibição dos resultados.
- Integração com os módulos de processamento de imagem e aprendizado de máquina.
- Geração de relatórios de correção para cada prova ou simulado.

## 7. Fluxo de Trabalho

### 7.1 Funcionalidades apresentadas:

- O usuário carrega a imagem da folha de resposta através da interface web.
- Cadastro de turma
- Cadastro de aluno
- Cadastro de provas
- Cadastro de gabaritos

### 7.2 Processamento de Imagem:

- A imagem é processada para realçar as marcações.
- Áreas relevantes são identificadas utilizando técnicas de visão computacional.

### 7.3 Aprendizado de Máquina:

- O modelo treinado é aplicado para classificar as respostas marcadas.
- A precisão do modelo é verificada utilizando técnicas de validação.

### 7.4 Geração de Relatórios:

- Um relatório de correção é gerado, mostrando as respostas corretas e incorretas.
- A interface web exibe os resultados de forma acessível para professores e alunos.

## 8. Requisitos do Sistema

- Python 3.11
- Bibliotecas: OpenCV, NumPy, Imutils

## 9. Instalação e Configuração

Clone o repositório para o seu sistema local:

```bash
git clone https://github.com/seu-usuario/meu-projeto-flask.git
```

Navegue até o diretório do projeto:

```bash
cd meu-projeto-flask
```

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

Ative o ambiente virtual:

No Windows:

```bash
venv\Scripts\activate
```

No macOS/Linux:

```bash
source venv/bin/activate
```

Instale as dependências do projeto:

```bash
pip install .
```

Agora que o ambiente está configurado, você pode iniciar o servidor Flask. Certifique-se de estar no diretório do projeto e com o ambiente virtual ativado.

```bash
flask --app snapcorrect run
```

## 11. Conclusão

O sistema fornece uma solução eficiente e automatizada para a correção de provas e simulados de múltipla escolha, economizando tempo e minimizando erros. A combinação de visão computacional e aprendizado de máquina oferece uma abordagem robusta e precisa para atender às necessidades de correção em larga escala. O sistema é flexível e pode ser adaptado para diferentes tipos de avaliações de múltipla escolha.
