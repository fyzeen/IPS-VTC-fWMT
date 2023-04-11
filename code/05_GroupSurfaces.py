from utils.group_analysis_utils import *
from utils.streamline_to_surface_utils import *

subjects_dir = "/Applications/freesurfer/7.3.2/subjects"
subjects_list = ["subj01", "subj02", "subj03",
                 "subj04", "subj05", "subj06", "subj07", "subj08"]
runs = ["run1", "run2"]
hemis = ["lh", "rh"]
tck_types = ["vof", "track-merged"]
thresh = "t>3"


# THIS IS SOLELY FOR VISUALIZATION... this example is for visualizing FFA1 to IPS with track-merged surface maps
fsaverage_dir = op.join(subjects_dir, "fsaverage_fyz", "fyz", "FFA1ToIPS")
# hemispheres must be changed manually because this subprocess will not run mri_concat command as written.
hemi = "lh"
surfs_list = []
for subj in subjects_list:
    subj_dir = op.join(subjects_dir, subj)
    for run in runs:
        surf_path = op.join(subj_dir, "fyz", run, hemi, "VTCtoWholeIPS",
                            thresh, "track-merged")

        if op.exists(op.join(surf_path, "node2-18.endpoints.IPS-intersected.mgz")):
            normalize_streamlines_on_surf(
                op.join(surf_path, "node2-18.endpoints.IPS-intersected.mgz"), surf_path)

            surfs_list.append(
                op.join(surf_path, "node2-18.endpoints.IPS-intersected.normalized.mgz"))

# for some reason subprocess will not run the concatenation command. We can, however, run the commands directly in command line.
#   This code will, at the end, output the failed command. Copy and paste that into your command line to get the output.
concatenate_endpoint_surfs(
    surfs_list, subjects_list, fsaverage_dir, hemi)
