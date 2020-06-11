# Guests for the SAMPL8 CB8 Drugs of Abuse Challenge

Provided are the guests for this challenge in PDB, Tripos MOL2 and SDF file formats. The guests are codenamed from `G1` through `G9`.

## What's here

- `CB8_guest_smiles.txt`: Source file hand-generated from Isaacs-provided `CB8_chemdraw.cdx` by copying-and-pasting SMILES (by David Mobley, June 9, 2020).
- `input_maker.ipynb`: The jupyter notebook used to generate the PDB, MOL2 and SDF files for each guest using OpenEye toolkits and the SMILES strings and codenames found in `CB8_guest_smiles.txt`. For some guests, random stereoisomers were chosen; this is expected for `G5` which is a racemate, but for others, steroechemistry of the nitrogen center may require care.
- `.mol2`, `.sdf` and `.pdb` files for all guests: These were auto-generated from the SMILES via `input_maker.ipynb` using the OpenEye toolkits.
