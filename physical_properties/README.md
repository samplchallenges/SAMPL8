# The SAMPL8 physical properties challenge

We recently finalized work with GSK on data collection for a physical properties challenge. The data recently cleared legal review at GSK and we are now making challenge details and input files available. The challenge will include pKa prediction as well as logD between (diverse) organic phases.

For details on [SAMPL8 physical properties dataset collection, refer to this GCC/EuroSAMPL talk](https://dx.doi.org/10.5281/zenodo.4245127]) by Aakankschit Nandkeolyar and Matthew Bahr. Full details of the experiments, along with the results of the measurements, are available in a paper draft which will be submitted after the challenge closes.

## Overview

We have collected pKa data for 24 diverse compounds, along with pH-dependent solubility. The pKa data will form the basis for an initial pKa challenge, followed by release of the pKa data.

We also measured logD for 11 of these compounds for distribution between different phases: : water-octanol, water-cyclohexane, water-ethyl acetate, water-heptane, water-MEK, water-TBME, and cyclohexane-DMF. Not all combinations of distribution coefficient are available because of compound solubility in the different phases. The total number of data points/combinations of (compound)x(phase identities) is between 40 and 50. These logD values will form the basis for a logD challenge which will run after the pKa challenge.  


## The pKa challenge

The pKa challenge involves predicting pKa values for SAMPL8 compounds SAMPL8-1 through SAMPL8-23 (except that for SAMPL8-11 and 13 we were only able to measure pH-dependent solubility but no pKa). pH-dependent solubility measurements are also available so please reach out if you are interested in predicting these. [Preliminary details of the experiments are available in this talk](https://zenodo.org/record/4245127).

As in [the SAMPL7 physical properties challenge](https://github.com/samplchallenges/SAMPL7/tree/master/physical_property/pKa), we will be collecting pKa values predicted as relative free energies to transition between microstates relative to a reference microstate for each compound; these can be estimated from predicted microstate populations. In some cases, compounds had multiple pKa values, and these are handled within the same framework.

In some cases, compounds have multiple measured pKa values; submissions for these cases should still follow the same format. Details and submission file format will be posted shortly.

## The logD challenge

The logD challenge involves distribution of each compound between phases in a series of biphasic systems. For this to occur, each compound must have some solubility in each phase, and we only included compounds with measurable pKa, which limited the number of possible compounds.

Thus, The logD challenge covers compounds for which pKa values were measured which were adequately soluble in both solvents and partitioned adequately into the seven combinations of biphasic systems considered.

Our full dataset includes partitioning for these biphasic systems:
- octanol-water
- cyclohexane-water
- ethyl acetate-water
- heptane-water
- MEK-water
- TBME-water
- cyclohexane-DMF
In all cases water was Britton-Robinson buffer from Ricca. The pH used was pH 3 or pH 8 depending on the pKa of the compound, and will be specified when the log D challenge is launched (e.g. for one compound water might have been at pH 3 and for another, at pH 8)

For our compounds, we have measurements for these combinations of solute and solvent system:
- SAMPL8-5:
  - octanol-water
  - cyclohexane-water
  - ethyl acetate-water
  - heptane-water
  - MEK-water
  - TBME-water
  - NOT cyclohexane-DMF
- SAMPL8-1
  - octanol-water
  - NOT cyclohexane-water
  - ethyl acetate-water
  - heptane-water
  - MEK-water
  - TBME-water
  - cyclohexane-DMF
- SAMPL8-6
  - octanol-water
  - NOT cyclohexane-water
  - ethyl acetate-water
  - NOT heptane-water
  - MEK-water
  - TBME-water
  - cyclohexane-DMF
- SAMPL8-3
    - NOT octanol-water
    - NOT cyclohexane-water
    - ethyl acetate-water
    - NOT heptane-water
    - MEK-water
    - NOT TBME-water
    - NOT cyclohexane-DMF
- SAMPL8-10
  - octanol-water
  - NOT cyclohexane-water
  - ethyl acetate-water
  - heptane-water
  - MEK-water
  - TBME-water
  - NOT cyclohexane-DMF
- SAMPL8-7
    - octanol-water
    - NOT cyclohexane-water
    - NOT ethyl acetate-water
    - NOT heptane-water
    - MEK-water
    - NOT TBME-water
    - NOT cyclohexane-DMF
- SAMPL8-9
  - octanol-water
  - NOT cyclohexane-water
  - ethyl acetate-water
  - NOT heptane-water
  - MEK-water
  - NOT TBME-water
  - NOT cyclohexane-DMF
- SAMPL8-12
    - octanol-water
    - NOT cyclohexane-water
    - ethyl acetate-water
    - NOT heptane-water
    - MEK-water
    - NOT TBME-water
    - NOT cyclohexane-DMF
- SAMPL8-17
    - NOT octanol-water
    - NOT cyclohexane-water
    - ethyl acetate-water
    - NOT heptane-water
    - MEK-water
    - NOT TBME-water
    - NOT cyclohexane-DMF
- SAMPL8-16
  - octanol-water
  - NOT cyclohexane-water
  - ethyl acetate-water
  - heptane-water
  - MEK-water
  - TBME-water
  - cyclohexane-DMF
- SAMPL8-14
  - octanol-water
  - NOT cyclohexane-water
  - ethyl acetate-water
  - NOT heptane-water
  - MEK-water
  - NOT TBME-water
  - NOT cyclohexane-water

## What's here?
- A Powerpoint file (and PDF thereof) from GSK giving the identity of the compounds under consideration

## What's coming?
- Machine readable files containing the compounds comprising the pKa and logD challenges.
- Challenge timeline and deadlines
- Submission format
- Submission link

## Manifest
- `source_data`: Files provided by GSK
