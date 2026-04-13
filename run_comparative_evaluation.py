"""
Comparative Evaluation Script
Compare ML-based (TF-IDF) vs Baseline (Keyword) matching algorithms
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.ml_model import EducationMatcher
from app.models.baseline_matcher import KeywordMatcher
from app.services.evaluation_service import EvaluationService

def run_comparative_evaluation():
    """Run side-by-side comparison of both algorithms"""
    
    print("=" * 80)
    print("COMPARATIVE EVALUATION: ML-BASED vs BASELINE KEYWORD MATCHING")
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
    
    print(f"✓ Total test cases: {len(test_data['test_cases'])}")
    print()
    
    # Initialize both matchers
    ml_matcher = EducationMatcher()
    baseline_matcher = KeywordMatcher()
    evaluator = EvaluationService()
    
    threshold = 0.5  # Standard threshold
    
    # Test both algorithms
    ml_predictions = []
    baseline_predictions = []
    
    print(f"{'─' * 80}")
    print(f"RUNNING BOTH ALGORITHMS (Threshold = {threshold})")
    print(f"{'─' * 80}\n")
    
    print(f"{'Case':<6} {'ML Score':<12} {'Baseline Score':<15} {'Expected':<10} {'ML Result':<12} {'Baseline Result'}")
    print("─" * 80)
    
    for i, test_case in enumerate(test_data['test_cases'], 1):
        # ML-based matching
        ml_score = ml_matcher.calculate_match_score(
            test_case['candidate_education'],
            test_case['job_requirements']
        )
        
        # Baseline keyword matching
        baseline_score = baseline_matcher.calculate_match_score(
            test_case['candidate_education'],
            test_case['job_requirements']
        )
        
        ml_predictions.append({
            'resume_id': test_case['resume_id'],
            'job_id': test_case['job_id'],
            'score': ml_score,
            'threshold': threshold,
            'test_case_id': test_case['id']
        })
        
        baseline_predictions.append({
            'resume_id': test_case['resume_id'],
            'job_id': test_case['job_id'],
            'score': baseline_score,
            'threshold': threshold,
            'test_case_id': test_case['id']
        })
        
        expected = "Match" if test_case['is_match'] else "No Match"
        ml_result = "Match" if ml_score >= threshold else "No Match"
        baseline_result = "Match" if baseline_score >= threshold else "No Match"
        
        ml_status = "✓" if (ml_score >= threshold) == test_case['is_match'] else "✗"
        baseline_status = "✓" if (baseline_score >= threshold) == test_case['is_match'] else "✗"
        
        print(f"{i:<6} {ml_score:.3f} {ml_status:<7} {baseline_score:.3f} {baseline_status:<10} {expected:<10} {ml_result:<12} {baseline_result}")
    
    # Prepare ground truth
    ground_truth = [
        {
            'resume_id': tc['resume_id'],
            'job_id': tc['job_id'],
            'is_match': tc['is_match']
        }
        for tc in test_data['test_cases']
    ]
    
    # Calculate metrics for both
    ml_metrics = evaluator.calculate_metrics(ml_predictions, ground_truth)
    baseline_metrics = evaluator.calculate_metrics(baseline_predictions, ground_truth)
    
    ml_metrics['algorithm_name'] = 'ML-Based (TF-IDF + Cosine)'
    baseline_metrics['algorithm_name'] = 'Baseline (Keyword Matching)'
    
    # Display comparison
    print(f"\n{'═' * 80}")
    print("PERFORMANCE COMPARISON")
    print(f"{'═' * 80}\n")
    
    print(f"{'Metric':<20} {'ML-Based':<20} {'Baseline':<20} {'Improvement':<15}")
    print("─" * 80)
    
    metrics_to_compare = ['accuracy', 'precision', 'recall', 'f1_score']
    
    for metric in metrics_to_compare:
        ml_value = ml_metrics[metric]
        baseline_value = baseline_metrics[metric]
        improvement = ((ml_value - baseline_value) / baseline_value * 100) if baseline_value > 0 else 0
        
        print(f"{metric.capitalize():<20} {ml_value:.4f} ({ml_value*100:.2f}%){'':<3} {baseline_value:.4f} ({baseline_value*100:.2f}%){'':<3} {improvement:+.2f}%")
    
    print(f"\n{'─' * 80}")
    print("CONFUSION MATRIX COMPARISON")
    print(f"{'─' * 80}\n")
    
    print("ML-Based Algorithm:")
    print(f"  True Positives:  {ml_metrics['true_positives']}")
    print(f"  False Positives: {ml_metrics['false_positives']}")
    print(f"  True Negatives:  {ml_metrics['true_negatives']}")
    print(f"  False Negatives: {ml_metrics['false_negatives']}")
    
    print("\nBaseline Algorithm:")
    print(f"  True Positives:  {baseline_metrics['true_positives']}")
    print(f"  False Positives: {baseline_metrics['false_positives']}")
    print(f"  True Negatives:  {baseline_metrics['true_negatives']}")
    print(f"  False Negatives: {baseline_metrics['false_negatives']}")
    
    # Save comparison results
    comparison_results = {
        'timestamp': datetime.now().isoformat(),
        'threshold': threshold,
        'test_cases': len(test_data['test_cases']),
        'ml_based': ml_metrics,
        'baseline': baseline_metrics,
        'improvement': {
            'accuracy': ((ml_metrics['accuracy'] - baseline_metrics['accuracy']) / baseline_metrics['accuracy'] * 100) if baseline_metrics['accuracy'] > 0 else 0,
            'precision': ((ml_metrics['precision'] - baseline_metrics['precision']) / baseline_metrics['precision'] * 100) if baseline_metrics['precision'] > 0 else 0,
            'recall': ((ml_metrics['recall'] - baseline_metrics['recall']) / baseline_metrics['recall'] * 100) if baseline_metrics['recall'] > 0 else 0,
            'f1_score': ((ml_metrics['f1_score'] - baseline_metrics['f1_score']) / baseline_metrics['f1_score'] * 100) if baseline_metrics['f1_score'] > 0 else 0
        }
    }
    
    os.makedirs('backend/evaluation_results', exist_ok=True)
    output_file = f"backend/evaluation_results/comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(comparison_results, f, indent=2)
    
    print(f"\n{'═' * 80}")
    print("STATISTICAL SUMMARY")
    print(f"{'═' * 80}\n")
    
    print(f"✓ Results saved to: {output_file}")
    print(f"\nOverall Improvement of ML-Based vs Baseline:")
    for metric in metrics_to_compare:
        improvement = comparison_results['improvement'][metric]
        symbol = "↑" if improvement > 0 else "↓" if improvement < 0 else "→"
        print(f"  {symbol} {metric.capitalize()}: {improvement:+.2f}%")
    
    # Determine winner
    print(f"\n{'─' * 80}")
    ml_score = sum([ml_metrics[m] for m in metrics_to_compare]) / len(metrics_to_compare)
    baseline_score = sum([baseline_metrics[m] for m in metrics_to_compare]) / len(metrics_to_compare)
    
    if ml_score > baseline_score:
        print("🏆 WINNER: ML-Based Algorithm (TF-IDF + Cosine Similarity)")
        print(f"   Average Score: {ml_score:.4f} vs {baseline_score:.4f}")
    elif baseline_score > ml_score:
        print("🏆 WINNER: Baseline Algorithm (Keyword Matching)")
        print(f"   Average Score: {baseline_score:.4f} vs {ml_score:.4f}")
    else:
        print("🤝 TIE: Both algorithms perform equally")
        print(f"   Average Score: {ml_score:.4f}")
    
    print(f"{'─' * 80}\n")
    
    return comparison_results

def generate_latex_table(results: Dict):
    """Generate LaTeX table for research paper"""
    
    print("\n" + "=" * 80)
    print("LaTeX TABLE FOR RESEARCH PAPER")
    print("=" * 80 + "\n")
    
    latex = r"""
\begin{table}[h]
\centering
\caption{Comparison of ML-Based vs Baseline Keyword Matching}
\label{tab:comparison}
\begin{tabular}{|l|c|c|c|}
\hline
\textbf{Metric} & \textbf{ML-Based} & \textbf{Baseline} & \textbf{Improvement} \\
\hline
"""
    
    ml = results['ml_based']
    baseline = results['baseline']
    improvement = results['improvement']
    
    latex += f"Accuracy & {ml['accuracy']:.4f} & {baseline['accuracy']:.4f} & {improvement['accuracy']:+.2f}\\% \\\\\n"
    latex += f"Precision & {ml['precision']:.4f} & {baseline['precision']:.4f} & {improvement['precision']:+.2f}\\% \\\\\n"
    latex += f"Recall & {ml['recall']:.4f} & {baseline['recall']:.4f} & {improvement['recall']:+.2f}\\% \\\\\n"
    latex += f"F1-Score & {ml['f1_score']:.4f} & {baseline['f1_score']:.4f} & {improvement['f1_score']:+.2f}\\% \\\\\n"
    
    latex += r"""\hline
\end{tabular}
\end{table}
"""
    
    print(latex)
    print("\n" + "=" * 80)
    print("Copy the above LaTeX code into your research paper")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    try:
        results = run_comparative_evaluation()
        if results:
            generate_latex_table(results)
    except Exception as e:
        print(f"\n❌ Error during comparative evaluation: {e}")
        import traceback
        traceback.print_exc()
