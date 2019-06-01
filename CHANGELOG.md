# Changelog
All notable changes to this project will be documented in this file.  
  
  
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2019-05
### Changes
- Added missing subject: sub-088
- Upgraded data with new FMRIPREP version 2019, this allows us to put data into linear space, using flag '--output-spaces  MNI152Lin'

## 2019-03-05 
### Added 
- Added 9 subjects, current subject count: 86
- All 85 subjects have data preprocessed and have run feat1 and feat2 analysis

### Fixed
- sub-081, run-3 files removed for bad volumes, 4 runs available 
- 4 subjects have three runs available:
sub-005 - run files removed for bad volumes, 3 files available
sub-015 - "run-2" removed for bad volume count, 3 files available 
sub-030 - "run-3" removed for bad volume, 3 files available
sub-036 - run files removed for bad volumes, 3 files available 
  
## 2019-02-11 
### Added  
- Complete up to date (no error) subject count: 77 
- complete DICOM to BIDS data added under ~/Nifti/ directory (90 subjects)
- complete fmriprep data added under ~/fmriprep/ directory (90 subjects)
- Confounds and skull stripped functionals complete for 77 subjects
- Feat1 analysis completed for 77 subjects 
- Feat1 betaseries analysis completed for 77 subjects
- Feat2 analysis completed for 77 subjects

### Fixed  
- many subjects were corrected for bad volumes, and went through pipeline again to adjust for any discrepancies between data 

### Errors
- these subjects sub-047, sub-055, sub-033: onset error when trying to run feat1, need further inspection
- sub-005,  sub-011,  sub-015, sub-030,  sub-036 are missing volumes and/or have too many bad volumes, need further inspection


### Removed
- sub-023, sub-049, sub-065 are each removed for unrecoverable scans. 

## 2019-03-22
### Added
- Design file for Feat1 that separates taste events by expectation (matched vs. prediction error [PE]) and splits "choice" EV into each image pair. 





