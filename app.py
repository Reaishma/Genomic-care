from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import random
import json
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# Disable caching for development
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Global data store for metrics
metrics_data = {
    'genes_analyzed': 12847,
    'targets_identified': 342,
    'pathways_active': 28,
    'model_accuracy': 87.3
}

# Gene database simulation
GENE_DATABASE = {
    'BRCA1': {'type': 'tumor_suppressor', 'function': 'DNA repair', 'disease_relevance': {'cancer': 0.95}},
    'TP53': {'type': 'tumor_suppressor', 'function': 'Cell cycle control', 'disease_relevance': {'cancer': 0.89}},
    'EGFR': {'type': 'oncogene', 'function': 'Growth signaling', 'disease_relevance': {'cancer': 0.82}},
    'APOE': {'type': 'apolipoprotein', 'function': 'Lipid transport', 'disease_relevance': {'alzheimer': 0.76}},
    'INS': {'type': 'hormone', 'function': 'Glucose regulation', 'disease_relevance': {'diabetes': 0.88}},
    'LDLR': {'type': 'receptor', 'function': 'Cholesterol uptake', 'disease_relevance': {'cardiovascular': 0.73}}
}

# Pathway data
PATHWAY_DATA = {
    'p53': {
        'name': 'p53 Signaling Pathway',
        'nodes': [
            {'id': 'p53', 'name': 'p53', 'type': 'tumor_suppressor', 'x': 300, 'y': 200},
            {'id': 'MDM2', 'name': 'MDM2', 'type': 'oncogene', 'x': 200, 'y': 100},
            {'id': 'p21', 'name': 'p21', 'type': 'kinase', 'x': 400, 'y': 100},
            {'id': 'PUMA', 'name': 'PUMA', 'type': 'apoptosis', 'x': 350, 'y': 300},
            {'id': 'BAX', 'name': 'BAX', 'type': 'apoptosis', 'x': 250, 'y': 300}
        ],
        'links': [
            {'source': 'p53', 'target': 'p21'},
            {'source': 'p53', 'target': 'PUMA'},
            {'source': 'p53', 'target': 'BAX'},
            {'source': 'MDM2', 'target': 'p53'}
        ]
    },
    'mapk': {
        'name': 'MAPK Signaling Pathway',
        'nodes': [
            {'id': 'RAS', 'name': 'RAS', 'type': 'signal', 'x': 200, 'y': 200},
            {'id': 'RAF', 'name': 'RAF', 'type': 'kinase', 'x': 300, 'y': 150},
            {'id': 'MEK', 'name': 'MEK', 'type': 'kinase', 'x': 400, 'y': 200},
            {'id': 'ERK', 'name': 'ERK', 'type': 'kinase', 'x': 500, 'y': 250},
            {'id': 'c-Fos', 'name': 'c-Fos', 'type': 'transcription_factor', 'x': 600, 'y': 200}
        ],
        'links': [
            {'source': 'RAS', 'target': 'RAF'},
            {'source': 'RAF', 'target': 'MEK'},
            {'source': 'MEK', 'target': 'ERK'},
            {'source': 'ERK', 'target': 'c-Fos'}
        ]
    },
    'pi3k': {
        'name': 'PI3K-AKT Pathway',
        'nodes': [
            {'id': 'PI3K', 'name': 'PI3K', 'type': 'kinase', 'x': 200, 'y': 200},
            {'id': 'AKT', 'name': 'AKT', 'type': 'kinase', 'x': 300, 'y': 200},
            {'id': 'mTOR', 'name': 'mTOR', 'type': 'kinase', 'x': 400, 'y': 150},
            {'id': 'GSK3β', 'name': 'GSK3β', 'type': 'kinase', 'x': 350, 'y': 250},
            {'id': 'PTEN', 'name': 'PTEN', 'type': 'tumor_suppressor', 'x': 150, 'y': 150}
        ],
        'links': [
            {'source': 'PI3K', 'target': 'AKT'},
            {'source': 'AKT', 'target': 'mTOR'},
            {'source': 'AKT', 'target': 'GSK3β'},
            {'source': 'PTEN', 'target': 'PI3K'}
        ]
    },
    'nf-kb': {
        'name': 'NF-κB Pathway',
        'nodes': [
            {'id': 'TNF-α', 'name': 'TNF-α', 'type': 'signal', 'x': 150, 'y': 200},
            {'id': 'IKK', 'name': 'IKK', 'type': 'kinase', 'x': 250, 'y': 200},
            {'id': 'IκB', 'name': 'IκB', 'type': 'inhibitor', 'x': 350, 'y': 150},
            {'id': 'NF-κB', 'name': 'NF-κB', 'type': 'transcription_factor', 'x': 450, 'y': 200},
            {'id': 'IL-6', 'name': 'IL-6', 'type': 'cytokine', 'x': 550, 'y': 250}
        ],
        'links': [
            {'source': 'TNF-α', 'target': 'IKK'},
            {'source': 'IKK', 'target': 'IκB'},
            {'source': 'IκB', 'target': 'NF-κB'},
            {'source': 'NF-κB', 'target': 'IL-6'}
        ]
    }
}

def generate_mechanisms(gene, disease):
    """Generate potential therapeutic mechanisms"""
    mechanisms = [
        'Protein kinase inhibition',
        'Transcriptional regulation',
        'Cell cycle arrest',
        'Apoptosis induction',
        'DNA repair pathway modulation',
        'Receptor antagonism',
        'Enzyme inhibition',
        'Signal transduction disruption',
        'Protein-protein interaction blocking',
        'Chromatin remodeling'
    ]
    
    # Select 2-4 mechanisms based on gene and disease
    num_mechanisms = random.randint(2, 4)
    return random.sample(mechanisms, num_mechanisms)

def generate_associated_pathways(gene):
    """Generate associated biological pathways"""
    pathways = [
        'p53 signaling pathway',
        'MAPK signaling pathway',
        'PI3K-AKT pathway',
        'Cell cycle regulation',
        'DNA damage response',
        'Apoptosis pathway',
        'NF-κB pathway',
        'Wnt signaling pathway',
        'mTOR signaling pathway',
        'JAK-STAT pathway'
    ]
    
    # Select 2-4 pathways
    num_pathways = random.randint(2, 4)
    return random.sample(pathways, num_pathways)

@app.route('/')
def index():
    """Serve the main genomic care application"""
    return render_template('genomic_care.html')

@app.route('/api/metrics')
def get_metrics():
    """Get current system metrics"""
    # Add some random variation to simulate live data
    current_metrics = {
        'genes_analyzed': metrics_data['genes_analyzed'] + random.randint(-50, 100),
        'targets_identified': metrics_data['targets_identified'] + random.randint(-10, 20),
        'pathways_active': metrics_data['pathways_active'] + random.randint(-2, 5),
        'model_accuracy': round(metrics_data['model_accuracy'] + random.uniform(-2, 2), 1)
    }
    return jsonify(current_metrics)

@app.route('/api/predict_target', methods=['POST'])
def predict_therapeutic_target():
    """Predict therapeutic targets for given gene and disease"""
    try:
        data = request.get_json()
        gene_symbol = data.get('gene_symbol', '').upper()
        disease = data.get('disease', '')
        
        if not gene_symbol or not disease:
            return jsonify({'error': 'Gene symbol and disease are required'}), 400
        
        # Simulate analysis delay
        time.sleep(1)
        
        # Get gene information
        gene_info = GENE_DATABASE.get(gene_symbol, {
            'type': 'unknown',
            'function': 'Unknown function',
            'disease_relevance': {disease: random.uniform(0.1, 0.9)}
        })
        
        # Calculate prediction score
        base_score = gene_info.get('disease_relevance', {}).get(disease, random.uniform(0.1, 0.9))
        prediction_score = min(0.99, base_score + random.uniform(-0.1, 0.1))
        
        # Determine prediction class
        if prediction_score >= 0.7:
            prediction_class = 'high'
            recommendation = 'Strong therapeutic target candidate'
        elif prediction_score >= 0.4:
            prediction_class = 'medium'
            recommendation = 'Moderate therapeutic potential'
        else:
            prediction_class = 'low'
            recommendation = 'Limited therapeutic potential'
        
        # Generate related genes
        related_genes = random.sample([g for g in GENE_DATABASE.keys() if g != gene_symbol], 
                                    min(3, len(GENE_DATABASE) - 1))
        
        # Generate drug targets
        drug_targets = [
            {'name': f'Target-{i+1}', 'confidence': round(random.uniform(0.6, 0.95), 2)}
            for i in range(random.randint(2, 5))
        ]
        
        result = {
            'gene': gene_symbol,
            'gene_symbol': gene_symbol,
            'disease': disease,
            'score': round(prediction_score, 3),
            'prediction_score': round(prediction_score, 3),
            'class': prediction_class,
            'prediction_class': prediction_class,
            'confidence': round(min(0.99, base_score + random.uniform(0.05, 0.15)), 3),
            'drugability': round(random.uniform(60, 95), 1),
            'recommendation': recommendation,
            'gene_type': gene_info['type'],
            'function': gene_info['function'],
            'mechanisms': generate_mechanisms(gene_symbol, disease),
            'pathways': generate_associated_pathways(gene_symbol),
            'related_genes': related_genes,
            'drug_targets': drug_targets,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Update metrics
        metrics_data['genes_analyzed'] += 1
        if prediction_score >= 0.4:
            metrics_data['targets_identified'] += 1
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pathway/<pathway_id>')
def get_pathway_data(pathway_id):
    """Get pathway network data"""
    if pathway_id not in PATHWAY_DATA:
        return jsonify({'error': 'Pathway not found'}), 404
    
    return jsonify(PATHWAY_DATA[pathway_id])

@app.route('/api/performance_data')
def get_performance_data():
    """Get ML model performance data for charts"""
    # Generate mock performance data
    epochs = list(range(1, 21))
    accuracy = [0.6 + (i * 0.02) + random.uniform(-0.03, 0.03) for i in epochs]
    loss = [0.8 - (i * 0.035) + random.uniform(-0.05, 0.05) for i in epochs]
    
    return jsonify({
        'labels': epochs,
        'accuracy': [round(a, 3) for a in accuracy],
        'loss': [round(l, 3) for l in loss]
    })

@app.route('/api/target_distribution')
def get_target_distribution():
    """Get target classification distribution data"""
    return jsonify({
        'labels': ['High Potential', 'Medium Potential', 'Low Potential', 'No Target'],
        'data': [25, 35, 30, 10],
        'colors': ['#27ae60', '#f39c12', '#e74c3c', '#95a5a6']
    })

@app.route('/api/validate_gene', methods=['POST'])
def validate_gene():
    """Validate gene symbol or sequence"""
    try:
        data = request.get_json()
        gene_input = data.get('gene_input', '').upper()
        
        if not gene_input:
            return jsonify({'valid': False, 'message': 'Gene input is required'})
        
        # Simple validation - check if it's a known gene symbol
        if gene_input in GENE_DATABASE:
            return jsonify({
                'valid': True,
                'gene_symbol': gene_input,
                'gene_info': GENE_DATABASE[gene_input]
            })
        
        # Check if it looks like a DNA sequence
        if all(c in 'ATCG' for c in gene_input) and len(gene_input) > 10:
            return jsonify({
                'valid': True,
                'sequence_length': len(gene_input),
                'gc_content': round((gene_input.count('G') + gene_input.count('C')) / len(gene_input) * 100, 1)
            })
        
        return jsonify({
            'valid': False,
            'message': 'Invalid gene symbol or sequence'
        })
        
    except Exception as e:
        return jsonify({'valid': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)