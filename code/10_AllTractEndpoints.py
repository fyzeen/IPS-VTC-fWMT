from utils.system_utils import *
from utils.surface_label_utils import *
from utils.anatomy_utils import *
from utils.diffusion_utils import *
from utils.streamline_to_surface_utils import *
import numpy as np
import os
import os.path as op

subjects_dir = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/data/freesurfer"
#subjects_list = ["subj01", "subj02", "subj03", "subj04", "subj05", "subj06", "subj07", "subj08"]
#hemis = ["lh", "rh"]
#runs = ["run1", "run2"]
tck_types = ["track-merged"]
subjects_list = ["subj01"]
runs = ["run1"]
hemis = ["lh"]


# Extracting the streamlines from connectome/assignments
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

                if tck_type == "vof":
                    tck = op.join(subj_dir, "fyz", "anatomy", "diffusion", run, tck_type+".tck")
                else:
                    if run == "run1":
                        temp = "run_1"
                    else:
                        temp = "run_2"
                    tck = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata_diffusion/ppdata", subj, 
                                  temp, "track", tck_type + ".tck")
                    
                    
                for thresh in ["t>3"]:
                    print("#########")
                    print("# " + tck_type + ", " + run + ", " + thresh + " #")
                    print("#########")
                    
                    rois_base = op.join(subj_dir, "fyz", "anatomy", hemi+"-rois", "all", "kastner+floc", thresh)
                    out_base = op.join(subj_dir, "fyz", run, hemi)

                    available_flocfaces_rois = available_floc_rois(op.join(subj_dir, "fyz", "anatomy", 
                                                                           hemi+"-rois", "all", "floc-faces", "t>0", 
                                                                           hemi+".floc-faces.subsetted.mgz"))
                    ips_rois = [18, 19, 20, 21]
                    
                    all_rois = op.join(rois_base, hemi+".Kastner2015.subsetted.projected.gmwmi_intersected.withVTC.nii.gz")
                    all_rois_out = op.join(out_base, "all", thresh, tck_type)
                    all_rois_nodes = available_flocfaces_rois[1] + ips_rois
                    
                    for roi in all_rois_nodes:
                        find_tracts_intersecting_with_node(tck, all_rois, all_rois_out, str(int(roi)))

                       
# Projecting streamlines to surface                  
thresh = "t>3"

print("######################################")
print("")
print("####### PROJECTING STREAMLINES #######")
print("")
print("######################################")

for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)
    T1_path = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata",
                      "ppdata", subj, "anat", "T1_0pt8_masked.nii.gz")

    for run in runs:
        for hemi in hemis:
            for tck_type in tck_types:
                print("##########")
                print(f"# {subj} {run} {tck_type} {hemi} #")
                print("##########")
                
                available_flocfaces_rois = available_floc_rois(op.join(subj_dir, "fyz", "anatomy", 
                                                                           hemi+"-rois", "all", "floc-faces", "t>0", 
                                                                           hemi+".floc-faces.subsetted.mgz"))
                ips_rois = [18, 19, 20, 21]
                
                all_rois_nodes = available_flocfaces_rois[1] + ips_rois
                
                for roi in all_rois_nodes:
                    print(f"Projecting node{str(int(roi))}.tck to surface")
                    tck_path = op.join(subj_dir, "fyz", run, hemi, "all", thresh, tck_type)
                    streamlines_to_surface(op.join(tck_path, f"node{str(int(roi))}.tck"), T1_path, tck_path, subj, hemi)
                    
                    
                