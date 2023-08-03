from flask import Flask, render_template, request

app = Flask(__name__)

from utils import *
from NSGA import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    domain_appearances = {}
    domains_num = int(request.form['domains_num'])
    domain_names = request.form['domain_names'].split(',')
    domain_lengths = list(map(int, request.form['domain_lengths'].split(',')))
    initial_population = []
    domains = []
    for i in range(domains_num):
        name = domain_names[i]
        domain_appearances[name] = []  # Initialize the list for each domain
        length = domain_lengths[i]
        sequence, complement_sequence = generate_unique_domain_and_complement(length)
        
        domain = Domain(name, sequence)
        domains.append(domain)
        initial_population.append(sequence); initial_population.append(complement_sequence)
        complement_domain = Domain(name + '\'', complement_sequence)
        domains.append(complement_domain)

    domain_sequences = [f"{domain.name}: {domain.sequence}" for domain in domains]

    strands_num = int(request.form['strands_num'])
    strand_structures = request.form['strand_structures'].split(',')
    
    with_overhang = 'overhang' in request.form

    
    for index, structure in enumerate(strand_structures):  # Added enumeration for index reference
        # Update the domain_appearances dictionary
        for domain_name in structure.split():
            domain_appearances[domain_name].append(index)  # Appending the index (or structure itself if desired)
        

    nsga = NSGA(initial_population, domain_appearances, strand_structures, domain_names)
    evolved_strands = nsga.run(6)
    evolved_strands = [strand + "TTTTT" for strand in evolved_strands] if with_overhang else evolved_strands

    strand_sequences = [f"Strand {i+1}: {strand}" for i, strand in enumerate(evolved_strands)]
    print(strand_sequences)
    print(strand_structures)
    
    return render_template('index.html', domain_sequences=domain_sequences, strand_sequences=strand_sequences)

if __name__ == '__main__':
    app.run(debug=True)
