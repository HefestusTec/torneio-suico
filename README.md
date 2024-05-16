# Gerenciador de Torneio Suiço Hefestus

Gerenciador de Torneio Suiço para competições de robótica desenvolvido pela Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus

![Logo Coliseu](assets/coliseu.png)

## Descrição

O Torneio Suiço é um sistema de competição que permite que um grande número de participantes com um número pequeno e determinado de rodadas sem a necessidade de eliminar participantes. Segue o mesmo sistema de contagem de pontos do sistema todos contra todos, conhecido como Round robin, porém com as seguintes regras:

- Número pré-determinado de rodadas.
- Dois participantes não se enfrentam mais que uma vez.
- Na rodada 1: o emparceiramento dos confrontos é feito através do rating ou de sorteio, caso os jogadores não possuam rating.
- Nas demais rodadas: participantes com pontuações iguais são emparceirados.
- Caso não seja possível emparceirar participantes com o mesmo número de pontos o confronto será com o concorrente com pontuação mais próxima possível.

Se o número total de participantes de um torneio for ímpar, um dos participantes acabará desemparelhado, ou seja sem adversário para enfrentar na rodada, recebendo a pontuação equivalente a uma vitória por motivo de adversário ausente, o chamado BYE. Os critérios para definir qual participante do torneio ficará desemparelhado na rodada é:

- Não ter recebido ainda nenhum BYE no torneio;
- Possuir o menor número de pontos;
- Possuir o menor rating;

O critério de desempate implementado é _Buchholz_, onde a soma dos pontos dos adversários de um jogador é calculada. O jogador com a maior soma é considerado o vencedor do desempate.

## Instalação

Para instalar o Gerenciador de Torneio Suiço, basta clonar o repositório do projeto e seu submódulo _swiss_ e instalar as dependências do projeto:

```bash
git clone --recursive https://github.com/HefestusTec/torneio-suico.git
cd torneio-suico
bash setup.sh
```

## Utilização

Para utilizar o Gerenciador de Torneio Suiço, basta executar o script `main.py` e uma interface gráfica será aberta para a configuração do torneio:

```bash
python3 src/main.py
```

## Desenvolvimento

O Gerenciador de Torneio Suiço foi desenvolvido pela Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus. O projeto utiliza a linguagem de programação Python e a biblioteca gráfica GTK para a interface gráfica e é mantido por uma equipe de desenvolvedores voluntários e é de código aberto, sob a licença GPL-3.0.

O código depende também de uma remificação biblioteca `Swiss` para a implementação do algoritmo de pareamento do torneio suíço, é uma biblioteca de código aberto, desenvolida por [HannesHaglund](https://github.com/HannesHaglund) sob licença MIT. O código fonte original da biblioteca, bem como sua licença pode ser encontrado no repositório [Swiss](https://github.com/HannesHaglund/Swiss).

## Contribuição

Se você deseja contribuir com o desenvolvimento do Gerenciador de Torneio Suiço, fique à vontade para abrir uma issue ou enviar um pull request. Sua contribuição é muito bem-vinda!

## Licença

O Gerenciador de Torneio Suiço é um software de código aberto licenciado sob a licença GPL-3.0. Para mais informações, consulte o arquivo `LICENSE`.

## Contato

Para mais informações sobre o Gerenciador de Torneio Suiço, entre em contato com a Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus: contato@hefestus.ind.br
