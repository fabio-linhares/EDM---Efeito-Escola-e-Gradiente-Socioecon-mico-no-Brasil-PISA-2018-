# README - Efeito Escola e Gradiente Socioeconômico no Brasil

<p align="center">
  <img src="https://ufal.br/ufal/comunicacao/identidade-visual/brasao/ods/ufal_ods1.png" alt="Logo da UFAL" width="600"/>
</p>

<h1 align="center">Efeito Escola e Gradiente Socioeconômico no Brasil</h1>
<h3 align="center">Quantificando o Papel da Gestão e do Clima Escolar na Equidade Educacional</h3>
<h4 align="center">Análise dos Microdados PISA 2018 via Mineração de Dados Educacionais (EDM)</h4>

<p align="center">
  <strong>Universidade Federal de Alagoas (UFAL)</strong><br>
  Programa de Pós-Graduação em Informática (Mestrado)<br>
  Disciplina: Inteligência Artificial Aplicada à Educação<br><br>
  <strong>Autor:</strong> Fábio Linhares<br>
  <strong>Orientador:</strong> Prof. Dr. Ig Ibert Bittencourt Santana Pinto<br>
  <strong>Ano:</strong> 2025
</p>

---

## 📋 Índice

- [Resumo Executivo](#-resumo-executivo)
- [Contexto e Motivação](#-contexto-e-motivação)
- [Objetivos e Perguntas de Pesquisa](#-objetivos-e-perguntas-de-pesquisa)
- [Fundamentação Teórica](#-fundamentação-teórica)
- [Metodologia](#-metodologia)
- [Dados](#-dados)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Instalação e Requisitos](#-instalação-e-requisitos)
- [Como Executar](#-como-executar)
- [Resultados Esperados](#-resultados-esperados)
- [Referências](#-referências)
- [Licença e Citação](#-licença-e-citação)

---

## 🎯 Resumo Executivo

Este projeto de Mineração de Dados Educacionais (EDM) investiga o **"efeito escola"** no Brasil, utilizando os microdados do **PISA 2018**. O objetivo é quantificar quanto da variância no desempenho em Leitura, Matemática e Ciências de estudantes brasileiros se deve a diferenças **entre escolas** (ICC - Intraclass Correlation Coefficient) e testar se condições de **gestão escolar** e **clima institucional** podem **moderar o gradiente socioeconômico** (relação entre ESCS - Economic, Social and Cultural Status - e notas), promovendo maior equidade educacional.

### Principais Questões

1. **Q1:** Quanto da variância nas proficiências está entre escolas vs. dentro de escolas?
2. **Q2:** O ESCS médio da escola (composição socioeconômica) tem efeito além do ESCS individual?
3. **Q3:** Escolas com melhor gestão/clima apresentam gradientes socioeconômicos mais planos (menos desigualdade)?

### Hipóteses Testáveis

- **H1 (Equidade):** Melhor clima disciplinar e gestão instrucional → gradiente ESCS menos íngreme (mais equitativo)
- **H2 (Desempenho):** Mesmas condições → médias escolares mais altas, controlando composição socioeconômica
- **H3 (Variância):** Inclusão de gestão/clima → redução do ICC (parcela governável da variância entre escolas)

### Abordagem Metodológica

- **Modelos multinível** (aluno *i* em escola *j*) com intercepto e slope aleatórios
- **Pesos amostrais** (SENWT) para inferência populacional
- **Análise de interações** ESCS × fatores escolares (EDUSHORT, STUBEHA, TEACHBEHA)
- **Sensibilidade:** Matemática e Ciências como robustez; variação de controles

---

## 🌍 Contexto e Motivação

### O PISA como Ferramenta de Diagnóstico

O **Programme for International Student Assessment (PISA)**, coordenado pela OCDE desde 2000, avalia competências de estudantes de 15 anos em Leitura, Matemática e Ciências. No Brasil, o INEP coordena a aplicação desde o primeiro ciclo. O PISA 2018 avaliou **10.691 estudantes** em **597 escolas** brasileiras.

A escolha deste tema de pesquisa foi motivada pelo fenômeno do **"PISA Shock"** ocorrido na Alemanha após a divulgação dos primeiros resultados em 2001. Até então considerado um modelo educacional de excelência, o país foi surpreendido ao descobrir que seus estudantes apresentavam desempenho mediano e, mais preocupante, **alto nível de desigualdade educacional** associado ao background socioeconômico dos alunos.

O impacto dessa revelação desencadeou uma profunda **reforma no sistema educacional alemão**, com:

- Ampliação da educação infantil (especialmente para famílias desfavorecidas)
- Implementação de avaliações padronizadas nacionais
- Foco em competências práticas (não apenas conteúdos acadêmicos)
- Investimento em formação continuada de professores
- Programas de apoio a escolas em contextos vulneráveis

Ao longo dos ciclos seguintes (2006-2015), a Alemanha conseguiu **reduzir significativamente as desigualdades** e melhorar o desempenho médio, demonstrando que **políticas baseadas em evidência** podem transformar sistemas educacionais.

**Para o Brasil**, esse exemplo histórico é particularmente relevante: assim como a Alemanha em 2001, o país enfrenta o desafio de **alto desempenho desigual**, com forte dependência entre origem socioeconômica e resultados educacionais. Este projeto busca, portanto, **quantificar fatores escolares modificáveis** (gestão, clima, práticas pedagógicas) que possam orientar políticas públicas rumo a um sistema mais **equitativo e eficaz**.

### Desigualdades Educacionais no Brasil

O desempenho educacional brasileiro é marcado por **forte desigualdade**:

- **Territorial:** Sul e Sudeste superam Norte e Nordeste
- **Socioeconômica:** Forte correlação entre ESCS e desempenho
- **Entre redes:** Escolas privadas e técnicas públicas atingem excelência; redes públicas típicas ficam próximas da média nacional

### Evidências do PISA para Escolas (2019)

Estudo da Fundação Cesgranrio mostrou:

- Redes privadas: acima da média PISA 2018
- Redes públicas típicas: próximas da média brasileira
- Redes técnicas públicas: patamar Coreia do Sul/Japão

**Variabilidade explicada por:** composição socioeconômica, práticas pedagógicas, clima disciplinar.

### Por que "Efeito Escola" Importa?

Enquanto o **ESCS** é um fator extraescolar (família), **gestão e clima** são **governáveis** por políticas públicas. Se escolas conseguem **"achatar" o gradiente socioeconômico**, isso significa que **a educação está cumprindo seu papel compensatório**, reduzindo desigualdades de origem.

---

## 🎯 Objetivos e Perguntas de Pesquisa

### Objetivo Geral

Quantificar o efeito escola no Brasil (PISA 2018) e investigar se condições de gestão escolar e clima institucional moderam a relação entre status socioeconômico (ESCS) e desempenho em Leitura, Matemática e Ciências, contribuindo para maior equidade educacional.

### Objetivos Específicos

1. **Estimar o ICC** (Intraclass Correlation Coefficient) para os três domínios no Brasil
2. **Testar efeito contextual** do ESCS médio da escola (composição) além do ESCS individual
3. **Modelar interações** ESCS × gestão/clima para identificar escolas que "achatam" gradientes
4. **Comparar perfis de escola** (pública vs. privada; urbana vs. rural) quanto à equidade
5. **Propor indicadores** de escolas eficazes e equitativas para orientar políticas

### Perguntas de Pesquisa

| ID | Pergunta | Análise | Hipótese |
|----|----------|---------|----------|
| **Q1** | Quanto da variância nas proficiências está **entre escolas**? | Modelo nulo (ICC) | ICC ~25-35% (típico em países desiguais) |
| **Q2** | ESCS médio da escola tem efeito **além** do ESCS individual? | Modelo com ESCS_mean | γ(ESCS_mean) > 0 e significativo (efeito composição) |
| **Q3** | Gestão/clima **moderam** o gradiente socioeconômico? | Modelo com interações ESCS × STUBEHA, etc. | γ₁₁ < 0 (melhor clima → gradiente mais plano) |

---

## 📚 Fundamentação Teórica

### 1. Conceitos-Chave

#### Efeito Escola

- **Definição:** Parcela da variância do desempenho explicada por diferenças **entre escolas**
- **Métrica:** ICC (Intraclass Correlation Coefficient) em modelos multinível
- **Interpretação:** ICC = 0,30 → 30% da variância está entre escolas; 70% dentro de escolas

#### Gradiente Socioeconômico

- **Definição:** Inclinação da reta que relaciona ESCS (nível socioeconômico) a notas
- **Sistemas equitativos:** Gradiente plano (ESCS explica pouco)
- **Sistemas desiguais:** Gradiente íngreme (forte dependência do background familiar)

#### ESCS (Economic, Social and Cultural Status)

A variável `ESCS` é um índice sintético que resume a posição socioeconômica, cultural e educacional da família. Ela é construída pela OCDE a partir de modelos de Teoria de Resposta ao Item, combinando informação sobre escolaridade e ocupação dos pais, recursos culturais no domicílio, bens, livros e outros indicadores em uma única medida contínua. Trata-se de um índice do tipo WLE (Estimativa de verossimilhança ponderada), calculado com base no procedimento descrito no [PISA 2018 Technical Report](https://www.oecd.org/pisa/data/pisa2018technicalreport/) (capítulo de Scaling Procedures), aplicado tanto às proficiências quanto aos índices derivados dos questionários.

**Componentes:**
- Ocupação parental (HISEI - International Socio-Economic Index)
- Educação parental (PAREDINT, HISCED)
- Posses domésticas (HOMEPOS - livros, arte, bens materiais)
- Recursos educacionais (HEDRES - mesa, computador, internet)
- Recursos de TIC (ICTRES)

No banco oficial do PISA, o `ESCS` já é divulgado em uma escala padronizada com média aproximada igual a 0 e desvio-padrão aproximado igual a 1. Para fins de armazenamento nos arquivos, a OCDE aplica uma transformação linear: o valor publicado é dado por `valor_no_arquivo = (valor_original + 5) × 1000`. Assim, um `ESCS` verdadeiro de `−0,103` aparece como `4897`, enquanto um valor de `+1,2` aparece como `6200`. Por conta disso, nós revertemos esse deslocamento para recuperar a escala oficial aplicando `ESCS = valor_no_arquivo / 1000 - 5`. Só para deixar claro, os fatores 5 e 1000 não são escolhas arbitrárias deste estudo, mas a inversão exata da codificação adotada pela OCDE, também utilizada para outros índices como `DISCLIMA`, `JOYREAD` e `SCREADCOMP` (documentados no [PISA 2018 Database – Codebook e Data Analysis Manual](https://www.oecd.org/pisa/data/2018database/)).

Em termos substantivos, valores mais altos de `ESCS` indicam famílias com maior capital socioeconômico. Neste estudo, tratamo-lo como eixo do gradiente socioeconômico e o coeficiente associado a ele indica como a proficiência varia em função da origem social do estudante, servindo de referência para quantificar desigualdades educacionais associadas ao contexto socioeconômico.

### 2. Literatura de Eficácia Escolar

#### Teoria dos Cinco Fatores (Edmonds, 1979)

Escolas eficazes apresentam:

1. Liderança pedagógica forte
2. Clima seguro e ordenado
3. Altas expectativas para todos
4. Monitoramento do progresso
5. Foco no ensino de habilidades básicas

#### Modelo de Creemers & Kyriakides (2008)

- **Nível do aluno:** Background, motivação, oportunidades de aprendizagem
- **Nível da sala:** Práticas de ensino, clima, gestão do tempo
- **Nível da escola:** Liderança, políticas de ensino, clima institucional
- **Nível do sistema:** Políticas nacionais, currículo, accountability

#### Evidências do PISA 2018 - Volume V (OECD, 2020)

Fatores escolares associados a melhor desempenho e equidade:

- **Clima disciplinar** (STUBEHA baixo)
- **Autonomia pedagógica** com accountability
- **Desenvolvimento profissional docente**
- **Recursos adequados** (não excesso)
- **Liderança instrucional** (foco em ensino/aprendizagem)

### 3. Desigualdade Educacional no Brasil

#### Alves & Soares (2007) - Eficácia das Escolas Públicas Brasileiras

- ICC no Brasil (Saeb) ~40-50% (entre escolas)
- Forte efeito composição (NSE médio da escola)
- Escolas eficazes: superam predição do NSE médio

#### Ernica, Rodrigues & Soares (2025) - Desigualdades Contemporâneas

- Segregação escolar crescente em metrópoles
- Efeito-escola menor que efeito-composição
- Políticas de redistribuição de alunos podem ser mais eficazes que melhorias intra-escola

#### Neuman (2022) - Clusters de Desigualdade no PISA

- Países se agrupam em perfis: alto desempenho/baixa desigualdade vs. baixo desempenho/alta desigualdade
- Brasil: cluster de desempenho médio-baixo com alta desigualdade intra-país

---

## ⚙️ Metodologia

> **Nota sobre EDM e IA:** Este projeto se enquadra em **Mineração de Dados Educacionais** porque combina ingestão de múltiplas fontes (STU/FLT/SCH), tratamento sistemático de dados (reescalonamento, imputação, agregação ponderada) e aplicação de modelos para responder perguntas educacionais. Optamos por técnicas estatísticas clássicas (WLS e modelos multinível) em vez de algoritmos de machine learning “black-box”. Essa abordagem é comum na literatura de EDM quando o foco é estimar efeitos e interpretar mecanismos (efeito escola, gradiente socioeconômico) com transparência e rigor inferencial.

### 1. Desenho do Estudo

- **Tipo:** Observacional transversal com dados secundários
- **População:** Estudantes brasileiros de 15 anos (PISA 2018)
- **Amostra:** 10.691 alunos em 597 escolas
- **Desenho amostral:** Probabilístico estratificado por escola

### 2. Pipeline de Preparação e Engenharia

1. **Ingestão e saneamento de IDs**
   - Carregamos `STU_BRA`, `FLT_BRA` e `SCH_BRA` diretamente da pasta `pisa2018/`.
   - Ajustamos `CNTSTUID` em `FLT_BRA` (a OCDE adiciona +50 000 para diferenciação) para permitir `merge` `one_to_one` com `STU_BRA`.
2. **Reversão das escalas WLE**
   - Índices como `ESCS`, `DISCLIMA`, `JOYREAD` e `SCREADCOMP` são armazenados como `(valor_real + 5) × 1000`. Aplicamos a transformação inversa para recuperar a métrica original (média 0, DP ≈ 1).
3. **Codificação de variáveis categóricas**
   - `ST004D01T` → `gender_male` (0 = menina, 1 = menino).
   - `REPEAT` → `repeat_flag` (0 = não repetiu, 1 = repetiu, 2 = sem informação, preservando a categoria “missing” para análises posteriores).
4. **Tratamento de ausentes**
   - Aplicamos `IterativeImputer` (20 iterações, amostragem posterior) em `ESCS`, `DISCLIMA`, `JOYREAD`, `SCREADCOMP` e `BELONG`, usando como preditores `READ`, `SENWT`, `gender_male`, `repeat_flag` e identificadores de escola.
5. **Agregação ponderada por escola**
   - Construímos `school_profile` com médias ponderadas (`estat.wavg`) para `READ`, `MATH`, `SCIENCE`, `ESCS`, `DISCLIMA`, `BELONG`, além de `n_students`.
   - Esses agregados foram anexados ao nível aluno (`students_final`) para permitir interações `ESCS × clima_escola` nos modelos.
6. **Datasets finais**
   - `students_imp`: base nivel aluno após imputação.
   - `students_final`: base analítica com variáveis individuais + agregados de escola (usada nas tarefas T1–T4 e no painel multidisciplinar).

Scripts auxiliares e artefatos relevantes:

| Artefato | Propósito |
|----------|-----------|
| `projeto_pisa_edm.ipynb` | Notebook principal com todo o pipeline descrito acima |
| `outputs/weighted_summary.csv` | Estatísticas descritivas ponderadas (médias, quantis) |
| `outputs/quartil_summary.csv` | Médias ponderadas por quartil de `ESCS` para READ/MATH/SCIENCE |

### 3. Variáveis

#### Nível do Aluno (Level 1)

| Tipo | Variável | Descrição | Fonte |
|------|----------|-----------|-------|
| **Desfecho** | READ, MATH, SCIE | Escores em Leitura, Matemática e Ciências (escala PISA) | STU_BRA |
| **Preditor principal** | ESCS | Índice socioeconômico e cultural (padronizado) | STU_BRA |
| **Clima e pertencimento** | BELONG | Sentimento de pertencimento à comunidade escolar | STU_BRA |
| | DISCLIMA | Clima disciplinar percebido | STU_BRA |
| | JOYREAD | Prazer declarado em ler | STU_BRA/FLT_BRA |
| | SCREADCOMP | Autoeficácia na leitura | STU_BRA/FLT_BRA |
| **Controles** | ST004D01T | Gênero (1=Fem, 2=Masc) | STU_BRA |
| | REPEAT | Repetência (histórico) | STU_BRA |
| | ST022Q01TA | Língua em casa = língua do teste? | STU_BRA |
| | ST019AQ01TA | Status de imigração | STU_BRA |
| **Peso** | SENWT | Peso amostral final (Senate Weight) | STU_BRA/FLT_BRA |

**Explicações adicionais sobre variáveis do nível aluno:**

**`BELONG`** (sentimento de pertencimento) captura o grau em que o estudante se sente parte da comunidade escolar. Algumas fontes pesquisadas sugerem que maior senso de pertencimento se associa a maior engajamento e, em média, a melhores resultados. Nesse contexto, avaliamos `BELONG` ao lado de `ESCS` e das proficiências, uma vez que parece plausível que um alto pertencimento atenue o efeito negativo de origens socioeconômicas desfavorecidas ao longo do gradiente. Um estudante de baixo `ESCS`, mas com forte vínculo com a escola, pode apresentar desempenho acima do esperado.

**`DISCLIMA`** mede a percepção de disciplina na sala de aula, outro fator que pode moderar o gradiente socioeconômico.

**`JOYREAD`** representa o prazer declarado em ler, enquanto **`SCREADCOMP`** mede a autoeficácia na leitura (confiança do estudante em sua capacidade de compreender textos). Ambos são utilizados para investigar se motivação e autopercepção moderam o gradiente socioeconômico: níveis altos de motivação e confiança podem amenizar o gradiente, enquanto baixa autoeficácia pode amplificar desigualdades. Assim como `ESCS` e `DISCLIMA`, esses índices são WLE armazenados com a mesma transformação `(valor + 5) × 1000` e revertidos da mesma forma.

Os controles de gênero (**`ST004D01T`**) e de histórico de repetência (**`REPEAT`**) foram incluídos para tentar separar o efeito do `ESCS` de outras características associadas ao desempenho. Cremos que possa haver, entre meninos e meninas, padrões distintos de proficiência, e como, popularmente, a repetência costuma estar associada a escores mais baixos, ao condicionarmo-nos ao modelo, pretendemos estimar um efeito condicional do `ESCS`, reduzindo a contaminação por fatores não diretamente socioeconômicos. Reconhecemos, porém, que `REPEAT` pode ser, em parte, consequência do próprio `ESCS`; logo, esse controle tende a subestimar o efeito total do contexto socioeconômico, o que deve ser levado em conta na interpretação.

**`SENWT`** (*Student Final Weight*) é o peso final do estudante, utilizado como fator de expansão. Como escolas e alunos são amostrados com probabilidades distintas, aplicar `SENWT` em médias, regressões e modelos garante que os resultados reflitam a população nacional de estudantes de 15 anos, e não apenas a amostra observada.

#### Nível da Escola (Level 2)

| Tipo | Variável | Descrição | Interpretação |
|------|----------|-----------|---------------|
| **Composição** | ESCS_mean | ESCS médio da escola | Efeito contextual/pares |
| **Gestão** | EDUSHORT | Escassez de material educacional (WLE) | Maior = mais escassez |
| | STAFFSHORT | Escassez de pessoal educacional (WLE) | Maior = mais escassez |
| | STRATIO | Razão aluno/professor | Maior = mais alunos por prof |
| | PROATCE | Proporção professores certificados | Maior = melhor qualificação |
| **Clima** | STUBEHA | Comportamento aluno atrapalha aprendizagem (WLE) | Maior = pior clima |
| | TEACHBEHA | Comportamento professor atrapalha (WLE) | Maior = pior clima |
| **Financiamento** | SC016Q01TA | % receita de fontes governamentais | SCH_BRA |
| | SC016Q02TA | % receita de contribuições privadas | SCH_BRA |
| **Controles** | SCHLTYPE (SC013Q01TA) | Tipo de escola (1=Pública, 2=Privada) | SCH_BRA |
| | SCHSIZE | Tamanho da escola (nº alunos) | SCH_BRA |
| | SC001Q01TA | Localização (1=Vila...5=Metrópole) | SCH_BRA |

**Explicações adicionais sobre variáveis do nível escola:**

Os índices **`EDUSHORT`** e **`STAFFSHORT`** são construídos a partir das respostas dos diretores sobre escassez de materiais pedagógicos e de pessoal qualificado. Os valores originais variam de 1 a 119; ao reescalonarmos (`/10 - 5`), recuperamos uma escala aproximadamente centrada em zero que facilita a interpretação, em que valores positivos indicam maior escassez que a média da OCDE e valores negativos indicam menor escassez.

As variáveis **`SC016Q01TA`** e **`SC016Q02TA`** (entre outros itens da série `SC016Q0*`) expressam os percentuais da receita escolar provenientes de fontes governamentais e de contribuições privadas (famílias, doadores, patrocínios), permitindo caracterizar a composição financeira do ambiente escolar.

Esses indicadores são vinculados aos alunos via `CNTSCHID`, o que possibilita testar se condições objetivas de recursos e financiamento moderam a inclinação do gradiente socioeconômico e quantificar quanto da variância entre escolas (efeito escola) está associada a fatores mensuráveis de gestão e infraestrutura.

### 3. Modelos Estatísticos

#### Sequência de Modelos Multinível

##### Modelo M0 (Nulo - ICC)

```
READ_ij = γ₀₀ + u₀ⱼ + εᵢⱼ
ICC = σ²(u₀ⱼ) / [σ²(u₀ⱼ) + σ²(εᵢⱼ)]
```

**Objetivo:** Estimar variância entre escolas (responde Q1)

##### Modelo M1 (ESCS Individual)

```
READ_ij = γ₀₀ + γ₁₀·ESCS_ij + γ₂₀·Gênero_ij + u₀ⱼ + εᵢⱼ
```

**Objetivo:** Estimar gradiente socioeconômico médio

##### Modelo M2 (Efeito Contextual)

```
READ_ij = γ₀₀ + γ₁₀·ESCS_centered_ij + γ₀₁·ESCS_mean_j + controles + u₀ⱼ + εᵢⱼ
onde:
  ESCS_centered_ij = ESCS_ij - ESCS_mean_j  (within-school)
  ESCS_mean_j = média do ESCS na escola j   (between-school)
```

**Objetivo:** Separar efeito individual de efeito composição (responde Q2)

##### Modelo M3 (Gestão e Clima - Efeitos Principais)

```
READ_ij = γ₀₀ + γ₁₀·ESCS_centered_ij + γ₀₁·ESCS_mean_j 
        + γ₀₂·EDUSHORT_j + γ₀₃·STUBEHA_j + γ₀₄·TEACHBEHA_j
        + controles + u₀ⱼ + εᵢⱼ
```

**Objetivo:** Testar se gestão/clima explicam variância entre escolas

##### Modelo M4 (Interações - MODELO PRINCIPAL)

```
READ_ij = γ₀₀ + γ₁₀·ESCS_centered_ij + γ₀₁·ESCS_mean_j 
        + γ₀₂·EDUSHORT_j + γ₀₃·STUBEHA_j
        + γ₁₁·(ESCS_centered_ij × EDUSHORT_j)
        + γ₁₂·(ESCS_centered_ij × STUBEHA_j)
        + controles + u₀ⱼ + u₁ⱼ·ESCS_centered_ij + εᵢⱼ
```

**Objetivo:** Testar se gestão/clima **moderam** gradiente (responde Q3)

**Interpretação-chave:**

- **γ₁₂ < 0:** Melhor clima (STUBEHA baixo) → gradiente mais plano (mais equidade)
- **γ₁₁ < 0:** Mais recursos (EDUSHORT baixo) → gradiente mais plano

### 4. Tratamento de Dados

#### Preparação

1. **Merge:** STU_BRA + FLT_BRA + SCH_BRA
2. **Agregação:** Criar ESCS_mean, ESCS_sd, n_students por escola
3. **Centralização:** ESCS_centered = ESCS - ESCS_mean (within-school)
4. **Missings:**
   - Exclusão listwise: READ, MATH, SCIE, ESCS, CNTSCHID (variáveis críticas)
   - Imputação mediana: Variáveis de escola (EDUSHORT, STUBEHA)
   - Dummy de missing: Sinalizar imputação
5. **Padronização (opcional):** Z-scores de variáveis de escola para comparar magnitudes

#### Pesos Amostrais

- **SENWT:** Peso final do estudante (corrige probabilidade desigual de seleção)
- **Aplicação:** Em todos os modelos e estatísticas descritivas
- **Limitação:** Pesos replicados (W_FSTR1-80) para BRR-Fay não disponíveis nos .xlsx

### 5. Software e Implementação

- **Linguagem:** Python 3.11+
- **Análise multinível:** `statsmodels.MixedLM`
- **Manipulação de dados:** `pandas`, `numpy`
- **Visualização:** `matplotlib`, `seaborn`
- **Notebook:** Jupyter (pesquisa.ipynb)

---

## 📊 Dados

### Fonte

**PISA 2018** - Programme for International Student Assessment (OCDE)

- **Download:** [OECD PISA Database](https://www.oecd.org/pisa/data/2018database/)
- **Documentação:** `PISA2018_CODEBOOK.xlsx`
- **País:** Brasil (CNTRYID = 76)

### Estrutura dos Dados

Antes de selecionar qualquer variável, examinamos a base de dados e separamos o conteúdo das principais planilhas brasileiras do PISA 2018. O fluxo deste projeto se ancora em três delas: `STU_BRA.xlsx`, `FLT_BRA.xlsx` e `SCH_BRA.xlsx`, cada um representando um nível analítico distinto (aluno, desempenho e escola). A tabela abaixo resume o que encontramos:

| Arquivo | Nível | Nº colunas | Variáveis-chave para o projeto |
|---------|-------|------------|--------------------------------|
| `STU_BRA.xlsx` | Aluno | 852 | Proficiências consolidadas `READ`, `MATH`, `SCIE` (com erros padrão), `ESCS`, `SENWT`, controles `ST004D01T`, `REPEAT`, clima e atitudes `DISCLIMA`, `BELONG`, `JOYREAD`, `SCREADCOMP`. |
| `FLT_BRA.xlsx` | Escalas <span title="No PISA, 'escala cognitiva/psicométrica' é basicamente a 'régua invisível' com que a OCDE mede a proficiência dos estudantes em leitura, matemática e ciências. Ela não é uma nota bruta (tipo 28 acertos de 50), mas um continuum latente de habilidade, construído com teoria de resposta ao item (TRI/IRT).">cognitivas/psicométricas</span> | 848 | `READ`, `MATH`, `READ.SE`, `MATH.SE`, índices motivacionais. **Não** há valores plausíveis `PV?READ`, `PV?MATH`, `PV?SCIE` nesta extração; os escores já vêm sintetizados. O identificador `CNTSTUID` aparece deslocado em +50 000. |
| `SCH_BRA.xlsx` | Escola | 208 | Indicadores de gestão/clima `SC016Q0*`, `SC013Q01TA`, escassez de recursos `EDUSHORT`, `STAFFSHORT` e demais variáveis respondidas pelos diretores, todos vinculados por `CNTSCHID`. |

Essa inspeção evita pressupostos equivocados (por exemplo, esperar `PV1READ`–`PV10READ` onde eles não existem) e nos guia na escolha das colunas que realmente contribuem para analisar leitura, matemática e ciências.

### `STU_BRA.xlsx`: nível aluno

Esta tabela contém os identificadores dos alunos (`CNTSTUID`) e das escolas (`CNTSCHID`), além de variáveis que descrevem o perfil socioeconômico, desempenho e atitudes dos estudantes:

#### Proficiências

`READ`, `MATH` e `SCIE` representam as proficiências em leitura, matemática e ciências, respectivamente. Esses escores já estão em escala PISA (média OCDE ≈ 500, desvio-padrão ≈ 100), comparável entre alunos e escolas. Utilizamos essas variáveis como dependentes por serem medidas padronizadas alinhadas ao foco do PISA em habilidades cognitivas fundamentais. Os erros-padrão associados (`READ.SE`, `MATH.SE`, `SCIE.SE`) expressam a precisão de cada estimativa: erros menores indicam maior confiabilidade na medida.

#### Gradiente socioeconômico: `ESCS`

A variável `ESCS` é um índice sintético que resume a posição socioeconômica, cultural e educacional da família. Ela é construída pela OCDE a partir de modelos de Teoria de Resposta ao Item, combinando informação sobre escolaridade e ocupação dos pais, recursos culturais no domicílio, bens, livros e outros indicadores em uma única medida contínua. Trata-se de um índice do tipo WLE (Estimativa de verossimilhança ponderada), calculado com base no procedimento descrito no [PISA 2018 Technical Report](https://www.oecd.org/pisa/data/pisa2018technicalreport/) (capítulo de Scaling Procedures), aplicado tanto às proficiências quanto aos índices derivados dos questionários.

No banco oficial do PISA, o `ESCS` já é divulgado em uma escala padronizada com média aproximada igual a 0 e desvio-padrão aproximado igual a 1. Para fins de armazenamento nos arquivos, a OCDE aplica uma transformação linear: o valor publicado é dado por `valor_no_arquivo = (valor_original + 5) × 1000`. Assim, um `ESCS` verdadeiro de `−0,103` aparece como `4897`, enquanto um valor de `+1,2` aparece como `6200`. Por conta disso, nós revertemos esse deslocamento para recuperar a escala oficial aplicando `ESCS = valor_no_arquivo / 1000 - 5`. Só para deixar claro, os fatores 5 e 1000 não são escolhas arbitrárias deste estudo, mas a inversão exata da codificação adotada pela OCDE, também utilizada para outros índices como `DISCLIMA`, `JOYREAD` e `SCREADCOMP` (documentados no [PISA 2018 Database – Codebook e Data Analysis Manual](https://www.oecd.org/pisa/data/2018database/)).

Em termos substantivos, valores mais altos de `ESCS` indicam famílias com maior capital socioeconômico. Neste estudo, tratamo-lo como eixo do gradiente socioeconômico e o coeficiente associado a ele indica como a proficiência varia em função da origem social do estudante, servindo de referência para quantificar desigualdades educacionais associadas ao contexto socioeconômico.

#### Clima escolar e pertencimento

**`BELONG`** (sentimento de pertencimento) captura o grau em que o estudante se sente parte da comunidade escolar. Algumas fontes pesquisadas sugerem que maior senso de pertencimento se associa a maior engajamento e, em média, a melhores resultados. Nesse contexto, avaliamos `BELONG` ao lado de `ESCS` e das proficiências, uma vez que parece plausível que um alto pertencimento atenue o efeito negativo de origens socioeconômicas desfavorecidas ao longo do gradiente. Vai saber. Quer dizer, saberemos! Um estudante de baixo `ESCS`, mas com forte vínculo com a escola, pode apresentar desempenho acima do esperado.

**`DISCLIMA`** mede a percepção de disciplina na sala de aula, outro fator que pode moderar o gradiente socioeconômico.

**`JOYREAD`** representa o prazer declarado em ler, enquanto **`SCREADCOMP`** mede a autoeficácia na leitura (confiança do estudante em sua capacidade de compreender textos). Ambos são utilizados para investigar se motivação e autopercepção moderam o gradiente socioeconômico: níveis altos de motivação e confiança podem amenizar o gradiente, enquanto baixa autoeficácia pode amplificar desigualdades. Assim como `ESCS` e `DISCLIMA`, esses índices são WLE armazenados com a mesma transformação `(valor + 5) × 1000` e revertidos da mesma forma.

#### Controles: gênero e repetência

Os controles de gênero (**`ST004D01T`**) e de histórico de repetência (**`REPEAT`**) foram incluídos para tentar separar o efeito do `ESCS` de outras características associadas ao desempenho. Cremos que possa haver, entre meninos e meninas, padrões distintos de proficiência, e como, popularmente, a repetência costuma estar associada a escores mais baixos, ao condicionarmo-nos ao modelo, pretendemos estimar um efeito condicional do `ESCS`, reduzindo a contaminação por fatores não diretamente socioeconômicos.

Reconhecemos, porém, que `REPEAT` pode ser, em parte, consequência do próprio `ESCS`; logo, esse controle tende a subestimar o efeito total do contexto socioeconômico, o que deve ser levado em conta na interpretação.

#### Pesos amostrais

**`SENWT`** (*Student Final Weight*) é o peso final do estudante, utilizado como fator de expansão. Como escolas e alunos são amostrados com probabilidades distintas, aplicar `SENWT` em médias, regressões e modelos garante que os resultados reflitam a população nacional de estudantes de 15 anos, e não apenas a amostra observada. Esta base não traz pesos replicados (`W_FSTR*`), então médias e regressões ponderadas usam `SENWT` diretamente.

#### Síntese

Em conjunto, essas informações permitem descrever o gradiente socioeconômico aluno a aluno e conectar esse gradiente às características das escolas, aproximando a análise tanto de evidências empíricas consolidadas quanto das hipóteses teóricas que motivam o estudo. Na literatura de EDM, pertencimento e clima escolar aparecem como fatores que podem amortecer desigualdades — razão pela qual os avaliamos sistematicamente.

### `FLT_BRA.xlsx`: escalas cognitivas e desenho amostral

A tabela `FLT_BRA.xlsx` complementa o nível aluno com as variáveis relacionadas ao desempenho medido pelo PISA e ao desenho amostral.

#### Proficiências e erros-padrão

Ela contém `READ` e `READ.SE`, calculados a partir dos dez valores plausíveis de leitura (`PV1READ`–`PV10READ`) gerados pela OCDE, que aplicam a Teoria de Resposta ao Item para lidar com o fato de cada estudante responder apenas parte dos itens do teste. Nos microdados completos da OCDE, `READ` e `READ.SE` seriam derivados desses dez valores plausíveis combinados com os pesos amostrais. Nesta versão brasileira, esses PVs não foram incluídos porque o INEP já distribuiu os escores sintetizados; ainda assim, a interpretação permanece a mesma: `READ` é a estimativa média da proficiência em leitura (escala 500/100), sintetizando a proficiência média comparável entre alunos e escolas, enquanto `READ.SE` expressa o erro-padrão associado a essa estimativa, de modo que erros menores indicam maior precisão.

A mesma base inclui `MATH` e `MATH.SE`, que seguem a mesma lógica para matemática. Usamos esse arquivo para validar consistência ou, se necessário, cruzar com outras tabelas oficiais.

#### Índices psicométricos

Além disso, `FLT_BRA.xlsx` reúne índices psicométricos que capturam aspectos intrapessoais relevantes para o desempenho, como `JOYREAD` e `SCREADCOMP`, construídos por escalas WLE e centrados em torno de zero.

#### Pesos e identificadores

A mesma base inclui o peso final do estudante, `SENWT`, que garante inferência representativa da população de estudantes de 15 anos.

**Observação importante**: `CNTSTUID` vem deslocado em +50 000 (ex.: 7650001). Antes de mesclar com outras tabelas, subtraímos 50 000 para casar os IDs. Assim como no `STU_BRA.xlsx`, só há `SENWT` disponível.

#### Ciências

Como `SCIE` não aparece no `FLT_BRA.xlsx`, tomamos os escores de ciências do `STU_BRA.xlsx` para manter os três domínios alinhados.

### `SCH_BRA.xlsx`: nível escola

A planilha `SCH_BRA.xlsx` introduz o nível de contexto escolar, correspondente ao segundo nível dos modelos. Para cada `CNTSCHID`, são disponibilizados, entre outros indicadores, variáveis respondidas pelos diretores que caracterizam as condições institucionais:

#### Escassez de recursos

Os índices **`EDUSHORT`** e **`STAFFSHORT`** são construídos a partir das respostas dos diretores sobre escassez de materiais pedagógicos e de pessoal qualificado. Os valores originais variam de 1 a 119; ao reescalonarmos (`/10 - 5`), recuperamos uma escala aproximadamente centrada em zero que facilita a interpretação, em que valores positivos indicam maior escassez que a média da OCDE e valores negativos indicam menor escassez.

#### Financiamento escolar

A base inclui também **`SC016Q01TA`** e **`SC016Q02TA`** (entre outros itens da série `SC016Q0*`), que expressam os percentuais da receita escolar provenientes de fontes governamentais e de contribuições privadas (famílias, doadores, patrocínios), permitindo caracterizar a composição financeira do ambiente escolar. **`SC013Q01TA`** diferencia redes públicas/privadas.

#### Vinculação aos alunos

Esses indicadores são vinculados aos alunos via `CNTSCHID`, o que possibilita testar se condições objetivas de recursos e financiamento moderam a inclinação do gradiente socioeconômico e quantificar quanto da variância entre escolas (efeito escola) está associada a fatores mensuráveis de gestão e infraestrutura.

Ligamos cada escola aos alunos via `CNTSCHID` e calculamos perfis ponderados (`read_mean_w`, `math_mean_w`, `science_mean_w`, `escs_mean_w`, `disclima_mean_w`, `belong_mean_w`). Isso alimenta o nível 2 dos modelos multiníveis, separando composição discente do verdadeiro efeito escola.

### Por que cada bloco é necessário?

Combinando as três bases, é possível modelar o gradiente socioeconômico ponderando corretamente o desenho amostral e explorando fatores intrapessoais e institucionais que podem suavizar ou acentuar o efeito da origem socioeconômica sobre as proficiências:

- **`ESCS`** e seus controles nos permitem medir o gradiente socioeconômico em leitura, matemática e ciências.
- **`BELONG`**, **`DISCLIMA`**, **`JOYREAD`** e **`SCREADCOMP`** ajudam a investigar se fatores intrapessoais (motivação, pertencimento, disciplina percebida) amortecem ou reforçam o efeito do contexto socioeconômico.
- **`EDUSHORT`**, **`STAFFSHORT`** e **`SC016Q0*`** aproximam condições institucionais governáveis, essenciais para testar as hipóteses sobre efeito escola e equidade (H1–H3).

Com essa estrutura de dados — estudantes, escores e escolas devidamente conectados e ponderados por `SENWT` — conseguimos modelar o gradiente socioeconômico nos três domínios, comparar resultados entre leitura/matemática/ciências e analisar como clima e gestão escolar influenciam o efeito escola no Brasil.

### Modelo de Dados Multinível

```
NÍVEL 2: Escola j (N=597)
├── CNTSCHID (chave)
├── Tipo/Localização: SCHLTYPE, SC001Q01TA, SCHSIZE
├── Gestão: EDUSHORT, STAFFSHORT, STRATIO, PROATCE
├── Clima: STUBEHA, TEACHBEHA
├── Financiamento: SC016Q01TA, SC016Q02TA
└── Variáveis agregadas (criadas de STU_BRA):
    ├── ESCS_mean (composição socioeconômica)
    ├── ESCS_sd (heterogeneidade)
    └── n_students (tamanho amostral)

NÍVEL 1: Aluno i em Escola j (N=10.691)
├── CNTSTUID (chave primária)
├── CNTSCHID (chave estrangeira → Escola)
├── Desfecho: READ, MATH, SCIE (Leitura, Matemática, Ciências)
├── Preditor: ESCS (status socioeconômico)
├── Clima/Pertencimento: BELONG, DISCLIMA, JOYREAD, SCREADCOMP
├── Controles: ST004D01T (gênero), REPEAT (repetência), língua, imigração
└── Peso: SENWT (peso amostral)
```

### Estatísticas Descritivas Ponderadas (Brasil, PISA 2018)

Todos os números abaixo foram calculados com `SENWT` para representar a população brasileira de estudantes de 15 anos (fonte: microdados PISA 2018, arquivo `STU_BRA.xlsx`). A tabela completa está disponível em `outputs/weighted_summary.csv`.

| Variável | Média (SENWT) | DP (SENWT) | P10 | Mediana | P90 | N válido |
|----------|---------------|------------|-----|---------|-----|---------|
| READ | **412,9** | 96,6 | 296,6 | 406,7 | 545,4 | 10.691 |
| MATH | 383,6 | 80,9 | 288,5 | 374,8 | 493,6 | 10.691 |
| SCIENCE | 403,6 | 85,1 | 301,7 | 395,2 | 522,7 | 10.691 |
| ESCS (valor no arquivo) | 4.706 | 2.659 | 1.853 | 4.717 | 8.403 | 10.453 |
| DISCLIMA | 546,1 | 305,9 | 140,0 | 621,0 | 915,0 | 10.099 |
| BELONG | 998,9 | 424,2 | 364,0 | 1.096,0 | 1.524,0 | 8.339 |
| JOYREAD | 453,0 | 231,6 | 220,0 | 458,0 | 768,0 | 9.655 |
| SCREADCOMP | 37,8 | 15,6 | 19,0 | 38,0 | 58,0 | 9.143 |

> **Nota:** valores do tipo WLE (ESCS, DISCLIMA, JOYREAD, SCREADCOMP) aparecem deslocados no arquivo original; após a transformação inversa, ESCS tem média próxima de 0 e DP ≈ 1.

Principais leituras:

- As proficiências brasileiras ficam ~90 pontos abaixo da média OCDE (≈500), confirmando o hiato de desempenho.
- A dispersão socioeconômica é ampla (P10 ≈ −3,1; P90 ≈ +3,4 na escala padronizada), o que justifica estudar o gradiente.
- Clima disciplinar (`DISCLIMA`) e pertencimento (`BELONG`) apresentam distribuições assimétricas, com caudas longas para contextos adversos.

### Perfis por Quartil de ESCS

Também calculamos médias ponderadas por quartil socioeconômico (arquivo `outputs/quartil_summary.csv`). Resultados-chave:

| Quartil de ESCS | READ | MATH | SCIENCE | DISCLIMA | BELONG | Estudantes representados (≈ milhares) |
|-----------------|------|------|---------|----------|--------|----------------------------------------|
| Q1 (mais vulnerável) | 373,0 | 350,7 | 377,9 | 463,5 | 935,3 | 1.216 |
| Q2 | 396,3 | 373,9 | 398,5 | 525,4 | 989,9 | 1.193 |
| Q3 | 417,6 | 393,5 | 417,8 | 568,1 | 993,5 | 1.199 |
| Q4 (mais favorecido) | **467,7** | **440,8** | **458,9** | **657,0** | 1.060,7 | 1.278 |

- A distância entre Q1 e Q4 chega a ~95 pontos em leitura e ~90 pontos em matemática/ciências.
- Climas disciplinares e sentimentos de pertencimento também melhoram conforme o contexto socioeconômico da escola, sugerindo efeito composição.

### Limitações dos Dados Fornecidos

#### 1. Plausible Values (PVs) Ausentes

- **O que falta:** PV1READ...PV10READ (10 valores plausíveis por aluno)
- **Impacto:** Não é possível replicar exatamente o método de pooling descrito na literatura
- **Alternativa:** Usar o escore agregado READ (possivelmente média dos 10 PVs)
- **Consequência:** Ligeira subestimação da incerteza (ICs podem estar estreitos)

#### 2. Pesos Replicados (BRR-Fay) Ausentes

- **O que falta:** W_FSTR1...W_FSTR80 (80 pesos replicados)
- **Impacto:** Não é possível calcular erros padrão via Balanced Repeated Replication
- **Alternativa:** SENWT + cluster robusto por escola
- **Consequência:** SEs podem estar ligeiramente subestimados

#### 3. Índices de Liderança Ausentes

- **O que falta:** LEADCOM, LEADINST, LEADPD (liderança comunicativa, instrucional, desenv. profissional)
- **Alternativa:** Usar itens individuais (SC034, SC052, SC053) ou criar índices manualmente
- **Consequência:** Análise fica focada em recursos e clima (não especificamente liderança)

---

## 🧠 Modelagem e Resultados

### Modelos de Gradiente Socioeconômico (WLS ponderado)

Executamos duas especificações para cada domínio:

1. **Modelo 1 – básico:** `Proficiência ~ ESCS_c` (ESCS centrado na média nacional).
2. **Modelo 2 – completo:** adiciona `clima_escola_c`, `DISCLIMA`, `EDUSHORT`, `STAFFSHORT`, gênero, repetência e a interação `ESCS_c × clima_escola_c`.

| Domínio | Modelo | Coef. ESCS_c | Coef. clima_escola_c | Interação ESCS×clima | R² |
|---------|--------|--------------|----------------------|----------------------|----|
| Leitura | Básico | **+14,39** (p<0,001) | – | – | 0,156 |
| Leitura | Completo | **+9,43** (p<0,001) | **+6,81** (p<0,001) | **+1,11** (p<0,001) | 0,375 |
| Matemática | Básico | +13,70 (p<0,001) | – | – | 0,201 |
| Matemática | Completo | +8,98 (p<0,001) | +5,97 (p<0,001) | +1,38 (p<0,001) | 0,428 |
| Ciências | Básico | +13,87 (p<0,001) | – | – | 0,192 |
| Ciências | Completo | +9,13 (p<0,001) | +5,52 (p<0,001) | +1,45 (p<0,001) | 0,413 |

**Leituras principais**

- O gradiente socioeconômico é positivo em todos os domínios: cada desvio-padrão adicional em `ESCS` adiciona 13–14 pontos nas especificações básicas.
- Ao introduzir moderadores de clima e escassez, a inclinação cai para ~9 pontos, mas continua positiva: escolas organizadas elevam o patamar médio (clima +6 a +7 pontos) **e** aumentam o retorno do capital socioeconômico (interação positiva).
- Os `R²` ponderados praticamente dobram no modelo completo (0,37–0,43), indicando que clima e gestão explicam parte relevante da desigualdade observada.

### Modelos Multinível (ICC e efeitos entre escolas)

| Domínio | Modelo | ICC | Variância entre escolas | Variância dentro das escolas | Coef. ESCS |
|---------|--------|-----|-------------------------|------------------------------|------------|
| Leitura | Intercepto aleatório | **0,222** | 1.444,9 | 5.057,0 | +3,13 |
| Leitura | Inclinação aleatória | 0,222 | 1.429,8 | 4.997,5 | +3,12 |
| Matemática | Intercepto aleatório | **0,241** | 1.021,8 | 3.226,8 | +3,86 |
| Ciências | Intercepto aleatório | **0,256** | 1.195,3 | 3.477,3 | +4,22 |

- Mesmo após adicionar moderadores de escola, **22–26%** da variância permanece entre instituições, sinalizando efeito escola substancial.
- A inclusão de inclinações aleatórias não reduziu o ICC, sugerindo que o componente entre-escolas é estável dado o conjunto de covariáveis atuais.

### Respostas às Perguntas e Hipóteses

- **Q1 – Quanto da variância está entre escolas?** Cerca de 22% (Leitura) a 26% (Ciências) da variância permanece entre escolas → o efeito escola brasileiro é elevado.  
  - **H3 (redução do ICC com moderadores)**: *Não confirmada*. Mesmo com clima/gestão no modelo, o ICC não diminuiu de forma significativa.

- **Q2 – O ESCS médio da escola importa além do ESCS individual?** Sim. Climas disciplinares favoráveis elevam as médias em +6 a +7 pontos e o gradiente individual cai de ~14 para ~9 pontos após controlar o contexto.  
  - **H2 (melhor gestão/clima → mais desempenho)**: *Confirmada*. Escolas com melhor clima têm interceptos mais altos, mesmo controlando composição socioeconômica.

- **Q3 – Escolas com melhor clima achatam o gradiente?** Não. A interação `ESCS × clima_escola` é positiva em todos os domínios (≈ +1 ponto no retorno do ESCS), indicando que climas organizados beneficiam mais os alunos já favorecidos.  
  - **H1 (clima reduz desigualdade)**: *Refutada*. O gradiente fica mais íngreme em contextos escolares de alta qualidade.

---

## ⚠️ Limitações e Próximos Passos

1. **Valores plausíveis (PV) indisponíveis:** usamos os escores já sintetizados pelo INEP; idealmente, deveríamos propagar a incerteza combinando os 10 PVs de cada domínio.
2. **Pesos replicados ausentes:** sem `W_FSTR1…W_FSTR80`, os erros-padrão BRR não puderam ser estimados. Para trabalhos futuros, recomenda-se ajustar modelos com replicates ou aplicar bootstrap estratificado.
3. **Validação estatística formal:** ainda não rodamos testes de hipóteses/comparações múltiplas (p.ex. Wald tests entre domínios) nem avaliamos resíduos/diagnósticos dos modelos.
4. **Outras variáveis de gestão:** indicadores de liderança (`LEADCOM`, `LEADINST`, etc.) não estavam disponíveis; incluir esses blocos pode refinar a interpretação do efeito escola.
5. **Comunicação dos dados:** aconselha-se acrescentar visualizações formais (densidades, boxplots ponderados) e publicar as tabelas CSV (já geradas em `outputs/`) em um dashboard ou anexo executivo.

## 📁 Estrutura do Repositório

```
ia-na-educacao/
├── README.md                           # Este arquivo
├── pesquisa.ipynb                      # Notebook principal (EDM pipeline completo)
├── artigo.pdf                          # Documento base do projeto
│
├── pisa2018/                           # Dados PISA 2018
│   ├── PISA2018_CODEBOOK.xlsx          # Dicionário de variáveis
│   ├── stu/
│   │   └── STU_BRA.xlsx                # Dados individuais de alunos
│   ├── sch/
│   │   └── SCH_BRA.xlsx                # Dados de escolas (questionário diretor)
│   ├── sch_stu/
│   │   └── SCH_STU_BRA.xlsx            # Dados agregados (escola + médias alunos)
│   ├── sch_tch/
│   │   └── SCH_TCH_BRA.xlsx            # Dados agregados (escola + médias professores)
│   ├── tch/
│   │   └── TCH_BRA.xlsx                # Dados individuais de professores
│   └── flt/
│       └── FLT_BRA.xlsx                # Letramento financeiro (opcional)
│
├── scripts/                            # Scripts auxiliares
│   └── arquivos.py                     # Funções diversas para preparação e análise
│
├── results/                            # Resultados das análises (criado ao executar)
│   ├── tables/                         # Tabelas de resultados
│   ├── figures/                        # Gráficos e visualizações
│   └── models/                         # Objetos de modelo salvos
│
└── docs/                               # Documentação adicional
    └── arquivos de pesquisa            # Documentos de apoio e referências
```

---

## 🔧 Instalação e Requisitos

### Requisitos de Sistema

- **Python:** 3.12 ou superior
- **Memória RAM:** Mínimo 8 GB (recomendado 16 GB para datasets completos)
- **Espaço em disco:** ~200 MB para dados PISA

### Dependências Python

Vide `requirements.txt` para lista completa.

### Instalação

#### 1. Clonar o Repositório

```bash
git clone https://github.com/fabio-linhares/EDM---Efeito-Escola-e-Gradiente-Socioeconômico-no-Brasil-PISA-2018-.git
cd EDM---Efeito-Escola-e-Gradiente-Socioeconômico-no-Brasil-PISA-2018
```

#### 2. Criar Ambiente Virtual

```bash
# Criar ambiente
conda create -n ambiente_edm python=3.12 -y
conda activate ambiente_edm
```

#### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Ou instalar pacotes individuais:

```bash
pip install pandas numpy statsmodels matplotlib seaborn openpyxl python-dotenv
```

#### 4. Baixar Dados PISA 2018

Caso os arquivos não estejam no repositório:

```bash
# Opção 1: Download manual
# Acesse: https://www.oecd.org/pisa/data/2018database/
# Baixe: Student questionnaire (Brazil), School questionnaire (Brazil)
# Extraia para: pisa2018/stu/STU_BRA.xlsx e pisa2018/sch/SCH_BRA.xlsx

# Opção 2: Script automatizado (se disponível)
python scripts/download_pisa_data.py --country BRA --year 2018
```

---

## 🚀 Como Executar

### Opção 1: Notebook Jupyter (Recomendado)

```bash
# Instalar Jupyter (se não tiver)
pip install jupyter

# Iniciar Jupyter
jupyter notebook

# Abrir: pesquisa.ipynb
```

**Estrutura do Notebook:**

1. **Setup:** Importação de bibliotecas e configuração
2. **Carregamento de Dados:** Leitura de STU_BRA, FLT_BRA e SCH_BRA
3. **Preparação:** Merge, criação de variáveis, tratamento de missings
4. **Análise Exploratória:** Estatísticas descritivas, correlações, gráficos
5. **Modelos Multinível:** M0 (nulo) → M1 (ESCS) → M2 (contextual) → M3 (gestão) → M4 (interações)
6. **Resultados:** Tabelas de coeficientes, testes de hipótese, visualizações
7. **Sensibilidade:** Matemática e Ciências, diferentes controles
8. **Conclusões:** Síntese e implicações

### Opção 2: Scripts Python

```bash
# 1. Preparar dados (Scripts em desenvolvimento)
python scripts/pisa_prep.py --input pisa2018/ --output data/processed/

# 2. Executar modelos
python main.py --config config/model_config.yaml

# 3. Gerar relatório
python scripts/generate_report.py --results results/ --output report.pdf
```

### Opção 3: Executar Análise Completa (Pipeline)

```bash
# Script que executa todo o pipeline EDM
bash run_analysis.sh
```

---

- Efeito composição é **2-3x maior** que efeito individual
- Implicação: **Segregação escolar** por NSE é um problema (estudar com colegas de alto NSE beneficia todos)

### 3. Moderação por Gestão/Clima (Q3)

**Resultado esperado (Modelo M4):**

```
Interação ESCS × STUBEHA: γ₁₂ ≈ -5 a -10 (negativo e significativo)
```

**Interpretação:**

- **Sim**, escolas com **melhor clima** (STUBEHA baixo) apresentam gradientes mais planos
- Em escolas com clima ruim (STUBEHA alto): gradiente ESCS íngreme (40 pontos/DP)
- Em escolas com bom clima (STUBEHA baixo): gradiente achatado (20 pontos/DP)
- **Implicação:** Investir em clima escolar pode **reduzir desigualdade** sem depender apenas de mudanças socioeconômicas

### 4. Visualizações

#### Gráfico 1: Gradientes por Tipo de Escola

```
[Scatter plot com linhas de regressão]
Eixo X: ESCS
Eixo Y: Proficiência (READ/MATH/SCIE)
Cores: Escola pública (vermelho) vs. privada (azul)

Resultado esperado:
- Escolas privadas: intercepto mais alto, gradiente mais plano
- Escolas públicas: intercepto mais baixo, gradiente mais íngreme
```

#### Gráfico 2: Efeito do Clima no Gradiente

```
[Gráfico de interação]
Eixo X: ESCS
Eixo Y: Proficiência
Linhas: STUBEHA baixo (verde) vs. médio (amarelo) vs. alto (vermelho)

Resultado esperado:
- Linha verde (bom clima): mais plana (equidade)
- Linha vermelha (clima ruim): mais íngreme (desigualdade)
```

### 5. Perfil de "Escolas Eficazes e Equitativas"

**Características esperadas:**

| Dimensão | Escolas Eficazes e Equitativas | Escolas Típicas |
|----------|-------------------------------|-----------------|
| **Desempenho médio** | Acima do esperado dado ESCS_mean | Conforme esperado |
| **Gradiente ESCS** | Plano (≤20 pontos/DP) | Íngreme (≥30 pontos/DP) |
| **STUBEHA** | Baixo (bom clima) | Médio/Alto |
| **EDUSHORT** | Baixo (recursos adequados) | Médio/Alto |
| **STRATIO** | ≤25 alunos/prof | >30 alunos/prof |
| **PROATCE** | >80% certificados | <60% certificados |

---

## 📚 Referências

### Fundamentação Teórica

1. **Edmonds, R. (1979).** Effective schools for the urban poor. *Educational Leadership*, 37(1), 15-24.
2. **Creemers, B. P., & Kyriakides, L. (2008).** *The dynamics of educational effectiveness: A contribution to policy, practice, and theory in contemporary schools*. Routledge.
3. **Coleman, J. S., et al. (1966).** *Equality of educational opportunity*. US Government Printing Office.

### PISA e Eficácia Escolar

4. **OECD (2020).** *PISA 2018 Results (Volume V): Effective Policies, Successful Schools*. OECD Publishing, Paris. DOI: 10.1787/ca768d40-en
   - https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/09/pisa-2018-results-volume-v_9748ee31/ca768d40-en.pdf
5. **OECD (2019).** *PISA 2018 Assessment and Analytical Framework*. OECD Publishing, Paris.
   - https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/04/pisa-2018-assessment-and-analytical-framework_d1c359c7/b25efab8-en.pdf
6. **Schleicher, A. (2018).** *World Class: How to Build a 21st-Century School System, Strong Performers and Successful Reformers in Education*. OECD Publishing, Paris.
7. **Avvisati, F., et al. (2020).** The Measure of Socio-Economic Status in PISA: A Review and an Update. *Large-scale Assessments in Education*, 8, 8. DOI: 10.1186/s40536-020-00086-x
   - https://largescaleassessmentsineducation.springeropen.com/articles/10.1186/s40536-020-00086-x

### Desigualdade Educacional no Brasil

8. **Alves, M. T. G., & Soares, J. F. (2007).** A Eficácia das Escolas Públicas Brasileiras no Ensino Fundamental. *Educação e Pesquisa*, 33(1), 163-180. DOI: 10.1590/S1517-97022007000100011
   - http://www.scielo.br/pdf/ep/v33n1/a11v33n1.pdf
9. **Ernica, M., Rodrigues, E. C., & Soares, J. F. (2025).** Desigualdades Educacionais no Brasil Contemporâneo: Definição, Medida e Resultados. *Dados – Revista de Ciências Sociais*, 68(1), e20220109. DOI: 10.1590/dados.2025.68.1.345
   - https://www.scielo.br/j/dados/a/x4zKhjLQ5tv7Tx3RrWPtnjn/
10. **Alves, M. T. G., & Franco, C. (2018).** Estudo Longitudinal sobre Eficácia Educacional no Brasil: Comparação entre Resultados Contextualizados e Valor Acrescentado. *Dados*, 61(4), 265-300. DOI: 10.1590/001152582018171
    - http://www.scielo.br/pdf/dados/v61n4/0011-5258-dados-61-4-0265.pdf

### Análise de Dados PISA

11. **Neuman, M. (2022).** PISA Data Clusters Reveal Student and School Inequality that Affects Results. *PLOS ONE*, 17(5), e0267040. DOI: 10.1371/journal.pone.0267040
    - https://pmc.ncbi.nlm.nih.gov/articles/PMC9094565/
12. **National Center for Education Statistics (2018).** Program for International Student Assessment (PISA) – Technical Notes. NCES.
    - https://nces.ed.gov/surveys/pisa/2018technotes-5.asp

### Contexto Brasileiro

13. **Brasil/Inep (2019).** Relatório Nacional PISA 2018. Brasília: Inep/MEC.
    - http://download.inep.gov.br/acoes_internacionais/pisa/documentos/2019/relatorio_nacional_PISA_2018.pdf
14. **Brasil/Inep (2023).** Divulgados os resultados do PISA 2022. Brasília: Inep/MEC.
    - https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/acoes-internacionais/divulgados-os-resultados-do-pisa-2022
15. **Ponne, B. G. (2023).** Better Incentives, Better Marks: A Synthetic Control Evaluation of the Educational Policies in Ceará, Brazil. *Brazilian Political Science Review*, 17(1), e0005. DOI: 10.1590/1981-3821202300010005
    - https://www.scielo.br/j/bpsr/a/s8jwsh34QmjcbN3pJSZTSFK/

---

## 📄 Licença e Citação

### Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### Como Citar

Se você usar este projeto em sua pesquisa, por favor cite:

```@mastersthesis{linhares2025efeito,
  author       = {Linhares, F{\'a}bio},
  title        = {Efeito Escola e Gradiente Socioecon{\^o}mico no Brasil:
                  Quantificando o Papel da Gest{\~a}o e do Clima Escolar na Equidade Educacional},
  school       = {Universidade Federal de Alagoas (UFAL), Programa de P{\'o}s-Gradua{\c c}{\~a}o em Inform{\'a}tica},
  address      = {Macei{\'o}, Brasil},
  year         = {2025},
  type         = {Disserta{\c c}{\~a}o de Mestrado},
  advisor      = {Ig Ibert Bittencourt Santana Pinto},
  keywords     = {PISA 2018, efeito escola, gradiente socioecon{\^o}mico, minera{\c c}{\~a}o de dados educacionais},
  note         = {Disciplina: Intelig{\^e}ncia Artificial Aplicada {\`a} Educa{\c c}{\~a}o}
}
```
