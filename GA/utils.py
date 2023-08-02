import random
import nupack as nu # installed on /usr/local/bin/python3, not on conda                     


def is_palindrome(seq):
    # Check if a DNA sequence is a palindrome.
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return all(complement[base] == seq[-i - 1] for i, base in enumerate(seq))

def initialize_sequence(length):
    MAX_TRIES = 1000
    tries = 0
    while tries < MAX_TRIES:
        sequence = [random.choice(["A", "T", "C", "G"]) for _ in range(length)]
        gc_content = sum(1 for base in sequence if base in ["G", "C"]) / length
        if 0.4 <= gc_content <= 0.6:
            palindrome = any(is_palindrome(sequence[i:i+length//2]) for i in range(length // 2))
            if not palindrome:
                return sequence
        tries += 1
    raise ValueError("Failed to generate sequence after {} tries.".format(MAX_TRIES))


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

