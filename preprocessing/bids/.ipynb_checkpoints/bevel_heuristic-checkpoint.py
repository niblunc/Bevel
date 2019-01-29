import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # create directories

    # anat/
    t1 = create_key('sub-{subject}/anat/sub-{subject}_T1w')


    # fmap/
    fmap_phase = create_key('sub-{subject}/fmap/sub-{subject}_phasediff')
    fmap_magnitude = create_key('sub-{subject}/fmap/sub-{subject}_magnitude')


    # func/
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_bold')
    prob = create_key('sub-{subject}/func/sub-{subject}_task-prob_run-{item:01d}_bold')




    info = {t1: [],  fmap_phase: [], rest: [], prob: [], fmap_magnitude: []}
    for s in seqinfo:
        print(s)
        if (s.dim3 == 192) and ('anat' in s.protocol_name):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 72) and ('fmap' in s.protocol_name):
            info[fmap_magnitude].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 36) and ('fmap' in s.protocol_name):
            info[fmap_phase].append(s.series_id)  # append if multiple series meet criteria
        if  ('run' in s.protocol_name):
            info[prob].append(s.series_id)  # append if multiple series meet criteria
	if (s.dim4 == 150) and ('resting' in s.protocol_name):
            info[rest].append(s.series_id)  # append if multiple series meet criteria


    return info