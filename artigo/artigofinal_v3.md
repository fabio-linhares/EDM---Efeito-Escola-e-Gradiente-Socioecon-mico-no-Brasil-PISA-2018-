<p align="center">
  <img src="https://ufal.br/ufal/comunicacao/identidade-visual/brasao/ods/ufal_ods1.png" alt="Logo da UFAL" width="600"/>
</p>

<h1 align="center">Efeito Escola e Gradiente Socioeconômico no Brasil: A Lição do "PISA Shock" sob Análise nos Dados de 2018</h1>
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


## Resumo

Inspirado pelas reformas educacionais pós-"PISA Shock" na Alemanha, que focaram no clima escolar como alavanca de equidade, este artigo investiga se premissa similar se aplica ao Brasil. Analisamos o efeito escola utilizando microdados do PISA 2018 de alunos (*n* = 10.691) e escolas (*n* = 597) por meio de modelos de regressão ponderada (WLS) e modelos multinível (MixedLM) com intercepto e inclinação aleatórios. O pipeline de Mineração de Dados Educacionais (EDM) incluiu a união das bases STU_BRA, FLT_BRA e SCH_BRA, reversão de escalas WLE, imputação múltipla (IterativeImputer) e agregação ponderada. Os resultados mostram que climas organizados elevam a média de proficiência (+6 a +7 pontos), confirmando a H2. No entanto, ao contrário da expectativa teórica, a interação ESCS × clima é positiva (≈ +1 ponto), tornando o gradiente mais íngreme e refutando a H1 (a "lição alemã" de equidade). O coeficiente de correlação intraclasse (ICC) manteve-se alto (0,22–0,26), indicando que 22–26% da variância persiste entre escolas. Discutimos por que, no Brasil, a melhoria do clima pode não ser suficiente para gerar equidade, apontando limitações (ausência de PVs e BRR) e diretrizes de reprodutibilidade.

**Palavras-chave:** PISA 2018; PISA Shock; efeito escola; gradiente socioeconômico; modelos multinível; clima escolar; equidade.

---

## 1. Introdução

Quando a Alemanha recebeu seus resultados do PISA 2000 e se viu abaixo da média da OCDE, a reação nacional ficou conhecida como "PISA Shock"[101]. Esse "choque" desencadeou profundas reformas, com um foco renovado não apenas em padrões de ensino, mas em fatores institucionais governáveis, como a gestão e o clima escolar[32][33]. A literatura sugere que parte da subsequente recuperação alemã esteve ligada à premissa de que um clima escolar positivo e organizado poderia servir como um motor duplo: elevar a proficiência média (qualidade) e, crucialmente, reduzir a dependência do desempenho em relação à origem socioeconômica (equidade), achatando o gradiente.

O Brasil, embora não tenha tido um "choque" singular, enfrenta cronicamente os mesmos desafios: baixo desempenho médio no PISA e um dos gradientes socioeconômicos mais íngremes entre os países participantes. A eficácia escolar, portanto, torna-se central no debate de políticas públicas.

Este estudo importa a premissa alemã para o contexto brasileiro. Investigamos se as lições do PISA Shock se aplicam aqui: será que fatores institucionais, como o clima disciplinar, atuam como moderadores da desigualdade?

### 1.1 Perguntas e Hipóteses de Pesquisa

Buscamos responder às seguintes perguntas:

- **Q1:** Quanto da variância nas proficiências de Leitura, Matemática e Ciências está entre escolas (ICC)?
- **Q2:** O clima escolar e o ESCS médio da escola agregam poder explicativo além do ESCS individual?
- **Q3:** Escolas com melhor clima/gestão apresentam gradientes socioeconômicos mais planos (achatados)?

Três hipóteses guiam a investigação:

- **H1 (A Hipótese da Equidade):** Inspirada na "lição alemã", esperamos que o clima disciplinar eficaz reduza a inclinação ESCS → proficiência (gradiente mais plano).
- **H2 (A Hipótese do Desempenho):** As mesmas condições elevam as médias de proficiência, controlando a composição socioeconômica.
- **H3 (A Hipótese da Variância):** A introdução de variáveis de clima/gestão deve reduzir o ICC, explicando parte do "efeito escola".

---

## 2. Dados e Preparação

### 2.1 Abordagem EDM

Todo o pipeline segue a lógica de Mineração de Dados Educacionais: ingestão de múltiplas bases PISA, tratamento minucioso (reescalonamento, imputação, agregação ponderada) e aplicação de modelos explicativos. Não utilizamos algoritmos de machine learning de caixa-preta; privilegiamos regressões ponderadas e modelos multinível pela capacidade de interpretar efeitos e quantificar o gradiente socioeconômico — prática consolidada na literatura de EDM.

### 2.2 Fontes e Cobertura

- **STU_BRA.xlsx:** respostas dos estudantes (*n* = 10.691) com proficiências (READ, MATH, SCIE), índice ESCS, clima e controles.
- **FLT_BRA.xlsx:** escalas cognitivas e índices motivacionais (mesmas proficiências já agregadas; não há PVs nesta extração brasileira).
- **SCH_BRA.xlsx:** questionário dos diretores (recursos, clima, financiamento).

Todos os cálculos aplicaram o peso final SENWT, respeitando o plano amostral do PISA para representar a população de estudantes de 15 anos matriculados em escolas brasileiras.

### 2.3 Pipeline de Preparação

1. **Correção de IDs:** o CNTSTUID do FLT recebeu −50.000 para casar com STU (merge *one_to_one*).

2. **Reversão das escalas WLE:** índices como ESCS, DISCLIMA, JOYREAD, SCREADCOMP e BELONG foram convertidos de (valor + 5) × 1000 para a escala original (média 0, DP ≈ 1 ou 0–10 no caso de BELONG).

3. **Codificação de controles:** `gender_male` = 1 (menino), `repeat_flag` ∈ {0,1,2} (não repetiu, repetiu, sem informação).

4. **Imputação múltipla:** IterativeImputer (20 iterações, amostragem posterior) em ESCS, DISCLIMA, JOYREAD, SCREADCOMP, BELONG utilizando READ, SENWT, `gender_male`, `repeat_flag` e identificadores escolares como preditores.

5. **Agregação ponderada:** construção de `school_profile` com médias ponderadas (estat.wavg) de READ, MATH, SCIENCE, ESCS, DISCLIMA, BELONG, além de `n_students`, usando SENWT.

6. **Base analítica final:** `students_final` combina as variáveis individuais imputadas com os agregados de escola e foi usada em todas as análises de gradiente e modelos multinível.

### 2.4 Estatísticas Descritivas

| Variável | Média (SENWT) | DP (SENWT) | P10 | Mediana | P90 | Fonte |
|----------|---------------|------------|-----|---------|-----|-------|
| READ | 412,9 | 96,6 | 296,6 | 406,7 | 545,4 | STU_BRA |
| MATH | 383,6 | 80,9 | 288,5 | 374,8 | 493,6 | STU_BRA |
| SCIENCE | 403,6 | 85,1 | 301,7 | 395,2 | 522,7 | STU_BRA |
| ESCS (valor no arq.) | 4.706 | 2.659 | 1.853 | 4.717 | 8.403 | STU_BRA |
| DISCLIMA | 546,1 | 305,9 | 140,0 | 621,0 | 915,0 | STU_BRA |
| BELONG | 998,9 | 424,2 | 364,0 | 1.096,0 | 1.524,0 | STU_BRA |

Quartis de ESCS mostram saltos de ≈ 95 pontos em leitura entre Q1 (373,0) e Q4 (467,7), confirmando o gradiente bruto.

---

## 3. Modelos

### 3.1 Regressões Ponderadas (WLS)

**Modelo 1:** Proficiência ~ ESCS_c (ESCS centrado na média brasileira).

**Modelo 2:** Proficiência ~ ESCS_c + clima_escola_c + DISCLIMA + EDUSHORT + STAFFSHORT + gender_male + repeat_flag + ESCS_c × clima_escola_c.

Estimação via `statsmodels.WLS`, pesos = SENWT, uma especificação para cada domínio (Leitura, Matemática, Ciências).

### 3.2 Modelos Multinível (MixedLM)

`statsmodels.MixedLM`, grupos = CNTSCHID.

Modelos com intercepto aleatório e, em seguida, intercepto + inclinação aleatórios para ESCS_c.

Pesos normalizados (SENWT/ média de SENWT) quando suportado pelo solver; fallback para ajuste sem pesos em caso de singularidade.

---

## 4. Resultados

### 4.1 Gradiente Socioeconômico (Modelo 2)

| Domínio | Coef. ESCS_c | Coef. clima_escola_c | Interação ESCS×clima | R² |
|---------|-------------|----------------------|----------------------|----|
| Leitura | +9,43 (p < 0,001) | +6,81 (p < 0,001) | +1,11 (p < 0,001) | 0,375 |
| Matemática | +8,98 (p < 0,001) | +5,97 (p < 0,001) | +1,38 (p < 0,001) | 0,428 |
| Ciências | +9,13 (p < 0,001) | +5,52 (p < 0,001) | +1,45 (p < 0,001) | 0,413 |

**Interpretação:** O clima escolar organizado eleva o intercepto (desempenho médio) em ≈ +6–7 pontos, confirmando H2. No entanto, a interação ESCS × clima é positiva e significativa, indicando que o gradiente se torna mais íngreme em escolas com melhor clima. Isso refuta a H1.

### 4.2 ICC e Modelos Multinível

| Domínio | ICC | Var_between | Var_within | Coef. ESCS (nível 1) |
|---------|-----|-------------|------------|----------------------|
| Leitura | 0,222 | 1.444,9 | 5.057,0 | +3,13 |
| Matemática | 0,241 | 1.021,8 | 3.226,8 | +3,86 |
| Ciências | 0,256 | 1.195,3 | 3.477,3 | +4,22 |

**Interpretação:** ≈ 22–26% da variância permanece entre escolas, mesmo após adicionar moderadores. O efeito escola no Brasil é substancial e não foi explicado pelas variáveis de clima incluídas, não confirmando H3.

### 4.3 Resumo das Perguntas e Hipóteses

- **Q1:** ICC elevado (0,22–0,26) → efeito escola substancial. H3 (redução do ICC via clima) não confirmada.
- **Q2:** Climas favoráveis elevam os resultados médios → H2 confirmada.
- **Q3:** Interações positivas indicam gradientes mais íngremes em escolas com bom clima → H1 (Hipótese da Equidade) refutada.

---

## 5. Discussão: A Refutação da "Lição Alemã"

O resultado mais provocativo deste estudo é a refutação da Hipótese 1. Iniciamos com a premissa, inspirada nas reformas pós-PISA Shock, de que o clima escolar seria um motor de equidade. Nossos dados para o Brasil de 2018 sugerem o oposto.

Enquanto H2 foi confirmada (bom clima = notas médias mais altas), a interação positiva ESCS × clima implica que os alunos de ESCS mais alto se beneficiam mais de um clima organizado do que os alunos de ESCS mais baixo.

### 5.1 Por que isso ocorreria no Brasil?

**Efeito Mateus (Matthew Effect):** No contexto brasileiro, um clima disciplinar organizado pode ser uma condição necessária, mas não suficiente[95][96]. Alunos com maior capital cultural (tipicamente de ESCS mais alto) podem ser mais capazes de "aproveitar" essa organização e convertê-la em desempenho, enquanto alunos vulneráveis podem precisar de intervenções pedagógicas e de apoio mais diretas que o "clima" por si só não oferece.

**Segregação Oculta:** Embora controlemos para o ESCS médio da escola, é possível que escolas com "bom clima" no Brasil sejam, majoritariamente, aquelas que já praticam seleção de alunos ou que atendem a um público que valoriza esse tipo de ambiente, reforçando desigualdades existentes.

### 5.2 Implicações Políticas

A lição para o Brasil é que a melhoria da gestão e do clima, embora desejável e positiva para a média (H2), não é, isoladamente, uma política de equidade. Sem ações pedagógicas compensatórias e focalizadas nos alunos mais vulneráveis dentro dessas escolas, a melhoria do clima pode, inadvertidamente, ampliar o gap de desempenho.

---

## 6. Reprodutibilidade

**Repositório:** https://github.com/fabio-linhares/EDM---Efeito-Escola-e-Gradiente-Socioeconomico-no-Brasil-PISA-2018-

**Ambiente:** Python 3.13 (venv), dependências listadas em `requirements-pisa-edm.txt` (pandas, numpy, statsmodels, scikit-learn, matplotlib, seaborn, openpyxl, nbformat).

**Dados:** baixar PISA 2018 (Brasil) no formato XLSX e colocá-los em `pisa2018/stu`, `pisa2018/flt`, `pisa2018/sch`.

**Execução:** rode `projeto_pisa_edm.ipynb` ou o notebook de apresentação `notebooks/apresentacao_especialista.ipynb`. As estatísticas usadas neste artigo estão armazenadas em `outputs/weighted_summary.csv` e `outputs/quartil_summary.csv`.

**Código:** todos os scripts auxiliares estão em `scripts/`. A pasta `notebooks/` contém versões ricas dos resultados.

---

## 7. Limitações e Próximos Passos

### 7.1 Limitações

**Valores Plausíveis (PVs) Ausentes:** A principal limitação. A ausência de PV1READ…PV10READ impede a combinação oficial de erros-padrão descrita pela OCDE[51]. Usamos as estimativas WLE, que são suficientes para os coeficientes, mas os erros-padrão estão subestimados.

**Pesos Replicados (BRR) Indisponíveis:** Sem W_FSTR1…W_FSTR80, não foi possível estimar erros-padrão via Balanced Repeated Replication (BRR-Fay).

**Avisos de Singularidade nos MixedLM:** Será necessário testar especificações alternativas, checar resíduos e considerar penalizações.

**Indicadores de Liderança:** Incluir variáveis de governança (LEADCOM/LEADINST) pode esclarecer mecanismos institucionais além do clima.

### 7.2 Próximos Passos

A agenda futura clara é: (a) importar os PVs e pesos replicados para validar formalmente os erros-padrão e (b) testar outras variáveis de gestão escolar (liderança, colaboração docente) como moderadoras.

---

## 8. Conclusões

Retomando a questão inicial inspirada no "PISA Shock", este estudo traz um alerta para o Brasil. Nossos achados sugerem que a "lição alemã" — melhorar o clima escolar para obter equidade — não se aplica diretamente ao contexto brasileiro nos dados de 2018.

Confirmamos que o efeito escola é robusto (ICC ≈ 0,24) e que o clima escolar melhora o desempenho médio (H2). Contudo, nossa principal descoberta é que a melhoria do clima, isoladamente, parece beneficiar mais quem já é privilegiado (H1 refutada).

A implicação para políticas públicas é clara: investir na gestão e no clima escolar é importante, mas não é uma bala de prata para a equidade. Para achatar o gradiente, essas políticas precisam ser combinadas com ações pedagógicas focalizadas, como tutoria, reforço e alocação de recursos adicionais para os estudantes de menor ESCS dentro das escolas.

---

## Referências

ALVES, M. T. G.; SOARES, J. F. Eficácia das escolas públicas brasileiras. *Estudos em Avaliação Educacional*, São Paulo, v. 18, n. 36, p. 71-98, 2007.

ERNICA, M.; RODRIGUES, B.; SOARES, J. F. Desigualdades educacionais contemporâneas no Brasil. *Revista Brasileira de Educação*, Rio de Janeiro, v. 30, n. 1, p. 1-28, 2025.

LAUTERBACH, R. et al. PISA as an ideational roadmap for policy change: exploring Germany and England in a comparative perspective. *Journal of Education Policy*, v. 28, n. 4, p. 1-20, 2013.

MERTON, R. K. The Matthew Effect in Science. *Science*, v. 159, n. 3810, p. 56-63, 1968.

ORGANIZATION FOR ECONOMIC CO-OPERATION AND DEVELOPMENT (OECD). PISA 2018 Database. Paris: OECD Publishing, 2019. Disponível em: https://www.oecd.org/pisa/data/2018database/. Acesso em: 13 nov. 2025.

ORGANIZATION FOR ECONOMIC CO-OPERATION AND DEVELOPMENT (OECD). PISA 2018 Technical Report. Paris: OECD Publishing, 2020.

REANALYSIS of the German PISA Data: A Comparison of Different Approaches for Trend Estimation With a Particular Emphasis on Mode Effects. *Frontiers in Psychology*, v. 11, p. 1-13, 2020. Disponível em: https://www.frontiersin.org/articles/10.3389/fpsyg.2020.01231. Acesso em: 13 nov. 2025.

SCHWIPPERT, K.; STANAT, P. PISA 2000: Zusammenfassung der Ergebnisse für den deutschsprachigen Raum. *Zeitschrift für Erziehungswissenschaft*, Berlin, v. 5, n. 2, p. 276-292, 2002.

STANAT, P.; PEKRUN, R. PISA: Schülerleistungen im internationalen Vergleich. In: ROST, D. H. (Org.). *Handwörterbuch Pädagogische Psychologie*. 4. ed. Weinheim: Beltz, 2010. p. 560-569.

THE power and paradoxes of PISA: Should Inquiry-Based Science Education be sacrificed to climb on the rankings? *Frontiers in Education*, v. 3, p. 1-13, 2018. Disponível em: https://www.frontiersin.org/articles/10.3389/feduc.2018.00003. Acesso em: 13 nov. 2025.

WALDOW, F. Central European perspectives on the transnational policy influence of the OECD. In: BREAKSPEAR, S. (Org.). *Power and Policy in Education: The Role of Ministries*. Paris: OECD Publishing, 2012. p. 1-25.
