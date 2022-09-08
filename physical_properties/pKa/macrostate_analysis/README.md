# Analysis of macro pK<sub>a</sub>'s

Submitted relative free energies were converted to macro pK<sub>a</sub> predictions and analyzed here.

Participants submitted relative free energies between microstates.
As a consistency check, two methods are implemented in the [pKa_analysis.py](pKa_analysis.py) code to convert participant submissions to macro pK<sub>a</sub>'s. One method is the delta G method given by Junjun Mao (Levich Institute, City College of New York), and the other is a titration method given by David Mobley which follows the [Selwa et al](https://link.springer.com/article/10.1007/s10822-018-0138-6) SAMPL6 work from JCAMD 2018 and the [Gunner et al](https://link.springer.com/article/10.1007/s10822-020-00280-7) SAMPL6 work from 2020. The macro-pK<sub>a</sub>'s were caluclated using titration curves for each compound. The microstates from each compound were combined to form macro state transition curves and the pK<sub>a</sub>'s were calculated by finding the intersection points of these curves. 

General analysis of pK<sub>a</sub> predictions include calculated vs predicted pK<sub>a</sub> correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported.

Molecular statistics analysis was performed to indicate which molecules were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

The macro-pKas were calculated by finding the intersection points of the transition states in a titration curve. The transition states were assigned with reference to an arbitrary reference state based on the publication by [`Gunner et al`](https://link.springer.com/article/10.1007/s10822-020-00280-7)The naming convention of the transition states was as follows-
|Formal Charge|Transition State From|Transition State to|
|:------------:|:--------------------:|:----------------:|
|+3|+2|+3|
|+2|+1|+2|
|+1|0|+1|
|-1|-1|0|
|-2|-2|-1|

The macrostate analysis performed using [`pKa_macrostate_analysis.py`](pKa_macrostate_analysis.py) assumes that the transitions states for both the experimental and predited pKa are the same. The appropriate transition states for the predicted pKa were selected by means of popular vote, to elaborate further we looked at the most commonly occuring transition state for each pKa per molecule across all submissions. This was selected as the transition state used for each prediction associated with each pKa for each molecule in a submission. Additionally, a minimum error was added to a specific pKa of a compound in a submission if the submission did not contain predictions for that specific compound using the popular transition state. This minimum error was assigned by either setting the predicted pKa for a compound with a missing popular transition in a submission to either 0 or 14 depending on which prediction would have the largest error.

## Manifest
- [`titration_curves.py`](titration_curves.py)- Script used to generate titration curves data frame containing all combinations of experimental and predicted macro-pKas.
- [`Titration_Curves.pdf`](Titration_Curves.pdf)- Document that contains the derivation used to calculate the macro-pKa's from the microstate relative free energy changes submitted.
- [`titration_curve_plots/`](titration_curve_plots/)- This directory contains all the titration curves and a csv file that contains a dataframe with all the predicted and experimental macro-pKas.
- [`macro_pKas_data.csv`](titration_curve_plots/macro_pKas_data.csv)- Dataframe that contains all the combinations of predicted macro-pKas and experimental macro-pKas for all compounds across all submissions.
- [`pKa_macrostate_analysis.py`](pKa_macrostate_analysis.py)- Script used to generate performance statistics for macro-pKa analysis.
- [`functions_pKa_macrostate_analysis.py`](functions_pKa_macrostate_analysis.py) - Script that contains functions used in the estimation of performance statistics for macrostate analysis.
- [`analysis_ouptuts_all`](analysis_outputs_all/)- This directory contains bar plots and correlation plots associated with the performance statistics for all submissions.
- [`analysis_outputs_ranked`](analysis_outputs_ranked/)- This directory contains bar plots and correlation plots associated with the performance statistics for all ranked submissions.