import subprocess
import os.path as op


def run_command(command):
    '''
    Runs command in command line using subprocess.run()

    Inputs
    ----------
    command: list
        List containing function name and all necessary arguments for a command

    Outputs
    ----------
    None
    '''

    return_code = subprocess.run(command).returncode
    if return_code != 0:
        command_string = " ".join(command)
        raise Exception(
            f"Command exited with return code: {return_code}. Could not run: {command_string}")
    return None


def write_nib_file(input_path, out_path, data, type, change_label):
    '''
    Takes a nibabel data object and writes a new file with modified data

    Inputs
    ----------
    input_path: str
        Path to original file

    out_path: str
        Path to output FOLDER (e.g., "usr/bin/hello/")

    data: nibabel object
        Data to be written into file

    type: str
        Type of data (vertex space vs volume); file type in which to be stored (i.e., .mgh, .mgz, .nii, or .nii.gz)

    change_label: str
        Short string to be concatentated with name of the original input file to indicate the changes made

    Outputs
    ----------
    Writes new file with modified data and name

    Returns None
    '''

    if type == ".nii.gz":
        cut = -7
    elif type == ".mgz" or type == ".mgh" or type == ".nii":
        cut = -4
    else:
        raise Exception("Invalid file type.")

    out_filename = op.basename(input_path)
    out_filename = out_filename[:cut] + f".{change_label}" + f"{type}"
    out_file = op.join(out_path, out_filename)
    print("Writing to: " + out_file)
    data.to_filename(out_file)

    return None
