from utils.system_utils import *
from utils.surface_label_utils import *
from utils.anatomy_utils import *
import numpy as np
import os.path as op

subjects_dir = "/Applications/freesurfer/7.3.2/subjects"
# subjects_list = ["subj01", "subj02", "subj03", "subj04", "subj05", "subj06", "subj07", "subj08", "subj09", "subj10"]
subjects_list = ["subj01", "subj02"]
hemis = ["lh", "rh"]

floc_faces_labels = {1: "OFA", 2: "FFA1", 3: "FFA2"}
kastner_atlas_labels = {18: "IPS0", 19: "IPS1", 20: "IPS2", 21: "IPS3"}

for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)

    # Define GMWMI for whole brain
    '''
    define_gmwmi(subj_dir, op.join(subj_dir, "fyz", "anatomy", "volumes"))
    
    unbinarized_gmwmi_path = op.join(
        subj_dir, "fyz", "anatomy", "volumes", "gmwmi.nii.gz")
    binarize_gmwmi(unbinarized_gmwmi_path, True,
                   op.join(subj_dir, "fyz", "anatomy", "volumes"))
    '''
    gmwmi_path = op.join(subj_dir, "fyz", "anatomy",
                         "volumes", "gmwmi.binarized.nii.gz")

    for hemi in hemis:

        floc_rois_path = op.join(subj_dir, "label", hemi + ".floc-faces.mgz")
        floc_faces_tval_path = op.join(
            subj_dir, "label", hemi + ".flocfacestval.mgz")
        kastner_rois_path = op.join(
            subj_dir, "label", hemi + ".Kastner2015.mgz")

        # Determine floc-faces ROIs available for subject
        available_rois = available_floc_rois(floc_rois_path)
        '''
        # Subset and threshold all ROIs #
        # subset kastner atlas
        subset_rois(np.array([18.0, 19.0, 20.0, 21.0]), kastner_rois_path, ".mgz", True,
                    out_path=op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "kastner"))

        # subset and threshold floc-faces
        subset_rois(available_rois[1], floc_rois_path,
                    ".mgz", True, subsetted_floc_path)

        subsetted_floc_path = op.join(
            subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-faces", "t>0", hemi + ".floc-faces.subsetted.mgz")

        threshold_rois(floc_faces_tval_path, subsetted_floc_path, 2, True,
                       op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-faces", "t>2"))
        threshold_rois(floc_faces_tval_path, subsetted_floc_path, 3, True,
                       op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-faces", "t>3"))

        # Project all floc-faces ROIs into WM and intersect all ROIs with GMWMI

        for i, thresh in enumerate(["t>0", "t>2", "t>3"]):
            if i == 0:
                roi_file = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-faces",
                                   thresh, hemi+".floc-faces.subsetted.mgz")
                wm_ROI_path = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-faces",
                                      thresh, hemi + ".floc-faces.subsetted.projected.nii.gz")

            else:
                roi_file = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-faces",
                                   thresh, hemi+f".floc-faces.subsetted.thresholded{i+1}.mgz")
                wm_ROI_path = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "floc-faces",
                                      thresh, hemi + f".floc-faces.subsetted.thresholded{i+1}.projected.nii.gz")

            proj_outpath = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois",
                                   "all", "floc-faces", thresh)


            surfROI_to_WM(roi_file, op.join(subj_dir, "mri", "aseg.mgz"), hemi, subj, proj_outpath)

            intersect_roi_gmwmi(wm_ROI_path, gmwmi_path, True, proj_outpath)


        # Projet all IPS (Kastner) ROIs into WM and intersect with GMWMI
        kastner_subsetted_rois_path = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois",
                                              "all", "kastner", hemi + ".Kastner2015.subsetted.mgz")

        kastner_proj_outpath = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois",
                                       "all", "kastner")

        surfROI_to_WM(kastner_subsetted_rois_path, op.join(subj_dir, "mri", "aseg.mgz"),
                      hemi, subj, kastner_proj_outpath)

        kastner_subsetted_projected_path = op.join(subj_dir, "fyz", "anatomy", hemi + "-rois", "all", "kastner",
                                                   hemi + ".Kastner2015.subsetted.projected.nii.gz")
        intersect_roi_gmwmi(kastner_subsetted_projected_path, gmwmi_path,
                            True, kastner_proj_outpath)
        '''
        # put gmwmi-intersected and surface label of each individual floc and kastner ROI into individual ROI folders
        '''
        for roi in available_rois[1]:
            for i, thresh in enumerate(["t>0", "t>2", "t>3"]):
                in_path = op.join(subj_dir, "fyz", "anatomy",
                                  hemi + "-rois", "all", "floc-faces", thresh)
                out_path = op.join(subj_dir, "fyz", "anatomy",
                                   hemi + "-rois", floc_faces_labels[roi], thresh)
                if i == 0:
                    subset_rois([roi], op.join(in_path, hemi + ".floc-faces.subsetted.mgz"),
                                ".mgz", True, out_path, floc_faces_labels[roi])
                    subset_rois([roi], op.join(in_path, hemi + ".floc-faces.subsetted.projected.gmwmi_intersected.nii.gz"),
                                ".nii.gz", True, out_path, floc_faces_labels[roi])
                else:
                    subset_rois([roi], op.join(in_path, hemi + f".floc-faces.subsetted.thresholded{i+1}.mgz"),
                                ".mgz", True, out_path, floc_faces_labels[roi])
                    subset_rois([roi], op.join(in_path, hemi + f".floc-faces.subsetted.thresholded{i+1}.projected.gmwmi_intersected.nii.gz"),
                                ".nii.gz", True, out_path, floc_faces_labels[roi])
            
        for i in [18.0, 19.0, 20.0, 21.0]:
            in_path = op.join(subj_dir, "fyz", "anatomy",
                              hemi + "-rois", "all", "kastner")
            out_path = op.join(subj_dir, "fyz", "anatomy",
                               hemi + "-rois", kastner_atlas_labels[i])
            subset_rois([i], op.join(in_path, hemi+".Kastner2015.subsetted.mgz"),
                        ".mgz", True, out_path, kastner_atlas_labels[i])
            subset_rois([i], op.join(in_path, hemi+".Kastner2015.subsetted.projected.gmwmi_intersected.nii.gz"),
                        ".nii.gz", True, out_path, kastner_atlas_labels[i])
        
        # binarize IPS (all) and floc (all) ROIs
        for i, thresh in enumerate(["t>0", "t>2", "t>3"]):
            directory = op.join(subj_dir, "fyz", "anatomy",
                                hemi+"-rois", "all", "floc-faces", thresh)
            if i == 0:
                binarize_gmwmi(op.join(directory, hemi + ".floc-faces.subsetted.projected.gmwmi_intersected.nii.gz"),
                               True, directory)
            else:
                binarize_gmwmi(op.join(directory, hemi + f".floc-faces.subsetted.thresholded{i+1}.projected.gmwmi_intersected.nii.gz"),
                               True, directory)
        directory = op.join(subj_dir, "fyz", "anatomy",
                            hemi+"-rois", "all", "kastner")
        binarize_gmwmi(op.join(directory, hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.nii.gz"),
                       True, directory, binarize_to=18)
        '''
        # Concatenate VTC and IPS ROIs into one volume
        for i, thresh in enumerate(["t>0", "t>2", "t>3"]):
            vtc_dir = op.join(subj_dir, "fyz", "anatomy",
                              hemi+"-rois", "all", "floc-faces", thresh)
            ips_dir = op.join(subj_dir, "fyz", "anatomy",
                              hemi+"-rois", "all", "kastner")
            out_dir = op.join(subj_dir, "fyz", "anatomy",
                              hemi+"-rois", "all", "kastner+floc")
            if i == 0:
                concat_volumes(op.join(ips_dir, hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.nii.gz"),
                               op.join(
                                   vtc_dir, hemi + ".floc-faces.subsetted.projected.gmwmi_intersected.nii.gz"),
                               "withVTC", True, op.join(out_dir, thresh))
                concat_volumes(op.join(ips_dir, hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.binarized.nii.gz"),
                               op.join(
                                   vtc_dir, hemi + ".floc-faces.subsetted.projected.gmwmi_intersected.nii.gz"),
                               "withVTC", True, op.join(out_dir, thresh))
                concat_volumes(op.join(ips_dir, hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.nii.gz"),
                               op.join(
                                   vtc_dir, hemi + ".floc-faces.subsetted.projected.gmwmi_intersected.binarized.nii.gz"),
                               "withBinaryVTC", True, op.join(out_dir, thresh))
            else:
                concat_volumes(op.join(ips_dir, hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.nii.gz"),
                               op.join(
                                   vtc_dir, hemi+f".floc-faces.subsetted.thresholded{i+1}.projected.gmwmi_intersected.nii.gz"),
                               "withVTC", True, op.join(out_dir, thresh))
                concat_volumes(op.join(ips_dir, hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.binarized.nii.gz"),
                               op.join(
                                   vtc_dir, hemi+f".floc-faces.subsetted.thresholded{i+1}.projected.gmwmi_intersected.nii.gz"),
                               "withVTC", True, op.join(out_dir, thresh))
                concat_volumes(op.join(ips_dir, hemi + ".Kastner2015.subsetted.projected.gmwmi_intersected.nii.gz"),
                               op.join(
                                   vtc_dir, hemi+f".floc-faces.subsetted.thresholded{i+1}.projected.gmwmi_intersected.binarized.nii.gz"),
                               "withBinaryVTC", True, op.join(out_dir, thresh))
