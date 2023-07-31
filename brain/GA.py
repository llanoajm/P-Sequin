import random

class Domain:
    def __init__(self, name, sequence) -> None:
        self.name = name
        self.sequence = sequence
        self.complement = '\'' in name

class Strand:
    def __init__(self, strand_domains) -> None:
        self.domains_in_strand = strand_domains
        # Construct the strand sequence with the 3' Poly-T overhang
        self.sequence = "".join([domain.sequence for domain in strand_domains]) + "TTT"

    def __str__(self):
        return self.sequence

def generate_random_sequence(length):
    return ''.join(random.choice('ACGT') for _ in range(length))

def is_palindromic(sequence):
    return sequence == sequence[::-1]

def compute_complement(sequence):
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement_map[base] for base in sequence)

generated_sequences = set()

def generate_unique_domain_and_complement(length):
    while True:
        sequence = generate_random_sequence(length)
        if not is_palindromic(sequence) and sequence not in generated_sequences:
            complement = compute_complement(sequence)
            generated_sequences.add(sequence)
            generated_sequences.add(complement)
            return sequence, complement

domains = []
strands = []

def create_domains():
    name = input("Enter domain name (without complement sign): ")
    length = int(input("Enter domain length: "))
    
    sequence, complement_sequence = generate_unique_domain_and_complement(length)
    
    domain = Domain(name, sequence)
    domains.append(domain)
    
    complement_domain = Domain(name + '\'', complement_sequence)
    domains.append(complement_domain)

    print(f"Generated unique sequence for {name}: {sequence}")
    print(f"Generated complementary sequence for {name}\': {complement_sequence}")

def create_strands():
    print("Separate each domain with a space:")
    structure = input().split()
    strand_domains = [next(domain for domain in domains if domain.name == name) for name in structure]
    strand = Strand(strand_domains)
    strands.append(strand)
    print(f"Generated strand: {strand}")

if __name__ == "__main__":
    print("Enter number of domains (excluding complements): ")
    domains_num = int(input())
    for _ in range(domains_num):
        create_domains()
    
    print("Would you like to create strands? (yes/no)")
    if input().lower() == 'yes':
        print("Enter number of strands:")
        strands_num = int(input())
        for _ in range(strands_num):
            create_strands()
