# The SAMPL8 CB8 "Drugs of Abuse" challenge

The CB8 "drugs of abuse" challenge focuses on binding of CB8 to nine guests which are drugs of abuse, including morphine, hydromorphine, methamphetamine, cocaine and others. Binding has been experimentally characterized, a provisional patent filed, and the Isaacs group is preparing a paper for publication. Experimental details are forthcoming shortly.

G8 and G9, cycloheptanamine and cyclooctanamine, are included in the graphic/writeup because binding was measured by competition with these guests; these are not part of the challenge as experimental values were previously reported.

Our deadline for this challenge will be posted in the top-level [README.md](https://github.com/samplchallenges/SAMPL8/blob/master/README.md#the-cb8-challenge)

If you want any announcements of updates/changes/fixes here, [sign up for our e-mail list](https://mailchi.mp/e36018629725/sampl8-sign-ups).

## A quick view of the host and guests

![](images/CB8_overview.png)

G8 and G9 are not part of this challenge.

Please be sure to read the Disclaimers section below to note points which may require particular attention.

## More on the host

This host-guest series is based on the host cucurbit[8]uril (CB8), which was used in SAMPL3 and SAMPL6 (as previously summarized in the [SAMPL3 overview](http://dx.doi.org/10.1007/s10822-012-9554-1) and the [SAMPL6 overview](http://dx.doi.org/10.1007/s10822-018-0170-6)). CB8 is the eight-membered relative of cucurbit[7]uril, which was used in several other prior SAMPL challenges. Background information on CB8 may be found in a number of publications aside from the SAMPL overview papers, including DOI 10.1021/jp2110067, 10.1002/chem.201403405, and 10.1021/ja055013x.

## Experimental conditions

The buffer was 20 mM sodium phosphate buffer at pH 7.4. Guest concentrations were in the 0.5 mM to 1.5 mM range and CB8 concentrations are 0.025 mM to 0.1 mM. All binding stoichiometries have been validated by repeat ITC experiments and by NMR spectroscopy binding studies.


## Disclaimers

Note that we have typically selected, or attempted to select, reasonable protonation states and conformers of the hosts and guests, but these may be controversial, uncertain, or change upon binding, so participants are encouraged to exercise care in selecting which states are modeled. Typically selection of protonation states, tautomers and conformers is one major place where participant protocols differ and lead to different downstream results.

**Here, the protonation state of G5, ketamine, may require particular attention**, as the pKa is [near neutral pH](https://pubchem.ncbi.nlm.nih.gov/compound/Ketamine#section=Environmental-Bioconcentration).

Additionally, **you may wish to pay attention to the geometry of certain trivalent nitrogen centers**; if these are protonated they can function (computationally) as a chiral center though experimentally they will likely interconvert quickly. Unless all guest geometries are sampled the selected geometry might impact binding estimates for some methods.

## What's here:
- `host_files`: Files relating to the CB8 host; provides structure files for the host.
- `guest_files`: Files relating to the CB8 guests; provides structure files for the guests.
- `images`: Images used in this repo
- `source_files`: Raw source files as provided by the Isaacs group
- `CB8_submission.txt`: An example submission file for submitting to our system (please replace text and values with your own!). Filenames must being with "CB8". See [host_guest_instructions.md](https://github.com/samplchallenges/SAMPL8/blob/master//host_guest_instructions.md) for submission instructions.
