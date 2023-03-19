% Subetting tracts to VOF using cleaned classification provided with NSD

% selecting tracts labeled as left VOF (58) or right VOF (59)
load("code/subj01_tests/classification-wholebrain-cleaned.mat");
subset = (classification.index == 58 | classification.index == 59);

% reading data
tracks = read_mrtrix_tracks("data/subj01/diffusion/track-merged.tck")
tracks.data = tracks.data(subset)

% subsetting the tracts, writing to file
write_mrtrix_tracks(tracks, 'data/subj01/diffusion/vof.tck')