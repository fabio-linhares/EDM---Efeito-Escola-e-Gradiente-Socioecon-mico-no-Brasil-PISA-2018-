<p align="center">
  <img src="https://ufal.br/ufal/comunicacao/identidade-visual/brasao/ods/ufal_ods1.png" alt="Logo da UFAL" width="600"/>
</p>

<h1 align="center">Efeito Escola e Gradiente Socioeconômico no Brasil</h1>
<h3 align="center">Quantificando o Papel da Gestão e do Clima Escolar na Equidade Educacional</h3>
<h4 align="center">Análise dos Microdados PISA 2018 via Mineração de Dados Educacionais (EDM)</h4>

<p align="center">
  <strong>Universidade Federal de Alagoas (UFAL)</strong><br>
  Programa de Pós-Graduação em Informática<br>
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

Este projeto de Mineração de Dados Educacionais (EDM) investiga o **"efeito escola"** no Brasil, utilizando os microdados do **PISA 2018**. O objetivo é quantificar quanto da variância no desempenho em Leitura de estudantes brasileiros se deve a diferenças **entre escolas** (ICC - Intraclass Correlation Coefficient) e testar se condições de **gestão escolar** e **clima institucional** podem **moderar o gradiente socioeconômico** (relação entre ESCS - Economic, Social and Cultural Status - e notas), promovendo maior equidade educacional.

### Principais Questões:

1. **Q1:** Quanto da variância em Leitura está entre escolas vs. dentro de escolas?
2. **Q2:** O ESCS médio da escola (composição socioeconômica) tem efeito além do ESCS individual?
3. **Q3:** Escolas com melhor gestão/clima apresentam gradientes socioeconômicos mais planos (menos desigualdade)?

### Hipóteses Testáveis:

- **H1 (Equidade):** Melhor clima disciplinar e gestão instrucional → gradiente ESCS menos íngreme (mais equitativo)
- **H2 (Desempenho):** Mesmas condições → médias escolares mais altas, controlando composição socioeconômica
- **H3 (Variância):** Inclusão de gestão/clima → redução do ICC (parcela governável da variância entre escolas)

### Abordagem Metodológica:

- **Modelos multinível** (aluno *i* em escola *j*) com intercepto e slope aleatórios
- **Pesos amostrais** (SENWT) para inferência populacional
- **Análise de interações** ESCS × fatores escolares (EDUSHORT, STUBEHA, TEACHBEHA)
- **Sensibilidade:** Matemática e Ciências como robustez; variação de controles

---

## 🌍 Contexto e Motivação

### O PISA como Ferramenta de Diagnóstico

O **Programme for International Student Assessment (PISA)**, coordenado pela OCDE desde 2000, avalia competências de estudantes de 15 anos em Leitura, Matemática e Ciências. No Brasil, o INEP coordena a aplicação desde o primeiro ciclo. O PISA 2018 avaliou **10.691 estudantes** em **597 escolas** brasileiras.

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

Quantificar o efeito escola no Brasil (PISA 2018) e investigar se condições de gestão escolar e clima institucional moderam a relação entre status socioeconômico (ESCS) e desempenho em Leitura, contribuindo para maior equidade educacional.

### Objetivos Específicos

1. **Estimar o ICC** (Intraclass Correlation Coefficient) para Leitura no Brasil
2. **Testar efeito contextual** do ESCS médio da escola (composição) além do ESCS individual
3. **Modelar interações** ESCS × gestão/clima para identificar escolas que "achatam" gradientes
4. **Comparar perfis de escola** (pública vs. privada; urbana vs. rural) quanto à equidade
5. **Propor indicadores** de escolas eficazes e equitativas para orientar políticas

### Perguntas de Pesquisa

| ID | Pergunta | Análise | Hipótese |
|----|----------|---------|----------|
| **Q1** | Quanto da variância em Leitura está **entre escolas**? | Modelo nulo (ICC) | ICC ~25-35% (típico em países desiguais) |
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
- **Índice padronizado** (média=0, DP=1) criado pela OCDE
- **Componentes:**
  - Ocupação parental (HISEI - International Socio-Economic Index)
  - Educação parental (PAREDINT, HISCED)
  - Posses domésticas (HOMEPOS - livros, arte, bens materiais)
  - Recursos educacionais (HEDRES - mesa, computador, internet)
  - Recursos de TIC (ICTRES)

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

### 1. Desenho do Estudo

- **Tipo:** Observacional transversal com dados secundários
- **População:** Estudantes brasileiros de 15 anos (PISA 2018)
- **Amostra:** 10.691 alunos em 597 escolas
- **Desenho amostral:** Probabilístico estratificado por escola

### 2. Variáveis

#### Nível do Aluno (Level 1)

| Tipo | Variável | Descrição | Fonte |
|------|----------|-----------|-------|
| **Desfecho** | READ | Escore em Leitura (escala PISA) | STU_BRA |
| **Preditor principal** | ESCS | Índice socioeconômico e cultural (padronizado) | STU_BRA |
| **Controles** | ST004D01T | Gênero (1=Fem, 2=Masc) | STU_BRA |
| | ST127Q01-03TA | Repetência (primário/fundamental/médio) | STU_BRA |
| | ST022Q01TA | Língua em casa = língua do teste? | STU_BRA |
| | ST019AQ01TA | Status de imigração | STU_BRA |
| **Peso** | SENWT | Peso amostral final (Senate Weight) | STU_BRA |

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
| **Controles** | SCHLTYPE | Tipo de escola (1=Pública, 2=Privada) | SCH_BRA |
| | SCHSIZE | Tamanho da escola (nº alunos) | SCH_BRA |
| | SC001Q01TA | Localização (1=Vila...5=Metrópole) | SCH_BRA |

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
1. **Merge:** STU_BRA + SCH_BRA por CNTSCHID
2. **Agregação:** Criar ESCS_mean, ESCS_sd, n_students por escola
3. **Centralização:** ESCS_centered = ESCS - ESCS_mean (within-school)
4. **Missings:**
   - Exclusão listwise: READ, ESCS, CNTSCHID (variáveis críticas)
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
- **Notebook:** Jupyter (projeto2.ipynb)

---

## 📊 Dados

### Fonte

**PISA 2018** - Programme for International Student Assessment (OCDE)
- **Download:** [OECD PISA Database](https://www.oecd.org/pisa/data/2018database/)
- **Documentação:** `PISA2018_CODEBOOK.xlsx`
- **País:** Brasil (CNTRYID = 76)

### Estrutura dos Dados

#### Arquivos Utilizados

| Arquivo | Registros | Variáveis | Nível | Descrição |
|---------|-----------|-----------|-------|-----------|
| **STU_BRA.xlsx** | 10.691 | 852 | Aluno (L1) | Dados individuais dos estudantes |
| **SCH_BRA.xlsx** | 597 | 208 | Escola (L2) | Questionário do diretor |
| **SCH_STU_BRA.xlsx** | 597 | 2.986 | Escola (agregado) | Escola + médias dos alunos |

#### Arquivos Opcionais (Análises Avançadas)

| Arquivo | Uso |
|---------|-----|
| **SCH_TCH_BRA.xlsx** | Práticas docentes agregadas (para testar mediação - H4) |
| **TCH_BRA.xlsx** | Dados individuais de professores (heterogeneidade docente) |
| **FLT_BRA.xlsx** | Letramento financeiro (fora do escopo) |

### Modelo de Dados Multinível

```
NÍVEL 2: Escola j (N=597)
├── CNTSCHID (chave)
├── Tipo/Localização: SCHLTYPE, SC001Q01TA, SCHSIZE
├── Gestão: EDUSHORT, STAFFSHORT, STRATIO, PROATCE
├── Clima: STUBEHA, TEACHBEHA
└── Variáveis agregadas (criadas de STU_BRA):
    ├── ESCS_mean (composição socioeconômica)
    ├── ESCS_sd (heterogeneidade)
    └── n_students (tamanho amostral)

NÍVEL 1: Aluno i em Escola j (N=10.691)
├── CNTSTUID (chave primária)
├── CNTSCHID (chave estrangeira → Escola)
├── Desfecho: READ (Leitura)
├── Preditor: ESCS (status socioeconômico)
├── Controles: ST004D01T (gênero), repetência, língua, imigração
└── Peso: SENWT (peso amostral)
```

### Estatísticas Descritivas (Esperadas)

| Variável | Nível | Média | DP | Min | Max |
|----------|-------|-------|-----|-----|-----|
| READ | Aluno | ~413 | ~93 | ~150 | ~700 |
| ESCS | Aluno | ~-1.0 | ~1.1 | ~-5 | ~3 |
| ESCS_mean | Escola | ~-1.0 | ~0.7 | ~-3 | ~2 |
| EDUSHORT | Escola | ~0.0 | ~1.0 | ~-2 | ~3 |
| STUBEHA | Escola | ~0.0 | ~1.0 | ~-2 | ~3 |

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

## 📁 Estrutura do Repositório

```
ia-na-educacao/
├── README.md                          # Este arquivo
├── projeto2.ipynb                     # Notebook principal (EDM pipeline completo)
├── projeto_artigo.pdf                 # Documento base do projeto
│
├── pisa2018/                          # Dados PISA 2018
│   ├── PISA2018_CODEBOOK.xlsx        # Dicionário de variáveis
│   ├── stu/
│   │   └── STU_BRA.xlsx              # Dados individuais de alunos
│   ├── sch/
│   │   └── SCH_BRA.xlsx              # Dados de escolas (questionário diretor)
│   ├── sch_stu/
│   │   └── SCH_STU_BRA.xlsx          # Dados agregados (escola + médias alunos)
│   ├── sch_tch/
│   │   └── SCH_TCH_BRA.xlsx          # Dados agregados (escola + médias professores)
│   ├── tch/
│   │   └── TCH_BRA.xlsx              # Dados individuais de professores
│   └── flt/
│       └── FLT_BRA.xlsx              # Letramento financeiro (opcional)
│
├── scripts/                           # Scripts auxiliares
│   ├── pisa_dataframes.py            # Carregamento e preparação de dados
│   ├── pisa_prep.py                  # Limpeza e transformações
│   ├── pisa_read_xlsx.py             # Leitura de arquivos Excel
│   └── ls_tree.py                    # Utilitário para estrutura de diretórios
│
├── results/                           # Resultados das análises (criado ao executar)
│   ├── tables/                       # Tabelas de resultados
│   ├── figures/                      # Gráficos e visualizações
│   └── models/                       # Objetos de modelo salvos
│
└── docs/                              # Documentação adicional
    ├── DADOS_PISA_2018_ANALISE_COMPLETA.md  # Guia detalhado dos dados
    └── metodologia_multinivel.md     # Aprofundamento metodológico
```

---

## 🔧 Instalação e Requisitos

### Requisitos de Sistema

- **Python:** 3.11 ou superior
- **Memória RAM:** Mínimo 8 GB (recomendado 16 GB para datasets completos)
- **Espaço em disco:** ~2 GB para dados PISA completos

### Dependências Python

```bash
# Análise de dados
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0              # Leitura de arquivos Excel

# Modelagem estatística
statsmodels>=0.14.0          # Modelos multinível (MixedLM)
scipy>=1.10.0

# Visualização
matplotlib>=3.7.0
seaborn>=0.12.0

# Utilitários
python-dotenv>=1.0.0         # Variáveis de ambiente
tqdm>=4.65.0                 # Barra de progresso

# Opcional (análises avançadas)
linearmodels>=5.3            # Modelos em painel
pyreadstat>=1.2.0            # Leitura de .sav (SPSS)
```

### Instalação

#### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/ia-na-educacao.git
cd ia-na-educacao
```

#### 2. Criar Ambiente Virtual

```bash
# Criar ambiente
python -m venv venv

# Ativar ambiente
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
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

#### 4. Baixar Dados PISA 2018 (se necessário)

Se os arquivos não estiverem no repositório:

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

# Abrir: projeto2.ipynb
```

**Estrutura do Notebook:**

1. **Setup:** Importação de bibliotecas e configuração
2. **Carregamento de Dados:** Leitura de STU_BRA e SCH_BRA
3. **Preparação:** Merge, criação de variáveis, tratamento de missings
4. **Análise Exploratória:** Estatísticas descritivas, correlações, gráficos
5. **Modelos Multinível:** M0 (nulo) → M1 (ESCS) → M2 (contextual) → M3 (gestão) → M4 (interações)
6. **Resultados:** Tabelas de coeficientes, testes de hipótese, visualizações
7. **Sensibilidade:** Matemática, diferentes controles
8. **Conclusões:** Síntese e implicações

### Opção 2: Scripts Python

```bash
# 1. Preparar dados
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

## 📈 Resultados Esperados

### 1. Estimativa do ICC (Q1)

**Resultado esperado:**
```
ICC (Leitura) ≈ 0,30 - 0,40 (30-40%)
```

**Interpretação:**
- 30-40% da variância em Leitura está **entre escolas**
- 60-70% da variância está **dentro de escolas** (entre alunos da mesma escola)
- Brasil apresenta ICC alto comparado a países mais equitativos (Finlândia ~10%)

### 2. Efeito Contextual (Q2)

**Resultado esperado:**
```
γ(ESCS_centered) ≈ 25-30 pontos por DP     (efeito individual)
γ(ESCS_mean) ≈ 50-70 pontos por DP         (efeito composição)
```

**Interpretação:**
- **Sim**, ESCS médio da escola tem efeito **além** do ESCS individual
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
Eixo Y: READ
Cores: Escola pública (vermelho) vs. privada (azul)

Resultado esperado:
- Escolas privadas: intercepto mais alto, gradiente mais plano
- Escolas públicas: intercepto mais baixo, gradiente mais íngreme
```

#### Gráfico 2: Efeito do Clima no Gradiente
```
[Gráfico de interação]
Eixo X: ESCS
Eixo Y: READ
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

```bibtex
@mastersthesis{linhares2025efeito,
  author  = {Linhares, Fábio},
  title   = {Efeito Escola e Gradiente Socioeconômico no Brasil: Quantificando o Papel da Gestão e do Clima Escolar na Equidade Educacional},
  school  = {Universidade Federal de Alagoas},
  year    = {2025},
  type    = {Projeto de Pesquisa},
  note    = {Disciplina: Inteligência Artificial Aplicada à Educação. Orientador: Prof. Dr. Ig Ibert Bittencourt Santana Pinto}
}
```

### Reconhecimentos

- **OECD** pela disponibilização dos dados PISA
- **INEP** pela coordenação do PISA no Brasil
- **Prof. Dr. Ig Ibert Bittencourt** pela orientação e suporte metodológico
- **Comunidade EDM** pelas discussões e feedback

---

## 📞 Contato

**Autor:** Fábio Linhares  
**Instituição:** Universidade Federal de Alagoas (UFAL)  
**Disciplina:** Inteligência Artificial Aplicada à Educação  
**Orientador:** Prof. Dr. Ig Ibert Bittencourt Santana Pinto  

---

<p align="center">
  <sub>Desenvolvido com 📊 e ☕ para promover equidade educacional no Brasil</sub>
</p>

<p align="center">
  <a href="#-resumo-executivo">⬆ Voltar ao topo</a>
</p>
# EDM---Efeito-Escola-e-Gradiente-Socioecon-mico-no-Brasil-PISA-2018-
