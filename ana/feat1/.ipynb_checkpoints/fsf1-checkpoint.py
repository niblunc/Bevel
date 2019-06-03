import glob
import os
from subprocess import check_output
import argparse
import re




def make_file(deriv_dir, key):
    for run in main_dict[key]:
        with open(os.path.join(deriv_dir,'design_files/design1.fsf'),'r') as infile:
            tempfsf=infile.read()

            num=int(run)
            out = main_dict[key][run]["OUTPUT"]
            func = main_dict[key][run]["FUNCRUN%i"%num]
            time = main_dict[key][run]["NTIMEPOINT%i"%num]
            con = main_dict[key][run]["CONFOUND%i"%num]

            tempfsf = tempfsf.replace("OUTPUT", out)
            tempfsf = tempfsf.replace("FUNCRUN", func) #4D AVW DATA
            tempfsf = tempfsf.replace("NTPTS", time)
            tempfsf = tempfsf.replace("CONFOUND", con)

            for key2 in main_dict[key][run]:
                if re.match(r'EV[0-9]TITLE', key2):
                    ev_title = main_dict[key][run][key2]
                    n = re.findall('\d+', key2)
                    n = ''.join(str(x) for x in n)
                    ev = main_dict[key][run]["EV%s"%n]
                    #print("EVTITLE: ", ev_title)
                    #print("EV%s"%n, ev)
                        #tempfsf = tempfsf.replace("EV%sTITLE"%n, ev_title)
                    tempfsf = tempfsf.replace("EV%s"%n, ev)

            for i in range(6):
                moco = main_dict[key][run]["MOCO%i"%i]
                tempfsf = tempfsf.replace("MOCO%i"%i, moco)
                #print("MOCO%i: "%i , main_dict[key][run]["MOCO%i"%i])
            outpath= os.path.join(deriv_dir, key, 'Analysis', "feat1")
                #print(tempfsf)
            if not os.path.exists(outpath):
                os.makedirs(outpath)
            #print("OUT PATH >>>>>>---------> ", outpath)
            with open(os.path.join(outpath,'%s_run-%s_no_reg.fsf'%(key,run)),'w') as outfile:
                outfile.write(tempfsf)
            outfile.close()
        infile.close()
        
        

def fill_dict(sub_path):
    sub = sub_path.split("/")[-1].split("_")[0]
    runs = glob.glob(os.path.join(sub_path, "func", "*run*bold_brain.nii.gz"))
    if len(runs) != 0:
        for func in runs:
            name = func.split("/")[-1].split(".")[0].split('_space-MNI152Lin')[0]
            run = name.split("_")[2].split("-")[1]
            if run not in main_dict[sub]:
                main_dict[sub][run] = {}
            x=int(run)
            output = os.path.join(sub_path, "Analysis", "feat1", "%s"%name)
            confound = os.path.join(sub_path, "func/motion_assessment", "%s_space-MNI152Lin_desc-preproc_bold_brain_confound.txt"%name)
            main_dict[sub][run]['OUTPUT'] = output
            scan = func.split(".")[0]
            main_dict[sub][run]["FUNCRUN%i"%x] = scan
            ntmpts=check_output(['fslnvols', scan])
            ntmpts = ntmpts.decode('utf-8')
            ntmpts = ntmpts.strip('\n')
            main_dict[sub][run]['NTIMEPOINT%i'%x] = ntmpts
            main_dict[sub][run]['CONFOUND%i'%x] = confound
            trs=check_output(['fslval','%s'%(scan),'pixdim4',scan])
            trs=trs.decode('utf-8')
            trs=trs.strip('\n')
            #print("TRs: ", trs)
            main_dict[sub][run]['TR'] = trs
            for i in range(6):
                motcor=os.path.join(sub_path, 'func/motion_assessment/motion_parameters','%s_moco%s.txt'%(name,i))
                main_dict[sub][run]['MOCO%i'%i] = motcor
                #print("MOTCOR: ", motcor)
            ctr=0
            ev_list = ["bitter", "img", "neu", "sweet"]
            for item in ev_list:
                ctr=ctr+1
                main_dict[sub][run]['EV%iTITLE'%ctr] = item
                ev=os.path.join(sub_path,'func','onsets','%s_task-%s_run-%s.txt'%(sub, item,run))
                main_dict[sub][run]['EV%i'%ctr] = ev
    else:
        print("NOT 4 RUNS: ", sub)


def set_dict(sub):
    main_dict[sub] = { }
    
    
def create_fsf():
    global main_dict
    main_dict= {}
    deriv_dir = '/projects/niblab/bids_projects/Experiments/Bevel/testing_lin/derivatives'
    sub_list = ["sub-005", "sub-013", "sub-015", "sub-023", "sub-030", "sub-035", "sub-036", "sub-039", "sub-045", "sub-053", "sub-065", "sub-086"]
    subs = [x for x in glob.glob(os.path.join(deriv_dir, 'sub-*')) if x.split("/")[-1] in sub_list]
    print(subs)
    for sub_path in subs:
        sub=sub_path.split("/")[-1]
        outdir = os.path.join(sub_path, "Analysis", "feat1")
        #print(sub)
        set_dict(sub)
        fill_dict(sub_path)
        make_file(deriv_dir, sub)

def main():
    create_fsf()
main()