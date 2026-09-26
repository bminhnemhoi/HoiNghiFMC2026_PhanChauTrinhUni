<!-- manuscript/main.md: journal manuscript skeleton (task C4.8). Every result is a registry placeholder; design constants use the equals form and exist in configs; see manuscript/TODO_manuscript.md. Not for submission until make verify passes and every bracketed TODO is resolved. -->

# Whose Standard of Care? Attributing Deviations of Locally Run Open-Weight Large Language Models From Vietnamese Ministry of Health Guidelines to Foreign and Superseded Sources: Preregistered Audit Study

*Registered title (configs/project.yaml, OSF):* Whose Standard of Care? Jurisdictional Defaults, Guideline Staleness and Certified Abstention of LLMs on Vietnamese Ministry of Health Guidelines.
*[AUTHOR DECISION before the main runs: keep the registered title or adopt the scope-explicit title above. Under registration §5.3, the title is not rewritten after the results are seen.]*

**Article type:** Original Paper (JMIR Medical Informatics)

**Authors:** Binh Minh Ngo¹; Binh Thong Ngo²; Tran Doan Mai Huong³

¹ Faculty of Information Technology, Ton Duc Thang University, Ho Chi Minh City, Vietnam
² Faculty of Medicine, Phan Chau Trinh University, Da Nang City, Vietnam
³ Faculty of Odonto-Stomatology, Phan Chau Trinh University, Da Nang City, Vietnam

**Corresponding author:** Binh Minh Ngo, Faculty of Information Technology, Ton Duc Thang University, [postal address: TODO], Ho Chi Minh City, Vietnam. Email: ngobinhminh.st@tdtu.edu.vn

*[TODO before submission: ORCID iDs; one name order for all authors (the byline keeps the names exactly as the first author typed them); all authors approve the submitted version (ICMJE). The second and third authors are students of the faculties named above and are not described anywhere as physicians.]*

---

## Abstract

**Background:** Medical students and clinicians in Vietnam increasingly consult large language models (LLMs). Even when asked to follow the Vietnamese Ministry of Health (MoH), an LLM may give a value that is correct under a foreign guideline or a superseded MoH version: an answer that sounds authoritative but is not concordant with national guidance.

**Objective:** To measure how often locally run open-weight LLMs give non-MoH values where MoH and named foreign guidance differ, to attribute these values to named foreign systems or superseded MoH versions beyond chance, to test whether they persist when the exact MoH passage is supplied, and to evaluate certified abstention.

**Methods:** In this preregistered audit, we extracted span-verified recommendation atoms (doses, thresholds, drugs and schedules) from {{corpus.n_current|en}} MoH guidelines in force at the corpus freeze and linked each atom to dated values from named foreign systems (WHO, US, European or UK), to superseded MoH versions and to a rule-generated decoy. We ran {{runs.n_models|en}} open-weight 7B–9B models with four-bit weights on one laptop GPU, in Vietnamese and English, with no country cue (A0), an explicit MoH cue (A1), retrieval over the MoH corpus (A2) and the exact MoH passage (A3). A preregistered rule-based grader, not an LLM, labeled every answer. The primary hypothesis (H1) was that, under A1 in Vietnamese, foreign-value matches exceed decoy matches, tested with intervals clustered by conflict family. Checks usually done by people were done by dual AI audits with adjudication and a code-only cross-check. [Keep only if completed: student co-authors checked random samples.]

**Results:** Of {{atoms.n_total|en}} atoms, {{atoms.n_conflict|en}} were conflict atoms in {{atoms.n_families|en}} families. Under A1 in Vietnamese, the foreign-match rate was {{h1.pi_f|en}} and the decoy-match rate {{h1.pi_d|en}} (difference {{h1.delta|en}}, {{h1.delta_ci|en}}; excess over chance {{h1.excess|en}}, {{h1.excess_ci|en}}); H1 was {{h1.decision_text}}. Of non-concordant answers, {{h1.as|en}} ({{h1.as_ci|en}}) matched a named foreign or superseded source and {{h1.unattributed_share|en}} matched no recorded value. H2 (English prompts increase US-value matches) was {{h2.decision_text}} (Holm-adjusted P={{h2.p_holm|en}}). With the exact passage, foreign or superseded answers ranged from {{h3.r_min|en}} to {{h3.r_max|en}} across models (H3 {{h3.decision_text}}). The disagreement signal gave a risk ratio of {{h4.rr_mh|en}} ({{h4.rr_ci|en}}; H4 {{h4.decision_text}}). At a coverage of {{=0.5}}, certified risk bounds for the disagreement group ranged from {{rq3.u_disagree_c050_min|en}} to {{rq3.u_disagree_c050_max|en}}.

**Conclusions:** [OPTION A, H1 supported: Under an explicit MoH cue, these models gave foreign-guideline values more often than chance, and part of their deviation can be traced to named foreign systems or superseded MoH versions.] [OPTION B, H1 not supported: Under an explicit MoH cue, these models did not give foreign-guideline values measurably more often than chance; most deviations matched no recorded source.] [BOTH, wording chosen from the A3 results: Supplying the exact MoH passage reduced but did not remove non-concordant values.] The results describe locally run 7B–9B open-weight models, not commercial chatbots. Learners should check doses and thresholds against the current MoH document.

**Preregistration:** Open Science Framework [OSF DOI: TODO after human gate HG2.9].

**Keywords:** large language models; clinical practice guidelines; Vietnam; Ministry of Health; guideline adherence; jurisdictional bias; guideline versioning; selective prediction; preregistration; TRIPOD-LLM; medical education

---

## Introduction

Large language models (LLMs) have become part of how medical students look for clinical information; in a survey of medical students in Vietnam, most respondents reported familiarity with common artificial intelligence tools [@bui2026kap]. For a question about a dose, a threshold, a duration or a first-line drug, the reference that matters in Vietnam is the diagnosis and treatment guidance of the Ministry of Health (MoH). This guidance differs from foreign guidance in specific, checkable values. For example, its blood-pressure target for adults with diabetes without kidney complications or high risk differs from the target of the American Diabetes Association Standards of Care [@ada2025cvd]. It also changes: the national guidance for chronic hepatitis B, chronic obstructive pulmonary disease and community-acquired pneumonia, among others, was replaced in 2025–2026 [TODO-CITE: MoH decisions, from the frozen corpus manifest, checked at HG7.3]. An LLM may answer with a value that is correct under a WHO, US or European guideline, or under the replaced MoH version. Such an answer sounds authoritative, and a learner may not recognize it as non-concordant with national guidance.

Evidence suggests that this risk is real. When a question names no jurisdiction, LLMs tend to assume US institutional frameworks, more so when forced to give a single answer [@wang2026jurisdictional]. In neuroradiology vignettes on which US and non-US guidelines conflict, LLMs favored the US recommendation even when asked to follow the non-US guideline, and supplying the guideline restored most of the lost accuracy [@bazerbachi2026cultural]. Manual review of a frontier model's errors on a Chinese radiation oncology examination attributed a substantial share of them to divergence between US and Chinese guidelines [@zhou2026localization]. Vignettes that stated the country showed frequent deviations from that country's guidance [@nguyen2025gpchatgpt; @zeng2025geographic], and a hepatitis B case series found low concordance with an updated WHO guideline unless its text was supplied [@siepmann2025hepatitisb]. LLMs also rely on outdated medical recommendations [@wu2025driftmedqa; @vladika2025factsfade], are poorly aware of which version of medical knowledge applies at a given time [@guan2026temporal] and, in statutory question answering, rely on provisions that are no longer in force [@prior2026oldfriend].

National-guideline benchmarks exist for Kenya [@mutisya2025alama], the United Kingdom [@harris2025pubhealthbench], Germany [@schwietering2026cpgqade] and Brazil [@abonizio2026brazilian] and across many countries [@tan2026cpgbench], and Vietnamese medical question-answering datasets are being built [@nguyen2025vm14k; @tran2024vimedaqa; @nguyen2026vihermes]. These resources measure or improve performance; they do not ask which competing standard a non-concordant answer came from. The clinical studies above rely on at most a few dozen vignettes graded by clinicians, or attribute errors qualitatively after grading, and none separates guideline-attributable errors from chance agreement with an arbitrary value. Models sometimes keep their parametric answer against supplied evidence [@wu2024clasheval; @xie2023chameleon; @xu2024knowledgeconflicts], and retrieval failure explained most retrieval-augmented errors on national guidelines in one setting [@vach2026neurovascular]. To our knowledge, whether a model keeps a foreign or superseded value when given the correct national passage has not been measured value by value. Finally, LLMs rarely abstain under medical uncertainty [@cocchieri2026abstain], and accuracy-only evaluation rewards guessing [@kalai2026hallucinations]. Selective prediction with finite-sample guarantees [@angelopoulos2025learnthentest; @gurram2026selective; @salem2026hgcrc] and cross-lingual disagreement as an abstention signal [@feng2024abstain; @duwal2025mka] exist, but, to our knowledge, signals of guideline conflict have not been used to define the groups of a certified abstention layer.

We therefore designed a preregistered audit of locally run open-weight LLMs against the MoH guidance in force on a fixed corpus freeze date. Its core is value-level source attribution. Each span-verified recommendation atom carries dated values from named foreign systems, values from named superseded MoH versions linked through the documents' own supersession clauses, and a decoy generated by a fixed rule, so that foreign matches can be compared with matches to a value that belongs to no source. We evaluated open-weight 7B–9B models that run on one laptop GPU: institutions that cannot send queries to external services can deploy such models on premises, and other researchers can pin and rerun them. They are not the commercial chatbots that many students use, and we draw no conclusion about those.

We asked four questions. RQ1: under an explicit MoH cue, how often do these models answer conflict atoms with a foreign or superseded value, and what share of their non-concordant answers can be attributed to a named source at all? RQ2: how much deviation remains with retrieval or with the exact passage, and is it due to retrieval failure or to the model keeping its own value? RQ3 (secondary): does a label-free disagreement signal separate higher-risk answers, and what selective risk can be certified at fixed coverage levels? RQ4 (exploratory): how are deviations distributed across the national framework of core clinical problems? US-centered defaults, the benefit of supplying guideline text, rule-based evaluation and national-guideline benchmarks have all been reported before. To our knowledge, the combination studied here has not: value-level attribution with a decoy control, for a Southeast Asian national standard with named supersession chains, in the national language and English, from no context to the exact passage.

---

## Methods

### Study Design and Reporting

This is an observational audit of LLM outputs against a document corpus. The units are guideline recommendations, not people. Every recommendation receives every level of the within-item factors (model, language, context condition and question format), so no random assignment is used; the few random procedures (multiple-choice option order and the RQ3 splits) are seeded and were fixed in the registration. The hypotheses, analysis sets, decision rules and analysis code were registered on the Open Science Framework (OSF) before any main-study output existed [OSF DOI: TODO after HG2.9]. A pilot was run, and its outputs were opened, before the registration was deposited; the section Preregistration and Deviations gives the timeline and every resulting change. We report according to the TRIPOD-LLM guideline [@gallifant2025tripodllm] (Supplement S6).

### Reference Standard

The reference standard is the MoH diagnosis and treatment guidance (ministerial decisions and circulars) in force on October {{=15}}, 2026, the corpus freeze date, for the population stated in each question. The study measures fidelity to Vietnamese guidance, not medical correctness: an answer concordant with MoH guidance may be clinically debatable, and a non-concordant answer may be defensible elsewhere. When two current MoH documents give different values for the same population, every current value counts as concordant; the MoH value set is their union, taken within the same level of care (decision rule DR8), and such internal inconsistencies are counted and reported. Answers that differ from MoH guidance are called non-concordant, never incorrect, wrong or harmful.

### Guideline Corpus and Supersession Chains

We catalogued candidate MoH decisions and circulars and classified each by validity, availability of an official PDF and presence of a text layer (Supplement S1). Documents were downloaded only from official hosts (kcb.vn, moh.gov.vn, vncdc.gov.vn, and official pages of provincial health departments and hospitals), and the URL, download date and SHA256 hash of every file were recorded. Unofficial legal aggregators were never scraped.

Eligible documents were current, had an official PDF and were issued on or before the freeze date. They were ranked by a mechanical rule: first, documents cited by the seed table of candidate conflicts compiled during protocol development ({{design.seed_rows|en}} rows) or by a pilot atom; then text-layer PDFs issued in 2025–2026; then other text-layer PDFs, most recent first; and last, scanned PDFs, most recent first. Documents were included in this order until {{=35}} were included, with at most {{=10}} documents that needed optical character recognition (OCR); the registered target was {{=25}}–{{=35}} current guidelines. If fewer than {{=400}} conflict atoms or {{=25}} conflict families resulted, the next eligible documents in the same order were added before the freeze (DR2). Documents issued after the freeze were not added (DR7); if such a document superseded a corpus document, the affected atoms were flagged for a sensitivity analysis.

Supersession chains were built from each document's own clauses on which earlier documents it replaces, including partial amendments, and recorded for every atom. Examples are the hepatitis B guidance, in which Decision 1740/QĐ-BYT of 2026 replaced Decision 3310/QĐ-BYT of 2019; dengue, in which Decision 2760/QĐ-BYT of 2023 replaced Decision 3705/QĐ-BYT of 2019; and multidrug-resistant tuberculosis, in which Decision 162/QĐ-BYT of 2024 replaced Decision 2760/QĐ-BYT of 2021. The chains were checked a second time, separately [TODO: state by whom: AI audit, code, or the second author]. Superseded documents supply version values only and do not count toward the current corpus. The included guidelines and their predecessors are listed in Table 1.

### Recommendation Atoms and Verbatim Verification

An atom is one recommendation with a checkable value for a stated population. It records the source (document number and year, section, page and verbatim span); the clinical context (population, condition and intervention); the slot type (dose, threshold, duration, schedule, first-line drug, classification, target or procedure); the value kind (numeric, blood pressure, schedule, drug set or category); the MoH value set, which may be a range, a set of drugs or several co-valid values; and the counterpart values described in the next section.

Atoms were extracted by an AI agent (Claude, Anthropic) with a fixed JSON schema, one section at a time. The protocol had planned a low-cost commercial LLM for this step; it was replaced because the study uses no paid application programming interface (API). An atom was kept only if its value appeared verbatim in the recorded source span after number normalization (span verification by code). Values read from OCR pages were checked against the page image.

Every conflict atom then underwent a context check against a written rubric, done by the AI audit protocol described below. The rubric confirms that population, disease and intervention match between the MoH value and each foreign value. It also requires that conditional clauses in the MoH text (for example "may be lower if tolerated" or "at most") be encoded as open bounds or the atom be removed; that MoH values of neighboring contexts (another step of the same protocol, another population or another level of care) be recorded with page and span; that computed rather than verbatim values be flagged as derived and ignored in the primary analysis; that the categorical population attributes that decide the MoH value (for example HBeAg status, trimester or level of care) be listed with Vietnamese and English synonyms, so that questions must state them; that drug and category atoms record whether the MoH text states a preferred option, acceptable options or an exhaustive list; and that each atom receive an acuity level from a registered topic list.

Extraction quality was estimated on a stratified sample of {{=200}} atoms ({{=100}} random and {{=100}} conflict atoms), checked by the AI audit and by the code-only cross-check. Precision is reported with a Clopper–Pearson interval [TODO-CITE Clopper and Pearson 1934]. A lower limit below {{=0.90}} triggered re-extraction of the affected part, and, after a second failure, restriction to slot types meeting the threshold (DR1). The number of false conflicts among the checked conflict atoms feeds the tipping-point analysis described below. Before the atom freeze, code checked that every atom had an effective date on or before the freeze date, that tolerance and conflict status equaled their recomputation, and that every conflict atom had passed the context check and carried its conflict family and decoy fields.

### Foreign and Superseded Counterparts

Foreign values were kept in a versioned store. Each record holds the system, the source document, its version date, the URL, the location of the value in the source, the fetch date and the SHA256 hash of the cached page. Systems are WHO global guidance, the WHO Western Pacific Region, US sources, European or UK sources, and other named international bodies where relevant (for example, resuscitation and allergy organizations for anaphylaxis). Earlier WHO versions are kept as separate records. Only values and citations are stored and released, never passage text of copyrighted foreign guidelines. For each conflicting foreign value, counterpart matching also recorded the earliest dated version of that system's guidance known to contain the value, with a verbatim quote or table cell and its location, or "unknown"; this date is used only in the knowable-value analysis. Superseded MoH values were taken from the superseded documents with page and span.

Conflict status is computed by code from the gaps between value items. For numeric and blood-pressure atoms, the tolerance is half the smallest positive gap between any MoH item and any other recorded item (foreign, superseded or decoy), so that no tolerance window can overlap the MoH set; for other value kinds, the tolerance is zero and any difference is a gap. An atom is a conflict atom if at least one foreign value lies outside the MoH value set and can be told apart from every superseded value and from the decoy; atoms whose foreign and superseded or decoy values cannot be told apart are "indistinguishable" and are excluded from every confirmatory test. The remaining statuses are "concordant" (no foreign value outside the MoH set) and "no counterpart". A conflict family groups conflict atoms that share one root discrepancy, assigned mechanically: the same slot type, value kind and unit, the same MoH value set and the same nearest conflicting foreign value. Families can span guidelines and are the cluster unit of H1–H3. For each conflict atom, k_i counts the distinct conflicting foreign value items. An atom is US-unique (the H2 analysis set) if every conflicting US value is distinguishable from every non-US foreign value, every superseded value and the decoy.

Matching quality was measured as sensitivity against the seed table and as precision on {{=100}} randomly chosen automatic pairs checked by the AI audit, each with a Clopper–Pearson interval.

### Rule-Generated Decoys

Each conflict atom carries one decoy: a value of the same kind and unit as the MoH value, about as far from it as the nearest conflicting foreign value, that belongs to no recorded source (including MoH values of neighboring contexts). The decoy measures how often an answer hits a non-MoH value by chance. For numeric and blood-pressure atoms, the decoy mirrors the nearest conflicting foreign value through the MoH value (arithmetically, geometrically when the arithmetic mirror would not be positive, and on the logarithmic scale for viral loads), rounded by a fixed rule and accepted only if code confirms that it is distinguishable from every recorded value and does not change the atom's status. For schedule, drug and category atoms, an agent proposed a real-looking alternative that belongs to no recorded source, and the same code check applied. The decoy rule and rounding were frozen with the atom before any output existed (Supplement S2).

Every conflict-atom decoy was rated for plausibility, blind to any output, against a written rubric: the same granularity as the source values, inside the range ever used for the parameter, and not equal to a neighboring, foreign or historical value. An implausible decoy was regenerated by a pre-specified rule (rounding to the source granularity, else borrowing a foreign value of another atom of the same kind) and rated again. Conflict atoms without an acceptable decoy keep their status but are excluded from H1 and H2 and are counted.

### Question Sets

Questions were built from fixed templates for each slot type and paraphrased by an AI agent (Claude); code checked that numbers, units and the population were preserved. Each atom has a short-answer question in Vietnamese and in English. The English questions were translated by an AI agent, checked for numbers and negation by machine back-translation, and flagged if edited by hand. Code removed any question that leaked a recorded value, omitted a number of the population description or a required population attribute, or differed between languages in numbers or negation. A question whose stated population would make the foreign value also concordant under MoH guidance was rewritten or removed; the AI audit checked every question of every conflict atom for this ambiguity.

Atoms with a planted non-MoH value, a decoy and a single distinct MoH item also received a multiple-choice question with four options: the MoH value, the nearest conflicting foreign value, a verbatim superseded value (or a rule-generated filler), and the decoy. Each question was asked in two option orders: a seeded permutation (seed {{=20260926}}) and the same permutation rotated by two positions, so that every option changes letter. For the exact-passage condition, code cut an oracle passage of {{=150}}–{{=300}} words around the source span at sentence boundaries; the passage always contains the span verbatim, page furniture (signature blocks, stamps and personal names) was removed, and passages that themselves state a foreign, superseded, decoy or neighboring value were flagged. For retrieval, documents were split into chunks of at most {{=500}} tokens with the gold chunk identified. Vignettes set in a Vietnamese district hospital, without an MoH cue, were written for the exploratory condition A6, and at least {{=100}} of them were checked [TODO: by the AI audit, and by the second author for clinical plausibility if done]. Questions, grading rules and prompts were frozen together with SHA256 checksums before any main-study model run.

### Models, Conditions and Runs

Four open-weight models were registered, in this run order: Qwen3-8B with thinking disabled, Sailor2-8B-Chat, Vistral-7B-Chat and Llama-3.1-8B-Instruct (Table 2; model cards [TODO-CITE]). All were run locally through Ollama (llama.cpp) with GGUF weights at four-bit quantization (Q4_K_M, or Q4_0 for Vistral-7B-Chat, for which no public Q4_K_M file exists) on one laptop with an NVIDIA RTX {{=4050}} Laptop GPU ({{=6}} GB of video memory). According to their developers, Qwen3-8B lists Vietnamese among its supported languages, Sailor2-8B-Chat was further pretrained for Southeast Asian languages, and Vistral-7B-Chat was adapted for Vietnamese; Vietnamese is not among the officially supported languages of Llama-3.1-8B-Instruct, and its Vietnamese results are read with that in mind [TODO-CITE model cards]. No commercial or API model was evaluated. An optional smaller model (`gemma4:e4b-it-qat`, or `gemma3:4b` if it did not fit in memory) could be run only as an exploratory analysis and is never pooled with the four registered models. Model tags, digests, the Ollama version ({{runs.ollama_version}}) and run dates were recorded.

The training-data cutoff of each model was recorded from its developer's documentation. Only Llama-3.1-8B-Instruct has a stated cutoff (December 2023). For Qwen3-8B (release, April 2025), Sailor2-8B-Chat (weight upload, December 2024) and Vistral-7B-Chat (GGUF upload, January 2024), the release or upload date is used as an upper bound on the unknown cutoff; no cutoff was estimated or guessed.

A0 poses the question with no context and no country cue (descriptive "default standard"). A1 prefixes the cue "According to the current diagnosis and treatment guidelines of the Vietnamese Ministry of Health" (confirmatory for H1 and H2). A2 supplies passages retrieved from the MoH corpus by hybrid dense and sparse retrieval with BAAI/bge-m3 [TODO-CITE], k={{=5}}, and requires a citation line (the deployment answer used for H4 and RQ3). A3 supplies the exact MoH passage (H3). A4 supplies the full relevant chapter, at most {{=28000}} tokens, on a subset of {{=300}} questions for Qwen3-8B and Llama-3.1-8B-Instruct, for comparison with Bazerbachi et al [@bazerbachi2026cultural]. A5 (retrieval over a mixed MoH, WHO and US corpus) and A6 (vignettes) are exploratory. A1 is a controlled probe, not the way students usually ask; A0 and A6 are closer to practice and are reported descriptively. Every question ends with a required answer line ("ĐÁP ÁN:" or "ANSWER:" followed by value and unit). The verbatim prompts are in Supplement S3.

Decoding was greedy (temperature {{=0.0}}, seed {{=0}}), with at most {{=128}} new tokens for short answers and {{design.mcq_max_tokens|en}} for multiple-choice questions, and a context window of {{design.num_ctx|en}} tokens for A0–A3. At A2, five additional answers were sampled for the RQ3 consistency signal (temperature {{=0.7}}, top-p {{=0.95}}). Throughput measured before the main runs was about {{compute.sec_per_request|en}} seconds per request. The resource rule DR6 applied if the forecast laptop time exceeded {{design.dr6_hours|en}} hours: conditions were cut in the registered order A5 and A6, then A4, then one model (the last in the run order that had not completed A1 and A3), always keeping A1 and A3. The cuts applied were {{runs.dr6_text}}, registered in the freeze addendum before any main run. A model that did not run at its registered quantization was replaced by the nearest public four-bit file of the same model (DR10), and Llama-3.1-8B-Instruct was replaceable by a registered candidate list if access was not granted (DR11). Each call recorded the model identifier and digest, date, prompt hash, retrieved chunk identifiers, raw output, token counts, finish reason and, where the runtime returns it, the mean token log-probability of the answer span. A run cell (model × condition × language × format) was complete when at least {{design.run_valid_min_pct|en}} of its planned requests were valid; failed requests were retried once, and completed requests were never rerun. GPU inference may be slightly nondeterministic even with greedy decoding; each request was run once and the recorded output is the observation.

### Rule-Based Grading

Every response received exactly one label, checked in the fixed priority order below [TODO: set as a numbered textbox at typesetting]:

| Label | Name | Meaning |
| --- | --- | --- |
| L1 | Correct and context-aware | Gives the MoH value and explicitly attributes a different value to a named foreign body or country, or (at A0 only) asks which country applies |
| L2 | Correct | Contained in the current MoH value set |
| L3 | Version drift | Matches a superseded MoH version |
| L4 | Foreign match | Matches at least one named foreign system; the systems and source versions are recorded |
| L5 | Unattributed | A value matching no recorded source; a decoy match is flagged within L5 |
| L6 | Self-abstention | No value given |

Labels L3–L5 are called non-concordant with MoH guidance. "Unattributed" means only that the value matched no value in the reference set; it includes format errors, unit errors and values that lie between recorded sources, and it depends on how completely the reference set covers other guidelines. It does not mean that the value was fabricated.

The grader is deterministic code (Supplement S4). It reads the last answer line, or the whole output if there is none; parses numbers in Vietnamese and English formats, ranges, comparison signs and units; converts units using the atom's own context (for example, concentration or body weight) and never without it; maps drug names and named regimens to International Nonproprietary Names through synonym tables; and compares values with the tolerance of the atom. An answer that states several distinct values, not all in the MoH set, is L1 only if every non-MoH value is attributed to a named foreign body or country, and otherwise L5. A drug class named without its form is graded once per member of the class, and conflicting readings give L5. Multiple-choice answers are graded by the recorded role of the chosen option. The grader uses the condition in one place only: asking which country applies counts as L1 only at A0. The version frozen for the main study was grader_version {{grader.version_frozen}}; the pilot was graded with version {{=1.2.0}} (see Preliminary Feasibility Study).

An LLM was used only to extract an answer string from responses that had no answer line and several candidate values: a fixed extraction prompt, given the question and the output but no reference value, was run by an AI agent (Claude), and the extracted string was then graded by the same rules. No LLM assigned a label.

The grader was validated three ways. First, before the question and grader freeze, it was validated on held-out atoms that were not in the pilot: {{design.gv_atoms_per_stratum|en}} atoms from each of three strata (conflict, version drift, other), drawn with a seeded shuffle, with the greedy short answers of Qwen3-8B at A1 and A3 in both languages (about {{design.gv_responses_approx|en}} responses). The reference label of each response came from the AI audit, whose passes did not see the grader's label. The grader was accepted if its accuracy was at least {{design.gv_acc_min|en}} and the lower limit of the design-effect Clopper–Pearson interval, with atoms as clusters, was at least {{design.gv_lcl_min|en}}; otherwise it was corrected from self-written test cases and validated once more on a new sample. These validation atoms are excluded from H1–H4 and RQ3 because their main-study outputs were seen before the freeze. Second, the answer extractor was checked on {{=500}} responses stratified by language, model and condition; if extraction errors or the rate of responses needing extraction exceeded the registered threshold for any model or language, the grader was fixed, its version incremented, every response regraded and both results reported (DR9). Third, the precision of L1 was checked on {{design.label1_check_n|en}} responses stratified by language and condition, and the precision and recall of L6 are reported next to every self-abstention rate.

### Verification Protocol: AI Audits, Code-Only Cross-Check and Co-Author Sample Checks

The protocol assigned several checks to people. The first author delegated them to an AI audit protocol, and no clinician took part. Each audited item was checked by two separate, blinded passes of Claude agents: pass A followed a written checklist, and pass B was instructed to be skeptical and to read the PDF page or page image before the recorded values. Neither pass saw the other's verdict, and an AI adjudicator decided every disagreement. In response checks, the passes saw the question, the reference values, the output and the parsed value, but not the model identity or condition; retrieval citation lines, which would reveal A2, were removed, and items were shown in a seeded random order. Agreement between passes before adjudication is reported as percent agreement with a Clopper–Pearson interval and as Cohen κ. The audit covered the context check of every conflict atom, the {{=200}}-atom quality sample, the {{=100}} counterpart pairs, decoy plausibility, question ambiguity, the held-out grader validation, the extractor check and the L1 check. The auditors belong to the same model family as the agents that extracted the atoms and drafted the grader, so their errors may be correlated; we therefore write "checked by AI, not by a person" wherever such a check is reported.

A code-only cross-check that uses no language model ran on every atom: it confirmed that the verbatim span occurs on the stated PDF page, that every MoH value can be parsed back from the span by the grader's parser, and that the numbers and drug names of every foreign value occur in the hashed cached source. Population and context have no code equivalent and were checked by AI only. Agreement between this check and the AI audit is reported.

[PLANNED, NOT YET DONE; keep this paragraph only if completed, and state its registration status (addendum before the atom freeze, or unregistered and labelled as such).] The two student co-authors checked seeded random samples, blind to the AI verdicts. The second author (a student of the Faculty of Medicine) compared the span, value, unit, page and population of a sample of {{coauthor.atoms_n|en}} conflict atoms with the PDF page images and rated the clinical plausibility of {{coauthor.vignettes_n|en}} vignettes. The third author (a student of the Faculty of Odonto-Stomatology) labeled a sample of {{coauthor.labels_n|en}} graded responses without seeing the grader's label. Agreement between these student checks and the AI audit or the grader is reported with intervals. These are checks by students, not clinician review.

### Statistical Analysis

#### Outcome Indicators

For each greedy response, indicators are derived from the label inside the analysis code: concordant (L1 or L2), non-concordant value (L3, L4 or L5; defined on value-stating answers), version drift (L3), foreign match (L4), unattributed (L5), self-abstention (L6), decoy match (any parsed value that matches the decoy, whatever the label) and US-value match (L4 with the US system among the matched systems). All intervals are two-sided at the {{design.ci_pct|en}} level, and all tests are one-sided in the direction of the hypothesis, at level {{design.alpha_one_sided|en}}.

#### H1 (Primary)

H1 states that, under A1 with Vietnamese questions and pooled open models, answers match foreign values more often than they match the chance-coincidence control. The analysis set is the greedy short-answer response of each model to each conflict atom that has a frozen decoy. The foreign-match rate π_f is the share of responses labeled L4, and the chance rate π_d is the share of decoy matches weighted by k_i, because L4 can be met by matching any of k_i foreign targets while each atom has one decoy; this weighting is conservative, and the unweighted rate is a registered sensitivity analysis. With N the number of valid responses pooled over models:

```math
π_f = Σ F_mi / N,   π_d = Σ k_i · D_mi / N,   Δ = π_f − π_d,   E = (π_f − π_d) / (1 − π_d)
```

Intervals and tests resample whole conflict families with {{design.bootstrap_b|en}} bootstrap replicates [TODO-CITE Field and Welsh 2007]. H1 is supported only if the lower limits of the bias-corrected and accelerated (BCa) interval [TODO-CITE Efron 1987], the expanded BCa interval and the cluster jackknife-t interval of Δ are all above zero, and the one-sided P value of the wild cluster restricted bootstrap-t [TODO-CITE Cameron, Gelbach and Miller 2008; MacKinnon and Webb 2017] is at most {{design.alpha_one_sided|en}}. This intersection–union rule is stricter than the protocol's BCa-only rule, which rejected true nulls above the nominal level in simulations with few or unequal families; the simulated operating characteristics of every registered rule are in Supplement S5. With fewer than {{design.small_cluster_min|en}} clusters, the jackknife-t replaces the bootstrap intervals. H1 is its own family and is not adjusted for multiplicity.

Because H1 could be supported by a small effect, results are interpreted through π_f and the excess over chance E with their intervals, read against a smallest effect of practical interest of E={{=0.10}}, registered before any main-study data existed. E is described as practically important if its lower limit is at least {{=0.10}}, as not practically important if its upper limit is below {{=0.10}}, and as inconclusive otherwise; this reading never changes the H1 decision.

#### Attributable Share (Co-Primary Descriptive Outcome)

Reported with H1, on the same analysis set, among answers that state a non-MoH value (L3–L5), the attributable share is the proportion that matches a superseded MoH version or a named foreign system, (L3+L4)/(L3+L4+L5). Its complement, the unattributed share, is reported with the proportion of decoy matches within L5, and a chance-corrected share subtracts the expected number of chance foreign matches (k_i-weighted decoy matches) from the numerator. Intervals are family-clustered. The share involves no hypothesis test and never changes the H1 decision. It is also reported by model, language and condition.

#### Robustness and Sensitivity Analyses of H1

Four robustness analyses are reported next to H1: a directional correction for decoys that lie on the less attractive side of the MoH value (S1), H1 restricted to arithmetic-mirror decoys (S2), H1 restricted to decoys at least as round as the nearest foreign value (S3), and H1 without atoms whose foreign value coincides with a neighboring MoH value (N1). "H1 robust" is written only if S1 and S2 both support it. Also next to H1 are H1 without pilot and seed-table atoms (B.1), H1 on knowable pairs (B.26, below), H1 clustered by guideline instead of family (B.10), and H1 restricted to decoys rated plausible (B.11). If H1 holds with family clusters but not with guideline clusters, we state that the evidence depends on treating families as independent. A tipping-point analysis reports how many of the most influential conflict atoms would have to be false conflicts to overturn H1, compared with the upper confidence limit of the false-conflict rate from the quality sample. The full list of registered sensitivity analyses is in Supplement S5; none can reverse a confirmatory decision.

#### H2

H2 is a value-level replication of Wang and Suresh [@wang2026jurisdictional]: under A1, English questions yield more US-value matches than Vietnamese questions, on US-unique conflict atoms with a decoy. Pairs of responses (atom × model) with valid answers in both languages are compared by the clustered McNemar test of Durkalski et al [TODO-CITE Durkalski 2003], with conflict families as clusters, or by an exact sign-flip randomization test when fewer than {{design.small_cluster_min|en}} families contain a discordant pair. The effect size is the paired difference in US-match rates with a family-clustered interval. Few US-unique atoms may exist, and low power for H2 was acknowledged in advance.

#### H3

H3 states that, under A3 with Vietnamese questions, the rate of foreign or superseded answers (L3 or L4) on conflict atoms stays above {{=0.05}} in at least half of the open models. For each model, the one-sided P value for a rate at most {{=0.05}} and its interval come from a clustered exact interval (a design-effect Clopper–Pearson construction [TODO-CITE Korn and Graubard 1998]) with families as clusters. The per-model P values are combined by a Bonferroni partial-conjunction P value for "at least half of the models" [TODO-CITE Benjamini and Heller 2008], which is valid under any dependence between models. The literal protocol criterion (the number of models whose lower limit exceeds {{=0.05}}) is reported descriptively. H3 is also reported without passages that themselves state a non-MoH value (B.22), without pilot atoms (B.1) and on knowable pairs (B.26). A stubbornness rate, the share of L3 or L4 answers at A3, is reported descriptively on conflict and version-drift atoms together.

#### H4

H4 states that, with every question answered, answers in the disagreement group have at least twice the risk of stating a non-MoH value as answers in the agreement group. The analysis set is the served A2 greedy answers that state a value (L1–L5), in both languages, on all frozen atoms except indistinguishable and grader-validation atoms. Groups are formed without labels: an answer is in the disagreement group if its A1 answer differs from its A2 answer, if its Vietnamese and English A2 answers differ, or if no cited passage contains the answered value. The estimate is the Mantel–Haenszel risk ratio [TODO-CITE Mantel–Haenszel estimator], stratified by model and language, and the one-sided test of a ratio above {{=2.0}} uses the registered interval rule (without the wild bootstrap) over a bootstrap clustered by guideline.

#### Multiplicity

H2, H3 and H4 form one family, adjusted by the Holm step-down procedure [TODO-CITE Holm 1979] at a familywise one-sided level of {{design.alpha_one_sided|en}}. The family always has three members; a hypothesis that cannot be computed enters with a P value of one. Unadjusted intervals are reported alongside. Results against a hypothesis are reported with the same prominence as results for it.

#### Knowable Foreign Values

A foreign value cannot be a model's default if no recorded version of it existed before the model's training data were collected. For each model, a conflicting foreign value item is knowable if its earliest recorded dated version (or, failing that, the version date of its source) ends on or before the model's cutoff date; undated items are never knowable. H1 and H3 are recomputed on the pairs (atom, model) that have at least one knowable conflicting item, counting an L4 answer only if it matches a knowable item (B.26). L4 answers on pairs without a knowable item are reported as a separate exploratory row. For the three models whose cutoff is an upper bound, the knowable sets are upper bounds too, and "not knowable" means only that no recorded version is dated on or before that bound.

#### Descriptive and Exploratory Analyses

Descriptive analyses include the full label distribution by model, language and condition; foreign matches by system and source version; per-model estimates; the multiple-choice replication of H1 (averaged over the two option orders, with the decoy baseline weighted by the number of foreign options); the context ladder from A0 to A4; the split of A2 non-concordant answers into retrieval errors (gold chunk not among the top {{=5}}) and in-context errors, with retrieval recall; internal MoH inconsistencies; and controls (the concordant rate on concordant atoms at A1, the A3 check on concordant atoms, option-order agreement, answer-line compliance and truncation). A descriptive generalized linear mixed model with random effects for guideline and atom, fitted in R [TODO-CITE lme4; glmmTMB], relates non-concordance to model, language, condition and slot type, with a cluster-robust generalized linear model as a check [TODO-CITE sandwich; Pustejovsky and Tipton 2018]; no decision depends on it.

Exploratory analyses (labeled as such wherever reported) include the A0 default standard by language; version drift as a function of the months between the issue date of the current MoH guideline and the model's cutoff, modeled with a natural spline; a "latest-version" bias check among atoms with several dated versions of the same foreign system; A5 and A6; an exploratory breakdown of L5 [TODO: only if its subtypes are registered before the question freeze]; and RQ4, the distribution of deviations across the national framework of core clinical problems.

#### Missing Data

Missingness is reported for every run cell. The primary analyses use all valid responses without imputation. If a cell had more than the registered share of missing responses, H1, H3 and H4 are recomputed under two extreme imputations (all missing set to the outcome that favors the hypothesis, then to the outcome that disfavors it), and both results are reported.

### Certified Abstention (RQ3)

RQ3 asks what selective risk an abstention layer can certify. The served answer is the A2 greedy answer; the analysis is run separately for each model, on one Vietnamese answer per atom that states a value (English is secondary), with the loss defined as stating a non-MoH value (L3–L5). Pilot, grader-validation and indistinguishable atoms are excluded. Atoms are split at random into reference, calibration and test sets (fractions {{=0.2}}, {{=0.4}} and {{=0.4}}; seed {{=20261001}}), with every language and format of an atom on the same side.

A score for each answer comes from a penalized logistic regression fitted on the reference split only, with out-of-fold scores from a grouped split by guideline; its features are the three disagreement signals, the consistency of the five sampled A2 answers with the greedy answer and, where available, the mean token log-probability. For each of the two groups (agreement and disagreement) and each coverage level ({{=1.0}}, {{=0.75}}, {{=0.5}} and {{=0.25}}), thresholds are quantiles of the reference-split scores. The primary output is the set of simultaneous Clopper–Pearson upper bounds on the selective risk, computed on the calibration split with a familywise error of δ={{=0.10}} (Bonferroni over the group and coverage bounds of one model), so that all bounds of a model hold together with probability at least one minus δ. Learn-then-Test thresholds [@angelopoulos2025learnthentest] are reported as a secondary output, with target risk α={{=0.10}}, or {{=0.15}} for a group with fewer than {{=300}} calibration atoms (DR4), and the layer is declared not useful for a group if its certified coverage is below {{=0.30}} (DR5). The self-abstention rate of each model is reported next to the bounds, because overall coverage is the product of the model's own answering rate and the layer's coverage.

The guarantee of regime (a) holds only for questions drawn at random from the same frozen atom pool; it says nothing about other questions, other corpora or later guideline versions. Regime (b) assesses transfer empirically by {{=500}} leave-guideline-out splits in which the score is refitted on reference guidelines only and violations are counted on unseen test guidelines; transfer is called acceptable only if the violation frequency is at most {{=0.20}}. Cluster-level guarantees would need far more guidelines than the corpus holds [@dunn2023hierarchical]. Comparators are no abstention; abstaining on every disagreement answer; a single-group Learn-then-Test layer; conformal risk control [@angelopoulos2022crc]; and grouping by specialty in the style of hierarchical group-conditional risk control [@salem2026hgcrc]. Bounds are not simultaneous across models. If, for every model and language, the upper limit of the rate of foreign or superseded answers at A2 on conflict atoms is below {{=0.05}} (DR3), the primary conclusion becomes that retrieval over the MoH corpus suffices for these atoms, and RQ3 is reported as exploratory.

### Preliminary Feasibility Study (Pilot)

Before the registration was deposited, a pilot tested the pipeline. It used {{pilot.n_atoms|en}} hand-picked atoms from {{pilot.n_guidelines|en}} MoH documents: clean conflicts from the seed table and similar atoms, version-drift atoms from three supersession chains, and concordant controls. Qwen3-8B (the same local weights as in the main study) answered short-answer questions at A0, A1 and A3 in both languages and planted multiple-choice questions at A1 in two option orders ({{pilot.grader_n|en}} responses). The outputs were sealed with a recorded SHA256 hash before the citations of the pilot atoms were audited, and were opened afterwards. They were graded with grader_version {{=1.2.0}} and a list of exclusions declared before the run. Two blinded AI graders and an AI adjudicator then relabeled every response. The pilot outputs are a separate dataset and are never pooled with main-study data; main-study outputs for pilot atoms were regenerated from the frozen questions. The pilot results are summarized in the Results section and reported in full in Supplement S7.

### Preregistration and Deviations

The protocol (version of September 2026), the analysis plan and the analysis code were fixed in the first author's local git repository before the pilot outputs were opened. The registration text committed at that time committed the author to upload a timestamped copy to OSF before any pilot output was opened; this was not done, so no third-party timestamp precedes the opening of the pilot outputs, and the local commit is the only record. The registration was submitted to OSF on [DATE: TODO after HG2.9], before the corpus freeze and before any main-study output existed, together with a first addendum. That addendum gives the timeline and lists every change made since the last version committed before the opening (changes C1–C12), stating for each whether pilot outputs informed it (Supplement S8).

Changes not informed by pilot outputs were the move to a single laptop with locally run models and no paid API (C1), the absence of clinician review with code surrogates for clinical variables (C3), the local run settings (C6), the knowable-value analysis (C9) and the rebuilding of four A3 passages from a newer document (C11). Changes informed by the pilot outputs were grader_version {{=1.3.0}}, derived from the grader errors that the AI check of the pilot grades found (C4); the multiple-choice token limit (C5); the attributable share as a co-primary descriptive outcome (C7); the plan for interpreting a non-supported H1 or H3 (C8); and the safeguards for pilot atoms (C12). Two changes were partly informed (the details of the AI audit protocol, C2, and the statement of scope, C10). No hypothesis, H1–H4 analysis set, decision rule, α, δ or coverage level changed. Because the pilot atoms remain in the main atom set and Qwen3-8B with greedy decoding will reproduce similar outputs for them, grading changes informed by the pilot could make their main-study grades optimistic. The registered safeguards are that pilot atoms are never used to validate the grader, are excluded from RQ3, and that H1 and H3 without pilot atoms (B.1) are reported next to the main results. Later deviations are recorded in the decision log, filed as dated OSF addenda and listed in Supplement S8; analyses not in the registration are labeled exploratory.

### Ethical Considerations

The study involved no human participants and no patient data; it used only public documents and model outputs. No ethics review was sought, because no human participants were involved [TODO: authors confirm whether their institutions require a formal exemption statement]. MoH documents were obtained from official sources and are not redistributed; atoms are released as values, citations and page locations. Copyrighted foreign guidelines are represented only by values, citations and locations, never by passage text. Every released artifact is labeled "for research and evaluation, not for clinical decision-making". Concordance with MoH guidance does not imply medical correctness; the study assessed neither clinical harm nor whether an MoH value lags current evidence, and it uses code surrogates (for example, whether the foreign source postdates the MoH document) that are labeled as surrogates, not clinical judgments.

---

## Results

<!-- Results skeleton. Every number is a registry placeholder produced by analysis code; sentences are templates to be edited once the numbers exist. Do not open data/runs before the confirmatory analysis is run by code. -->

### Corpus, Atoms and Questions

The catalogue held {{corpus.n_catalogued|en}} MoH documents, of which {{corpus.n_catalogued_current|en}} were current. The frozen corpus comprised {{corpus.n_current|en}} current guidelines ({{corpus.n_ocr|en}} requiring OCR) and {{corpus.n_superseded|en}} superseded versions linked in {{corpus.n_chains|en}} supersession chains, including {{corpus.n_partial_amendments|en}} partial amendments (Table 1; Supplement S1). Extraction yielded {{atoms.n_total|en}} span-verified atoms: {{atoms.n_conflict|en}} conflict atoms in {{atoms.n_families|en}} conflict families ({{atoms.n_families_multi_guideline|en}} families spanning more than one guideline), {{atoms.n_concordant|en}} concordant atoms, {{atoms.n_no_counterpart|en}} atoms without a foreign counterpart and {{atoms.n_indistinguishable|en}} indistinguishable atoms. {{atoms.n_drift|en}} atoms had a distinguishable superseded value. Of the conflict atoms, {{atoms.n_conflict_decoy|en}} had an acceptable decoy and entered H1 ({{atoms.n_conflict_no_decoy|en}} did not), and {{atoms.n_us_unique|en}} were US-unique. Internal MoH inconsistencies (DR8) affected {{atoms.n_dr8|en}} atoms. The atom set includes {{atoms.n_pilot|en}} pilot atoms, which contributed {{atoms.h1_share_pilot|en}} of the H1 units, and {{atoms.n_gv|en}} grader-validation atoms excluded from confirmatory analyses. After quality checks, {{questions.n_short|en}} short-answer questions per language and {{questions.n_mcq|en}} multiple-choice questions (both languages and orders) were frozen; {{questions.n_removed|en}} questions were removed ({{questions.n_removed_ambiguity|en}} for ambiguity) and {{questions.n_translation_edited|en}} English questions were edited after machine translation. The workflow and counts are shown in Figure 1.

**Figure 1.** Study workflow: corpus catalogue and freeze, supersession chains, atom extraction and verification, counterpart matching, decoys and conflict status, question generation and quality control, model runs under A0–A3 (and A4–A6 where run), rule-based grading, and analyses. Counts at each step from the registry. [Generated by analysis code into results/figures as PDF and PNG; TODO: script name.]

**Table 1.** Guideline corpus: document, issuing decision or circular and year, topic and specialty, text layer or OCR, superseded predecessors, and numbers of atoms by conflict status. [Generated by analysis code into results/tables; inserted at build.]

| Guideline | Year | Topic | Text layer or OCR | Superseded predecessor(s) | Atoms | Conflict atoms |
| --- | --- | --- | --- | --- | --- | --- |
| [generated] | | | | | | |

### Data Quality

Extraction precision on the {{=200}}-atom quality sample was {{qc.extraction_precision|en}} ({{qc.extraction_precision_ci|en}}); DR1 was {{qc.dr1_text}}. Among the {{=100}} conflict atoms of the sample, {{qc.false_conflicts|en}} were false conflicts (one-sided upper limit {{qc.false_conflict_ucl|en}}). Counterpart matching had a precision of {{qc.matching_precision|en}} ({{qc.matching_precision_ci|en}}) on {{=100}} pairs and a sensitivity of {{qc.matching_sensitivity|en}} ({{qc.matching_sensitivity_ci|en}}) against the seed table. On the context check of conflict atoms, the two AI passes agreed on {{qc.audit_agree_pct|en}} of criteria before adjudication (κ={{qc.audit_kappa|en}}). The code-only cross-check found the span on the stated page for {{qc.code_span_ok_pct|en}} of atoms, parsed every MoH value back for {{qc.code_values_ok_pct|en}}, and agreed with the AI audit on {{qc.code_ai_agree_pct|en}}. Of conflict-atom decoys, {{qc.decoy_plausible_pct|en}} were rated plausible after regeneration ({{qc.decoy_regenerated|en}} regenerated). [Keep only if done:] Student checks agreed with the AI audit on {{coauthor.atoms_agree_pct|en}} ({{coauthor.atoms_agree_ci|en}}) of {{coauthor.atoms_n|en}} atoms and with the grader on {{coauthor.labels_agree_pct|en}} (κ={{coauthor.labels_kappa|en}}) of {{coauthor.labels_n|en}} responses.

In the held-out validation before the freeze, the grader's accuracy was {{grader.gv_accuracy|en}} ({{grader.gv_accuracy_ci|en}}) on {{grader.gv_n_responses|en}} responses in {{grader.gv_n_atoms|en}} atoms, and the grader was {{grader.gv_decision_text}} (per stratum and language, Supplement S4). The answer extractor was checked on {{=500}} responses: extraction error {{grader.extractor_err_pct|en}} ({{grader.extractor_err_ci|en}}); the highest rate of responses needing extraction for any model or language was {{grader.needs_llm_max_pct|en}}; DR9 was {{grader.dr9_text}}. L1 precision ranged from {{grader.label1_precision_min|en}} to {{grader.label1_precision_max|en}} across strata. L6 had a precision of {{grader.label6_precision|en}} and a recall of {{grader.label6_recall|en}}.

### Model Runs

The models run are listed in Table 2. The main runs produced {{runs.n_requests|en}} requests over {{runs.laptop_hours|en}} laptop GPU hours; every cell reached at least {{runs.valid_min_pct|en}} valid responses [or: cells below the threshold are listed in Supplement S5]. Answer-line compliance ranged from {{runs.answer_line_min_pct|en}} to {{runs.answer_line_max_pct|en}} across models and languages, and truncation of short answers from {{runs.truncated_min_pct|en}} to {{runs.truncated_max_pct|en}}. DR6 cuts: {{runs.dr6_text}}. Model replacements under DR10 or DR11: {{runs.dr10_dr11_text}}.

**Table 2.** Models: name, Ollama tag and digest, quantization, license, stated support for Vietnamese, training-data cutoff used and its basis (stated or upper bound), and conditions run. [Generated from configs/models.yaml group local_main and results/model_versions.json; inserted at build.]

| Model | Ollama tag and digest | Quantization | License | Cutoff used (basis) | Conditions run |
| --- | --- | --- | --- | --- | --- |
| [generated] | | | | | |

### RQ1: Deviation and Attribution Under an Explicit MoH Cue

Figure 2 shows the label distribution at A1 by model and language. On conflict atoms in Vietnamese, pooled over models, {{rq1.a1_vi_concordant_pct|en}} of answers were concordant (L1 or L2), {{rq1.a1_vi_l3_pct|en}} matched a superseded version, {{rq1.a1_vi_l4_pct|en}} matched a foreign value, {{rq1.a1_vi_l5_pct|en}} matched no recorded value and {{rq1.a1_vi_l6_pct|en}} gave no value. Context-aware answers (L1) were {{rq1.a1_l1_pct|en}}. On concordant atoms, where the MoH value equals the international value, {{rq1.a1_vi_control_correct_pct|en}} of answers were concordant.

**H1.** In {{h1.n_responses|en}} responses on {{h1.n_atoms|en}} conflict atoms in {{h1.n_families|en}} families, π_f was {{h1.pi_f|en}} ({{h1.pi_f_ci|en}}) and π_d was {{h1.pi_d|en}} ({{h1.pi_d_ci|en}}; unweighted {{h1.pi_d_unweighted|en}}). Δ was {{h1.delta|en}} ({{h1.delta_ci|en}}; one-sided P={{h1.p|en}}), and H1 was {{h1.decision_text}} (Table 3). The excess over chance E was {{h1.excess|en}} ({{h1.excess_ci|en}}), which is {{h1.sesoi_text}} against the smallest effect of interest. Foreign matches came from {{h1.systems_text}} (by system and source version in Supplement S5). Per model, Δ ranged from {{h1.delta_model_min|en}} to {{h1.delta_model_max|en}}.

**Attributable share.** Of non-concordant answers in the H1 set, {{h1.as|en}} ({{h1.as_ci|en}}) matched a named foreign system or superseded version and {{h1.unattributed_share|en}} matched no recorded value; decoy matches were {{h1.decoy_share_l5|en}} of L5 answers. The chance-corrected attributable share was {{h1.as_c|en}} ({{h1.as_c_ci|en}}).

**Robustness.** S1: {{h1.s1_delta_ci|en}}; S2: {{h1.s2_delta_ci|en}}; S3: {{h1.s3_delta_ci|en}}; N1: {{h1.n1_delta_ci|en}}; H1 is {{h1.robust_text}}. Without pilot and seed-table atoms (B.1), Δ was {{h1.b1_delta|en}} ({{h1.b1_delta_ci|en}}); on knowable pairs (B.26), {{h1.b26_delta|en}} ({{h1.b26_delta_ci|en}}); with guideline clusters (B.10), {{h1.b10_delta_ci|en}}; with plausible decoys only (B.11), {{h1.b11_delta_ci|en}}. L4 answers on pairs without any knowable foreign value numbered {{h1.l4_not_knowable|en}} (exploratory). The tipping point was {{h1.tipping_point|en}} atoms against a plausible number of false conflicts of {{h1.false_conflicts_plausible|en}}.

**Multiple-choice replication (secondary).** With the foreign and decoy options displayed side by side, Δ was {{rq1.mcq_delta|en}} ({{rq1.mcq_delta_ci|en}}); option-order agreement was {{rq1.mcq_order_agree_pct|en}}.

**H2.** On {{h2.n_atoms|en}} US-unique atoms ({{h2.n_pairs|en}} pairs; {{h2.n_discordant_families|en}} families with a discordant pair), the US-match rate was {{h2.rate_en|en}} in English and {{h2.rate_vi|en}} in Vietnamese (difference {{h2.diff|en}}, {{h2.diff_ci|en}}; {{h2.test_text}} one-sided P={{h2.p|en}}; Holm-adjusted P={{h2.p_holm|en}}). H2 was {{h2.decision_text}}.

**A0 default standard (exploratory).** With no country cue, US values were matched in {{rq1.a0_us_en_pct|en}} of English and {{rq1.a0_us_vi_pct|en}} of Vietnamese answers on conflict atoms, and models asked which country applied in {{rq1.a0_ask_country_pct|en}}.

**Figure 2.** Attribution of answers at A1 by model and language on conflict atoms: stacked shares of L1–L6, with the k_i-weighted decoy-match rate marked as a reference line. [Generated by analysis code.]

**Table 3.** Confirmatory results for H1–H4 and the registered analyses reported beside them.

| Analysis | Set (n) | Estimate | Interval | One-sided P | Holm-adjusted P | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| H1: Δ = π_f − π_d (A1, Vietnamese) | {{h1.n_responses|en}} | {{h1.delta|en}} | {{h1.delta_ci|en}} | {{h1.p|en}} | not adjusted | {{h1.decision_text}} |
| Excess over chance E | {{h1.n_responses|en}} | {{h1.excess|en}} | {{h1.excess_ci|en}} | — | — | {{h1.sesoi_text}} |
| Attributable share (descriptive) | {{h1.n_nonconcordant|en}} | {{h1.as|en}} | {{h1.as_ci|en}} | — | — | — |
| H1, B.1 (no pilot or seed atoms) | {{h1.b1_n|en}} | {{h1.b1_delta|en}} | {{h1.b1_delta_ci|en}} | — | — | — |
| H1, B.26 (knowable pairs) | {{h1.b26_n|en}} | {{h1.b26_delta|en}} | {{h1.b26_delta_ci|en}} | — | — | — |
| H1, S1, S2, S3, N1 | — | — | see text | — | — | {{h1.robust_text}} |
| H2: US-match difference, English minus Vietnamese | {{h2.n_pairs|en}} | {{h2.diff|en}} | {{h2.diff_ci|en}} | {{h2.p|en}} | {{h2.p_holm|en}} | {{h2.decision_text}} |
| H3: rate of L3 or L4 at A3, per model | {{h3.n_responses|en}} | {{h3.r_min|en}} to {{h3.r_max|en}} | per model in text | {{h3.p_pc|en}} | {{h3.p_holm|en}} | {{h3.decision_text}} |
| H3, B.1 and B.26 | — | {{h3.b1_range|en}}; {{h3.b26_range|en}} | — | — | — | — |
| H4: Mantel–Haenszel risk ratio | {{h4.n_answers|en}} | {{h4.rr_mh|en}} | {{h4.rr_ci|en}} | {{h4.p|en}} | {{h4.p_holm|en}} | {{h4.decision_text}} |

### RQ2: Context, Retrieval and Stubbornness

Across the context ladder (Figure 3), the share of foreign or superseded answers on conflict atoms went from {{rq2.l34_a0_pct|en}} at A0 and {{rq2.l34_a1_pct|en}} at A1 to {{rq2.l34_a2_pct|en}} at A2 and {{rq2.l34_a3_pct|en}} at A3 (pooled, Vietnamese) [A4: {{rq2.l34_a4_pct|en}}, subset, if run].

**H3.** Under A3 in Vietnamese, per-model rates of L3 or L4 answers on conflict atoms were: Qwen3-8B {{h3.r_qwen3_8b|en}} ({{h3.r_qwen3_8b_ci|en}}), Sailor2-8B-Chat {{h3.r_sailor2_8b|en}} ({{h3.r_sailor2_8b_ci|en}}), Vistral-7B-Chat {{h3.r_vistral_7b|en}} ({{h3.r_vistral_7b_ci|en}}), Llama-3.1-8B-Instruct {{h3.r_llama31_8b|en}} ({{h3.r_llama31_8b_ci|en}}). The partial-conjunction P was {{h3.p_pc|en}} (Holm-adjusted {{h3.p_holm|en}}), and H3 was {{h3.decision_text}}. {{h3.n_models_lcl_above|en}} models had a lower limit above {{=0.05}} (descriptive). Without passages that state a non-MoH value (B.22), the rates ranged from {{h3.b22_min|en}} to {{h3.b22_max|en}}; B.1 and B.26 are in Table 3. The stubbornness rate on conflict and version-drift atoms was {{rq2.stubborn_pct|en}} ({{rq2.stubborn_ci|en}}).

**Retrieval versus in-context errors (A2).** Retrieval recall at the top {{=5}} was {{rq2.recall_pct|en}}. Of non-concordant A2 answers, {{rq2.retrieval_err_share|en}} occurred when the gold chunk was not retrieved and {{rq2.incontext_err_share|en}} when it was (Table 4). DR3 was {{rq2.dr3_text}}.

**Table 4.** Decomposition of non-concordance by model at A2 and A3.

| Model | Recall of gold chunk (A2) | Retrieval errors (A2) | In-context errors (A2) | L3 or L4 with exact passage (A3) |
| --- | --- | --- | --- | --- |
| Qwen3-8B | {{rq2.recall_qwen3_8b|en}} | {{rq2.retrieval_err_qwen3_8b|en}} | {{rq2.incontext_err_qwen3_8b|en}} | {{h3.r_qwen3_8b|en}} |
| Sailor2-8B-Chat | {{rq2.recall_sailor2_8b|en}} | {{rq2.retrieval_err_sailor2_8b|en}} | {{rq2.incontext_err_sailor2_8b|en}} | {{h3.r_sailor2_8b|en}} |
| Vistral-7B-Chat | {{rq2.recall_vistral_7b|en}} | {{rq2.retrieval_err_vistral_7b|en}} | {{rq2.incontext_err_vistral_7b|en}} | {{h3.r_vistral_7b|en}} |
| Llama-3.1-8B-Instruct | {{rq2.recall_llama31_8b|en}} | {{rq2.retrieval_err_llama31_8b|en}} | {{rq2.incontext_err_llama31_8b|en}} | {{h3.r_llama31_8b|en}} |

**Figure 3.** Context ladder from A0 to A4: shares of L3, L4 and L5 on conflict atoms by condition, model and language. [Generated by analysis code.]

### Version Drift (Exploratory)

On {{drift.n_atoms|en}} version-drift atoms, {{drift.l3_a1_pct|en}} of A1 answers matched a superseded MoH version. The probability of L3 by months from guideline issue to the model's cutoff is shown in Figure 4 ({{drift.model_text}}). Among atoms with several dated versions of the same foreign system, the latest-version bias was {{drift.latest_bias|en}} ({{drift.latest_bias_ci|en}}).

**Figure 4.** Version drift: estimated probability of matching a superseded MoH value against months between the issue date of the current guideline and the model's training cutoff (negative when issued after the cutoff), by model; the cutoffs of three models are upper bounds. [Generated by analysis code.]

### RQ3: Disagreement Signal and Certified Abstention

**H4.** Of {{h4.n_answers|en}} served value-stating answers, {{h4.disagree_share|en}} fell in the disagreement group. The Mantel–Haenszel risk ratio was {{h4.rr_mh|en}} ({{h4.rr_ci|en}}; one-sided P={{h4.p|en}}; Holm-adjusted P={{h4.p_holm|en}}; crude ratio {{h4.rr_crude|en}}), and H4 was {{h4.decision_text}}.

**Certified bounds.** Figure 5 shows, for each model, the certified upper bounds on selective risk by coverage level and group. At a coverage of {{=0.5}}, bounds for the disagreement group ranged from {{rq3.u_disagree_c050_min|en}} to {{rq3.u_disagree_c050_max|en}} and for the agreement group from {{rq3.u_agree_c050_min|en}} to {{rq3.u_agree_c050_max|en}} across models. Learn-then-Test certified a coverage of {{rq3.ltt_cov_disagree_min|en}} to {{rq3.ltt_cov_disagree_max|en}} in the disagreement group; DR4 was {{rq3.dr4_text}} and DR5 was {{rq3.dr5_text}}. Self-abstention at A2 ranged from {{rq3.self_abstain_min|en}} to {{rq3.self_abstain_max|en}}. In the regime (a) re-randomizations, the familywise violation frequency was {{rq3.regime_a_violation|en}}. In regime (b), bound violations on unseen guidelines occurred in {{rq3.regime_b_bound_violation_min|en}} to {{rq3.regime_b_bound_violation_max|en}} of splits and Learn-then-Test violations in {{rq3.regime_b_ltt_violation_min|en}} to {{rq3.regime_b_ltt_violation_max|en}}; transfer was {{rq3.regime_b_text}}. Comparators are reported in Supplement S5.

**Figure 5.** Certified upper bounds on selective risk (non-MoH value among answered questions) at coverage levels {{=1.0}}, {{=0.75}}, {{=0.5}} and {{=0.25}}, by group and model, with empirical test-split risks. [Generated by analysis code.]

### RQ4: Core Clinical Problems (Exploratory)

[Only if the mapping of atoms to core clinical problems was completed.] Deviations were distributed across {{rq4.n_problems_covered|en}} core clinical problems; {{rq4.summary_text}}. Vignettes without an MoH cue (A6) agreed with A1 short-answer concordance in {{rq4.a6_a1_agree_pct|en}} of atom × model pairs (κ={{rq4.a6_a1_kappa|en}}).

### Preliminary Feasibility Study (Pilot)

The pilot is a separate, hand-picked dataset from one model, graded with grader_version {{=1.2.0}}; it is not pooled with the main study and was not reviewed by clinicians. Of {{pilot.n_atoms|en}} atoms from {{pilot.n_guidelines|en}} documents, {{pilot.n_atoms_analysed|en}} atoms from {{pilot.n_guidelines_analysed|en}} documents still in force were analyzed. The AI citation audit confirmed {{pilot.audit_confirmed|en}} atoms, corrected {{pilot.audit_corrected|en}} without a change of value and found real errors in {{pilot.audit_errors|en}}. The code-only cross-check found every span on its stated page ({{pilot.indep_span_ok|en}} of {{pilot.indep_n|en}}) and the numbers and drug names of {{pilot.indep_foreign_found|en}} of {{pilot.indep_foreign_records|en}} foreign records in the cached sources.

For short answers, the rule-based grader agreed with the AI-adjudicated labels in {{pilot.grader_short_agree_pct|en}} ({{pilot.grader_short_agree_ci|en}}; κ={{pilot.grader_short_kappa|en}}). Disagreements were concentrated in a few rule classes; in particular, the grader labeled {{pilot.rule_label6_n|en}} responses as self-abstentions, against {{pilot.adj_label6_n|en}} after adjudication. These errors defined grader_version {{=1.3.0}} for the main study.

Under A1 in Vietnamese, on {{pilot.a1_vi_conflict_n|en}} conflict atoms, Qwen3-8B gave the MoH value in {{pilot.a1_vi_conflict_correct|en}} ({{pilot.a1_vi_conflict_correct_pct|en}}; {{pilot.ci_level}} CI {{pilot.a1_vi_conflict_correct_ci|en}}), a foreign value in {{pilot.a1_vi_conflict_foreign|en}}, a value matching no recorded source in {{pilot.a1_vi_conflict_unattributed|en}} and no value in {{pilot.a1_vi_conflict_abstain|en}}; with AI-adjudicated labels, it gave the MoH value in {{pilot.adj_a1_vi_conflict_correct|en}}. On concordant control atoms, it gave the MoH value in {{pilot.a1_vi_concordant_correct|en}} of {{pilot.a1_vi_concordant_n|en}}. On the {{pilot.n_conflict_h1_atoms|en}} conflict atoms with a decoy, foreign and decoy matches were {{pilot.a1_vi_h1_foreign|en}} and {{pilot.a1_vi_decoy|en}} for short answers; on the multiple-choice questions, where the foreign and decoy options were shown side by side, they were {{pilot.mcq_a1_vi_foreign|en}} and {{pilot.mcq_a1_vi_decoy|en}} of {{pilot.mcq_a1_vi_n|en}} answers (both option orders counted, so answers are not independent). On {{pilot.a1_vi_drift_n|en}} version-drift atoms, {{pilot.a1_vi_drift_stale|en}} answers matched the superseded value. With the exact passage (A3), the MoH value was given for {{pilot.a3_vi_conflict_correct|en}} of {{pilot.a3_vi_conflict_n|en}} conflict atoms ({{pilot.a1a3_vi_conflict_improved|en}} changed from non-concordant to concordant and {{pilot.a1a3_vi_conflict_worsened|en}} the reverse; two-sided exact McNemar P={{pilot.a1a3_vi_conflict_p|en}}), and foreign or superseded values for {{pilot.a3_vi_foreign_or_stale|en}}. Of the pilot decoys, {{pilot.decoy_plausible|en}} of {{pilot.decoy_rated|en}} were rated plausible by the AI audit, and {{pilot.mcq_truncated|en}} of {{pilot.mcq_total|en}} multiple-choice outputs reached the token limit. English results are in Supplement S7.

---

## Discussion

### Principal Findings

[CHOOSE ONE OPTION AFTER THE CONFIRMATORY ANALYSIS HAS BEEN RUN BY CODE; delete the other. Neither option may be rewritten to present a negative result as positive (registration §5.3).]

[OPTION A, H1 supported.] Under an explicit instruction to follow Vietnamese MoH guidance, locally run open-weight models of 7B–9B parameters answered conflict atoms with values from named foreign guideline systems more often than with a decoy value that belongs to no source (Δ {{h1.delta|en}}; E {{h1.excess|en}}). [If the lower limit of E is at least the smallest effect of interest:] The excess is practically important by the preregistered criterion. [If E is inconclusive:] Whether the excess is practically important is not settled by these data. [If "H1 robust" holds:] The finding held under the directional correction and with arithmetic-mirror decoys. [Otherwise:] The finding depended on the decoy construction and should be read with that caveat. The attributable share shows that {{h1.as|en}} of non-concordant answers can be traced to a named foreign system or a superseded MoH version, while {{h1.unattributed_share|en}} matched no recorded value.

[OPTION B, H1 not supported.] Under an explicit instruction to follow Vietnamese MoH guidance, locally run open-weight models of 7B–9B parameters did not answer conflict atoms with foreign values measurably more often than with a decoy value. [If the upper limit of E is below the smallest effect of interest:] No practically important excess of foreign-value matches over chance was found for these models (a precise negative result). [Otherwise:] The data neither show nor exclude an excess of practical importance. [If most non-concordant answers were L5:] Most of the non-concordant answers ({{h1.unattributed_share|en}}) matched no recorded source. For these models, deviation from MoH guidance is therefore dominated by values that match neither a foreign guideline nor a superseded MoH version, rather than by foreign defaults. This describes these models only and is not extended to commercial or larger models.

[BOTH OPTIONS; complete from the results.] English prompts [did / did not] increase US-value matches (H2 {{h2.decision_text}}), [consistent / not consistent] with the language-driven jurisdictional defaults reported for administrative questions [@wang2026jurisdictional]. With the exact MoH passage in the prompt, foreign or superseded values [persisted above / fell below] the registered margin of {{=0.05}} in [at least half / fewer than half] of the models (H3 {{h3.decision_text}}). [If H3 is not confirmed and every upper limit is below the margin: "with the exact MoH passage supplied, foreign or superseded answers were below the margin in every model", which is a finding in its own right.] The label-free disagreement signal [did / did not] identify answers with at least twice the risk of a non-MoH value (H4 {{h4.decision_text}}), and the certified bounds at fixed coverage were [informative / wide] at the sample sizes available.

### Comparison With Prior Work

Bazerbachi et al found that large general-purpose models followed US neuroradiology recommendations even when asked for a non-US guideline, and that supplying the guideline restored most of the accuracy [@bazerbachi2026cultural]. Our design differs in scale ({{atoms.n_total|en}} atoms rather than a few dozen vignettes), in grading (rules that compare values rather than clinician judgment), in the decoy control, in the version axis and in the model class (locally run 7B–9B open-weight models rather than large general-purpose models). [Result-dependent: Our A1 results (agree / disagree) with theirs for this model class; our A3 results (agree / disagree) with their full-document condition, and the A4 subset allows a closer comparison.] Zhou et al attributed a substantial share of a frontier model's examination errors to divergence between US and Chinese guidelines by manual review after grading [@zhou2026localization]; our attribution is automatic, value-level and compared with a chance baseline, and [result-dependent sentence]. Country-stated vignette studies [@nguyen2025gpchatgpt; @zeng2025geographic] correspond to our A1 condition, and our results [extend / qualify] them for a Southeast Asian national standard in two languages. Siepmann et al reported low concordance with an updated WHO hepatitis B guideline unless its text was supplied [@siepmann2025hepatitisb]; our version axis replaces one guideline system with {{corpus.n_chains|en}} named MoH supersession chains, and [result-dependent sentence on version drift]. H2 replicates, at the level of clinical values, the language-driven defaults that Wang and Suresh found in administrative and legal questions [@wang2026jurisdictional], and it is consistent with [or: differs from] findings that the language of a question shifts guideline adherence and implicit geography [@zhao2025chinesemedicine; @wong2026implicit].

National-guideline benchmarks for Kenya, the United Kingdom, Germany and Brazil, and multi-country CPGBench, measure or improve adherence [@mutisya2025alama; @harris2025pubhealthbench; @schwietering2026cpgqade; @abonizio2026brazilian; @tan2026cpgbench]; our atoms add the question of which competing standard a non-concordant answer came from. Temporal benchmarks show that LLMs rely on outdated medical knowledge [@wu2025driftmedqa; @vladika2025factsfade; @guan2026temporal; @yu2026outdated]; [result-dependent: our version-drift analysis (supports / does not support) this for national guidance, with the caveat that model cutoffs are mostly upper bounds]. On context use, retrieval failure explained most retrieval-augmented errors in German neurovascular guidelines [@vach2026neurovascular]. [Result-dependent: our A2 decomposition (agrees / disagrees).] Studies of counterfactual evidence show models over-trusting the context [@mo2026faithfulness], and knowledge-conflict studies show models keeping their priors when evidence is mixed [@wu2024clasheval; @xie2023chameleon]. Our A3 condition tests the opposite failure to counterfactual over-trust: keeping a foreign or superseded parametric value despite the correct national passage.

For abstention, accuracy-only scoring rewards guessing [@kalai2026hallucinations] and medical LLMs rarely abstain [@cocchieri2026abstain], which is why self-abstention is reported as its own outcome here. Our certificates are relative to the MoH standard: a certificate is only as valid as the reference labels on which it is calibrated [@liu2026certified]. Clustered calibration data reduce the effective sample size of thresholds [@noonan2026exceedance], and certified selective-prediction bounds have exceeded their budgets under grouped splits in other domains [@zhou2026falsesense]. We therefore split by atom for the guarantee and report transfer to unseen guidelines separately (regime b). The grouped Learn-then-Test machinery itself is not new [@angelopoulos2025learnthentest; @gurram2026selective; @salem2026hgcrc]; the additions here are groups defined by signals of guideline conflict and an empirical test of whether those signals separate higher-risk answers.

### Implications for Medical Education in Vietnam

Students in Vietnam already use AI tools [@bui2026kap]. [Result-dependent framing.] Three messages follow from the design and, where stated, from the results. First, "According to the Ministry of Health" in a prompt does not guarantee an MoH value: [insert the A1 concordance on conflict atoms and on concordant control atoms]. A learner should treat any dose, threshold, duration or first-line drug from an LLM as a claim to be checked against the current MoH decision and its version, and should ask which guideline and which version a value comes from. Second, supplying the MoH text [reduced / did not remove] non-concordant values [insert A3 result]; teaching materials should show that even an answer given with the correct passage in context can be non-concordant, including unit and conversion errors. Third, the behavior worth rewarding in teaching and in tools is the context-aware answer (L1), which gives the MoH value and names where other guidelines differ; it was [rare / common] in this study ({{rq1.a1_l1_pct|en}}). [If RQ4 was done: the mapping to core clinical problems identifies the topics where deviations concentrate, which can guide teaching.] The atoms, questions and grader are released for educators to build exercises on guideline versions and jurisdiction. They measure fidelity to MoH guidance, not clinical correctness, and are not a tool for clinical decisions.

### Limitations

The study concerns one country and one reference standard. The corpus and the atoms are a purposive, conflict-enriched sample of current MoH guidance, selected by a mechanical priority order that favors topics known to conflict, so the rates describe that sample and not MoH guidance at large. We make no claim that the method transfers to other countries without testing. A1 is a controlled probe with an explicit MoH cue, not the way students usually ask; the conditions closer to practice (A0 and the vignettes) are descriptive or exploratory. Each condition used one prompt wording in each language, and the results may be sensitive to phrasing.

Only open-weight models of 7B–9B parameters were evaluated, run locally with four-bit quantized weights on one laptop GPU; no commercial, frontier or larger model was run, and none of the commercial chatbots that students may use through a web interface. These choices followed the resources of the study (one laptop and no paid API) and were made before the pilot outputs were opened. Small quantized models may deviate from MoH guidance because they do not know the value at all, and this floor effect can mask the jurisdictional pattern that H1 tests; the concordant-atom control and the attributable share are reported for this reason. Quantization itself may change answers; a registered comparison with eight-bit weights on a subset (Supplement S5) addresses this only for one model. One model does not officially support Vietnamese. Greedy GPU inference can be slightly nondeterministic, and each request was run once.

Verification beyond code relied on AI. Atom extraction, counterpart proposals, question paraphrase, translation, answer extraction, and every check that the protocol assigned to people were done by Claude agents, and the auditors belong to the same model family as the agents that extracted the atoms and drafted the grader. Their errors may be correlated, and agreement between two passes of the same model family is not evidence of independent verification. The pilot showed that this risk is not hypothetical: the AI citation audit of the pilot atoms found real errors in {{pilot.audit_errors|en}} of {{pilot.n_atoms|en}} atoms that had already passed automatic span verification. The code-only cross-check is independent of any language model but covers only spans, values and the presence of foreign numbers in cached sources, not population or clinical context. [If done:] Student co-authors checked random samples; they are not clinicians, and their checks cover samples, not every atom. [If not done: no person checked the atoms or grades systematically.]

No physician reviewed the atoms, the counterparts or the grades. Clinical variables that the protocol planned (clinician confirmation, whether an MoH value lags current evidence, and clinical harm) were not collected; code surrogates such as whether a foreign source postdates the MoH document are reported and labeled as surrogates. Some recorded conflicts may therefore be clinically immaterial, and some foreign values may apply to populations that differ in ways that the rubric did not capture; the tipping-point analysis bounds how many false conflicts the confirmatory conclusions can absorb.

Model knowledge cutoffs limit attribution. Only one model has a developer-stated cutoff; for the other three, the release or upload date is an upper bound. Several current MoH guidelines were issued after these dates, so the models could not have learned their values, and several foreign values were first published after some cutoffs, so the models could not have defaulted to them. The knowable-pair analysis addresses the second problem, but its knowable sets are upper bounds, and a value may have appeared in an earlier edition that was not recorded. Attribution is value-level coincidence beyond chance; it does not show that a model learned a value from the matched source.

The rule-based grader can err, and its errors need not be random. In the pilot, grader errors were more frequent on conflict atoms ({{pilot.grader_err_conflict_pct|en}}) than on concordant control atoms ({{pilot.grader_err_concordant_pct|en}}), and the grader over-assigned self-abstention. Grader_version {{=1.3.0}} was derived from those errors, which were found in pilot outputs; because pilot atoms remain in the main set, their main-study grades may be optimistic. The held-out validation on non-pilot atoms, the exclusion of pilot atoms from grader validation and RQ3, and B.1 next to H1 and H3 limit but do not remove this risk. L5 (unattributed) is a residual category: it includes format and unit errors and values between recorded sources, and it grows when the reference store misses a foreign or historical value. The decoy may be less attractive than the foreign value (farther, less round or on the other side of the MoH value), which would understate chance matches and bias H1 toward support; in the pilot, only {{pilot.decoy_plausible|en}} of {{pilot.decoy_rated|en}} decoys were rated plausible by the AI audit. The directional, mirror-rule, roundness and plausibility analyses and the multiple-choice replication address this, but they cannot guarantee equal attractiveness.

Sample size was bounded by the number of current MoH guidelines with official PDFs and by one laptop's throughput. The conflict atoms fall into {{atoms.n_families|en}} families of unequal size, and confirmatory intervals are clustered by family. H2 depends on the number of US-unique atoms and was expected to have low power, and H3 was expected to have limited power if the true rates lie only slightly above the registered margin. [If DR2 or DR6 applied: state the shortfall or the conditions and models cut.] The RQ3 guarantees hold only for questions drawn from the same frozen atom pool; they do not apply to guidelines issued after the freeze, and bounds are not simultaneous across models.

Finally, the registration was not deposited before the pilot outputs were opened, contrary to what the registration text committed at the time. Several design changes were informed by the pilot, and they are listed with their provenance in Supplement S8. Readers should weigh the pilot-informed changes accordingly; none of them altered a hypothesis, analysis set or decision rule.

### Conclusions

[OPTION A, H1 supported.] When asked to follow Vietnamese MoH guidance, locally run open-weight LLMs of 7B–9B parameters gave values from named foreign guidelines more often than chance, and a measurable part of their deviation from national guidance can be traced to foreign systems or superseded MoH versions. [OPTION B, H1 not supported.] When asked to follow Vietnamese MoH guidance, locally run open-weight LLMs of 7B–9B parameters did not give foreign-guideline values measurably more often than chance; their deviations from national guidance mostly matched no recorded source. [BOTH.] Supplying the exact MoH passage [changed the picture as follows], and a label-free disagreement signal [did / did not] support a useful certified abstention layer. Value-level attribution with a decoy control is a reusable way to audit LLMs against a national standard, and the atoms, questions, grader and outputs are released for that purpose. Anyone using an LLM for Vietnamese clinical reference should check its values against the current MoH document.

---

## Acknowledgments

[TODO: acknowledgments, if any. AI assistance is disclosed in the AI Use Disclosure section and not listed here.]

## Data Availability

The code (extraction, matching, question generation, runners, grader, analysis and figures), the frozen atoms (values, citations and page locations only), the questions, the run records with raw model outputs, the grades, the registry of every reported number, and the SHA256 checksums of all frozen and sealed files are available at [repository URL and archived DOI: TODO]. MoH documents are not redistributed; each atom cites the official source URL, document number, page and span, and the SHA256 hash of the downloaded file allows verification. For copyrighted foreign guidelines, only values, citations and locations are released, never passage text. The pilot outputs are released as a separate dataset. The OSF registration, its addenda and the decision log are available at [OSF DOI: TODO].

## AI Use Disclosure

In line with ICMJE recommendations, we disclose that Claude (Anthropic), used through the Claude Code agent environment [model identifiers and dates of use: TODO from logs], was used for the following: writing and testing the study code; extracting candidate recommendation atoms from MoH documents; proposing foreign counterpart values and decoys for schedule, drug and category atoms; paraphrasing and translating questions; extracting answer strings from model outputs that had no answer line (without access to reference values); the AI audits that replaced checks assigned to people in the protocol (two passes and an adjudicator per check); literature searching; internal review of drafts by AI agents, which are not people and are not reported as peer or clinician review; and drafting this manuscript. Every AI-produced value that enters an analysis was checked by code (verbatim span matching, unit and number checks, the code-only cross-check and citation lookup in bibliographic registries) and by the AI audit, as described in the Methods. No LLM assigned the labels analyzed in this paper. All numbers in this paper are produced by analysis code and inserted from a registry. The authors reviewed and edited the manuscript and take full responsibility for its content. No AI system is listed as an author.

## Authors' Contributions

*[PROPOSED, from state/gates/coauthor_roles.md; to be agreed by all three authors before submission and updated to the work actually done (CRediT).]*

Binh Minh Ngo: conceptualization, methodology, software, data curation, formal analysis, project administration and writing (original draft). Binh Thong Ngo: validation (checking of atom citations and vignettes), investigation and writing (review and editing). Tran Doan Mai Huong: validation (checking of grading labels), investigation and writing (review and editing). All authors approved the final manuscript and agree to be accountable for it. [TODO: confirm.]

## Conflicts of Interest

None declared. [TODO: each author confirms.]

## Funding

This study received no specific funding. [TODO: authors confirm; state any institutional support.]

## Abbreviations

A0–A6: context conditions (see Methods); API: application programming interface; BCa: bias-corrected and accelerated; CI: confidence interval; DR: decision rule; GGUF: file format for quantized model weights used by llama.cpp; LLM: large language model; MoH: Ministry of Health (Vietnam); OCR: optical character recognition; OSF: Open Science Framework; RAG: retrieval-augmented generation; TRIPOD-LLM: the TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis) reporting guideline for studies using large language models; WHO: World Health Organization.

## Multimedia Appendices

- Supplement S1: document catalogue, corpus selection and supersession chains.
- Supplement S2: atom schema, extraction rules, context-check rubric, decoy rules and quality control.
- Supplement S3: verbatim prompts and conditions in Vietnamese and English; decoding and runtime settings.
- Supplement S4: grading rules of the frozen grader, test cases, held-out validation and extractor check.
- Supplement S5: full statistical specification, simulated operating characteristics, sensitivity and exploratory analyses, and comparators.
- Supplement S6: completed TRIPOD-LLM checklist.
- Supplement S7: pilot study, full results in both languages.
- Supplement S8: preregistration timeline, the first addendum (changes C1–C12 with provenance), and later deviations.

## References

[Generated at build from manuscript/references.yaml (AMA numbered style for JMIR). Every entry must be "ok" or "ok_manual" in manuscript/citations_verified.json before submission. In-text markers of the form TODO-CITE must be resolved first; see manuscript/TODO_manuscript.md.]

<!-- NEW REGISTRY KEYS: the list is kept in manuscript/TODO_manuscript.md (section "New registry keys") and repeated here for the statistician.
```text
atoms (15):
  atoms.h1_share_pilot atoms.n_concordant atoms.n_conflict atoms.n_conflict_decoy atoms.n_conflict_no_decoy
  atoms.n_dr8 atoms.n_drift atoms.n_families atoms.n_families_multi_guideline atoms.n_gv atoms.n_indistinguishable
  atoms.n_no_counterpart atoms.n_pilot atoms.n_total atoms.n_us_unique
coauthor (7):
  coauthor.atoms_agree_ci coauthor.atoms_agree_pct coauthor.atoms_n coauthor.labels_agree_pct coauthor.labels_kappa
  coauthor.labels_n coauthor.vignettes_n
compute (1):
  compute.sec_per_request
corpus (7):
  corpus.n_catalogued corpus.n_catalogued_current corpus.n_chains corpus.n_current corpus.n_ocr
  corpus.n_partial_amendments corpus.n_superseded
design (13):
  design.alpha_one_sided design.bootstrap_b design.ci_pct design.dr6_hours design.gv_acc_min
  design.gv_atoms_per_stratum design.gv_lcl_min design.gv_responses_approx design.label1_check_n
  design.mcq_max_tokens design.num_ctx design.run_valid_min_pct design.small_cluster_min
drift (5):
  drift.l3_a1_pct drift.latest_bias drift.latest_bias_ci drift.model_text drift.n_atoms
grader (14):
  grader.dr9_text grader.extractor_err_ci grader.extractor_err_pct grader.gv_accuracy grader.gv_accuracy_ci
  grader.gv_decision_text grader.gv_n_atoms grader.gv_n_responses grader.label1_precision_max
  grader.label1_precision_min grader.label6_precision grader.label6_recall grader.needs_llm_max_pct
  grader.version_frozen
h1 (41):
  h1.as h1.as_c h1.as_c_ci h1.as_ci h1.b10_delta_ci h1.b11_delta_ci h1.b1_delta h1.b1_delta_ci h1.b1_n h1.b26_delta
  h1.b26_delta_ci h1.b26_n h1.decision_text h1.decoy_share_l5 h1.delta h1.delta_ci h1.delta_model_max
  h1.delta_model_min h1.excess h1.excess_ci h1.false_conflicts_plausible h1.l4_not_knowable h1.n1_delta_ci h1.n_atoms
  h1.n_families h1.n_nonconcordant h1.n_responses h1.p h1.pi_d h1.pi_d_ci h1.pi_d_unweighted h1.pi_f h1.pi_f_ci
  h1.robust_text h1.s1_delta_ci h1.s2_delta_ci h1.s3_delta_ci h1.sesoi_text h1.systems_text h1.tipping_point
  h1.unattributed_share
h2 (11):
  h2.decision_text h2.diff h2.diff_ci h2.n_atoms h2.n_discordant_families h2.n_pairs h2.p h2.p_holm h2.rate_en
  h2.rate_vi h2.test_text
h3 (19):
  h3.b1_range h3.b22_max h3.b22_min h3.b26_range h3.decision_text h3.n_models_lcl_above h3.n_responses h3.p_holm
  h3.p_pc h3.r_llama31_8b h3.r_llama31_8b_ci h3.r_max h3.r_min h3.r_qwen3_8b h3.r_qwen3_8b_ci h3.r_sailor2_8b
  h3.r_sailor2_8b_ci h3.r_vistral_7b h3.r_vistral_7b_ci
h4 (8):
  h4.decision_text h4.disagree_share h4.n_answers h4.p h4.p_holm h4.rr_ci h4.rr_crude h4.rr_mh
pilot (11):
  pilot.adj_label6_n pilot.audit_confirmed pilot.audit_corrected pilot.audit_errors pilot.decoy_plausible
  pilot.decoy_rated pilot.grader_err_concordant_pct pilot.grader_err_conflict_pct pilot.mcq_total pilot.mcq_truncated
  pilot.rule_label6_n
qc (16):
  qc.audit_agree_pct qc.audit_kappa qc.code_ai_agree_pct qc.code_span_ok_pct qc.code_values_ok_pct
  qc.decoy_plausible_pct qc.decoy_regenerated qc.dr1_text qc.extraction_precision qc.extraction_precision_ci
  qc.false_conflict_ucl qc.false_conflicts qc.matching_precision qc.matching_precision_ci qc.matching_sensitivity
  qc.matching_sensitivity_ci
questions (5):
  questions.n_mcq questions.n_removed questions.n_removed_ambiguity questions.n_short questions.n_translation_edited
rq1 (13):
  rq1.a0_ask_country_pct rq1.a0_us_en_pct rq1.a0_us_vi_pct rq1.a1_l1_pct rq1.a1_vi_concordant_pct
  rq1.a1_vi_control_correct_pct rq1.a1_vi_l3_pct rq1.a1_vi_l4_pct rq1.a1_vi_l5_pct rq1.a1_vi_l6_pct rq1.mcq_delta
  rq1.mcq_delta_ci rq1.mcq_order_agree_pct
rq2 (23):
  rq2.dr3_text rq2.incontext_err_llama31_8b rq2.incontext_err_qwen3_8b rq2.incontext_err_sailor2_8b
  rq2.incontext_err_share rq2.incontext_err_vistral_7b rq2.l34_a0_pct rq2.l34_a1_pct rq2.l34_a2_pct rq2.l34_a3_pct
  rq2.l34_a4_pct rq2.recall_llama31_8b rq2.recall_pct rq2.recall_qwen3_8b rq2.recall_sailor2_8b rq2.recall_vistral_7b
  rq2.retrieval_err_llama31_8b rq2.retrieval_err_qwen3_8b rq2.retrieval_err_sailor2_8b rq2.retrieval_err_share
  rq2.retrieval_err_vistral_7b rq2.stubborn_ci rq2.stubborn_pct
rq3 (16):
  rq3.dr4_text rq3.dr5_text rq3.ltt_cov_disagree_max rq3.ltt_cov_disagree_min rq3.regime_a_violation
  rq3.regime_b_bound_violation_max rq3.regime_b_bound_violation_min rq3.regime_b_ltt_violation_max
  rq3.regime_b_ltt_violation_min rq3.regime_b_text rq3.self_abstain_max rq3.self_abstain_min rq3.u_agree_c050_max
  rq3.u_agree_c050_min rq3.u_disagree_c050_max rq3.u_disagree_c050_min
rq4 (4):
  rq4.a6_a1_agree_pct rq4.a6_a1_kappa rq4.n_problems_covered rq4.summary_text
runs (11):
  runs.answer_line_max_pct runs.answer_line_min_pct runs.dr10_dr11_text runs.dr6_text runs.laptop_hours runs.n_models
  runs.n_requests runs.ollama_version runs.truncated_max_pct runs.truncated_min_pct runs.valid_min_pct
TOTAL new keys: 240 (display in Vietnamese format; main.md uses the |en suffix on numeric keys; *_text keys are English strings)
```
-->
