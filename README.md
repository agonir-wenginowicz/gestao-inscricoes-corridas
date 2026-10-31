# Gestão de Inscrições em Corridas de Rua

**Sistema web para gerenciamento de inscrições em corridas de rua comunitárias.**

## Sobre o projeto

Este projeto consiste no desenvolvimento de um MVP (*Minimum Viable Product*) voltado à organização de corridas de rua gratuitas e comunitárias.

A solução surgiu da necessidade de melhorar o gerenciamento das inscrições, atualmente realizadas por meio de grupos de WhatsApp, processo que pode dificultar o controle dos participantes, a organização das informações e o acompanhamento dos eventos.

O objetivo é oferecer uma plataforma simples, responsiva e de fácil utilização, permitindo centralizar as corridas disponíveis e suas respectivas inscrições.

## Objetivos

- Facilitar a divulgação de corridas comunitárias.
- Centralizar as informações dos eventos.
- Simplificar o processo de inscrição dos participantes.
- Permitir que o organizador consulte os inscritos por corrida.
- Reduzir o trabalho manual e a dispersão de informações.

## Funcionalidades do MVP

- Cadastro de corridas pelo organizador.
- Consulta de corridas com inscrições abertas.
- Inscrição de participantes em eventos disponíveis.
- Consulta da relação de inscritos por corrida.
- Validação de dados e prevenção de inscrições duplicadas.
- Controle de acesso às funcionalidades administrativas.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Flask | Framework web |
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização |
| JavaScript | Interatividade |
| Bootstrap | Interface responsiva |
| Flask-SQLAlchemy | Integração com banco de dados |
| SQLite | Persistência inicial dos dados |
| Pytest | Testes automatizados |
| Git e GitHub | Versionamento e hospedagem do código |

## Arquitetura

O sistema utiliza uma arquitetura monolítica em camadas, organizada segundo o padrão MVC (*Model-View-Controller*).

- **Model:** representa os dados e as regras de negócio.
- **View:** apresenta as informações e permite a interação dos usuários.
- **Controller:** recebe as solicitações, executa as validações e coordena as operações.
- **Banco de dados:** armazena corridas e inscrições.

Essa organização busca facilitar a manutenção, os testes e a evolução incremental da aplicação.

## Estrutura prevista do projeto

```text
gestao-inscricoes-corridas/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── controllers/
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── tests/
│
├── config.py
├── run.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

*Observação: a estrutura poderá ser ajustada durante o desenvolvimento.*

## Segurança e qualidade

O projeto considera práticas fundamentais de segurança e qualidade de software:

- Validação de dados no cliente e obrigatoriamente no servidor.
- Proteção contra consultas SQL inseguras.
- Escape de conteúdo apresentado nas páginas.
- Controle de acesso às operações administrativas.
- Armazenamento seguro de senhas por meio de hash.
- Proteção de informações sensíveis e variáveis de ambiente.
- Testes das funcionalidades principais.

## Acessibilidade

A interface será desenvolvida considerando boas práticas de acessibilidade, incluindo contraste adequado, identificação clara dos campos, mensagens compreensíveis, navegação consistente e adaptação a diferentes tamanhos de tela.

## Escopo do MVP

A primeira versão prioriza o cadastro de corridas, a consulta de eventos abertos, a realização de inscrições e a visualização dos participantes pelo organizador.

Integração automatizada com WhatsApp, aplicativos nativos para Android e iOS e funcionalidades de pagamento não fazem parte do escopo inicial.

## Como executar o projeto

Após a disponibilização do código, os passos previstos para execução local serão:

1. Clonar o repositório:

```bash
git clone https://github.com/SEU-USUARIO/gestao-inscricoes-corridas.git
```

2. Acessar a pasta:

```bash
cd gestao-inscricoes-corridas
```

3. Criar e ativar um ambiente virtual:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

4. Instalar as dependências:

```bash
pip install -r requirements.txt
```

5. Configurar as variáveis de ambiente conforme o arquivo `.env.example`.

6. Executar a aplicação:

```bash
python run.py
```

*Os comandos e a configuração poderão ser atualizados conforme a implementação efetiva.*

## Contexto acadêmico

Projeto desenvolvido individualmente como atividade prática da disciplina **Projeto de Software**, do curso de Análise e Desenvolvimento de Sistemas (ADS).

A proposta busca aplicar conhecimentos de engenharia de software, levantamento de requisitos, arquitetura, desenvolvimento web, segurança, acessibilidade e validação de protótipos em uma necessidade observada em uma iniciativa esportiva comunitária.

## Status do projeto

**Em desenvolvimento — fase de planejamento e prototipação do MVP.**
