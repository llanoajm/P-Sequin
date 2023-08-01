import random
import nupack as nu # only installed in /usr/local/bin/python3


def initialize_sequence(length):
    sequence = []
    for _ in range(length):
        sequence.append(random.choice(["A", "T", "C", "G"]))
    
    # TODO: Ensure 40-60% GC content and avoid palindromes and repeated sequences
    
    return sequence


def compute_stability(sequence):
    
    my_model = nu.Model(material='DNA')
    result = nu.pfunc([sequence], model=my_model)
    # Return the negative logarithm of the partition function as a measure of stability
    return -result[0] #.log_pfunc


def check_secondary_structures(sequence):
    
    my_model = nu.Model(material='DNA')
    result = nu.mfe([sequence], model=my_model)
    # Return the free energy of the MFE structure
    # Lower values (more negative) indicate more stable secondary structures
    return result[0].energy






# TODO
# establish all orthogonal relationships graph










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

