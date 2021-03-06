from joblib import load

matrix_shape = load('matrix_shape_mscpyr')
window_position = 0
window_step = 10_000_000
window_length_for_calibration = 4_000_000
min_level_treshold = 0
max_level_treshold = 0
peak_minimal_distance = 50
sample_rate = 2_000_000
matrix_treshold_probability = 0.85
fibre_treshold_probability = 0.95
fibre_bottom_freq_location = 50000
fibre_top_freq_location = 75000
matrix_bottom_freq_location = 200000
matrix_top_freq_location = 400000
comments_in_header_number_of_lines = 9
clustering_window = 10_000_000
number_of_clusters = 2
