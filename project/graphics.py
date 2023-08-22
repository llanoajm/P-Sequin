import matplotlib.pyplot as plt

complex_structure = "fb( sc( mc( + fc* ) ) ) mb*( sb*( + hcj ) )"
obtained_strands = []
current_strand = ""
stack = []

# Make sure strands are represented as strings for a (way) faster comparison.
for domain in complex_structure.split():
    if len(current_strand) != 0:
        current_strand += ' '
    if domain == ')':
        complement = stack.pop()
        if complement.endswith('*'):
            domain_temp = complement[:-1]
        else:
            domain_temp = complement + '*'
        current_strand += domain_temp
        continue
    elif domain == '+':
        current_strand = current_strand[:-1]
        obtained_strands.append(current_strand)
        current_strand = ""
        continue
    if domain.endswith('('):
        stack.append(domain[:-1])
        current_strand += domain[:-1]
    else:
        current_strand += domain

if current_strand:
    current_strand = current_strand.rstrip()
    obtained_strands.append(current_strand)

# Should strands ever be used more than once in a particular complex? doubt so. if not, graph search could be way easier. 
# For safety, a dictionary will be utilized


strands_data = [
    {'name': 'Strand1', 'sequence': 'fb sc mc', 'contains_polymerase': True},
    {'name': 'Strand2', 'sequence': 'fc* mc* sc* fb* mb* sb*', 'contains_polymerase': False},
    {'name': 'Strand3', 'sequence': 'hcj sb mb', 'contains_polymerase': False},

]
# Convert the strands_data into a dictionary for faster lookup
strands_lookup = {strand['sequence']: strand for strand in strands_data}

# Iterate through the obtained strands and match them to the strands_data
matched_strands = []
for strand_sequence in obtained_strands:
    strand_details = strands_lookup.get(strand_sequence)
    if strand_details:
        matched_strands.append(strand_details)
        