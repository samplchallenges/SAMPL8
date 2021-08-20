## logD Challenge Instructions

The SAMPL8 Multi-solvent logD Challenge consists of predicting logD values for small molecules between a variety of different solvents (see grid in the [physical properties README.md](https://github.com/samplchallenges/SAMPL8/tree/master/physical_properties/README.md)). A submission template file can be found in the [`submission_template/`](submission_template) directory and an example submission file can be found in the [`example_submission_file`](example_submission_file) directory. Predictions must be submitted via our AWS submissions server, [http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL8-logD](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL8-logD).

**Predictions should be submitted as calculated logD values** in dimensionless units.

**The submission deadline is Aug. 24, 2021**.

In general the format/style of this challenge is similar to that for the SAMPL7 logP/logD challenge, except that we are using dimensionless units (rather than free energy units) and now, each solute may have been measured across multiple solvent phases, substantially changing the submission format. Note also that *only logD values are available*, not logP values, though pKa values will be released before the challenge deadline (after the pKa challenge closes in early August).

**Experimental details posted 2021-08-20**: We just provided additional clarification on the logD experiments; the experiments were done at pH 8 for compounds SAMPL8-1, 3, 5 and 6; all other compounds were measured at pH 3. This information will also be published in the SAMPL8 manuscript, which will be available after the challenge closes.

### Filling out the submission file

- Fill one [`submission_template/logD_prediction_template.csv`](submission_template/logD_prediction_template.csv) template for all molecules/solvents predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method. Your filename should begin with the characters "logD".

- Your logD prediction does NOT have to be SMXX_micro000 (the challenge provided microstate). If you use a microstate other than the challenge provided microstate, please fill out the Molecule ID/IDs considered (no commas) section using a molecule ID in the form of SMXX_extra001 (number can vary). In the METHOD DESCRIPTION SECTION in the submission file, please list the molecule ID and the SMILES string of the microstate that was used.

- If multiple microstates are used, please report the order of population in the aqueous phase in descending order. See further below for more info regarding predictions using multiple microstates.

- You may report only 1 logD value per molecule per method.

- Each participant or organization is allowed only one ranked submission.

- Anonymous participation is not allowed.

- The energy units must be dimensionless (logD units).

- Predictions must include predicted values for all compounds measured in the phases being considered (though our submission validation script will not necessarily check that you have done this)

- Not all phases need to be submitted; for example, you could submit only water-octanol predictions or only predictions for a selected subset of phases. However, participants submitting predictions for a reduced number of phases may not have their results included in the full analysis.

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [3,4]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log D challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions (broken out by solvent pair, see the example submission file), a name for your computational protocol (that is 40 characters or less), the average compute time across all of the molecules in hours (GPU/CPU time for physical methods, query time for empirical methods), details of the computing resources and hardware used to make predictions, a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: Predictions:, Participant name:, Participant organization:, Name:, Compute time:, Computing and hardware:, Software:, Category:, Method:, and Ranked:, as illustrated in the example file. An example submission file can be found here to illustrate expected format when filling submission templates.

- For the "Method Category" section please state if your prediction method can be better classified as an empirical modeling method, physical quantum mechanics (QM) modeling method, physical molecular mechanics (MM) modeling method, or mixed (both empirical and physical), using the category labels Empirical, Physical (MM), Physical (QM), or Mixed. Empirical models are prediction methods that are trained on experimental data, such as QSPR, machine learning models, artificial neural networks etc. Physical models are prediction methods that rely on the physical principles of the system, such as molecular mechanics or quantum mechanics based methods to predict molecular properties. If your method takes advantage of both kinds of approaches please report it as “Mixed”. If you choose the “Mixed” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a -: predicted property logP, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it logD-myname-1.csv, where myname is arbitrary text of your choice. If you submit three prediction files, you would name them logD-myname-1.csv, logD-myname-2.csv, and logD-myname-3.csv.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.

## Multiple submissions
As per our policy on multiple submissions, each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form. We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.


## Method descriptions
Your method descriptions should give a detailed description of your approach, ideally with enough detail that someone could reproduce the work. These often serve to allow researchers to coordinate on why calculations which seem similar performed quite different in practice, so you should be sure to address how you generated poses, selected protonation states and tautomers if applicable, dealt with counterions, and various other aspects that might be important, as well as any method-specific details that, if varied, might result in different performance. For example, with MD simulations, the amount of equilibration might impact performance significantly in some cases, so this should also be included.


## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical logD prediction tools etc.

## Submission of multiple predictions
Some participants use SAMPL to help evaluate various computational methods. To accommodate this, multiple prediction sets from a single research group or company are allowed, even for the same type of predictions if they are made by different methods. If you would like to submit predictions from multiple methods, you should fill a separate submission template files for each different method.

## References
[1] Gunner, M.R., Murakami, T., Rustenburg, A.S. et al. "Standard state free energies, not pKas, are ideal for describing small molecule protonation and tautomeric states." Journal of Computer-Aided Molecular Design 34, 561–573 (2020). https://doi.org/10.1007/s10822-020-00280-7

[2] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[3] Mobley, David L., Karisa L. Wymer, Nathan M. Lim, and J. Peter Guthrie. “Blind Prediction of Solvation Free Energies from the SAMPL4 Challenge.” Journal of Computer-Aided Molecular Design 28, no. 3 (March 2014): 135–50. https://doi.org/10.1007/s10822-014-9718-2

[4] U. A. Chaudry and P. L. A. Popelier. “Estimation of pKa Using Quantum Topological Molecular Similarity Descriptors:  Application to Carboxylic Acids, Anilines and Phenols.” The Journal of Organic Chemistry 2004 69 (2), 233-241. https://doi.org/10.1021/jo0347415

[5] Işık, M., Levorse, D., Rustenburg, A.S. et al. "pKa measurements for the SAMPL6 prediction challenge for a set of kinase inhibitor-like fragments." Journal of Computer-Aided Molecular Design 32, 1117–1138 (2018). https://doi.org/10.1007/s10822-018-0168-0

[5] Bergazin, T. D., Tielker, N., Zhang, Y., Mao, J., Gunner, M. R., Francisco, K., Ballatore, C. Kast, S. M., Mobley, D. L. "Evaluation of logP, pKa and logD predictions from the SAMPL7 blind challenge," Journal of Computer Aided Molecular Design, 2021. https://dx.doi.org/10.1007/s10822-021-00397-3
