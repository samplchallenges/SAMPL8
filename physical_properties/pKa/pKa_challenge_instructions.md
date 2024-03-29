## pK<sub>a</sub> Challenge Instructions

The SAMPL8 pK<sub>a</sub> Challenge consists of predicting microscopic pK<sub>a</sub>'s of small molecules. Participants are asked to report relative free energies of protonation microstates calculated based on a provided reference state and pH detailed below, as in the SAMPL7 challenge ([paper](https://link.springer.com/article/10.1007/s10822-021-00397-3) and [preprint](https://dx.doi.org/10.26434/chemrxiv.14461962.v1)). Relative free energies of microstates were chosen as the reporting format rather than the microscopic pK<sub>a</sub> values because this makes analysis much more straightforward and provides additional insight. If your method cannot predict transition free energies or handle microstates but you would still like to participate, please reach out to David Mobley to discuss options.

**The submission deadline is Aug. 3, 2021**.

### Specifying relative free energies
For each molecule, the relative free energy must be predicted between the reference microstate and the rest of the enumerated microstates for that molecule at a reference pH of 0. Specifically, report the free energy for the reaction or transition *from the reference state to the specified microstate*, even if this does not represent a physical transition (e.g. even if it differs by more than a single proton). In other words, we are after the relative state free energy including the proton free energy (if that is helpful in clarifying), which could also be called the reaction free energy for the microstate transition which has the reference state (`SAMPL8-XX_micro000`) as the reactant and the alternate state as one of the products.

The first microstate in each CSV file indicated by `SAMPL8-XX_micro000` is our selected neutral reference state. For example, for molecule SAMPL8-1, if the reference microstate is `SAMPL8-1_micro000`, then relative free energies must be computed between `SAMPL8-1_micro000` and `SAMPL8-1_micro001`, `SAMPL8-1_micro000` and `SAMPL8-1_micro002`, and `SAMPL8-1_micro000` and `SAMPL8-1_micro003` (at a pH of 0). Any omitted microstates will be assumed to be so unfavorable in free energy that their population is negligible.

All possible tautomers of each ionization (charge) state are defined as distinct protonation microstates.

### Submitting your predictions
A submission template file can be found in the [submission_template/](submission_template/) directory and an example submission file can be found in [example_submission_file/](example_submission_file/). Predictions must be submitted via our AWS submissions server, [http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL8-pKa](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL8-pKa).

**For any critical updates, please follow our [email list](http://eepurl.com/dPj11j) (be sure to indicate interest in SAMPL8 and pKa).**.

### Filling out the submission file

- Fill one [`submission_template/pKa_prediction_template.csv`](submission_template/pKa_prediction_template.csv) template for all molecules predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method. Your filename should begin with the characters "pKa".

- Record the pair of microstates IDs associated with each relative free energy calculation between the reference state and the predicted microstates. Enumerated microstates, IDs, SMILES strings and SDF/MOL2 files can be found in https://github.com/samplchallenges/SAMPL8/tree/master/physical_property/pKa/microstates.

- We **highly recommend including your predicted macroscopic pKa values for each compound in your `Method` section** in the specified format; see template.

- If you have evaluated additional microstates, we ask that you include the same information as the other challenge molecules, but include the SMILES string in your submission and email a `.mol2` file of the microstate with explicit hydrogens and correct bond orders to `bergazin@uci.edu`, copying `dmobley@uci.edu`. Additonal microstate molecule ID's must be in the form `SAMPL8-XX_extra001`, where the molecule tag `SAMPL8-XX` is followed by `_extra` and some number `001` with three characters. See [`here`](example_submission_file/example_submission.csv) for an example. (We added some additional microstates from Stefan Kast and Nicolas Tielker (Dortmund) just prior to the challenge close, see `../microstates/README.md`. We also added some additional microstates from Michael Diedenhofen after the challenge close (2021-08-25), in case they are useful in analysis; see the same file. At the same time, Diedenhofen pointed out some possible duplicates, which are listed in the same place.)

- You may report only 1 relative free energy value per molecule per method.

- Each participant or organization is allowed only one ranked submission.

- Anonymous participation is not allowed.

- The energy units must be in kcal/mol.

- It is mandatory to submit predictions for all molecules. Incomplete submissions will not be accepted.

- Report relative free energy values to two decimal places (e.g. 13.71).

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [2,3]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log D challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

- Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions, a name for your computational protocol (that is 40 characters or less), the average compute time across all of the molecules in hours (GPU/CPU time for physical methods, query time for empirical methods), details of the computing resources and hardware used to make predictions, a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: `Predictions:`, `Participant name:`, `Participant organization:`, `Name:`, `Compute time:`, `Computing and hardware:`, `Software:`, `Category:`, `Method:`, and `Ranked:`, as illustrated in the example file. An example submission file can be found [here](example_submission_file/pKa-DanielleBergazinExampleFile-1.csv) to illustrate expected format when filling submission templates.

- For Method Category section please state if your prediction method can be better classified as an
experimental database lookup (DL), linear free energy relationship (LFER)[3], quantitative structure-property relationship or machine learning (QSPR/ML)[3], quantum mechanics without empirical correction (QM) models, quantum mechanics with linear empirical correction (QM+LEC), and combined quantum mechanics and molecular mechanics (QM+MM), or Other, using the category labels `DL`, `LFER`, `QSPR/ML`, `QM`, `QM+LEC`, `QM+MM` or `Other`. If you choose the “Other” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a `-`: predicted property `pKa`, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it `pKa-myname-1.csv`, where `myname` is arbitrary text of your choice. If you submit three prediction files, you would name them `pKa-myname-1.csv`, `pKa-myname-2.csv`, and `pKa-myname-3.csv`.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.

## Multiple submissions
As per our policy on multiple submissions, each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form. We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.

## Experimental details
pK<sub>a</sub> measurements were obtained via pH-dependent solubility measurement by AK Nandkeolyar and Matt Bahr and collaborators at GSK (via the Henderson-Hasselbalch equation), as discussed [in this talk](https://dx.doi.org/10.5281/zenodo.4245127) and in a forthcoming paper. The temperature was 22C.

## Method descriptions
Your method descriptions should give a detailed description of your approach, ideally with enough detail that someone could reproduce the work. These often serve to allow researchers to coordinate on why calculations which seem similar performed quite different in practice, so you should be sure to address how you generated poses, selected protonation states and tautomers if applicable, dealt with counterions, and various other aspects that might be important, as well as any method-specific details that, if varied, might result in different performance. For example, with MD simulations, the amount of equilibration might impact performance significantly in some cases, so this should also be included.

As per above, we are also highly recommending you include your predicted macro pKa values in this section in the specified format (see template) to allow us to use these for consistency checking later.

## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical pK<sub>a</sub> prediction tools etc.

## Submission of multiple predictions
Some participants use SAMPL to help evaluate various computational methods. To accommodate this, multiple prediction sets from a single research group or company are allowed, even for the same type of predictions if they are made by different methods. If you would like to submit predictions from multiple methods, you should fill a separate submission template files for each different method.

## References
[1] Gunner, M.R., Murakami, T., Rustenburg, A.S. et al. "Standard state free energies, not pKas, are ideal for describing small molecule protonation and tautomeric states." Journal of Computer-Aided Molecular Design 34, 561–573 (2020). https://doi.org/10.1007/s10822-020-00280-7

[2] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[3] Mobley, David L., Karisa L. Wymer, Nathan M. Lim, and J. Peter Guthrie. “Blind Prediction of Solvation Free Energies from the SAMPL4 Challenge.” Journal of Computer-Aided Molecular Design 28, no. 3 (March 2014): 135–50. https://doi.org/10.1007/s10822-014-9718-2

[4] U. A. Chaudry and P. L. A. Popelier. “Estimation of pKa Using Quantum Topological Molecular Similarity Descriptors:  Application to Carboxylic Acids, Anilines and Phenols.” The Journal of Organic Chemistry 2004 69 (2), 233-241. https://doi.org/10.1021/jo0347415

[5] Işık, M., Levorse, D., Rustenburg, A.S. et al. "pKa measurements for the SAMPL6 prediction challenge for a set of kinase inhibitor-like fragments." Journal of Computer-Aided Molecular Design 32, 1117–1138 (2018). https://doi.org/10.1007/s10822-018-0168-0

[5] Bergazin, T. D., Tielker, N., Zhang, Y., Mao, J., Gunner, M. R., Francisco, K., Ballatore, C. Kast, S. M., Mobley, D. L. "Evaluation of logP, pKa and logD predictions from the SAMPL7 blind challenge," Journal of Computer Aided Molecular Design, 2021. https://dx.doi.org/10.1007/s10822-021-00397-3
