"""
Cross-Validation for Resume Screening System
Implements k-fold cross-validation for robust performance evaluation
"""

import sys
import os
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.ml_model import EducationMatcher
from app.services.evaluation_service import EvaluationService

def split_dataset(test_cases: List[Dict], k: int = 5) -> List[Tuple[List[Dict], List[Dict]]]:
    """
    Split dataset into k folds
    
    Args:
        test_cases: List of all test cases
        k: Number of folds
    
    Returns:
        List of (train, test) tuples
    """
    n = len(test_cases)
    fold_size = n // k
    folds = []
    
    # Shuffle indices
    indices = list(range(n))
    np.random.seed(42)  # For reproducibility
    np.random.shuffle(indices)
    
    for i in range(k):
        start_idx = i * fold_size
        end_idx = start_idx + fold_size if i < k - 1 else n
        
        test_indices = indices[start_idx:end_idx]
        train_indices = [idx for idx in indices if idx not in test_indices]
        
        test_fold = [test_cases[idx] for idx in test_indices]
        train_fold = [test_cases[idx] for idx in train_indices]
        
        folds.append((train_fold, test_fold))
    
    return folds

def run_cross_validation(k: int = 5, threshold: float = 0.5):
    """
    Run k-fold cross-validation
    
    Args:
        k: Number of folds
        threshold: Matching threshold
    """
    
    print("=" * 80)
    print(f"{k}-FOLD CROSS-VALIDATION")
    print("EmpowerTech Solutions - Research Evaluation")
    print("=" * 80)
    print()
    
    # Load test dataset
    data_path = os.path.join('backend', 'data', 'test_dataset.json')
    if not os.path.exists(data_path):
        print(f"❌ Test dataset not found at: {data_path}")
        return
    
    print(f"✓ Loading test dataset from: {data_path}")
    with open(data_path, 'r') as f:
        test_data = json.load(f)
    
    test_cases = test_data['test_cases']
    print(f"✓ Total test cases: {len(test_cases)}")
    print(f"✓ Number of folds: {k}")
    print(f"✓ Threshold: {threshold}")
    print()
    
    # Split into folds
    folds = split_dataset(test_cases, k)
    
    matcher = EducationMatcher()
    evaluator = EvaluationService()
    
    fold_results = []
    
    print(f"{'─' * 80}")
    print("RUNNING CROSS-VALIDATION")
    print(f"{'─' * 80}\n")
    
    for fold_num, (train_fold, test_fold) in enumerate(folds, 1):
        print(f"Fold {fold_num}/{k} (Train: {len(train_fold)}, Test: {len(test_fold)})")
        
        # Run on test fold
        predictions = []
        ground_truth = []
        
        for test_case in test_fold:
            score = matcher.calculate_match_score(
                test_case['candidate_education'],
                test_case['job_requirements']
            )
            
            predictions.append({
                'resume_id': test_case['resume_id'],
                'job_id': test_case['job_id'],
                'score': score,
                'threshold': threshold
            })
            
            ground_truth.append({
                'resume_id': test_case['resume_id'],
                'job_id': test_case['job_id'],
                'is_match': test_case['is_match']
            })
        
        # Calculate metrics for this fold
        metrics = evaluator.calculate_metrics(predictions, ground_truth)
        fold_results.append(metrics)
        
        print(f"  Accuracy: {metrics['accuracy']:.4f}, Precision: {metrics['precision']:.4f}, "
              f"Recall: {metrics['recall']:.4f}, F1: {metrics['f1_score']:.4f}")
        print()
    
    # Calculate mean and standard deviation
    print(f"{'═' * 80}")
    print("CROSS-VALIDATION RESULTS")
    print(f"{'═' * 80}\n")
    
    metrics_names = ['accuracy', 'precision', 'recall', 'f1_score']
    
    print(f"{'Metric':<15} {'Mean':<12} {'Std Dev':<12} {'Min':<12} {'Max':<12}")
    print("─" * 80)
    
    cv_summary = {}
    
    for metric in metrics_names:
        values = [fold[metric] for fold in fold_results]
        mean_val = np.mean(values)
        std_val = np.std(values)
        min_val = np.min(values)
        max_val = np.max(values)
        
        cv_summary[metric] = {
            'mean': float(mean_val),
            'std': float(std_val),
            'min': float(min_val),
            'max': float(max_val),
            'values': [float(v) for v in values]
        }
        
        print(f"{metric.capitalize():<15} {mean_val:.4f}      {std_val:.4f}      {min_val:.4f}      {max_val:.4f}")
    
    print(f"\n{'─' * 80}")
    print("STATISTICAL INTERPRETATION")
    print(f"{'─' * 80}\n")
    
    for metric in metrics_names:
        mean = cv_summary[metric]['mean']
        std = cv_summary[metric]['std']
        confidence_interval = 1.96 * std  # 95% confidence interval
        
        print(f"{metric.capitalize()}:")
        print(f"  Mean: {mean:.4f} ({mean*100:.2f}%)")
        print(f"  95% CI: [{mean - confidence_interval:.4f}, {mean + confidence_interval:.4f}]")
        print(f"  Std Dev: {std:.4f} (Variance: {std**2:.6f})")
        print()
    
    # Save results
    cv_results = {
        'timestamp': datetime.now().isoformat(),
        'k_folds': k,
        'threshold': threshold,
        'total_cases': len(test_cases),
        'fold_results': fold_results,
        'summary': cv_summary
    }
    
    os.makedirs('backend/evaluation_results', exist_ok=True)
    output_file = f"backend/evaluation_results/cross_validation_{k}fold_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(cv_results, f, indent=2)
    
    print(f"{'═' * 80}")
    print("ROBUSTNESS ASSESSMENT")
    print(f"{'═' * 80}\n")
    
    # Assess consistency
    for metric in metrics_names:
        std = cv_summary[metric]['std']
        mean = cv_summary[metric]['mean']
        cv_coefficient = (std / mean * 100) if mean > 0 else 0
        
        if cv_coefficient < 5:
            consistency = "Excellent"
            symbol = "✓✓"
        elif cv_coefficient < 10:
            consistency = "Good"
            symbol = "✓"
        elif cv_coefficient < 15:
            consistency = "Moderate"
            symbol = "~"
        else:
            consistency = "Poor"
            symbol = "✗"
        
        print(f"{symbol} {metric.capitalize()}: {consistency} (CV = {cv_coefficient:.2f}%)")
    
    print(f"\n✓ Results saved to: {output_file}")
    print(f"\n{'═' * 80}")
    print("CONCLUSION")
    print(f"{'═' * 80}\n")
    
    overall_mean = np.mean([cv_summary[m]['mean'] for m in metrics_names])
    overall_std = np.mean([cv_summary[m]['std'] for m in metrics_names])
    
    print(f"Overall Performance: {overall_mean:.4f} ± {overall_std:.4f}")
    
    if overall_std < 0.05:
        print("✓ The model shows EXCELLENT stability across different data splits.")
        print("  Results are highly reliable and reproducible.")
    elif overall_std < 0.1:
        print("✓ The model shows GOOD stability across different data splits.")
        print("  Results are reliable for publication.")
    else:
        print("⚠ The model shows MODERATE variability across different data splits.")
        print("  Consider collecting more data or adjusting the algorithm.")
    
    print(f"\n{'═' * 80}\n")
    
    return cv_results

def generate_cv_latex_table(results: Dict):
    """Generate LaTeX table for cross-validation results"""
    
    print("\n" + "=" * 80)
    print("LaTeX TABLE FOR CROSS-VALIDATION RESULTS")
    print("=" * 80 + "\n")
    
    summary = results['summary']
    
    latex = r"""
\begin{table}[h]
\centering
\caption{""" + str(results['k_folds']) + r"""-Fold Cross-Validation Results}
\label{tab:crossvalidation}
\begin{tabular}{|l|c|c|c|}
\hline
\textbf{Metric} & \textbf{Mean} & \textbf{Std Dev} & \textbf{95\% CI} \\
\hline
"""
    
    for metric in ['accuracy', 'precision', 'recall', 'f1_score']:
        mean = summary[metric]['mean']
        std = summary[metric]['std']
        ci = 1.96 * std
        
        metric_name = metric.replace('_', '-').capitalize()
        latex += f"{metric_name} & {mean:.4f} & {std:.4f} & [{mean-ci:.4f}, {mean+ci:.4f}] \\\\\n"
    
    latex += r"""\hline
\end{tabular}
\end{table}
"""
    
    print(latex)
    print("\n" + "=" * 80)
    print("Copy the above LaTeX code into your research paper")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run k-fold cross-validation')
    parser.add_argument('--k', type=int, default=5, help='Number of folds (default: 5)')
    parser.add_argument('--threshold', type=float, default=0.5, help='Matching threshold (default: 0.5)')
    
    args = parser.parse_args()
    
    try:
        results = run_cross_validation(k=args.k, threshold=args.threshold)
        if results:
            generate_cv_latex_table(results)
    except Exception as e:
        print(f"\n❌ Error during cross-validation: {e}")
        import traceback
        traceback.print_exc()
