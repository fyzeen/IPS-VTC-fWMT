from utils.system_utils import *
from utils.surface_label_utils import *
from utils.anatomy_utils import *
from utils.diffusion_utils import *
from utils.streamline_to_surface_utils import *
import numpy as np
import os
import os.path as op

subjects_dir = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/data/freesurfer"
subjects_list = ["subj01", "subj02", "subj03", "subj04", "subj05", "subj06", "subj07", "subj08"]
hemis = ["lh", "rh"]
runs = ["run1", "run2"]

# DEFINE ANATOMY
for subj in subjects_list:
    print("################################")
    print("# Defining anatomy for: " + subj + " #")
    print("################################")

    subj_dir = op.join(subjects_dir, subj)
    
    gmwmi_path = op.join(subj_dir, "fyz", "anatomy", "volumes", "gmwmi.binarized.nii.gz")

    for hemi in hemis:
        floc_words_path = op.join(subj_dir, "label", hemi + ".floc-words.mgz")
        floc_words_tval_path = op.join(subj_dir, "label", hemi + ".flocwordtval.mgz")
            
        # Determine floc-words ROIs available for subject
        print("Determining floc-words ROIs available for: " + subj)
        available_rois = available_floc_rois(floc_words_path)
        
        # subset and threshold floc-words
        print("Subsetting and thresholding floc-words ROIs for: " + subj)
        
        try:
            os.mkdir(op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words"))
        except FileExistsError:
            pass
        
        subsetted_floc_out_path = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words")
        subset_rois(available_rois[1], floc_words_path, ".mgz", True, subsetted_floc_out_path)
        
        subsetted_floc_path = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words", 
                                      hemi + ".floc-words.subsetted.mgz")
        
        threshold_rois(floc_words_tval_path, subsetted_floc_path, 3, True,
                       op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words"))
        
        
        # project floc-word ROIs to GMWMI
        roi_file = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words", 
                           hemi + ".floc-words.subsetted.thresholded3.mgz")
        
        wm_ROI_path = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words",
                              hemi + ".floc-words.subsetted.thresholded3.projected.nii.gz")
        
        proj_outpath = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words")
        
        surfROI_to_WM(roi_file, op.join(subj_dir, "mri",
                          "aseg.mgz"), hemi, subj, proj_outpath)

        intersect_roi_gmwmi(wm_ROI_path, gmwmi_path, True, proj_outpath)

        # concatenate with GMWMI-intersected VTC
        floc_words_gmwmi = op.join(subj_dir, "fyz", "anatomy", hemi+"-rois", "all", "floc-words",
                                   hemi+".floc-words.subsetted.thresholded3.projected.gmwmi_intersected.nii.gz")
        
        ips_gmwmi = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "kastner", 
                            hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.nii.gz")
        
        concat_volumes(ips_gmwmi, floc_words_gmwmi, "withFlocWordsRois", True, 
                       op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-words"))



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
            print("# " + "track-merged" + ", " + run + ", " + hemi + " #")
            print("#########")

            available_flocwords_rois = available_floc_rois(op.join(subj_dir, "fyz", "anatomy", hemi+"-rois", "all", 
                                                                   "floc-words", hemi+".floc-words.subsetted.mgz"))

            out_base = op.join(subj_dir, "fyz", run, hemi)
            floc_words_folder = op.join(subj_dir, "fyz", "anatomy",
                                 hemi+"-rois", "all", "floc-words")
            all_rois = op.join(floc_words_folder,
                               hemi+".Kastner2015.subsetted.projected.gmwmi_intersected.withFlocWordsRois.nii.gz")
            
            try:
                os.mkdir(op.join(out_base, "floc-words"))
            except FileExistsError:
                pass
              
            all_rois_out = op.join(out_base, "floc-words")
            all_rois_nodes = available_flocwords_rois[1] + [18, 19] # all floc_words_rois, IPS0, and IPS1
            all_rois_nodes = ", ".join(str(int(node)) for node in all_rois_nodes)

            intersect_tck_with_rois(tck, all_rois, all_rois_out, all_rois_nodes)


# Projecting fWMTs to surface
for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)
    T1_path = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata",
                      "ppdata", subj, "anat", "T1_0pt8_masked.nii.gz")

    for run in runs:
        for hemi in hemis:
            print("##########")
            print(f"# {subj} {run} track-merged {hemi} #")
            print("##########")

            tck_path = op.join(subj_dir, "fyz", run, hemi, "floc-words")
            os.chdir(tck_path)
            out = subprocess.check_output("echo node*-*.tck", shell=True)
            tck_list = str(out)[2:-3].split()

            for tck in tck_list:
                print("All " + tck)
                streamlines_to_surface(op.join(tck_path, tck), T1_path, tck_path, subj, hemi)

                intersect_surf_labels(op.join(tck_path, tck[:-4]+".endpoints.mgz"),
                                      op.join(subj_dir, "fyz", "anatomy", hemi+"-rois",
                                              "all", "kastner", hemi+".Kastner2015.subsetted.mgz"),
                                      True, tck_path, "IPS-intersected")
                
                de_intersect_surflabels(op.join(subj_dir, "label", hemi+".NonIPSManuallyDefined.label"),
                                         op.join(tck_path, tck[:-4]+".endpoints.mgz"),
                                         True, tck_path, "cleaned_withManualIPS")

