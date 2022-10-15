import numpy as np


def export_matrix_to_csv(filename, matrix):
    np.savetxt(filename, matrix, fmt='%.1f', delimiter=";")


def perf_gain(perf_matrix, attribute_gain_loss):
    matrix = []

    for alt in range(len(perf_matrix)):
        matrix.append([])

        for attr in range(len(perf_matrix[0])):
            matrix[alt].append(perf_matrix[alt][attr] * attribute_gain_loss[attr])

    return matrix


def concordance_index_a_b(alt_a, alt_b, weights, indif_value, pref_value):
    idx_value = 0

    for attr in range(len(alt_a)):
        if alt_a[attr] + indif_value[attr] >= alt_b[attr]:
            idx_value += weights[attr]
        elif alt_a[attr] + pref_value[attr] > alt_b[attr]:
            idx_value += weights[attr] \
                         * ((pref_value[attr] + alt_a[attr] - alt_b[attr]) / (pref_value[attr] - indif_value[attr]))

    return idx_value
