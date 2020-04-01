import glob
import os
from subprocess import check_output
import argparse
import re
        
        

        


def make_file(sub,main_dict, task, deriv_dir, fsf_template):
    print("making file for subject ", sub)
    #for sess_id in sessions:


    if task == "resting":
        # case - no runs, only single task (i.e. resting)
        pass

    else:
        for key in main_dict[sub]:
            if key != "ANAT":
                run = key
                #print(run)
                outpath = os.path.join(deriv_dir, sub, 'func', 'Analysis', "feat1")
                if not os.path.exists(outpath):
                    os.makedirs(outpath)


                with open(fsf_template, 'r') as infile:
                    #print("Opening template file {}".format(fsf_template))
                    tempfsf = infile.read()

                    #  fill in tempfsf file with parameters
                    tempfsf = tempfsf.replace("OUTPUT", main_dict[sub][run]["OUTPUT"])
                    tempfsf = tempfsf.replace("FUNCTIONAL", main_dict[sub][run]["FUNC"])
                    tempfsf = tempfsf.replace("CONFOUND", main_dict[sub][run]['CONFOUND'])
                    tempfsf = tempfsf.replace("VOL", main_dict[sub][run]['VOL'])


                    # loop through keys in dict to find EVs and MOCOs
                    for key in main_dict[sub][run]:


                        # Fill in EVS
                        if re.match(r'EV', key):
                            ev_name= "{}_file".format(key.replace("EV_", ""))
                            ev = main_dict[sub][run][key]
                            tempfsf = tempfsf.replace(ev_name, ev)
                            #print(ev_name)
                        if re.match(r'moco', key):
                            moco_file = main_dict[sub][run][key]
                            moco_id = moco_file.split("/")[-1].split("_")[3].split(".")[0].upper()
                            tempfsf = tempfsf.replace(moco_id, moco_file)
                            #print(moco_id)

                    fsf_outfile = 'task-%s_run-%s_expanded2.0.fsf' % (task, run)
                    print(fsf_outfile)
                    #print(outpath)
                    #print(tempfsf)
                    with open(os.path.join(outpath, fsf_outfile), 'w') as outfile: #os.path.join(outpath,
                        outfile.write(tempfsf)
                    outfile.close()
                infile.close()

                
                


def fill_dict(sub, main_dict, task, deriv_path, evs, all_runs):
    
    
    sub_path = os.path.join(deriv_path, sub)
    bevel_id = "bevel%s"%sub.split("-")[1][1:]
    print(bevel_id)
    #print("SUBJECT: %s \t TASK: %s \nPATH: %s"% (sub, task, sub_path))

    # only specified sessions
    #for sess_id in sessions:

    if task == 'resting':
        # case for no runs, only task (i.e. resting)
        pass
    else:
    # 2 cases: individual/given runs or all runs found

        # case 1: if flag false, grab all available runs found
        if all_runs == True:
            funcs_found = glob.glob(os.path.join(deriv_path, sub, 'func',
                                         "%s_task-%s_run-*preproc*brain.nii.gz" % (sub,task)))
            runs=[x.split("/")[-1].split("_")[2].split("-")[1] for x in funcs_found]
            for run in runs:
                main_dict[sub][run] = {}
            #print("Dictionary initialized as: {}".format(main_dict[sub]))

            for func in funcs_found:
                x = int(run)
                run=func.split("/")[-1].split("_")[2].split("-")[1]
                
                
                # SET OUTPUT PATH FOR FEAT DIRECTORY
                output_path=os.path.join(sub_path, 'func',
                                         'Analysis', 'feat1', 'task-%s_run-%s_expanded2.0' %(task, run))


                # SET CONFOUND
                # sub-001_task-prob_run-1_bold_space-MNI152NLin2009cAsym_preproc_brain_confound.txt

                confound = os.path.join(deriv_path, sub, 'func', 'motion_assessment',
                                 '%s_task-%s_run-%s_bold_space-MNI152NLin2009cAsym_preproc_brain_confound.txt'%(sub, task, run))

                # SET ANAT
                #anat = os.path.join(deriv_path, sub, 'ses-1/anat', 'highres.nii.gz')





                # FILL DICTIONARY
                #main_dict[sub]['ANAT'] = anat
                main_dict[sub][run]['OUTPUT'] = output_path
                scan = func.split(".")[0]
                main_dict[sub][run]['FUNC'] = scan
                vol = check_output(['fslnvols', scan])
                vol = vol.decode('utf-8')
                vol = vol.strip('\n')
                main_dict[sub][run]['VOL'] = vol
                main_dict[sub][run]['CONFOUND'] = confound



                # TRS FROM NIFTI -- this value will always be 2, therefore we only run the check once
                trs = check_output(['fslval', '%s' % (scan), 'pixdim4', scan])
                trs = trs.decode('utf-8')
                trs = trs.strip('\n')
                # print("TRs: ", trs)

                main_dict[sub][run]['TR'] = trs


                # SET MOTION PARAMETERS
                for i in range(6):
                    motcor = os.path.join(sub_path, 'func', 'motion_assessment', 'motion_parameters',
                                      '%s_task-%s_run-%s_moco%s.txt' % (sub, task, run, i))
                    main_dict[sub][run]['moco%i' % i] = motcor


                # SET EVS
                # Loop through the given EVs and add the corresponding file to the dictionary

                ctr = 0
                onset_path = "/projects/niblab/bids_projects/Experiments/Bevel/onsets/onsets_expandedPE"
                for ev_name in evs:
                    # print(item)
                    ctr = ctr + 1

                    ev = os.path.join(onset_path,  '%s_%s_run0%s.txt' % (bevel_id, ev_name, run))
                    
                    #print(ev)
                    # print("EV: ", ev)
                    main_dict[sub][run]['EV_%s' % ev_name] = ev


        else:
            ## go through runs given in arguments

            pass




        
def main():
    #set_paths()
    # removed path function for now
    print("Starting program....")
    
    deriv_dir = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives"
    main_dict = {}
    subject_folders = sorted(glob.glob(os.path.join(deriv_dir, 'sub-*')))
    run_bash = True
    write_file = False
    
    if write_file == True:
        ## case: Get all subjects available --add flag for individual subjects or passed list option
        for sub_path in subject_folders:

            # set variables
            sub = sub_path.split("/")[-1]
            task = "prob"
            sessions = ["ses-1"]
            evs = ['AB_sweet_match', 'AB_sweet_PE', 'AB_bitter_match', 'AB_bitter_PE', 'CD_sweet_match', 'CD_sweet_PE', 'CD_bitter_match', 'CD_bitter_PE','EF_sweet_match', 'EF_sweet_PE', 'EF_bitter_match', 'EF_bitter_PE']
            all_runs = True
            fsf_template = os.path.join(deriv_dir,'design_files/design1-expanded2.0.fsf')


            #set_dict(sub)
               
            if sub not in main_dict:
                main_dict[sub] = {}


            # set up dict for runs IF flag is passed
            # def fill_dict(sub, main_dict, task, deriv_path, sessions,evs, all_runs)
            fill_dict(sub, main_dict, task, deriv_dir, evs, all_runs)

            #for key in main_dict[sub]:
                #for ky in main_dict[sub][key]:
                    #for k in main_dict[sub][key]:
                    #print(ky, main_dict[sub][key][ky])

            #def make_file(sub,main_dict, run, task, deriv_dir, fsf_template)
            make_file(sub, main_dict, task, deriv_dir, fsf_template)
    

    if run_bash == True:
        
        subject_set = sorted([x.split("/")[-1].split("-")[1].lstrip("0") for x in subject_folders])

        bash_file = os.path.join('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/code', 'feat1_exp2.0.job')
        start = subject_set[0]
        end = subject_set[-1]
        #print(start, end)
        #for sub_num in subject_set:
        shell_cmd = "sbatch --array={}-{}%{} {}".format(start, end, len(subject_set), bash_file)
        os.system(shell_cmd)
        print(shell_cmd)

            
main()