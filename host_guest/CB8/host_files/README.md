# CB8 host files

The CB8 host files provided here are duplicated from [those used in SAMPL6](https://github.com/samplchallenges/SAMPL6/tree/master/host_guest/CB8AndGuests), meaning that the source file is the `CB8.sdf` file which originates from the PDB [ligand C8L](https://www4.rcsb.org/ligand/C8L) and downloaded as the `C8_ideal.sdf` file. Other files were generated from this as described in the SAMPL6 repo.

## Manifest
- `CB8.sdf`: Original source CB8 file from PDB
- `CB8.mol2`: mol2 format CB8 file generated from source file. AM1BCC charges were assigned using `Assign_Charge.ipynb`.
- `CB8.pdb`: PDB format CB8 file generated from source file
- `Assign_Charge.ipynb`: Jupyter notebook used to assign AM1BCC charges (via Openeye) to `CB8.mol2` host file.  
