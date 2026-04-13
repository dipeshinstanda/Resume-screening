"""
Baseline Keyword Matching Algorithm
Simple keyword-based approach for comparison with ML-based matching
"""

import re
from typing import List, Dict

class KeywordMatcher:
    """
    Simple baseline algorithm using keyword matching
    Used as a baseline comparison for the ML-based approach
    """
    
    def __init__(self):
        self.degree_keywords = {
            'phd': ['phd', 'ph.d', 'doctorate', 'doctoral', 'doctor of philosophy'],
            'masters': ['masters', 'master', 'msc', 'm.sc', 'mba', 'm.b.a', 'ma', 'm.a'],
            'bachelors': ['bachelors', 'bachelor', 'bsc', 'b.sc', 'ba', 'b.a', 'btech', 'b.tech', 'undergraduate'],
            'diploma': ['diploma', 'associate'],
            'high_school': ['high school', 'secondary', '12th', '10th']
        }
        
        self.field_keywords = {
            'computer_science': ['computer science', 'cs', 'computing', 'informatics'],
            'engineering': ['engineering', 'engineer'],
            'data_science': ['data science', 'data analytics', 'analytics'],
            'ai_ml': ['artificial intelligence', 'machine learning', 'ai', 'ml', 'deep learning'],
            'business': ['business', 'management', 'mba', 'administration'],
            'mathematics': ['mathematics', 'math', 'statistics', 'statistical']
        }
    
    def calculate_match_score(self, candidate_education: List[Dict], job_requirements: List[str]) -> float:
        """
        Calculate match score using simple keyword matching
        
        Args:
            candidate_education: List of education dictionaries
            job_requirements: List of requirement strings
        
        Returns:
            Match score between 0 and 1
        """
        if not candidate_education or not job_requirements:
            return 0.0
        
        # Combine all candidate education into searchable text
        candidate_text = ' '.join([
            f"{edu.get('degree', '')} {edu.get('field', '')} {edu.get('institution', '')}"
            for edu in candidate_education
        ]).lower()
        
        # Combine all requirements into searchable text
        requirements_text = ' '.join(job_requirements).lower()
        
        # Extract required degree level
        required_degree_level = self._extract_required_degree(requirements_text)
        
        # Extract candidate's highest degree level
        candidate_degree_level = self._extract_candidate_degree(candidate_text)
        
        # Calculate degree match score
        degree_match = self._compare_degree_levels(candidate_degree_level, required_degree_level)
        
        # Calculate field match score
        field_match = self._calculate_field_match(candidate_text, requirements_text)
        
        # Calculate keyword overlap score
        keyword_overlap = self._calculate_keyword_overlap(candidate_text, requirements_text)
        
        # Final score: weighted combination
        final_score = (degree_match * 0.5) + (field_match * 0.3) + (keyword_overlap * 0.2)
        
        return round(final_score, 3)
    
    def _extract_required_degree(self, requirements_text: str) -> int:
        """Extract required degree level from requirements"""
        for degree_level, keywords in self.degree_keywords.items():
            for keyword in keywords:
                if keyword in requirements_text:
                    if degree_level == 'phd':
                        return 5
                    elif degree_level == 'masters':
                        return 4
                    elif degree_level == 'bachelors':
                        return 3
                    elif degree_level == 'diploma':
                        return 2
                    elif degree_level == 'high_school':
                        return 1
        return 0
    
    def _extract_candidate_degree(self, candidate_text: str) -> int:
        """Extract candidate's highest degree level"""
        max_level = 0
        for degree_level, keywords in self.degree_keywords.items():
            for keyword in keywords:
                if keyword in candidate_text:
                    if degree_level == 'phd':
                        max_level = max(max_level, 5)
                    elif degree_level == 'masters':
                        max_level = max(max_level, 4)
                    elif degree_level == 'bachelors':
                        max_level = max(max_level, 3)
                    elif degree_level == 'diploma':
                        max_level = max(max_level, 2)
                    elif degree_level == 'high_school':
                        max_level = max(max_level, 1)
        return max_level
    
    def _compare_degree_levels(self, candidate_level: int, required_level: int) -> float:
        """Compare degree levels"""
        if required_level == 0:
            return 0.5  # No specific requirement
        
        if candidate_level >= required_level:
            return 1.0  # Meets or exceeds requirement
        elif candidate_level == required_level - 1:
            return 0.6  # One level below
        elif candidate_level > 0:
            return 0.3  # Has some education but insufficient
        else:
            return 0.0  # No matching education
    
    def _calculate_field_match(self, candidate_text: str, requirements_text: str) -> float:
        """Calculate field of study match"""
        matches = 0
        total_fields = 0
        
        for field, keywords in self.field_keywords.items():
            required = any(kw in requirements_text for kw in keywords)
            if required:
                total_fields += 1
                candidate_has = any(kw in candidate_text for kw in keywords)
                if candidate_has:
                    matches += 1
        
        if total_fields == 0:
            return 0.5  # No specific field required
        
        return matches / total_fields
    
    def _calculate_keyword_overlap(self, candidate_text: str, requirements_text: str) -> float:
        """Calculate simple keyword overlap"""
        # Extract words from requirements (excluding common words)
        stop_words = {'the', 'a', 'an', 'in', 'of', 'or', 'and', 'to', 'with', 'for', 'from'}
        
        req_words = set(re.findall(r'\b\w+\b', requirements_text.lower()))
        req_words = req_words - stop_words
        
        if not req_words:
            return 0.0
        
        # Count matching words
        matches = sum(1 for word in req_words if word in candidate_text)
        
        return matches / len(req_words)
