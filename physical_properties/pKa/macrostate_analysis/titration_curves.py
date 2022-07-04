# Titration Curve Generation
# =============================================================================
# =============================================================================
# =============================================================================


# =============================================================================
# GLOBAL IMPORTS
# =============================================================================
import os
import glob
import io
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# CONSTANTS
# =============================================================================
pKa_SUBMISSIONS_DIR_PATH = '../submissions'
EXPERIMENTAL_DATA_FILE_PATH = '../experimental_pKas.csv'
USER_MAP_FILE_PATH = '../SAMPL8-pKa-user-map.csv'
if not os.path.exists("./titration_curve_plots"):
    os.makedirs("./titration_curve_plots")
# =============================================================================
# Utility Classes
# =============================================================================

class IgnoredSubmissionError(Exception):
    """Exception used to signal a submission that must be ignored."""
    pass


class BadFormatError(Exception):
    """Exception used to signal a submission with unexpected formatting."""
    pass

class SamplSubmission:
    """A generic SAMPL submission.
    Parameters
    ----------
    file_path : str
        The path to the submission file.
    Raises
    ------
    IgnoredSubmission
        If the submission ID is among the ignored submissions.
    """
    # Section of the submission file.
    SECTIONS = {}

    # Sections in CSV format with columns names.
    CSV_SECTIONS = {}

    def __init__(self, file_path, user_map):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_data = file_name.split('-')

        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        self.data = sections['Predictions']  # This is a list
        self.data = pd.DataFrame(data=self.data) # Now a DataFrame
        self.file_name = file_name
        self.method_name = sections['Name'][0]

        # Check if this is a reference submission
        self.reference_submission = False

        if "REF" in self.method_name or "NULL" in self.method_name:
            print("REF found: ", self.method_name)
            self.reference_submission = True
        #print(self.data)


    @classmethod
    def _read_lines(cls, file_path):
        """Generator to read the file and discard blank lines and comments."""
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                # Strip whitespaces.
                line = line.strip()
                # Don't return blank lines and comments.
                if line != '' and line[0] != '#':
                    yield line

    @classmethod
    def _load_sections(cls, file_path):
        """Load the data in the file and separate it by sections."""
        #print("file_path",file_path)
        sections = {}
        current_section = None
        for line in cls._read_lines(file_path):
            # Check if this is a new section.
            if line[:-1] in cls.SECTIONS:
                current_section = line[:-1]
            else:
                if current_section is None:
                    import pdb
                    pdb.set_trace()
                try:
                    sections[current_section].append(line)
                except KeyError:
                    sections[current_section] = [line]

        # Check that all the sections have been loaded.
        found_sections = set(sections.keys())
        if found_sections != cls.SECTIONS:
            raise BadFormatError('Missing sections: {}.'.format(found_sections - cls.SECTIONS))

        # Create a Pandas dataframe from the CSV format.
        for section_name in cls.CSV_SECTIONS:
            csv_str = io.StringIO('\n'.join(sections[section_name]))
            columns = cls.CSV_SECTIONS[section_name]
            id_column = columns[0]
            #print("trying", sections)
            section = pd.read_csv(csv_str, index_col=id_column, names=columns, skipinitialspace=True)
            #section = pd.read_csv(csv_str, names=columns, skipinitialspace=True)
            sections[section_name] = section
        return sections

    @classmethod
    def _create_comparison_dataframe(cls, column_name, submission_data, experimental_data):
        """Create a single dataframe with submission and experimental data."""
        # Filter only the systems IDs in this submissions.


        experimental_data = experimental_data[experimental_data.index.isin(submission_data.index)] # match by column index
        # Fix the names of the columns for labelling.
        submission_series = submission_data[column_name]
        submission_series.name += ' (calc)'
        experimental_series = experimental_data[column_name]
        experimental_series.name += ' (expt)'

        # Concatenate the two columns into a single dataframe.
        return pd.concat([experimental_series, submission_series], axis=1)

    @classmethod
    def _create_single_dataframe(cls, column_name, submission_data):
        """Create a single dataframe with submission and experimental data."""
        # Filter only the systems IDs in this submissions.


        #experimental_data = experimental_data[experimental_data.index.isin(submission_data.index)] # match by column index
        # Fix the names of the columns for labelling.
        submission_series = submission_data[column_name]
        #submission_series.name += ' (calc)'
        #experimental_series = experimental_data[column_name]
        #experimental_series.name += ' (expt)'

        # Concatenate the two columns into a single dataframe.
        return pd.DataFrame(submission_series)#, axis=1) #pd.concat([submission_series], axis=1)


# =============================================================================
# pKa PREDICTION CHALLENGE
# =============================================================================

class pKaSubmission(SamplSubmission):
    """A submission for pKa challenge.
    Parameters
    ----------
    file_path : str
        The path to the submission file
    Raises
    ------
    IgnoredSubmission
        If the submission ID is among the ignored submissions.
    """

    # Section of the submission file.
    SECTIONS = {"Predictions",
                "Participant name",
                "Participant organization",
                "Name",
                "Compute time",
                "Computing and hardware",
                "Software",
                "Category",
                "Method",
                "Ranked"}

    # Sections in CSV format with columns names.
    #CSV_SECTIONS = {‘Predictions’: (“Molecule ID”, “pKa mean”, “pKa SEM”, “pKa model uncertainty”)}
    CSV_SECTIONS = {"Predictions": ("Molecule ID",
                                    "ID tag",
                                    "total charge",
                                    "pKa mean",
                                    "pKa SEM",
                                    "pKa model uncertainty")}


    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        print("file_name: \n", file_name)
        file_data = file_name.split('-')

        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        self.data = sections['Predictions']  # This is a pandas DataFrame.
        self.method_name = sections['Name'][0]
        self.category = sections['Category'][0]
        self.participant = sections['Participant name'][0].strip()
        self.organization = sections['Participant organization'][0].strip()
        self.ranked = sections['Ranked'][0].strip() =='True'




def load_submissions(directory_path, user_map):
    """Load submissions from a specified directory using a specified user map,
    correct unit and sign errors in submissions, and convert relative free energy
    calculations to macro pKa predictions.
    Returns: submissions (where each prediction is a macro pKa)
    """
    submissions = []
    for file_path in glob.glob(os.path.join(directory_path, '*.csv')):
        try:
            submission = pKaSubmission(file_path, user_map)
            print(submission)

        except IgnoredSubmissionError:
            continue
        submissions.append(submission)

    return submissions

# =============================================================================
# Load data from submissions and Experimental Data
# =============================================================================

microstates_df = load_submissions(pKa_SUBMISSIONS_DIR_PATH,USER_MAP_FILE_PATH)

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
# Relative Free Energy and Charged Population Fraction Calculations
# =============================================================================

# Define Constants
kB = 1.381 * 6.02214 / 1000.0 # Converts Boltzmann constant to kJ/mol*K
beta = (1 / ((kB/4.184) * 300)) # Convert to kcal
C_unit = (1 /beta)*np.log(10)# C_unit = RT*ln10 from Gunner et. al
pH_vals = np.arange(-15,22,0.1) # pH values for estimating all macro-pKa's from submissions

# Compute free energy as a function of pH for states
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

# Compute populations for mscrostates
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

# Compute populations for individual microstates
def pop_charge_microstates(pH, formal_charge, state_details):
    free_energies = []
    microstates = []
    for item in state_details:
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

# Construct Experimental and Predicted Data Frame
# Loops over Experimental and Predicted pKa values to construct a data frame that contains all possible combinations of predicted and experimental pKa's
pKa_dt = pd.DataFrame(columns=['Submission','Method Name','Method Type','Molecule ID','Formal Charge','Predicted pKa','Experimental pKa','Absolute Error'])
for submission in microstates_df:
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
        charge_dist_df_microstate = pd.DataFrame(columns = ["pH","pop_charge","formal_charge"])
        for charges in form_charge:
            for pH in pH_vals:
                n_frac,microstates = pop_charge_microstates(pH,charges,mol_details)
                pH_microstates = np.tile(pH,(len(microstates),))
                temp_df = pd.DataFrame({"pH":pH_microstates,
                                        "pop_charge":n_frac,
                                        "formal_charge":microstates})
                charge_dist_df = charge_dist_df.append({"pH":pH,"pop_charge":pop_charge(pH,charges,mol_details),"formal_charge":charges},ignore_index = True)
                charge_dist_df_microstate = pd.concat([charge_dist_df_microstate,temp_df],ignore_index=True)
        charge_dist_df_microstate["formal_charge"] = charge_dist_df_microstate["formal_charge"].astype("category")
        # Slice DataFrame for Plotting Titration Curves
        plotting_dt_formal_charge = charge_dist_df.loc[charge_dist_df['pH'].between(0,15,inclusive=True),] # Only formal charges
        plotting_dt_microstates = charge_dist_df_microstate.loc[charge_dist_df_microstate['pH'].between(0,15,inclusive=True),] # Microstates
        # Graphical Options for Figure
        fig_name = submission.file_name+":"+names.split('_')[0]
        plt.figure(figsize=(10,6))
        sns.lineplot(data=plotting_dt_formal_charge,x="pH",y="pop_charge",hue="formal_charge")
        sns.lineplot(data=plotting_dt_microstates,x="pH",y="pop_charge",hue="formal_charge",linestyle="--",palette="husl")
        plt.xticks(np.arange(0,14,1).tolist())
        plt.ylabel("population fraction", fontsize = 14)
        plt.xlabel("pH",fontsize=14)
        plt.title(fig_name,fontsize = 18)
        lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),fancybox=True, shadow=True, ncol=4,prop={'size': 12})
        plt.savefig("./titration_curve_plots"+"/"+fig_name+".pdf",bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.close('all')
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

# Write dataframe to csv file
# Located in the same folder as the titration curves
pKa_dt.to_csv("./titration_curve_plots"+"/"+"macro_pKas_data.csv")