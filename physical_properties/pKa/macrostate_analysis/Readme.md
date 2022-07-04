# Analysis of macro pK<sub>a</sub>'s

Submitted relative free energies were converted to macro pK<sub>a</sub> predictions and analyzed here.

Participants submitted relative free energies between microstates.
As a consistency check, two methods are implemented in the [pKa_analysis.py](pKa_analysis.py) code to convert participant submissions to macro pK<sub>a</sub>'s. One method is the delta G method given by Junjun Mao (Levich Institute, City College of New York), and the other is a titration method given by David Mobley which follows the [Selwa et al](https://link.springer.com/article/10.1007/s10822-018-0138-6) SAMPL6 work from JCAMD 2018 and the [Gunner et al](https://link.springer.com/article/10.1007/s10822-020-00280-7) SAMPL6 work from 2020. The macro-pK<sub>a</sub>'s were caluclated using titration curves for each compound. The microstates from each compound were combined to form macro state transition curves and the pK<sub>a</sub>'s were calculated by finding the intersection points of these curves. 

General analysis of pK<sub>a</sub> predictions include calculated vs predicted pK<sub>a</sub> correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported.

Molecular statistics analysis was performed to indicate which molecules were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

## Manifest
- [`titration_curves.py`](titration_curves.py)- Script used to generate titration curves data frame containing all combinations of experimental and predicted macro-pKas.
- [`Titration_Curves.pdf`](Titration_Curves.pdf)- Document that contains the derivation used to calculate the macro-pKa's from the microstate relative free energy changes submitted.
- [`titration_curves_plots/`](titration_curves_plots/)- This directory contains all the titration curves and a csv file that contains a dataframe with all the predicted and experimental macro-pKas.
- [`macro_pKas_data.csv`](titration_curves_plots/macro_pKas_data.csv)- Dataframe that contains all the combinations of predicted macro-pKas and experimental macro-pKas for all compounds across all submissions.
