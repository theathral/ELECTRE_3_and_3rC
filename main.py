import numpy as np

import electre_3
import electre_3_rc

if __name__ == '__main__':
    alternatives = open("given_data/countries.csv", "r", encoding='utf-8-sig').read().splitlines()  # Alternatives
    classes = ["Unacceptable Freedom", "Limited Freedom", "Neutral", "Acceptable Freedom", "Full Freedom"]  # Classes
    attributes = open('given_data/attributes.csv', "r", encoding='utf-8-sig').read().splitlines()  # Attributes
    weights = [0.03, 0.10, 0.05, 0.33, 0.10, 0.07, 0.13, 0.06, 0.03, 0.01, 0.07, 0.03]  # Weights
    performance_matrix = np.genfromtxt('given_data/performance_matrix.csv', delimiter=';', dtype=float,
                                       encoding='utf-8-sig')
    profile_matrix = [
        [20, 30, 30, 30, 20, 20, 20, 25, 25, 25, 20, 25],
        [40, 45, 40, 35, 30, 30, 30, 30, 30, 35, 30, 35],
        [50, 60, 50, 60, 55, 50, 50, 50, 50, 45, 45, 50],
        [70, 80, 75, 80, 75, 70, 75, 70, 70, 70, 75, 75],
        [85, 90, 85, 90, 90, 80, 90, 80, 80, 85, 90, 85]
    ]
    gain_loss = [1 for _ in range(len(attributes))]

    q = [50, 30, 35, 15, 25, 30, 20, 40, 45, 45, 25, 30]  # Indifference Threshold
    p = [55, 30, 35, 20, 30, 30, 25, 35, 35, 40, 25, 30]  # Preference Threshold
    v = [60, 70, 70, 85, 70, 60, 65, 55, 55, 50, 75, 70]  # Veto Threshold

    q_rc = [
        [20, 15, 15, 10, 15, 20, 15, 15, 20, 20, 15, 15],
        [20, 15, 15, 10, 15, 20, 15, 15, 20, 20, 15, 15],
        [20, 10, 10, 5, 10, 20, 10, 15, 20, 20, 10, 15],
        [20, 10, 10, 5, 10, 20, 10, 15, 20, 20, 10, 15],
        [20, 10, 10, 5, 10, 20, 10, 15, 20, 20, 10, 15]
    ]  # Indifference Thresholds
    p_rc = [
        [25, 20, 20, 15, 20, 25, 15, 20, 20, 20, 15, 20],
        [25, 20, 20, 15, 20, 25, 15, 20, 20, 20, 15, 20],
        [25, 15, 20, 15, 20, 20, 15, 25, 25, 20, 15, 15],
        [25, 15, 20, 15, 20, 20, 15, 25, 25, 20, 15, 15],
        [25, 15, 20, 15, 20, 20, 15, 25, 25, 20, 15, 15]
    ]  # Preference Thresholds
    v_rc = [
        [40, 30, 35, 30, 35, 35, 30, 35, 35, 40, 25, 30],
        [40, 30, 35, 30, 35, 35, 30, 35, 35, 40, 25, 30],
        [40, 30, 30, 25, 30, 35, 30, 40, 40, 40, 30, 35],
        [40, 30, 30, 25, 30, 35, 30, 40, 40, 40, 30, 35],
        [40, 30, 30, 25, 30, 35, 30, 40, 40, 40, 30, 35]
    ]  # Veto Thresholds

    l = 0.5  # Cut-Off Value
    l_rc = 0.5  # Cut-Off Value

    electre_3.method(performance_matrix, alternatives, gain_loss, p, q, v, weights, l)
    electre_3_rc.method(performance_matrix, gain_loss, alternatives, classes, attributes, weights, profile_matrix,
                        p_rc, q_rc, v_rc, l_rc)
