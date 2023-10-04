# Functions for pKa macrostate Analysis
# # Analysis follows similar setup to "titrations.py"

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle
import scipy
from operator import add
from collections import Counter
import glob
import io

# Macrostate Calculation Functions-
kB = 1.381 * 6.02214 / 1000.0 # Converts Boltzmann constant to kJ/mol*K
beta = (1 / ((kB/4.184) * 300)) # Convert to kcal
C_unit = (1 /beta)*np.log(10)# C_unit = RT*ln10 from Gunner et. al
pH_vals = np.arange(-15,22,0.1) # pH values

# Compute free energy as a function of pH for states
#WITHIN-charge transitions have same pH dependence
def DeltaG(pH, state,state_details):
    for item in state_details:
        if item[0]==state:
            # 0 serves as the reference state; all transitions are away from 0.
            if item[2]==-1:
                DeltaM=1
            elif item[2]==1:
                DeltaM=-1
            elif item[2]==2:
                DeltaM=-2
            elif item[2]==-2:
                DeltaM=2
            elif item[2]==0:
                DeltaM=0
            elif item[2]==3:
                DeltaM=-3
            elif item[2]==-3:
                DeltaM=3
            else:
                raise Exception("Issue with Formal Charges")
            # Compute value
            return (item[1]-pH*DeltaM*C_unit) # Gunner eq 3: This checks out since we are alloting -1 to 1 formal charge so the negative sign is justified

    # Returns the sum of all free energies associated with the microstates for that molecule
def total_pop_charge(pH,state_details):
    free_energies = []
    microstates = []
    for item in state_details:
        free_energies.append(-beta * DeltaG(pH, item[0], state_details))
        microstates.append(item[0])
    if not "micro000" in [m.split('_')[1] for m in microstates]:
        free_energies.append(0 * pH)
    total_sum = np.sum(np.exp(free_energies))
    return total_sum


    # Compute populations for charge states-Cumulative formal charges
def pop_charge(pH, formal_charge, state_details):
    free_energies = []
    microstates = []
    for item in state_details: #state_details [('SM42_micro001', 0.5304000000000001, -1, 0.0, 1.3872000000000002)
        microstates.append(item[0])
        if item[2] == formal_charge:
            free_energies.append(-beta * DeltaG(pH, item[0], state_details))
    if not "micro000" in [m.split('_')[1] for m in microstates] and formal_charge==0:
        free_energies.append(0 * pH)
    pop_charge_sum = total_pop_charge(pH,state_details)
    n_frac = (np.exp(free_energies))/(pop_charge_sum) # Use this when using Teilker's method
    return np.sum(n_frac) # Modified to sum fraction populations for selected microstates


    # Compute populations for charge states (without normalization, due to laziness/since it'll drop out)
def pop_charge_microstates(pH, formal_charge, state_details):
    free_energies = []
    microstates = []
    for item in state_details: #state_details [('SM42_micro001', 0.5304000000000001, -1, 0.0, 1.3872000000000002)
        if item[2] == formal_charge:
            free_energies.append(-beta * DeltaG(pH, item[0], state_details))
            microstates.append(item[0])
    if not "micro000" in [m.split('_')[1] for m in microstates] and formal_charge==0:
        free_energies.append(0 * pH)
        microstates.append("reference")
    elif "micro000" in [m.split('_')[1] for m in microstates] and formal_charge==0:
        microstates[[m.split('_')[1] for m in microstates].index("micro000")]="reference"
    # Total population Charge
    pop_charge_sum = total_pop_charge(pH,state_details)
    n_frac = (np.exp(free_energies))/(pop_charge_sum) # Use this when using Teilker's method
    return n_frac,microstates # returns a list of the microstate values

# =============================================================================
# Generate Dataset-Compute Predicted pKa values
# =============================================================================

def getdataset(submission_collection,experimental_data,output_directory):
    pKa_dt = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
    for submission in submission_collection:
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
            charge_dist_df = pd.DataFrame(columns = ["pH", "pop_charge", "formal_charge"])
            for charges in form_charge:
                for pH in pH_vals:
                    n_frac,microstates = pop_charge_microstates(pH,charges,mol_details)
                    pH_microstates = np.tile(pH,(len(microstates),))
                    temp_df = pd.DataFrame({"pH":pH_microstates,
                                            "pop_charge":n_frac,
                                            "formal_charge":microstates})
                    charge_dist_df = charge_dist_df.append({"pH":pH,"pop_charge":pop_charge(pH,charges,mol_details),"formal_charge":charges},ignore_index = True)
            # Experimental Macro pKas
            exp_pKas = experimental_data.loc[experimental_data.index==names.split('_')[0],'pKa mean'].values
            # Macrostate Calculation and Absolute Error Computation
            temp_df2 = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
            for first, second in zip(form_charge[1:], form_charge):  # This is just using th
                idx = np.argwhere(np.diff(np.sign(charge_dist_df.loc[charge_dist_df.loc[:, 'formal_charge'] == first, 'pop_charge'].values - charge_dist_df.loc[charge_dist_df.loc[:, 'formal_charge'] == second, 'pop_charge'].values))).flatten()
                pred_pKa = charge_dist_df.loc[charge_dist_df.loc[:, 'formal_charge'] == second, 'pH'].values[idx]
                # Formal Charge Assignment
                # This is based on the end transition state
                if first == 3 and second == 2:
                    formal_charge_val = 2
                elif first == 2 and second == 1:
                    formal_charge_val = 1
                elif first == 1 and second == 0:
                    formal_charge_val = 0
                elif first == 0 and second == -1:
                    formal_charge_val = -1
                elif first == -1 and second == -2:
                    formal_charge_val = -2
                elif first == -2 and second == -3:
                    formal_charge_val = -3
                for exp_pKa in exp_pKas:
                    abs_error = np.abs(pred_pKa-exp_pKa)
                    temp_df3 = pd.DataFrame({'Submission':submission.file_name,'Method Name':submission.method_name,'Method Type':submission.category,'Molecule ID':names.split('_')[0],'Formal Charge':formal_charge_val,'Predicted pKa':pred_pKa,'Experimental pKa':exp_pKa,'Absolute Error':abs_error})
                    temp_df2 = pd.concat([temp_df2,temp_df3],ignore_index=True)
            if temp_df2.empty:
                for exp_pKa in exp_pKas:
                    if 14-exp_pKa > abs(0-exp_pKa):
                        pred_pKa = 14
                    else:
                        pred_pKa = 0
                    abs_error = np.abs(pred_pKa-exp_pKa)
                    temp_df4 = pd.DataFrame({'Submission':submission.file_name,'Method Name':submission.method_name,'Method Type':submission.category,'Molecule ID':names.split('_')[0],'Formal Charge':formal_charge_val,'Predicted pKa':[pred_pKa],'Experimental pKa':exp_pKa,'Absolute Error':abs_error})
                    temp_df2 = pd.concat([temp_df2,temp_df4],ignore_index=True)         
            pKa_dt_temp = pd.concat([pKa_dt_temp,temp_df2],ignore_index=True)
        pKa_dt = pd.concat([pKa_dt,pKa_dt_temp],ignore_index=True)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        pKa_dt.to_csv(output_directory+"macrostate_pKa_data.csv")
    return pKa_dt



# =============================================================================
# Extract popular transition state predictions for each submission
# =============================================================================    

def getpopulartransitions(data, experimental_data):
    """Gets the most popular transitions states used for predictions across submissions and extracts these datapoints from the above generated dataset"""
    popular_transitions = pd.DataFrame(columns=["Molecule ID", "Experimental pKa", "Formal Charge"])
    for idx, row in experimental_data.iterrows():
        formal_charges_withID = data.loc[data.loc[:, 'Molecule ID'] == idx, ["Molecule ID", "Experimental pKa",
                                                                                 "Formal Charge"]]  # Get all formal Charges with Mol ID
        if len(list(formal_charges_withID["Experimental pKa"].drop_duplicates())) > 1:
            print(idx)
            formal_charge_feq = formal_charges_withID["Formal Charge"].value_counts().sort_values(ascending=False)[0:2]
            exp_pKa = list(formal_charges_withID["Experimental pKa"].drop_duplicates())
            # Add the acidic pKa to the popular Transitions Dataframe
            df_temp1 = pd.DataFrame(
                {"Molecule ID": idx, "Experimental pKa": min(exp_pKa), "Formal Charge": [max(formal_charge_feq.index)]})
            popular_transitions = pd.concat([popular_transitions, df_temp1], ignore_index=True)
            # Add the basic pKa to the popular Transitions Dataframe
            df_temp2 = pd.DataFrame(
                {"Molecule ID": idx, "Experimental pKa": max(exp_pKa), "Formal Charge": [min(formal_charge_feq.index)]})
            popular_transitions = pd.concat([popular_transitions, df_temp2], ignore_index=True)
        else:
            print(idx)
            df_temp = pd.DataFrame({"Molecule ID": idx, "Experimental pKa": row['pKa mean'],
                                    "Formal Charge": formal_charges_withID["Formal Charge"].mode()})
            popular_transitions = pd.concat([popular_transitions, df_temp], ignore_index=True)
        
        popular_transitions = popular_transitions.drop_duplicates(subset=['Molecule ID', 'Experimental pKa'])
    return popular_transitions


def getpopulartransitionsdata(popular_transitions, data, experimental_data, output_directory):
        pKa_dt_pop_transition_states = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
        for submission in data.loc[:,'Submission'].unique():
            submission_data = data.loc[data.loc[:,'Submission']==submission,] #Slice off data for that particular submission
            for idx,row in experimental_data.iterrows():
                if idx in popular_transitions.loc[:,"Molecule ID"].tolist():
                    popular_transitions_mol = popular_transitions.loc[(popular_transitions.loc[:,'Experimental pKa']==row['pKa mean']) & (popular_transitions.loc[:,"Molecule ID"]==idx),]
                    if row['pKa mean'] in submission_data.loc[:,"Experimental pKa"].tolist() and idx in submission_data.loc[:,"Molecule ID"].tolist():
                        df_temp1 = submission_data.loc[(submission_data.loc[:,'Experimental pKa']==row['pKa mean']) & (submission_data.loc[:,"Molecule ID"]==idx),]
                        # df_temp2 = df_temp1.loc[df_temp1.loc[:,'Formal Charge']==popular_transitions_mol.loc[:,"Formal Charge"].values.item(),]
                        if popular_transitions_mol.loc[:,"Formal Charge"].values.item() in df_temp1.loc[:,'Formal Charge'].tolist():
                            df_temp2 = df_temp1.loc[df_temp1.loc[:,'Formal Charge']==popular_transitions_mol.loc[:,"Formal Charge"].values.item(),]
                        else:
                            df_temp1 = df_temp1.reset_index()
                            df_temp1 = df_temp1.drop(['index'],axis=1)
                            df_temp2 = df_temp1.loc[0,].to_frame().T
                            df_temp2.loc[:,'Formal Charge'] = popular_transitions_mol.loc[:,"Formal Charge"].values.item()
                            if abs(df_temp2.loc[:,'Experimental pKa'].values-14) > abs(df_temp2.loc[:,'Experimental pKa'].values-0):
                                df_temp2.loc[:,'Predicted pKa'] = 14
                                df_temp2.loc[:,'Absolute Error'] = abs(df_temp2.loc[:,'Experimental pKa']-14)
                            else:
                                df_temp2.loc[:,'Predicted pKa']=0
                                df_temp2.loc[:,'Absolute Error'] = abs(df_temp2.loc[:,'Experimental pKa']-0)

                        pKa_dt_pop_transition_states = pd.concat([pKa_dt_pop_transition_states,df_temp2],ignore_index=True)



        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        pKa_dt_pop_transition_states.to_csv(output_directory+"popular_transitions_pKa_data.csv")
        plt.figure(figsize=(15,10))
        with sns.axes_style("darkgrid"):
            sns.barplot(x='Method Name',y='Absolute Error',hue="Method Type",palette="Set1",data=pKa_dt_pop_transition_states,dodge=False)
            plt.xlabel("Method", fontsize=14)
            plt.ylabel("Absolute Error", fontsize=14)
            plt.title("Absolute Error based on method",fontsize=16)
            plt.gcf().subplots_adjust(bottom=0.25)
            plt.xticks(rotation=90)
        plt.savefig(output_directory+"abs_error_bymethod_plot"+".pdf", bbox_inches="tight")

        plt.figure(figsize=(15,10))
        sns.barplot(x='Molecule ID',y='Absolute Error',data=pKa_dt_pop_transition_states,dodge=False)
        plt.xlabel("Method", fontsize=14)
        plt.ylabel("Absolute Error", fontsize=14)
        plt.title("Absolute Error for each Molecule",fontsize=16)
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.xticks(rotation=90)
        plt.savefig(output_directory+"abs_error_bymol_plot"+".pdf", bbox_inches="tight")
        return pKa_dt_pop_transition_states

# =============================================================================
# Correlation Statistics
# =============================================================================

def getpKaCorrelationstats(data,output_directory):
    """Uses data to compute correlation Statistics and Creates Correlation Plots"""
    perform_stats_submissions = pd.DataFrame(columns=["Submission","R-squared","Slope","Kendall Tau"])
    for submission_name in data.loc[:,'Submission'].unique():
        submission_dt = data.loc[data.loc[:,'Submission']==submission_name,]
        # Compute Correlation Statistics
        slope, intercept, r_value, p_value, stderr = scipy.stats.linregress(submission_dt.loc[:,"Experimental pKa"].astype(float),submission_dt.loc[:,"Predicted pKa"].astype(float))
        correlation, p_value = scipy.stats.kendalltau(submission_dt.loc[:,"Experimental pKa"],submission_dt.loc[:,"Predicted pKa"])
        df_temp = pd.DataFrame({"Submission":submission_name,"R-squared":[r_value],"Slope":[slope],"Kendall Tau":[correlation]})
        perform_stats_submissions = pd.concat([perform_stats_submissions,df_temp],ignore_index=True)

        # Correlation Plots
        sns.set_theme()
        join_plot =  sns.jointplot(x=submission_dt.loc[:,"Experimental pKa"].astype(float), y=submission_dt.loc[:,"Predicted pKa"].astype(float), kind="reg")

        ## Adding Diagonal line to plot with errors
        ### Find extreme values to make axes equal.
        x0, x1 = join_plot.ax_joint.get_xlim()
        y0, y1 = join_plot.ax_joint.get_ylim()
        lims = np.array([max(x0, y0), min(x1, y1)])

        ### Plot diagonal line
        ax = join_plot.ax_joint
        ax.plot(lims, lims, ls='--', c='black', alpha=0.8, lw=0.7)

        ### Add shaded area for 0.5-1 logD error.
        palette = sns.color_palette('BuGn_r')
        ax.fill_between(lims, lims - 0.5, lims + 0.5, alpha=0.2, color=palette[2])
        ax.fill_between(lims,lims - 1, lims + 1, alpha=0.2, color=palette[3])

        ## Create textbox with Correlation Statistics
        text_str = '\n'.join((
            r'$R^{2}=%.2f$' % (r_value,),
            r'$Slope=%.2f$' % (slope,),
            r'$Kendall \tau = %.2f$' % (correlation,)))
        props = dict(boxstyle='round', alpha=0.5)
        join_plot.ax_joint.annotate(text_str, xy = (0.05,0.8), xycoords='axes fraction',bbox=props)

        ## Modifying Plot
        join_plot.fig.suptitle(submission_name)
        join_plot.fig.tight_layout()
        join_plot.fig.subplots_adjust(top=0.95)
        
        Corr_plot_dir = output_directory+"Correlation_Plots/"
        if not os.path.exists(Corr_plot_dir):
            os.makedirs(Corr_plot_dir)
        plt.savefig(Corr_plot_dir+submission_name+"Corr_plot"+".pdf", bbox_inches="tight")
        plt.close()
        perform_stats_submissions.to_csv(Corr_plot_dir+"Correlation_statistics.csv")
        
    return perform_stats_submissions


# =============================================================================
# Error Statistics
# =============================================================================

def getpKaErrorstats(data,output_directory):
    """Computes Error Statistics and Creates a variety of Error plots"""
    perform_stats_mols = pd.DataFrame(columns=["Molecule ID","Mean Error","Mean Absolute Error", "Root Mean Squared Error"])
    for mol_names in data.loc[:,"Molecule ID"].unique():
        mol_dt = data.loc[data.loc[:,"Molecule ID"]==mol_names,]
        # Mean Error Calculation
        error = mol_dt.loc[:,'Predicted pKa'].astype(float)-mol_dt.loc[:,'Experimental pKa'].astype(float)
        me = error.mean()
        mae = np.array(mol_dt.loc[:,"Absolute Error"]).mean()
        rmse = np.sqrt(error**2).mean()
        df_temp = pd.DataFrame({"Molecule ID": mol_names,"Mean Error":[me],"Mean Absolute Error":[mae],"Root Mean Squared Error":[rmse]})
        perform_stats_mols = pd.concat([perform_stats_mols,df_temp],ignore_index=True)
        

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    perform_stats_mols.to_csv(output_directory+"Error_statistics.csv")

    plt.figure(figsize=(15,10))
    sns.barplot(x="Molecule ID",y="Root Mean Squared Error",data=perform_stats_mols)
    plt.xlabel("Molecule ID",fontsize=14)
    plt.ylabel("RMSE",fontsize=14)
    plt.title("RMSE across all Molecules",fontsize=16)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.savefig(output_directory+"rmse_plot"+".pdf", bbox_inches="tight")

    plt.figure(figsize=(15,10))
    sns.barplot(x="Molecule ID",y="Mean Error",data=perform_stats_mols)
    plt.xlabel("Molecule ID",fontsize=14)
    plt.ylabel("Mean Error",fontsize=14)
    plt.title("Mean Error across all Molecules",fontsize=16)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.savefig(output_directory+"mean_error_plot"+".pdf", bbox_inches="tight")

    plt.figure(figsize=(15,10))
    sns.barplot(x="Molecule ID",y="Mean Absolute Error",data=perform_stats_mols)
    plt.xlabel("Molecule ID",fontsize=14)
    plt.ylabel("Mean Absolute Error",fontsize=14)
    plt.title("Mean Absolute Error across all Molecules",fontsize=16)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.savefig(output_directory+"mean_abs_error_plot"+".pdf", bbox_inches="tight")
        

    return perform_stats_mols

    

    

