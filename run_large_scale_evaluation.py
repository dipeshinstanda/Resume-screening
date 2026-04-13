"""
High-Performance Evaluation for Large Datasets
Optimized for 10K+ test cases with progress tracking
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List
from multiprocessing import Pool, cpu_count

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.enhanced_ml_model import EnhancedEducationMatcher
from app.models.baseline_matcher import KeywordMatcher
from app.services.evaluation_service import EvaluationService

class LargeScaleEvaluator:
    """Efficient evaluator for large datasets"""
    
    def __init__(self, use_enhanced=True):
        self.matcher = EnhancedEducationMatcher() if use_enhanced else None
        self.baseline_matcher = KeywordMatcher()
        self.evaluator = EvaluationService()
        self.use_enhanced = use_enhanced
    
    def evaluate_single_case(self, test_case: Dict, threshold: float) -> Dict:
        """Evaluate a single test case"""
        try:
            if self.use_enhanced:
                score = self.matcher.calculate_match_score(
                    test_case['candidate_education'],
                    test_case['job_requirements'],
                    test_case.get('candidate_skills'),
                    test_case.get('job_skills')
                )
            else:
                score = self.baseline_matcher.calculate_match_score(
                    test_case['candidate_education'],
                    test_case['job_requirements']
                )
            
            return {
                'resume_id': test_case['resume_id'],
                'job_id': test_case['job_id'],
                'score': score,
                'threshold': threshold,
                'test_case_id': test_case['id'],
                'predicted_match': score >= threshold,
                'actual_match': test_case['is_match']
            }
        except Exception as e:
            print(f"Error evaluating case {test_case.get('id')}: {e}")
            return None
    
    def run_evaluation(
        self,
        dataset_path: str,
        threshold: float = 0.5,
        sample_size: int = None,
        save_predictions: bool = False
    ) -> Dict:
        """
        Run evaluation on large dataset
        
        Args:
            dataset_path: Path to test dataset JSON
            threshold: Matching threshold
            sample_size: If set, evaluate only a sample
            save_predictions: Whether to save detailed predictions
        
        Returns:
            Evaluation results dictionary
        """
        print("\n" + "=" * 80)
        print("LARGE-SCALE EVALUATION")
        print("EmpowerTech Solutions - High-Performance Testing")
        print("=" * 80 + "\n")
        
        # Load dataset
        print(f"✓ Loading dataset from: {dataset_path}")
        start_load = time.time()
        
        with open(dataset_path, 'r') as f:
            test_data = json.load(f)
        
        load_time = time.time() - start_load
        print(f"✓ Loaded {len(test_data['test_cases']):,} cases in {load_time:.2f}s\n")
        
        # Sample if requested
        test_cases = test_data['test_cases']
        if sample_size and sample_size < len(test_cases):
            import random
            random.seed(42)
            test_cases = random.sample(test_cases, sample_size)
            print(f"✓ Using sample of {len(test_cases):,} cases\n")
        
        # Evaluate
        print(f"{'─' * 80}")
        print(f"RUNNING EVALUATION (Threshold = {threshold})")
        print(f"Algorithm: {'Enhanced ML' if self.use_enhanced else 'Baseline'}")
        print(f"{'─' * 80}\n")
        
        predictions = []
        start_eval = time.time()
        
        total = len(test_cases)
        checkpoint = max(total // 20, 1)  # Update every 5%
        
        for i, test_case in enumerate(test_cases, 1):
            prediction = self.evaluate_single_case(test_case, threshold)
            if prediction:
                predictions.append(prediction)
            
            # Progress update
            if i % checkpoint == 0 or i == total:
                progress = (i / total) * 100
                elapsed = time.time() - start_eval
                rate = i / elapsed if elapsed > 0 else 0
                eta = (total - i) / rate if rate > 0 else 0
                
                print(f"Progress: {i:,}/{total:,} ({progress:.1f}%) | "
                      f"Rate: {rate:.0f} cases/s | ETA: {eta:.0f}s")
        
        eval_time = time.time() - start_eval
        
        # Prepare ground truth
        ground_truth = [
            {
                'resume_id': tc['resume_id'],
                'job_id': tc['job_id'],
                'is_match': tc['is_match']
            }
            for tc in test_cases
        ]
        
        # Calculate metrics
        print(f"\n{'─' * 80}")
        print("CALCULATING METRICS")
        print(f"{'─' * 80}\n")
        
        metrics = self.evaluator.calculate_metrics(predictions, ground_truth)
        distribution = self.evaluator.calculate_score_distribution(predictions)
        
        # Calculate accuracy by difficulty
        difficulty_metrics = self._calculate_difficulty_metrics(test_cases, predictions)
        
        # Results
        results = {
            'timestamp': datetime.now().isoformat(),
            'dataset': dataset_path,
            'algorithm': 'Enhanced ML' if self.use_enhanced else 'Baseline',
            'total_cases': len(test_cases),
            'threshold': threshold,
            'evaluation_time': eval_time,
            'cases_per_second': len(test_cases) / eval_time,
            'metrics': metrics,
            'distribution': distribution,
            'difficulty_breakdown': difficulty_metrics
        }
        
        if save_predictions:
            results['predictions'] = predictions[:100]  # Save first 100
        
        # Display results
        print(f"\n{'═' * 80}")
        print("EVALUATION RESULTS")
        print(f"{'═' * 80}\n")
        
        print(f"Dataset: {os.path.basename(dataset_path)}")
        print(f"Test Cases: {len(test_cases):,}")
        print(f"Evaluation Time: {eval_time:.2f}s")
        print(f"Processing Rate: {len(test_cases)/eval_time:.0f} cases/second")
        print(f"\n{'─' * 80}")
        print("PERFORMANCE METRICS")
        print(f"{'─' * 80}\n")
        
        print(f"Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        print(f"Precision: {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
        print(f"Recall:    {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
        print(f"F1-Score:  {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
        
        print(f"\n{'─' * 80}")
        print("CONFUSION MATRIX")
        print(f"{'─' * 80}\n")
        
        print(f"True Positives:  {metrics['true_positives']:,}")
        print(f"False Positives: {metrics['false_positives']:,}")
        print(f"True Negatives:  {metrics['true_negatives']:,}")
        print(f"False Negatives: {metrics['false_negatives']:,}")
        
        if difficulty_metrics:
            print(f"\n{'─' * 80}")
            print("PERFORMANCE BY DIFFICULTY")
            print(f"{'─' * 80}\n")
            
            for difficulty, metrics_diff in difficulty_metrics.items():
                print(f"{difficulty.upper()}:")
                print(f"  Accuracy: {metrics_diff['accuracy']:.4f}")
                print(f"  Cases: {metrics_diff['count']:,}")
        
        # Save results
        os.makedirs('backend/evaluation_results', exist_ok=True)
        output_file = f"backend/evaluation_results/large_eval_{len(test_cases)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}")
        print(f"\n{'═' * 80}\n")
        
        return results
    
    def _calculate_difficulty_metrics(
        self,
        test_cases: List[Dict],
        predictions: List[Dict]
    ) -> Dict:
        """Calculate metrics broken down by difficulty"""
        difficulty_data = {}
        
        for test_case in test_cases:
            difficulty = test_case.get('difficulty', 'unknown')
            if difficulty not in difficulty_data:
                difficulty_data[difficulty] = {'predictions': [], 'ground_truth': []}
        
        # Organize by difficulty
        pred_dict = {f"{p['resume_id']}_{p['job_id']}": p for p in predictions}
        
        for test_case in test_cases:
            difficulty = test_case.get('difficulty', 'unknown')
            key = f"{test_case['resume_id']}_{test_case['job_id']}"
            
            if key in pred_dict:
                difficulty_data[difficulty]['predictions'].append(pred_dict[key])
                difficulty_data[difficulty]['ground_truth'].append({
                    'resume_id': test_case['resume_id'],
                    'job_id': test_case['job_id'],
                    'is_match': test_case['is_match']
                })
        
        # Calculate metrics for each difficulty
        difficulty_metrics = {}
        
        for difficulty, data in difficulty_data.items():
            if data['predictions']:
                metrics = self.evaluator.calculate_metrics(
                    data['predictions'],
                    data['ground_truth']
                )
                difficulty_metrics[difficulty] = {
                    'accuracy': metrics['accuracy'],
                    'precision': metrics['precision'],
                    'recall': metrics['recall'],
                    'f1_score': metrics['f1_score'],
                    'count': len(data['predictions'])
                }
        
        return difficulty_metrics


def run_large_scale_comparative_evaluation(
    dataset_path: str,
    threshold: float = 0.5,
    sample_size: int = None
):
    """Run comparative evaluation on large dataset"""
    
    print("\n" + "=" * 80)
    print("LARGE-SCALE COMPARATIVE EVALUATION")
    print("Enhanced ML vs Baseline on Large Dataset")
    print("=" * 80 + "\n")
    
    # Load dataset info
    with open(dataset_path, 'r') as f:
        test_data = json.load(f)
    
    total_cases = len(test_data['test_cases'])
    eval_size = sample_size if sample_size else total_cases
    
    print(f"Dataset: {os.path.basename(dataset_path)}")
    print(f"Total Cases: {total_cases:,}")
    print(f"Evaluating: {eval_size:,} cases")
    print(f"Threshold: {threshold}\n")
    
    # Evaluate Enhanced ML
    print("=" * 80)
    print("PHASE 1: Enhanced ML Algorithm")
    print("=" * 80)
    
    ml_evaluator = LargeScaleEvaluator(use_enhanced=True)
    ml_results = ml_evaluator.run_evaluation(dataset_path, threshold, sample_size)
    
    # Evaluate Baseline
    print("\n" + "=" * 80)
    print("PHASE 2: Baseline Algorithm")
    print("=" * 80)
    
    baseline_evaluator = LargeScaleEvaluator(use_enhanced=False)
    baseline_results = baseline_evaluator.run_evaluation(dataset_path, threshold, sample_size)
    
    # Compare
    print("\n" + "=" * 80)
    print("COMPARATIVE ANALYSIS")
    print("=" * 80 + "\n")
    
    print(f"{'Metric':<15} {'Enhanced ML':<15} {'Baseline':<15} {'Improvement':<15}")
    print("─" * 80)
    
    metrics_to_compare = ['accuracy', 'precision', 'recall', 'f1_score']
    
    for metric in metrics_to_compare:
        ml_val = ml_results['metrics'][metric]
        base_val = baseline_results['metrics'][metric]
        improvement = ((ml_val - base_val) / base_val * 100) if base_val > 0 else 0
        
        print(f"{metric.capitalize():<15} {ml_val:.4f}         {base_val:.4f}         {improvement:+.2f}%")
    
    # Save comparison
    comparison = {
        'timestamp': datetime.now().isoformat(),
        'dataset': dataset_path,
        'cases_evaluated': eval_size,
        'threshold': threshold,
        'enhanced_ml': ml_results['metrics'],
        'baseline': baseline_results['metrics'],
        'improvement': {
            metric: ((ml_results['metrics'][metric] - baseline_results['metrics'][metric]) / 
                    baseline_results['metrics'][metric] * 100) 
                    if baseline_results['metrics'][metric] > 0 else 0
            for metric in metrics_to_compare
        },
        'performance': {
            'enhanced_ml_rate': ml_results['cases_per_second'],
            'baseline_rate': baseline_results['cases_per_second']
        }
    }
    
    output_file = f"backend/evaluation_results/large_comparison_{eval_size}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print(f"\n✓ Comparison saved to: {output_file}")
    
    # Winner
    ml_avg = sum([ml_results['metrics'][m] for m in metrics_to_compare]) / len(metrics_to_compare)
    base_avg = sum([baseline_results['metrics'][m] for m in metrics_to_compare]) / len(metrics_to_compare)
    
    print(f"\n{'─' * 80}")
    if ml_avg > base_avg:
        print(f"🏆 WINNER: Enhanced ML Algorithm")
        print(f"   Average Score: {ml_avg:.4f} vs {base_avg:.4f}")
        print(f"   Improvement: {((ml_avg - base_avg) / base_avg * 100):+.2f}%")
    else:
        print(f"🏆 WINNER: Baseline Algorithm")
        print(f"   Average Score: {base_avg:.4f} vs {ml_avg:.4f}")
    
    print(f"{'─' * 80}\n")
    
    return comparison


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Large-scale evaluation')
    parser.add_argument('--dataset', type=str, 
                       default='backend/data/large_test_dataset.json',
                       help='Path to test dataset')
    parser.add_argument('--threshold', type=float, default=0.5,
                       help='Matching threshold')
    parser.add_argument('--sample', type=int, default=None,
                       help='Sample size (for testing)')
    parser.add_argument('--compare', action='store_true',
                       help='Run comparative evaluation')
    parser.add_argument('--enhanced', action='store_true', default=True,
                       help='Use enhanced ML model')
    
    args = parser.parse_args()
    
    try:
        if args.compare:
            results = run_large_scale_comparative_evaluation(
                args.dataset,
                args.threshold,
                args.sample
            )
        else:
            evaluator = LargeScaleEvaluator(use_enhanced=args.enhanced)
            results = evaluator.run_evaluation(
                args.dataset,
                args.threshold,
                args.sample
            )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
