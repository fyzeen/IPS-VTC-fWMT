# We define EVC as V1v, V1d, V2v, V2d, V3v, V3d, hV4
# These are the MANUALLY DEFINED ROIs that are covered in hemi.prf-visualrois.mgz and hemi.prf-eccrois.mgz for each subject

from utils.system_utils import *
from utils.surface_label_utils import *
from utils.anatomy_utils import *
from utils.diffusion_utils import *
from utils.streamline_to_surface_utils import *
import numpy as np
import os
import os.path as op

subjects_dir = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/data/freesurfer"
subjects_list = ["subj01", "subj02", "subj03",
                 "subj04", "subj05", "subj06", "subj07", "subj08"]
hemis = ["lh", "rh"]
runs = ["run1", "run2"]


# DEFINE ANATOMY
for subj in subjects_list:
    print("################################")
    print("# Defining anatomy for: " + subj + " #")
    print("################################")

    subj_dir = op.join(subjects_dir, subj)

    for hemi in hemis:
        gmwmi_path = op.join(subj_dir, "fyz", "anatomy",
                             "volumes", "gmwmi.binarized.nii.gz")
        evc_eccrois = op.join(subj_dir, "label", hemi+".prf-eccrois.mgz")
        evc_folder = op.join(subj_dir, "fyz", "anatomy", hemi+"-rois", "EVC")

        # project EVC ROI to GMWMI
        surfROI_to_WM(evc_eccrois, op.join(subj_dir, "mri", "aseg.mgz"),
                      hemi, subj, evc_folder)

        evc_projected_path = op.join(
            evc_folder, hemi+".prf-eccrois.projected.nii.gz")
        intersect_roi_gmwmi(evc_projected_path, gmwmi_path,
                            True, evc_folder)

        # binarize EVC ROI
        evc_gmwmi = op.join(evc_folder,
                            hemi+".prf-eccrois.projected.gmwmi_intersected.nii.gz")
        binarize_gmwmi(evc_gmwmi, True, evc_folder, binarize_to=10)

        # concatenate with GMWMI-intersected VTC
        floc_face_gmwmi = op.join(subj_dir, "fyz", "anatomy", hemi+"-rois", "all", "floc-faces",
                                  "t>3", hemi+".floc-faces.subsetted.thresholded3.projected.gmwmi_intersected.nii.gz")
        evc_gmwmi_binarized = op.join(evc_folder,
                                      hemi+".prf-eccrois.projected.gmwmi_intersected.binarized.nii.gz")
        concat_volumes(evc_gmwmi_binarized, floc_face_gmwmi,
                       "withVTCrois", True, evc_folder)

# define FWMTs from VTC ROIs to WHOLE EVC (requires binary)
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

        if run == "run1":
            temp = "run_1"
        else:
            temp = "run_2"
        tck = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata_diffusion/ppdata", subj,
                      temp, "track", "track-merged" + ".tck")

        print("#########")
        print("# " + "track-merged" + ", " + run + ", " + "t>3" + " #")
        print("#########")

        available_flocfaces_rois = available_floc_rois(op.join(
            subj_dir, "fyz", "anatomy", hemi+"-rois", "all", "floc-faces", "t>0", hemi+".floc-faces.subsetted.mgz"))

        out_base = op.join(subj_dir, "fyz", run, hemi)
        evc_folder = op.join(subj_dir, "fyz", "anatomy", hemi+"-rois", "EVC")
        all_rois = op.join(evc_folder,
                           hemi+".prf-eccrois.projected.gmwmi_intersected.withVTC.nii.gz")

        all_rois_out = op.join(out_base, "EVC")
        all_rois_nodes = available_flocfaces_rois[1] + [10]
        all_rois_nodes = ", ".join(str(int(node)) for node in all_rois_nodes)

        intersect_tck_with_rois(tck, all_rois, all_rois_out, all_rois_nodes)


# We will use hemi.prf-eccrois.mgz OR smoothed pRF eccentricities for associating eccentricites to streamline endpoints ONLY
for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)
    T1_path = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata",
                      "ppdata", subj, "anat", "T1_0pt8_masked.nii.gz")

    for run in runs:
        for hemi in hemis:
            print("##########")
            print(f"# {subj} {run} track-merged {hemi} #")
            print("##########")

            tck_path = op.join(subj_dir, "fyz", run, hemi, "EVC")
            os.chdir(tck_path)
            out = subprocess.check_output("echo node*-18.tck", shell=True)
            tck_list = str(out)[2:-3].split()

            for tck in tck_list:
                print("VTCtoWholeIPS " + tck)
                streamlines_to_surface(
                    op.join(tck_path, tck), T1_path, tck_path, subj, hemi)

                intersect_surf_labels(op.join(tck_path, tck[:-4]+".endpoints.mgz"),
                                      op.join(subj_dir, "label",
                                              hemi+".prf-eccrois.mgz"),
                                      True, tck_path, "EVC-intersected")
