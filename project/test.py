from NSGAtest import *

# Domains
initial_population = ["AACTGT", "GGTA", "TACC", "TAGC", "AGGT"]

# Dictionary of domain appearances in strands.
# Here, for simplicity, I'm assuming domains are identified by their index (0-based) in the initial_population list.
# Let's say:
# Strand 1 = "AACTGTGGTA"
# Strand 2 = "TACCTAGC"
# Strand 3 = "AGGTGGTA"
domain_appearances = {
    0: [0],          # "AACTGT" appears in Strand 1
    1: [0, 2],       # "GGTA" appears in Strand 1 and Strand 3
    2: [1],          # "TACC" appears in Strand 2
    3: [1],          # "TAGC" appears in Strand 2
    4: [2]           # "AGGT" appears in Strand 3
}

# Strand structures, represented by domain indices
strand_structures = [
    [0, 1],          # Strand 1
    [2, 3],          # Strand 2
    [4, 1]           # Strand 3
]

nsga = NSGA(initial_population, domain_appearances, strand_structures)
result = nsga.run(50)
for s in result:
    print(s)
