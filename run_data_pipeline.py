"""
Step 3: Collect and Process Dataset for Training and Testing
=============================================================

ENHANCED PIPELINE with Interview-Level Features:
1. Generate synthetic/real-world dataset (10K+ samples)
2. NLP preprocessing (tokenization, lemmatization, stopwords)
3. Feature engineering layer (10 engineered features)
4. Data versioning with SHA-256 hashing
5. Train/validation/test splits with stratification
6. Advanced metrics (ROC-AUC, Calibration, Confusion Matrix)
7. Bias/fairness analysis (institution, degree)

Usage:
    python run_data_pipeline.py --size 10000 --train
    python run_data_pipeline.py --size 10000 --train --advanced
    python run_data_pipeline.py --real-data data.csv --train
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Add paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'backend'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'backend', 'data'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'backend', 'app', 'models'))


def run_data_pipeline(size: int = 10000, train_model: bool = False, evaluate: bool = True,
                      advanced: bool = False, real_data_path: str = None, run_bias: bool = True):
    """
    Run the complete data collection and processing pipeline

    Args:
        size: Number of samples to generate
        train_model: Whether to train the ML model after processing
        evaluate: Whether to evaluate model performance
        advanced: Enable advanced metrics (ROC-AUC, calibration, bias)
        real_data_path: Path to real-world CSV data
        run_bias: Run bias/fairness analysis
    """
    print("\n" + "=" * 80)
    print("ENHANCED DATA PIPELINE - PRODUCTION READY")
    print("=" * 80)

    if advanced:
        print("""
Features Enabled:
  [x] NLP Preprocessing (lemmatization, stopwords)
  [x] Feature Engineering (10 features)
  [x] Data Versioning (SHA-256)
  [x] Parallel Processing (multi-threaded)
  [x] Feature Scaling (StandardScaler)
  [x] Advanced Metrics (ROC-AUC, Calibration)
  [x] Bias/Fairness Analysis
  [x] Model Persistence with Metadata
""")

    # Step 1: Load real data OR generate synthetic dataset
    print("\n[STEP 1] Data Collection")
    print("-" * 50)

    # CRITICAL FIX: Actually use RealWorldDataLoader
    if real_data_path and os.path.exists(real_data_path):
        print(f"Loading real-world data from: {real_data_path}")
        from backend.data.enhanced_pipeline import RealWorldDataLoader

        real_data = RealWorldDataLoader.load_csv(real_data_path)
        print(f" Loaded {len(real_data):,} samples from real data")

        # Convert to dataset format for processing
        dataset = {
            'description': f'Real-world dataset from {real_data_path}',
            'source': 'real_world',
            'test_cases': [
                {
                    'id': i + 1,
                    'candidate_education': sample['candidate'],
                    'job_requirements': sample['requirements'],
                    'candidate_skills': sample.get('candidate_skills', []),
                    'job_skills': sample.get('job_skills', []),
                    'is_match': sample['label'] == 1
                }
                for i, sample in enumerate(real_data)
            ]
        }

        # Save for processing
        with open('backend/data/large_test_dataset.json', 'w') as f:
            json.dump(dataset, f, indent=2)
    else:
        print("[GEN] Generating synthetic dataset...")
        from generate_synthetic_dataset import SyntheticDataGenerator

        generator = SyntheticDataGenerator(seed=42)
        dataset = generator.generate_dataset(
            size=size,
            balance=True,
            output_file='backend/data/large_test_dataset.json'
        )

    # Add data versioning
    if advanced:
        from backend.data.enhanced_pipeline import DataVersioning
        version_info = DataVersioning.create_version_info(dataset)
        dataset['version_info'] = version_info
        print(f" Dataset version: {version_info['version']}")
        print(f" Dataset hash: {version_info['hash']}")

    # Step 2: Process and prepare dataset
    print("\n STEP 2: Processing and Preparing Dataset")
    print("-" * 50)

    from backend.data.dataset_processor import DatasetProcessor, process_and_prepare_dataset

    result = process_and_prepare_dataset(
        input_file='large_test_dataset.json',
        output_dir='processed',
        generate_new=False  # Already generated above
    )

    if not result:
        print(" Dataset processing failed!")
        return None

    # Step 3: Load ML training data
    print("\n STEP 3: Loading ML Training Data")
    print("-" * 50)

    ml_data_path = os.path.join('backend', 'data', 'processed', 'ml_training_data.json')
    with open(ml_data_path, 'r') as f:
        ml_data = json.load(f)

    print(f" Training samples:   {len(ml_data['train']):,}")
    print(f" Validation samples: {len(ml_data['validation']):,}")
    print(f" Test samples:       {len(ml_data['test']):,}")

    # Step 3.5: Feature Engineering with Parallel Processing (if advanced)
    feature_scaler = None
    dataset_hash = None

    if advanced:
        print("\n STEP 3.5: Feature Engineering (Parallel)")
        print("-" * 50)

        from backend.data.enhanced_pipeline import (
            FeatureEngineer, ParallelProcessor, FeatureScaler, DataVersioning
        )

        feature_engineer = FeatureEngineer()
        processor = ParallelProcessor()

        # CRITICAL FIX: Use parallel processing for feature extraction
        print(f"   Using {processor.n_workers} parallel workers...")

        # Extract features from FULL training set (not sample)
        all_train_features = processor.parallel_extract_features(
            ml_data['train'], feature_engineer
        )

        print(f" Extracted {len(all_train_features[0])} features per sample")
        print(f"  Features: {list(all_train_features[0].keys())}")

        # CRITICAL FIX: Feature scaling - fit on FULL training set
        # This prevents data leakage - we fit only on training data
        print("\n Applying Feature Scaling (StandardScaler)...")
        print("   NOTE: Fitting scaler on FULL training set to prevent data leakage")
        import numpy as np

        # Convert features to numpy array
        feature_names = list(all_train_features[0].keys())
        X_train_full = np.array([[f.get(name, 0) for name in feature_names] for f in all_train_features])

        feature_scaler = FeatureScaler(method='standard')
        X_scaled = feature_scaler.fit_transform(X_train_full)

        print(f" Features scaled: mean={X_scaled.mean():.4f}, std={X_scaled.std():.4f}")
        print(f" Scaler fitted on {len(X_train_full)} samples (training set only)")

        # Get dataset hash for model metadata
        dataset_hash = DataVersioning.generate_hash(ml_data['train'])

        # Save engineered features (sample only for inspection)
        features_path = os.path.join('backend', 'data', 'processed', 'engineered_features.json')
        with open(features_path, 'w') as f:
            json.dump({
                'feature_names': feature_names,
                'sample_features': all_train_features[:10],
                'total_samples': len(ml_data['train']),
                'scaler_params': feature_scaler.get_params()
            }, f, indent=2)
        print(f" Features saved to: {features_path}")

    # Step 4: Train model (optional)
    if train_model:
        print("\n STEP 4: Training Enhanced ML Model")
        print("-" * 50)

        from backend.app.models.enhanced_ml_model import TrainableEnhancedMatcher

        # INTERVIEW NOTE: Model Selection Justification
        # - Logistic Regression: Interpretable baseline, calibrated probabilities
        # - use_interactions=True: Adds polynomial features for non-linearity
        # - For production, compare with RandomForest using model_type='rf'

        model = TrainableEnhancedMatcher(
            model_type='logistic',
            use_institution_ranking=False,  # Avoid institution bias
            use_semantic=True,
            use_experience=True,
            use_interactions=True,
            handle_imbalance='auto'
        )

        # CRITICAL FIX: Proper train/validation split
        # DON'T merge validation into training - this removes unbiased evaluation
        # Use validation for early stopping / hyperparameter selection
        # Use test for FINAL unbiased evaluation

        training_data = ml_data['train']  # Only training data
        validation_data = ml_data['validation']  # Keep separate

        print(f"Training on {len(training_data):,} samples...")
        print(f"Validation on {len(validation_data):,} samples (held out)...")

        # Train on training data only
        metrics = model.train(training_data, test_size=0.15)

        print("\n Training Results:")
        print(f"   Accuracy:  {metrics['accuracy']:.4f}")
        print(f"   Precision: {metrics['precision']:.4f}")
        print(f"   Recall:    {metrics['recall']:.4f}")
        print(f"   F1 Score:  {metrics['f1_score']:.4f}")

        if metrics.get('feature_importances'):
            print("\n Top Feature Importances:")
            sorted_features = sorted(
                metrics['feature_importances'].items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )[:5]
            for name, importance in sorted_features:
                print(f"   {name}: {importance:.4f}")

        # Cross-validation
        print("\n Running Cross-Validation...")
        cv_results = model.cross_validate(training_data, cv=5)
        print(f"   CV Accuracy: {cv_results['cv_accuracy']:.4f} ± {cv_results['cv_accuracy_std']:.4f}")
        print(f"   CV F1 Score: {cv_results['cv_f1']:.4f}")

        # CRITICAL FIX: Save model WITH METADATA
        model_path = os.path.join('backend', 'data', 'processed', 'trained_model.pkl')

        if advanced:
            from backend.data.enhanced_pipeline import ModelPersistence

            # Get feature names from model
            feature_names = model.feature_names if hasattr(model, 'feature_names') else None

            ModelPersistence.save_model_with_metadata(
                model=model,
                filepath=model_path,
                dataset_hash=dataset_hash,
                training_metrics=metrics,
                feature_names=feature_names,
                scaler=feature_scaler,
                version="2.0.0"
            )
        else:
            model.save_model(model_path)
            print(f"\n Model saved to: {model_path}")

        # Evaluate on test set
        if evaluate and ml_data['test']:
            print("\n STEP 5: Evaluating on Test Set")
            print("-" * 50)

            correct = 0
            total = len(ml_data['test'])
            predictions = []

            for sample in ml_data['test']:
                result = model.classify(
                    sample['candidate'],
                    sample['requirements'],
                    sample.get('candidate_skills'),
                    sample.get('job_skills')
                )
                
                predicted = 1 if result['decision'] == 'SELECTED' else 0
                actual = sample['label']
                
                if predicted == actual:
                    correct += 1
                
                predictions.append({
                    'predicted': predicted,
                    'actual': actual,
                    'score': result['score'],
                    'confidence': result['confidence']
                })
            
            test_accuracy = correct / total
            
            # Calculate more metrics
            tp = sum(1 for p in predictions if p['predicted'] == 1 and p['actual'] == 1)
            fp = sum(1 for p in predictions if p['predicted'] == 1 and p['actual'] == 0)
            fn = sum(1 for p in predictions if p['predicted'] == 0 and p['actual'] == 1)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            print(f"\n Test Set Results ({total:,} samples):")
            print(f"   Accuracy:  {test_accuracy:.4f}")
            print(f"   Precision: {precision:.4f}")
            print(f"   Recall:    {recall:.4f}")
            print(f"   F1 Score:  {f1:.4f}")
            
            # Save evaluation results
            eval_results = {
                'test_date': datetime.now().isoformat(),
                'test_samples': total,
                'accuracy': round(test_accuracy, 4),
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1_score': round(f1, 4),
                'training_metrics': metrics,
                'cv_results': cv_results
            }
            
            eval_path = os.path.join('backend', 'data', 'processed', 'evaluation_results.json')
            with open(eval_path, 'w') as f:
                json.dump(eval_results, f, indent=2)
            print(f"\n Evaluation results saved to: {eval_path}")

            # Advanced metrics (ROC-AUC, Calibration, Confusion Matrix)
            if advanced:
                print("\n STEP 5.5: Advanced Evaluation Metrics")
                print("-" * 50)

                from backend.data.enhanced_pipeline import AdvancedEvaluator

                evaluator = AdvancedEvaluator()
                for p in predictions:
                    evaluator.add_prediction(p['actual'], p['predicted'], p['score'])

                adv_metrics = evaluator.compute_metrics()

                if adv_metrics.get('roc_auc'):
                    print(f"   ROC-AUC:     {adv_metrics['roc_auc']:.4f}")

                print(f"   Specificity: {adv_metrics['specificity']:.4f}")
                print(f"   ECE (Calibration Error): {adv_metrics['calibration']['expected_calibration_error']:.4f}")

                print(f"\n Confusion Matrix:")
                cm = adv_metrics['confusion_matrix']
                print(f"   TP: {cm['true_positive']:4d}  |  FP: {cm['false_positive']:4d}")
                print(f"   FN: {cm['false_negative']:4d}  |  TN: {cm['true_negative']:4d}")

                print(f"\n Threshold Analysis:")
                for thresh, perf in adv_metrics['threshold_analysis'].items():
                    print(f"   @{thresh}: P={perf['precision']:.3f} R={perf['recall']:.3f} F1={perf['f1_score']:.3f}")

                # Save advanced metrics
                adv_path = os.path.join('backend', 'data', 'processed', 'advanced_metrics.json')
                with open(adv_path, 'w') as f:
                    json.dump(adv_metrics, f, indent=2, default=str)
                print(f"\n[OK] Advanced metrics saved to: {adv_path}")

            # Bias/Fairness Analysis
            if advanced and run_bias:
                print("\n[BIAS] STEP 6: Bias & Fairness Analysis")
                print("-" * 50)

                from backend.data.enhanced_pipeline import BiasAnalyzer

                bias_analyzer = BiasAnalyzer(model)
                fairness_report = bias_analyzer.generate_fairness_report(ml_data['test'])

                print("\n[INST] Institution Bias Analysis:")
                inst_bias = fairness_report['institution_bias']
                for tier in ['tier1', 'tier2', 'tier3']:
                    if tier in inst_bias:
                        print(f"   {tier}: mean_score={inst_bias[tier]['mean_score']:.3f}, n={inst_bias[tier]['sample_count']}")

                if 'bias_detected' in inst_bias:
                    if inst_bias['bias_detected']:
                        print(f"\n   [WARN] BIAS DETECTED: Gap = {inst_bias['bias_gap']:.3f}")
                        print(f"   [NOTE] {inst_bias['recommendation']}")
                    else:
                        print(f"\n   [OK] No significant institution bias detected")

                # Save fairness report
                fairness_path = os.path.join('backend', 'data', 'processed', 'fairness_report.json')
                with open(fairness_path, 'w') as f:
                    json.dump(fairness_report, f, indent=2)
                print(f"\n[OK] Fairness report saved to: {fairness_path}")

    # Final summary
    print("\n" + "=" * 80)
    print("[OK] DATA PIPELINE COMPLETE")
    print("=" * 80)
    print(f"""
Generated Files:
----------------
backend/data/
   large_test_dataset.json      ({size:,} samples - full dataset)
   processed/
       train_dataset.json        (70% for training)
       train_augmented.json      (with noise variations)
        validation_dataset.json   (15% for validation)
        test_dataset.json         (15% for testing)
        ml_training_data.json     (ML-ready format)
        full_dataset.csv          (for analysis)
       {' engineered_features.json  (10 extracted features)' if advanced else ''}
       {' trained_model.pkl         (trained model)' if train_model else ''}
       {' advanced_metrics.json     (ROC-AUC, calibration)' if train_model and evaluate and advanced else ''}
       {' fairness_report.json      (bias analysis)' if train_model and evaluate and advanced and run_bias else ''}
       {' evaluation_results.json   (evaluation metrics)' if train_model and evaluate else ''}

Next Steps:
-----------
1. Review the generated data in backend/data/processed/
2. Run: python run_data_pipeline.py --train --advanced  (full pipeline)
3. Use the trained model in your application

For large-scale evaluation:
    python run_large_scale_evaluation.py
""")

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Enhanced Data Pipeline with Interview-Level Features'
    )
    parser.add_argument('--size', type=int, default=10000,
                       help='Number of samples to generate (default: 10000)')
    parser.add_argument('--train', action='store_true',
                       help='Train the ML model after processing')
    parser.add_argument('--no-eval', action='store_true',
                       help='Skip model evaluation')
    parser.add_argument('--advanced', action='store_true',
                       help='Enable advanced metrics (ROC-AUC, calibration, bias)')
    parser.add_argument('--real-data', type=str, default=None,
                       help='Path to real-world CSV data')
    parser.add_argument('--no-bias', action='store_true',
                       help='Skip bias analysis')

    args = parser.parse_args()

    run_data_pipeline(
        size=args.size,
        train_model=args.train,
        evaluate=not args.no_eval,
        advanced=args.advanced,
        real_data_path=args.real_data,
        run_bias=not args.no_bias
    )
