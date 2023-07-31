import random
import string

# clamp domains.
# 3' Poly-T overhang (primer-template mismatch)
# avoid palindromes and repeated sequences.
# minimize LCS.
  
class Domain:
    length = 0
    name = ""
    complement = False
    def __init__(self, name, length) -> None:
        self.name = name
        self.length = length
        self.complement = '\'' in name
        pass
    
class Strand:
    domains_in_strand = []
    def __init__(self, strand_domains) -> None:
        self.domains_in_strand = strand_domains
        pass
    # d and o attributes defined after the complexes are specified
   
    
domains = []
strands = []
complexes = []

def create_domains():
    name = input("Enter domain name: ")
    length = int(input("Enter domain length: "))
    domain = Domain(name, length)
    
    if '\'' in name:  # If it's a complement
        original_domain_name = name.replace('\'', '')
        index_of_original = next(i for i, d in enumerate(domains) if d.name == original_domain_name)
        # Insert the complement right after the original domain
        domains.insert(index_of_original + 1, domain)
    else:
        domains.append(domain)

    
def create_strands():
    print("Separate each domain with a space")
    structure = input()
    strand_domains = structure.split()
    current_strand = Strand(strand_domains)


#design each domain such that 1) it is complementary to complementary ones 2) the strands which it occupies minimize symmetry 3) they are unique 4) there is a 3' Poly-T overhang for every strand.
print("Enter number of domains: ")
domains_num = int(input())
for _ in range(domains_num):
    create_domains()
    

# Simulated input for demonstration purposes
simulated_inputs = {
    "domain_names": ["A", "B", "C"],
    "domain_lengths": [5, 6, 7]
}

def create_domains_simulated():
    for idx, name in enumerate(simulated_inputs["domain_names"]):
        length = simulated_inputs["domain_lengths"][idx]
        
        # Generate domain and its complement
        sequence, complement_sequence = generate_domain_and_complement(length)
    
        # Create domain
        domain = Domain(name, sequence)
        domains.append(domain)
    
        # Create complement domain
        complement_domain = Domain(name + '\'', complement_sequence)
        domains.append(complement_domain)

        print(f"Generated sequence for {name}: {sequence}")
        print(f"Generated complementary sequence for {name}\': {complement_sequence}")

# Create domains using simulated input
create_domains_simulated()
