# all metrics are to be minimized

import random
import sys
sys.path.append('NUPACK/src/source')


def compute_stability(sequence):
    #lazy import bc there is a circular

    my_model = nu.Model(material='DNA')
    result = nu.pfunc([sequence], model=my_model)
    # Return the negative logarithm of the partition function as a measure of stability
    return float(-result[0]) #.log_pfunc
   


def check_secondary_structures(sequence):

    my_model = nu.Model(material='DNA')
    result = nu.mfe([sequence], model=my_model)
    # Return the free energy of the MFE structure
    # Lower values (more negative) indicate more stable secondary structures
    return result[0].energy



def check_if_palindrome(sequence):
    return float(sequence == sequence[::-1])

def check_gc_content(sequence):
    gc_content = sum(1 for base in sequence if base in ["G", "C"]) / len(sequence)
    return float(not (0.4 <= gc_content <= 0.6))





test_sequences = ["ATCG", "TATC", "GCTA", "TAGC"]

for seq in test_sequences:
    stability_result = check_gc_content(seq)
    print(f"Stability of {seq}: {stability_result}")




# TODO
# establish all orthogonal relationships graph
# factor in domain designs into first sequence initialization
# crossover null.
# propagation of mutations, high frequency. boost!


# def check_cross_hybridization(sequence, all_sequences):
#     # Compute pairwise binding energies with all other sequences
#     binding_energies = []
#     for other_seq in all_sequences:
#         if sequence != other_seq:
#             my_set = nupack.DesignSet(
#                 sequences=[sequence, other_seq],
#                 conditions=nupack.DefaultConditions
#             )
#             result = nupack.mfe(my_set)
#             binding_energies.append(result[0].energy)
    
#     # Return the most stable (lowest) binding energy
#     return min(binding_energies)

