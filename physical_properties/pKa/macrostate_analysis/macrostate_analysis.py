# Macrostate Analysis
# =============================================================================
# =============================================================================
# =============================================================================

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
from titration_curves import pKaSubmission
from titration_curves import load_submissions
from titration_curves import DeltaG, total_pop_charge,pop_charge,pop_charge_microstates

# =============================================================================
# CONSTANTS
# =============================================================================
pKa_SUBMISSIONS_DIR_PATH = '../submissions'
EXPERIMENTAL_DATA_FILE_PATH = '../experimental_pKas.csv'
USER_MAP_FILE_PATH = '../SAMPL8-pKa-user-map.csv'
if not os.path.exists("./Performance_stats_plots"):
    os.makedirs("./Performance_stats_plots")

# Define Constants for relative FE calculations
kB = 1.381 * 6.02214 / 1000.0 # Converts Boltzmann constant to kJ/mol*K
beta = (1 / ((kB/4.184) * 300)) # Convert to kcal
C_unit = (1 /beta)*np.log(10)# C_unit = RT*ln10 from Gunner et. al
pH_vals = np.arange(-15,22,0.1) # pH values for estimating all macro-pKa's from submissions
# =============================================================================
# Load data from submissions and Experimental Data
# =============================================================================

microstate_dt = load_submissions(pKa_SUBMISSIONS_DIR_PATH,USER_MAP_FILE_PATH)

# Load experimental data
with open(EXPERIMENTAL_DATA_FILE_PATH, 'r') as f:
    # experimental_data = pd.read_json(f, orient='index')
    names = ('Molecule ID', 'pKa mean', 'pKa SEM')
    experimental_data = pd.read_csv(f, names=names, skiprows=1)

# Convert numeric values to dtype float.
for col in experimental_data.columns[1:7]:
    experimental_data[col] = pd.to_numeric(experimental_data[col], errors='coerce')

experimental_data.set_index("Molecule ID", inplace=True)
experimental_data["Molecule ID"] = experimental_data.index

# =============================================================================
# Combining all predicted and experimental pKa's
# =============================================================================
pKa_dt = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
for submission in microstate_dt:
    submission_data  = submission.data
    # Create a dictionary with the microstate details for each molecule in the submission
    molecules = {}
    for index, row in submission_data.iterrows():
        SM = index
        state = row["ID tag"]
        charge = row["total charge"]
        rfe = row["pKa mean"]
        sem = row["pKa SEM"]
        model_uncertainty = row["pKa model uncertainty"]

        if SM in molecules:
            molecules[SM].append((state, rfe, charge, sem, model_uncertainty))
        else:
            molecules[SM] = [(state, rfe, charge, sem, model_uncertainty)]

    # Loop over molecules, convert to state_details
    SM_names = [x for x in molecules.keys()]
    SM_names.sort()
    # Loop Over all molecules
    pKa_dt_temp = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
    for names in SM_names:
        mol_details = molecules[names] # Get the state details for each molecule
        form_charge = []
        for items in mol_details:
            form_charge.append(items[2])
        formal_charge = form_charge
        formal_charge = np.unique(formal_charge)
        form_charge.append(0)
        form_charge = np.unique(form_charge)
        charge_dist_df = pd.DataFrame(columns = ["pH","pop_charge","formal_charge"])
        for charges in form_charge:
            for pH in pH_vals:
                n_frac,microstates = pop_charge_microstates(pH,charges,mol_details)
                charge_dist_df = charge_dist_df.append({"pH":pH,"pop_charge":pop_charge(pH,charges,mol_details),"formal_charge":charges},ignore_index = True)
        # Experimental Macro pKas
        exp_pKas = experimental_data.loc[experimental_data.index==names.split('_')[0],'pKa mean'].values
        # Macrostate Calculation and Absolute Error Computation
        temp_df2 = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
        for first,second in zip(form_charge,form_charge[1:]):
            idx = np.argwhere(np.diff(np.sign(charge_dist_df.loc[charge_dist_df.loc[:,'formal_charge']==first,'pop_charge'].values - charge_dist_df.loc[charge_dist_df.loc[:,'formal_charge']==second,'pop_charge'].values))).flatten()
            pred_pKa = charge_dist_df.loc[charge_dist_df.loc[:,'formal_charge']==first,'pH'].values[idx]
            # Formal Charge Assignment
            if first==2 and second==3:
                formal_charge_val=3
            elif first==1 and second==2:
                formal_charge_val=2
            elif first== 0 and second==1:
                formal_charge_val=1
            elif first==-1 and second==0:
                formal_charge_val=-1
            elif first==-2 and second==-1:
                formal_charge_val=-2
            elif first==-3 and second==-2:
                formal_charge_val=-3
            for exp_pKa in exp_pKas:
                abs_error = np.abs(pred_pKa-exp_pKa)
                temp_df3 = pd.DataFrame({'Submission':submission.file_name,'Method Name':submission.method_name,'Method Type':submission.category,'Molecule ID':names.split('_')[0],'Formal Charge':formal_charge_val,'Predicted pKa':pred_pKa,'Experimental pKa':exp_pKa,'Absolute Error':abs_error})
                temp_df2 = pd.concat([temp_df2,temp_df3],ignore_index=True)
        pKa_dt_temp = pd.concat([pKa_dt_temp,temp_df2],ignore_index=True)
    pKa_dt = pd.concat([pKa_dt,pKa_dt_temp],ignore_index=True)

# =============================================================================
# Estimating most popular transitions for each pKa
# =============================================================================

# Most frequently occurring transition state per experimental macro-pKa across all submissions
# If there are molecules where there are more than one popular transition were dropped from the analysis
popular_transitions = pd.DataFrame(columns=["Molecule ID","Experimental pKa","Formal Charge"])
for idx,row in experimental_data.iterrows():
    formal_charges_withID = pKa_dt.loc[pKa_dt.loc[:,'Experimental pKa']==row['pKa mean'],["Molecule ID","Formal Charge"]]#Get all formal Charges with Mol ID
    formal_charges1 = formal_charges_withID.loc[formal_charges_withID.loc[:,"Molecule ID"]==idx,"Formal Charge"]
    df_temp = pd.DataFrame({"Molecule ID":idx,"Experimental pKa":row['pKa mean'],"Formal Charge":formal_charges1.mode()})
    popular_transitions = pd.concat([popular_transitions,df_temp],ignore_index=True)
popular_transitions = popular_transitions.drop_duplicates(subset=['Molecule ID','Experimental pKa'],keep=False)


# Selects the most popular transition for each pKa per molecule per submission based on the selected transitions from above
pKa_dt_pop_transition_states = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
for submission in microstate_dt:
    submission_data = pKa_dt.loc[pKa_dt.loc[:,'Submission']==submission.file_name,] #Slice off data for that particular submission
    for idx,row in experimental_data.iterrows():
        if idx in popular_transitions.loc[:,"Molecule ID"].tolist():
            popular_transitions_mol = popular_transitions.loc[(popular_transitions.loc[:,'Experimental pKa']==row['pKa mean']) & (popular_transitions.loc[:,"Molecule ID"]==idx),]
            if row['pKa mean'] in submission_data.loc[:,"Experimental pKa"].tolist() and idx in submission_data.loc[:,"Molecule ID"].tolist():
                df_temp1 = submission_data.loc[(submission_data.loc[:,'Experimental pKa']==row['pKa mean']) & (submission_data.loc[:,"Molecule ID"]==idx),]
                df_temp2 = df_temp1.loc[df_temp1.loc[:,'Formal Charge']==popular_transitions_mol.loc[:,"Formal Charge"].values.item(),]
                pKa_dt_pop_transition_states = pd.concat([pKa_dt_pop_transition_states,df_temp2],ignore_index=True)

# Plot Absolute errors
plt.figure(figsize=(15,10))
with sns.axes_style("darkgrid"):
    sns.barplot(x='Method Name',y='Absolute Error',hue="Method Type",palette="Set1",data=pKa_dt_pop_transition_states,dodge=False)
    plt.xlabel("Method", fontsize=14)
    plt.ylabel("Absolute Error", fontsize=14)
    plt.title("Absolute Error based on method",fontsize=16)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.xticks(rotation=90)
plt.savefig("./Performance_stats_plots"+"/"+"abs_error_bymethod_plot"+".pdf")

plt.figure(figsize=(15,10))
sns.set_theme()
sns.barplot(x='Molecule ID',y='Absolute Error',data=pKa_dt_pop_transition_states,dodge=False)
plt.xlabel("Method", fontsize=14)
plt.ylabel("Absolute Error", fontsize=14)
plt.title("Absolute Error for each Molecule",fontsize=16)
plt.gcf().subplots_adjust(bottom=0.25)
plt.xticks(rotation=90)
plt.savefig("./Performance_stats_plots"+"/"+"abs_error_bymol_plot"+".pdf")
# =============================================================================
# Calculating Performance Statistics across all molecules per submission
# =============================================================================
submission_names = []
for submission in microstate_dt:
    submission_names.append(submission.file_name)

perform_stats_submissions = pd.DataFrame(columns=["Submission","R-squared","Slope","Kendall Tau"])
for submission_name in submission_names:
    submission_dt = pKa_dt_pop_transition_states.loc[pKa_dt_pop_transition_states.loc[:,'Submission']==submission_name,["Experimental pKa","Predicted pKa"]]
    slope, intercept, r_value, p_value, stderr = scipy.stats.linregress(submission_dt.loc[:,"Experimental pKa"], submission_dt.loc[:,"Predicted pKa"])
    correlation, p_value = scipy.stats.kendalltau(submission_dt.loc[:,"Experimental pKa"],submission_dt.loc[:,"Predicted pKa"])
    df_temp = pd.DataFrame({"Submission":submission_name,"R-squared":[r_value],"Slope":[slope],"Kendall Tau":[correlation]})
    perform_stats_submissions = pd.concat([perform_stats_submissions,df_temp],ignore_index=True)
    fig =  sns.jointplot(submission_dt.loc[:,"Experimental pKa"],submission_dt.loc[:,"Predicted pKa"],kind="reg")
    text_str = '\n'.join((
        r'$\bf{%s}$' % (submission_name,),
        r'$R^{2}=%.2f$' % (r_value,),
        r'$Slope=%.2f$' % (slope,),
        r'$Kendall \tau = %.2f$' % (correlation,)))
    props = dict(boxstyle='round', alpha=0.5)
    fig.ax_joint.annotate(text_str, xy = (0.65,0.75), xycoords='axes fraction',bbox=props)
    plt.savefig("./Performance_stats_plots"+"/"+submission_name+"_Corr_plot"+".pdf")
perform_stats_submissions.to_csv("./Performance_stats_plots"+"/"+"performance_stats_submissions.csv")
# =============================================================================
# Calculating Performance Statistics for each molecule across all submissions
# =============================================================================

perform_stats_mols = pd.DataFrame(columns=["Molecule ID","Mean Error","Mean Absolute Error", "Root Mean Squared Error"])
for mol_names in popular_transitions.loc[:,"Molecule ID"].unique():
    mol_dt = pKa_dt_pop_transition_states.loc[pKa_dt_pop_transition_states.loc[:,"Molecule ID"]==mol_names,]
    error = np.array(mol_dt.loc[:,'Predicted pKa'])-np.array(mol_dt.loc[:,'Experimental pKa'])
    me = error.mean()
    mae = np.array(mol_dt.loc[:,"Absolute Error"]).mean()
    rmse = np.sqrt(error**2).mean()
    df_temp = pd.DataFrame({"Molecule ID": mol_names,"Mean Error":[me],"Mean Absolute Error":[mae],"Root Mean Squared Error":[rmse]})
    perform_stats_mols = pd.concat([perform_stats_mols,df_temp],ignore_index=True)
perform_stats_mols.to_csv("./Performance_stats_plots"+"/"+"performance_stats_mol.csv")

plt.figure(figsize=(15,10))
sns.barplot(x="Molecule ID",y="Root Mean Squared Error",data=perform_stats_mols)
plt.xlabel("Molecule ID",fontsize=14)
plt.ylabel("RMSE",fontsize=14)
plt.title("RMSE across all Molecules",fontsize=16)
plt.xticks(rotation=90)
plt.savefig("./Performance_stats_plots"+"/"+"rmse_plot"+".pdf")

plt.figure(figsize=(15,10))
sns.barplot(x="Molecule ID",y="Mean Error",data=perform_stats_mols)
plt.xlabel("Molecule ID",fontsize=14)
plt.ylabel("Mean Error",fontsize=14)
plt.title("Mean Error across all Molecules",fontsize=16)
plt.xticks(rotation=90)
plt.savefig("./Performance_stats_plots"+"/"+"mean_error_plot"+".pdf")

plt.figure(figsize=(15,10))
sns.barplot(x="Molecule ID",y="Mean Absolute Error",data=perform_stats_mols)
plt.xlabel("Molecule ID",fontsize=14)
plt.ylabel("Mean Absolute Error",fontsize=14)
plt.title("Mean Absolute Error across all Molecules",fontsize=16)
plt.xticks(rotation=90)
plt.savefig("./Performance_stats_plots"+"/"+"mean_abs_error_plot"+".pdf")