# Analysis Outputs of macro pK<sub>a</sub>'s
Contains data and plots associated with macrostate analysis across all ranked submissions.
## Manifest
- [`abs_error_by_method_plot.pdf`](abs_error_by_method_plot.py) - A plot that shows the absolute error across all methods.
- [`abs_error_bymol_plot.pdf`](abs_error_bymol_plot.pdf) - A plot that shows the absolute error across all molecules.
- [`Correlation_Plots`](Correlation_Plots/) - This directory contains correlation statistics data as well as correlation plots associated with each submission.
- [`mean_abs_error_plot.pdf`](mean_abs_error_plot.pdf) - A plot that shows the mean absolute error for each molecule.
- [`mean_error_plot.pdf`](mean_error_plot.pdf) - A plot that shows the mean error for each molecule.
- [`rmse_plot.pdf`](rmse_plot.pdf) - A plot that shows the root mean squared error for each molecule.
- [`Error_statistics.csv`](titration_curve_plots/macro_pKas_data.csv) - A `.csv` file that contains the error statistics (ME, MAE and RMSE) associated with predictions from across all ranked submissions.
- [`macrostate_pKa_data.csv`](macrostate_pKa_data.csv) - A `.csv` file that contains the macro pKa's computed from the microstates.
- [`popular_transitions_pKa_data.csv`](popular_transitions_pKa_data.csv) - A `.csv` file that contains the popular transition states for each compound i.e the dominant transition state that occured most frequently across all ranked submissions for each compound.  Please note that the column "Formal Charge" represents the charged state that the molecule is transitioning to.