# Exploratory Analysis of Combination Lock Tolerances and Keyspace Implications

**Author:** Tracktor97  
**Date:** 2/17/26

---

## Abstract

This study investigates the mechanical tolerances of a consumer-grade combination lock and examines how those tolerances affect its effective keyspace. By systematically varying each dial from the original combination and recording the success or failure of unlocking attempts, this experiment explores the relationship between manufacturing tolerances, usability, and security implications.

The findings suggest that measurable tolerance windows may significantly reduce the effective keyspace of the lock relative to its nominal design.

---

## Introduction

Combination locks are commonly assumed to function on discrete numerical inputs. In theory, a lock with three discs ranging from 0–39 has a keyspace of 40³ = 64,000 possible combinations.

However, physical systems are not mathematically discrete. Mechanical tolerances, material properties, machining precision, and component geometry introduce deviation from idealized behavior. This experiment aims to determine:

- How wide the mechanical tolerance window is for each disc.
- Whether tolerances reduce the effective keyspace.
- What mechanical factors may contribute to observed behavior.
- Whether usability considerations influence security trade-offs.

---

## Methodology

### Original Combination
33-4-13

### Experimental Procedure

1. Begin with the known working combination.
2. Shift one disc at a time ±1 unit.
3. If a combination fails, refine by ±0.5 units.
4. Record each attempt as:
   - Adequate (opens normally)
   - Adequate with manipulation (wiggling, tension, or rapid movement required)
   - Inadequate (does not open)

Only one disc was adjusted at a time to isolate tolerance effects. Disc 2 and Disc 3 were tested more narrowly due to time constraints.

---

## Results

### Disc 1 Variation

| Combination | Result |
|------------|--------|
| 33-4-13 | Adequate (original) |
| 32-4-13 | Adequate |
| 32.5-4-13 | Adequate (with manipulation) |
| 31-4-13 | Adequate (with manipulation) |
| 30-4-13 | Inadequate |
| 34-4-13 | Adequate |
| 35-4-13 | Adequate (intense manipulation) |
| 36-4-13 | Inadequate |

Disc 1 demonstrated a tolerance window of approximately ±2 units from the original value, though values farther from center required increasing manipulation.

### Disc 2 Variation

| Combination | Result |
|------------|--------|
| 33-3-13 | Adequate |
| 33-2-13 | Inadequate |
| 33-2.5-13 | Inadequate |
| 33-5-13 | Adequate |
| 33-6-13 | Adequate |
| 33-7-13 | Inadequate |
| 33-6.5-13 | Inadequate |

Disc 2 appeared to exhibit tighter tolerances than Disc 1.

### Disc 3 Variation

| Combination | Result |
|------------|--------|
| 33-4-12 | Adequate (light manipulation) |
| 33-4-12.5 | Adequate |
| 33-4-13.5 | Adequate |
| 33-4-14 | Adequate |

Disc 3 also demonstrated a measurable tolerance window, though testing was limited.

---

## Analysis

### Effective Keyspace Reduction

If each disc allows approximately ±2 units of tolerance under certain conditions, the number of effective working combinations increases significantly relative to the nominal combination count.

This reduces the effective security margin and increases the probability of a successful brute-force attempt compared to purely discrete assumptions.

### Mechanical Considerations

The observed tolerances may result from:

- Width of the gate/channel in each disc.
- Thickness of the locking component (e.g., ball bearing or bar).
- Machining precision of disc interfaces.
- Material deformation under tension.
- Intentional engineering trade-offs to reduce user frustration (false negatives).

If tolerances were tightened, usability may decrease. Excessively tight tolerances could lead to customer dissatisfaction due to difficulty opening the lock even with correct input.

---

## Discussion

This experiment highlights the gap between theoretical and physical security models. In mathematical abstraction, keyspaces are discrete and exact. In physical systems, tolerances blur those boundaries.

The findings parallel concepts in cybersecurity such as:

- Side-channel leakage
- Timing variance
- Information revealed through imperfect system implementation

Even small deviations from ideal design can meaningfully alter the attack surface.

Further research could include:

- Testing multiple discs offset simultaneously.
- Applying constant tension to detect mechanical feedback signals.
- Comparing multiple lock brands or models.
- Quantifying statistical success rates across repeated trials.

---

## Limitations

- Single lock model tested.
- Limited number of trials for Disc 2 and Disc 3.
- Manipulation pressure not quantitatively measured.
- No statistical modeling performed.

---

## Conclusion

This exploratory study demonstrates that measurable mechanical tolerances can reduce the effective keyspace of a combination lock. While not conclusive across all lock types, the results illustrate how engineering trade-offs between usability and precision may influence security outcomes.
