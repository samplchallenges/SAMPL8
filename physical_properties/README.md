# The SAMPL8 physical properties challenge

We recently finalized work with GSK on data collection for a physical properties challenge. The data recently cleared legal review at GSK and challenge details and input files are now available. The challenge will include pKa prediction as well as logD between (diverse) organic phases.

For details on [SAMPL8 physical properties dataset collection, refer to this GCC/EuroSAMPL talk](https://dx.doi.org/10.5281/zenodo.4245127) by Aakankschit Nandkeolyar and Matthew Bahr. Full details of the experiments, along with the results of the measurements, are available in a paper draft which will be submitted after the challenge closes.

## Overview

We have collected pKa data for 23 diverse compounds, along with pH-dependent solubility (which was used to determine pKa). The pKa data will form the basis for an initial pKa challenge, followed by release of the pKa data.

We also measured logD for 11 of these compounds for distribution between different phases: : water-octanol, water-cyclohexane, water-ethyl acetate, water-heptane, water-MEK, water-TBME, and cyclohexane-DMF. Not all combinations of distribution coefficient are available because of compound solubility in the different phases. The total number of data points/combinations of (compound)x(phase identities) is between 40 and 50. These logD values will form the basis for a logD challenge which will run after the pKa challenge.  

We are planning on a deadline of Aug. 3, 2021 for the pKa challenge and Aug. 25, 2021 for the logD challenge. We will release pKa values immediately upon the close of the pKa challenge to allow these to be used in logD predictions if desired.

The general format of the challenge will follow that of SAMPL7, so refer to the [SAMPL7 physical properties overview paper](https://doi.org/10.26434/chemrxiv.14461962.v1) for details. Challenge instructions are also being made available here in the relevant subdirectories.

## A view of the compounds

![23 SAMPL8 molecules](images/SAMPL8-molecules.png)

**Fig 1. SAMPL8 Challenge molecules.**

## The pKa challenge

The pKa challenge involves predicting pKa values for SAMPL8 compounds SAMPL8-1 through SAMPL8-23 (except that for SAMPL8-11 and 13 we were only able to measure pH-dependent solubility but no pKa). pH-dependent solubility measurements are also available so please reach out if you are interested in predicting these. [Preliminary details of the experiments are available in this talk](https://zenodo.org/record/4245127).

As in [the SAMPL7 physical properties challenge](https://github.com/samplchallenges/SAMPL7/tree/master/physical_property/pKa), we will be collecting pKa values predicted as relative free energies to transition between microstates relative to a reference microstate for each compound; these can be estimated from predicted microstate populations. In some cases, compounds had multiple pKa values, and these are handled within the same framework. Refer to our [SAMPL7 report](https://doi.org/10.26434/chemrxiv.14461962.v1).

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
|           | octanol-water | cyclohexane-water | ethyl acetate-water | heptane-water | MEK-water | TBME-water | cyclohexane-DMF |
|-----------|--------------|-------------------|---------------------|---------------|-----------|------------|-----------------|
| SAMPL8-1  |       ✓      |         x         |          ✓          |       ✓       |     ✓     |      ✓     |        ✓        |
| SAMPL8-3  |       x      |         x         |          ✓          |       x       |     ✓     |      x     |        x        |
| SAMPL8-5  |       ✓      |         ✓         |          ✓          |       ✓       |     ✓     |      ✓     |        x        |
| SAMPL8-6  |       ✓      |         x         |          ✓          |       x       |     ✓     |      ✓     |        ✓        |
| SAMPL8-7  |       ✓      |         x         |          x          |       x       |     ✓     |      x     |        x        |
| SAMPL8-9  |       ✓      |         x         |          ✓          |       x       |     ✓     |      x     |        x        |
| SAMPL8-10 |       ✓      |         x         |          ✓          |       ✓       |     ✓     |      ✓     |        x        |
| SAMPL8-12 |       ✓      |         x         |          ✓          |       x       |     ✓     |      x     |        x        |
| SAMPL8-14 |       ✓      |         x         |          ✓          |       x       |     ✓     |      x     |        x        |
| SAMPL8-16 |       ✓      |         x         |          ✓          |       ✓       |     ✓     |      ✓     |        ✓        |
| SAMPL8-17 |       x      |         x         |          ✓          |       x       |     ✓     |      x     |        x        |


## What's here?
- A Powerpoint file (and PDF thereof) from GSK giving the identity of the compounds under consideration
- Submission formats
- Challenge instructions for the challenges ([pKa](pKa/pKa_challenge_instructions.md), [logD](logD/logD_challenge_instructions.md))
- Submission links:
  - [pKa](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL8-pka)
  - [logD](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL8-logD) (**As of July 24 this server is not yet working and we may have to wait til the pKa challenge concludes in order to fix it.**)

## What's coming?
- Analysis after the challenges close

## Manifest
- [`source_data/`](source_data): Files provided by GSK
- [`SAMPL8_molecule_ID_and_SMILES.csv`](SAMPL8_molecule_ID_and_SMILES.csv): A `.CSV` file containing SAMPL8 challenge molecule IDs and isomeric SMILES. SMILES were provided by GSK.
- [`microstates/`](microstates): This directory currently contains molecules in Tripos MOL2 (`.mol2`), SDF (`.sdf`), and PDB (`.pdb`) file format (generated from the SMILES in [`SAMPL8_molecule_ID_and_SMILES.csv`](SAMPL8_molecule_ID_and_SMILES.csv)). This directory will be updated at a later time to include enumerated microstates of each SAMPL molecule.
- [`images/`](images): Folder containing images related to this challenge in various formats.
- `pKa`: pKa challenge details and instructions
- `logD`: logD challenge details and instructions
