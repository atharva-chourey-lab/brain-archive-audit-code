# Blind Benchmark — PREDICTION.md §3, as registered

**Run:** 2026-11-17 · **Script:** `scripts/benchmark.py` · **Data:** `outputs/benchmark_testset.csv`
**Status:** pre-registered test, executed exactly as registered in `PREDICTION.md` §3 (commit `d54361f`, before any test-set value was extracted). No refitting. No public release.

## Verdict

**The registered line FAILS the registered success criterion.**

On the full blind test set (343 species), the registered line's median absolute
percentage error is **66.0%**, against **18.2%** for the one gradeable comparator
(Patzke et al. 2015). The criterion required our median APE to beat *every*
gradeable comparator on the same species set. It beats none. The line does not
predict unseen published anatomy better than the existing literature model —
on this test it is not close, and the failure is structural, not a matter of a
few outliers (only 2.0% of test species fall within ±25% of the line's
prediction; 18.7% within ±50%).

What the failure consists of is itself a finding, and it is reported in full
below: the published record is histology, the registered line is MRI
segmentation, and the two method classes disagree in level by roughly a factor
of 1.5–2 — the same offset §4 localized for the felids, now visible across the
whole literature. The line may still describe MRI-segmentation anatomy (its own
class); the claim that it *predicts the published record* is dead.

## The registered line and criterion

```
log10(hippocampus_cm3) = -1.6609 + 0.8467 x log10(brain_cm3)
```
(QC-passed labels-only fit, n = 8 Brain Catalogue species, fit range
brain ≈ 6–443 cm³.)

Criterion (§3, verbatim in substance): the line "predicts unseen anatomy
better" only if its median absolute % error is lower than **every** gradeable
comparator's on the same species set. Metrics: median APE (primary), mean
signed % error, head-to-head win/loss vs each gradeable comparator.

## Test set

Eligibility (§3): a species with a published hippocampus volume that is
(a) **not** among the Brain Catalogue's 37 specimens and (b) **not** lion or
leopard (those belong to §4). **343 species** qualified.

### Primary subset — Reep, Finlay & Darlington 2007 (n = 26)

*Reep, Finlay & Darlington (2007), "The Limbic System in Mammalian Brain
Evolution," Brain Behav Evol 70:57–70*, Table 1 — full text openly posted
(Cornell CDN PDF), opened and transcribed in full. Table 1 lists 29 species;
lion and leopard are excluded by §4 and the zebra is a Brain Catalogue
specimen, leaving **26**.

- **Brain-volume operationalization (declared):** total brain volume = the sum
  of the row's 11 printed regional components (mm³ → cm³). This is the paper's
  own accounting — the excluded lion row sums to 231.09 cm³, matching the
  ~231 cm³ figure stated when the test was designed. One declared wrinkle:
  the paper's footnote states the amygdala is *also* included in the
  paleocortex column, so the component sum double-counts the amygdala by
  ~0.2–0.7% of brain volume. The sum as printed is used unchanged.
- **Hippocampus** = the table's hippocampus column (includes dentate gyrus,
  cornu ammonis, alveus, hippocampal commissure and fornix-fimbria caudal to
  the septum; measured on one side and doubled; shrinkage-corrected —
  species-specific factors for six taxa, a mean factor of 2.4 for the rest).
- Two printed values required the only sensible parse, declared here:
  olingo isocortex "90,30.72" read as 9030.72 mm³; manatee diencephalon
  "1,2847.68" read as 12847.68 mm³.

### Compilation subset — Patzke et al. 2015 (n = 317)

*Patzke et al. (2015), "In contrast to many other mammals, cetaceans have
relatively small hippocampi that appear to lack adult neurogenesis," Brain
Struct Funct 220:361–383*, Table 1 — the Stephan-series / Manger compilation.
Full text opened (publisher PDF; author manuscript PMC8734557); the table was
transcribed from the PMC version and cross-checked against the PDF. Each row
carries its underlying source: Pirlot & Nelson 1978, Stephan et al. 1981,
Reep et al. 2007, Montie et al. 2008, Patzke et al. 2015 (new measurements), or
Baron et al. 1996. The compilation contains no rodents or lagomorphs; it is
bats-, insectivore- and primate-heavy (247 of the 343 test species have brains
under 2 cm³).

- **Brain volume** = the table's Vb (ml), which the paper constructs as brain
  mass / 1.036.
- Species also present in Reep Table 1 (source code 3) are graded **once**, on
  the Reep primary values; their compilation rows are not double-counted.
- Species with multiple specimen rows are **averaged** (Vb and Vh): elephant
  (3 specimens), hippopotamus (2), Atlantic white-sided dolphin (3), harbour
  porpoise (2), minke whale (2), and ten bat species (2 each, near-identical).
- Genus-level entries (*Tarsius* sp., *Alouatta* sp., *Ardops* sp.,
  *Scotomanes* sp., *Syconycteris* sp.) are graded as printed and flagged in
  the CSV. *Cebus* sp. was **excluded** conservatively: the catalogue's
  white-headed capuchin is a *Cebus*, so catalogue overlap cannot be ruled out.
- Catalogue-species exclusions applied at species level: platypus, slow loris,
  Demidoff's galago, night monkey, rhesus macaque, grey-cheeked mangabey,
  baboon (*Papio* — the catalogue specimen is *Papio* sp., excluded
  conservatively), chimpanzee, gorilla, human, gibbon, bottlenose dolphin,
  black rhinoceros, plains zebra, plus lion and leopard (§4).

### Validation of the transcription

- **Internal checksum:** the compilation states Vb = Mb/1.036 for every row.
  All ~390 transcribed rows were checked against that identity. Exactly three
  rows fail beyond rounding: *Micropotamogale lamottei* (Vb printed 0.077,
  identity gives ≈0.77), *Hipposideros sperois* (0.027 vs ≈0.27) and
  *Notopteris macdonaldi* (1.14 vs ≈1.41) — internal inconsistencies in the
  published table (dropped digits). **These three species are excluded and
  reported here, not silently corrected.** (The three *Lagenorhynchus* rows
  show a ~0.5% internal inconsistency, within the table's rounding behaviour
  at that size; retained as printed.)
- **Cross-source check:** all 29 Reep hippocampus values agree between the
  Reep PDF and the compilation's source-3 rows to rounding (max discrepancy
  0.005 cm³). The two transcriptions corroborate each other.

## Comparators

### Patzke et al. 2015 — GRADEABLE, graded

The paper's best model (fit to log-transformed data across its compilation,
excluding cetaceans, elephants, hippopotami and the manatee from the fit) is
the exponential curve, parameters as published (a = 9.26, b = 0.72, c = 0.097;
r² = 0.97):

```
ln(Vh) = 9.26 x (0.72 - exp(-0.097 x ln(Vb)))
```

The paper prints the curve as "y = a × (b − exp(−c × x))" fitted to
log-transformed data without naming the log base. The natural-log reading is
**verified numerically**: it reproduces the paper's own table values across
four orders of magnitude (e.g. predicted vs published hippocampus: tree shrew
0.195 vs 0.15 ml; manatee 4.07 vs 3.63; elephant 13.6 vs 11.21), while a log₁₀
reading predicts ~800 ml hippocampi and is impossible. This is the only
reading under which the published parameters describe the published data.

**In-sample warning (material):** Patzke's model was fitted on essentially
this test set — its own compilation, including the Reep rows. On 337 of 343
test species the comparator is being graded on its own training data, an
enormous structural advantage. The verdict below reports the fully-blind
subset separately; the failure does not depend on the in-sample rows.

### Karbowski 2007 — NOT GRADEABLE (a finding)

Karbowski (2007), "Global and regional brain metabolic scaling and its
functional consequences," *BMC Biology* 5:18, is widely cited for a
hippocampal scaling exponent of −0.14. Opening the paper shows that number is
the scaling exponent of **volume-specific glucose metabolic rate**
(CMRglc per unit volume, Fig. 3B: y = −0.14x − 0.13, n = 7), not of volume.
The paper publishes **no hippocampal volume equation at all** — no slope, no
intercept, no normalization for volume. It therefore cannot be graded as a
volume predictor, and no volume equation was reconstructed from it. The
registered criterion is accordingly evaluated against the single gradeable
comparator. (Reep et al.'s own Fig. 1 reports a hippocampus-vs-brain-core
exponent of 0.912, but against a different predictor variable — brain core,
not whole brain — with arbitrary plot constants; it is not a whole-brain
point predictor and was not graded either.)

## Scorecard

Median APE = median absolute % error (primary). Signed = mean signed % error.
W–L = head-to-head, registered line vs Patzke 2015 (no ties occurred).

| Set | n | Line median APE | Line signed | Patzke median APE | Patzke signed | W–L |
|---|---|---|---|---|---|---|
| **Full test set** | 343 | **66.0%** | −53.5% | **18.2%** | +17.5% | 56–287 |
| Reep 2007 primary | 26 | 55.5% | −45.8% | 29.2% | +0.8% | 5–21 |
| Patzke compilation only | 317 | 66.3% | −54.1% | 18.0% | +18.8% | 51–266 |
| Both-blind subset* | 6 | 301.6% | +379.8% | 184.0% | +286.9% | 1–5 |
| Sensitivity: Reep with compilation Vb† | 26 | 51.0% | −38.3% | 31.2% | +11.8% | 8–18 |

\* Species in groups Patzke excluded from their own fit (cetaceans, elephant,
hippopotamus, manatee): Atlantic white-sided dolphin, harbour porpoise, minke
whale, African elephant, hippopotamus, Florida manatee. Both models fail
catastrophically here — these are the known small-hippocampus exceptions —
but Patzke's median is still lower and it wins 5 of 6 head-to-heads.
† Sensitivity: Reep species re-graded using the compilation's mass-derived Vb
instead of the component-sum brain volume. The two brain-volume
operationalizations differ by up to ~15% per species; the verdict is unchanged.

Within-tolerance rates, full set: line within ±25% on **2.0%** of species,
within ±50% on 18.7%; Patzke within ±25% on 61.2%, within ±50% on 82.5%.

## Reading the failure (post-hoc diagnostics — labelled, not registered)

The registered scorecard above is the result. The breakdowns below were
computed after the fact to explain it; they change no verdict.

**1. A method-class level offset (dominant inside the fit range).** The line
underpredicts nearly everywhere in the histology literature: mean signed
error −45.8% on the Reep subset, −36.9% even restricting Reep to brains
≥ 20 cm³ (median APE 46.5%). Published histological hippocampi are simply
larger, at the same brain size, than MRI-segmentation hippocampi — by a
factor of roughly 1.6 here, and ~2.2 in the felid case §4 examined in depth.
§4's boundary-sensitivity test already localized that offset to the histology
side (shrinkage-correction multipliers, sparse-section estimation,
single-hemisphere doubling). The benchmark generalizes §4: **an
MRI-segmentation allometry and the histological record are two different
rulers.** Any future version of the line must either be fit to, or explicitly
bridged to, the method class it claims to predict.

**2. Functional form at small sizes.** 247 of 343 test species have brains
under 2 cm³ — two orders of magnitude below the registered fit range. There,
true hippocampal share rises steeply (least weasel 8.1% of brain, nine-banded
armadillo 11.0%, common shrew ~10.5%): the relationship bends, a single power
law cannot follow it, and Patzke's saturating exponential — built for exactly
this range — can. Size-band medians for the line: 65.7% (<2 cm³), 69.0%
(2–20 cm³), 51.3% (>20 cm³). The failure is not only extrapolation, though:
inside the line's own fit range (5–450 cm³, n = 65) its median APE is still
62.6%, because component 1 operates there too.

**3. The known exceptions stay exceptional.** Cetaceans are the largest
errors for both models (line: minke whale +1152%, harbour porpoise +575%,
Atlantic white-sided dolphin +435%; Patzke: +652%, +706%, +343%). The
elephant: line +168%, Patzke +25% (Patzke excluded elephants from their fit;
the elephant is out-of-sample for both, and only one model survives it).
Pinnipeds run the other way — the only Reep group the line *over*predicts
(California sea lion +44.9%, northern fur seal +27.1%, stellar sea lion
+22.2%) — consistent with genuinely small pinniped hippocampi meeting a
histology ruler that, for once, reads low relative to the line.

**Best and worst for the line.** Closest predictions: harbour seal +7.0%,
squirrel monkey −10.7%, spider monkey −18.5%. Worst: the three cetaceans and
the elephant above, then nine-banded armadillo −85.7% and the elephant shrews
(*Elephantulus* −84.2%, *Rhynchocyon* −83.1%).

## Caveats, stated plainly

- **The comparator's in-sample advantage is real and large** (see above). It
  does not rescue the line: the line loses on the Reep subset by 26 points of
  median APE, loses the both-blind subset, and loses every size band. But an
  honest statement of what this benchmark shows is: *a line fit to 8 MRI
  segmentations does not predict the histological literature* — not that the
  line is a worse description of MRI anatomy than Patzke's curve. Grading
  Patzke's curve against MRI-segmentation values would be the symmetric test,
  and it has not been run.
- **Printed precision bounds the small end.** Compilation hippocampus values
  are printed to 0.01 ml; for species with Vh = 0.01–0.03 ml, rounding alone
  permits ±17–50% apparent error. This inflates both models' APEs on the
  smallest species; the Reep subset (mm³ precision) shows the same ordering,
  so the verdict does not rest on rounding.
- **n = 1 throughout.** Nearly every literature value is a single specimen;
  the sources publish no measurement uncertainty, so none could be carried.
- **No refitting was done or is licensed by this report.** Any revised line
  (e.g. fit across method classes with a declared bridge, or a curved form)
  is a new hypothesis requiring its own registration and a fresh blind set.

## Reep primary subset — full roster

Brain = component sum (cm³); Obs = published hippocampus (cm³); errors signed %.

| Species | Brain | Obs | Line err | Patzke err |
|---|---|---|---|---|
| Coyote (*Canis latrans*) | 73.02 | 2.159 | −61.7% | −18.9% |
| Red fox (*Vulpes vulpes*) | 37.80 | 1.288 | −63.3% | −9.2% |
| Fennec (*Fennecus zerda*) | 14.75 | 0.486 | −56.1% | +29.3% |
| Polar bear (*Ursus maritimus*) | 391.32 | 5.589 | −38.8% | −21.6% |
| Crab-eating raccoon (*Procyon cancrivorus*) | 36.86 | 1.026 | −54.9% | +12.3% |
| Coatimundi (*Nasua nasua*) | 24.19 | 0.494 | −34.5% | +77.4% |
| Olingo (*Bassaricyon gabbii*) | 15.75 | 0.579 | −61.1% | +13.4% |
| Least weasel (*Mustela nivalis*) | 2.07 | 0.168 | −76.0% | −16.4% |
| Badger (*Taxidea taxus*) | 42.72 | 1.448 | −63.8% | −12.7% |
| Striped skunk (*Mephitis mephitis*) | 7.81 | 0.312 | −60.1% | +27.9% |
| Spotted hyena (*Crocuta crocuta*) | 140.61 | 3.081 | −53.3% | −17.2% |
| Mountain lion (*Felis concolor*) | 104.80 | 1.799 | −37.6% | +20.1% |
| Northern fur seal (*Callorhinus ursinus*) | 268.04 | 1.953 | +27.1% | +84.8% |
| California sea lion (*Zalophus californianus*) | 384.97 | 2.328 | +44.9% | +86.7% |
| Stellar sea lion (*Eumetopias jubatus*) | 514.56 | 3.530 | +22.2% | +42.2% |
| Harbor seal (*Phoca vitulina*) | 239.90 | 2.114 | +7.0% | +61.1% |
| Collared peccary (*Tayassu tajacu*) | 50.44 | 2.668 | −77.4% | −47.5% |
| Llama (*Lama glama*) | 162.49 | 3.524 | −53.9% | −21.6% |
| Camel (*Camelus dromedarius*) | 553.21 | 8.577 | −46.5% | −39.4% |
| White-tailed deer (*Odocoileus virginianus*) | 115.64 | 3.260 | −62.6% | −29.9% |
| Zebu (*Bos taurus indicus*) | 498.10 | 7.708 | −45.5% | −35.9% |
| Giant anteater (*Myrmecophaga tridactyla*) | 45.65 | 2.685 | −79.3% | −51.0% |
| Collared anteater (*Tamandua tetradactyla*) | 19.45 | 1.070 | −74.8% | −29.1% |
| Two-toed sloth (*Choloepus didactylis*) | 19.62 | 1.138 | −76.2% | −33.0% |
| Nine-banded armadillo (*Dasypus novemcinctus*) | 8.43 | 0.928 | −85.7% | −54.5% |
| Florida manatee (*Trichechus manatus*) | 283.02 | 3.634 | −28.4% | +2.2% |

Excluded from Reep Table 1 by the protocol: African lion and leopard (§4);
zebra (Brain Catalogue specimen).

## Files

- `outputs/benchmark_testset.csv` — all 343 graded species: brain volume,
  published hippocampus, both models' predictions and signed/absolute % errors,
  per-row source. This CSV is the complete roster of record; Appendix A below
  reproduces the compilation subset from it.
- `scripts/benchmark.py` — the full computation, with both source tables
  transcribed in-line and every operationalization declared in the docstring.
- `PREDICTION.md` §3 — the registered protocol this run executed.

## Appendix A — Patzke compilation subset roster (n = 317)

Brain = Vb as published (ml); Obs = published hippocampus (ml). Source =
underlying source per Patzke et al. 2015 Table 1. Rows marked † average
multiple specimen rows.

| Species | Brain | Obs | Source |
|---|---|---|---|
| Aethechinus algirus | 3.09 | 0.23 | Stephan et al. 1981 |
| Alouatta sp. | 50.19 | 1.32 | Stephan et al. 1981 |
| Anoura caudifer | 0.39 | 0.03 | Baron et al. 1996 |
| Anoura geoffroyi | 0.57 | 0.05 | Baron et al. 1996 |
| Ardops sp. | 0.55 | 0.04 | Baron et al. 1996 |
| Artibeus concolor | 0.61 | 0.04 | Baron et al. 1996 |
| Artibeus jamaicensis | 0.98 | 0.06 | Baron et al. 1996 |
| Artibeus lituratus | 1.19 | 0.08 | Baron et al. 1996 |
| Asellicus stoliczkanus | 0.15 | 0.01 | Baron et al. 1996 |
| Asellicus tricuspidatus | 0.13 | 0.01 | Baron et al. 1996 |
| Ateles geoffroyi | 104.25 | 1.37 | Stephan et al. 1981 |
| Avahi laniger | 10.13 | 0.53 | Stephan et al. 1981 |
| Avahi occidentalis | 9.33 | 0.48 | Stephan et al. 1981 |
| Balaenoptera acutorostrata | 2750.97 | 1.43 | Patzke et al. 2015 (current study † |
| Balionycteris maculata | 0.49 | 0.06 | Baron et al. 1996 |
| Brachyphylla cavernarum | 1.15 | 0.08 | Baron et al. 1996 |
| Callicebus moloch | 18.34 | 0.59 | Stephan et al. 1981 |
| Callimico goeldii | 10.61 | 0.28 | Stephan et al. 1981 |
| Callithrix jacchus | 7.34 | 0.22 | Stephan et al. 1981 |
| Cardioderma cor | 0.65 | 0.03 | Baron et al. 1996 |
| Carollia castanea | 0.44 | 0.04 | Baron et al. 1996 |
| Carollia perspicullata | 0.53 | 0.04 | Baron et al. 1996 |
| Casinycteris argynnis | 0.81 | 0.07 | Baron et al. 1996 |
| Cebuella pygmaea | 4.34 | 0.13 | Stephan et al. 1981 |
| Cercopithecus ascanius | 64.67 | 1.19 | Stephan et al. 1981 |
| Cercopithecus mitis | 72.39 | 1.37 | Stephan et al. 1981 |
| Cercopithecus talapoin | 38.61 | 0.71 | Stephan et al. 1981 |
| Chalinolobus gouldi | 0.23 | 0.02 | Baron et al. 1996 |
| Chalinolobus morio | 0.18 | 0.02 | Baron et al. 1996 |
| Cheirogaleus major | 6.56 | 0.35 | Stephan et al. 1981 |
| Cheirogaleus medius | 3.03 | 0.17 | Stephan et al. 1981 |
| Cheiromeles torquatus | 1.32 | 0.06 | Baron et al. 1996 |
| Chiroderma salvini | 0.79 | 0.06 | Baron et al. 1996 |
| Chiroderma trinitatum | 0.52 | 0.03 | Baron et al. 1996 |
| Chiroderma villosum | 0.74 | 0.05 | Baron et al. 1996 † |
| Chironax melanocephalus | 0.59 | 0.06 | Baron et al. 1996 |
| Chlorotalpa stuhlmanni | 0.71 | 0.06 | Stephan et al. 1981 |
| Choeroniscus minor | 0.38 | 0.04 | Baron et al. 1996 |
| Chrysochloris asiatica | 0.68 | 0.07 | Stephan et al. 1981 |
| Coleura afra | 0.25 | 0.01 | Baron et al. 1996 |
| Colobus badius | 75.29 | 1.67 | Stephan et al. 1981 |
| Cormura brevirostris | 0.21 | 0.01 | Baron et al. 1996 |
| Craseonycteris thonglongyai | 0.08 | 0.01 | Baron et al. 1996 |
| Crocidura occidentalis | 0.43 | 0.04 | Stephan et al. 1981 |
| Crocidura russula | 0.18 | 0.02 | Stephan et al. 1981 |
| Cynopterus brachyotis | 0.95 | 0.08 | Baron et al. 1996 |
| Cynopterus horsfieldi | 1.33 | 0.11 | Baron et al. 1996 |
| Cyttarops alecto | 0.17 | 0.01 | Baron et al. 1996 |
| Daubentonia madagascarie. | 43.58 | 1.78 | Stephan et al. 1981 |
| Desmana moschata | 3.86 | 0.27 | Stephan et al. 1981 |
| Desmodus rotundus | 0.96 | 0.04 | Baron et al. 1996 |
| Didelphis marsupialis | 6.65 | 0.53 | Pirlot & Nelson 1978 |
| Diphylla ecaudata | 0.77 | 0.04 | Baron et al. 1996 |
| Dobsonia inermis | 2.61 | 0.19 | Baron et al. 1996 |
| Dobsonia moluccensis | 4.43 | 0.28 | Baron et al. 1996 † |
| Dobsonia praedatrix | 2.92 | 0.18 | Baron et al. 1996 |
| Echinops telfairi | 0.60 | 0.05 | Stephan et al. 1981 |
| Echtophylla macconnelli | 0.33 | 0.03 | Baron et al. 1996 |
| Eidolon helvum | 4.14 | 0.26 | Baron et al. 1996 |
| Elephantulus fuscipes | 1.28 | 0.17 | Stephan et al. 1981 |
| Emballonura monticola | 0.16 | 0.01 | Baron et al. 1996 |
| Emballonura raffrayana | 0.17 | 0.01 | Baron et al. 1996 |
| Emballonura semicaudata | 0.18 | 0.01 | Baron et al. 1996 |
| Enchisthenes harti | 0.49 | 0.04 | Baron et al. 1996 |
| Eonycteris spelaean | 1.26 | 0.10 | Baron et al. 1996 |
| Epomophorus labiatus | 1.53 | 0.11 | Baron et al. 1996 |
| Epomops franqueti | 2.13 | 0.16 | Baron et al. 1996 |
| Eptesicus brasiliensis | 0.19 | 0.01 | Baron et al. 1996 † |
| Eptesicus flavenscens | 0.18 | 0.01 | Baron et al. 1996 |
| Eptesicus fuscus | 0.23 | 0.02 | Baron et al. 1996 |
| Eptesicus pumilis | 0.12 | 0.01 | Baron et al. 1996 |
| Erinaceus europaeus | 3.23 | 0.24 | Stephan et al. 1981 |
| Erythrocebus patas | 104.25 | 1.59 | Stephan et al. 1981 |
| Eumops auripendulus | 0.59 | 0.03 | Baron et al. 1996 |
| Eumops glaucinus | 0.63 | 0.03 | Baron et al. 1996 |
| Furipterus horrens | 0.12 | 0.01 | Baron et al. 1996 |
| Galago crassicaudatus | 9.94 | 0.46 | Stephan et al. 1981 |
| Galago senegalensis | 4.63 | 0.26 | Stephan et al. 1981 |
| Galemys pyrenaicus | 1.28 | 0.11 | Stephan et al. 1981 |
| Glauconycteris poensis | 0.20 | 0.01 | Baron et al. 1996 |
| Glischropus tylopus | 0.10 | 0.01 | Baron et al. 1996 |
| Glossophaga longirostris | 0.42 | 0.04 | Baron et al. 1996 |
| Glossphaga soricina | 0.38 | 0.03 | Baron et al. 1996 |
| Harpiocephalus hapria | 0.43 | 0.04 | Baron et al. 1996 |
| Hemicentetes semispinosus | 0.80 | 0.06 | Stephan et al. 1981 |
| Hemiechinus auritus | 1.83 | 0.13 | Stephan et al. 1981 |
| Hesperopterus blandfordi | 0.15 | 0.01 | Baron et al. 1996 |
| Hippopotamus amphibius | 476.31 | 5.22 | Patzke et al. 2015 (current study † |
| Hipposideros armiger | 0.77 | 0.05 | Baron et al. 1996 |
| Hipposideros calcaratus | 0.35 | 0.03 | Baron et al. 1996 † |
| Hipposideros cervinus | 0.21 | 0.01 | Baron et al. 1996 |
| Hipposideros commersoni | 0.72 | 0.05 | Baron et al. 1996 |
| Hipposideros diadema | 0.69 | 0.05 | Baron et al. 1996 |
| Hipposideros fulvus | 0.23 | 0.02 | Baron et al. 1996 |
| Hipposideros halophyllus | 0.15 | 0.01 | Baron et al. 1996 |
| Hipposideros lankadiva | 0.71 | 0.05 | Baron et al. 1996 |
| Hipposideros larvatus | 0.40 | 0.03 | Baron et al. 1996 |
| Hipposideros lekaguli | 0.53 | 0.04 | Baron et al. 1996 |
| Hipposideros maggietaylor. | 0.53 | 0.04 | Baron et al. 1996 † |
| Hipposideros ridleyi | 0.26 | 0.02 | Baron et al. 1996 |
| Hipposideros turpis | 0.58 | 0.04 | Baron et al. 1996 |
| Hypsignathus monstrosus | 3.36 | 0.22 | Baron et al. 1996 |
| Ia io | 0.74 | 0.05 | Baron et al. 1996 |
| Indri indri | 36.97 | 1.52 | Stephan et al. 1981 |
| Kerivoula papillosa | 0.30 | 0.04 | Baron et al. 1996 |
| Kerivoula pellucida | 0.20 | 0.01 | Baron et al. 1996 |
| Kerivoula phalaena | 0.11 | 0.01 | Baron et al. 1996 |
| Lagenorhynchus acutus | 1267.57 | 1.73 | Montie et al. 2008 † |
| Lagothrix lagotricha | 97.49 | 1.59 | Stephan et al. 1981 |
| Lasiurus borealis | 0.16 | 0.01 | Baron et al. 1996 |
| Lavia frons | 0.62 | 0.03 | Baron et al. 1996 |
| Lemur fulvus | 22.49 | 0.75 | Stephan et al. 1981 |
| Lemur variegatus | 30.41 | 1.40 | Stephan et al. 1981 |
| Lepilemur ruficaudatus | 7.34 | 0.39 | Stephan et al. 1981 |
| Leptonycteris curasoae | 0.59 | 0.05 | Baron et al. 1996 |
| Leptonycteris nivalis | 0.57 | 0.04 | Baron et al. 1996 |
| Limnogale mergulus | 1.11 | 0.08 | Stephan et al. 1981 |
| Lionycteris spurrelli | 0.34 | 0.03 | Baron et al. 1996 |
| Lonchophylla mordax | 0.42 | 0.04 | Baron et al. 1996 |
| Lonchophylla thomasi | 0.33 | 0.03 | Baron et al. 1996 |
| Loris tardigradus | 6.37 | 0.19 | Stephan et al. 1981 |
| Loxodonta africana | 4900.26 | 10.84 | Patzke et al. 2015 (current study † |
| Macroderma gigas | 1.65 | 0.07 | Baron et al. 1996 |
| Macroglossus minimus | 0.54 | 0.05 | Baron et al. 1996 |
| Macroglossus sobrinus | 0.67 | 0.06 | Baron et al. 1996 |
| Macrophyllum macrophyll. | 0.31 | 0.02 | Baron et al. 1996 |
| Megaderma lyra | 0.88 | 0.04 | Baron et al. 1996 |
| Megaderma spasma | 0.62 | 0.03 | Baron et al. 1996 |
| Megaerops ecaudatus | 0.77 | 0.07 | Baron et al. 1996 |
| Megaloglossus woermanni | 0.66 | 0.06 | Baron et al. 1996 |
| Melonyceris melanops | 1.25 | 0.08 | Baron et al. 1996 |
| Microcebus murinus | 1.72 | 0.10 | Stephan et al. 1981 |
| Microgale cowani | 0.41 | 0.04 | Stephan et al. 1981 |
| Micronycteris brachyotis | 0.39 | 0.02 | Baron et al. 1996 |
| Micronycteris megalotis | 0.26 | 0.01 | Baron et al. 1996 |
| Micronycteris minuta | 0.28 | 0.02 | Baron et al. 1996 |
| Micronycteris schmidtorum | 0.30 | 0.01 | Baron et al. 1996 |
| Micropteropus pusillus | 0.80 | 0.06 | Baron et al. 1996 |
| Mimon crenulatum | 0.31 | 0.02 | Baron et al. 1996 |
| Miniopterus australis | 0.20 | 0.02 | Baron et al. 1996 |
| Miniopterus haradai | 0.22 | 0.02 | Baron et al. 1996 |
| Miniopterus inflatus | 0.31 | 0.02 | Baron et al. 1996 |
| Miniopterus magnater | 0.31 | 0.02 | Baron et al. 1996 |
| Miniopterus medius | 0.26 | 0.02 | Baron et al. 1996 |
| Miniopterus pusillus | 0.21 | 0.02 | Baron et al. 1996 |
| Miniopterus tristis | 0.32 | 0.02 | Baron et al. 1996 |
| Molossops abrasus | 0.40 | 0.02 | Baron et al. 1996 |
| Molossops greenhalli | 0.29 | 0.01 | Baron et al. 1996 |
| Molossops planirostris | 0.18 | 0.01 | Baron et al. 1996 |
| Molossus ater | 0.51 | 0.02 | Baron et al. 1996 |
| Molossus trinitatus | 0.42 | 0.02 | Baron et al. 1996 |
| Molussus molossus | 0.31 | 0.02 | Baron et al. 1996 |
| Monophyllus plethodon | 0.43 | 0.03 | Baron et al. 1996 |
| Mormoops megalophylla | 0.37 | 0.03 | Baron et al. 1996 |
| Murina cyclotis | 0.26 | 0.02 | Baron et al. 1996 † |
| Murina huttoni | 0.25 | 0.02 | Baron et al. 1996 |
| Murina turbinaris | 0.21 | 0.02 | Baron et al. 1996 |
| Myonycteris torquata | 1.12 | 0.09 | Baron et al. 1996 |
| Myotis adversus | 0.25 | 0.01 | Baron et al. 1996 |
| Myotis albescens | 0.12 | 0.01 | Baron et al. 1996 |
| Myotis altarium | 0.23 | 0.02 | Baron et al. 1996 |
| Myotis annectans | 0.21 | 0.02 | Baron et al. 1996 |
| Myotis bechsteini | 0.26 | 0.03 | Baron et al. 1996 |
| Myotis bocagei | 0.18 | 0.01 | Baron et al. 1996 |
| Myotis dasycneme | 0.30 | 0.03 | Baron et al. 1996 |
| Myotis montivagus | 0.16 | 0.01 | Baron et al. 1996 |
| Myotis myotis | 0.47 | 0.04 | Baron et al. 1996 |
| Myotis nattereri | 0.21 | 0.02 | Baron et al. 1996 |
| Myotis nigricans | 0.14 | 0.01 | Baron et al. 1996 † |
| Myotis siligorensis | 0.10 | 0.01 | Baron et al. 1996 |
| Nasalis larvatus | 93.63 | 1.97 | Stephan et al. 1981 |
| Natalus tumidirostris | 0.24 | 0.03 | Baron et al. 1996 |
| Neomys fodiens | 0.31 | 0.03 | Stephan et al. 1981 |
| Nesogale dobsoni | 0.54 | 0.07 | Stephan et al. 1981 |
| Nesogale talazaci | 0.76 | 0.10 | Stephan et al. 1981 |
| Nesonycteris woodfordi | 0.98 | 0.07 | Baron et al. 1996 |
| Noctilio albiventris | 0.58 | 0.02 | Baron et al. 1996 |
| Noctilio leporinus | 1.14 | 0.05 | Baron et al. 1996 |
| Nyctalus noctula | 0.35 | 0.02 | Baron et al. 1996 |
| Nyctalus stenopterus | 0.24 | 0.01 | Baron et al. 1996 |
| Nycteris arge | 0.34 | 0.02 | Baron et al. 1996 |
| Nycteris grandis | 0.68 | 0.04 | Baron et al. 1996 |
| Nycteris hispida | 0.27 | 0.02 | Baron et al. 1996 |
| Nycteris javanica | 0.45 | 0.03 | Baron et al. 1996 |
| Nycteris nana | 0.23 | 0.02 | Baron et al. 1996 |
| Nycteris thebaica | 0.31 | 0.02 | Baron et al. 1996 |
| Nycteris tragata | 0.44 | 0.02 | Baron et al. 1996 |
| Nyctimene albiventer | 0.80 | 0.07 | Baron et al. 1996 |
| Nyctimene robinsoni | 1.19 | 0.10 | Baron et al. 1996 |
| Nyctimene vizcaccia | 0.95 | 0.07 | Baron et al. 1996 |
| Nyctophilus geoffroyi | 0.16 | 0.01 | Baron et al. 1996 |
| Nyctophilus timoriensis | 0.25 | 0.02 | Baron et al. 1996 |
| Oryzorictes talpoides | 0.56 | 0.06 | Stephan et al. 1981 |
| Otomops martiensseni | 0.73 | 0.03 | Baron et al. 1996 |
| Paranyctimene raptor | 0.71 | 0.06 | Baron et al. 1996 |
| Perodicticus potto | 13.51 | 0.61 | Stephan et al. 1981 |
| Peropteryx macrotis | 0.16 | 0.01 | Baron et al. 1996 |
| Peropteryx trinitatis | 0.13 | 0.01 | Baron et al. 1996 |
| Phocoena phocoena | 477.31 | 0.60 | Patzke et al. 2015 (current study † |
| Phoniscus atrox | 0.18 | 0.03 | Baron et al. 1996 |
| Phylloderma stenops | 1.29 | 0.09 | Baron et al. 1996 |
| Phyllostomus discolor | 1.05 | 0.08 | Baron et al. 1996 |
| Phyllostomus elongates | 0.85 | 0.05 | Baron et al. 1996 |
| Phyllostomus hastatus | 1.46 | 0.08 | Baron et al. 1996 |
| Pipistrellus babu | 0.09 | 0.01 | Baron et al. 1996 |
| Pipistrellus ceylonicus | 0.18 | 0.01 | Baron et al. 1996 |
| Pipistrellus circumdatus | 0.22 | 0.02 | Baron et al. 1996 |
| Pipistrellus crassulus | 0.13 | 0.01 | Baron et al. 1996 |
| Pipistrellus imbricatus | 0.13 | 0.01 | Baron et al. 1996 |
| Pipistrellus javanicus | 0.12 | 0.01 | Baron et al. 1996 |
| Pipistrellus mimus | 0.09 | 0.01 | Baron et al. 1996 |
| Pipistrellus nanus | 0.10 | 0.01 | Baron et al. 1996 |
| Pipistrellus papuanus | 0.11 | 0.01 | Baron et al. 1996 |
| Pipistrellus pulveratus | 0.14 | 0.01 | Baron et al. 1996 |
| Pipistrellus subflavus | 0.12 | 0.01 | Baron et al. 1996 |
| Pithecia monachal | 33.78 | 0.83 | Stephan et al. 1981 |
| Potamogale velox | 4.02 | 0.30 | Stephan et al. 1981 |
| Propithecus verreauxi | 25.77 | 1.04 | Stephan et al. 1981 |
| Pteronotus gymnonotus | 0.33 | 0.02 | Baron et al. 1996 |
| Pteronotus parnelli | 0.52 | 0.04 | Baron et al. 1996 |
| Pteronotus personatus | 0.22 | 0.01 | Baron et al. 1996 |
| Pteropus alecto | 6.79 | 0.36 | Baron et al. 1996 |
| Pteropus conspicillatus | 8.06 | 0.39 | Baron et al. 1996 |
| Pteropus hypomelanus | 5.12 | 0.28 | Baron et al. 1996 |
| Pteropus lylei | 5.92 | 0.29 | Baron et al. 1996 |
| Pteropus mahaganus | 5.10 | 0.28 | Baron et al. 1996 |
| Pteropus neohibernicus | 8.80 | 0.40 | Baron et al. 1996 |
| Pteropus poliocephalus | 7.00 | 0.36 | Baron et al. 1996 |
| Pteropus samoensis | 5.59 | 0.32 | Baron et al. 1996 |
| Pteropus scapulatus | 5.17 | 0.27 | Baron et al. 1996 |
| Pteropus temmincki | 4.72 | 0.28 | Baron et al. 1996 |
| Pteropus tonganus | 5.87 | 0.31 | Baron et al. 1996 |
| Pteropus vampyrus | 8.80 | 0.44 | Baron et al. 1996 |
| Pygathrix nemaeus | 74.32 | 2.30 | Stephan et al. 1981 |
| Rhinolophus cornutus | 0.19 | 0.02 | Baron et al. 1996 |
| Rhinolophus eloquens | 0.39 | 0.03 | Baron et al. 1996 |
| Rhinolophus hipposerdos | 0.14 | 0.01 | Baron et al. 1996 |
| Rhinolophus landeri | 0.27 | 0.02 | Baron et al. 1996 |
| Rhinolophus lepidus | 0.18 | 0.01 | Baron et al. 1996 |
| Rhinolophus luctus | 0.60 | 0.03 | Baron et al. 1996 |
| Rhinolophus macrotis | 0.20 | 0.02 | Baron et al. 1996 |
| Rhinolophus malayanus | 0.19 | 0.01 | Baron et al. 1996 |
| Rhinolophus megaphyllus | 0.23 | 0.02 | Baron et al. 1996 † |
| Rhinolophus paradoxolo. | 0.26 | 0.02 | Baron et al. 1996 |
| Rhinolophus pearsoni | 0.32 | 0.03 | Baron et al. 1996 |
| Rhinolophus pusillus | 0.16 | 0.01 | Baron et al. 1996 |
| Rhinolophus trifoliatus | 0.34 | 0.02 | Baron et al. 1996 |
| Rhinolophus yunanensis | 0.42 | 0.03 | Baron et al. 1996 |
| Rhinonycteris aurantius | 0.24 | 0.02 | Baron et al. 1996 |
| Rhinophylla pumilio | 0.34 | 0.03 | Baron et al. 1996 |
| Rhinopoma hardwickei | 0.27 | 0.02 | Baron et al. 1996 |
| Rhinopoma microphyllum | 0.37 | 0.03 | Baron et al. 1996 |
| Rhogessa parvula | 0.11 | 0.01 | Baron et al. 1996 |
| Rhynchocyon stuhlmanni | 5.89 | 0.58 | Stephan et al. 1981 |
| Rhynchonycteris naso | 0.11 | 0.01 | Baron et al. 1996 |
| Rousettus aegyptiacus | 2.20 | 0.15 | Baron et al. 1996 |
| Rousettus amplexicaudatus | 1.49 | 0.12 | Baron et al. 1996 † |
| Saccopteryx bilineata | 0.22 | 0.01 | Baron et al. 1996 |
| Saccopteryx canescens | 0.13 | 0.01 | Baron et al. 1996 |
| Saccopteryx leptura | 0.16 | 0.01 | Baron et al. 1996 |
| Saguinus oedipus | 9.65 | 0.26 | Stephan et al. 1981 |
| Saguinus tamarin | 9.94 | 0.28 | Stephan et al. 1981 |
| Saimiri sciureus | 23.17 | 0.35 | Stephan et al. 1981 |
| Scotomanes ornatus | 0.37 | 0.03 | Baron et al. 1996 |
| Scotomanes sp. | 0.33 | 0.03 | Baron et al. 1996 |
| Scotonycteris zenkeri | 0.69 | 0.07 | Baron et al. 1996 |
| Scotophilus dinganii | 0.42 | 0.02 | Baron et al. 1996 |
| Scotophilus heathi | 0.46 | 0.03 | Baron et al. 1996 |
| Scotophilus kuhli | 0.33 | 0.02 | Baron et al. 1996 |
| Scotorepens sanborni | 0.15 | 0.01 | Baron et al. 1996 |
| Scotozous dormeri | 0.14 | 0.01 | Baron et al. 1996 |
| Setifer setosus | 1.46 | 0.10 | Stephan et al. 1981 |
| Solenodon paradoxus | 4.51 | 0.30 | Stephan et al. 1981 |
| Sorex araneus | 0.19 | 0.02 | Stephan et al. 1981 |
| Sorex minutus | 0.10 | 0.01 | Stephan et al. 1981 |
| Sphaeris blanfordi | 0.80 | 0.07 | Baron et al. 1996 |
| Sphaeronycteris toxophyll. | 0.51 | 0.03 | Baron et al. 1996 |
| Strunira ludovici | 0.65 | 0.05 | Baron et al. 1996 |
| Sturnira lilium | 0.60 | 0.05 | Baron et al. 1996 |
| Sturnira tildae | 0.68 | 0.05 | Baron et al. 1996 |
| Suncus murinus | 0.37 | 0.03 | Stephan et al. 1981 |
| Syconycteris sp. | 0.58 | 0.06 | Baron et al. 1996 † |
| Tachyglossus aculeatus | 26.56 | 1.77 | Pirlot & Nelson 1978 |
| Tadarida aegyptiaca | 0.38 | 0.02 | Baron et al. 1996 |
| Tadarida beccarii | 0.23 | 0.01 | Baron et al. 1996 |
| Tadarida condylura | 0.44 | 0.02 | Baron et al. 1996 |
| Tadarida jobensis | 0.35 | 0.02 | Baron et al. 1996 |
| Tadarida leucostigma | 0.38 | 0.02 | Baron et al. 1996 |
| Tadarida mops | 0.46 | 0.03 | Baron et al. 1996 |
| Tadarida niveiventer | 0.42 | 0.02 | Baron et al. 1996 |
| Tadarida plicata | 0.37 | 0.01 | Baron et al. 1996 † |
| Talpa europaea | 0.98 | 0.09 | Stephan et al. 1981 |
| Taphozous australis | 0.50 | 0.03 | Baron et al. 1996 |
| Taphozous hildegardeae | 0.53 | 0.03 | Baron et al. 1996 |
| Taphozous mauritianus | 0.53 | 0.03 | Baron et al. 1996 |
| Taphozous melanopogon | 0.52 | 0.02 | Baron et al. 1996 |
| Taphozous theobaldi | 0.66 | 0.03 | Baron et al. 1996 |
| Tarsius sp. | 3.47 | 0.15 | Stephan et al. 1981 |
| Tenrec ecaudatus | 2.48 | 0.15 | Stephan et al. 1981 |
| Tonatia bidens | 0.76 | 0.04 | Baron et al. 1996 |
| Tonatia schulzi | 0.49 | 0.02 | Baron et al. 1996 |
| Tonatia sylvicola | 0.73 | 0.03 | Baron et al. 1996 |
| Trachops cirrhosus | 0.97 | 0.05 | Baron et al. 1996 |
| Triaenops persicus | 0.26 | 0.02 | Baron et al. 1996 |
| Tupaia glis | 3.09 | 0.15 | Stephan et al. 1981 |
| Tupaia minor | 2.49 | 0.13 | Stephan et al. 1981 |
| Tylonycteris pachypus | 0.08 | 0.01 | Baron et al. 1996 |
| Tylonycteris robustula | 0.11 | 0.01 | Baron et al. 1996 |
| Uroderma bilobatum | 0.59 | 0.04 | Baron et al. 1996 |
| Urogale everetti | 4.13 | 0.17 | Stephan et al. 1981 |
| Vampyressa pusilla | 0.37 | 0.03 | Baron et al. 1996 |
| Vampyrodes caraccioloi | 0.91 | 0.06 | Baron et al. 1996 |
| Vampyrops helleri | 0.50 | 0.03 | Baron et al. 1996 |
| Vampyrops infuscus | 1.07 | 0.08 | Baron et al. 1996 |
| Vampyrops lineatus | 0.72 | 0.05 | Baron et al. 1996 |
| Vampyrops vittatus | 1.13 | 0.07 | Baron et al. 1996 |
| Vampyrum spectrum | 2.50 | 0.11 | Baron et al. 1996 |

Compilation subset total: 317 species. Full per-row errors for every species are in `outputs/benchmark_testset.csv`.
