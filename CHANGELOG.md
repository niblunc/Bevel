# Changelog
All notable changes to this project will be documented in this file.  
  
  
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
  
  
## [0.0.1] - 2019-02-06 
### Added  
- Complete up to date (no error) subject count: 77 
- complete DICOM to BIDS data added under ~/Nifti/ directory (90 subjects)
- complete fmriprep data added under ~/fmriprep/ directory (90 subjects)
- Confounds and skull stripped functionals complete for 77 subjects
- Feat1 analysis completed for 77 subjects 
- Feat1 betaseries analysis completed for 77 subjects
- Feat2 analysis completed for 77 subjects

#### Fixed  
- many subjects were corrected for bad volumes, and went through pipeline again to adjust for any discrepancies between data 

#### Errors
- these subjects sub-047, sub-055, sub-033: onset error when trying to run feat1, need further inspection
- sub-005,  sub-011,  sub-015, sub-030,  sub-036 are missing volumes and/or have too many bad volumes, need further inspection


### Removed
- sub-065, sub-023, sub-049 each are removed for bad scans





