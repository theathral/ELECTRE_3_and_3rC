import numpy as np

import electre_3
import electre_3_rc

if __name__ == '__main__':
    alternatives = open("given_data/countries.csv", "r", encoding='utf-8-sig').read().splitlines()  # Alternatives
    classes = ["Repressed", "Mostly Unfree", "Moderated Free", "Mostly Free", "Free"]  # Classes
    attributes = open('given_data/attributes.csv', "r", encoding='utf-8-sig').read().splitlines()  # Attributes
    weights = [1 / len(attributes) for _ in range(len(attributes))]  # Weights
    performance_matrix = np.genfromtxt('given_data/performance_matrix.csv', delimiter=';', dtype=float,
                                       encoding='utf-8-sig')
    profile_matrix = [[i for _ in range(len(attributes))] for i in [35, 50, 60, 70, 80]]  # Profiles
    gain_loss = [1 for _ in range(len(attributes))]

    q = [20 for _ in range(len(alternatives))]  # Indifference Threshold
    p = [30 for _ in range(len(alternatives))]  # Preference Threshold
    v = [70 for _ in range(len(alternatives))]  # Veto Threshold

    q_rc = [[20 for _ in range(len(attributes))] for _ in range(len(classes))]  # Indifference Thresholds
    p_rc = [[30 for _ in range(len(attributes))] for _ in range(len(classes))]  # Preference Thresholds
    v_rc = [[60 for _ in range(len(attributes))] for _ in range(len(classes))]  # Veto Thresholds

    l = 0.1  # Cut-Off Value
    l_rc = 0.6  # Cut-Off Value

    # electre_3.method(performance_matrix, alternatives, gain_loss, p, q, v, weights, l)
    electre_3_rc.method(performance_matrix, gain_loss, alternatives, classes, attributes, weights, profile_matrix,
                        p_rc, q_rc, v_rc, l_rc)
