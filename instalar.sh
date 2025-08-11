#!/bin/bash

echo "=== Instalador do Contador Sequencial ==="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-tk
fi

# Verificar se tkinter está disponível
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando tkinter..."
    sudo apt-get install -y python3-tk
fi

echo "Dependências verificadas!"
echo ""
echo "Para executar o programa:"
echo "  python3 contador.py"
echo ""
echo "Para criar um executável:"
echo "  pip3 install pyinstaller"
echo "  pyinstaller --onefile --windowed --name='Contador' contador.py"
echo ""
echo "Instalação concluída!"

