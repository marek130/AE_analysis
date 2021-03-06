#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cupy
from tubes import Each
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from constants import window_length_for_calibration, window_position, \
    window_step, min_level_treshold, peak_minimal_distance, \
    max_level_treshold, matrix_shape, matrix_treshold_probability, \
    matrix_bottom_freq_location, matrix_top_freq_location, \
    fibre_treshold_probability, fibre_bottom_freq_location, \
    fibre_top_freq_location, peak_minimal_distance, sample_rate, comments_in_header_number_of_lines

signal = []
fibres_hits = []
matrix_hits = []


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


def set_start_point():
    global window_position, window_length_for_calibration
    window_position = window_length_for_calibration


def analyze_data():
    global window_position, window_step, signal, min_level_treshold, \
        max_level_treshold
    end = 0
    steps = (len(signal) // window_step) + 1
    for chunk in range(steps):
        print("Analyzing " + str(chunk) + " chunk from " + str(steps - 1))
        peaks = np.where((signal[window_position:window_position
                         + window_step] > max_level_treshold)
                         | (signal[window_position:window_position
                         + window_step] < min_level_treshold))[0]
        peaks = filter_peaks(peaks)
        for position_of_peak in peaks:
            if window_position + position_of_peak > end:
                end = analyze_peak(position_of_peak)
        window_position += window_step


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


def normalize_freqs(f):
    return (np.abs(f) - np.min(np.abs(f))) / (np.max(np.abs(f))
            - np.min(np.abs(f)))


def cosine_of_vectors(a, b):
    num = (a * b).sum()
    da = (a * a).sum()
    db = (b * b).sum()
    return num / np.sqrt(da * db)


def analyze_peak(peak_position):
    global window_position, signal, matrix_shape, signal, fibres_hits, \
        matrix_hits, sample_rate, matrix_treshold_probability, \
        fibre_treshold_probability, fibre_bottom_freq_location, \
        fibre_top_freq_location, matrix_bottom_freq_location, \
        matrix_top_freq_location
    (start, end) = get_start_and_end_for_peak(window_position
            + peak_position)
    pad_size = (sample_rate - 1 - len(signal[window_position
                + peak_position - start:window_position + peak_position
                + end + 1])) // 2
    freqs_spectrum_of_peak = \
        cupy.fft.rfft(cupy.asarray(np.pad(signal[window_position
                      + peak_position - start:window_position
                      + peak_position + end + 1], pad_size)))
    freqs_spectrum_of_peak = normalize_freqs(freqs_spectrum_of_peak)
    freqs_spectrum_of_peak = cupy.asnumpy(freqs_spectrum_of_peak)  # Convert cupy array into numpy array
    if len(np.where(np.abs(freqs_spectrum_of_peak[fibre_bottom_freq_location:fibre_top_freq_location])
           > fibre_treshold_probability)[0]) > 0:  # FIBRE
        fibres_hits.append(window_position + peak_position)
    probability = \
        cosine_of_vectors(matrix_shape[matrix_bottom_freq_location:matrix_top_freq_location],
                          freqs_spectrum_of_peak[matrix_bottom_freq_location:matrix_top_freq_location])
    if probability > matrix_treshold_probability:  # MATRIX
        matrix_hits.append(window_position + peak_position)
    return end + window_position + peak_position


def make_graphs(file_name):
    global matrix_hits, fibres_hits
    print("Creating final graph")
    cummulative_counter_matrix = []
    cummulative_counter_fibres = []
    
    for i,v in enumerate(matrix_hits):
        cummulative_counter_matrix.append(i + 1)

    for i,v in enumerate(fibres_hits):
        cummulative_counter_fibres.append(i + 1)

    plt.figure()
    plt.plot(matrix_hits, cummulative_counter_matrix)
    plt.plot(fibres_hits, cummulative_counter_fibres)
    plt.savefig(file_name + "-" + str(datetime.now()) + ".png")
    plt.close()
    print("Graph created")

def init():
    load_data(sys.argv[1])
    set_tresholds()
    set_start_point()
    analyze_data()
    make_graphs(sys.argv[1])


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Missing file name!")
    else:
        init()
