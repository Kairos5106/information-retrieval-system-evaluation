import pandas as pd
import numpy as np
from scipy import stats
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
import os

def perform_significance_test(system1_data, system2_data, alpha=0.05):
    """
    Perform a paired t-test between two systems.
    
    Args:
        system1_data: List of metric values for system 1
        system2_data: List of metric values for system 2
        alpha: Significance level (default: 0.05)
    
    Returns:
        t_statistic: The t-statistic
        p_value: The p-value
        significant: Boolean indicating if the difference is significant
    """
    t_statistic, p_value = stats.ttest_rel(system1_data, system2_data)
    significant = p_value < alpha
    return t_statistic, p_value, significant

def analyze_metric_significance(metric_table, metric_name):
    """
    Analyze significance between all pairs of systems for a given metric and save results to Excel.
    
    Args:
        metric_table: DataFrame containing the metric values for each system
        metric_name: Name of the metric being analyzed
    
    Returns:
        DataFrame containing the significance test results
    """
    # Handle different table structures
    if 'topic' in metric_table.columns:
        systems = metric_table.columns[1:]  # Skip the 'topic' column
        id_column = 'topic'
    else:
        systems = metric_table.columns[1:]  # Skip the 'input_file' column
        id_column = 'input_file'
    
    system_pairs = list(itertools.combinations(systems, 2))
    
    results = []
    
    for sys1, sys2 in system_pairs:
        t_stat, p_val, significant = perform_significance_test(
            metric_table[sys1].values,
            metric_table[sys2].values
        )
        
        results.append({
            'System 1': sys1,
            'System 2': sys2,
            't-statistic': t_stat,
            'p-value': p_val,
            'Significant': significant
        })
    
    results_df = pd.DataFrame(results)
    
    # Save to Excel
    output_file = f'output/significance_test_{metric_name.lower()}.xlsx'
    results_df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    # Create boxplot
    plt.figure(figsize=(12, 6))
    melted_data = metric_table.melt(id_vars=[id_column])
    sns.boxplot(data=melted_data, x='variable', y='value')
    plt.title(f'{metric_name} Distribution by System')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'output/significance_{metric_name.lower()}_boxplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return results_df

def main():
    os.makedirs('output', exist_ok=True)
    
    try:
        ndcg_table = pd.read_excel('output/ndcg_10_table.xlsx')
        map_table = pd.read_excel('output/average_precision_table.xlsx')
        mrr_table = pd.read_excel('output/mean_reciprocal_rank_table.xlsx')
        
        print("Performing significance testing for NDCG@10...")
        ndcg_results = analyze_metric_significance(ndcg_table, 'NDCG@10')
        
        print("Performing significance testing for MAP...")
        map_results = analyze_metric_significance(map_table, 'MAP')
        
        print("Performing significance testing for MRR...")
        mrr_results = analyze_metric_significance(mrr_table, 'MRR')
        
        with pd.ExcelWriter('output/significance_test_summary.xlsx') as writer:
            ndcg_results.to_excel(writer, sheet_name='NDCG@10', index=False)
            map_results.to_excel(writer, sheet_name='MAP', index=False)
            mrr_results.to_excel(writer, sheet_name='MRR', index=False)
        print("\nSummary results saved to output/significance_test_summary.xlsx")
        
        print("\n" + "="*50)
        print("SIGNIFICANCE TESTING SUMMARY")
        print("="*50)
        
        for metric_name, results_df in [("NDCG@10", ndcg_results), ("MAP", map_results), ("MRR", mrr_results)]:
            print(f"\n{metric_name}:")
            if results_df.empty:
                print("  No results available for this metric.")
            elif 'Significant' not in results_df.columns:
                print("  ⚠️ Warning: 'Significant' column not found. Skipping analysis.")
            else:
                significant_pairs = results_df[results_df['Significant'] == True]
                if not significant_pairs.empty:
                    print(f"  Significant differences found in {len(significant_pairs)} system pairs:")
                    for _, row in significant_pairs.iterrows():
                        print(f"    {row['System 1']} vs {row['System 2']} (p-value: {row['p-value']:.4f})")
                else:
                    print("  No significant differences found between any system pairs.")
        
    except FileNotFoundError as e:
        print("Error: Could not find required data files. Make sure you have run the evaluation metrics first.")
        print(f"Missing file: {e.filename}")

if __name__ == "__main__":
    main()