from utils.system_utils import *
from utils.diffusion_utils import *
from utils.surface_label_utils import *
import numpy as np
import os.path as op

subjects_dir = "/Applications/freesurfer/7.3.2/subjects"
subjects_list = ["subj01", "subj02", "subj03", "subj04",
                 "subj05", "subj06", "subj07", "subj08", "subj09", "subj10"]
runs = ["run1", "run2"]
hemis = ["lh", "rh"]
tck_types = ["vof", "track-merged"]

for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)

    for run in runs:
        for hemi in hemis:
            for tck_type in tck_types:

                if tck_type == "vof":
                    tck = op.join(subj_dir, "fyz", "anatomy",
                                  "diffusion", run, tck_type+".tck")
                else:
                    if run == "run1":
                        temp = "run_1"
                    else:
                        temp = "run_2"

                tck = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata_diffusion/ppdata",
                              subj, temp, "track", tck_type + ".tck")

                for thresh in ["t>0", "t>2", "t>3"]:
                    rois_base = op.join(
                        subj_dir, "fyz", "anatomy", hemi+"-rois", "all", "kastner+floc", thresh)
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
                        tck, all_rois, all_rois_out, all_rois_nodes)

                    whole_kastner_rois = op.join(
                        rois_base, hemi+".Kastner2015.subsetted.projected.gmwmi_intersected.binarized.withVTC.nii.gz")
                    whole_kastner_rois_out = op.join(
                        out_base, "VTCtoWholeIPS", thresh, tck_type)
                    whole_kastner_nodes = available_flocfaces_rois[1] + [18]
                    whole_kastner_nodes = ", ".join(str(int(node))
                                                    for node in whole_kastner_nodes)

                    intersect_tck_with_rois(
                        tck, whole_kastner_rois, whole_kastner_rois_out, whole_kastner_nodes)

                    whole_vtc_rois = op.join(
                        rois_base, hemi+".Kastner2015.subsetted.projected.gmwmi_intersected.withBinaryVTC.nii.gz")
                    whole_vtc_rois_out = op.join(
                        out_base, "IPStoWholeVTC", thresh, tck_type)
                    whole_vtc_nodes = [1] + ips_rois
                    whole_vtc_nodes = ", ".join(str(int(node))
                                                for node in whole_vtc_nodes)

                    intersect_tck_with_rois(
                        tck, whole_vtc_rois, whole_vtc_rois_out, whole_vtc_nodes)
