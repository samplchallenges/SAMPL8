# Functions for logD Analysis

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import io
import scipy

# =============================================================================
# Construct Dataframe with experimental and Predicted Values from submission class objects
# =============================================================================
def getlogDdataframe(logD_submissions,experimental_data,output_directory):
    """This function creates a dataframe of all logD Combinations across all submissions, 
    returns a dataframe that contains data from all the submissions first and then another
    that contains data from submissions that predictions for all solvent combinations"""
    logD_dt = pd.DataFrame(columns=['Molecule ID','Solvent-Combo','Method Name','Method Category','File Name','Predicted logD','Experimental logD','Absolute Error']) # Dataframe that contains all of the logD data from across all submissions
    logD_dt_all_combos = pd.DataFrame(columns=['Molecule ID','Solvent-Combo','Method Name','Method Category','File Name','Predicted logD','Experimental logD','Absolute Error']) # Dataframe that contains logD data from submissions that contain predictions for all 7 solvent combinations
    for submission in logD_submissions:
        submission_data = submission.data # This is a dictionary
        logD_all_combos_temp = pd.DataFrame() # This is a temporary dataframe that will contain all logD values for a single submission
        for key in submission_data.keys():
            temp_df = submission_data[key]
            temp_df = temp_df.drop(['ID tag','logD SEM','logD model uncertainty'],axis=1)
            temp_df['Molecule ID'] = temp_df.index
            solvent_combo = [' '.join(key.split(' ')[:-1])]*len(temp_df)
            temp_df['Solvent-Combo'] = solvent_combo # Adds the solvent combo listing
            logD_all_combos_temp = pd.concat([logD_all_combos_temp,temp_df],ignore_index=True)
        logD_all_combos_temp['Method Name'] = [submission.method_name]*len(logD_all_combos_temp)
        logD_all_combos_temp['Method Type'] = [submission.category]*len(logD_all_combos_temp)
        logD_all_combos_temp['File Name'] = [submission.file_name]*len(logD_all_combos_temp)

        ## Add experimental Data
        logD_all_combos =  pd.DataFrame(columns=['Molecule ID','Solvent-Combo','Method Name','Method Category','File Name','Predicted logD','Experimental logD','Absolute Error'])
        for idx,row in logD_all_combos_temp.iterrows():
            exp_logD = experimental_data.loc[(experimental_data.loc[:,'Molecule ID']==row['Molecule ID'])&(experimental_data.loc[:,'Solvent-Combo']==row["Solvent-Combo"]),"logD"].values
            abs_error = abs(row['logD mean']-exp_logD)
            temp_df2 = pd.DataFrame({"Molecule ID":row['Molecule ID'],
                                     "Solvent-Combo":row["Solvent-Combo"],
                                     "Method Name":row["Method Name"],
                                     "Method Category":row["Method Type"],
                                    "File Name":row["File Name"],
                                     "Predicted logD":row["logD mean"],
                                     "Experimental logD":exp_logD,
                                    "Absolute Error":abs_error})
            logD_all_combos = pd.concat([temp_df2,logD_all_combos],ignore_index=True) # This contains all data associated with a single submission
        ## Concatenating all submissions together into a single Data Frame
        logD_dt = pd.concat([logD_all_combos,logD_dt],ignore_index=True)
        if len(set(submission_data.keys()))==7: # Only concat data from submissions that contains predictions for all 7 solvent combinations
            logD_dt_all_combos = pd.concat([logD_all_combos,logD_dt_all_combos],ignore_index=True)
        logD_dt.to_csv(output_directory+"logD_dataset.csv")
        logD_dt_all_combos.to_csv(output_directory+"logD_all_combos_dataset.csv")
    return logD_dt,logD_dt_all_combos

# =============================================================================
# Performance Statistics by Submission
# =============================================================================
def getperformancestatsbysubmission(dataset,output_directory):
    """This function is mainly intended for submissions that contain predictions 
    for all solvent combinations"""
    corr_stats_df_by_submission = pd.DataFrame(columns=['Submission','R-squared','Slope','Kendall Tau'])
    for names in dataset.loc[:,'File Name'].unique():
        submission_data = dataset.loc[dataset.loc[:,'File Name']==names,] # Slice dataframe that contains data associated with a specified submission name

        ## Correlation Performance Statistics for each Submission
        slope,intercept,r_value,p_value,stderr = scipy.stats.linregress(submission_data.loc[:,"Experimental logD"],submission_data.loc[:,"Predicted logD"]) 
        correlation, p_value = scipy.stats.kendalltau(submission_data.loc[:,"Experimental logD"],submission_data.loc[:,"Predicted logD"])
        corr_df_temp = pd.DataFrame({"Submission":names,"R-squared":[r_value],"Slope":[slope],"Kendall Tau":[correlation]})
        corr_stats_df_by_submission = pd.concat([corr_df_temp,corr_stats_df_by_submission],ignore_index=True)

        # Correlation Plots
        sns.set_theme()
        join_plot =  sns.jointplot(submission_data.loc[:,"Experimental logD"],submission_data.loc[:,"Predicted logD"],kind="reg")

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

        ## Adding Textbox containing performance statistics
        text_str = '\n'.join((
            r'$R^{2}=%.2f$' % (r_value,),
            r'$Slope=%.2f$' % (slope,),
            r'$Kendall \tau = %.2f$' % (correlation,)))
        props = dict(boxstyle='round', alpha=0.5)
        join_plot.ax_joint.annotate(text_str, xy = (0.65,0.05), xycoords='axes fraction',bbox=props)


        ## Modifying Plot
        join_plot.fig.suptitle(names)
        join_plot.fig.tight_layout()
        join_plot.fig.subplots_adjust(top=0.95)

        ## Saving Plot to appropriate folder
        corr_plots_dir = output_directory+"Performance_stats_by_submission/"+"Corr_plots/"
        if not os.path.exists(corr_plots_dir):
            os.makedirs(corr_plots_dir)
        join_plot.savefig(corr_plots_dir+names+"_Corr_plot"+".pdf")
        plt.close()
        corr_stats_df_by_submission.to_csv(corr_plots_dir+"corr_stats_all_combos"+".csv")
    
    # Absolute Error Plots by Method and hued by method category
    plt.figure(figsize=(15,10))
    sns.set_theme()
    sns.barplot(x='Method Name',y='Absolute Error', hue = 'Method Category',palette="Set1",data = dataset,dodge=False)
    plt.xlabel("Method",fontsize = 16)
    plt.ylabel("Absolute Error",fontsize = 16)
    plt.title("Absolute Error Plot based on Method-All Solvent Combinations",fontsize=18)
    plt.legend(loc="best")
    plt.gcf().subplots_adjust(bottom=0.35)
    plt.xticks(rotation=90)
    error_plots_dir = output_directory+"Performance_stats_by_submission/"+"Error_plots/"
    if not os.path.exists(error_plots_dir):
        os.makedirs(error_plots_dir)
    plt.savefig(error_plots_dir+"Absolute_Errors_all_combo_by_method"+".pdf")
    
    # Absolute error plot for all solvent combinations
    plt.figure(figsize=(15,10))
    sns.set_theme()
    sns.barplot(x='Solvent-Combo',y='Absolute Error',palette = 'husl',data = dataset,dodge=False)
    plt.xlabel("Solvent Combinations",fontsize = 16)
    plt.ylabel("Absolute Error",fontsize = 16)
    plt.title("Absolute Error Plot based on Solvent Combinations",fontsize=18)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.xticks(rotation=90)
    plt.savefig(error_plots_dir+"Absolute_error_all_combo_by_solvent_combo"+".pdf")
    
    return corr_stats_df_by_submission

# =============================================================================
# Performance Statistics by Solvent Combination
# =============================================================================

def getperformancestatsbysolventcombo(data,output_directory):
    """This function estimates performance statistics for all submissions
    (That may contain predictions for all or few solvent combinations),
    it groups the plots by solvent combination"""
    
    error_stats_dt = pd.DataFrame(columns=['Solvent-Combo','Molecule ID','Mean Error','Mean Absolute Error','Root Mean Squared Error'])
    
    error_plots_dir = output_directory+"Performance_stats_by_solvent_combo/"+"Error_plots/"
    if not os.path.exists(error_plots_dir):
        os.makedirs(error_plots_dir)
        
        
    for sol_combo in data.loc[:,'Solvent-Combo'].unique():
        sol_combo_dt = data.loc[data.loc[:,'Solvent-Combo']==sol_combo,] # Slice of data containing each solvent combination
        
        # Generate Absolute Error Plots for each solvent Combination
        plt.figure(figsize=(15,10))
        sns.set_theme()
        sns.barplot(x='Method Name',y='Absolute Error', hue = 'Method Category',palette="Set1",data = sol_combo_dt,dodge=False)
        plt.xlabel("Method",fontsize = 16)
        plt.ylabel("Absolute Error",fontsize = 16)
        plt.title("Absolute Error Plot for "+sol_combo,fontsize=18)
        plt.legend(loc="upper right")
        plt.gcf().subplots_adjust(bottom=0.35)
        plt.xticks(rotation=90)
        plt.savefig(error_plots_dir+"Absolute_Errors_" +sol_combo+".pdf")
        plt.close()

        for mol_name in sol_combo_dt.loc[:,'Molecule ID'].unique(): # Iterate through molecules in for that solvent combination
            sol_combo_mol_dt = sol_combo_dt.loc[sol_combo_dt.loc[:,'Molecule ID']==mol_name,] # Slice of data for that specific compound
            error = sol_combo_mol_dt.loc[:,'Predicted logD'].values-sol_combo_mol_dt.loc[:,'Experimental logD'].values
            me = error.mean()
            mae = sol_combo_mol_dt.loc[:,'Absolute Error'].values.mean()
            rmse = np.sqrt(error**2).mean()
            error_stats_dt_temp = pd.DataFrame({"Solvent-Combo":sol_combo,"Molecule ID":mol_name,"Mean Error":[me],"Mean Absolute Error":[mae],"Root Mean Squared Error":[rmse]})
            error_stats_dt = pd.concat([error_stats_dt_temp,error_stats_dt],ignore_index=True) # Generates Error Statistics per solvent-combo per compound
    error_stats_dt.to_csv(error_plots_dir+"error_stats_all_by_sols"+".csv")
    
    for sol_combo in error_stats_dt.loc[:,'Solvent-Combo'].unique():
        sol_combo_error_dt = error_stats_dt.loc[error_stats_dt.loc[:,'Solvent-Combo']==sol_combo,]

        # Mean Error Plot
        plt.figure(figsize=(15,10))
        sns.set_theme()
        sns.barplot(x='Molecule ID',y='Mean Error',palette = 'husl',data = sol_combo_error_dt,dodge=False)
        plt.xlabel("Molecule ID",fontsize = 16)
        plt.ylabel("Mean Error",fontsize = 16)
        plt.title("Mean Error Plot for "+sol_combo,fontsize=18)
        plt.gcf().subplots_adjust(bottom=0.35)
        plt.xticks(rotation=90)
        ## Create a new directory and save the plots
        mean_error_plots_dir = error_plots_dir+"Performance_stats_by_sol_combo/"+"/Mean_Error_plots/"
        if not os.path.exists(mean_error_plots_dir):
            os.makedirs(mean_error_plots_dir)
        plt.savefig(mean_error_plots_dir+"Mean_error_"+sol_combo+".pdf")
        plt.close()

        # RMSE Error Plots
        plt.figure(figsize=(15,10))
        sns.set_theme()
        sns.barplot(x='Molecule ID',y='Root Mean Squared Error',palette = 'husl',data = sol_combo_error_dt,dodge=False)
        plt.xlabel("Molecule ID",fontsize = 16)
        plt.ylabel("Root Mean Squared Error",fontsize = 16)
        plt.title(" Root Mean Squared Error Plot for "+sol_combo,fontsize=18)
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.xticks(rotation=90)
        ## Create a new directory and save the plots
        rmse_plots_dir = error_plots_dir+"Performance_stats_by_sol_combo/"+"/RMS_Error_plots/"
        if not os.path.exists(rmse_plots_dir):
            os.makedirs(rmse_plots_dir)
        plt.savefig(rmse_plots_dir+"rmse_"+sol_combo+".pdf")
        plt.close()

        # Mean Absolute Error Plots
        plt.figure(figsize=(15,10))
        sns.set_theme()
        sns.barplot(x='Molecule ID',y='Mean Absolute Error',palette = 'husl',data = sol_combo_error_dt,dodge=False)
        plt.xlabel("Molecule ID",fontsize = 16)
        plt.ylabel("Mean Absolute Error",fontsize = 16)
        plt.title(" Mean Absolute Error Plot for "+sol_combo,fontsize=18)
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.xticks(rotation=90)
        ## Create a new directory and save the plots
        mae_plots_dir = error_plots_dir+"Performance_stats_by_sol_combo/"+"/MA_Error_plots/"
        if not os.path.exists(mae_plots_dir):
            os.makedirs(mae_plots_dir)
        plt.savefig(mae_plots_dir+"mae_"+sol_combo+".pdf")
        plt.close()
    return error_stats_dt
    