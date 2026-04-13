"""
Dataset Collection and Processing Pipeline
Step 3: Collect and process dataset for training and testing the AI system

Features:
- Generate diverse synthetic datasets
- Process and validate data quality
- Create balanced train/validation/test splits
- Add real-world noise and variations
- Export in multiple formats (JSON, CSV)
- Statistics and quality metrics
"""

import json
import os
import random
import csv
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import Counter
import sys

# Add parent directories to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DatasetProcessor:
    """Process and prepare datasets for ML training"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.dirname(os.path.abspath(__file__))
        self.datasets = {}
        
    def load_dataset(self, filepath: str) -> Dict:
        """Load dataset from JSON file"""
        full_path = os.path.join(self.data_dir, filepath) if not os.path.isabs(filepath) else filepath
        with open(full_path, 'r') as f:
            return json.load(f)
    
    def save_dataset(self, dataset: Dict, filepath: str) -> None:
        """Save dataset to JSON file"""
        full_path = os.path.join(self.data_dir, filepath) if not os.path.isabs(filepath) else filepath
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"[OK] Dataset saved to: {full_path}")
    
    def validate_dataset(self, dataset: Dict) -> Dict:
        """
        Validate dataset quality and structure
        
        Returns validation report with issues and statistics
        """
        report = {
            'valid': True,
            'total_cases': 0,
            'issues': [],
            'warnings': [],
            'statistics': {}
        }
        
        test_cases = dataset.get('test_cases', [])
        report['total_cases'] = len(test_cases)
        
        if len(test_cases) == 0:
            report['valid'] = False
            report['issues'].append("Dataset is empty")
            return report
        
        # Check required fields
        required_fields = ['candidate_education', 'job_requirements', 'is_match']
        missing_fields = Counter()
        
        for i, case in enumerate(test_cases):
            for field in required_fields:
                if field not in case:
                    missing_fields[field] += 1
                    report['valid'] = False
            
            # Validate education structure
            education = case.get('candidate_education', [])
            if not education:
                report['warnings'].append(f"Case {i+1}: Empty education")
            else:
                for edu in education:
                    if not edu.get('degree'):
                        report['warnings'].append(f"Case {i+1}: Missing degree")
                    if not edu.get('field'):
                        report['warnings'].append(f"Case {i+1}: Missing field")
        
        # Add missing field issues
        for field, count in missing_fields.items():
            report['issues'].append(f"Missing '{field}' in {count} cases")
        
        # Calculate statistics
        positive = sum(1 for c in test_cases if c.get('is_match', False))
        negative = len(test_cases) - positive
        
        report['statistics'] = {
            'positive_cases': positive,
            'negative_cases': negative,
            'positive_ratio': round(positive / len(test_cases), 4) if test_cases else 0,
            'unique_jobs': len(set(c.get('job_id', '') for c in test_cases)),
            'unique_resumes': len(set(c.get('resume_id', '') for c in test_cases))
        }
        
        # Check balance
        pos_ratio = report['statistics']['positive_ratio']
        if pos_ratio < 0.3 or pos_ratio > 0.7:
            report['warnings'].append(f"Dataset is imbalanced (positive ratio: {pos_ratio:.2%})")
        
        return report
    
    def create_train_test_split(
        self,
        dataset: Dict,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        stratify: bool = True,
        seed: int = 42
    ) -> Tuple[Dict, Dict, Dict]:
        """
        Split dataset into train/validation/test sets
        
        Args:
            dataset: Full dataset
            train_ratio: Proportion for training
            val_ratio: Proportion for validation
            test_ratio: Proportion for testing
            stratify: Maintain class balance in splits
            seed: Random seed for reproducibility
        
        Returns:
            (train_dataset, val_dataset, test_dataset)
        """
        random.seed(seed)
        
        test_cases = dataset.get('test_cases', [])
        
        if stratify:
            # Separate positive and negative cases
            positive = [c for c in test_cases if c.get('is_match', False)]
            negative = [c for c in test_cases if not c.get('is_match', False)]
            
            random.shuffle(positive)
            random.shuffle(negative)
            
            # Split each class
            def split_list(lst, train_r, val_r):
                n = len(lst)
                train_end = int(n * train_r)
                val_end = train_end + int(n * val_r)
                return lst[:train_end], lst[train_end:val_end], lst[val_end:]
            
            pos_train, pos_val, pos_test = split_list(positive, train_ratio, val_ratio)
            neg_train, neg_val, neg_test = split_list(negative, train_ratio, val_ratio)
            
            train_cases = pos_train + neg_train
            val_cases = pos_val + neg_val
            test_cases_split = pos_test + neg_test
            
            random.shuffle(train_cases)
            random.shuffle(val_cases)
            random.shuffle(test_cases_split)
        else:
            random.shuffle(test_cases)
            n = len(test_cases)
            train_end = int(n * train_ratio)
            val_end = train_end + int(n * val_ratio)
            
            train_cases = test_cases[:train_end]
            val_cases = test_cases[train_end:val_end]
            test_cases_split = test_cases[val_end:]
        
        # Create split datasets
        def create_split_dataset(cases, split_name):
            pos = sum(1 for c in cases if c.get('is_match', False))
            return {
                'description': f'{split_name} split from {dataset.get("description", "dataset")}',
                'split': split_name,
                'created_date': datetime.now().isoformat(),
                'total_cases': len(cases),
                'positive_cases': pos,
                'negative_cases': len(cases) - pos,
                'test_cases': cases
            }
        
        train_dataset = create_split_dataset(train_cases, 'train')
        val_dataset = create_split_dataset(val_cases, 'validation')
        test_dataset = create_split_dataset(test_cases_split, 'test')
        
        print(f"\n{'=' * 60}")
        print("DATASET SPLIT COMPLETE")
        print(f"{'=' * 60}")
        print(f"Train:      {len(train_cases):,} cases ({len(train_cases)/len(test_cases)*100:.1f}%)")
        print(f"Validation: {len(val_cases):,} cases ({len(val_cases)/len(test_cases)*100:.1f}%)")
        print(f"Test:       {len(test_cases_split):,} cases ({len(test_cases_split)/len(test_cases)*100:.1f}%)")
        print(f"{'=' * 60}\n")
        
        return train_dataset, val_dataset, test_dataset
    
    def add_noise_variations(
        self,
        dataset: Dict,
        typo_rate: float = 0.05,
        synonym_rate: float = 0.1,
        missing_field_rate: float = 0.02
    ) -> Dict:
        """
        Add real-world noise and variations to dataset
        
        Simulates:
        - Typos in degree/field names
        - Synonym variations
        - Missing fields
        - Inconsistent formatting
        """
        # Synonyms for augmentation
        degree_synonyms = {
            'bachelors': ['bachelor', 'bsc', 'b.s.', 'bs', 'ba', 'b.a.'],
            'masters': ['master', 'msc', 'm.s.', 'ms', 'ma', 'm.a.', 'mba'],
            'phd': ['ph.d.', 'doctorate', 'doctoral', 'dr.'],
            'diploma': ['dip', 'dip.', 'certification', 'cert']
        }
        
        field_synonyms = {
            'computer science': ['cs', 'comp sci', 'computing', 'computer sciences'],
            'data science': ['data analytics', 'analytics', 'data analysis'],
            'software engineering': ['software eng', 'software development', 'swe'],
            'artificial intelligence': ['ai', 'machine learning', 'ml'],
            'information technology': ['it', 'info tech', 'information systems']
        }
        
        def add_typo(text):
            """Add random typo to text"""
            if not text or len(text) < 3:
                return text
            pos = random.randint(1, len(text) - 2)
            chars = list(text)
            # Random typo types
            typo_type = random.choice(['swap', 'delete', 'duplicate'])
            if typo_type == 'swap' and pos < len(chars) - 1:
                chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
            elif typo_type == 'delete':
                chars.pop(pos)
            elif typo_type == 'duplicate':
                chars.insert(pos, chars[pos])
            return ''.join(chars)
        
        def apply_synonym(text, synonyms):
            """Apply random synonym substitution"""
            text_lower = text.lower()
            for key, syns in synonyms.items():
                if key in text_lower:
                    replacement = random.choice(syns)
                    # Preserve original case
                    if text[0].isupper():
                        replacement = replacement.capitalize()
                    return text_lower.replace(key, replacement)
            return text
        
        augmented_cases = []
        
        for case in dataset.get('test_cases', []):
            new_case = case.copy()
            new_case['candidate_education'] = []
            
            for edu in case.get('candidate_education', []):
                new_edu = edu.copy()
                
                # Apply typos
                if random.random() < typo_rate:
                    new_edu['degree'] = add_typo(new_edu.get('degree', ''))
                
                # Apply synonyms
                if random.random() < synonym_rate:
                    new_edu['degree'] = apply_synonym(new_edu.get('degree', ''), degree_synonyms)
                    new_edu['field'] = apply_synonym(new_edu.get('field', ''), field_synonyms)
                
                # Missing fields
                if random.random() < missing_field_rate:
                    field_to_remove = random.choice(['institution', 'year'])
                    new_edu.pop(field_to_remove, None)
                
                new_case['candidate_education'].append(new_edu)
            
            augmented_cases.append(new_case)
        
        augmented_dataset = dataset.copy()
        augmented_dataset['test_cases'] = augmented_cases
        augmented_dataset['augmented'] = True
        augmented_dataset['augmentation_params'] = {
            'typo_rate': typo_rate,
            'synonym_rate': synonym_rate,
            'missing_field_rate': missing_field_rate
        }
        
        return augmented_dataset
    
    def export_to_csv(self, dataset: Dict, filepath: str) -> None:
        """Export dataset to CSV format for analysis"""
        full_path = os.path.join(self.data_dir, filepath) if not os.path.isabs(filepath) else filepath
        
        with open(full_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'id', 'resume_id', 'job_id', 
                'degree', 'field', 'institution', 'year',
                'job_requirements', 'candidate_skills', 'job_skills',
                'is_match', 'expected_score_min', 'expected_score_max'
            ])
            
            for case in dataset.get('test_cases', []):
                edu = case.get('candidate_education', [{}])[0] if case.get('candidate_education') else {}
                writer.writerow([
                    case.get('id', ''),
                    case.get('resume_id', ''),
                    case.get('job_id', ''),
                    edu.get('degree', ''),
                    edu.get('field', ''),
                    edu.get('institution', ''),
                    edu.get('year', ''),
                    '|'.join(case.get('job_requirements', [])),
                    '|'.join(case.get('candidate_skills', [])),
                    '|'.join(case.get('job_skills', [])),
                    case.get('is_match', False),
                    case.get('expected_score_min', 0),
                    case.get('expected_score_max', 1)
                ])
        
        print(f"[OK] CSV exported to: {full_path}")
    
    def convert_to_ml_format(self, dataset: Dict) -> List[Dict]:
        """
        Convert dataset to format expected by TrainableEnhancedMatcher
        
        Returns list of dicts with:
        - candidate: List[Dict] (education entries)
        - requirements: List[str] (job requirements)
        - candidate_skills: List[str]
        - job_skills: List[str]
        - label: int (0 or 1)
        """
        ml_data = []
        
        for case in dataset.get('test_cases', []):
            ml_data.append({
                'candidate': case.get('candidate_education', []),
                'requirements': case.get('job_requirements', []),
                'candidate_skills': case.get('candidate_skills', []),
                'job_skills': case.get('job_skills', []),
                'label': 1 if case.get('is_match', False) else 0
            })
        
        return ml_data
    
    def generate_quality_report(self, dataset: Dict) -> str:
        """Generate detailed quality report for dataset"""
        validation = self.validate_dataset(dataset)
        test_cases = dataset.get('test_cases', [])
        
        # Collect statistics
        degrees = Counter()
        fields = Counter()
        job_types = Counter()
        
        for case in test_cases:
            for edu in case.get('candidate_education', []):
                degrees[edu.get('degree', 'Unknown')] += 1
                fields[edu.get('field', 'Unknown')] += 1
            job_types[case.get('job_type', 'Unknown')] += 1
        
        report = f"""
{'=' * 70}
DATASET QUALITY REPORT
{'=' * 70}

OVERVIEW
--------
Total Cases:     {validation['total_cases']:,}
Positive Cases:  {validation['statistics']['positive_cases']:,}
Negative Cases:  {validation['statistics']['negative_cases']:,}
Positive Ratio:  {validation['statistics']['positive_ratio']:.2%}
Valid:           {'[OK] Yes' if validation['valid'] else '[X] No'}

DEGREE DISTRIBUTION
-------------------
"""
        for degree, count in degrees.most_common(10):
            report += f"  {degree:25} {count:,} ({count/sum(degrees.values())*100:.1f}%)\n"
        
        report += f"""
FIELD DISTRIBUTION (Top 10)
---------------------------
"""
        for field, count in fields.most_common(10):
            report += f"  {field:25} {count:,} ({count/sum(fields.values())*100:.1f}%)\n"
        
        report += f"""
JOB TYPE DISTRIBUTION
---------------------
"""
        for jtype, count in job_types.most_common():
            report += f"  {jtype:25} {count:,} ({count/sum(job_types.values())*100:.1f}%)\n"
        
        if validation['issues']:
            report += f"""
ISSUES
------
"""
            for issue in validation['issues']:
                report += f"  [X] {issue}\n"
        
        if validation['warnings']:
            report += f"""
WARNINGS
--------
"""
            for warning in validation['warnings'][:10]:  # Limit to 10
                report += f"  [WARN] {warning}\n"
            if len(validation['warnings']) > 10:
                report += f"  ... and {len(validation['warnings']) - 10} more warnings\n"
        
        report += f"\n{'=' * 70}\n"
        
        return report


def process_and_prepare_dataset(
    input_file: str = 'large_test_dataset.json',
    output_dir: str = 'processed',
    generate_new: bool = False,
    size: int = 10000
) -> Dict:
    """
    Main function to process and prepare dataset for ML training
    
    Args:
        input_file: Input dataset file
        output_dir: Directory for processed outputs
        generate_new: Generate new synthetic data
        size: Size if generating new data
    
    Returns:
        Dict with paths to processed files
    """
    processor = DatasetProcessor()
    
    # Generate new data if requested
    if generate_new:
        print("\n📊 Generating new synthetic dataset...")
        # Import generator
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from generate_synthetic_dataset import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator()
        dataset = generator.generate_dataset(
            size=size,
            balance=True,
            output_file=os.path.join(processor.data_dir, input_file)
        )
    else:
        print(f"\n[FILE] Loading existing dataset: {input_file}")
        dataset = processor.load_dataset(input_file)
    
    # Validate
    print("\n[CHECK] Validating dataset...")
    validation = processor.validate_dataset(dataset)
    if not validation['valid']:
        print("[FAIL] Dataset validation failed!")
        for issue in validation['issues']:
            print(f"   - {issue}")
        return None
    print("[OK] Dataset validation passed")
    
    # Generate quality report
    report = processor.generate_quality_report(dataset)
    print(report)
    
    # Create output directory
    output_path = os.path.join(processor.data_dir, output_dir)
    os.makedirs(output_path, exist_ok=True)
    
    # Create train/val/test splits
    print("\n[PKG] Creating train/validation/test splits...")
    train, val, test = processor.create_train_test_split(
        dataset, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15
    )
    
    # Save splits
    processor.save_dataset(train, os.path.join(output_dir, 'train_dataset.json'))
    processor.save_dataset(val, os.path.join(output_dir, 'validation_dataset.json'))
    processor.save_dataset(test, os.path.join(output_dir, 'test_dataset.json'))
    
    # Add noise variations to training data
    print("\n[SHUFFLE] Adding noise variations for robustness...")
    train_augmented = processor.add_noise_variations(train, typo_rate=0.03, synonym_rate=0.08)
    processor.save_dataset(train_augmented, os.path.join(output_dir, 'train_augmented.json'))
    
    # Export to CSV
    print("\n[DOC] Exporting to CSV...")
    processor.export_to_csv(dataset, os.path.join(output_dir, 'full_dataset.csv'))
    
    # Convert to ML format and save
    print("\n[ML] Converting to ML training format...")
    ml_train = processor.convert_to_ml_format(train_augmented)
    ml_val = processor.convert_to_ml_format(val)
    ml_test = processor.convert_to_ml_format(test)
    
    ml_data = {
        'train': ml_train,
        'validation': ml_val,
        'test': ml_test,
        'created_date': datetime.now().isoformat(),
        'total_samples': len(ml_train) + len(ml_val) + len(ml_test)
    }
    
    ml_path = os.path.join(output_dir, 'ml_training_data.json')
    processor.save_dataset(ml_data, ml_path)
    
    # Summary
    result = {
        'train_path': os.path.join(output_path, 'train_dataset.json'),
        'train_augmented_path': os.path.join(output_path, 'train_augmented.json'),
        'validation_path': os.path.join(output_path, 'validation_dataset.json'),
        'test_path': os.path.join(output_path, 'test_dataset.json'),
        'ml_data_path': os.path.join(output_path, 'ml_training_data.json'),
        'csv_path': os.path.join(output_path, 'full_dataset.csv'),
        'statistics': {
            'total_cases': len(dataset.get('test_cases', [])),
            'train_cases': len(ml_train),
            'validation_cases': len(ml_val),
            'test_cases': len(ml_test)
        }
    }
    
    print(f"\n{'=' * 70}")
    print("[OK] DATASET PROCESSING COMPLETE")
    print(f"{'=' * 70}")
    print(f"\nProcessed files saved to: {output_path}")
    print(f"  - train_dataset.json:       {result['statistics']['train_cases']:,} samples")
    print(f"  - train_augmented.json:     {result['statistics']['train_cases']:,} samples (with noise)")
    print(f"  - validation_dataset.json:  {result['statistics']['validation_cases']:,} samples")
    print(f"  - test_dataset.json:        {result['statistics']['test_cases']:,} samples")
    print(f"  - ml_training_data.json:    Ready for TrainableEnhancedMatcher")
    print(f"  - full_dataset.csv:         For analysis in Excel/Pandas")
    print(f"\n{'=' * 70}\n")
    
    return result


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Process dataset for ML training')
    parser.add_argument('--input', type=str, default='large_test_dataset.json',
                       help='Input dataset file')
    parser.add_argument('--output', type=str, default='processed',
                       help='Output directory')
    parser.add_argument('--generate', action='store_true',
                       help='Generate new synthetic dataset')
    parser.add_argument('--size', type=int, default=10000,
                       help='Size of dataset to generate')
    
    args = parser.parse_args()
    
    result = process_and_prepare_dataset(
        input_file=args.input,
        output_dir=args.output,
        generate_new=args.generate,
        size=args.size
    )
