# Formulário de Inserção Social - Quadriênio 2021-2024

Este é um aplicativo Streamlit para coleta de dados sobre ações de inserção social de programas de pós-graduação no período de 2021-2024.

## Configuração da Persistência de Dados no Streamlit Cloud

Para garantir que os dados submetidos através do formulário sejam salvos corretamente quando o aplicativo estiver hospedado no Streamlit Cloud, siga estas instruções:

### 1. Gerar um Token de Acesso Pessoal (PAT) do GitHub

1. Faça login na sua conta do GitHub
2. Clique na sua foto de perfil no canto superior direito e selecione **Settings**
3. Role para baixo e selecione **Developer settings** no menu lateral
4. Clique em **Personal access tokens** e depois em **Tokens (classic)**
5. Clique em **Generate new token** e selecione **Generate new token (classic)**
6. Dê um nome ao token (ex: "Streamlit Cloud Data Access")
7. Selecione os seguintes escopos:
   - `repo` (acesso completo ao repositório)
8. Clique em **Generate token**
9. **IMPORTANTE**: Copie o token gerado e guarde-o em um local seguro. Você não poderá vê-lo novamente!

### 2. Configurar o Segredo no Streamlit Cloud

1. Faça o deploy do seu aplicativo no Streamlit Cloud
2. No painel do aplicativo no Streamlit Cloud, vá para **App Settings** > **Secrets**
3. Adicione o seguinte segredo no formato TOML:
   ```toml
   github_token = "seu-token-aqui"
   ```
   Substitua "seu-token-aqui" pelo token PAT que você gerou no GitHub

### ⚠️ Avisos de Segurança - IMPORTANTE

- **NUNCA** adicione seu token diretamente no código ou em qualquer arquivo que seja enviado para o GitHub
- O token só deve ser configurado através dos **Secrets** do Streamlit Cloud
- Não imprima ou exiba o token em logs ou na interface do aplicativo
- Considere usar um token com permissões mínimas necessárias (apenas acesso ao repositório específico)
- Revogue o token imediatamente se suspeitar que ele foi comprometido
- Configure o token para expirar após um período de tempo razoável (por exemplo, 90 dias)

### 3. Atualize o Repositório no Código

No arquivo `app.py`, atualize a variável `GITHUB_REPO` com o nome do seu usuário e repositório:

```python
GITHUB_REPO = "seu-usuario/seu-repositorio"
```

Por exemplo, se seu nome de usuário no GitHub é "joao" e o nome do repositório é "formulario-insercao", você deve definir:

```python
GITHUB_REPO = "joao/formulario-insercao"
```

### Como funciona

- Quando o aplicativo está sendo executado localmente, os dados são salvos no arquivo `dados_insercao.json` no seu computador
- Quando o aplicativo está em execução no Streamlit Cloud, os dados são salvos diretamente no arquivo `dados_insercao.json` no seu repositório GitHub
- Se o token do GitHub não estiver configurado corretamente no Streamlit Cloud, o aplicativo exibirá um aviso e tentará usar o armazenamento local (que não persiste no Streamlit Cloud)

## Funcionalidades

- Formulário completo para coleta de dados sobre:
  - Dados do Programa e do Respondente
  - Cursos de Especialização (Lato Sensu)
  - Cursos de Extensão e Atividades de Divulgação
  - Consultorias e Atividades de Assessoria
  - Participação e Coordenação de Redes de Pesquisa
  - Organização e Participação em Eventos Científicos
  - Intervenções para Populações Vulneráveis e Comunidades
  - Atividades em Educação Básica (Escolas)

## Requisitos

- Python 3.x
- Streamlit

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/leomartinsjf/forms.git
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

Para executar o aplicativo:

```bash
streamlit run app.py
```

## Desenvolvimento Local

Para testar a aplicação localmente com persistência de dados:

1. Crie um arquivo `.streamlit/secrets.toml` na raiz do projeto
2. Adicione o seguinte conteúdo ao arquivo:
   ```toml
   github_token = "seu-token-de-teste"
   ```
3. **IMPORTANTE**: Não compartilhe este arquivo ou adicione-o ao controle de versão. O arquivo `.streamlit/secrets.toml` já está incluído no `.gitignore`.

Quando a aplicação é executada localmente:
- Os dados são salvos no arquivo `dados_insercao.json` no seu computador
- O token do GitHub é usado apenas se você estiver testando a integração com o GitHub

## Estrutura do Projeto

- `app.py`: Aplicativo principal Streamlit
- `requirements.txt`: Lista de dependências do projeto
- `README.md`: Este arquivo de documentação 