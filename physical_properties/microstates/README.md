## SAMPL7 Molecules

23 small molecules are assigned moleculed IDs in the form of `SAMPL8-XX` from SAMPL8-1 to SAMPL8-23. This directory was updated on 5/3/2021 to include enumerated microstates.

Also provided are the molecules in Tripos MOL2 (`.mol2`), SDF (`.sdf`), and PDB (`.pdb`) file format.

Please note, the microstate lists provided here may not be comprehensive.

### Manifest
- [`make_mol2_sdf_pdb_files.ipynb`](make_mol2_sdf_pdb_files.ipynb) - The jupyter notebook used to generate the MOL2 (`.mol2`), SDF (`.sdf`), and PDB (`.pdb`) files for molecules using OpenEye toolkits and the SMILES strings and codenames found in the `SAMPL8_molecule_ID_and_SMILES.csv` files.
- [`SAMPL8_molecule_ID_and_SMILES.csv`](SAMPL8_molecule_ID_and_SMILES.csv) - A `.CSV` file that indicates SAMPL8 challenge molecule IDs and SMILES.
- `SAMPL8-X_microstates.csv` - Files include microstate IDs and canonical SMILES of each SAMPL8 microstate. The first microstate in each `.CSV` file indicated by SAMPL8-X_micro000 is our selected neutral reference state. Microstates were generated following the notebbok found [`here`](https://github.com/samplchallenges/SAMPL7/blob/master/physical_property/pKa/microstates/get_states.ipynb). Additional microstates were enumerated outside of this notebook by Chemicilaize (Chemaxon) and added to the `SAMPL8-X_microstates.csv` files here. 
