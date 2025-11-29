# Instruções de Instalação no Windows

## Problema Comum: Erro ao Instalar Pandas

Se você receber o erro `subprocess-exited-with-error` ao instalar o pandas, siga estas soluções:

### Solução 1: Atualizar pip e usar wheels pré-compilados (RECOMENDADO)

1. Abra o Prompt de Comando como Administrador
2. Execute os seguintes comandos:

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel
python -m pip install -r requirements.txt
```

### Solução 2: Instalar dependências uma por uma

Se a Solução 1 não funcionar, tente instalar as dependências separadamente:

```bash
pip install PyPDF2==3.0.1
pip install edge-tts==6.1.9
pip install streamlit==1.29.0
pip install pandas
```

### Solução 3: Usar versões específicas compatíveis

Se ainda houver problemas, edite o arquivo `requirements.txt` para:

```
PyPDF2==3.0.1
edge-tts==6.1.9
streamlit==1.29.0
pandas
```

E instale com:

```bash
pip install -r requirements.txt --only-binary :all:
```

O parâmetro `--only-binary :all:` força o pip a usar apenas versões pré-compiladas.

### Solução 4: Instalar Microsoft C++ Build Tools (última opção)

Se nenhuma das soluções acima funcionar, você pode instalar as ferramentas de compilação:

1. Baixe o [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Execute o instalador
3. Selecione "Desktop development with C++"
4. Aguarde a instalação (pode demorar)
5. Reinicie o computador
6. Execute `run.bat` novamente

## Verificar Versão do Python

Certifique-se de que está usando Python 3.9 ou superior:

```bash
python --version
```

## Após a Instalação

Depois que as dependências forem instaladas com sucesso:

1. Execute `run.bat`
2. Aguarde o navegador abrir automaticamente
3. Use a aplicação!

## Problemas Conhecidos

- **Python 3.13+**: Algumas bibliotecas podem não ter wheels disponíveis ainda. Recomendamos Python 3.11 ou 3.12 para melhor compatibilidade no Windows.

## Suporte

Se os problemas persistirem, abra uma issue com:
- Versão do Python (`python --version`)
- Sistema operacional (Windows 10/11)
- Mensagem de erro completa
