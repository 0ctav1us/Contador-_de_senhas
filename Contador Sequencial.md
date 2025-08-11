# Contador Sequencial

Um programa de contador sequencial (0-999) com interface gráfica e sincronização via banco de dados.

## Características

- Interface gráfica minimalista e bonita
- Contador de 0 a 999
- Botões +1, -1 e Zerar
- Edição direta clicando no número
- Atalhos de teclado:
  - Seta para cima: incrementa
  - Seta para baixo: decrementa
  - Backspace: zera o contador
- Sincronização automática a cada segundo via banco de dados SQLite
- Múltiplos usuários podem usar o programa simultaneamente

## Como usar

### Opção 1: Executar diretamente com Python
```bash
python3 contador.py
```

### Opção 2: Criar executável (requer PyInstaller)
```bash
# Instalar dependências
pip install pyinstaller

# Criar executável
pyinstaller --onefile --windowed --name="Contador" contador.py

# O executável estará em dist/Contador
```

## Requisitos

- Python 3.6 ou superior
- tkinter (geralmente incluído com Python)
- SQLite3 (incluído com Python)

## Banco de dados

O programa cria automaticamente um arquivo `contador.db` no diretório home do usuário para armazenar o valor do contador.

## Funcionalidades

1. **Interface Gráfica**: Interface limpa e intuitiva
2. **Sincronização**: Atualização automática a cada segundo
3. **Persistência**: O valor é mantido entre execuções
4. **Multi-usuário**: Vários usuários podem usar simultaneamente
5. **Atalhos**: Controle via teclado para maior produtividade

