from NSGA import *
from utils import *


def generate():
    domains_num = 3
    domain_names = ["D1", "D2", "D3"]
    domain_lengths = [4,4,4]
    domains = []
    for i in range(domains_num):
        name = domain_names[i]
        length = domain_lengths[i]
        sequence, complement_sequence = generate_unique_domain_and_complement(length)
        domain = Domain(name, sequence)
        domains.append(domain)
        complement_domain = Domain(name + '\'', complement_sequence)
        domains.append(complement_domain)

    domain_sequences = [f"{domain.name}: {domain.sequence}" for domain in domains]

    strands_num = 2
    strand_structures = ["D1 D2'", "D2 D3'"]
    
    with_overhang = True

    initial_population = []
    for structure in strand_structures:
        strand_domains = [next(domain for domain in domains if domain.name == name) for name in structure.split()]
        sequence = "".join([domain.sequence for domain in strand_domains])
        initial_population.append(sequence)
    
    
    nsga = NSGA(initial_population)
    evolved_strands = nsga.run()
    evolved_strands = [strand + "TTTTT" for strand in evolved_strands] if with_overhang else evolved_strands

    strand_sequences = [f"Strand {i+1}: {strand}" for i, strand in enumerate(evolved_strands)]
    for i in evolved_strands:
        print(i)
    # return render_template('index.html', domain_sequences=domain_sequences, strand_sequences=strand_sequences)