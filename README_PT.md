# zero-to-trade

[中文](README.md) · [English](README_EN.md) · [Español](README_ES.md) · **Português** · [Français](README_FR.md) · [العربية](README_AR.md) · [Русский](README_RU.md) · [Deutsch](README_DE.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Türkçe](README_TR.md) · [Bahasa Indonesia](README_ID.md)

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-306998)

**Sete etapas, de "que país eu escolho" até "o dinheiro chegou." Mais catorze scripts Python que fazem o trabalho chato, e um site com quatro ferramentas que rodam direto no seu navegador. Não se presume nenhuma experiência. É esse o ponto.**

> Você mandou 200 e-mails frios e recebeu zero respostas. Não é o seu inglês. É a ordem das operações.
>
> Este repositório transforma "começar a exportar" em algo em que dá para trabalhar de fato: qual site abrir nesta tarde, o que digitar nele e que resultado significa que você passou.

> A única regra por trás de tudo aqui: **a IA faz o trabalho pesado, você toma as decisões.**

Sem curso para comprar. Sem plano pago. Sem pedir e-mail. Licença MIT, V20.

> PRs são bem-vindos, especialmente de quem vende para um mercado que este repositório nunca ouviu falar. Veja [CONTRIBUTING.md](CONTRIBUTING.md).

Esta versão em português é uma tradução completa do [README_EN.md](README_EN.md), em português brasileiro — o Brasil é um dos mercados-alvo deste projeto (pneus TBR, certificação INMETRO). Os termos comerciais (FOB, CIF, L/C, T/T, D/P) ficam em inglês e são explicados no [GLOSSARY.md](GLOSSARY.md).

---

## O que isto realmente resolve

Pesquise no Google "como começar a exportar". Você encontra a história de sucesso de um cara, duzentos posts de SEO, a prévia grátis de um curso pago e uma miniatura de YouTube prometendo dinheiro rápido. Você lê tudo, se sente informado e, na manhã seguinte, está olhando para um site de dados aduaneiros sem ideia do que colocar no primeiro campo.

Isso não é falta de informação. É informação no formato errado: picada em fragmentos, escrita do ponto de vista do vencedor e parando bem antes da parte em que você faz alguma coisa.

É assim que a maioria dos tutoriais trata o assunto. *"Você deve fazer uma pesquisa de antecedentes dos seus clientes."* Depois: *"A pesquisa de antecedentes é importante."* E nada mais. Você continua sem saber quais campos, quais sites, como é um sinal de alerta ou quando já verificou o suficiente.

Este repositório faz o oposto: **pegar uma tarefa e continuar quebrando-a até virar uma ação.**

| O que um tutorial diz | O que este repositório diz |
|---|---|
| "Faça pesquisa de antecedentes" | Triagem L1, três verificações: o site existe, há quanto tempo a empresa está registrada, as contas nas redes sociais estão vivas. Falhou em uma e o lead está morto. |
| "Qualidade importa mais que quantidade" | 10 leads são ordenados em T0/T1/T2/T3, cada nível com seu próximo passo e seu próprio orçamento de tempo. |
| "Faça acompanhamento" | Dias 1, 3, 5, 7. Um ângulo diferente a cada vez, e o dia 7 termina com uma decisão: empurrar ou descartar. |
| "A IA está mudando o comércio" | Dez scripts Python só com a biblioteca padrão (um deles o motor de cotação, ainda em alfa). `python scripts/lead_score.py examples/leads_example.csv` e você tem a classificação completa em cerca de trinta segundos. |

A mesma informação. Um **tamanho de grão** diferente. Essa é toda a diferença. Cada afirmação aqui tem de sobreviver a uma pergunta: o que eu abro nesta tarde e o que eu digito?

Então não, isto não é motivação. É uma lista de verificação e quinze arquivos de script (quatorze scripts de negócio + um guarda de privacidade).

---

## As sete etapas

Uma cadeia, do início ao fim: escolher um país e terminar com o dinheiro no banco. Um documento por etapa, e cada documento termina com algo que você pode realmente usar.

| Etapa | O que você faz | Resultado |
|---|---|---|
| **01 Escolher um mercado** | Avalie por idioma, demanda e barreira | 1 primeiro mercado + 3 razões para defendê-lo |
| **02 Encontrar leads** | Quatro rotas: dados aduaneiros, redes sociais, busca, feiras | ≥20 leads verificados por dia |
| **03 Avaliar o comprador** | Triagem L1 → padrão L2 → mergulho L3 | Classificação A/B/C; golpistas filtrados |
| **04 Fazer contato** | Separe os leads em T0-T3; use três canais no primeiro contato | Lista por nível + plano de acompanhamento D0/D2/D5 (3 toques em 6 dias) |
| **05 Falar de especificações** | Pedidos pequenos primeiro. O preço é sempre por último | Especificação / quantidade / porto de destino |
| **06 Cotar e negociar** | Disciplina de cotação: cada concessão compra algo em troca | Folha de cotação + escada de concessões + roteiros de conversa |
| **07 Entregar o pedido** | Contrato, produção, inspeção, documentos, pagamento, frete | Ciclo de entrega fechado + plano de recompra |

Os documentos das etapas ficam em `docs/`, um arquivo por etapa, todos seguindo a mesma estrutura de seis partes (veja [CONTRIBUTING.md](CONTRIBUTING.md)): **para que serve esta etapa → como fazer, passo a passo → os critérios de aprovação/reprovação → os erros clássicos → modelos de copiar e colar → os prompts de IA desta etapa.**

**Nunca fez isso antes?** [`docs/00-getting-started.md`](docs/00-getting-started.md) presume que você não sabe git nem Python e coloca você em movimento em cerca de 10 minutos. Com pressa? [`docs/fast-path.md`](docs/fast-path.md) é sete dias do zero até a primeira resposta.

---
## Início rápido em 30 segundos

**Não quer instalar Python?** Abra o site: [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/). São quatro ferramentas no navegador — classificação de leads, primeiro contato, plano de follow-up e cotação — com a interface em 12 idiomas. Cole um CSV e veja a classificação T0-T3. Nada para instalar, e a sua lista não sai do navegador.

São 15 arquivos de script: quatorze scripts de negócio, um deles o motor de cotação, mais um script guarda de privacidade (`check_private_data.py`, verifica se há dados reais de clientes antes de você commitar). Só biblioteca padrão. Python 3.10+.

```bash
# 1. Classifique seus leads. CSV entra, T0-T3 sai, cada nível com seu próximo passo.
python scripts/lead_score.py examples/leads_example.csv

# 2. Escreva a mensagem de contato para um nível, inglês e 中文 lado a lado.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Monte o plano de acompanhamento. Três toques, com datas reais.
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. Cotação: custo + frete + margem -> faixa FOB/CIF + escada de concessões em 3 passos.
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

O que o primeiro comando realmente imprime, com 10 leads de exemplo. A saída do script é em chinês; 【示例】 é só um marcador que significa "exemplo", e a última coluna está traduzida aqui:

| Nível | Empresa | País | Pontuação | Próxima ação |
|---|---|---|---|---|
| T0 | 【示例】Comércio de Pneus do Golfo | Saudi Arabia | 95 | mandar o primeiro contato hoje, sem esperar |
| T0 | 【示例】Pneus Delta | Saudi Arabia | 88 | mandar o primeiro contato hoje, sem esperar |
| T1 | 【示例】Mar Azul de Omã | Oman | 77 | nesta semana; escrever o texto hoje |
| T1 | 【示例】Auto Península | Saudi Arabia | 71 | nesta semana; escrever o texto hoje |
| T1 | 【示例】Comércio Nilo | Egypt | 67 | nesta semana; escrever o texto hoje |
| T1 | 【示例】Rodas Dubai | UAE | 65 | nesta semana; escrever o texto hoje |
| T1 | 【示例】Autopeças Riade | Saudi Arabia | 60 | nesta semana; escrever o texto hoje |
| T2 | 【示例】Pioneira da Nigéria | Nigeria | 46 | lista fria, varrer uma vez por dia |
| T3 | 【示例】Fornecedora Levante | Lebanon | 20 | pouca informação, buscar contato + necessidade primeiro |
| T3 | 【示例】Peças Riade | Saudi Arabia | 10 | pouca informação, buscar contato + necessidade primeiro |

Resumo: **T0:2 / T1:5 / T2:1 / T3:2**. Contato hoje: 【示例】Comércio de Pneus do Golfo, 【示例】Pneus Delta. Nesta semana: 【示例】Mar Azul de Omã, 【示例】Auto Península, 【示例】Comércio Nilo, 【示例】Rodas Dubai, 【示例】Autopeças Riade. Deixar quieto por enquanto: 【示例】Fornecedora Levante, 【示例】Peças Riade.

Cabeçalho do CSV:

```
company,country,product,source,email,phone,years,contact,note
```

Só `company` é obrigatório. Todo o resto pode ficar em branco, e brancos pontuam no mínimo. `source` é o que mais mexe na nota: `referral` / `trade_show` / `customs` / `linkedin` / `search`.

Todos os catorze scripts aceitam `--help`. O `lead_score.py` também tem `--format json` e filtros `--country` / `--product`, caso você queira jogar o resultado numa planilha.

Os scripts só decidem o que uma máquina pode decidir: se há e-mail, se há site, se passa da barra do T0. Se um lead merece a sua tarde, isso está nos documentos — e na sua cabeça.

---

## Estrutura do repositório

```
zero-to-trade/
├── README.md              # Versão completa em chinês
├── README_EN.md           # Versão completa em inglês (a referência)
├── README_ES.md           # Versão em espanhol (starter, buscando revisores)
├── README_PT.md           # Este arquivo: versão completa em português brasileiro
├── README_AR.md           # Versão completa em árabe (RTL)
├── index.html             # O site: 4 ferramentas no navegador, interface em 12 idiomas, zero dependências (GitHub Pages)
├── MANIFESTO.md           # Anonimato, sem curso pago: a posição da marca
├── GITHUB_LAUNCH.md       # Lançamento + lista de divulgação (Topics/About/PR/Show HN)
├── CONTRIBUTING.md        # Como contribuir + convenções de docs e código
├── CHANGELOG.md           # Registro de mudanças: o que mudou a cada vez
├── ROADMAP.md             # Roteiro: para onde vão as versões
├── LICENSE                # MIT
├── docs/                  # Um arquivo por etapa
│   ├── 00-getting-started.md
│   ├── fast-path.md       # 7 dias do zero até a primeira resposta
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md # Um primeiro negócio realista, passo a passo
├── scripts/               # Python executável, só biblioteca padrão
│   ├── lead_score.py      # Classifica leads em T0-T3
│   ├── outreach_gen.py    # Textos de contato por nível (EN/ZH + ES/PT/AR com referência em inglês, V13)
│   ├── followup_plan.py   # Plano de acompanhamento D0/D2/D5 (3 toques em 6 dias)
│   ├── quote_engine.py    # Motor de cotação: faixa FOB/CIF + escada de concessões em 3 passos
│   ├── due_diligence.py   # Agente V11 de verificação: L1/L2/L3 + classificação A/B/C + sinais de alerta
│   ├── tire_pack.py       # Pacote V12 de pneus: medida + mercado → pontos GCC + documentos de desembaraço + notas de mercado
│   ├── landed_cost.py     # Custo em destino, V14: FOB + frete + seguro → CIF, mais imposto + gastos no destino → DDP
│   ├── trade_show.py      # Feiras, V15: expositores coletados na feira → plano de acompanhamento de 24 horas (agradecimento em 2h, pista de cotação em 12h, ligação/WhatsApp em 24h)
│   ├── nudge.py           # Biblioteca de lembretes, V16: D3/D7/D14/D30 × cotado/amostra enviada/preço em negociação → versão curta de WhatsApp + versão longa de e-mail (inglês + chinês)
│   ├── anchor_price.py    # Fixação de preço por âncora da concorrência, V18: faixa de preços da concorrência (dados de alfândega) + seu custo → três níveis CIF agressivo/médio/conservador + lista de verificação de 5 itens
│   ├── fast_path.py     # Rota rápida interativa de 7 dias, V19: --day N mostra as tarefas, --done N marca, --progress resume (alinhada com docs/fast-path.md)
│   ├── fulfillment_checklist.py  # Checklist de cumprimento do pedido: PI → sinal → produção → inspeção → saldo → reserva → alfândega → B/L → documentos → pós-venda, travas de dinheiro em sinal/liberação/envio
│   └── check_private_data.py  # Guarda de privacidade: verifica dados reais de clientes antes do commit
├── examples/
│   ├── leads_example.csv  # Dados de exemplo, prontos para executar
│   └── trade_show_example.csv  # Expositores de exemplo, um por nível de interesse
├── prompts/
│   └── AI_PROMPTS.md      # 40 prompts de copiar e colar (28 principais + 12 avançados), agrupados por etapa
└── assets/                # Capturas de tela, diagramas
```

---
## Por que scripts, e não só um documento de método

A maioria dos repositórios de "IA para negócios" faz a mesma coisa: pega a metodologia, cola num prompt e entrega. Este aqui anda ao contrário. **Disciplina primeiro, ferramentas depois.**

O motivo: **ser bom de prompt não é o mesmo que ser bom de comércio.** A minha aposta é que não faltam palavras para você. Falta um jeito de decidir. Então:

- **As regras são o produto aqui.** T0 recebe um e-mail hoje. T3 fica numa gaveta por três meses. Uma concessão que não compra nada de volta é um presente, não uma negociação. Nenhum modelo toma essas decisões por você.
- **O volume vai para a IA.** Triar 8 leads numa passada, esboçar três níveis de pesquisa de antecedentes para 50 empresas, gerar sete dias de variantes de acompanhamento. Horas de trabalho, quase nenhum julgamento envolvido.
- **Tudo que se repete vira script.** Se a classificação é uma sensação, não é um padrão. Então é um script de menos de 200 linhas, sem dependências, e duas pessoas rodando chegam à mesma resposta.

Onde fica a linha: **dá para ser um `if/else`? Vai para um script. Precisa de uma troca? Vai para os documentos. Tem de soar como se um humano tivesse escrito? Vai para `prompts/`.**

Sem pandas, sem SDK da OpenAI, de propósito. A configuração do ambiente é onde os iniciantes desistem. Alguém novo em exportação vai perder mais horas com `pip install` do que procurando clientes, e esse é um lugar idiota para perder horas.

---

## Roteiro

> Roteiro completo: [ROADMAP.md](ROADMAP.md); histórico de mudanças: [CHANGELOG.md](CHANGELOG.md).

| Versão | Estado | Conteúdo |
|---|---|---|
| **V18** | ✅ Concluída (2026-11-07) | Fixação de preço por âncora da concorrência (`scripts/anchor_price.py`: faixa de preços da concorrência (dados de alfândega) + seu custo → três níveis CIF agressivo/médio/conservador, cada um com margem, rentabilidade, equivalente FOB, recargo implícito e quando usar; lista de verificação de 5 itens — custo, frete, câmbio, condições de pagamento, validade — antes de cotar, qualquer item sem verificação é sinalizado; aviso de baixo custo «abaixo do custo, não feche o pedido, negocie volume por preço primeiro»; sem mediana, estimada como (mínimo + máximo) / 2 e marcada como estimativa; `--format json` / `--audience client`) + `docs/anchor-price.md` (uso + guia de ancoragem + 2 saídas reais coladas palavra por palavra) + uma linha em `docs/06-quote.md` (ancorar antes de cotar) + `tests/` com 187 testes da biblioteca padrão + 40 prompts sem alteração (28 principais + 12 avançados) + 11 arquivos de script |
| **V20** | ✅ Atual (2026-11-14) | Mesclagem dos incrementos locais + 10 rodadas de endurecimento: entradas de CLI unificadas (erros em linguagem clara, códigos de saída alinhados) + testes reforçados (modo de mensagem única, apelido `--start-date`, logs de execução) + números da documentação alinhados + exemplo fora de pneus (8 leads de iluminação LED) + página de demonstração sincronizada com a V19 + erros claros para CSVs ruins (coluna ausente / arquivo vazio / aspas sem fechar não dão mais traceback) + prompts alinhados (o comando de acompanhamento P04-4 ganha `--avoid-weekend`, a janela P10-2 unificada em 48 horas) + rastreamento de execução lançado (`logs/trace-YYYY-MM-DD.jsonl`, uma linha por execução dos três scripts principais) + limpeza de código (funções compartilhadas em um só lugar, −151 linhas líquidas; dois trechos mortos removidos) + `tests/` com 586 testes da biblioteca padrão + 40 prompts sem alteração (28 principais + 12 avançados) + 15 arquivos de script |
| **V19** | ✅ Concluída (2026-11-07) | Rota rápida interativa de 7 dias (`scripts/fast_path.py`: `--day N` mostra as tarefas do dia — nome da tarefa + o que produzir + qual script ou documento usar; `--done N` marca um dia com carimbo de tempo, salvo no JSON de `--state`, repetir o registro avisa que já está marcado e não duplica; `--progress` resume feitos / pendentes / vencidos (vencido = data prevista anterior a hoje e sem marca, data prevista = primeiro dia de `--start` + (N-1) dias; sem `--start` não se contam vencidos, e isso é dito claro; `--list` mostra os 7 dias; tarefas alinhadas linha por linha com `docs/fast-path.md`, sem inventar outra lista; `--help` traz exemplos reais, um dia ou data inválidos dão um erro em linguagem clara) + `docs/fast-path-interactive.md` (uso + formato do arquivo de estado + regra de vencimento + panorama de 7 dias + 2 saídas reais coladas palavra por palavra) + uma linha no topo de `docs/fast-path.md` (entrada interativa) + uma linha em `docs/00-getting-started.md` passo B5 (8 scripts restantes → 9) + `tests/` com 226 testes da biblioteca padrão + 40 prompts sem alteração (28 principais + 12 avançados) + 12 arquivos de script |
| **V17** | ✅ Concluída (2026-11-07) | READMEs completos em português e árabe (novos `README_PT.md` em português brasileiro e `README_AR.md` em árabe com layout RTL, ambos traduzidos por inteiro e alinhados com o README_EN.md: mesmas seções, tabelas, comandos, nomes de scripts, nomes de arquivos, versão e números; todas as empresas, preços e contatos de exemplo são fictícios, marcados com 【示例】 e domínio reservado sample.example) + `tests/` com 167 testes da biblioteca padrão + 40 prompts sem alteração (28 principais + 12 avançados) + 10 arquivos de script |
| **V16** | ✅ Concluída (2026-11-07) | Biblioteca de lembretes (`scripts/nudge.py`: D3/D7/D14/D30 × cotado/amostra enviada/preço em negociação, 12 textos no total, versão curta de WhatsApp + versão longa de e-mail, inglês primeiro com tradução para o chinês depois de cada texto; escada de tom — D3 lembrete leve, D7 perguntar como vai, D14 três opções para salvar a cara (preço mais baixo / outra especificação / prazo de pagamento mais longo), D30 última mensagem sem queimar pontes; o dia 0 é o dia em que a cotação, a amostra ou a conversa de preço saiu, uma âncora diferente da cadência de primeiro contato do followup_plan, um fio segue uma só linha; `--channel whatsapp/email/both` / `--format json` / `--out`) + `docs/nudge.md` (uso + como se encaixa com o followup_plan + 2 saídas reais coladas palavra por palavra) + uma linha em `docs/00-getting-started.md` (lista de scripts 6 → 7) + `tests/` com 152 testes da biblioteca padrão + 40 prompts sem alteração (28 principais + 12 avançados) + 10 arquivos de script |
| **V15** | ✅ Concluída (2026-11-07) | Acompanhamento de feiras (`scripts/trade_show.py`: os expositores coletados na feira, ordenados por interesse num plano de acompanhamento de 24 horas — agradecimento + material em 2 h, pista de cotação em 12 h, ligação/WhatsApp em 24 h; `--add` um a um + `--csv` em lote, `--format json` / `--out`; o primeiro texto segue o modelo T0/T1/T2 do outreach_gen) + `docs/trade-show.md` (uso + 1 saída real colada palavra por palavra) + `examples/trade_show_example.csv` (3 expositores de exemplo, um por nível de interesse) + uma linha em `docs/00-getting-started.md` e outra em `docs/02-find-leads.md` (o que fazer com os contatos depois da feira) + `tests/` com 127 testes + 40 prompts sem alteração (28 principais + 12 avançados) + 9 arquivos de script |
| **V14** | ✅ Concluída (2026-11-07) | Custo em destino (`scripts/landed_cost.py`: FOB + frete + seguro → CIF, mais imposto + gastos no porto de destino → DDP; custo por unidade + totais + margem se houver preço de venda; `--qty` / `--format json` / `--audience client`) + `docs/landed-cost.md` (uso + tabela de fórmulas + 2 saídas reais coladas palavra por palavra) + uma linha em `docs/00-getting-started.md` e outra em `docs/06-quote.md` (primeiro FOB/CIF com o quote_engine, depois o custo total em destino com o landed_cost) + `tests/` com 97 testes + 40 prompts sem alteração (28 principais + 12 avançados) + 8 arquivos de script |
| **V13** | ✅ Concluída (2026-11-07) | Contato multilíngue (`scripts/outreach_gen.py --lang es/pt/ar`: texto em espanhol/português/árabe + original em inglês depois de cada texto; modelos em correspondência um a um com os ingleses T0/T1/T2, um só dicionário dentro do script) + `docs/04-outreach.md` com uma seção nova (uso + 3 saídas reais coladas palavra por palavra) + `tests/` com 80 testes da biblioteca padrão + 40 prompts sem alteração (28 principais + 12 avançados) + 7 arquivos de script |
| **V12** | ✅ Concluída (2026-11-07) | Pacote de pneus (`scripts/tire_pack.py`: medida + mercado → pontos de certificação GCC + documentos de desembaraço no porto de destino + notas do mercado; 4 medidas TBR × 8 mercados) + `docs/tire-pack.md` (uso + 2 saídas reais coladas palavra por palavra) + lista de scripts atualizada em `docs/00-getting-started.md` + `tests/` com 68 testes + 40 prompts (28 principais + 12 avançados) + 7 arquivos de script |
| **V11** | ✅ Concluída (2026-11-07) | Agente de verificação de compradores (`scripts/due_diligence.py`: L1/L2/L3 + classificação A/B/C + lista de alertas + visão do cliente + saída JSON) + seção 13 em `docs/03-due-diligence.md` (saída real colada palavra por palavra) + prompt P03-5 + `tests/` com 52 testes + 40 prompts (28 principais + 12 avançados) + 6 arquivos de script |
| **V10** | ✅ Concluída (2026-11-07) | 6 módulos avançados (08 site próprio / 09 matriz social / 10 feiras / 11 logística e pagamento / 12 risco e conformidade / 13 contas-chave) + 3 rotas de aprendizagem + manual de resolução de problemas e fluxo de colaboração + motor de cotação reforçado (visão do cliente isolada, validação de limites) + `tests/` com 30 testes + 39 prompts (27 principais + 12 avançados) + demo do navegador alinhada com o Python |
| **v0.1.5** | Entregue | Demo no navegador (index.html) + motor de cotação em fase alfa (quote_engine.py) + manifesto de marca (MANIFESTO) + lista de lançamento e divulgação (GITHUB_LAUNCH) + Fast Path + exemplo de venda |
| **v0.1** | Entregue | 7 documentos de etapas, 4 scripts com biblioteca padrão, 27 prompts e README bilíngue |
| **v0.2** | ✅ Concluída (alfa) | **Motor de cotação com IA**: `scripts/quote_engine.py` está no ar — custos de entrada + mercado + preço âncora do concorrente → faixa FOB/CIF + escada de concessões em três passos (cada passo tem de comprar alguma coisa); isolamento da visão do cliente e validações de limite reforçados (veja `tests/test_quote_engine.py`) |
| **Próxima versão** | A decidir | Direção a decidir (a rota rápida interativa de 7 dias chegou na V19) |
| **Longo prazo** | — | Pacotes por indústria (pneus, materiais de construção, máquinas, ferragens); textos de contato em francês e russo (espanhol, português e árabe chegaram na V13); conjuntos públicos de leads sem identificação; ligar o motor de cotação aos dados aduaneiros para ancorar preços da concorrência automaticamente |

A V20 não espera pela próxima versão: as 10 rodadas de endurecimento já podem ser usadas agora (CSVs ruins dão erros em linguagem clara em vez de traceback, cada execução escreve uma linha de rastreamento, as funções compartilhadas vivem em um só lugar). Não precisa esperar a próxima versão — os scripts já estão no repositório, com 586 testes todos verdes.

---
## Como contribuir

O buraco aqui não é de documentos. É de **detalhes de campo de cada país.** Eu sei como vai o primeiro pedido de pneus para o Oriente Médio. Não tenho ideia de como funciona a distribuição de materiais de construção no Equador, nem de quais documentos a alfândega da Nigéria realmente quer. Só quem vende lá pode preencher isso.

Três jeitos de entrar, do mais barato ao mais caro:

1. **Corrigir algo.** Erro de digitação, fato desatualizado, uma regra que soa como mingau. Abra uma issue. Uma frase vale mais que silêncio. O modelo pede três coisas: qual linha te perdeu, qual número não tem fonte, qual regra não se sustenta no seu setor.
2. **Traduzir uma etapa.** Espanhol, árabe, português, russo, francês, vietnamita — o que você realmente fala. Mantenha a estrutura de seis partes, troque o idioma, alinhe os termos com o [GLOSSARY.md](GLOSSARY.md).
3. **Acrescentar seu país ou setor.** Esta é a parte que falta. Escreva o que você já fez, não o que você acha que deveria ser feito. Nomes de campos, nomes de documentos, como o canal é construído, como as pessoas pagam e por que se recusam a pagar.

Código também, com uma regra dura: **Python 3.10+, só biblioteca padrão.** O raciocínio está em [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Para desenvolvedores: dá para mexer, e não tem dependências

Todos os quatorze scripts de negócio (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine` / `due_diligence` / `tire_pack` / `landed_cost` / `trade_show` / `nudge` / `anchor_price` / `fast_path` / `market_rules` / `daily_video_list` / `fulfillment_checklist`, mais o guarda de privacidade `check_private_data.py`) usam só a biblioteca padrão. Não há `pip install`. Faça um fork, mude, jogue nas suas coisas:

- Os pesos parecem errados? Quatro constantes no topo do `lead_score.py` (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`). Continua com teto em 100.
- Tem seus próprios dados aduaneiros? Alinhe o cabeçalho (`company,country,product,source,email,phone,years,contact,note`) e jogue dentro.
- Quer colocar dentro da sua própria ferramenta? Cada script importa de forma limpa. `score_lead()`, `render()`, `plan_followups()`, `build_quote()` são funções puras que devolvem dicionários e listas. Sem rede, sem arquivos escritos.
- O CI roda `py_compile` mais a suíte de testes completa (Python 3.10–3.13) mais um portão de privacidade em cada PR, então uma edição ruim não passa escondida.

> O viés aqui é **verificável acima de esperto.** Não acredite na minha palavra: rode `python scripts/lead_score.py examples/leads_example.csv` e leia o que sai.

---

## Se isto te salvou de um passo errado

Dê uma estrela. No canto superior direito. É só isso que peço. É também como você acha isto de novo daqui a seis meses, quando tiver esquecido o nome e precisar do plano de acompanhamento às 23h.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[Ver o gráfico completo do Star History](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Traduções

O README existe em 12 idiomas, e a interface do site também. A versão em inglês é a referência.

- [中文](README.md) (chinês, completa)
- [English](README_EN.md) (inglês, completa — a referência)
- [Español](README_ES.md) (espanhol, starter, buscando revisores)
- [Português](README_PT.md) (português brasileiro, completa — esta página)
- [Français](README_FR.md) (francês, completa)
- [العربية](README_AR.md) (árabe, completa, RTL)
- [Русский](README_RU.md) (russo, completa)
- [Deutsch](README_DE.md) (alemão, completa)
- [日本語](README_JA.md) (japonês, completa)
- [한국어](README_KO.md) (coreano, completa)
- [Türkçe](README_TR.md) (turco, completa)
- [Bahasa Indonesia](README_ID.md) (indonésio, completa)

Os documentos de etapa em `docs/` ainda estão só em chinês. Traduza qualquer etapa no idioma que você domina; mantenha a estrutura de seis partes e alinhe os termos com o [GLOSSARY.md](GLOSSARY.md). Falantes nativos que possam revisar um README são muito bem-vindos. Veja [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Perguntas frequentes

**Custa dinheiro?**
Não. Código aberto com licença MIT, sem versão paga, sem curso avançado e sem o passo de "deixe seu e-mail para receber o material".

**Não sei nada de Python, dá para usar?**
Dá. Clique duas vezes em `index.html` e veja o resultado da classificação no navegador, sem instalar nada. Só pense em instalar o Python se quiser rodar os scripts; a primeira instalação leva cerca de 20 minutos.

**As empresas de exemplo são reais?**
Não, são todas fictícias. Os nomes das empresas levam o prefixo 【示例】, os domínios de e-mail usam o domínio reservado `sample.example` e os telefones são marcadores de posição. Não tente contatar ninguém a partir delas.

**Garante que eu vou fechar um pedido?**
Não. Isto aqui só resolve o "não sei qual é o próximo passo". Produto, momento do mercado, sorte — essas três coisas eu não posso dar.

**Os scripts mandam os meus dados de clientes para algum lugar?**
Não. Os 15 scripts só usam a biblioteca padrão e não acessam a rede; os 14 scripts de negócio não escrevem arquivos de negócio (a menos que você mesmo passe `--out`), e três deles — `lead_score` / `outreach_gen` / `followup_plan` — registram uma linha de execução em `logs/` (só hora, parâmetros e resumo do resultado, sem dados de clientes); o script de verificação de privacidade só lê, não escreve. O CSV que você alimenta fica só na sua máquina.

**Não trabalho com pneus, serve para mim?**
O fluxo serve, os detalhes do setor você mesmo completa. O esqueleto das 7 etapas é genérico, mas nomes de documentos, estrutura de canais e hábitos de pagamento mudam de setor para setor — e essa é justamente a parte em que mais espero PRs.

---

## Licença

[MIT](LICENSE) © 2026 zero-to-trade contributors

Use, mude, venda com isto. Mantenha a linha de crédito. Uma ressalva: nada disto garante que você vai fechar um negócio. O que garante é que você não vai travar só porque não sabia qual era o próximo passo.

---

## Perguntas e contribuições

**Abra uma issue: https://github.com/6hn68/zero-to-trade/issues**

Tem algo errado aqui? Diga — isso já conta como contribuição. Vende para um mercado que este repositório nunca ouviu falar? Esse é o PR que eu realmente quero. Acha que o método inteiro está errado? Discuta comigo numa issue; prefiro estar errado em voz alta.

Sem biografia do autor, de propósito. **O conteúdo é que deve convencer você, não quem o escreveu.** Precisa falar comigo: mencione o mantenedor (@) numa issue ou deixe uma mensagem pelo formulário no fim do site. De um jeito ou de outro, chega ao autor.
