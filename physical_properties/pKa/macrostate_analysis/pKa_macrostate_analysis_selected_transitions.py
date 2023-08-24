# pKa Macrostate Analysis
# =============================================================================
# =============================================================================
# =============================================================================


# =============================================================================
# GLOBAL IMPORTS
# =============================================================================
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
from functions_pKa_macrostate_analysis import *

# =============================================================================
# CONSTANTS
# =============================================================================
pKa_SUBMISSIONS_DIR_PATH = '../submissions'
EXPERIMENTAL_DATA_FILE_PATH = '../experimental_pKas.csv'
USER_MAP_FILE_PATH = '../SAMPL8-pKa-user-map.csv'
SELECTED_TRANSITIONS_DATA_FILE = './selected_transitions.csv'
output_PATH_DIR = "selected_transitions_analysis/analysis_outputs_all/"
if not os.path.exists(output_PATH_DIR):
    os.makedirs(output_PATH_DIR)
output_PATH_DIR_ranked = "selected_transitions_analysis/analysis_outputs_ranked/"
if not os.path.exists(output_PATH_DIR_ranked):
    os.makedirs(output_PATH_DIR_ranked)

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
            section = pd.read_csv(csv_str, index_col=id_column, names=columns, skipinitialspace=True)
            sections[section_name] = section
        return sections


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

def load_ranked_submissions(directory_path, user_map):
    """
    Load submissions from a specified directory using a specified user map.
    Returns: submissions
    """
    submissions = []

    for file_path in glob.glob(os.path.join(directory_path, '*.csv')):
        try:
            submission = pKaSubmission(file_path, user_map)
        except IgnoredSubmissionError:
            continue
        # only continue if submission is ranked
        if not submission.ranked:
            continue
        if "REF" in submission.method_name or "NULL" in submission.method_name:
            continue

        submissions.append(submission)

    method_names = []
    for submission in submissions:
        method_names.append(submission.method_name)
    print("Ranked submissions: \n", method_names)

    return submissions

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    sns.set_style('whitegrid')
    sns.set_context('paper')
    
    # Load Unranked Submissions
    microstates_df = load_submissions(pKa_SUBMISSIONS_DIR_PATH,USER_MAP_FILE_PATH)
    # Load Ranked Submissions
    microstates_df_ranked = load_ranked_submissions(pKa_SUBMISSIONS_DIR_PATH,USER_MAP_FILE_PATH)

    # Load experimental data
    with open(EXPERIMENTAL_DATA_FILE_PATH, 'r') as f:
        # experimental_data = pd.read_json(f, orient='index')
        names = ('Molecule ID', 'pKa mean', 'pKa SEM')
        experimental_data = pd.read_csv(f, names=names, skiprows=1)
    #
    with open(SELECTED_TRANSITIONS_DATA_FILE, 'r') as f:
        names = ('Molecule ID', 'Experimental pKa', 'Formal Charge')
        selected_transitions = pd.read_csv(f, names=names, skiprows=1)

    # Convert numeric values to dtype float.
    for col in experimental_data.columns[1:7]:
        experimental_data[col] = pd.to_numeric(experimental_data[col], errors='coerce')

    experimental_data.set_index("Molecule ID", inplace=True)
    experimental_data["Molecule ID"] = experimental_data.index
    
    # All Submissions Analysis  
    pKa_dt = getdataset(microstates_df,experimental_data,output_PATH_DIR)
    
    ## Compute Selected Transition States across all submission in pKaCollection-
    
    popular_transitions_pKa_dt = getpopulartransitionsdata(selected_transitions,pKa_dt,experimental_data,output_PATH_DIR)
    
    ## Correlation Statistics
    Corr_stats = getpKaCorrelationstats(popular_transitions_pKa_dt,output_PATH_DIR)
    
    ## Error Statistics
    Error_stats = getpKaErrorstats(popular_transitions_pKa_dt,output_PATH_DIR)
    
    
    # Ranked Submissions Analysis
    pKa_dt_ranked = getdataset(microstates_df_ranked,experimental_data,output_PATH_DIR_ranked)
    
    ## Compute Selected Transition States across all ranked submissions
    popular_transitions_pKa_dt_ranked = getpopulartransitionsdata(selected_transitions,pKa_dt_ranked,experimental_data,output_PATH_DIR_ranked)
    
    ## Correlation Statistics for each submission
    Corr_stats_ranked = getpKaCorrelationstats(popular_transitions_pKa_dt_ranked,output_PATH_DIR_ranked)
    
    ## Error Statistics for each molecule 
    Error_stats_ranked = getpKaErrorstats(popular_transitions_pKa_dt_ranked,output_PATH_DIR_ranked)

    


