# Program to generate beta series files 

# Import packages 
import glob
import os
from subprocess import check_output
import argparse
import re


def make_file(sub_id, _dict, trial_id, output_path, run):
    print(">>>-----------> MAKING FILES")
    with open('/projects/niblab/bids_projects/Experiments/Bevel/testing_lin/derivatives/design_files/level1_betaseries.fsf','r') as infile:
        tempfsf=infile.read()
        if not os.path.exists(os.path.join(output_path, "design_files")):
            os.makedirs(os.path.join(output_path, "design_files"))
        design_fileout = os.path.join(output_path, "design_files/%s_%s_trial-%s_design1.fsf"%(sub_id, run, trial_id))
        # SET PARAMS 
        out_param = _dict[sub_id][run]["TRIALS"]["TRIAL%s"%trial_id]["OUTPUT"]
        func_param = _dict[sub_id][run]["FUNCRUN"]
        confound_param = _dict[sub_id][run]["CONFOUND"]
        trial_param = _dict[sub_id][run]["TRIALS"]["TRIAL%s"%trial_id]["TRIAL"]
        nuis_param = _dict[sub_id][run]["TRIALS"]["TRIAL%s"%trial_id]["NUIS"]

        tempfsf = tempfsf.replace("OUTPUT", out_param)
        tempfsf = tempfsf.replace("FUNCRUN", func_param) 
        tempfsf = tempfsf.replace("CONFOUND", confound_param)
        tempfsf = tempfsf.replace("TRIAL", trial_param)
        tempfsf = tempfsf.replace("NUIS", nuis_param)

        for i in range(6):
            moco = _dict[sub_id][run]["MOCO%i"%i]
            tempfsf = tempfsf.replace("MOCO%i"%i, moco)
        try:
            with open(design_fileout,'w') as outfile:
                outfile.write(tempfsf)
            outfile.close()
        except:
            print("BAD SUBJECT ", sub_id)
        infile.close()
        
    
# Fill the dictionary
def fill_dict(sub_path, _dict):
    sub_id = sub_path.split("/")[-1]
    functional_runs = glob.glob(os.path.join(sub_path, "func", "*run-*brain.nii.gz"))
    for functional in functional_runs:
        run_id = functional.split("/")[-1].split("_")[2]
        if run_id not in _dict[sub_id]:
            _dict[sub_id][run_id] = {}
        output_path = os.path.join(sub_path, 'Analysis/feat1/betaseries/%s'%run_id)
        
        _dict[sub_id][run_id]["FUNCRUN"] = functional
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        confound_file = os.path.join(sub_path, "func/motion_assessment/%s_task-prob_%s_space-MNI152Lin_desc-preproc_bold_brain_confound.txt"%(sub_id, run_id))
        _dict[sub_id][run_id]["CONFOUND"] = confound_file
        # MOTION PARAMETER FILES
        for i in range(6):
            motcor=os.path.join(sub_path, 'func','motion_assessment', 'motion_parameters','%s_task-prob_%s_moco%s.txt'%(sub_id, run_id,i))
            _dict[sub_id][run_id]['MOCO%i'%i] = motcor
        
        # ONSET FILES
        trial_files = sorted(glob.glob(os.path.join(sub_path, "func", "onsets", "bevel*run0%s*trial*.txt"%run_id.split("-")[1])))
        
        if not trial_files:
            pass
        else:
            if "TRIALS" not in _dict[sub_id][run_id]:
                _dict[sub_id][run_id]["TRIALS"] = {}
            for trial_file in trial_files:
                _id = sub_id.split("-")[1]
                _id = _id[1:]
                trial_id = trial_file.split("/")[-1].split(".")[0].split("_")[2].split("l")[1]
                nuis_file = os.path.join(sub_path, "func", "onsets", "bevel%s_run0%s_nuis%s.txt"%(_id, run_id.split("-")[1], trial_id))
                fileout = os.path.join(output_path, "%s_%s_trial-%s"%(sub_id, run_id, trial_id))
                _dict[sub_id][run_id]["TRIALS"]["TRIAL%s"%trial_id] = {"TRIAL" : trial_file, "NUIS": nuis_file, "OUTPUT" : fileout}
                make_file(sub_id, _dict, trial_id, output_path, run_id)

        
# Initialize Subject dict         
def set_dict(sub, _dict):
    _dict[sub] = {}         
            
# Main Method 
def main():
    deriv_dir= '/projects/niblab/bids_projects/Experiments/Bevel/testing_lin/derivatives'
    _dict= {}
    # START LOOP!!! -- looping through subjects
    SUBJECTS = glob.glob(os.path.join(deriv_dir, 'sub-*'))
    for sub_path in SUBJECTS:
        sub_id=sub_path.split("/")[-1]
        set_dict(sub_id, _dict)
        fill_dict(sub_path, _dict)
main()

