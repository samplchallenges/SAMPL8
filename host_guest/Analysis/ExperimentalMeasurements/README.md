## Manifest

- `CB8-DOA-SAMPL-Answer-Sheet-20200908.docx`: Data provided by the Isaacs group (docx).
- `CB8-DOA-SAMPL-Answer-Sheet-20200908.pdf`: Data provided by the Isaacs group (pdf).
- `generate_tables.py`: Script used to perform error propagation and create the experimental_measurements.X files based on the data provided by the Isaacs (and, later, Gilson and Gibb) groups. Adapted from [the SAMPL6 `generate_tables.py`](https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by Andrea Rizzi, and [the SAMPL7 `generate_tables.py`](https://github.com/samplchallenges/SAMPL7/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by David Mobley.

Experimental conditions/details are available in the above provided files, the [Isaacs' CB8 README](https://github.com/samplchallenges/SAMPL8/blob/master/host_guest/CB8/README.md), and in [CB8 literature](https://chemrxiv.org/articles/preprint/In_Vitro_and_In_Vivo_Sequestration_of_Phencyclidine_by_Me4Cucurbit_8_uril/12994004) as of 9/25/20

## Notes on error propagation

Currently, for Isaacs' CB8 system, we are utilizing uncertainties provided by Lyle Isaacs, which provide ITC-based uncertainties, along with additional error propagation to handle uncertainties in titrant concentrations, as was done for SAMPL6 and SAMPL7.
