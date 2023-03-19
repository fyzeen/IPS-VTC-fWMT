from utils.system_utils import *
import os.path as op
import os


def concatenate_endpoint_surfs(surfs_list, freesurfer_subjects_list, out_path, hemi):
    subjects_list_with_repeats = [
        ele for ele in freesurfer_subjects_list for i in range(2)]

    for i, surf_path in enumerate(surfs_list):
        freesurfer_subj = subjects_list_with_repeats[i]

        file_name = surf_path.replace(
            ".mgz", f".fsaverage.{freesurfer_subj}_{hemi}{i}.mgz")
        file_name = op.basename(file_name)
        out_file = op.join(out_path, file_name)

        surf2fsaverage_command = ["mri_surf2surf",
                                  "--srcsurfval", surf_path,
                                  "--srcsubject", freesurfer_subj,
                                  "--trgsubject", "fsaverage",
                                  "--trgsurfval", out_file,
                                  "--hemi", hemi]

        run_command(surf2fsaverage_command)

    os.chdir(out_path)
    concat_mris = op.join(out_path, f"*.fsaverage.*.mgz")
    out_file = op.join(out_path, f"fsaverage.concatenated.{hemi}.mgz")
    concat_command = ["mri_concat",
                      "--i", concat_mris,
                      "--o", out_file,
                      "--mean"]
    run_command(concat_command)

    return None
