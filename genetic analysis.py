Define the data
genomics_data = {
    'Gene1': {'mutation': 'A>T', 'copy_number': 2},
    'Gene2': {'mutation': 'C>G', 'copy_number': 3},
    'Gene3': {'mutation': 'G>C', 'copy_number': 1}
}

transcriptomics_data = {
    'Gene1': {'expression_level': 2.5},
    'Gene2': {'expression_level': 1.8},
    'Gene3': {'expression_level': 3.2}
}

proteomics_data = {
    'Gene1': {'protein_abundance': 100},
    'Gene2': {'protein_abundance': 50},
    'Gene3': {'protein_abundance': 200}
}

# Create integrated data
integrated_data = {}
for gene in genomics_data:
    integrated_data[gene] = {
        'mutation': genomics_data[gene]['mutation'],
        'copy_number': genomics_data[gene]['copy_number'],
        'expression_level': transcriptomics_data[gene]['expression_level'],
        'protein_abundance': proteomics_data[gene]['protein_abundance']
    }

# Print integrated data
print("Integrated Data:")
for gene, data in integrated_data.items():
    print(f"Gene: {gene}")
    print(f"Mutation: {data['mutation']}")
    print(f"Copy Number: {data['copy_number']}")
    print(f"Expression Level: {data['expression_level']}")
    print(f"Protein Abundance: {data['protein_abundance']}")
    print("------------------------")

# Analyze the relationship between copy number and expression level
print("\nRelationship between Copy Number and Expression Level:")
copy_numbers = [data['copy_number'] for data in integrated_data.values()]
expression_levels = [data['expression_level'] for data in integrated_data.values()]
print(f"Copy Number: {copy_numbers}")
print(f"Expression Level: {expression_levels}")

# Examine the correlation between expression level and protein abundance
print("\nCorrelation between Expression Level and Protein Abundance:")
expression_levels = [data['expression_level'] for data in integrated_data.values()]
protein_abundances = [data['protein_abundance'] for data in integrated_data.values()]
print(f"Expression Level: {expression_levels}")
print(f"Protein Abundance: {protein_abundances}")
