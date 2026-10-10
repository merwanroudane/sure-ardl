# surardl — validation record

**Version 1.0.1** (10 October 2026). Changes since 1.0.0: corrected the
Palm–Smeekes–Urbain DOI in `surardl.sthlp` (the previous one resolved to
Choi & Saikkonen 2010); `estat graph, bootdist equation(#)` now accepts the
option; the figures are drawn directly rather than `nodraw` + `graph
display`, so they work in batch and with `graph export`; `stata.toc` added.
No change to any estimate, statistic, critical value or stored result.

Every number below was produced by running the command, not asserted.
Reproduce with `do surardl_example.do` and `do surardl_asean6.do`.

---

## 1. Source audit

Target paper: Arif & Furuoka (2026), *Seemingly Unrelated Cointegrating
Regressions with Autoregressive Distributed Lag Dynamics*, Research Square,
doi:10.21203/rs.3.rs-9237078/v1 (58 pp).

**Status of the companion GitHub repositories.** `nonlinear-lab/SUR-ARDL-analysis`
and `nonlinear-lab/SUR-ARDL-empirical-distribution` are associated with the
second author but are **not** the replication package for this version of the
paper:

- the paper's own availability statement says code is obtainable from the
  corresponding author on request, i.e. not from a public repository;
- the shipped data file carries nine variables per country
  (`rec cpu epu eru tpu gpr gdp fdi to`) and the author's path string names an
  *uncertainty* project, while the paper uses four;
- the posted scripts specify **case 4** (a trend in the unrestricted model,
  dropped from the restricted one, q = 5), whereas the published Table 10 is
  reproduced only by **case 3** (q = 4);
- the posted scripts use the variables in **levels**; Table 10 is reproduced
  only in **logs**.

They were therefore treated as a secondary implementation reference, not as
authority. Two things of real value came out of them:

1. the restriction count: `tnv1 − tnv2 = 9 − 4 = 5` in the OxGauss code
   settles that their F is a case-4 statistic, resolving what would otherwise
   look like an arbitrary constant;
2. the null DGP design in `SUR-ARDL-empirical-distribution`: AR(1) regressors
   with coefficients 0.92–1.00 driven by **shared** shocks across units, which
   is what preserves cross-equation dependence. This informed `simrho()`.

**Load-bearing sources, all obtained.** PSS (2001), Pesaran & Shin (1999),
Zellner (1962), Breusch & Pagan (1980), Pesaran (2004), Narayan (2005),
Kripfganz & Schneider (2020, 2023), Wagner et al. (2020), Lin & Reuvers
(2025), Mark et al. (2005), Moon & Perron (2005).

**The one gap that mattered.** The paper calls for a bootstrap ("Approach B")
but never specifies it. `wp16-08.pdf` in the source folder turned out to be
McNown, Sam & Goh's working paper on bootstrapping the ARDL bounds test —
the published design (Applied Economics 2018), itself Palm, Smeekes & Urbain
(2010). That is what `bootstrap()` implements, extended to the SUR system.

---

## 2. Agreement with the estimation benchmark

`surardl` vs `sureg` on an identical design (ASEAN-6, case 3, ARDL(1,1,1,1)):

```
max |b_surardl  - b_sureg|   =  9.628e-11
max |V_surardl  - V_sureg|   =  2.304e-10
max relative difference in b =  5.544e-10
```

`method(iterated)` vs `sureg, isure`: λ(Thailand) = −0.663008 vs −0.663007.

`method(ols)` vs `regress` + `test` on equation 3:

```
regress  F = 5.729288    se(L.y) = 0.147231    b(L.y) = -0.559079
surardl  F = 5.729288    (Wald form)           b       = -0.559079
```

Delta-method long-run standard error vs `nlcom` on the same ratio:
0.0633465 from both.

---

## 3. Agreement with the published critical value tables

The `simulate()` engine, run with Σ = **I** so that SUR collapses to OLS by
Proposition 1, must reproduce the single-equation tabulations. 4000
replications, k = 3:

**T = 500 (asymptotic), case 3**

| | 10% | 5% | 1% |
|---|---|---|---|
| simulated I(0) | 2.756 | 3.298 | 4.460 |
| PSS Table CI   | 2.72  | 3.23  | 4.29  |
| simulated I(1) | 3.877 | 4.447 | 5.705 |
| PSS Table CI   | 3.77  | 4.35  | 5.61  |

**T = 500, case 5**

| | 10% | 5% |
|---|---|---|
| simulated I(0) | 3.481 | 4.010 |
| PSS Table CI   | 3.47  | 4.01  |
| simulated I(1) | 4.547 | 5.211 |
| PSS Table CI   | 4.45  | 5.07  |

This exercises the ECM design, the restriction set, the FGLS solve and the
Wald form together, from first principles.

**At T = 34 the simulated values are far above the tabulated ones** (I(0) 5%:
5.07 simulated vs 3.63 Narayan). That is not an error: the SUR Wald statistic
embeds a jointly estimated Σ̂ and divides by T rather than T − m, so its null
distribution is genuinely more dispersed in small samples. This is the
quantitative content of the paper's Simulation 2, and the reason `bootstrap()`
exists.

---

## 4. Reproduction of the paper's empirical application

The draft does not state its transformations. They were identified by matching
the published tables:

**ln(REC), ln(GDP), ln(FDI + 4), ln(TO); case 3; ARDL(1,1,1,1); T = 34.**

Table 9 (residual correlation matrix) is matched to RMSD 0.0002 over the 15
off-diagonal entries. Table 10:

| | Indonesia | Malaysia | Philippines | Singapore | Thailand | Vietnam |
|---|---|---|---|---|---|---|
| λ OLS, paper   | −0.098 | −0.212 | −0.559 | −0.384 | −0.528 | −0.505 |
| λ OLS, surardl | −0.0987 | −0.2122 | −0.5591 | −0.3845 | −0.5269 | −0.5045 |
| F OLS, paper   | 0.51 | 1.71 | 5.73 | 4.37 | 7.28 | 3.89 |
| F OLS, surardl | 0.52 | 1.71 | 5.73 | 4.38 | 7.26 | 3.89 |
| λ SUR, paper   | −0.092 | −0.205 | −0.541 | −0.441 | −0.619 | −0.497 |
| λ SUR, surardl | −0.0931 | −0.2055 | −0.5399 | −0.4423 | −0.6163 | −0.4968 |
| se(λ) paper    | 0.085 | 0.086 | 0.107 | 0.138 | 0.129 | 0.109 |
| se(λ) surardl  | 0.0847 | 0.0856 | 0.1072 | 0.1380 | 0.1295 | 0.1085 |
| F SUR, paper   | 0.56 | 2.38 | 8.63 | 7.24 | 11.45 | 6.14 |
| F SUR, surardl | 0.58 | 2.38 | 8.63 | 7.28 | 11.37 | 6.13 |
| θ_GDP, paper   | 2.323 | 2.524 | 0.719 | 1.060 | 1.967 | 1.282 |
| θ_GDP, surardl | 2.336 | 2.520 | 0.719 | 1.060 | 1.968 | 1.282 |

Diagnostics: Breusch–Pagan LM 28.84 (paper 28.91); Pesaran CD 1.299 (paper
1.32); mean |correlation| 0.1898 (paper 0.190).

Residual differences are consistent with the FDI shift constant being
approximately, not exactly, 4.

The F column confirms the **Wald form**, F = W/q, is the statistic behind the
published table — not the RSS form, which gives 5.04 for the Philippines where
the paper reports 8.63.

---

## 5. Known-truth Monte Carlo

Paper's §4.1 DGP, with β = +0.09 so that θ = −β/λ = 0.3 as stated
(see note 4 in `help surardl methods`).

**Parameter recovery**, N = 3, T = 500, ρ = 0.6, 50 replications:
λ̂ = −0.3169 (truth −0.300); θ̂ = 0.3012 (truth 0.300).

**Relative efficiency** RMSE(OLS)/RMSE(SUR) for λ, N = 5, T = 100:

| ρ | 0.0 | 0.3 | 0.6 | 0.8 |
|---|---|---|---|---|
| surardl | 0.966 | 1.151 | 1.177 | 1.415 |
| paper, Table 1 Panel C | 0.980 | — | 1.308 | 1.728 |

RE ≈ 1 at ρ = 0 (Proposition 1) and rising in ρ (Proposition 2), matching the
published pattern.

**Bounds test size**, H0 true, N = 3, T = 60, ρ = 0.6, nominal 5%, 100
replications with the seed varied every replication:

```
PSS 5% tabulated bound   rejection rate = 0.020
SUR residual bootstrap   rejection rate = 0.040
```

The bootstrap is mildly conservative, which is safe. The tabulated rate of
0.020 matches the conservatism the paper reports for N = 3 in its Table 3.

**Power**, H1 true (λ = −0.3), same configuration: bootstrap rejection rate
**0.890** against a size of 0.040.

---

## 6. Coverage

42 option and postestimation paths were exercised on a clean
`net install`: all five deterministic cases, three estimation methods, four
Σ̂ divisors, three F forms, fixed and selected lag orders, `small`, `level()`,
`eqnames()`, both bootstrap null targets, both marginal DGPs, `nodrift`,
`simrho()`, every `estat` subcommand with its options, all four `predict`
statistics, all six figures, and cross-equation `test`/`lincom`/`nlcom`.
All pass. Six invalid calls are correctly rejected.

---

## 7. A result worth understanding, not suppressing

On the ASEAN-6 data Singapore's bootstrap critical values come out an order of
magnitude above the other countries' (5% CV ≈ 47 against 6–9), so the bootstrap
does **not** reject where the tabulated bounds would.

This was investigated rather than patched. It is not a drift artefact —
Vietnam has a higher drift-to-noise ratio and behaves normally — and it is not
caused by the marginal VECM, since it survives `bootdgp(rw)`. The cause is that
Singapore's differenced dependent variable is dominated by the contemporaneous
differenced regressors, with impact coefficients 1.51 on `D.lgdp` and −1.11 on
`D.lto`. The pseudo-dependent variable is then close to a linear combination of
the pseudo-regressors plus a random walk, the lagged level terms in the bounds
regression are nearly collinear, and the null distribution acquires a very
heavy right tail.

The tabulated PSS bounds assume the regressors are independent of the
dependent variable. Singapore violates that badly, so the tabulated bounds do
not apply to it and the bootstrap is right to disagree with them. This is
documented in `help surardl methods` as a diagnostic to interpret, not a
failure to work around.

---

**Dr Merwan Roudane** · merwanroudane920@gmail.com · github.com/merwanroudane
