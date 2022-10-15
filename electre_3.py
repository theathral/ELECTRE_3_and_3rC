import numpy as np

import gen_func as func


def concordance_index_a_b(alt_a, alt_b, weights, indif_value, pref_value):
    return func.concordance_index_a_b(alt_a, alt_b, weights, indif_value, pref_value)


def concordance_index(p_m, weights, indif_value, pref_value):
    concordance_table = []

    for a in range(len(p_m)):
        concordance_table.append([])
        for b in range(len(p_m)):
            concordance_table[a].append(concordance_index_a_b(p_m[a], p_m[b], weights, indif_value, pref_value))

    return concordance_table


def discordance_index_a_b(p_m_a, p_m_b, pref_value, veto_value):
    idx_value = []

    for attr in range(len(p_m_a)):
        if p_m_a[attr] + pref_value[attr] >= p_m_b[attr]:
            idx_value.append(0)
        elif p_m_a[attr] + veto_value[attr] <= p_m_b[attr]:
            idx_value.append(1)
        else:
            idx_value.append((p_m_b[attr] - p_m_a[attr] - pref_value[attr]) / (veto_value[attr] - pref_value[attr]))

    return idx_value


def discordance_index(p_m, pref_value, veto_value):
    discordance_table = []

    for a in range(len(p_m)):
        discordance_table.append([])
        for b in range(len(p_m)):
            discordance_table[a].append(discordance_index_a_b(p_m[a], p_m[b], pref_value, veto_value))

    return discordance_table


def credibility_index_a_b(concordance, discordance):
    idx_value = concordance

    if concordance >= max(discordance):
        return idx_value

    for dis in discordance:
        if concordance < dis:
            idx_value *= (1 - dis) / (1 - concordance)

    return idx_value


def credibility_index(concordance_matrix, discordance_matrix):
    credibility_table = []

    for a in range(len(concordance_matrix[0])):
        credibility_table.append([])

        for b in range(len(concordance_matrix[0])):
            credibility_table[a].append(credibility_index_a_b(concordance_matrix[a][b], discordance_matrix[a][b]))

    return credibility_table


def rank(credibility_matrix, l, alternatives):
    score_table = [0 for _ in range(len(credibility_matrix))]

    for a in range(len(credibility_matrix)):
        for b in range(len(credibility_matrix[a])):
            if credibility_matrix[a][b] >= l:
                score_table[a] += 1
                score_table[b] -= 1

    return dict(zip(alternatives, score_table))


def method(performance_matrix, alternatives, gain_loss, p, q, v, weights, l):
    performance_matrix_normalized = func.perf_gain(performance_matrix, gain_loss)

    print("Concordance Matrix:")
    concordance_matrix = concordance_index(performance_matrix_normalized, weights, q, p)
    func.export_matrix_to_csv("results/concordance.csv", concordance_matrix)
    print(np.round(concordance_matrix, decimals=2))

    print()

    print("Discordance Matrix:")
    discordance_matrix = discordance_index(performance_matrix_normalized, p, v)
    with open('results/discordance.csv', 'w') as f:
        for row in discordance_matrix:
            for col in row:
                print(np.round(col, decimals=2), end="")
                f.write(f"{np.str(np.round(col, decimals=2))};")
            print()
            f.write(f"\n")

    print()

    print("Credibility Matrix:")
    credibility_matrix = credibility_index(concordance_matrix, discordance_matrix)
    func.export_matrix_to_csv("results/credibility.csv", credibility_matrix)
    print(np.round(np.matrix(credibility_matrix), decimals=2))

    print()

    ranking = rank(credibility_matrix, l, alternatives)
    with open('results/electre_3_ranking.txt', 'w') as f:
        for (i, w) in zip(range(len(ranking)), sorted(ranking, key=ranking.get, reverse=True)):
            print(str(i + 1) + ": " + str(w) + " (" + str(ranking[w]) + ")")
            f.write(f"{i+1}: {w} ({ranking[w]})\n")
