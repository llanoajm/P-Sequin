import random

class Domain:
    def __init__(self, name, sequence) -> None:
        self.name = name
        self.sequence = sequence
        self.complement = '*' in name
        

class Strand:
    def __init__(self, strand_domains) -> None:
        self.domains_in_strand = strand_domains
        self.sequence = "".join([domain.sequence for domain in strand_domains])
        #if with_overhang:
        #   self.sequence += "TTT" # add this only after final generation.

def generate_random_sequence(length):
    return ''.join(random.choice('ACGT') for _ in range(length))

def compute_complement(sequence):
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement_map[base] for base in sequence)

generated_sequences = set()

def generate_unique_domain_and_complement(length):
    while True:
        sequence = generate_random_sequence(length)
        if sequence not in generated_sequences:
            complement = compute_complement(sequence)
            generated_sequences.add(sequence)
            generated_sequences.add(complement)
            return sequence, complement
        
def represent_complex(strands, dot_paren):
    strands_list = strands.split(',')
    representation = ""
    
    # Example logic for processing the strands and dot-paren notation
    # This logic can be customized based on the exact structure and requirements
    for i, char in enumerate(dot_paren):
        if char == '.':
            representation += strands_list[i % len(strands_list)] + " "
        elif char == '(':
            representation += "(" + strands_list[i % len(strands_list)] + " "
        elif char == ')':
            representation += strands_list[i % len(strands_list)] + ") "
    
    return representation

        

        
# 40-60% GC 
# clamp domains.
# 3' Poly-T overhang (primer-template mismatch)               
# avoid palindromes and repeated sequences.
# minimize LCS.
# 40 - 60 % GC (high melting point)
# BS3 enzyme
# peppercorn to show structure formation.