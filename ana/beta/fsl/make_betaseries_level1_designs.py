import glob
import os
from subprocess import check_output
import argparse
import re
        

def make_file(sub_id, run, trial_id, output_dir):
    with open(os.path.join(deriv_dir,'design_files/beta1_v2_design.fsf'),'r') as infile:
        tempfsf=infile.read()
        if not os.path.exists(os.path.join(output_dir, "design_files")):
            os.makedirs(os.path.join(output_dir, "design_files"))
        design_fileout = os.path.join(output_dir, "design_files/%s_run-%s_trial-%s_design1_rinse.fsf"%(sub_id, run, trial_id))
        print("Making file {}.........\n".format(design_fileout))
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

# here we set up the nested dictionary where the outer keys are the subjects
# we assume we have 4 runs for each subject and set up the a dictionary w/i the subj dict where the runs are the keys
# the run dictionary holds another dictionary w/ key "TRIALS", a list of MOCO files, and the input nifti file w/ key FUNCRUN

def set_dict(sub):
    _dict[sub] = {}
    for run in RUNS:
        _dict[sub][run] = {
            "TRIALS" : { },
            "CONFOUND" : None,
            "FUNCRUN" : None
        }           
            
def create_fsf():
    global _dict
    _dict= {}
    # START LOOP!!! -- looping through subjects
    SUBJECTS = glob.glob(os.path.join(deriv_dir, 'sub-*'))
    for sub_path in SUBJECTS:
        sub_id=sub_path.split("/")[-1]
        set_dict(sub_id)
        for run in RUNS: # SECOND LOOP -- looping through RUNS
            # MAKE/SET OUTPUT DIRECTORY
            output_dir = os.path.join(sub_path, "func/Analysis/beta/run-%s"%run)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # GET INPUT FILE 
            # -- FUNCRUN
            funcrun_file = os.path.join(sub_path, "func/%s_task-prob_run-%s_bold_space-MNI152NLin2009cAsym_preproc_brain.nii.gz"%(sub_id, run))
            _dict[sub_id][run]["FUNCRUN"] = funcrun_file
            # GET CONFOUND
            confound_file = os.path.join(sub_path, "func/motion_assessment/%s_task-prob_run-%s_bold_space-MNI152NLin2009cAsym_preproc_brain_confound.txt"%(sub_id, run))
            _dict[sub_id][run]["CONFOUND"] = confound_file
            # GET MOCO FILES
            # -- MOTION CORRECTION
            for i in range(6):
                motcor=os.path.join(sub_path, 'func','motion_assessment', 'motion_parameters','%s_task-prob_run-%s_moco%s.txt'%(sub_id, run,i))
                _dict[sub_id][run]['MOCO%i'%i] = motcor
            # GET TRIALS 
            bevel_id = sub_id.replace("sub-0", "bevel")
            subj_trials = sorted(glob.glob(os.path.join(sub_path, "func", "onsets", "bevel*run0%s*rinse*trial*.txt"%run)))
            if not subj_trials:
                pass
            else:
                # Get NUIS condition files
                for trial_file in subj_trials:
                    _id = sub_id.split("-")[1]
                    _id = _id[1:]
                    trial_id = trial_file.split("/")[-1].split(".")[0].split("_")[3].split("l")[1]
                    #print(trial_id)
                    nuis_file = os.path.join(sub_path, "func", "onsets", "bevel%s_run0%s_rinse_nuis%s.txt"%(_id, run, trial_id))
                    output_path = os.path.join(output_dir, "%s_run-%s_rinse-%s"%(sub_id, run, trial_id))
                    _dict[sub_id][run]["TRIALS"]["TRIAL%s"%trial_id] = {"TRIAL" : trial_file, "NUIS": nuis_file, "OUTPUT" : output_path}
                    make_file(sub_id, run, trial_id,output_dir) 
def set_paths():
    global input_dir
    global deriv_dir
    print(">>>----> SETTING PATHS")
    input_dir =  '/projects/niblab/bids_projects/Experiments/Bevel'
    deriv_dir= '/projects/niblab/bids_projects/Experiments/Bevel/derivatives'
    

def main():
    global RUNS
    RUNS = ["1", "2", "3", "4"]
    set_paths()
    create_fsf()
main()
