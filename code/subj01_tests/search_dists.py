from utils.system_utils import *
from utils.diffusion_utils import *
from utils.streamline_to_surface_utils import *
from utils.surface_label_utils import *
import numpy as np
import os.path as op
import os
import subprocess

subjects_dir = "/Applications/freesurfer/7.3.2/subjects"
subjects_list = ["subj01"]
runs = ["run1"]
hemis = ["lh"]
tck_types = ["track-merged"]

for subj in subjects_list:
    print("################################")
    print("# Defining fWMTS for: " + subj + " #")
    print("################################")
    subj_dir = op.join(subjects_dir, subj)

    for run in runs:
        for hemi in hemis:
            print("#########")
            print("# " + hemi + " #")
            print("#########")

            for tck_type in tck_types:
                thresh = "t>3"
                tck = op.join(subj_dir, "fyz", "anatomy",
                              "diffusion", "run1", "track-merged.tck")

                rois_base = op.join(subj_dir, "fyz", "anatomy",
                                    hemi+"-rois", "all", "kastner+floc", thresh)
                out_base = op.join(subj_dir, "fyz", run, hemi)

                available_flocfaces_rois = available_floc_rois(op.join(
                    subj_dir, "fyz", "anatomy", hemi+"-rois", "all", "floc-faces", "t>0", hemi+".floc-faces.subsetted.mgz"))
                ips_rois = [18, 19, 20, 21]

                all_rois = op.join(
                    rois_base, hemi+".Kastner2015.subsetted.projected.gmwmi_intersected.withVTC.nii.gz")
                all_rois_out = op.join(out_base, "all", thresh, tck_type)
                all_rois_nodes = available_flocfaces_rois[1] + ips_rois
                all_rois_nodes = ", ".join(str(int(node))
                                           for node in all_rois_nodes)

                intersect_tck_with_rois(
                    tck, all_rois, all_rois_out, all_rois_nodes, search_dist="0.5")

for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)
    T1_path = op.join(subj_dir, "fyz", "anatomy",
                      "volumes", "T1_0pt8_masked.nii.gz")

    for run in runs:
        for hemi in hemis:
            for tck_type in tck_types:
                print("##########")
                print(f"# {subj} {run} {tck_type} {hemi} #")
                print("##########")

                tck_path = op.join(subj_dir, "fyz", run,
                                   hemi, "all", thresh, tck_type)
                os.chdir(tck_path)
                out = subprocess.check_output("echo node*-*.tck", shell=True)
                tck_list = str(out)[2:-3].split()

                for tck in tck_list:
                    print("All " + tck)
                    streamlines_to_surface(
                        op.join(tck_path, tck), T1_path, tck_path, subj, hemi)

                    intersect_surf_labels(op.join(tck_path, tck[:-4]+".endpoints.mgz"),
                                          op.join(subj_dir, "fyz", "anatomy", hemi+"-rois",
                                                  "all", "kastner", hemi+".Kastner2015.subsetted.mgz"),
                                          True, tck_path, "IPS-intersected")
