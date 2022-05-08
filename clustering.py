from joblib import dump
from init import normalize_freqs
from tubes import Each
from sklearn.cluster import KMeans
from constants import window_length_for_calibration, min_level_treshold, max_level_treshold, clustering_window, number_of_clusters, sample_rate, peak_minimal_distance, max_level_treshold, min_level_treshold, comments_in_header_number_of_lines
import cupy
import sys
import numpy as np
import matplotlib.pyplot as plt

signal = []
clusters = None

def load_data(file):
    global signal
    print('Loading data from file: ' + file)
    f = file
    tmp = Each([f]).read_files().split().skip(comments_in_header_number_of_lines).skip_if(lambda x: \
            x.len().equals(0)).to(int)
    signal = tmp.ndarray(estimated_rows=150_000_000)
    print('Data have been loaded successfully')


def set_tresholds():
    global signal, window_length_for_calibration, min_level_treshold, \
        max_level_treshold
    min_level_treshold = np.min(signal[:window_length_for_calibration])
    max_level_treshold = np.max(signal[:window_length_for_calibration])

def filter_peaks(peaks):
    global peak_minimal_distance
    # Remove peaks which are not at a sufficient distance
    if len(peaks) < 2:  # If there is only one peak return it
        return peaks
    result = [peaks[0]]
    for i in range(1, len(peaks)):
        if np.abs(result[-1] - peaks[i]) > peak_minimal_distance:  # Two peaks need to have minimal_distance
            result.append(peaks[i])
    return result


def get_start_and_end_for_peak(peak_position):
    global peak_minimal_distance, signal
    start = 0
    if peak_position > peak_minimal_distance:
        start = 1
        nS = 0
        while nS != peak_minimal_distance:
            if min_level_treshold <= signal[peak_position - start] \
                <= max_level_treshold:
                nS += 1
            start += 1
    end = 1
    nE = 0
    while nE != peak_minimal_distance:
        if min_level_treshold <= signal[peak_position + end] \
            <= max_level_treshold:
            nE += 1
        end += 1
    return (start, end)

def find_clusters():
	global signal, clusters
	finalResult = []
	peaks = np.where((signal[window_length_for_calibration : window_length_for_calibration + clustering_window] > max_level_treshold ) | (signal[window_length_for_calibration : window_length_for_calibration + clustering_window] < min_level_treshold ))[0]
	peaks = filter_peaks(peaks)
	for p in peaks:
		finalResult.append(cupy.asnumpy(analyze_peak(p)))
	clusters = KMeans(n_clusters=number_of_clusters).fit(finalResult)


def analyze_peak(p):
	global signal
	start, end = get_start_and_end_for_peak(p)
	pad_size = (sample_rate - 1 - len(signal[p - start: p + end + 1])) // 2
	freqs = cupy.fft.rfft(cupy.asarray(np.pad(signal[p - start: p + end + 1], pad_size)))
	return normalize_freqs(freqs)



def save_clusters(file_name):
        global clusters
        for i in range(number_of_clusters):
                dump(clusters.cluster_centers_[i], file_name + '-cluster' + str(i))
                plt.figure()
                plt.plot(clusters.cluster_centers_[i])
                plt.savefig(file_name + '-cluster' + str(i) + '.png')
                plt.close()

def init():
    load_data(sys.argv[1])
    set_tresholds()
    find_clusters()
    save_clusters(sys.argv[1])


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Missing file name!")
    else:
        init()
