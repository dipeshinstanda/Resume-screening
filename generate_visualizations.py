"""
Generate visualizations for research paper
Creates charts and graphs from evaluation results
"""

import sys
import os
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import numpy as np
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

def load_latest_comparison():
    """Load the latest comparison results"""
    results_dir = 'backend/evaluation_results'

    if not os.path.exists(results_dir):
        print(f"❌ No results directory found at {results_dir}")
        return None

    # Find latest comparison file (supports both 'comparison_' and 'large_comparison_' prefixes)
    comparison_files = [f for f in os.listdir(results_dir) if f.startswith('comparison_') or f.startswith('large_comparison_')]

    if not comparison_files:
        print("❌ No comparison results found. Run run_comparative_evaluation.py or run_large_scale_evaluation.py --compare first.")
        return None
    
    latest_file = sorted(comparison_files)[-1]
    filepath = os.path.join(results_dir, latest_file)
    
    print(f"✓ Loading results from: {filepath}")
    
    with open(filepath, 'r') as f:
        return json.load(f)

def load_threshold_results():
    """Load threshold analysis results"""
    results_dir = 'backend/evaluation_results'

    # Support both 'threshold_' and 'large_eval_' file patterns
    threshold_files = [f for f in os.listdir(results_dir) if f.startswith('threshold_') or f.startswith('large_eval_')]

    if not threshold_files:
        print("⚠ No threshold results found. Skipping threshold analysis charts.")
        return None
    
    results = []
    for filename in sorted(threshold_files)[:5]:  # Get first 5 threshold results
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            if 'metrics' in data:
                results.append(data)
    
    return results if results else None

def create_comparison_chart(results):
    """Create bar chart comparing ML vs Baseline"""
    
    print("\n📊 Creating comparison chart...")
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    ml_values = [
        results['ml_based']['accuracy'],
        results['ml_based']['precision'],
        results['ml_based']['recall'],
        results['ml_based']['f1_score']
    ]
    baseline_values = [
        results['baseline']['accuracy'],
        results['baseline']['precision'],
        results['baseline']['recall'],
        results['baseline']['f1_score']
    ]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, ml_values, width, label='ML-Based (TF-IDF)', color='#2563eb')
    bars2 = ax.bar(x + width/2, baseline_values, width, label='Baseline (Keyword)', color='#dc2626')
    
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Performance Comparison: ML-Based vs Baseline Algorithm', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, 1.0])
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.3f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    output_file = 'visualizations/comparison_chart.png'
    os.makedirs('visualizations', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved to: {output_file}")

def create_improvement_chart(results):
    """Create chart showing improvement percentages"""
    
    print("📊 Creating improvement chart...")
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    improvements = [
        results['improvement']['accuracy'],
        results['improvement']['precision'],
        results['improvement']['recall'],
        results['improvement']['f1_score']
    ]
    
    colors = ['#10b981' if x > 0 else '#ef4444' if x < 0 else '#6b7280' for x in improvements]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(metrics, improvements, color=colors)
    
    ax.set_xlabel('Improvement (%)', fontsize=12)
    ax.set_title('ML-Based Algorithm Improvement over Baseline', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, improvements)):
        ax.text(value + (1 if value > 0 else -1), i, f'{value:+.2f}%',
               ha='left' if value > 0 else 'right', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_file = 'visualizations/improvement_chart.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved to: {output_file}")

def create_confusion_matrix_charts(results):
    """Create confusion matrix visualizations"""
    
    print("📊 Creating confusion matrix charts...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ML-Based confusion matrix
    ml_matrix = np.array([
        [results['ml_based']['true_positives'], results['ml_based']['false_negatives']],
        [results['ml_based']['false_positives'], results['ml_based']['true_negatives']]
    ])
    
    im1 = ax1.imshow(ml_matrix, cmap='Blues', aspect='auto')
    ax1.set_xticks([0, 1])
    ax1.set_yticks([0, 1])
    ax1.set_xticklabels(['Predicted\nMatch', 'Predicted\nNo Match'])
    ax1.set_yticklabels(['Actual\nMatch', 'Actual\nNo Match'])
    ax1.set_title('ML-Based Algorithm\nConfusion Matrix', fontsize=12, fontweight='bold')
    
    for i in range(2):
        for j in range(2):
            ax1.text(j, i, str(ml_matrix[i, j]),
                    ha="center", va="center", color="white" if ml_matrix[i, j] > ml_matrix.max()/2 else "black",
                    fontsize=20, fontweight='bold')
    
    # Baseline confusion matrix
    baseline_matrix = np.array([
        [results['baseline']['true_positives'], results['baseline']['false_negatives']],
        [results['baseline']['false_positives'], results['baseline']['true_negatives']]
    ])
    
    im2 = ax2.imshow(baseline_matrix, cmap='Reds', aspect='auto')
    ax2.set_xticks([0, 1])
    ax2.set_yticks([0, 1])
    ax2.set_xticklabels(['Predicted\nMatch', 'Predicted\nNo Match'])
    ax2.set_yticklabels(['Actual\nMatch', 'Actual\nNo Match'])
    ax2.set_title('Baseline Algorithm\nConfusion Matrix', fontsize=12, fontweight='bold')
    
    for i in range(2):
        for j in range(2):
            ax2.text(j, i, str(baseline_matrix[i, j]),
                    ha="center", va="center", color="white" if baseline_matrix[i, j] > baseline_matrix.max()/2 else "black",
                    fontsize=20, fontweight='bold')
    
    plt.tight_layout()
    output_file = 'visualizations/confusion_matrices.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved to: {output_file}")

def create_threshold_analysis_chart(threshold_results):
    """Create chart showing performance across thresholds"""
    
    if not threshold_results:
        return
    
    print("📊 Creating threshold analysis chart...")
    
    thresholds = []
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    
    for result in threshold_results:
        if 'threshold' in result:
            thresholds.append(result['threshold'])
            metrics = result['metrics']
            accuracies.append(metrics['accuracy'])
            precisions.append(metrics['precision'])
            recalls.append(metrics['recall'])
            f1_scores.append(metrics['f1_score'])
    
    if not thresholds:
        print("⚠ No threshold data found")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(thresholds, accuracies, marker='o', label='Accuracy', linewidth=2)
    ax.plot(thresholds, precisions, marker='s', label='Precision', linewidth=2)
    ax.plot(thresholds, recalls, marker='^', label='Recall', linewidth=2)
    ax.plot(thresholds, f1_scores, marker='d', label='F1-Score', linewidth=2)
    
    ax.set_xlabel('Threshold', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Performance Metrics vs Matching Threshold', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1.0])
    
    plt.tight_layout()
    output_file = 'visualizations/threshold_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved to: {output_file}")

def create_score_distribution_chart(threshold_results):
    """Create score distribution histogram"""
    
    if not threshold_results:
        return
    
    print("📊 Creating score distribution chart...")
    
    # Use first threshold result
    result = threshold_results[0]
    
    if 'distribution' in result and 'distribution' in result['distribution']:
        dist = result['distribution']['distribution']
        
        ranges = list(dist.keys())
        counts = list(dist.values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(ranges, counts, color='#3b82f6', edgecolor='black', linewidth=1.2)
        
        ax.set_xlabel('Score Range', fontsize=12)
        ax.set_ylabel('Number of Test Cases', fontsize=12)
        ax.set_title('Distribution of Match Scores', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        output_file = 'visualizations/score_distribution.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved to: {output_file}")

def create_all_visualizations():
    """Generate all visualizations for research paper"""
    
    print("=" * 80)
    print("GENERATING VISUALIZATIONS FOR RESEARCH PAPER")
    print("EmpowerTech Solutions")
    print("=" * 80)
    print()
    
    # Load comparison results
    comparison_results = load_latest_comparison()
    threshold_results = load_threshold_results()
    
    if not comparison_results:
        print("\n❌ No comparison results found.")
        print("   Run: python run_comparative_evaluation.py first")
        return
    
    # Create output directory
    os.makedirs('visualizations', exist_ok=True)
    
    # Generate all charts
    create_comparison_chart(comparison_results)
    create_improvement_chart(comparison_results)
    create_confusion_matrix_charts(comparison_results)
    
    if threshold_results:
        create_threshold_analysis_chart(threshold_results)
        create_score_distribution_chart(threshold_results)
    
    print("\n" + "=" * 80)
    print("VISUALIZATION GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("✓ All visualizations saved to: visualizations/")
    print()
    print("Generated files:")
    print("  1. comparison_chart.png - ML vs Baseline comparison")
    print("  2. improvement_chart.png - Improvement percentages")
    print("  3. confusion_matrices.png - Confusion matrices for both algorithms")
    
    if threshold_results:
        print("  4. threshold_analysis.png - Performance across thresholds")
        print("  5. score_distribution.png - Distribution of match scores")
    
    print()
    print("📄 These charts can be included in your research paper!")
    print("=" * 80)

if __name__ == '__main__':
    try:
        create_all_visualizations()
    except Exception as e:
        print(f"\n❌ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure matplotlib is installed:")
        print("  pip install matplotlib")
