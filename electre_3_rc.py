import numpy as np

import gen_func as func


def concordance_index_a_b(alt_a, alt_b, weights, indif_value, pref_value):
    return func.concordance_index_a_b(alt_a, alt_b, weights, indif_value, pref_value)


def concordance_index_pref(perf_m, prof_m, weights, indif_value, pref_value):
    concordance_table = []

    for perf in range(len(perf_m)):
        concordance_table.append([])
        for prof in range(len(prof_m)):
            concordance_table[perf].append(
                concordance_index_a_b(perf_m[perf], prof_m[prof], weights, indif_value[prof], pref_value[prof]))

    return concordance_table


def concordance_index_prof(prof_m, perf_m, weights, indif_value, pref_value):
    concordance_table = []

    for prof in range(len(prof_m)):
        concordance_table.append([])
        for perf in range(len(perf_m)):
            concordance_table[prof].append(
                concordance_index_a_b(prof_m[prof], perf_m[perf], weights, indif_value[prof], pref_value[prof]))

    return concordance_table


def discordance_index_a_b(a, b, veto_value):
    for attr in range(len(a)):
        if b[attr] - a[attr] >= veto_value[attr]:
            return 0
    else:
        return 1


def discordance_index_perf(perf_m, prof_m, veto_value):
    discordance_table = []

    for perf in range(len(perf_m)):
        discordance_table.append([])
        for prof in range(len(prof_m)):
            discordance_table[perf].append(discordance_index_a_b(perf_m[perf], prof_m[prof], veto_value[prof]))

    return discordance_table


def discordance_index_prof(prof_m, perf_m, veto_value):
    discordance_table = []

    for prof in range(len(prof_m)):
        discordance_table.append([])
        for perf in range(len(perf_m)):
            discordance_table[prof].append(discordance_index_a_b(prof_m[prof], perf_m[perf], veto_value[prof]))

    return discordance_table


def credibility_index(concordance_matrix, discordance_matrix):
    credibility_matrix = [[concordance_matrix[a][b] * discordance_matrix[a][b] for b in
                           range(len(concordance_matrix[a]))] for a in range(len(concordance_matrix))]

    return credibility_matrix


def credibility_threshold_matrix(credibility, l):
    return np.array(np.array(credibility) >= l, dtype=bool)


def assessment(cred_perf, cred_prof, cred_thres_perf, cred_thres_prof, alternatives, classes):
    clusters = {}

    for alt in range(len(alternatives)):
        for pr in range(len(classes) - 2, 0, -1):
            if cred_thres_perf[alt][pr] and cred_perf[alt][pr + 1] > cred_prof[pr][alt]:
                clusters[alternatives[alt]] = [classes[pr + 1]]
                break
        else:
            clusters[alternatives[alt]] = [classes[0]]

        for pr in range(1, len(classes)):
            if cred_thres_prof[pr][alt] and cred_prof[pr - 1][alt] > cred_perf[alt][pr]:
                if clusters[alternatives[alt]][0] != classes[pr - 1]:
                    clusters[alternatives[alt]].append(classes[pr - 1])
                break

    return clusters


def method(performance_matrix, gain_loss, alternatives, classes, attributes, weights, profile_matrix, p, q, v, l):
    performance_matrix_normalized = func.perf_gain(performance_matrix, gain_loss)
    profile_matrix_normalized = func.perf_gain(profile_matrix, gain_loss)
    print(np.matrix(performance_matrix_normalized))
    print(np.matrix(profile_matrix_normalized))

    print("Concordance Matrix:")
    concordance_matrix_perf = concordance_index_pref(performance_matrix_normalized, profile_matrix_normalized, weights,
                                                     q, p)
    func.export_matrix_to_csv("results/concordance_rc_perf.csv", concordance_matrix_perf)
    print(np.round(concordance_matrix_perf, decimals=2))

    concordance_matrix_prof = concordance_index_prof(profile_matrix_normalized, performance_matrix_normalized, weights,
                                                     q, p)
    func.export_matrix_to_csv("results/concordance_rc_prof.csv", concordance_matrix_prof)
    print(np.round(concordance_matrix_prof, decimals=2))

    print()

    print("Discordance Matrix:")
    discordance_matrix_perf = discordance_index_perf(performance_matrix_normalized, profile_matrix_normalized, v)
    func.export_matrix_to_csv("results/discordance_rc_perf.csv", discordance_matrix_perf)
    print(np.round(discordance_matrix_perf, decimals=2))

    discordance_matrix_prof = discordance_index_prof(profile_matrix_normalized, performance_matrix_normalized, v)
    func.export_matrix_to_csv("results/discordance_rc_prof.csv", discordance_matrix_prof)
    print(np.round(discordance_matrix_prof, decimals=2))

    print()

    print("Credibility Matrix:")
    credibility_matrix_perf = credibility_index(concordance_matrix_perf, discordance_matrix_perf)
    func.export_matrix_to_csv("results/credibility_rc_perf.csv", credibility_matrix_perf)
    print(np.round(np.matrix(credibility_matrix_perf)))

    credibility_matrix_prof = credibility_index(concordance_matrix_prof, discordance_matrix_prof)
    func.export_matrix_to_csv("results/credibility_rc_prof.csv", credibility_matrix_prof)
    print(np.round(np.matrix(credibility_matrix_prof)))

    print()

    print("Credibility Threshold")
    credibility_threshold_perf = credibility_threshold_matrix(credibility_matrix_perf, l)
    func.export_matrix_to_csv("results/credibility_rc_threshold_perf.csv", credibility_threshold_perf)
    print(np.matrix(credibility_threshold_perf))

    credibility_threshold_prof = credibility_threshold_matrix(credibility_matrix_prof, l)
    func.export_matrix_to_csv("results/credibility_rc_threshold_prof.csv", credibility_threshold_prof)
    print(np.matrix(credibility_threshold_prof))

    print()

    print("Assessment")
    clusters = assessment(credibility_matrix_perf, credibility_matrix_prof, credibility_threshold_perf,
                          credibility_threshold_prof, alternatives, classes)

    with open('results/electre_3_rc_assessment.txt', 'w') as f:
        for key, value in clusters.items():
            print(key + ": " + np.str(value))
            f.write(f"{key}: {np.str(value)}\n")
