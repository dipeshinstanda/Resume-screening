from typing import List, Dict, Tuple
import json
from datetime import datetime
import os

class EvaluationService:
    def __init__(self):
        self.results_dir = 'evaluation_results'
        os.makedirs(self.results_dir, exist_ok=True)
    
    def calculate_metrics(self, predictions: List[Dict], ground_truth: List[Dict]) -> Dict:
        """
        Calculate accuracy, precision, recall, and F1 score
        
        Args:
            predictions: List of predicted matches with scores
            ground_truth: List of actual matches (labeled data)
        
        Returns:
            Dictionary with all evaluation metrics
        """
        if not predictions or not ground_truth:
            return {
                'accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'total_predictions': 0,
                'total_ground_truth': 0
            }
        
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        true_negatives = 0
        
        gt_dict = {f"{gt['resume_id']}_{gt['job_id']}": gt['is_match'] 
                   for gt in ground_truth}
        
        for pred in predictions:
            key = f"{pred['resume_id']}_{pred['job_id']}"
            predicted_match = pred['score'] >= pred.get('threshold', 0.5)
            actual_match = gt_dict.get(key, False)
            
            if predicted_match and actual_match:
                true_positives += 1
            elif predicted_match and not actual_match:
                false_positives += 1
            elif not predicted_match and actual_match:
                false_negatives += 1
            else:
                true_negatives += 1
        
        total = true_positives + true_negatives + false_positives + false_negatives
        accuracy = (true_positives + true_negatives) / total if total > 0 else 0
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics = {
            'accuracy': round(accuracy, 4),
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1_score, 4),
            'true_positives': true_positives,
            'false_positives': false_positives,
            'true_negatives': true_negatives,
            'false_negatives': false_negatives,
            'total_predictions': len(predictions),
            'total_ground_truth': len(ground_truth),
            'timestamp': datetime.now().isoformat()
        }
        
        return metrics
    
    def calculate_score_distribution(self, predictions: List[Dict]) -> Dict:
        """Calculate distribution of match scores"""
        if not predictions:
            return {}
        
        scores = [p['score'] for p in predictions]
        
        ranges = {
            '0.0-0.2': 0,
            '0.2-0.4': 0,
            '0.4-0.6': 0,
            '0.6-0.8': 0,
            '0.8-1.0': 0
        }
        
        for score in scores:
            if score < 0.2:
                ranges['0.0-0.2'] += 1
            elif score < 0.4:
                ranges['0.2-0.4'] += 1
            elif score < 0.6:
                ranges['0.4-0.6'] += 1
            elif score < 0.8:
                ranges['0.6-0.8'] += 1
            else:
                ranges['0.8-1.0'] += 1
        
        return {
            'distribution': ranges,
            'mean_score': round(sum(scores) / len(scores), 4),
            'min_score': round(min(scores), 4),
            'max_score': round(max(scores), 4),
            'total_predictions': len(scores)
        }
    
    def save_evaluation_results(self, metrics: Dict, experiment_name: str = None):
        """Save evaluation results to file"""
        if experiment_name is None:
            experiment_name = f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filename = os.path.join(self.results_dir, f"{experiment_name}.json")
        
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return filename
    
    def compare_algorithms(self, results: List[Dict]) -> Dict:
        """Compare multiple algorithm results"""
        comparison = {
            'algorithms': [],
            'best_accuracy': None,
            'best_precision': None,
            'best_recall': None,
            'best_f1': None
        }
        
        best_acc = 0
        best_prec = 0
        best_rec = 0
        best_f1 = 0
        
        for result in results:
            comparison['algorithms'].append({
                'name': result.get('algorithm_name', 'unknown'),
                'accuracy': result['accuracy'],
                'precision': result['precision'],
                'recall': result['recall'],
                'f1_score': result['f1_score']
            })
            
            if result['accuracy'] > best_acc:
                best_acc = result['accuracy']
                comparison['best_accuracy'] = result.get('algorithm_name')
            
            if result['precision'] > best_prec:
                best_prec = result['precision']
                comparison['best_precision'] = result.get('algorithm_name')
            
            if result['recall'] > best_rec:
                best_rec = result['recall']
                comparison['best_recall'] = result.get('algorithm_name')
            
            if result['f1_score'] > best_f1:
                best_f1 = result['f1_score']
                comparison['best_f1'] = result.get('algorithm_name')
        
        return comparison
