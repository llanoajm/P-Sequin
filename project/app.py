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
    new_domain_names = []
    for i in range(domains_num):
        name = domain_names[i]
        domain_appearances[name] = []
        domain_appearances[name + '\''] = []
        length = domain_lengths[i]
        sequence, complement_sequence = generate_unique_domain_and_complement(length)
        new_domain_names.append(name)
        new_domain_names.append(name+"\'")
        domain = Domain(name, sequence)
        domains.append(domain)
        initial_population.append(sequence); initial_population.append(complement_sequence)
        complement_domain = Domain(name + '\'', complement_sequence)
        domains.append(complement_domain)

    domain_sequences = [f"{domain.name}: {domain.sequence}" for domain in domains]
    
    strand_structures = request.form.getlist('strand_structure[]')
    complex_notations = request.form.getlist('complex_notation[]')  # Getting complexes from the form
    complex_strands_input = request.form.getlist('complex_strands[]')
    complex_strands = complex_strands_input
    print("Checkpoint")
    for complex_strand, complex_notation in zip(complex_strands, complex_notations):
        print(represent_complex(complex_strand, complex_notation))

    
    
    is_polymerase = request.form.getlist('is_polymerase') 
    with_overhang = 'overhang' in request.form

    for index, structure in enumerate(strand_structures):
        for domain_name in structure.split():
            domain_appearances[domain_name].append(index)

    # Process complex notations as needed
    complexes = []  # Create a list to store the complexes
    for notation in complex_notations:
        # Process each complex notation here
        complexes.append(notation)  # Add the complex to the list

    nsga = NSGA(initial_population, domain_appearances, strand_structures, new_domain_names)
    
    evolved_strands, evolved_domain_data = nsga.run(6)
    evolved_strands = [strand + "TTTTT" for strand in evolved_strands] if with_overhang else evolved_strands

    strand_sequences = [f"Strand {i+1}: {strand}" for i, strand in enumerate(evolved_strands)]
    domain_sequences = [f"{domain_data['name']}: {domain_data['sequence']}" for domain_data in evolved_domain_data]

    return render_template('index.html', domain_sequences=domain_sequences, strand_sequences=strand_sequences)

if __name__ == '__main__':
    app.run(debug=True)
