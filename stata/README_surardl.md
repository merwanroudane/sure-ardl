# surardl — Seemingly unrelated ARDL cointegration for Stata

`surardl` implements the **SUR-ARDL** framework of Arif & Furuoka (2026):
the Pesaran–Shin–Smith (2001) conditional error-correction model written for
each of *N* cross-sectional units and estimated jointly as a Zellner (1962)
SUR system by feasible GLS.

Because the ARDL lag structure absorbs short-run dynamics and regressor
endogeneity parametrically, the estimator needs only the *N* × *N*
contemporaneous covariance **Σ**, not the 2*N* × 2*N* long-run covariance
required by FM-SUR (Wagner, Grabarczyk & Hong 2020) or the banded inverse
autocovariance of Lin & Reuvers (2025).

```stata
ssc install surardl
help surardl
```

## Quick start

```stata
webuse set none
use surardl_asean6, clear          // shipped with the package: net get surardl

generate double lrec = ln(rec)
generate double lgdp = ln(gdp)
generate double lfdi = ln(fdi + 4)
generate double lto  = ln(to)
xtset country year

surardl lrec lgdp lfdi lto, bootstrap(999)
estat longrun, fieller
estat ecequal, mtest(holm)
estat graph
```

Each panel is one equation. Variables enter in **levels**; `surardl` builds
the error-correction form itself.

## What it does

| | |
|---|---|
| **Estimation** | two-step FGLS (default), iterated FGLS (→ ML), or OLS benchmark; four Σ̂ divisors |
| **Deterministics** | all five PSS cases, with the restriction count *q* derived from the case, never hard-coded |
| **Lag structure** | common or unit-specific orders, fixed or chosen by AIC/SBC on a common sample |
| **Bounds test** | Wald and two RSS forms; the *t* test on λ; the *F* test on the lagged regressor levels (second degenerate case) |
| **Critical values** | PSS (2001) Tables CI and CII; Narayan (2005); SUR-specific Monte Carlo bounds; SUR residual bootstrap |
| **Long run** | θ = −β/λ with delta-method, Fieller and bootstrap intervals |
| **Cross-equation** | poolability, equality of adjustment speeds, equality of long-run coefficients, with Holm/Bonferroni/Šidák corrections |
| **Diagnostics** | Breusch–Pagan LM, Pesaran CD, Breusch–Godfrey, Σ̂ conditioning |
| **Output** | journal-style tables and five figures, built with official `twoway` only |

`e(b)` and `e(V)` are posted in the standard way, so `test`, `lincom`,
`nlcom` and `testnl` all work across equations with the full SUR covariance.

## Choosing critical values — read this

The PSS and Narayan bounds are calibrated for the **single-equation OLS**
*F* statistic. The SUR statistic has a more dispersed null distribution in
small samples because Σ is estimated jointly from the same *T* observations,
so the tabulated bounds are **liberal** here. The paper's own equation (193)
gives the rule:

> use tabulated values if *N* ≤ 3 or mean correlation ≤ 0.3;
> use bootstrap values if *N* ≥ 5 and mean correlation ≥ 0.5.

`surardl` prints the tabulated bounds for reference and warns whenever no
resampling has been requested. When the decision matters, run
`bootstrap(999)`.

## Validation

The build was checked against external benchmarks, not against itself:

- **`sureg`** — coefficients and covariance agree to ~1e-10 on an identical
  design; `method(iterated)` matches `sureg, isure` to six decimals.
- **`regress` + `test`** — under `method(ols)` the Wald bounds statistic
  equals the single-equation *F* to six decimals.
- **`nlcom`** — delta-method long-run standard errors agree exactly.
- **PSS (2001) Table CI** — with Σ = **I** and *T* = 500 the `simulate()`
  engine reproduces the published asymptotic bounds to simulation error
  (case 5, *K* = 3: simulated I(0) 3.481/4.010 against published 3.47/4.01).
- **The paper's own tables** — on the shipped ASEAN-6 data the command
  reproduces Table 9, the Breusch–Pagan statistic (28.84 vs 28.91), the
  Pesaran CD statistic (1.30 vs 1.32), and both columns of Table 10.
- **The DGP** — `surardl_example.do` regenerates the paper's Monte Carlo
  design and checks parameter recovery, consistency, the relative-efficiency
  pattern of Tables 1–2, bootstrap size under H0 (0.040 at nominal 5%) and
  power under H1 (0.890).

Run it yourself:

```stata
net get surardl
do surardl_example.do     // self-test on a known-truth DGP
do surardl_asean6.do      // the published empirical application
```

## Departures from the draft

Each is documented in `help surardl methods`, with the reasoning:

1. The printed Pesaran CD formula (eq. 100) omits a factor of 2;
   `surardl` uses Pesaran's own formula, which reproduces the CD = 1.32
   quoted in the paper from the paper's own Table 9.
2. Equation (69) restricts only equation *i*; the authors' scripts restrict
   all equations. Both are available (`fstat(rss)`, `fstat(rssall)`).
3. The authors' posted scripts use case 4; the published Table 10 is
   reproduced by case 3.
4. The Monte Carlo baseline in §4.1 states λ = −0.3, β = −0.09 and θ = 0.3,
   which are mutually inconsistent; the self-test uses β = +0.09.
5. §§3.3 and 4 cite equation numbers absent from the draft, so the
   cross-equation restriction matrices are reconstructed from the
   hypotheses as stated in words in §4.5.
6. "RFN" is referred to but never defined; `surardl` reports its own
   definition and labels it as such.

## Files

```
surardl.ado                     estimation command + Mata library
surardl_estat.ado               postestimation + graphs + the same library
surardl_p.ado                   predict
surardl.sthlp                   overview
surardl_postestimation.sthlp    estat suite
surardl_methods.sthlp           methods, step→equation map, validation
surardl_example.do              self-test on the paper's Monte Carlo DGP
surardl_asean6.do               the published empirical application
surardl_asean6.dta              ASEAN-6 panel, 1990–2024
```

The Mata library is carried inside both `.ado` files. Stata compiles an
auto-loaded ado's Mata block into a namespace private to that file, so a
shared library would otherwise need a `.mlib`, which would impose a needless
Stata-version floor on an SSC package. Sources live in `_sa_*.mata`;
`build.py` assembles them. Edit the sources, not the built `.ado`.

## References

Arif, M. A., and F. Furuoka. 2026. Seemingly unrelated cointegrating
regressions with autoregressive distributed lag dynamics. Research Square.
[doi:10.21203/rs.3.rs-9237078/v1](https://doi.org/10.21203/rs.3.rs-9237078/v1)

Pesaran, M. H., Y. Shin, and R. J. Smith. 2001. Bounds testing approaches to
the analysis of level relationships. *Journal of Applied Econometrics* 16:
289–326. [doi:10.1002/jae.616](https://doi.org/10.1002/jae.616)

McNown, R., C. Y. Sam, and S. K. Goh. 2018. Bootstrapping the autoregressive
distributed lag test for cointegration. *Applied Economics* 50: 1509–1521.
[doi:10.1080/00036846.2017.1366643](https://doi.org/10.1080/00036846.2017.1366643)

Full reference list in `help surardl`.

## Author

**Dr Merwan Roudane**
merwanroudane920@gmail.com
[github.com/merwanroudane](https://github.com/merwanroudane)
