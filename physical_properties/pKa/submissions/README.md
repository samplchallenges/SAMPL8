# SAMPL8 pK<sub>a</sub> Prediction Challenge

## Submissions and reference calculation

- All files in this directory are the pK<sub>a</sub> values submitted by the participants excepts for the `pKa_Chemaxon.csv` file, which contains the reference pK<sub>a</sub> values predicted using Chemaxon software.
### File Modification
- There were issues in reading the following files `pKa-3DS-1.csv`,`pKa-3DS-2.csv`, `pKa-3DS-3.csv`,`PKA_ECRISM.csv` and `pKa_Chemaxon.csv` given that the SMILE strings were in the same line as the predictions. Hence, these files were modified by removing the smile strings before analysis.
- The `pKa_Chemaxon.csv` file was modified by removing comments with SMILE strings.
- Since there were no experimental values for the following compounds - SAMPL8-11 and SAMPL8-13 the predictions were also deleted from each one of the submssions to use the automated analysis scripts.