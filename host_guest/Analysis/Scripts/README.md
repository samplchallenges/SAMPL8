# SAMPL8 host-guest analysis scripts

## Manifest
- `analyze_hostguest.py`: Master analysis script, based on SAMPL6 host-guest analysis script from Andrea Rizzi.
- `get_usermap.py`: Should be run before `analyze_hostguest.py`; obtains and stores a submission map which lists submission IDs and corresponding file names.
- `pkganalysis`: Utility classes/functions to parse SAMPL submissions and for statistical analysis. 
