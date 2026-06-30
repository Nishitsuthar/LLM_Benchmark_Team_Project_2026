#!/usr/bin/env python3
"""
Create combined optimization notebooks by stacking parameters
Modifies existing TOP_K=10 notebooks to add additional optimizations
"""

import json
import sys

def create_combined_optimization(base_notebook_path, output_notebook_path, optimizations):
    """
    Create a new notebook with combined optimizations

    optimizations = {
        'TOP_K': 10,
        'CHUNK_SIZE': 1500,
        'CHUNK_OVERLAP': 150,
        'TEMPERATURE': 0.3,
        'output_suffix': 'topk10_chunk1500'
    }
    """

    print(f"Reading base notebook: {base_notebook_path}")
    with open(base_notebook_path, 'r') as f:
        notebook = json.load(f)

    # Find and update the parameters cell (usually cell 5)
    params_updated = False
    for cell in notebook['cells']:
        if 'source' in cell:
            source_text = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

            # Check if this is the parameters cell
            if 'DATASET_NAME = ' in source_text and 'CHUNK_SIZE = ' in source_text:
                print(f"Found parameters cell")

                # Update source line by line
                new_source = []
                for line in (cell['source'] if isinstance(cell['source'], list) else [cell['source']]):

                    # Update each parameter if specified
                    if 'TOP_K = ' in line and 'TOP_K' in optimizations:
                        new_source.append(f"TOP_K = {optimizations['TOP_K']}\n")
                        print(f"  Updated TOP_K to {optimizations['TOP_K']}")

                    elif 'CHUNK_SIZE = ' in line and 'CHUNK_SIZE' in optimizations:
                        new_source.append(f"CHUNK_SIZE = {optimizations['CHUNK_SIZE']}\n")
                        print(f"  Updated CHUNK_SIZE to {optimizations['CHUNK_SIZE']}")

                    elif 'CHUNK_OVERLAP = ' in line and 'CHUNK_OVERLAP' in optimizations:
                        new_source.append(f"CHUNK_OVERLAP = {optimizations['CHUNK_OVERLAP']}\n")
                        print(f"  Updated CHUNK_OVERLAP to {optimizations['CHUNK_OVERLAP']}")

                    elif 'TEMPERATURE = ' in line and 'TEMPERATURE' in optimizations:
                        new_source.append(f"TEMPERATURE = {optimizations['TEMPERATURE']}\n")
                        print(f"  Updated TEMPERATURE to {optimizations['TEMPERATURE']}")

                    elif 'OUTPUT_DIR = ' in line and 'output_suffix' in optimizations:
                        # Extract dataset name from original OUTPUT_DIR
                        if 'tathybrid' in line:
                            dataset = 'tathybrid'
                        elif 'finhybrid' in line:
                            dataset = 'finhybrid'
                        elif 'nqtext' in line:
                            dataset = 'nqtext'
                        elif 'fetatab' in line:
                            dataset = 'fetatab'
                        elif 'papertext' in line:
                            dataset = 'papertext'
                        elif 'papertab' in line:
                            dataset = 'papertab'
                        else:
                            dataset = 'unknown'

                        new_output_dir = f"./experiments/nemotron-3-ultra-550b/2_optimization/results/{dataset}_{optimizations['output_suffix']}"
                        new_source.append(f'OUTPUT_DIR = "{new_output_dir}"\n')
                        print(f"  Updated OUTPUT_DIR to {new_output_dir}")

                    else:
                        new_source.append(line)

                cell['source'] = new_source
                params_updated = True
                break

    if not params_updated:
        print("  ⚠️  Warning: Could not find parameters cell to update")
        return False

    # Save new notebook
    print(f"Saving combined notebook: {output_notebook_path}")
    with open(output_notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)

    return True

# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("Creating Combined Optimization Notebooks")
    print("=" * 80)
    print()

    # Define combined optimizations
    experiments = [
        {
            'name': 'TatHybrid: TOP_K=10 + CHUNK_SIZE=1500',
            'base': 'tathybrid_topk10_experiment.ipynb',
            'output': 'tathybrid_topk10_chunk1500_experiment.ipynb',
            'params': {
                'TOP_K': 10,
                'CHUNK_SIZE': 1500,
                'CHUNK_OVERLAP': 150,
                'output_suffix': 'topk10_chunk1500'
            }
        },
        {
            'name': 'FinHybrid: TOP_K=10 + CHUNK_SIZE=1500',
            'base': 'finhybrid_topk10_experiment.ipynb',
            'output': 'finhybrid_topk10_chunk1500_experiment.ipynb',
            'params': {
                'TOP_K': 10,
                'CHUNK_SIZE': 1500,
                'CHUNK_OVERLAP': 150,
                'output_suffix': 'topk10_chunk1500'
            }
        },
        {
            'name': 'FinHybrid: TOP_K=10 + TEMPERATURE=0.3',
            'base': 'finhybrid_topk10_experiment.ipynb',
            'output': 'finhybrid_topk10_temp03_experiment.ipynb',
            'params': {
                'TOP_K': 10,
                'TEMPERATURE': 0.3,
                'output_suffix': 'topk10_temp03'
            }
        }
    ]

    base_dir = '/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization'

    results = []
    for exp in experiments:
        print(f"Experiment: {exp['name']}")
        print("-" * 80)

        base_path = f"{base_dir}/{exp['base']}"
        output_path = f"{base_dir}/{exp['output']}"

        success = create_combined_optimization(base_path, output_path, exp['params'])

        results.append({
            'name': exp['name'],
            'output': exp['output'],
            'success': success
        })

        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['name']}")
        if result['success']:
            print(f"   Saved to: {result['output']}")
        print()

    successful = sum(1 for r in results if r['success'])
    print(f"Created {successful}/{len(results)} combined optimization notebooks")
    print()

    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("Run these notebooks to test combined optimizations:")
    print()
    for result in results:
        if result['success']:
            print(f"  jupyter notebook {result['output']}")
    print()
