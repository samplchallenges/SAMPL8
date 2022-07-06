# The SAMPL8 Blind Prediction Challenges for Computational Chemistry
[![DOI](https://zenodo.org/badge/271066350.svg)](https://zenodo.org/badge/latestdoi/271066350)



Challenge details, inputs, and results for the SAMPL8 series (phase) of challenges. Each individual SAMPL8 challenge may be broken up into multiple stages.

See the [SAMPL website](https://samplchallenges.github.io/) for information on the Statistical Assessment of the Modeling of Proteins and Ligands (SAMPL) series of challenges as a whole. This repository focuses specifically on the SAMPL8 series of challenges. Additionally, see the [SAMPL community](https://zenodo.org/communities/sampl/?page=1&size=20) on Zenodo for content related to the SAMPL series of challenges. If you wish to use Zenodo to post your presentation slides, datasets, and/or other SAMPL related material, and get a DOI for them, please upload to the community [here](https://zenodo.org/communities/sampl/?page=1&size=20) so that your content will be listed.

Because these files are available publicly, we have no record of who downloads them. Therefore, you should sign up for notifications. Specifically, if you want to receive updates if we uncover any problems, it is imperative that you either (a) [sign up for the SAMPL e-mail list](https://mailchi.mp/e36018629725/sampl8-sign-ups), or (b) sign up for notifications of changes to this GitHub repository (the Watch button, above); ideally you would do both.

Please note that some aspects of the SAMPL7 series of challenges are still ongoing, but as we are launching a new host-guest challenge that marks the beginning of the SAMPL8 series of challenges, so we have opened up this repository.

## Acknowledging and citing SAMPL

If you've benefitted from our work on the SAMPL series of challenges, please be sure to acknowledge our SAMPL NIH grant in any publications/presentations. This funded host-guest experiments, as well as our work organizing and administrating these challenges. You may acknowledge SAMPL by saying something like, "We appreciate the National Institutes of Health for its support of the SAMPL project via R01GM124270 to David L. Mobley (UC Irvine)."

We also ask you to cite the SAMPL dataset(s) you used. These are versioned on Zenodo, and the latest DOI is here: [![DOI](https://zenodo.org/badge/271066350.svg)](https://zenodo.org/badge/latestdoi/271066350) . Click through for access to all data releases. You may cite these sets by their DOI.

Of course, we also appreciate it if you cite any overview/experimental papers relevant to the particular SAMPL challenge you participated in.

## What's here
- Host-guest challenge files for the CB8 challenge and results from this challenge
- Host-guest challenge files for the GDCC challenge.
- [Host-guest participation instructions](https://github.com/samplchallenges/SAMPL8/blob/master//host_guest_instructions.md) with information on the submissions format, etc. Submission templates are available in the the subdirectories for individual host-guest systems.
- Introductory details on the GSK physical properties challenge.
- GSK physical properties challenge molecules in Tripos MOL2, SDF, and PDB file format, and enumerated microstates

## What's coming
This challenge is concluded; analysis results are still forthcoming for the physical properties challenge.


## Changes and Data Set Versions

### Releases
- **Release 0.1** ([DOI 10.5281/zenodo.4029560](http://dx.doi.org/10.5281/zenodo.4029560), Sept. 14, 2020): Release version of the info that was here prior to the closing of the [CB8 "drugs of abuse" challenge](https://github.com/samplchallenges/SAMPL8/tree/master/host_guest/CB8) from Isaacs.

### Changes not in a release

- Add SAMPL8 CB8 submissions, user map, utilities, functions, and analysis scripts; add/update README files at all directories in SAMPL8 repo.(9/25/20)
- Add experimental measurements and link for CB8 experimental publication. (9/25/20)
- Updates submission files (give unique method names and edit ext) (10/1/20)
- Updates analysis script (10/1/20)
- Add preliminary results (plots, tables, etc) for the host-guest challenge. Currently only includes CB8. (10/1/20)
- Add source files and tentative deadline for GDCC challenge (2020-10-14)
- Add guest and host curated/generated sdf,mol2,pdb files for the GDCC challenge (10/17/20)
- Update CB8 experimental results and analysis (plots, tables, etc) to correct errors in the first version which had been posted. Note the experimental Ka and/or binding free energy values for Morphine, Hydromorphone, and Cocaine have been updated; see [pdf](https://github.com/samplchallenges/SAMPL8/blob/master/host_guest/Analysis/ExperimentalMeasurements/CB8-DOA-SAMPL-Answer-Sheet-20201014.pdf) and [docx](https://github.com/samplchallenges/SAMPL8/blob/master/host_guest/Analysis/ExperimentalMeasurements/CB8-DOA-SAMPL-Answer-Sheet-20201014.docx) answer sheets. (10/17/20)
- Add minor additional notes on GDCC experiments/provenance (2020-12-23)
- Add GDCC submission template, update host-guest submission instructions, update README files (1/14/21)
- Add GDCC submission server link (1/20/21)
- Add info on physical properties challenge
- 2021-03-02: Add links to talk on experimental data collection for GSK physical properties challenge.
- 2021-03-10: Add GSK physical properties challenge molecules in Tripos MOL2, SDF, and PDB file format (with enumerated microstates of each molecule to be added at a later date).
- Add GDCC experimental measurements (3/25/21)
- 2021-04-13: Add GDCC submissions for analysis
- 2021-04-13: Add GSK challenge deadline
- 2021-05-04: Add a submission template and an example submission file for both the pKa and logD challenge. Add enumerated microstates for the challenge molecules.
- 2021-07-05: Update example submission for pKa challenge; add pKa challenge instructions; update README files.
- 2021-07-06: Add GDCC (TEMOA/TEETOA) to SAMPL8 host-guest analysis, add/update preliminary statistics and analysis tables, plots, and figures for GDCC dataset.
- 2021-07-24: Add submission link for logD challenge; update submission format example for logD challenge. Add logD challenge instructions.
- 2021-08-03: Add additional optional microstates from Stefan Kast/Nicolas Tielker from TU Dortmund
- 2021-08-20: Add experimental pH for logD measurements (pH 8 for SAMPL8-1, 3, 5 and 6; pH 3 for all other compounds)
- 2021-08-23: Update logD deadline to Aug. 31
- 2021-08-25: Add additional retrospective microstate information, and information on possible duplicate microstates, in case it is helpful for those doing analysis. See `microstates/README.md`.
- 2021-09-07: Add logD submissions, user map
- 2021-10-01: Add Chemaxon pK<sub>a</sub> predictions
- 2021-10-01: Add link to [preprint on physical properties experiments](https://chemrxiv.org/engage/chemrxiv/article-details/61547c46b19c7e6aade3c2b1)
- 2022-04-26: Add [experimental publication doi:10.1021/acs.jpcb.2c00628](https://doi.org/10.1021/acs.jpcb.2c00628) for Gibb GDCC Dataset. 
- 2022-07-05: Add [alternative experimental measurements](https://github.com/samplchallenges/SAMPL8/blob/master/physical_properties/experimental_data/pKa%20-%20SiriusT3%20measurements.csv) and [comparison with original data](https://github.com/samplchallenges/SAMPL8/blob/master/physical_properties/experimental_data/SAMPL8%20-%20SiriusT3%20measurements.pdf) of four SAMPL8 compounds. 

## Challenge construction

### Overview

The SAMPL8 phase of challenges included two new host-guest challenges (CB8 and Gibb's deep cavity cavitands). We are currently running our physical properties challenge with GSK (details below) including pKa and logD prediction.


### The CB8 challenge

The CB8 "drugs of abuse" challenge focused on binding of CB8 to seven guests which are drugs of abuse, including morphine, hydromorphine, methamphetamine, cocaine and others. Binding has been experimentally characterized, a provisional patent filed, and the Isaacs group has prepared a paper for publication [available here](https://chemrxiv.org/articles/preprint/In_Vitro_and_In_Vivo_Sequestration_of_Phencyclidine_by_Me4Cucurbit_8_uril/12994004). Experimental results/data is available [in this repository](https://github.com/samplchallenges/SAMPL8/blob/master/host_guest/Analysis/ExperimentalMeasurements/).

**Deadline**: The deadline for CB8 submissions was September 15, 2020. [The submission format is available](https://github.com/samplchallenges/SAMPL8/blob/master/host_guest/CB8/CB8_submissions.txt).

### The GDCC challenge

The GDCC challenge focused on binding of two Gibb Deep Cavity Cavitand (GDCC) hosts (related to the familiar OctaAcid) to five guests. Binding has been experimentally characterized and these compounds form the basis of this challenge, as detailed [in this repository](host_guest/GDCC/README.md).

**Deadline**: The deadline for GDCC submissions was Feb. 21, 2021 (updated from Feb. 4, 2021). [The submission format is available](https://github.com/samplchallenges/SAMPL8/blob/master/host_guest/GDCC/GDCC_submissions.txt). Additionally, [SAMPL8 GDCC predictions may be submitted here](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL8-GDCC). Challenge is closed and experimental results/data is [available here](https://github.com/samplechallenges/SAMPL8/blob/master/host_guest/Analysis/ExperimentalMeasurements/Final-Data-Table-031621-SAMPL8.docx)

GDCC experimental publication is available. doi:10.1021/acs.jpcb.2c00628

### The GSK physical properties challenges

We recently concluded work with GSK for a physical properties challenge. The challenge involved:

- pKa data for 24 compounds
- pH-dependent solubility for these compounds
- logD for 11 of these compounds for distribution between different phases: water-octanol, water-cyclohexane, water-ethyl acetate, water-heptane, water-MEK, water-TBME, and cyclohexane-DMF. Not all combinations of distribution coefficient are available because of compound solubility in the different phases. The total number of data points/combinations of (compound)x(phase identities) is between 40 and 50.

We first ran a pKa challenge on the 24 compounds, and then a logD challenge.

Details on dataset collection [are available in this talk from the GCC/EuroSAMPL workshop](https://dx.doi.org/10.5281/zenodo.4245127) and then further described [in this preprint at chemRxiv](https://dx.doi.org/10.33774/chemrxiv-2021-8gd90) (DOI 10.33774/chemrxiv-2021-8gd90).

GSK physical properties challenge molecules in Tripos MOL2, SDF, and PDB file format are now available (3/10/21). Enumerated microstates of each molecule are available (as of 5/4/21).

Generally, the challenge structure resembles that of the [SAMPL7 physical properties challenge](https://doi.org/10.26434/chemrxiv.14461962.v1).

Submission deadlines were in August, 2021, as [discussed in the challenge details](physical_properties/README.md). Submission links were available from the files giving instructions for each challenge component.


## MANIFEST
- [`host_guest/`](host_guest/): Details on host-guest challenges.
- [`physical_properties/`](physical_properties/): Details on the GSK physical properties challenge

## SAMPL-related
If you give a SAMPL-related talk or presentation or an analysis of its data, and are willing to share publicly, please consider posting on Zenodo and linking it to the [SAMPL Zenodo community](https://zenodo.org/communities/sampl?page=1&size=20).

## LICENSE

This material here is made available under CC-BY and MIT licenses, as appropriate:

- MIT for all software/code
- CC-BY 4.0 for all other materials

In other words, we are happy to have you reuse any of the materials here for any purpose as long as proper credit/citation is given.
