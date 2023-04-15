from utils.surface_label_utils import smooth_surf_labels
import os.path as op

subjects_dir = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/data/freesurfer"
subjects_list = ["subj01", "subj02", "subj03",
                 "subj04", "subj05", "subj06", "subj07", "subj08"]

for subj in subjects_list:
    for hemi in ["lh", "rh"]:
        subj_dir = op.join(subjects_dir, subj)

        label_path = op.join(subj_dir, "label")
        eccentricity_path = op.join(label_path, hemi+".prfeccentricity.mgz")
        smooth_surf_labels(eccentricity_path, label_path, subj, hemi)
