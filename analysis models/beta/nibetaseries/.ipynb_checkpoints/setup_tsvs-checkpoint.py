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
subjs_dirs = [sub for sub in glob.glob(os.path.join(data_dir, "sub-*")) if "html" not in sub]


# loop through subjects then runs and edit tsvs

for subj_dir in sorted(subjs_dirs):
    sub_id = subj_dir.split("/")[-1]
    event_files = glob.glob(os.path.join(data_dir, '{}/func/{}_run*_task-pst_events.tsv'.format(sub_id, sub_id)))
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
        #new_df.to_csv(newfile, sep="\t", na_rep="n/a", index=False)
        # remove original files:
        #os.remove(event_file)