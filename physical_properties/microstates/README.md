## SAMPL8 Molecules

23 small molecules are assigned moleculed IDs in the form of `SAMPL8-XX` from SAMPL8-1 to SAMPL8-23. This directory was updated on 5/3/2021 to include enumerated microstates.

Also provided are the molecules in Tripos MOL2 (`.mol2`), SDF (`.sdf`), and PDB (`.pdb`) file format.

Please note, the microstate lists provided here may not be comprehensive, and indeed, on 2021-08-03 we added several additional optional microstates (for compounds 1, 3, 12, 14, 21 and 22) from Stefan Kast and Nicolas Tielker, with microstate IDs including "dortmund". These are optional and included in case they are helpful. There may be some redundancy, e.g. we noticed that SAMPL8-21_dortmund004 and SAMPL8-21_dortmund005 seem equivalent, and SAMPL8-22_dortmund001 and SAMPL8-22_dortmund003 seem equivalent.

We also added some additional microstates from Michael Diedenhofen (Biovia/Dassault/3DS) he used in his submission, after the challenge closed, in case these are useful in analysis.

Diedenhofen also kindly provided this list of microstates that he thinks are equivalent; if you have any additions, please let us know:
> SAMPL8-4_micro000 <-> SAMPL8-4_micro004
> SAMPL8-14_micro000 <-> SAMPL8-14_micro016
> SAMPL8-14_micro002 <-> SAMPL8-14_micro023
> SAMPL8-14_micro006 <-> SAMPL8-14_micro034
> SAMPL8-14_micro013 <-> SAMPL8-14_micro033
> SAMPL8-14_micro017 <-> SAMPL8-14_micro030

### Manifest
- [`make_mol2_sdf_pdb_files.ipynb`](make_mol2_sdf_pdb_files.ipynb) - The jupyter notebook used to generate the MOL2 (`.mol2`), SDF (`.sdf`), and PDB (`.pdb`) files for molecules using OpenEye toolkits and the SMILES strings and codenames found in the `SAMPL8_molecule_ID_and_SMILES.csv` files.
- [`SAMPL8_molecule_ID_and_SMILES.csv`](SAMPL8_molecule_ID_and_SMILES.csv) - A `.CSV` file that indicates SAMPL8 challenge molecule IDs and SMILES.
- `SAMPL8-X_microstates.csv` - Files include microstate IDs and canonical SMILES of each SAMPL8 microstate. The first microstate in each `.CSV` file indicated by SAMPL8-X_micro000 is our selected neutral reference state. Microstates were generated following the notebbok found [`here`](https://github.com/samplchallenges/SAMPL7/blob/master/physical_property/pKa/microstates/get_states.ipynb). Additional microstates were enumerated outside of this notebook by Chemicialize (Chemaxon) and added to the `SAMPL8-X_microstates.csv` files here. Additionally, on 2021-08-03, we added additional microstates from Stefan Kast and Nicolas Tielker (TU Dortmund) with IDs of the form `SAMPL8-X_dortmundYYY` in the microstate csv files.
- `dortmund_microstates`: Structure files corresponding to the additional microstates provided by Kast/Tielker (Dortmund), added on 2021-08-03.
- `dassault_microstates`: Microstates used by Michael Diedenhofen (Dassault Systemes/3DS/Biovia) in his submission, added after the challenge close (2021-08-25).
