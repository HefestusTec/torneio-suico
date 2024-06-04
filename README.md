# Gerenciador de Torneio Suiço Hefestus

Gerenciador de Torneio Suiço para competições de robótica desenvolvido pela Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus

![Logo Coliseu](assets/coliseu.png)

## Descrição

O Torneio Suiço é um sistema de competição que permite um grande número de participantes com um número pequeno e determinado de rodadas sem a necessidade de eliminar participantes. Segue o mesmo sistema de contagem de pontos do sistema todos contra todos, conhecido como Round robin, porém com as seguintes regras:

- Número pré-determinado de rodadas.
- Dois participantes não se enfrentam mais que uma vez.
- Na rodada 1: o emparceiramento dos confrontos é feito através do rating ou de sorteio, caso os jogadores não possuam rating. (atualmente essa aplicação não suporta rating)
- Nas demais rodadas: participantes com pontuações iguais são emparceirados.
- Caso não seja possível emparceirar participantes com o mesmo número de pontos o confronto será com o concorrente com pontuação mais próxima possível.

Se o número total de participantes de um torneio for ímpar, um dos participantes acabará desemparelhado, ou seja sem adversário para enfrentar na rodada, recebendo a pontuação equivalente a uma vitória por motivo de adversário ausente, o chamado BYE. Os critérios para definir qual participante do torneio ficará desemparelhado na rodada é:

- Não ter recebido ainda nenhum BYE no torneio;
- Possuir o menor número de pontos;
- Possuir o menor rating;

O critério de desempate implementado é _Buchholz_, onde a soma dos pontos dos adversários de um jogador é calculada. O jogador com a maior soma é considerado o vencedor do desempate.

## Instalação por binário

### Ubuntu

Para instalar o binário basta acessar a aba Releases no GitHub, encontrar a release mais recente, e baixar `Gerenciador.de.Torneio.Suico.Hefestus.Ubuntu.zip`.

Após feito o download, abra o terminal e descompacte a pasta:

```bash
mkdir ~/Gerenciador\ de\ Torneio\ Suico\ Hefestus
unzip ~/Downloads/Gerenciador.de.Torneio.Suico.Hefestus.Ubuntu.zip -d ~/Gerenciador\ de\ Torneio\ Suico\ Hefestus/
```

Após a instalação, basta navegar até a pasta onde os arquivos foram extraídos e dar um duplo-clique em `Gerenciador de Torneio Suiço Hefestus` e a interface de usuário se abrirá. Ou, se preferir, executar via linha de comando:

```bash
~/Gerenciador\ de\ Torneio\ Suico\ Hefestus/Gerenciador\ de\ Torneio\ Suiço\ Hefestus
```

### Windows

Para instalar o binário basta acessar a aba Releases no GitHub, encontrar a release mais recente, e baixar `Gerenciador.de.Torneio.Suico.Hefestus.Windows.zip`.

Após feito o download, navegue até a pasta onde o arquivo se encontra, clique com o botão direito no arquivo e então clique com o botão esquerdo em "Extrair Tudo" e selecione a pasta alvo (recomendado que seja em `Documentos/Gerenciador de Torneio Suiço Hefestus`), então clique com o botão esquerdo em "Extrair".

Após a instalação, basta navegar até a pasta onde os arquivos foram extraídos e dar um duplo-clique em `Gerenciador de Torneio Suiço Hefestus` e a interface de usuário se abrirá.

## Instalação por código fonte

### Ubuntu

Para instalar por código fonte o Gerenciador de Torneio Suiço no Ubuntu, basta clonar o repositório do projeto e seu submódulo _swiss_ e instalar as dependências do projeto:

```bash
git clone --recursive https://github.com/HefestusTec/torneio-suico.git
cd torneio-suico
bash setup.sh
```

### Windows

Para instalar por código fonte o Gerenciador de Torneio Suiço no Windows é necessário instalar [MSYS2](https://www.msys2.org/) seguindo as orientações na página.
Após instalado procure por `MSYS2 UCRT64` no menu Iniciar e execute-o. Após aberto o terminal basta instalar o git, clonar o repositório do projeto e seu submódulo _swiss_ e instalar as dependências do projeto:

```bash
pacman -Suy
pacman -Sy git
git clone --recursive https://github.com/HefestusTec/torneio-suico.git
cd torneio-suico
bash setup_msys.sh
```

## Utilização

Para utilizar o Gerenciador de Torneio Suiço, certifique-se que está na pasta raiz do projeto git, então, basta executar o script `main.py` e uma interface gráfica será aberta para a configuração do torneio:

```bash
python3 src/main.py
```

## Empacotar executável

### Ubuntu

Para criar um executável é necessário instalar o módulo PyInstaller. Abra o terminal e instale o módulo PyInstaller para Python:

```bash
python3 -m pip install pyinstaller
```

Após instalado o módulo, certifique-se que está na pasta raiz do projeto git, então execute o PyInstaller para empacotar a aplicação em um executável:

```bash
pyinstaller src/main.py --onefile --noconsole --icon=assets/coliseu.ico
```

#### Parâmetros
- **src/main.py:** Arquivo de entrada da aplicação.
- **--onefile:** Especifica para o PyInstaller empacotar tudo em um arquivo só.
- **--noconsole:** Especifica para o PyInstaller omitir o console, já que é uma aplicação de interface gráfica
- **--icon=assets/coliseu.ico**: Especifica para o PyInstaller o arquivo a ser utilizado como ícone da aplicação

Após empacotado, o projeto se encontrará no diretório `dist`. Copie o diretório `assets` para `dist`:

```bash
cp -r assets/ dist/
```

Por fim, basta executar `main` e a aplicação iniciará. Sinta-se livre para renomear o diretório `dist/` bem como o executável `main` para um nome que melhor remeta a aplicação.

### Windows

Para criar um executável é necessário instalar é necessário instalar [MSYS2](https://www.msys2.org/) seguindo as orientações na página.
Após instalado procure por `MSYS2 UCRT64` no menu Iniciar e execute-o. Após aberto o terminal instale o módulo PyInstaller para Python:

```bash
python3 -m pip install pyinstaller
```

Após instalado o módulo, certifique-se que está na pasta raiz do projeto git, então execute o PyInstaller para empacotar a aplicação em um executável:

```bash
pyinstaller src/main.py --onefile --noconsole --icon=assets/coliseu.ico
```

#### Parâmetros
- **src/main.py:** Arquivo de entrada da aplicação.
- **--onefile:** Especifica para o PyInstaller empacotar tudo em um arquivo só.
- **--noconsole:** Especifica para o PyInstaller omitir o console, já que é uma aplicação de interface gráfica
- **--icon=assets/coliseu.ico**: Especifica para o PyInstaller o arquivo a ser utilizado como ícone da aplicação

Após empacotado, o projeto se encontrará no diretório `dist`. Copie o diretório `assets` para `dist`:

```bash
cp -r assets/ dist/
```

Por fim, basta executar `main.exe` e a aplicação iniciará. Sinta-se livre para renomear o diretório `dist/` bem como o executável `main.exe` para um nome que melhor remeta a aplicação.

#### Nota

Tanto a versão binária disponível em GitHub quanto a versão empacotada manualmente dessa aplicação é portável (ambos Windows e Ubuntu), ou seja, é possível copiar seu conteúdo para uma mídia removível (como um pendrive) e utilizá-lo em máquinas diferentes desde que seu Sistema Operacional seja o mesmo.

## Desenvolvimento

O Gerenciador de Torneio Suiço foi desenvolvido pela Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus. O projeto utiliza a linguagem de programação Python e a biblioteca gráfica GTK para a interface, é mantido por uma equipe de desenvolvedores voluntários e é de código aberto, sob a licença GPL-3.0.

O código depende também de uma ramificação da biblioteca `Swiss` para a implementação do algoritmo de pareamento do torneio suíço, é uma biblioteca de código aberto, desenvolida por [HannesHaglund](https://github.com/HannesHaglund) sob licença MIT. O código fonte original da biblioteca, bem como sua licença pode ser encontrado no repositório [Swiss](https://github.com/HannesHaglund/Swiss).

## Contribuição

Se você deseja contribuir com o desenvolvimento do Gerenciador de Torneio Suiço, fique à vontade para abrir uma issue ou enviar um pull request. Sua contribuição é muito bem-vinda!

## Licença

O Gerenciador de Torneio Suiço é um software de código aberto licenciado sob a licença GPL-3.0. Para mais informações, consulte o arquivo `LICENSE`.

## Contato

Para mais informações sobre o Gerenciador de Torneio Suiço, entre em contato com a Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus: contato@hefestus.ind.br
