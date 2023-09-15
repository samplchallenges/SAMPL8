# logD Analysis
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
import os
import glob
import io
import scipy
from functions_analysis_logD import *

# =============================================================================
# CONSTANTS
# =============================================================================
submissions_dir = './Submissions_edited'
experimental_dir = '../SAMPL8-logD_experimental_values.csv'
user_map_dir = '../SAMPL8-logD_-user-map.csv'
output_dir_all = "./analysis_all/"
if not os.path.exists(output_dir_all):
    os.makedirs(output_dir_all)
output_dir_ranked = "./analysis_ranked/"
if not os.path.exists(output_dir_ranked):
    os.makedirs(output_dir_ranked)

# =============================================================================
# Utility Classes
# =============================================================================
# Utility Classes for Importing Data
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
    # The IDs of submissions used for reference calculations
    REF_SUBMISSIONS = ['REF0', 'NULL0']


    # Section of the submission file.
    SECTIONS = {}

    # Sections in CSV format with columns names.
    CSV_SECTIONS = {}

    def __init__(self, file_path, user_map):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_data = file_name.split('-')

        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        #print(sections)
        #self.data = sections['Predictions']  # This is a list
        #self.data = pd.DataFrame(data=self.data) # Now a DataFrame
        #self.name = sections['Name'][0] #want this to take the place of the 5 letter code
        self.file_name = file_name

        self.method_name = sections['Name'][0] #want this to take the place of the 5 letter code

        # Check if this is a reference submission
        self.reference_submission = False
        #if self.method_name in self.REF_SUBMISSIONS:
        if "REF" in self.method_name or "NULL" in self.method_name:
            print("REF found: ", self.method_name)
            self.reference_submission = True

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
        csv_sections_test = []
        for keys in found_sections:
            if keys.split(' ')[-1]=="predictions":
                csv_sections_test.append(keys)
        cls.CSV_SECTIONS = csv_sections_test # Only use the sections that have data
            
        # Create a Pandas dataframe from the CSV format.
        for section_name in cls.CSV_SECTIONS:
            csv_str = io.StringIO('\n'.join(sections[section_name]))
            columns = ("Molecule ID", "ID tag", "logD mean", "logD SEM", "logD model uncertainty")
            id_column = columns[0]
            section = pd.read_csv(csv_str, index_col=id_column, names=columns, skipinitialspace=True)
            sections[section_name] = section
        return sections

    
# =============================================================================
# logD PREDICTION CHALLENGE
# =============================================================================
class logDSubmission(SamplSubmission):
    """A submission for logD challenge.
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
    SECTIONS = {"Octanol-water predictions",
                "Cyclohexane-water predictions",
                "Ethyl acetate-water predictions",
                "Heptane-water predictions",
                "MEK-water predictions",
                "TBME-water predictions",
                "Cyclohexane-DMF predictions",
                "Participant name",
                "Participant organization",
                "Name",
                "Compute time",
                "Computing and hardware",
                "Software",
                "Category",
                "Method",
                "Ranked"}

    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_data = file_name.split('-')


        # Load predictions for all different solvent systems
        self.data = {}
        sections = self._load_sections(file_path)  # From parent-class.
        data_section_names = []
        for names in sections.keys():
            if names.split(' ')[-1]=="predictions":
                data_section_names.append(names)
        for data_sections in data_section_names:
            self.data[data_sections] = sections[data_sections]
        self.method_name = sections['Name'][0]
        self.category = sections['Category'][0] # New section for logD challenge.
        self.ranked = sections['Ranked'][0].strip() =='True'
        self.sections = sections


def load_submissions(directory_path, user_map):
    """Load submissions from a specified directory using a specified user map.
    Optional argument:
        ref_ids: List specifying submission IDs (alphanumeric, typically) of
        reference submissions which are to be ignored/analyzed separately.
    Returns: submissions
    """
    submissions = []
    for file_path in glob.glob(os.path.join(directory_path, '*.csv')):
        try:
            submission = logDSubmission(file_path, user_map)

        except IgnoredSubmissionError:
            continue
        submissions.append(submission)
    method_names = []
    for submission in submissions:
        method_names.append(submission.method_name)
    print("Ranked submissions: \n", method_names,len(method_names))
    return submissions


def load_ranked_submissions(directory_path, user_map):
    """
    Load submissions from a specified directory using a specified user map.
    Optional argument:
        ref_ids: List specifying submission IDs (alphanumeric, typically) of
        reference submissions which are to be ignored/analyzed separately.
    Returns: submissions
    """
    submissions = []

    for file_path in glob.glob(os.path.join(directory_path, '*.csv')):
        try:
            submission = logDSubmission(file_path, user_map)
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
    print("Ranked submissions: \n", method_names,len(method_names))

    return submissions

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    
    
    sns.set_style('whitegrid')
    sns.set_context('paper')
    
    # Read experimental data.
    with open(experimental_dir, 'r') as f:
        # experimental_data = pd.read_json(f, orient='index')
        names = ('Solvent-Combo', 'Molecule ID', 'logD')
        experimental_data = pd.read_csv(f, names=names, skiprows=1)

    experimental_data['logD'] = pd.to_numeric(experimental_data['logD'], errors='coerce')

    experimental_data.set_index("Solvent-Combo", inplace=True)
    experimental_data["Solvent-Combo"] = experimental_data.index
    
    
    # Analysis all submissions
    # Load Data from all Submissions
    logD_submissions = load_submissions(submissions_dir,user_map_dir)
    logD_dt_all,logD_dt_all_combo_all = getlogDdataframe(logD_submissions,experimental_data,output_dir_all)
    # Performance Statistics from across all submissions that contain predictions for all solvent combinations
    perform_stats_bysubmission = getperformancestatsbysubmission(logD_dt_all_combo_all,output_dir_all)
    # Performance Statistics by solvent Combination across all submissions
    perform_stats_by_solvent_comb_all = getperformancestatsbysolventcombo(logD_dt_all,output_dir_all)
    
    # Analysis ranked submissions
    # Load Data from all ranked submissions
    logD_submissions_ranked = load_ranked_submissions(submissions_dir,user_map_dir)
    logD_dt_ranked,logD_dt_ranked_combo_all = getlogDdataframe(logD_submissions_ranked,experimental_data,output_dir_ranked)
    
    # Performance Statistics from across all ranked submissions that contain predictions for all solvent combinations
    perform_stats_bysubmission_ranked = getperformancestatsbysubmission(logD_dt_ranked_combo_all,output_dir_ranked)
    
    # Performance Statistics by solvent combination across all ranked submissions
    perform_stats_by_solvent_comb_ranked = getperformancestatsbysolventcombo(logD_dt_ranked,output_dir_ranked)