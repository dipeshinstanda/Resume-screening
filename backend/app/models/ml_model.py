"""
ML-based Education Matching Model

This module provides both rule-based similarity matching and
trainable ML classification for resume-job matching.

Gaps Addressed:
- ✅ True ML with trainable classifier (LogisticRegression/RandomForest)
- ✅ Learnable weights instead of hardcoded values
- ✅ Classification output (SELECTED/REJECTED)
- ✅ Evaluation metrics integration
- ✅ No hardcoded institution bias
"""

import re
import os
import pickle
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np


class EducationMatcher:
    """
    Rule-based similarity matcher (baseline approach).
    Uses TF-IDF + cosine similarity with degree hierarchy matching.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=500
        )
        self.degree_hierarchy = {
            'phd': 5,
            'doctorate': 5,
            'masters': 4,
            'master': 4,
            'mba': 4,
            'bachelor': 3,
            'bachelors': 3,
            'undergraduate': 3,
            'diploma': 2,
            'associate': 2,
            'high school': 1,
            'secondary': 1
        }

    def calculate_match_score(self, candidate_education, job_requirements):
        """Calculate similarity-based match score (0.0 to 1.0)"""
        if not candidate_education or not job_requirements:
            return 0.0

        candidate_text = ' '.join([
            f"{edu.get('degree', '')} {edu.get('field', '')} {edu.get('institution', '')}"
            for edu in candidate_education
        ]).lower()

        requirements_text = ' '.join(job_requirements).lower()

        if not candidate_text.strip() or not requirements_text.strip():
            return 0.0

        try:
            vectors = self.vectorizer.fit_transform([candidate_text, requirements_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        except Exception:
            similarity = 0.0

        degree_match = self._calculate_degree_match(candidate_education, requirements_text)
        field_match = self._calculate_field_match(candidate_text, requirements_text)

        # Weighted combination
        final_score = (similarity * 0.4) + (degree_match * 0.35) + (field_match * 0.25)

        return round(final_score, 3)

    def classify(self, candidate_education, job_requirements, threshold: float = 0.5) -> Dict:
        """
        Classify candidate as SELECTED or REJECTED based on threshold.

        Returns:
            Dict with score, decision, and confidence
        """
        score = self.calculate_match_score(candidate_education, job_requirements)
        decision = 'SELECTED' if score >= threshold else 'REJECTED'
        confidence = min(abs(score - threshold) / max(threshold, 1 - threshold), 1.0)

        return {
            'score': score,
            'decision': decision,
            'confidence': round(confidence, 3),
            'threshold': threshold
        }

    def _calculate_degree_match(self, candidate_education, requirements_text) -> float:
        """Calculate degree level match score"""
        candidate_degrees = []
        for edu in candidate_education:
            degree = edu.get('degree', '').lower()
            for key in self.degree_hierarchy:
                if key in degree:
                    candidate_degrees.append(self.degree_hierarchy[key])
                    break

        if not candidate_degrees:
            return 0.0

        max_candidate_level = max(candidate_degrees)

        required_level = 0
        for key, level in self.degree_hierarchy.items():
            if key in requirements_text:
                required_level = max(required_level, level)

        if required_level == 0:
            return 0.5

        if max_candidate_level >= required_level:
            return 1.0
        else:
            return max_candidate_level / required_level

    def _calculate_field_match(self, candidate_text: str, requirements_text: str) -> float:
        """Calculate field of study overlap score"""
        candidate_words = set(candidate_text.split())
        requirement_words = set(requirements_text.split())

        if not candidate_words or not requirement_words:
            return 0.0

        overlap = candidate_words.intersection(requirement_words)
        union = candidate_words.union(requirement_words)

        return len(overlap) / len(union) if union else 0.0


class TrainableEducationMatcher:
    """
    True ML model that learns optimal weights from labeled training data.

    Features:
    - Trains on labeled resume-job pairs
    - Learns feature weights automatically
    - Provides probability-based predictions
    - Supports model persistence (save/load)
    - Cross-validation for robust evaluation
    """

    def __init__(self, model_type: str = 'logistic'):
        """
        Initialize trainable matcher.

        Args:
            model_type: 'logistic' for LogisticRegression, 'rf' for RandomForest
        """
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=500
        )

        if model_type == 'rf':
            self.classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
        else:
            self.classifier = LogisticRegression(
                max_iter=1000,
                random_state=42
            )

        self.model_type = model_type
        self.is_trained = False
        self.feature_names = ['tfidf_similarity', 'degree_match', 'field_overlap', 'text_length_ratio']

        self.degree_hierarchy = {
            'phd': 5, 'doctorate': 5,
            'masters': 4, 'master': 4, 'mba': 4,
            'bachelor': 3, 'bachelors': 3, 'undergraduate': 3,
            'diploma': 2, 'associate': 2,
            'high school': 1, 'secondary': 1
        }

    def extract_features(self, candidate_education: List[Dict], job_requirements: List[str]) -> np.ndarray:
        """
        Extract feature vector for ML model.

        Features:
        1. TF-IDF cosine similarity
        2. Degree level match ratio
        3. Field overlap (Jaccard)
        4. Text length ratio
        """
        cand_text = ' '.join([
            f"{e.get('degree', '')} {e.get('field', '')}"
            for e in candidate_education
        ]).lower()
        req_text = ' '.join(job_requirements).lower()

        # Feature 1: TF-IDF cosine similarity
        try:
            vectors = self.vectorizer.fit_transform([cand_text, req_text])
            tfidf_sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        except Exception:
            tfidf_sim = 0.0

        # Feature 2: Degree match ratio
        degree_match = self._degree_match_score(candidate_education, req_text)

        # Feature 3: Field overlap (Jaccard similarity)
        field_overlap = self._field_overlap_score(cand_text, req_text)

        # Feature 4: Text length ratio (normalized)
        len_ratio = min(len(cand_text), len(req_text)) / max(len(cand_text), len(req_text), 1)

        return np.array([tfidf_sim, degree_match, field_overlap, len_ratio])

    def train(self, training_data: List[Dict], test_size: float = 0.2) -> Dict:
        """
        Train model on labeled data.

        Args:
            training_data: List of {'candidate': [...], 'requirements': [...], 'label': 0/1}
            test_size: Fraction of data for validation

        Returns:
            Dict with training metrics (accuracy, feature importances)
        """
        if not training_data or len(training_data) < 5:
            raise ValueError("Need at least 5 training samples")

        X = np.array([
            self.extract_features(d['candidate'], d['requirements'])
            for d in training_data
        ])
        y = np.array([d['label'] for d in training_data])

        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y if len(set(y)) > 1 else None
        )

        # Train classifier
        self.classifier.fit(X_train, y_train)
        self.is_trained = True

        # Calculate metrics
        train_accuracy = self.classifier.score(X_train, y_train)
        val_accuracy = self.classifier.score(X_val, y_val)

        # Get feature importances
        if hasattr(self.classifier, 'coef_'):
            importances = dict(zip(self.feature_names, self.classifier.coef_[0].tolist()))
        elif hasattr(self.classifier, 'feature_importances_'):
            importances = dict(zip(self.feature_names, self.classifier.feature_importances_.tolist()))
        else:
            importances = {}

        return {
            'train_accuracy': round(train_accuracy, 4),
            'val_accuracy': round(val_accuracy, 4),
            'feature_importances': importances,
            'samples_trained': len(X_train),
            'samples_validated': len(X_val)
        }

    def cross_validate(self, training_data: List[Dict], cv: int = 5) -> Dict:
        """
        Perform k-fold cross-validation.

        Args:
            training_data: Labeled training data
            cv: Number of folds

        Returns:
            Dict with mean and std of accuracy across folds
        """
        X = np.array([
            self.extract_features(d['candidate'], d['requirements'])
            for d in training_data
        ])
        y = np.array([d['label'] for d in training_data])

        scores = cross_val_score(self.classifier, X, y, cv=min(cv, len(X)))

        return {
            'cv_mean_accuracy': round(float(np.mean(scores)), 4),
            'cv_std_accuracy': round(float(np.std(scores)), 4),
            'cv_scores': [round(s, 4) for s in scores.tolist()],
            'cv_folds': len(scores)
        }

    def predict(self, candidate_education: List[Dict], job_requirements: List[str]) -> float:
        """
        Predict match probability (0.0 to 1.0).

        Args:
            candidate_education: Candidate's education list
            job_requirements: Job requirement strings

        Returns:
            Probability of being a good match
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")

        features = self.extract_features(candidate_education, job_requirements)
        proba = self.classifier.predict_proba([features])[0]

        # Return probability of positive class (index 1)
        return float(proba[1]) if len(proba) > 1 else float(proba[0])

    def classify(self, candidate_education: List[Dict], job_requirements: List[str], 
                 threshold: float = 0.5) -> Dict:
        """
        Classify candidate as SELECTED or REJECTED.

        Returns:
            Dict with score, decision, confidence
        """
        score = self.predict(candidate_education, job_requirements)
        decision = 'SELECTED' if score >= threshold else 'REJECTED'
        confidence = abs(score - threshold) / max(threshold, 1 - threshold)

        return {
            'score': round(score, 3),
            'decision': decision,
            'confidence': round(min(confidence, 1.0), 3),
            'threshold': threshold,
            'model_type': self.model_type
        }

    def save_model(self, path: str = 'trained_model.pkl') -> None:
        """Save trained model to file."""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")

        with open(path, 'wb') as f:
            pickle.dump({
                'classifier': self.classifier,
                'vectorizer': self.vectorizer,
                'model_type': self.model_type,
                'feature_names': self.feature_names
            }, f)

    def load_model(self, path: str = 'trained_model.pkl') -> None:
        """Load trained model from file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")

        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.classifier = data['classifier']
            self.vectorizer = data['vectorizer']
            self.model_type = data['model_type']
            self.feature_names = data['feature_names']
            self.is_trained = True

    def _degree_match_score(self, candidate_education: List[Dict], requirements_text: str) -> float:
        """Calculate degree level match score"""
        candidate_levels = []
        for edu in candidate_education:
            degree = edu.get('degree', '').lower()
            for key, level in self.degree_hierarchy.items():
                if key in degree:
                    candidate_levels.append(level)
                    break

        if not candidate_levels:
            return 0.0

        max_cand = max(candidate_levels)

        required_level = 0
        for key, level in self.degree_hierarchy.items():
            if key in requirements_text:
                required_level = max(required_level, level)

        if required_level == 0:
            return 0.5

        return min(max_cand / required_level, 1.0)

    def _field_overlap_score(self, cand_text: str, req_text: str) -> float:
        """Calculate Jaccard similarity of field words"""
        cand_words = set(cand_text.split())
        req_words = set(req_text.split())

        if not cand_words or not req_words:
            return 0.0

        intersection = cand_words & req_words
        union = cand_words | req_words

        return len(intersection) / len(union) if union else 0.0
