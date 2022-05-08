from joblib import dump
from init import load_data, normalize_freqs, get_start_and_end_for_peak, filter_peaks
from sklearn.cluster import Kmeans
from constants import window_length_for_calibration, min_level_treshold, max_level_treshold, clustering_window, number_of_clusters, sample_rate
import cupy
import numpy as np
import matplotlib.pyplot as plt

signal = []
clusters = None

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
                dump(clusters[i], file_name + '-cluster' + str(i))
                plt.figure()
                plt.plot(clusters[i])
                plt.savefig(file_name + '-cluster' + str(i) + '.png')
                plt.close()

def init():
    load_data(sys.argv[1])
    find_clusters()
    save_clusters(sys.argv[1])


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Missing file name!")
    else:
        init()
