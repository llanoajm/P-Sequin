import matplotlib.pyplot as plt

# Define the complex structure and initialize necessary variables
complex_structure = "fb( sc( mc( + fc* ) ) ) mb*( sb*( + hcj ) )"
obtained_strands = []
current_strand = ""
stack = []

# Extract strands from the complex structure
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

# Define the strand data and create a lookup dictionary
strands_data = [
    {'name': 'Strand1', 'sequence': 'fb sc mc', 'contains_polymerase': True},
    {'name': 'Strand2', 'sequence': 'fc* mc* sc* fb* mb* sb*', 'contains_polymerase': False},
    {'name': 'Strand3', 'sequence': 'hcj sb mb', 'contains_polymerase': False},
]
strands_lookup = {strand['sequence']: strand for strand in strands_data}

# Find the matched strands
matched_strands = []
for strand_sequence in obtained_strands:
    strand_details = strands_lookup.get(strand_sequence)
    if strand_details:
        matched_strands.append(strand_details)

# Define coordinates for the quadrants
quadrant_coordinates = {
    0: (-0.5, 0.5),  # Top-left quadrant for Strand 1
    1: (0, -0.5),    # Bottom quadrant for Strand 2
    2: (0.5, 0.5)    # Top-right quadrant for Strand 3
}

# Initialize a new figure
fig, ax = plt.subplots(figsize=(8, 8))

# Plot each matched strand in its respective quadrant
for index, strand in enumerate(matched_strands):
    color = 'red' if strand['contains_polymerase'] else 'blue'
    ax.scatter(*quadrant_coordinates[index], color=color, s=100, label=strand['name'])

# Set labels, title, and legend
ax.set_title('Matched Strands Representation')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axhline(0, color='black',linewidth=0.5)
ax.axvline(0, color='black',linewidth=0.5)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.grid(True, which='both')
ax.legend(loc="lower right")

# Display the plot
plt.show()
