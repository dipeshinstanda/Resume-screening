"""
Large-Scale Synthetic Dataset Generator
Generates 10K+ realistic test cases for evaluation
"""

import json
import random
import os
from datetime import datetime
from typing import List, Dict, Tuple

class SyntheticDataGenerator:
    """Generate realistic synthetic resume-job matching test cases"""
    
    def __init__(self, seed=42):
        random.seed(seed)
        
        # Degree types with levels
        self.degrees = {
            'PhD': 6,
            'Doctorate': 6,
            'Masters': 5,
            'MBA': 5,
            'MSc': 5,
            'Bachelors': 4,
            'BSc': 4,
            'BTech': 4,
            'Diploma': 3,
            'Associate': 3,
            'High School': 1
        }
        
        # Fields of study
        self.fields = {
            'Computer Science': ['cs', 'software', 'programming'],
            'Data Science': ['analytics', 'statistics', 'data'],
            'Artificial Intelligence': ['ai', 'ml', 'deep learning'],
            'Software Engineering': ['software', 'development', 'engineering'],
            'Information Technology': ['it', 'systems', 'technology'],
            'Electrical Engineering': ['electrical', 'electronics', 'circuits'],
            'Mechanical Engineering': ['mechanical', 'mechanics', 'manufacturing'],
            'Business Administration': ['business', 'management', 'mba'],
            'Finance': ['finance', 'accounting', 'economics'],
            'Mathematics': ['math', 'statistics', 'applied math'],
            'Physics': ['physics', 'theoretical', 'applied physics'],
            'Biology': ['biology', 'life sciences', 'biotech'],
            'Chemistry': ['chemistry', 'chemical', 'biochemistry'],
            'Psychology': ['psychology', 'cognitive', 'behavioral'],
            'English Literature': ['english', 'literature', 'writing']
        }
        
        # Institutions with tiers
        self.institutions = {
            'tier1': [
                'MIT', 'Stanford University', 'Harvard University', 'Oxford University',
                'Cambridge University', 'Caltech', 'UC Berkeley', 'Princeton University',
                'Yale University', 'Columbia University', 'Carnegie Mellon University',
                'Georgia Tech', 'IIT Delhi', 'IIT Bombay', 'ETH Zurich'
            ],
            'tier2': [
                'University of Michigan', 'UCLA', 'University of Texas',
                'University of Washington', 'Cornell University', 'NYU',
                'University of Illinois', 'Penn State', 'Purdue University',
                'University of Maryland', 'Boston University', 'NUS Singapore'
            ],
            'tier3': [
                'State University', 'Tech University', 'Engineering College',
                'City College', 'Regional University', 'Community College',
                'Online University', 'Local Institute', 'Technical Institute'
            ]
        }
        
        # Job requirement templates
        self.job_templates = {
            'research': {
                'degree': ['PhD', 'Doctorate', 'Masters'],
                'fields': ['Computer Science', 'Artificial Intelligence', 'Data Science', 'Mathematics', 'Physics'],
                'level': 5
            },
            'senior': {
                'degree': ['Masters', 'MBA', 'Bachelors'],
                'fields': ['Computer Science', 'Software Engineering', 'Business Administration', 'Data Science'],
                'level': 4
            },
            'mid': {
                'degree': ['Bachelors', 'Masters'],
                'fields': ['Computer Science', 'Information Technology', 'Software Engineering'],
                'level': 4
            },
            'junior': {
                'degree': ['Bachelors'],
                'fields': ['Computer Science', 'Information Technology', 'any Engineering'],
                'level': 4
            },
            'entry': {
                'degree': ['Bachelors', 'Diploma'],
                'fields': ['any field'],
                'level': 3
            }
        }
        
        # Skills database
        self.skills = {
            'programming': ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'Go', 'Rust'],
            'web': ['React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'HTML', 'CSS'],
            'ml': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'NLP', 'Computer Vision'],
            'data': ['SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'Data Analysis', 'Tableau', 'PowerBI'],
            'cloud': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes'],
            'general': ['Git', 'Agile', 'Scrum', 'CI/CD', 'Testing', 'Debugging']
        }
    
    def generate_candidate_education(self, difficulty='random') -> Tuple[List[Dict], str]:
        """
        Generate candidate education
        
        Args:
            difficulty: 'easy', 'medium', 'hard', or 'random'
        
        Returns:
            (education_list, tier)
        """
        if difficulty == 'random':
            difficulty = random.choice(['easy', 'medium', 'hard'])
        
        # Select degree based on difficulty
        if difficulty == 'easy':
            degree_options = ['PhD', 'Doctorate', 'Masters', 'MBA']
            tier = 'tier1' if random.random() > 0.5 else 'tier2'
        elif difficulty == 'medium':
            degree_options = ['Masters', 'Bachelors', 'BSc', 'BTech']
            tier = 'tier2' if random.random() > 0.5 else 'tier3'
        else:  # hard
            degree_options = ['Bachelors', 'Diploma', 'Associate']
            tier = 'tier3'
        
        degree = random.choice(degree_options)
        field = random.choice(list(self.fields.keys()))
        institution = random.choice(self.institutions[tier])
        year = str(random.randint(2010, 2024))
        
        education = [{
            'degree': degree,
            'field': field,
            'institution': institution,
            'year': year
        }]
        
        # 30% chance of multiple degrees
        if random.random() < 0.3:
            lower_degree = 'Bachelors' if degree in ['Masters', 'MBA', 'PhD', 'Doctorate'] else 'High School'
            prev_field = random.choice(list(self.fields.keys()))
            prev_institution = random.choice(self.institutions[random.choice(['tier2', 'tier3'])])
            prev_year = str(random.randint(2005, int(year) - 2))
            
            education.insert(0, {
                'degree': lower_degree,
                'field': prev_field,
                'institution': prev_institution,
                'year': prev_year
            })
        
        return education, tier
    
    def generate_job_requirements(self, job_type='random') -> Tuple[List[str], str, int]:
        """
        Generate job requirements
        
        Returns:
            (requirements_list, job_type, required_level)
        """
        if job_type == 'random':
            job_type = random.choice(['research', 'senior', 'mid', 'junior', 'entry'])
        
        template = self.job_templates[job_type]
        degree_req = random.choice(template['degree'])
        field_req = random.choice(template['fields'])
        
        requirements = [
            f"{degree_req} in {field_req}",
        ]
        
        # Add additional requirements
        if job_type == 'research':
            requirements.append("Research experience required")
            requirements.append("Publications preferred")
        elif job_type == 'senior':
            requirements.append("5+ years experience")
        
        return requirements, job_type, template['level']
    
    def generate_skills(self, job_type: str, count: int = 5) -> List[str]:
        """Generate random skills based on job type"""
        all_skills = []
        
        if job_type in ['research', 'senior']:
            all_skills.extend(self.skills['programming'])
            all_skills.extend(self.skills['ml'])
            all_skills.extend(self.skills['data'])
        elif job_type in ['mid', 'junior']:
            all_skills.extend(self.skills['programming'])
            all_skills.extend(self.skills['web'])
        else:
            all_skills.extend(self.skills['general'])
        
        return random.sample(all_skills, min(count, len(all_skills)))
    
    def determine_match(
        self,
        candidate_education: List[Dict],
        job_requirements: List[str],
        required_level: int
    ) -> Tuple[bool, float, float]:
        """
        Determine if candidate should match
        
        Returns:
            (is_match, expected_score_min, expected_score_max)
        """
        # Get candidate's highest degree level
        candidate_level = 0
        for edu in candidate_education:
            degree = edu['degree']
            candidate_level = max(candidate_level, self.degrees.get(degree, 0))
        
        # Check field match
        candidate_fields = [edu['field'].lower() for edu in candidate_education]
        req_text = ' '.join(job_requirements).lower()
        
        field_match = any(
            field.lower() in req_text or
            any(keyword in req_text for keyword in self.fields.get(field, []))
            for field in candidate_fields
        )
        
        # Determine match
        if candidate_level >= required_level and field_match:
            # Good match
            if candidate_level == required_level:
                return True, 0.75, 1.0
            else:  # Overqualified
                return True, 0.80, 1.0
        elif candidate_level >= required_level - 1 and field_match:
            # Borderline match
            return random.choice([True, False]), 0.50, 0.75
        elif field_match and candidate_level < required_level:
            # Field match but underqualified
            return False, 0.30, 0.60
        else:
            # No match
            return False, 0.0, 0.40
    
    def generate_dataset(
        self,
        size: int = 10000,
        balance: bool = True,
        output_file: str = None
    ) -> Dict:
        """
        Generate large synthetic dataset
        
        Args:
            size: Number of test cases to generate
            balance: Whether to balance positive/negative cases
            output_file: Path to save JSON file
        
        Returns:
            Dataset dictionary
        """
        print(f"\n{'=' * 80}")
        print(f"GENERATING SYNTHETIC DATASET: {size:,} TEST CASES")
        print(f"{'=' * 80}\n")
        
        test_cases = []
        positive_count = 0
        negative_count = 0
        
        target_positive = size // 2 if balance else size
        
        case_id = 1
        attempts = 0
        max_attempts = size * 2
        
        while len(test_cases) < size and attempts < max_attempts:
            attempts += 1
            
            # Generate candidate
            candidate_education, tier = self.generate_candidate_education()
            
            # Generate job
            job_requirements, job_type, required_level = self.generate_job_requirements()
            
            # Determine match
            is_match, expected_min, expected_max = self.determine_match(
                candidate_education, job_requirements, required_level
            )
            
            # Balance dataset
            if balance:
                if is_match and positive_count >= target_positive:
                    continue
                if not is_match and negative_count >= (size - target_positive):
                    continue
            
            # Generate skills
            candidate_skills = self.generate_skills(job_type, random.randint(3, 7))
            job_skills = self.generate_skills(job_type, random.randint(3, 5))
            
            # Create test case
            test_case = {
                'id': case_id,
                'resume_id': f'resume_{case_id:06d}',
                'job_id': f'job_{(case_id % 1000) + 1:04d}',
                'candidate_education': candidate_education,
                'candidate_skills': candidate_skills,
                'job_requirements': job_requirements,
                'job_skills': job_skills,
                'job_type': job_type,
                'institution_tier': tier,
                'is_match': is_match,
                'expected_score_min': expected_min,
                'expected_score_max': expected_max,
                'difficulty': 'easy' if expected_max - expected_min < 0.2 else 'hard'
            }
            
            test_cases.append(test_case)
            
            if is_match:
                positive_count += 1
            else:
                negative_count += 1
            
            case_id += 1
            
            # Progress update
            if len(test_cases) % 1000 == 0:
                print(f"[OK] Generated {len(test_cases):,} cases "
                      f"(Positive: {positive_count:,}, Negative: {negative_count:,})")
        
        # Create dataset
        dataset = {
            'description': f'Synthetic dataset for AI Resume Screening System',
            'generated_date': datetime.now().isoformat(),
            'total_cases': len(test_cases),
            'positive_cases': positive_count,
            'negative_cases': negative_count,
            'balanced': balance,
            'test_cases': test_cases,
            'statistics': {
                'job_types': {},
                'institution_tiers': {},
                'difficulty_levels': {}
            }
        }
        
        # Calculate statistics
        for case in test_cases:
            job_type = case['job_type']
            tier = case['institution_tier']
            difficulty = case['difficulty']
            
            dataset['statistics']['job_types'][job_type] = \
                dataset['statistics']['job_types'].get(job_type, 0) + 1
            dataset['statistics']['institution_tiers'][tier] = \
                dataset['statistics']['institution_tiers'].get(tier, 0) + 1
            dataset['statistics']['difficulty_levels'][difficulty] = \
                dataset['statistics']['difficulty_levels'].get(difficulty, 0) + 1
        
        # Save to file
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(dataset, f, indent=2)
            print(f"\n[OK] Dataset saved to: {output_file}")
        
        # Print summary
        print(f"\n{'=' * 80}")
        print("DATASET GENERATION COMPLETE")
        print(f"{'=' * 80}\n")
        print(f"Total Cases: {len(test_cases):,}")
        print(f"Positive Cases: {positive_count:,} ({positive_count/len(test_cases)*100:.1f}%)")
        print(f"Negative Cases: {negative_count:,} ({negative_count/len(test_cases)*100:.1f}%)")
        print(f"\nJob Types Distribution:")
        for job_type, count in dataset['statistics']['job_types'].items():
            print(f"  {job_type}: {count:,} ({count/len(test_cases)*100:.1f}%)")
        print(f"\nInstitution Tiers:")
        for tier, count in dataset['statistics']['institution_tiers'].items():
            print(f"  {tier}: {count:,} ({count/len(test_cases)*100:.1f}%)")
        print(f"\nDifficulty Levels:")
        for diff, count in dataset['statistics']['difficulty_levels'].items():
            print(f"  {diff}: {count:,} ({count/len(test_cases)*100:.1f}%)")
        print(f"\n{'=' * 80}\n")
        
        return dataset


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate synthetic dataset')
    parser.add_argument('--size', type=int, default=10000, help='Number of test cases')
    parser.add_argument('--output', type=str, default='backend/data/large_test_dataset.json',
                       help='Output file path')
    parser.add_argument('--no-balance', action='store_true', help='Do not balance dataset')
    
    args = parser.parse_args()
    
    generator = SyntheticDataGenerator()
    dataset = generator.generate_dataset(
        size=args.size,
        balance=not args.no_balance,
        output_file=args.output
    )
    
    print(f"Dataset generated successfully with {len(dataset['test_cases']):,} cases!")
