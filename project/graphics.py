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

# Define coordinates for the middle of each quadrant
quadrant_middle_coordinates = {
    0: (-0.5, 0.5),  # Top-left quadrant for Strand 1
    1: (0, -0.5),    # Bottom quadrant for Strand 2
    2: (0.5, 0.5)    # Top-right quadrant for Strand 3
}

# Determine the maximum number of domains in any strand to set a universal spacing
max_domains = max(len(strand['sequence'].split()) for strand in matched_strands)
universal_spacing = 1.0 / (max_domains + 1)

# Update the function to use the universal spacing
def calculate_aligned_domain_coordinates(strand, index, quadrant_middle, left_bound=None, right_bound=None):
    # Get the sequence of domains in the strand
    domains = strand['sequence'].split()
    
    # Determine the direction for allocating coordinates (right to left or left to right)
    direction = -1 if index in [0, 2] else 1
    
    # Calculate the X and Y coordinates for each domain
    if left_bound is not None and right_bound is not None:
        coordinates = [(left_bound + i * universal_spacing * direction, quadrant_middle[1]) for i in range(len(domains))]
    else:
        coordinates = [(quadrant_middle[0] + direction * (i + 1) * universal_spacing, quadrant_middle[1]) for i in range(len(domains))]
    
    return list(zip(domains, coordinates))

# Step 1: Find the x-coordinate of the "mc" domain in Strand 1
initial_domain_coordinates = []
for index, strand in enumerate(matched_strands):
    initial_domain_coordinates.extend(calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index]))

mc_x_coordinate = initial_domain_coordinates[len(matched_strands[0]['sequence'].split()) - 1][1][0]

# Step 2 & 3: Set the x-coordinate of the leftmost domain in Strand 2 and find the new right bound for Strand 2
left_bound_strand2 = mc_x_coordinate
strand2_domains = matched_strands[1]['sequence'].split()
right_bound_strand2 = left_bound_strand2 + (len(strand2_domains) - 1) * universal_spacing

# Step 4: Use the new bounds to calculate coordinates for all strands with the correct alignments
# Calculate the x-coordinate for the last domain in strand 3
strand1_domains_count = len(matched_strands[0]['sequence'].split())


# Setting the x-coordinate of the last domain of strand 3
last_domain_strand3_x = (strand1_domains_count) * universal_spacing - 0.2
print(universal_spacing)

# Adjusting the middle coordinate of quadrant III to set the correct x-coordinate for the last domain of strand 3
quadrant_middle_coordinates[2] = (last_domain_strand3_x - (len(matched_strands[2]['sequence'].split()) - 1) * universal_spacing, quadrant_middle_coordinates[2][1])

# Calculate coordinates for all strands with the correct alignments
all_domain_coordinates = []
for index, strand in enumerate(matched_strands):
    if index == 0:  # Strand 1 in quadrant I
        all_domain_coordinates.extend(calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index]))
    elif index == 2:  # Strand 3 in quadrant III
        all_domain_coordinates.extend(calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index]))
    else:  # Strand 2 in quadrant II
        all_domain_coordinates.extend(calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index], left_bound=left_bound_strand2, right_bound=right_bound_strand2))

# Initialize a new figure
fig, ax = plt.subplots(figsize=(8, 8))

# Plot each domain at its allocated coordinates
for domain, (x, y) in all_domain_coordinates:
    ax.text(x, y, domain, fontsize=9, ha='center')
    ax.plot(x, y, marker='o', markersize=5, label=domain)

# Set labels, title, and grid
ax.set_title('Aligned Domain Coordinates Representation')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, which='both')

# Display the plot
plt.show()
