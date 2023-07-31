from flask import Flask, render_template, request

app = Flask(__name__)

import random

class Domain:
    def __init__(self, name, sequence) -> None:
        self.name = name
        self.sequence = sequence
        self.complement = '\'' in name

class Strand:
    def __init__(self, strand_domains) -> None:
        self.domains_in_strand = strand_domains
        self.sequence = "".join([domain.sequence for domain in strand_domains]) + "TTT"

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    domains_num = int(request.form['domains_num'])
    domain_names = request.form['domain_names'].split(',')
    domain_lengths = list(map(int, request.form['domain_lengths'].split(',')))
    
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

    strands_num = int(request.form['strands_num'])
    strand_structures = request.form['strand_structures'].split(',')

    strands = []
    for structure in strand_structures:
        strand_domains = [next(domain for domain in domains if domain.name == name) for name in structure.split()]
        strand = Strand(strand_domains)
        strands.append(strand)
    
    strand_sequences = [f"Strand {i+1}: {strand.sequence}" for i, strand in enumerate(strands)]

    return render_template('index.html', domain_sequences=domain_sequences, strand_sequences=strand_sequences)

if __name__ == '__main__':
    app.run(debug=True)
