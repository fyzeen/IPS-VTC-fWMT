from utils.system_utils import *
import os.path as op


def intersect_tck_with_rois(tck_path,
                            gmwmi_rois_path,
                            out_path,
                            nodes_list,
                            search_type="-assignment_radial_search", search_dist="3",
                            forLiFESubsetting=False):
    '''
    This function intersects track files (.tck) with ROIs restricted to the gray-white matter interface
    ** Note: this function is largely based off of extract_tck_mrtrix() in fsub_extractor **

    Inputs
    ----------
    tck_path: str
        Path to tck file from which to extract streamlines that intersect with GMWMI of ROIs

    gmwmi_rois_path: str
        Path to volume with ROIs of interest (labeled with integers) restricted to GMWMI

    out_path: str
        Path to the FOLDER to write all file outputs

    nodes_list: str
        Comma-separated list as a string (e.g., "0,1,2,3") with all the nodes from which to extract streamlines

    search_type: str
        Type of search. All options described here: 
        https://mrtrix.readthedocs.io/en/dev/reference/commands/tck2connectome.html#structural-connectome-streamline-assignment-option

    search_dist: double
        Distance to search as defined in the MRtrix3 documentation. See search_type description.

    Outputs
    ----------
    Outputs connectome.txt and assignments.txt at specified location. Also outputs extracted .tck files with tracks that connect to
    each node in the list of nodes. 
    '''
    connectome_txt_path = op.join(out_path, "connectome.txt")
    assignments_txt_path = op.join(out_path, "assignments.txt")
    tck2connectome_command = ["tck2connectome",
                              tck_path,
                              gmwmi_rois_path,
                              connectome_txt_path,
                              search_type, search_dist,
                              "-out_assignments", assignments_txt_path, "-force"]
    run_command(tck2connectome_command)

    connectom2tck_prefix = op.join(out_path, "node")
    if forLiFESubsetting:
        connectome2tck_command = ["connectome2tck", tck_path,
                                  assignments_txt_path,
                                  connectom2tck_prefix,
                                  "-nodes", "1",
                                  "-keep_self", "-files", "single", "-force"]
    else:
        connectome2tck_command = ["connectome2tck", tck_path,
                                  assignments_txt_path,
                                  connectom2tck_prefix,
                                  "-nodes", nodes_list,
                                  "-files", "per_edge",
                                  "-exclusive", "-force"]
    run_command(connectome2tck_command)

    return None

def find_tracts_intersecting_with_node(tck_path,
                                       gmwmi_rois_path,
                                       out_path,
                                       node,
                                       search_type="-assignment_radial_search", search_dist="3"):
    '''
    This function intersects track files (.tck) with ROIs restricted to the gray-white matter interface
    ** Note: this function is largely based off of extract_tck_mrtrix() in fsub_extractor **
    
    **Was written to operate only AFTER connectome.txt and assignments.txt are created!

    Inputs
    ----------
    tck_path: str
        Path to tck file from which to extract streamlines that intersect with GMWMI of ROIs

    gmwmi_rois_path: str
        Path to volume with ROIs of interest (labeled with integers) restricted to GMWMI

    out_path: str
        Path to the FOLDER to write all file outputs

    node: str
        String (e.g., "0" or "1") with the node from which to extract streamlines

    search_type: str
        Type of search. All options described here: 
        https://mrtrix.readthedocs.io/en/dev/reference/commands/tck2connectome.html#structural-connectome-streamline-assignment-option

    search_dist: double
        Distance to search as defined in the MRtrix3 documentation. See search_type description.

    Outputs
    ----------
    Outputs connectome.txt and assignments.txt at specified location. Also outputs extracted .tck files wit ALL tracks that
    connect to a the specified node. 
    '''
    connectome_txt_path = op.join(out_path, "connectome.txt")
    assignments_txt_path = op.join(out_path, "assignments.txt")

    connectom2tck_prefix = op.join(out_path, "node")
    
    connectome2tck_command = ["connectome2tck", tck_path,
                              assignments_txt_path,
                              node, "-files", "per_node",
                              "-force"]
   
    run_command(connectome2tck_command)
    
    return None
        
    
