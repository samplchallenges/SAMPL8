# Analysis of macro pK<sub>a</sub>'s

Submitted relative free energies were converted to macro pK<sub>a</sub> predictions and analyzed here.

Participants submitted relative free energies between microstates.
As a consistency check, two methods are implemented in the [pKa_analysis.py](pKa_analysis.py) code to convert participant submissions to macro pK<sub>a</sub>'s. One method is the delta G method given by Junjun Mao (Levich Institute, City College of New York), and the other is a titration method given by David Mobley which follows the [Selwa et al](https://link.springer.com/article/10.1007/s10822-018-0138-6) SAMPL6 work from JCAMD 2018 and the [Gunner et al](https://link.springer.com/article/10.1007/s10822-020-00280-7) SAMPL6 work from 2020. The macro-pK<sub>a</sub>'s were caluclated using titration curves for each compound. The microstates from each compound were combined to form macro state transition curves and the pK<sub>a</sub>'s were calculated by finding the intersection points of these curves. 

General analysis of pK<sub>a</sub> predictions include calculated vs predicted pK<sub>a</sub> correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported.

Molecular statistics analysis was performed to indicate which molecules were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

The macro-pKas were calculated by finding the intersection points of the transition states in a titration curve. The transition states were assigned with reference to an arbitrary reference state based on the publication by [`Gunner et al`](https://link.springer.com/article/10.1007/s10822-020-00280-7)The naming convention of the transition states was as follows-
|Formal Charge Assigned|Transition State Formal Charge From|Transition State Formal Charge to|
|:------------:|:--------------------:|:----------------:|
|+2|+3|+2|
|+1|+2|+1|
|0|+1|0|
|-1|0|-1|
|-2|-1|-2|


The macrostate analysis performed using two methods- [`pKa_macrostate_analysis_popular_trasntions.py`](pKa_macrostate_analysis_popular_transitions.py) and [`pKa_macrostate_analysis_selected_trasntions.py`](pKa_macrostate_analysis_selected_transitions.py).

In the case of [popular transitions](pKa_macrostate_analysis_popular_transitions.py), the appropriate transition states for the predicted pKa were selected by means of popular vote, to elaborate further we looked at the most commonly occuring transition state for each pKa per molecule across all submissions.
If there were multiple experimental pKa's then we selected the top two most popular transition states and assigned the pKa with a higher value the lower of two formal charges while the other pKa was assigned to higher formal charge.

For the [selected transitions](pKa_macrostate_analysis_selected_transitions.py) method, a transition state was selected manually by looking at the pH-solubility curve and the predicted pKa corresponding to this transition was used in comparison to the experimental pKa.
The [selected transitions](selected_transitions.csv) were compiled based on the following assumptions while looking at the pH log-solubility curves-
* We assume the species is neutral at the lowest point of the log-solubility pH curves provided in the experimental data.
* pKa values that are greater than the pH of the lowest point of the log-solubility are treated as acidic with a formal charge of -1
* pKa values that are lesser than the ph of the lowest point of the log-solubility are treated as basic with a formal charge of +1


## Manifest
- [`selected_transitions.csv`](selected_transitions.csv)- A .csv file that contains the selected transition states that were manually selected for each compound. 
- [`titration_curves.py`](titration_curves.py)- Script used to generate titration curves data frame containing all combinations of experimental and predicted macro-pKas.
- [`Titration_Curves.pdf`](Titration_Curves.pdf)- Document that contains the derivation used to calculate the macro-pKa's from the microstate relative free energy changes submitted.
- [`titration_curve_plots/`](titration_curve_plots/)- This directory contains all the titration curves and a csv file that contains a dataframe with all the predicted and experimental macro-pKas.
- [`macro_pKas_data.csv`](titration_curve_plots/macro_pKas_data.csv)- Dataframe that contains all the combinations of predicted macro-pKas and experimental macro-pKas for all compounds across all submissions.
- [`pKa_macrostate_analysis_popular_transitions.py`](pKa_macrostate_analysis_popular_transitions.py)- Script used to generate performance statistics for macro-pKa analysis using popular transition states.
- [`pKa_macrostate_analysis_selected_transitions.py`](pKa_macrostate_analysis_popular_transitions.py)- Script used to generate performance statistics for macro-pKa analysis using selected transition states.
- [`functions_pKa_macrostate_analysis.py`](functions_pKa_macrostate_analysis.py)- Script that contains functions used in the estimation of performance statistics for macrostate analysis.
- [`popular_transitions_analysis/`](popular_transitions_analysis/)-  This directory contains plots associated with analysis of all and ranked methods using popular transition states.
- [`selected_transitions_analysis/`](selected_transitions_analysis/)- This directory contains plots associated with analysis of all and ranked methods using selected transition states.
 
