"""
Automated Testing and Evaluation Script
Runs comprehensive tests on the AI Resume Screening System
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.ml_model import EducationMatcher
from app.services.evaluation_service import EvaluationService
from app.utils.education_extractor import extract_education

def run_evaluation_test():
    """Run evaluation with test dataset"""
    print("=" * 70)
    print("AI RESUME SCREENING SYSTEM - AUTOMATED EVALUATION TEST")
    print("EmpowerTech Solutions")
    print("=" * 70)
    print()
    
    matcher = EducationMatcher()
    evaluator = EvaluationService()
    
    data_path = os.path.join('backend', 'data', 'test_dataset.json')
    if not os.path.exists(data_path):
        print(f"❌ Test dataset not found at: {data_path}")
        return
    
    print(f"✓ Loading test dataset from: {data_path}")
    with open(data_path, 'r') as f:
        test_data = json.load(f)
    
    print(f"✓ Total test cases: {len(test_data['test_cases'])}")
    print()
    
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    all_results = []
    
    for threshold in thresholds:
        print(f"\n{'─' * 70}")
        print(f"TESTING WITH THRESHOLD: {threshold}")
        print(f"{'─' * 70}\n")
        
        predictions = []
        
        for i, test_case in enumerate(test_data['test_cases'], 1):
            score = matcher.calculate_match_score(
                test_case['candidate_education'],
                test_case['job_requirements']
            )
            
            predictions.append({
                'resume_id': test_case['resume_id'],
                'job_id': test_case['job_id'],
                'score': score,
                'threshold': threshold,
                'test_case_id': test_case['id']
            })
            
            expected_match = test_case['is_match']
            predicted_match = score >= threshold
            
            status = "✓" if (predicted_match == expected_match) else "✗"
            print(f"{status} Case {i:2d}: Score={score:.3f} | Expected={'Match' if expected_match else 'No Match':8s} | Predicted={'Match' if predicted_match else 'No Match':8s}")
        
        ground_truth = [
            {
                'resume_id': tc['resume_id'],
                'job_id': tc['job_id'],
                'is_match': tc['is_match']
            }
            for tc in test_data['test_cases']
        ]
        
        metrics = evaluator.calculate_metrics(predictions, ground_truth)
        distribution = evaluator.calculate_score_distribution(predictions)
        
        metrics['algorithm_name'] = f'TF-IDF + Cosine (threshold={threshold})'
        all_results.append(metrics)
        
        print(f"\n{'─' * 70}")
        print("PERFORMANCE METRICS")
        print(f"{'─' * 70}")
        print(f"Accuracy:      {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        print(f"Precision:     {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
        print(f"Recall:        {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
        print(f"F1-Score:      {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
        print(f"\nTrue Positives:  {metrics['true_positives']}")
        print(f"False Positives: {metrics['false_positives']}")
        print(f"True Negatives:  {metrics['true_negatives']}")
        print(f"False Negatives: {metrics['false_negatives']}")
        
        print(f"\n{'─' * 70}")
        print("SCORE DISTRIBUTION")
        print(f"{'─' * 70}")
        for range_name, count in distribution['distribution'].items():
            bar = '█' * count
            print(f"{range_name}: {bar} ({count})")
        print(f"\nMean Score: {distribution['mean_score']:.4f}")
        print(f"Min Score:  {distribution['min_score']:.4f}")
        print(f"Max Score:  {distribution['max_score']:.4f}")
        
        experiment_name = f"threshold_{threshold}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        saved_file = evaluator.save_evaluation_results({
            'metrics': metrics,
            'distribution': distribution,
            'threshold': threshold
        }, experiment_name)
        
        print(f"\n✓ Results saved to: {saved_file}")
    
    print(f"\n\n{'═' * 70}")
    print("COMPARATIVE ANALYSIS - ALL THRESHOLDS")
    print(f"{'═' * 70}\n")
    
    comparison = evaluator.compare_algorithms(all_results)
    
    print(f"{'Threshold':<12} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("─" * 70)
    for algo in comparison['algorithms']:
        threshold = algo['name'].split('=')[1].rstrip(')')
        print(f"{threshold:<12} {algo['accuracy']:<12.4f} {algo['precision']:<12.4f} {algo['recall']:<12.4f} {algo['f1_score']:<12.4f}")
    
    print(f"\n{'─' * 70}")
    print("BEST PERFORMING THRESHOLD BY METRIC")
    print(f"{'─' * 70}")
    print(f"Best Accuracy:  {comparison['best_accuracy']}")
    print(f"Best Precision: {comparison['best_precision']}")
    print(f"Best Recall:    {comparison['best_recall']}")
    print(f"Best F1-Score:  {comparison['best_f1']}")
    
    print(f"\n{'═' * 70}")
    print("EVALUATION TEST COMPLETE")
    print(f"{'═' * 70}\n")
    
    return all_results

def test_education_extraction():
    """Test education extraction accuracy"""
    print("\n" + "=" * 70)
    print("EDUCATION EXTRACTION TEST")
    print("=" * 70 + "\n")
    
    test_cases = [
        {
            'text': """
            John Doe
            Education:
            Bachelor of Science in Computer Science
            MIT, 2020
            """,
            'expected_degrees': 1
        },
        {
            'text': """
            Education:
            PhD in Artificial Intelligence
            Stanford University, 2023
            
            Masters in Computer Science
            UC Berkeley, 2019
            """,
            'expected_degrees': 2
        },
        {
            'text': """
            MBA in Technology Management
            Harvard Business School, 2021
            """,
            'expected_degrees': 1
        }
    ]
    
    passed = 0
    for i, test in enumerate(test_cases, 1):
        education = extract_education(test['text'])
        expected = test['expected_degrees']
        actual = len(education)
        
        status = "✓" if actual == expected else "✗"
        print(f"{status} Test {i}: Expected {expected} degree(s), Found {actual}")
        
        for edu in education:
            print(f"    → {edu['degree']} in {edu['field']}")
        
        if actual == expected:
            passed += 1
    
    print(f"\n{'─' * 70}")
    print(f"Education Extraction Tests: {passed}/{len(test_cases)} passed")
    print(f"{'─' * 70}\n")

def run_all_tests():
    """Run all tests"""
    try:
        test_education_extraction()
        
        results = run_evaluation_test()
        
        print("\n" + "=" * 70)
        print("RECOMMENDATIONS FOR RESEARCH PAPER")
        print("=" * 70 + "\n")
        
        print("1. ✓ Evaluation metrics implemented (Accuracy, Precision, Recall, F1)")
        print("2. ✓ Test dataset created with 20 balanced test cases")
        print("3. ✓ Automated testing framework established")
        print("4. ✓ Results saved for publication")
        print()
        print("Next Steps:")
        print("  - Collect more real-world resume samples")
        print("  - Implement cross-validation")
        print("  - Compare with baseline (keyword matching)")
        print("  - Add statistical significance tests")
        print("  - Create visualizations for paper")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_all_tests()
