# Gerenciador de Torneio Suiço Hefestus

Gerenciador de Torneio Suiço para competições de robótica desenvolvido pela Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus

![Logo Coliseu](assets/coliseu.png)

## Descrição

O Torneio Suiço é um sistema de competição em que todos os competidores jogam contra todos os outros competidores. O sistema é utilizado em competições de robótica para garantir que todos os competidores tenham a oportunidade de jogar contra todos os outros competidores, garantindo que o vencedor seja o competidor que obteve o melhor desempenho em relação a todos os outros.

O sistema de competição é dividido em rodadas, em que os competidores são pareados de acordo com o desempenho nas rodadas anteriores. O competidor que obteve o melhor desempenho na rodada anterior joga contra o competidor que obteve o segundo melhor desempenho, o competidor que obteve o terceiro melhor desempenho joga contra o competidor que obteve o quarto melhor desempenho, e assim por diante.

## Instalação

Para instalar o Gerenciador de Torneio Suiço, basta clonar o repositório do projeto e instalar as dependências do projeto:

```bash
git clone https://github.com/HefestusTec/torneio-suico.git
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

O código depende também da biblioteca `Swiss` para a implementação do algoritmo de pareamento do torneio suíço, é uma biblioteca de código aberto, desenvolida por [HannesHaglund](https://github.com/HannesHaglund) sob licença customizada. O código fonte da biblioteca, bem como sua licença pode ser encontrado no repositório [Swiss](https://github.com/HannesHaglund/Swiss).

## Contribuição

Se você deseja contribuir com o desenvolvimento do Gerenciador de Torneio Suiço, fique à vontade para abrir uma issue ou enviar um pull request. Sua contribuição é muito bem-vinda!

## Licença

O Gerenciador de Torneio Suiço é um software de código aberto licenciado sob a licença GPL-3.0. Para mais informações, consulte o arquivo `LICENSE`.

## Contato

Para mais informações sobre o Gerenciador de Torneio Suiço, entre em contato com a Associação de Pesquisa, Desenvolvimento e Tecnologia Hefestus: contato@hefestus.ind.br
