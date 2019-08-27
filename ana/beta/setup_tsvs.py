## Run nibetaseries on data

## Title: Set up TSV files
## Iterate through subject folders and grab the original tsv files for each run and edit/rename them with the BIDS standard for betaseries running, etc. 


# import packages
import os 
import glob 
import pandas as pd


# get data directory path
data_dir = '/projects/niblab/bids_projects/Experiments/Bevel/BIDS' #RENCI PATH
#data_dir = '/Users/nikkibytes/Documents/niblunc/testing_beta' # LOCAL PATH
print('Our working directory: {}'.format(data_dir))

# get subjects from data directory
#subjs_dirs = [sub for sub in glob.glob(os.path.join(data_dir, "sub-*")) if "html" not in sub]

subjs_dirs=['sub-012', 'sub-014', 'sub-018', 'sub-022', 'sub-025', 'sub-031', 'sub-032', 'sub-034', 'sub-035', 'sub-037', 'sub-038', 'sub-039', 'sub-042', 'sub-043', 'sub-044', 'sub-045', 'sub-046', 'sub-048', 'sub-050', 'sub-056', 'sub-058', 'sub-061', 'sub-062', 'sub-063', 'sub-064', 'sub-066', 'sub-067', 'sub-068', 'sub-069', 'sub-070', 'sub-071', 'sub-072', 'sub-073', 'sub-075', 'sub-076', 'sub-077', 'sub-079', 'sub-080', 'sub-082', 'sub-083', 'sub-084', 'sub-085', 'sub-089', 'sub-090']
# loop through subjects then runs and edit tsvs
subjs_dirs = ['sub-005']
for subj_dir in sorted(subjs_dirs):
    sub_id = subj_dir.split("/")[-1]
    event_files = glob.glob(os.path.join(data_dir, '{}/func/{}_run02_task-pst_events.tsv'.format(sub_id, sub_id)))
    for event_file in event_files:
        run_id = event_file.split("/")[-1].split("_")[1]
        run_id = run_id.replace("0", "-")
        #print(event_file)
        events_df = pd.read_csv(event_file, sep=",", na_values="n/a")
        events_df.head()
# Rename our original columns
        events_df.rename({"outcome": "trial_type"}, axis='columns', inplace=True)
        events_df.head()
        events_df.rename({"RT": "response_time"}, axis='columns', inplace=True)
        #print(events_df.head)
        events_df = events_df.dropna(axis="rows")
        events_df.head()
        new_df= events_df[["onset", "duration", 'trial_type', 'response_time']]
        print(new_df.head())
        newfile = os.path.join(data_dir, '{}/func/{}_task-prob_{}_events.tsv'.format(sub_id, sub_id, run_id))
        print("Writing to new file .... {}".format(newfile))
        new_df.to_csv(newfile, sep="\t", na_rep="n/a", index=False)
        # remove original files:
        #os.remove(event_file)
        
df = pd.read_csv("/projects/niblab/bids_projects/Experiments/Bevel/BIDS/sub-001/func/sub-001_task-prob_run-1_events.tsv", sep='\t')

correct=['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']