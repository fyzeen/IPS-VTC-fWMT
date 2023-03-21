from utils.system_utils import *
from utils.streamline_to_surface_utils import *
from utils.surface_label_utils import *
import os.path as op
import os
import subprocess

subjects_dir = "/Applications/freesurfer/7.3.2/subjects"
subjects_list = ["subj01", "subj02", "subj03",
                 "subj04", "subj05", "subj06", "subj07", "subj08"]
runs = ["run1", "run2"]
hemis = ["lh", "rh"]
tck_types = ["vof", "track-merged"]
thresh = "t>3"

for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)
    T1_path = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata",
                      "ppdata", subj, "anat", "T1_0pt8_masked.nii.gz")

    for run in runs:
        for hemi in hemis:
            for tck_type in tck_types:
                # VTC ROIs to whole IPS
                tck_path = op.join(subj_dir, "fyz", run, hemi,
                                   "VTCtoWholeIPS", thresh, tck_type)
                os.chdir(tck_path)
                out = subprocess.check_output("echo node*-18.tck", shell=True)
                tck_list = str(out)[2:-3].split()

                for tck in tck_list:
                    streamlines_to_surface(
                        op.join(tck_path, tck), T1_path, tck_path, subj, hemi)

                    intersect_surf_labels(op.join(tck_path, tck[:-4]+".endpoints.mgz"),
                                          op.join(subj_dir, "fyz", "anatomy", hemi+"-rois",
                                                  "all", "kastner", hemi+".Kastner2015.subsetted.mgz"),
                                          True, tck_path, "IPS-intersected")

                # VTC ROIs (each separate) to IPS0 and IPS1
                tck_path = op.join(subj_dir, "fyz", run,
                                   hemi, "all", thresh, tck_type)
                os.chdir(tck_path)
                out = subprocess.check_output("echo node*-*.tck", shell=True)
                tck_list = str(out)[2:-3].split()

                for tck in tck_list:
                    streamlines_to_surface(
                        op.join(tck_path, tck), T1_path, tck_path, subj, hemi)

                    intersect_surf_labels(op.join(tck_path, tck[:-4]+".endpoints.mgz"),
                                          op.join(subj_dir, "fyz", "anatomy", hemi+"-rois",
                                                  "all", "kastner", hemi+".Kastner2015.subsetted.mgz"),
                                          True, tck_path, "IPS-intersected")
