# Nowcasting PEFT — Project Brief

A private, bilingual (English / Arabic) study brief for the master's thesis proposal:
**cross-dataset parameter-efficient fine-tuning for precipitation nowcasting.**

Open `index.html` in any browser. It is a single self-contained file — no server, no
build step, no internet connection required. Use the **EN / ع** buttons in the top bar
to switch language; the choice is remembered per browser.

## What is in it

| Section | |
|---|---|
| 01 | The five sentences to memorise |
| 02 | The problem — domain shift, with measured skill decay |
| 03 | The four radar datasets, and three traps in them |
| 04 | AlphaPre — the frozen base model |
| 05 | What PEFT means, drawn to scale |
| 06 | **The kernel's four axes — the core technical argument** |
| 07 | The two research contents |
| 08 | Where the innovation is (novelty defence) |
| 09 | **The three experiments already run, with real numbers** |
| 10 | What the results do *not* prove |
| 11 | What still has to be run |
| 12 | **How to present, and how to handle questions** |
| 13 | The five papers this stands on |
| 14 | Glossary |
| 15 | Status and next steps |

Sections 06, 09 and 12 are the ones to know cold.

## Provenance of the numbers

Every figure and statistic is taken from measured results in
`nowcasting-proposal/prelim/experiments_summary.md` — the parameter census, the
cross-dataset baseline with its SEVIR control, and the seven-arm adaptation
comparison. **Nothing on the page is quoted from a paper or estimated.** Where a
result is not yet established (the sign flip, the unexplained cross-budget ordering)
the page says so explicitly, in section 10.

## A note on "private"

This repository is private, so the source is visible only to you.

**GitHub Pages cannot serve this privately.** Access-controlled Pages sites are a
GitHub Enterprise Cloud feature; on a Free or Pro account, publishing Pages from a
private repository still produces a *publicly reachable* URL. So this repo
deliberately has **no Pages workflow**. To read the brief, clone or download the repo
and open `index.html` locally.

## Files

- `index.html` — the brief (self-contained)
- `patch_ar_headings.py` — one-time patch that split the section headings into
  English/Arabic pairs; kept as a record of the change
