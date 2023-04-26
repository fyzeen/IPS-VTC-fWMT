# We define EVC as V1v, V1d, V2v, V2d, V3v, V3d, hV4
# These are the MANUALLY DEFINED ROIs that are covered in hemi.prf-visualrois.mgz and hemi.prf-eccrois.mgz for each subject

from utils.system_utils import *
from utils.surface_label_utils import *
from utils.anatomy_utils import *
from utils.diffusion_utils import *
import numpy as np
import os.path as op

subjects_dir = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/data/freesurfer"
subjects_list = ["subj01", "subj02", "subj03",
                 "subj04", "subj05", "subj06", "subj07", "subj08"]
hemis = ["lh", "rh"]
tck_types = ["track-merged"]


# DEFINE ANATOMY
for subj in subjects_list:
    print("################################")
    print("# Defining anatomy for: " + subj + " #")
    print("################################")

    subj_dir = op.join(subjects_dir, subj)

    for hemi in hemis:
        # binarize EVC ROI
        # project EVC ROI to GMWMI

        # concatenate with GMWMI-intersected VTC

        # define FWMTs from VTC ROIs to WHOLE EVC (requires binary)
        # We will use hemi.prf-eccrois.mgz for associating eccentricites to streamline endpoints ONLY
