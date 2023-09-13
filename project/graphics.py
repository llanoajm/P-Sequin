import matplotlib.pyplot as plt
import mpld3

class DNAComplexPlotter:
    def __init__(self, complex_structure, strands_data):
        self.complex_structure = complex_structure
        self.strands_data = strands_data
        self.obtained_strands = []
        self.matched_strands = []
        self.all_domain_coordinates = []
        self.extract_strands()
        self.find_matched_strands()
        max_domains = max(len(strand['sequence'].split()) for strand in self.matched_strands)
        self.universal_spacing = 1.0 / (max_domains + 1)
        
    def extract_strands(self):
        current_strand = ""
        stack = []

        for domain in self.complex_structure.split():
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
                self.obtained_strands.append(current_strand)
                current_strand = ""
                continue
            if domain.endswith('('):
                stack.append(domain[:-1])
                current_strand += domain[:-1]
            else:
                current_strand += domain
        
        if current_strand:
            current_strand = current_strand.rstrip()
            self.obtained_strands.append(current_strand)
            
    def find_matched_strands(self):
        strands_lookup = {strand['sequence']: strand for strand in self.strands_data}
        for strand_sequence in self.obtained_strands:
            strand_details = strands_lookup.get(strand_sequence)
            if strand_details:
                self.matched_strands.append(strand_details)

    def calculate_aligned_domain_coordinates(self, strand, index, quadrant_middle, left_bound=None, right_bound=None):
        domains = strand['sequence'].split()
        direction = -1 if index in [0, 2] else 1

        if left_bound is not None and right_bound is not None:
            coordinates = [(left_bound + i * self.universal_spacing * direction, quadrant_middle[1]) for i in range(len(domains))]
        else:
            coordinates = [(quadrant_middle[0] + direction * (i + 1) * self.universal_spacing, quadrant_middle[1]) for i in range(len(domains))]
        
        return list(zip(domains, coordinates))

    def plot_strands(self):
        quadrant_middle_coordinates = {
            0: (-0.5, 0.5),
            1: (0, 0.45),
            2: (0.5, 0.5)
        }

        max_domains = max(len(strand['sequence'].split()) for strand in self.matched_strands)
        universal_spacing = 1.0 / (max_domains + 1)
        
        initial_domain_coordinates = []
        for index, strand in enumerate(self.matched_strands):
            initial_domain_coordinates.extend(self.calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index]))

        mc_x_coordinate = initial_domain_coordinates[len(self.matched_strands[0]['sequence'].split()) - 1][1][0]
        left_bound_strand2 = mc_x_coordinate
        strand2_domains = self.matched_strands[1]['sequence'].split()
        right_bound_strand2 = left_bound_strand2 + (len(strand2_domains) - 1) * universal_spacing

        strand1_domains_count = len(self.matched_strands[0]['sequence'].split())
        last_domain_strand3_x = (strand1_domains_count) * universal_spacing - 0.22
        quadrant_middle_coordinates[2] = (last_domain_strand3_x - (len(self.matched_strands[2]['sequence'].split()) - 1) * universal_spacing, quadrant_middle_coordinates[2][1])

        all_domain_coordinates = []
        for index, strand in enumerate(self.matched_strands):
            if index == 0:
                all_domain_coordinates.extend(self.calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index]))
            elif index == 2:
                all_domain_coordinates.extend(self.calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index]))
            else:
                all_domain_coordinates.extend(self.calculate_aligned_domain_coordinates(strand, index, quadrant_middle_coordinates[index], left_bound=left_bound_strand2, right_bound=right_bound_strand2))

        fig, ax = plt.subplots(figsize=(8, 8))
        strand_colors = ['red', 'green', 'blue']
        for index, strand in enumerate(self.matched_strands):
            if strand.get('contains_polymerase'):
                strand_colors[index] = 'purple'
        for index, strand in enumerate(self.matched_strands):
            strand_domains = strand['sequence'].split()
            strand_coordinates = [coord for domain, coord in all_domain_coordinates if domain in strand_domains]
            
            x_coords, y_coords = zip(*strand_coordinates)
            ax.plot(x_coords, y_coords, color=strand_colors[index], label=strand['name'])
            
            for domain, (x, y) in zip(strand_domains, strand_coordinates):
                ax.text(x, y, domain, fontsize=9, ha='center')

        ax.set_title('DNA Complex Plot')
        ax.legend()
        with open('plot.html', 'w') as f:
            mpld3.save_html(fig, f)
        
# Usage:
strands_data = [
    {'name': 'Strand1', 'sequence': 'fb sc mc', 'contains_polymerase': True},
    {'name': 'Strand2', 'sequence': 'fc* mc* sc* fb* mb* sb*', 'contains_polymerase': False},
    {'name': 'Strand3', 'sequence': 'hcj sb mb', 'contains_polymerase': False},
]

complex_structure = "fb( sc( mc( + fc* ) ) ) mb*( sb*( + hcj ) )"

plotter = DNAComplexPlotter(complex_structure, strands_data)
plotter.plot_strands()
