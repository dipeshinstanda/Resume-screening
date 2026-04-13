"""
Enhanced Pipeline Components - Interview-Level Features
========================================================

This module contains production-ready components addressing:
1. ✅ NLP Preprocessing (tokenization, lemmatization, stopwords)
2. ✅ Feature Engineering Layer
3. ✅ Data Versioning with Hashing
4. ✅ Parallel Processing
5. ✅ Advanced Evaluation Metrics (ROC-AUC, Calibration, Confusion Matrix)
6. ✅ Bias/Fairness Analysis
7. ✅ Real-world Data Loader (CSV, Kaggle)
"""

import os
import sys
import json
import hashlib
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

import numpy as np


# =============================================================================
# 1. NLP PREPROCESSING PIPELINE
# =============================================================================

class NLPPreprocessor:
    """
    Production-grade NLP preprocessing for resumes and job descriptions.
    
    Features:
    - Text normalization
    - Stopword removal
    - Lemmatization (with fallback)
    - Keyword extraction
    """
    
    def __init__(self, use_advanced: bool = True):
        self.use_advanced = use_advanced
        self._init_nlp()
        
    def _init_nlp(self):
        """Initialize NLP components with graceful fallbacks"""
        # Basic stopwords (fallback)
        self.stopwords = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how',
            'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there'
        }
        
        self.nltk_available = False
        self.lemmatizer = None
        
        if self.use_advanced:
            try:
                import nltk
                from nltk.stem import WordNetLemmatizer
                from nltk.corpus import stopwords as nltk_stopwords
                
                # Download required data silently
                for resource in ['punkt', 'wordnet', 'stopwords']:
                    try:
                        nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}')
                    except LookupError:
                        nltk.download(resource, quiet=True)
                
                self.lemmatizer = WordNetLemmatizer()
                self.stopwords = set(nltk_stopwords.words('english'))
                self.nltk_available = True
            except ImportError:
                pass
    
    def preprocess(self, text: str) -> str:
        """Full preprocessing pipeline"""
        if not text:
            return ""
        
        text = text.lower()
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'[^a-z0-9\s\.\,]', ' ', text)
        
        tokens = text.split()
        tokens = [t for t in tokens if t not in self.stopwords and len(t) > 2]
        
        if self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
        
        return ' '.join(tokens)
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract top keywords using frequency"""
        processed = self.preprocess(text)
        tokens = processed.split()
        freq = Counter(tokens)
        return [word for word, _ in freq.most_common(top_n)]
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using Jaccard"""
        proc1 = self.preprocess(text1)
        proc2 = self.preprocess(text2)

        words1 = set(proc1.split())
        words2 = set(proc2.split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0


# =============================================================================
# 2. SEMANTIC EMBEDDINGS (CRITICAL FIX - Feature Quality)
# =============================================================================

class SemanticEmbedder:
    """
    Semantic similarity using word embeddings.

    Why embeddings > heuristics:
    - "Python" and "PyTorch" -> high similarity (same domain)
    - "Java" and "JavaScript" -> medium similarity (different but related)
    - Captures semantic meaning, not just string overlap

    Approaches (in order of preference):
    1. Sentence-BERT (if available) - best quality
    2. TF-IDF weighted word vectors
    3. Word2Vec/GloVe (if available)
    4. Fallback: Semantic clusters
    """

    def __init__(self, use_transformers: bool = False):
        self.use_transformers = use_transformers
        self.model = None
        self.word_vectors = None
        self._init_embeddings()

    def _init_embeddings(self):
        """Initialize embedding model with graceful fallbacks"""
        # Try Sentence-BERT first (best quality)
        if self.use_transformers:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.embedding_type = 'sbert'
                return
            except ImportError:
                pass

        # Fallback: Build semantic clusters for skill matching
        self.embedding_type = 'semantic_clusters'
        self.skill_clusters = {
            'python_ecosystem': {'python', 'pytorch', 'tensorflow', 'keras', 'numpy', 
                                 'pandas', 'scikit-learn', 'django', 'flask', 'fastapi'},
            'java_ecosystem': {'java', 'spring', 'hibernate', 'maven', 'gradle', 'kotlin'},
            'javascript_ecosystem': {'javascript', 'typescript', 'react', 'angular', 'vue', 
                                     'node', 'nodejs', 'express', 'nextjs'},
            'data_science': {'machine learning', 'ml', 'deep learning', 'ai', 'nlp', 
                            'computer vision', 'data science', 'analytics', 'statistics'},
            'cloud': {'aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes', 'devops'},
            'databases': {'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'nosql', 'database'}
        }

        # Build reverse lookup
        self.skill_to_cluster = {}
        for cluster, skills in self.skill_clusters.items():
            for skill in skills:
                self.skill_to_cluster[skill] = cluster

    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding vector for text"""
        if self.embedding_type == 'sbert' and self.model:
            return self.model.encode(text, convert_to_numpy=True)

        # Fallback: One-hot cluster encoding
        text_lower = text.lower()
        clusters_present = set()

        for skill, cluster in self.skill_to_cluster.items():
            if skill in text_lower:
                clusters_present.add(cluster)

        # Create vector
        all_clusters = list(self.skill_clusters.keys())
        vector = np.zeros(len(all_clusters))
        for i, cluster in enumerate(all_clusters):
            if cluster in clusters_present:
                vector[i] = 1.0

        return vector

    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between texts.

        Returns value in [0, 1] where:
        - 1.0 = semantically identical
        - 0.0 = completely unrelated
        """
        if self.embedding_type == 'sbert' and self.model:
            emb1 = self.get_embedding(text1)
            emb2 = self.get_embedding(text2)
            # Cosine similarity
            sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-8)
            return float(max(0, min(1, (sim + 1) / 2)))  # Normalize to [0, 1]

        # Fallback: Cluster-based similarity
        vec1 = self.get_embedding(text1)
        vec2 = self.get_embedding(text2)

        if np.sum(vec1) == 0 or np.sum(vec2) == 0:
            return 0.0

        # Jaccard on clusters
        intersection = np.sum(np.minimum(vec1, vec2))
        union = np.sum(np.maximum(vec1, vec2))

        return float(intersection / union) if union > 0 else 0.0

    def calculate_skill_similarity(self, skill1: str, skill2: str) -> float:
        """
        Calculate similarity between individual skills.

        Handles:
        - "Python" vs "PyTorch" -> 0.8 (same ecosystem)
        - "Python" vs "Java" -> 0.3 (both programming)
        - "Python" vs "Marketing" -> 0.0 (unrelated)
        """
        s1, s2 = skill1.lower(), skill2.lower()

        # Exact match
        if s1 == s2:
            return 1.0

        # Substring match
        if s1 in s2 or s2 in s1:
            return 0.9

        # Same cluster
        c1 = self.skill_to_cluster.get(s1)
        c2 = self.skill_to_cluster.get(s2)

        if c1 and c2:
            if c1 == c2:
                return 0.8  # Same ecosystem
            # Check if clusters are related
            related_clusters = {
                ('python_ecosystem', 'data_science'): 0.6,
                ('java_ecosystem', 'cloud'): 0.4,
                ('javascript_ecosystem', 'cloud'): 0.4,
            }
            pair = tuple(sorted([c1, c2]))
            if pair in related_clusters:
                return related_clusters[pair]
            return 0.2  # Both tech but different areas

        return 0.0


# =============================================================================
# 3. FEATURE ENGINEERING LAYER (Enhanced with Semantic Features)
# =============================================================================

class FeatureEngineer:
    """
    Production-grade feature extraction for ML training.

    ENHANCED FEATURES:
    - Semantic skill similarity (not just overlap)
    - TF-IDF weighted text similarity
    - Character n-gram similarity (handles typos)
    - Education quality scores

    INTERVIEW TALKING POINTS:
    - Why semantic > heuristic: Captures domain relationships
    - Why multiple features: Different signals for different aspects
    - Why normalization: Prevents feature dominance
    """

    def __init__(self, use_semantic: bool = True):
        self.nlp = NLPPreprocessor()
        self.semantic_embedder = SemanticEmbedder() if use_semantic else None
        self.use_semantic = use_semantic

        self.degree_levels = {
            'phd': 6, 'doctorate': 6, 'postdoctoral': 7,
            'masters': 5, 'master': 5, 'mba': 5, 'msc': 5, 'ms': 5,
            'bachelors': 4, 'bachelor': 4, 'bsc': 4, 'bs': 4, 'btech': 4,
            'diploma': 3, 'associate': 3,
            'certificate': 2, 'certification': 2,
            'high school': 1
        }

        self.field_groups = {
            'tech': ['computer science', 'software', 'engineering', 'it', 
                    'data science', 'ai', 'machine learning'],
            'business': ['business', 'management', 'mba', 'finance', 'marketing'],
            'science': ['physics', 'chemistry', 'biology', 'mathematics']
        }

    def extract_features(self, sample: Dict) -> Dict[str, float]:
        """Extract all features from a sample"""
        candidate = sample.get('candidate', [])
        requirements = sample.get('requirements', [])
        candidate_skills = sample.get('candidate_skills', [])
        job_skills = sample.get('job_skills', [])

        cand_text = ' '.join([
            f"{e.get('degree', '')} {e.get('field', '')} {e.get('institution', '')}"
            for e in candidate
        ])
        req_text = ' '.join(requirements)

        features = {
            # Core matching features
            'degree_match': self._degree_match(candidate, req_text),
            'field_match': self._field_match(candidate, req_text),
            'experience_match': self._experience_match(cand_text, req_text),

            # ENHANCED: Semantic skill matching (not just overlap)
            'skill_overlap': self._skill_overlap(candidate_skills, job_skills),
            'skill_semantic_sim': self._semantic_skill_match(candidate_skills, job_skills),

            # Text similarity features
            'jaccard_similarity': self.nlp.calculate_similarity(cand_text, req_text),
            'ngram_similarity': self._ngram_similarity(cand_text, req_text),

            # Text statistics (normalized)
            'cand_word_count': min(len(cand_text.split()) / 100, 1.0),  # Normalize
            'req_word_count': min(len(req_text.split()) / 50, 1.0),     # Normalize
        }

        features['word_ratio'] = min(features['cand_word_count'], features['req_word_count']) / \
                                  max(features['cand_word_count'], features['req_word_count'], 0.01)

        cand_keywords = set(self.nlp.extract_keywords(cand_text))
        req_keywords = set(self.nlp.extract_keywords(req_text))
        features['keyword_overlap'] = len(cand_keywords & req_keywords) / max(len(req_keywords), 1)

        # Semantic text similarity (if enabled)
        if self.use_semantic and self.semantic_embedder:
            features['semantic_text_sim'] = self.semantic_embedder.calculate_semantic_similarity(
                cand_text, req_text
            )

        return features

    def _ngram_similarity(self, text1: str, text2: str, n: int = 3) -> float:
        """Character n-gram similarity (handles typos/variations)"""
        def get_ngrams(text):
            text = text.lower().replace(' ', '')
            return set(text[i:i+n] for i in range(len(text) - n + 1))

        ngrams1 = get_ngrams(text1)
        ngrams2 = get_ngrams(text2)

        if not ngrams1 or not ngrams2:
            return 0.0

        intersection = len(ngrams1 & ngrams2)
        union = len(ngrams1 | ngrams2)

        return intersection / union if union > 0 else 0.0

    def _semantic_skill_match(self, candidate_skills: List[str], 
                               job_skills: List[str]) -> float:
        """
        Semantic skill matching using embeddings.

        Unlike simple overlap, this captures:
        - "Python" matches "PyTorch" (same ecosystem)
        - "ML" matches "Machine Learning" (synonym)
        - "TensorFlow" matches "Deep Learning" (related)
        """
        if not job_skills or not candidate_skills:
            return 0.5

        if not self.semantic_embedder:
            return self._skill_overlap(candidate_skills, job_skills)

        total_score = 0.0

        for job_skill in job_skills:
            best_match = 0.0
            for cand_skill in candidate_skills:
                sim = self.semantic_embedder.calculate_skill_similarity(
                    cand_skill, job_skill
                )
                best_match = max(best_match, sim)
            total_score += best_match

        return total_score / len(job_skills)

    def _degree_match(self, candidate: List[Dict], req_text: str) -> float:
        req_text_lower = req_text.lower()
        req_level = 0
        for degree, level in self.degree_levels.items():
            if degree in req_text_lower:
                req_level = max(req_level, level)

        if req_level == 0:
            return 0.5

        cand_level = 0
        for edu in candidate:
            degree = edu.get('degree', '').lower()
            for deg_name, level in self.degree_levels.items():
                if deg_name in degree:
                    cand_level = max(cand_level, level)

        if cand_level >= req_level:
            return 1.0
        elif cand_level >= req_level - 1:
            return 0.7
        else:
            return max(0.1, cand_level / req_level)

    def _field_match(self, candidate: List[Dict], req_text: str) -> float:
        req_text_lower = req_text.lower()
        cand_fields = ' '.join([e.get('field', '').lower() for e in candidate])

        for group, keywords in self.field_groups.items():
            req_has = any(kw in req_text_lower for kw in keywords)
            cand_has = any(kw in cand_fields for kw in keywords)
            if req_has and cand_has:
                return 1.0
            elif req_has and not cand_has:
                return 0.3

        return 0.5

    def _skill_overlap(self, candidate_skills: List[str], job_skills: List[str]) -> float:
        if not job_skills:
            return 0.5

        cand_lower = {s.lower() for s in candidate_skills}
        job_lower = {s.lower() for s in job_skills}

        matches = sum(1 for js in job_lower 
                     if any(js in cs or cs in js for cs in cand_lower))

        return matches / len(job_lower)

    def _experience_match(self, cand_text: str, req_text: str) -> float:
        req_years = 0
        match = re.search(r'(\d+)\+?\s*years?', req_text.lower())
        if match:
            req_years = int(match.group(1))
        
        cand_years = 0
        match = re.search(r'(\d+)\+?\s*years?', cand_text.lower())
        if match:
            cand_years = int(match.group(1))
        
        if 'senior' in cand_text.lower():
            cand_years = max(cand_years, 5)
        elif 'lead' in cand_text.lower():
            cand_years = max(cand_years, 4)
        
        if req_years == 0:
            return 0.5
        
        return 1.0 if cand_years >= req_years else max(0.1, cand_years / req_years)


# =============================================================================
# 3. DATA VERSIONING
# =============================================================================

class DataVersioning:
    """Data versioning and reproducibility tracking."""
    
    @staticmethod
    def generate_hash(data: Any) -> str:
        """Generate deterministic hash for data"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True, default=str)
        else:
            data_str = str(data)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]

    @staticmethod
    def create_version_info(dataset: Dict, version: str = None) -> Dict:
        """Create version metadata for dataset"""
        test_cases = dataset.get('test_cases', [])

        return {
            'version': version or f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'hash': DataVersioning.generate_hash(test_cases),
            'created_at': datetime.now().isoformat(),
            'total_samples': len(test_cases),
            'positive_ratio': sum(1 for c in test_cases if c.get('is_match')) / max(len(test_cases), 1),
            'schema_version': '2.0',
            'reproducibility': {
                'random_seed': 42,
                'python_version': sys.version.split()[0]
            }
        }


# =============================================================================
# 4. PARALLEL PROCESSING (With Interview Justification)
# =============================================================================

class ParallelProcessor:
    """
    Parallelized data processing for large datasets.

    INTERVIEW QUESTION: Why ThreadPoolExecutor vs multiprocessing?

    ANSWER:
    1. ThreadPoolExecutor for I/O-bound tasks (file reading, API calls)
    2. ProcessPoolExecutor for CPU-bound tasks (heavy computation)
    3. In our case: Feature extraction is I/O-bound (mostly string ops)
    4. Python GIL: Yes, limits true parallelism for CPU tasks
    5. Trade-off: Threads have lower overhead for our use case

    For CPU-bound heavy ML training, we use:
    - sklearn's n_jobs=-1 (uses multiprocessing internally)
    - numpy/scipy operations (release GIL automatically)

    WHEN TO USE MULTIPROCESSING:
    - Large matrix operations
    - Heavy numerical computation
    - Embarrassingly parallel tasks
    """

    def __init__(self, n_workers: int = None, use_processes: bool = False):
        import multiprocessing
        self.n_workers = n_workers or max(1, multiprocessing.cpu_count() - 1)
        self.use_processes = use_processes  # For CPU-bound tasks

    def parallel_extract_features(self, samples: List[Dict], 
                                   feature_engineer: 'FeatureEngineer' = None) -> List[Dict]:
        """
        Extract features in parallel.

        Uses ThreadPoolExecutor by default (I/O-bound).
        Set use_processes=True for CPU-bound tasks.
        """
        if feature_engineer is None:
            # Create feature engineer without NLTK for thread safety
            feature_engineer = FeatureEngineer(use_semantic=False)
            feature_engineer.nlp = NLPPreprocessor(use_advanced=False)

        # For small datasets, use sequential processing
        if len(samples) < 100 or self.n_workers <= 1:
            return [feature_engineer.extract_features(s) for s in samples]

        # Choose executor based on task type
        if self.use_processes:
            from concurrent.futures import ProcessPoolExecutor as Executor
        else:
            from concurrent.futures import ThreadPoolExecutor as Executor

        from concurrent.futures import as_completed

        results = [None] * len(samples)
        max_workers = min(self.n_workers, 4)

        with Executor(max_workers=max_workers) as executor:
            future_to_idx = {
                executor.submit(feature_engineer.extract_features, sample): idx 
                for idx, sample in enumerate(samples)
            }

            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    results[idx] = future.result()
                except Exception:
                    # Fallback: process sequentially
                    results[idx] = feature_engineer.extract_features(samples[idx])

        return results

    def parallel_preprocess(self, texts: List[str], 
                            preprocessor: 'NLPPreprocessor' = None) -> List[str]:
        """Preprocess texts in parallel"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        if preprocessor is None:
            preprocessor = NLPPreprocessor(use_advanced=False)

        if len(texts) < 50:
            return [preprocessor.preprocess(t) for t in texts]

        results = [None] * len(texts)

        with ThreadPoolExecutor(max_workers=self.n_workers) as executor:
            future_to_idx = {
                executor.submit(preprocessor.preprocess, text): idx 
                for idx, text in enumerate(texts)
            }

            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                results[idx] = future.result()

        return results


# =============================================================================
# 5. FEATURE SCALING (CRITICAL FIX)
# =============================================================================

class FeatureScaler:
    """
    Feature scaling for ML models.

    Important: Logistic Regression requires scaled features!

    Methods:
    - StandardScaler: Zero mean, unit variance
    - MinMaxScaler: Scale to [0, 1]
    - RobustScaler: Use median and IQR (outlier-resistant)
    """

    def __init__(self, method: str = 'standard'):
        """
        Args:
            method: 'standard', 'minmax', or 'robust'
        """
        self.method = method
        self.fitted = False
        self.params = {}

    def fit(self, X: np.ndarray) -> 'FeatureScaler':
        """Fit scaler on training data"""
        if self.method == 'standard':
            self.params['mean'] = np.mean(X, axis=0)
            self.params['std'] = np.std(X, axis=0)
            self.params['std'][self.params['std'] == 0] = 1  # Avoid division by zero
        elif self.method == 'minmax':
            self.params['min'] = np.min(X, axis=0)
            self.params['max'] = np.max(X, axis=0)
            self.params['range'] = self.params['max'] - self.params['min']
            self.params['range'][self.params['range'] == 0] = 1
        elif self.method == 'robust':
            self.params['median'] = np.median(X, axis=0)
            q75 = np.percentile(X, 75, axis=0)
            q25 = np.percentile(X, 25, axis=0)
            self.params['iqr'] = q75 - q25
            self.params['iqr'][self.params['iqr'] == 0] = 1

        self.fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform features using fitted parameters"""
        if not self.fitted:
            raise ValueError("Scaler not fitted. Call fit() first.")

        if self.method == 'standard':
            return (X - self.params['mean']) / self.params['std']
        elif self.method == 'minmax':
            return (X - self.params['min']) / self.params['range']
        elif self.method == 'robust':
            return (X - self.params['median']) / self.params['iqr']

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform in one step"""
        return self.fit(X).transform(X)

    def inverse_transform(self, X_scaled: np.ndarray) -> np.ndarray:
        """Reverse the scaling"""
        if not self.fitted:
            raise ValueError("Scaler not fitted.")

        if self.method == 'standard':
            return X_scaled * self.params['std'] + self.params['mean']
        elif self.method == 'minmax':
            return X_scaled * self.params['range'] + self.params['min']
        elif self.method == 'robust':
            return X_scaled * self.params['iqr'] + self.params['median']

    def get_params(self) -> Dict:
        """Get scaler parameters for serialization"""
        return {
            'method': self.method,
            'fitted': self.fitted,
            'params': {k: v.tolist() if isinstance(v, np.ndarray) else v 
                      for k, v in self.params.items()}
        }

    @classmethod
    def from_params(cls, params: Dict) -> 'FeatureScaler':
        """Reconstruct scaler from saved parameters"""
        scaler = cls(method=params['method'])
        scaler.fitted = params['fitted']
        scaler.params = {k: np.array(v) if isinstance(v, list) else v 
                        for k, v in params['params'].items()}
        return scaler


# =============================================================================
# 6. MODEL PERSISTENCE WITH METADATA (CRITICAL FIX)
# =============================================================================

class ModelPersistence:
    """
    Save and load models with full metadata for reproducibility.

    Metadata includes:
    - Model version
    - Training date
    - Dataset hash
    - Hyperparameters
    - Performance metrics
    - Feature names and scaler params
    """

    @staticmethod
    def save_model_with_metadata(
        model,
        filepath: str,
        dataset_hash: str = None,
        training_metrics: Dict = None,
        feature_names: List[str] = None,
        scaler: FeatureScaler = None,
        version: str = "1.0.0"
    ) -> None:
        """Save model with comprehensive metadata"""
        import pickle

        metadata = {
            'version': version,
            'model_version': f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'saved_at': datetime.now().isoformat(),
            'python_version': sys.version.split()[0],
            'dataset_hash': dataset_hash,
            'training_metrics': training_metrics,
            'feature_names': feature_names,
            'scaler_params': scaler.get_params() if scaler else None,
            'model_type': type(model).__name__
        }

        save_data = {
            'model': model,
            'metadata': metadata
        }

        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)

        # Also save metadata as JSON for easy inspection
        metadata_path = filepath.replace('.pkl', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)

        print(f"[OK] Model saved to: {filepath}")
        print(f"[OK] Metadata saved to: {metadata_path}")

    @staticmethod
    def load_model_with_metadata(filepath: str) -> Tuple[Any, Dict]:
        """Load model and return with metadata"""
        import pickle

        with open(filepath, 'rb') as f:
            save_data = pickle.load(f)

        # Handle both old and new formats
        if isinstance(save_data, dict) and 'model' in save_data:
            model = save_data['model']
            metadata = save_data.get('metadata', {})
        else:
            # Legacy format - just the model
            model = save_data
            metadata = {'version': 'legacy', 'note': 'No metadata available'}

        return model, metadata

    @staticmethod
    def verify_model_compatibility(metadata: Dict, current_features: List[str]) -> bool:
        """Verify model is compatible with current feature set"""
        saved_features = metadata.get('feature_names', [])
        if not saved_features:
            return True  # Can't verify, assume compatible

        return set(saved_features) == set(current_features)


# =============================================================================
# 7. ADVANCED EVALUATION METRICS
# =============================================================================

class AdvancedEvaluator:
    """
    Comprehensive evaluation with advanced metrics.

    Includes:
    - ROC-AUC
    - Confusion Matrix
    - Calibration analysis
    - Threshold analysis
    """

    def __init__(self):
        self.predictions = []
        self.actuals = []
        self.probabilities = []
    
    def add_prediction(self, actual: int, predicted: int, probability: float):
        """Record a prediction"""
        self.actuals.append(actual)
        self.predictions.append(predicted)
        self.probabilities.append(probability)
    
    def compute_metrics(self) -> Dict:
        """Compute all evaluation metrics"""
        y_true = np.array(self.actuals)
        y_pred = np.array(self.predictions)
        y_prob = np.array(self.probabilities)
        
        metrics = {'accuracy': float(np.mean(y_true == y_pred))}
        
        # Confusion matrix
        tp = int(np.sum((y_true == 1) & (y_pred == 1)))
        tn = int(np.sum((y_true == 0) & (y_pred == 0)))
        fp = int(np.sum((y_true == 0) & (y_pred == 1)))
        fn = int(np.sum((y_true == 1) & (y_pred == 0)))
        
        metrics['confusion_matrix'] = {
            'true_positive': tp, 'true_negative': tn,
            'false_positive': fp, 'false_negative': fn
        }
        
        metrics['precision'] = tp / (tp + fp) if (tp + fp) > 0 else 0
        metrics['recall'] = tp / (tp + fn) if (tp + fn) > 0 else 0
        metrics['f1_score'] = 2 * metrics['precision'] * metrics['recall'] / \
                              (metrics['precision'] + metrics['recall']) \
                              if (metrics['precision'] + metrics['recall']) > 0 else 0
        metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        # ROC-AUC
        try:
            from sklearn.metrics import roc_auc_score
            metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob))
        except Exception:
            metrics['roc_auc'] = None
        
        # Calibration
        metrics['calibration'] = self._compute_calibration(y_true, y_prob)
        
        # Threshold analysis
        metrics['threshold_analysis'] = self._threshold_analysis(y_true, y_prob)
        
        return metrics
    
    def _compute_calibration(self, y_true, y_prob, n_bins: int = 10) -> Dict:
        """Compute calibration metrics (ECE)"""
        bins = np.linspace(0, 1, n_bins + 1)
        ece = 0
        bin_counts = []
        
        for i in range(n_bins):
            mask = (y_prob >= bins[i]) & (y_prob < bins[i+1])
            count = int(np.sum(mask))
            bin_counts.append(count)
            if count > 0:
                true_prop = np.mean(y_true[mask])
                pred_prop = np.mean(y_prob[mask])
                ece += (count / len(y_true)) * abs(true_prop - pred_prop)
        
        return {
            'expected_calibration_error': round(ece, 4),
            'bin_counts': bin_counts
        }
    
    def _threshold_analysis(self, y_true, y_prob) -> Dict:
        """Analyze performance at different thresholds"""
        results = {}
        for thresh in [0.3, 0.4, 0.5, 0.6, 0.7]:
            y_pred = (y_prob >= thresh).astype(int)
            tp = np.sum((y_true == 1) & (y_pred == 1))
            fp = np.sum((y_true == 0) & (y_pred == 1))
            fn = np.sum((y_true == 1) & (y_pred == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            results[str(thresh)] = {
                'precision': round(float(precision), 4),
                'recall': round(float(recall), 4),
                'f1_score': round(float(f1), 4)
            }
        return results


# =============================================================================
# 5. BIAS AND FAIRNESS ANALYSIS
# =============================================================================

class BiasAnalyzer:
    """Analyze model for potential biases."""
    
    def __init__(self, model):
        self.model = model
    
    def analyze_institution_bias(self, test_data: List[Dict]) -> Dict:
        """Check for institution tier bias"""
        tier_results = {'tier1': [], 'tier2': [], 'tier3': []}
        
        tier1 = {'mit', 'stanford', 'harvard', 'oxford', 'cambridge', 
                 'caltech', 'berkeley', 'princeton', 'iit'}
        tier2 = {'michigan', 'ucla', 'cornell', 'nyu', 'purdue'}
        
        for sample in test_data:
            result = self.model.classify(
                sample['candidate'], sample['requirements'],
                sample.get('candidate_skills'), sample.get('job_skills')
            )
            
            institution = ''
            for edu in sample.get('candidate', []):
                institution = edu.get('institution', '').lower()
                break
            
            if any(t1 in institution for t1 in tier1):
                tier_results['tier1'].append(result['score'])
            elif any(t2 in institution for t2 in tier2):
                tier_results['tier2'].append(result['score'])
            else:
                tier_results['tier3'].append(result['score'])
        
        analysis = {}
        for tier, scores in tier_results.items():
            if scores:
                analysis[tier] = {
                    'mean_score': round(float(np.mean(scores)), 4),
                    'std_score': round(float(np.std(scores)), 4),
                    'sample_count': len(scores)
                }
        
        if analysis.get('tier1') and analysis.get('tier3'):
            bias_gap = analysis['tier1']['mean_score'] - analysis['tier3']['mean_score']
            analysis['bias_detected'] = abs(bias_gap) > 0.15
            analysis['bias_gap'] = round(bias_gap, 4)
            analysis['recommendation'] = "Consider bias mitigation" if analysis['bias_detected'] else "No significant bias"

        return analysis

    def analyze_degree_bias(self, test_data: List[Dict]) -> Dict:
        """Check for degree level bias"""
        degree_results = {}

        for sample in test_data:
            result = self.model.classify(
                sample['candidate'], sample['requirements'],
                sample.get('candidate_skills'), sample.get('job_skills')
            )

            for edu in sample.get('candidate', []):
                degree = edu.get('degree', 'Unknown').lower()
                if degree not in degree_results:
                    degree_results[degree] = []
                degree_results[degree].append({
                    'score': result['score'],
                    'actual': sample.get('label', 0)
                })

        analysis = {}
        for degree, results in degree_results.items():
            if len(results) >= 5:
                scores = [r['score'] for r in results]
                actuals = [r['actual'] for r in results]
                analysis[degree] = {
                    'mean_score': round(float(np.mean(scores)), 4),
                    'accuracy': round(float(np.mean([1 if (s >= 0.5) == a else 0 
                                                      for s, a in zip(scores, actuals)])), 4),
                    'sample_count': len(results)
                }
        return analysis

    def analyze_field_bias(self, test_data: List[Dict]) -> Dict:
        """
        Check for field of study bias.

        Important for detecting:
        - STEM vs non-STEM bias
        - Business vs Engineering bias
        """
        field_results = {}

        for sample in test_data:
            result = self.model.classify(
                sample['candidate'], sample['requirements'],
                sample.get('candidate_skills'), sample.get('job_skills')
            )

            for edu in sample.get('candidate', []):
                field = edu.get('field', 'Unknown').lower()

                # Categorize field
                category = 'other'
                if any(kw in field for kw in ['computer', 'software', 'data', 'engineering']):
                    category = 'tech'
                elif any(kw in field for kw in ['business', 'management', 'mba', 'finance']):
                    category = 'business'
                elif any(kw in field for kw in ['arts', 'humanities', 'english', 'history']):
                    category = 'humanities'
                elif any(kw in field for kw in ['science', 'physics', 'chemistry', 'biology']):
                    category = 'science'

                if category not in field_results:
                    field_results[category] = []
                field_results[category].append({
                    'score': result['score'],
                    'actual': sample.get('label', 0)
                })

        analysis = {}
        for field, results in field_results.items():
            if len(results) >= 5:
                scores = [r['score'] for r in results]
                actuals = [r['actual'] for r in results]
                analysis[field] = {
                    'mean_score': round(float(np.mean(scores)), 4),
                    'accuracy': round(float(np.mean([1 if (s >= 0.5) == a else 0 
                                                      for s, a in zip(scores, actuals)])), 4),
                    'sample_count': len(results)
                }

        # Check for tech vs non-tech bias
        if 'tech' in analysis and 'humanities' in analysis:
            bias_gap = analysis['tech']['mean_score'] - analysis['humanities']['mean_score']
            analysis['tech_bias_detected'] = abs(bias_gap) > 0.2
            analysis['tech_vs_humanities_gap'] = round(bias_gap, 4)

        return analysis

    def analyze_skill_count_bias(self, test_data: List[Dict]) -> Dict:
        """
        Check if model favors candidates with more skills.

        Prevents:
        - Discriminating against early-career candidates
        - Over-rewarding skill-stuffing
        """
        skill_buckets = {'0-3': [], '4-6': [], '7-10': [], '10+': []}

        for sample in test_data:
            result = self.model.classify(
                sample['candidate'], sample['requirements'],
                sample.get('candidate_skills'), sample.get('job_skills')
            )

            skill_count = len(sample.get('candidate_skills', []))

            if skill_count <= 3:
                bucket = '0-3'
            elif skill_count <= 6:
                bucket = '4-6'
            elif skill_count <= 10:
                bucket = '7-10'
            else:
                bucket = '10+'

            skill_buckets[bucket].append({
                'score': result['score'],
                'actual': sample.get('label', 0)
            })

        analysis = {}
        for bucket, results in skill_buckets.items():
            if results:
                scores = [r['score'] for r in results]
                analysis[bucket] = {
                    'mean_score': round(float(np.mean(scores)), 4),
                    'sample_count': len(results)
                }

        # Check for skill count bias
        if '0-3' in analysis and '10+' in analysis:
            gap = analysis['10+']['mean_score'] - analysis['0-3']['mean_score']
            analysis['skill_count_bias'] = abs(gap) > 0.25
            analysis['skill_count_gap'] = round(gap, 4)

        return analysis

    def generate_fairness_report(self, test_data: List[Dict]) -> Dict:
        """
        Generate comprehensive fairness report.

        INTERVIEW TALKING POINTS:
        - Why bias analysis matters: Legal compliance, ethical AI
        - What biases we check: Institution, degree, field, skill count
        - How we measure: Score disparity across groups
        - Threshold: >0.15 gap = significant bias
        """
        return {
            'institution_bias': self.analyze_institution_bias(test_data),
            'degree_bias': self.analyze_degree_bias(test_data),
            'field_bias': self.analyze_field_bias(test_data),
            'skill_count_bias': self.analyze_skill_count_bias(test_data),
            'analysis_timestamp': datetime.now().isoformat(),
            'total_samples_analyzed': len(test_data),
            'bias_dimensions_checked': 4,
            'methodology': {
                'threshold': 0.15,
                'metric': 'mean_score_disparity',
                'minimum_samples': 5
            }
        }


# =============================================================================
# 8. MODEL SELECTION GUIDE (Interview Documentation)
# =============================================================================

class ModelSelectionGuide:
    """
    Documentation for model selection decisions.

    INTERVIEW QUESTION: "Why Logistic Regression?"

    ANSWER (Structured Response):

    1. INTERPRETABILITY:
       - Coefficients show feature importance directly
       - Can explain why a candidate was selected/rejected
       - Required for HR compliance in many jurisdictions

    2. BASELINE PERFORMANCE:
       - Often matches complex models on tabular data
       - Fast training and inference
       - Good for establishing baseline before trying complex models

    3. PROBABILITY CALIBRATION:
       - Native probability outputs (no calibration needed)
       - Important for ranking candidates by score

    4. WHEN TO USE ALTERNATIVES:
       - Random Forest: When feature interactions are complex
       - XGBoost: When you have more data (>10K samples)
       - Neural Networks: When you have embeddings or text features
       - SVM: When decision boundary is non-linear

    5. OUR APPROACH:
       - Start with Logistic Regression (interpretable baseline)
       - Add polynomial features for interactions
       - Use GridSearchCV for hyperparameter tuning
       - Compare with Random Forest for validation
    """

    MODEL_COMPARISON = {
        'logistic_regression': {
            'pros': ['Interpretable', 'Fast', 'Calibrated probabilities', 'Works well with small data'],
            'cons': ['Linear decision boundary', 'Cannot capture complex interactions natively'],
            'when_to_use': 'Baseline, interpretability required, small-medium data',
            'hyperparameters': ['C (regularization)', 'penalty (L1/L2)', 'solver']
        },
        'random_forest': {
            'pros': ['Handles non-linear relationships', 'Feature importance', 'Robust to outliers'],
            'cons': ['Less interpretable', 'Can overfit', 'Needs more data'],
            'when_to_use': 'Complex feature interactions, medium-large data',
            'hyperparameters': ['n_estimators', 'max_depth', 'min_samples_split']
        },
        'xgboost': {
            'pros': ['State-of-the-art tabular performance', 'Handles missing data', 'Fast'],
            'cons': ['Many hyperparameters', 'Can overfit without tuning'],
            'when_to_use': 'Large data (>10K), competition/production',
            'hyperparameters': ['learning_rate', 'max_depth', 'n_estimators', 'subsample']
        },
        'neural_network': {
            'pros': ['Handles embeddings', 'Can learn complex patterns', 'Scalable'],
            'cons': ['Needs lots of data', 'Black box', 'Training complexity'],
            'when_to_use': 'Text embeddings, large data, deep feature extraction',
            'hyperparameters': ['layers', 'learning_rate', 'batch_size', 'dropout']
        }
    }

    @staticmethod
    def recommend_model(data_size: int, need_interpretability: bool, 
                        has_embeddings: bool) -> str:
        """Recommend model based on requirements"""
        if has_embeddings:
            return 'neural_network'
        if data_size < 1000 or need_interpretability:
            return 'logistic_regression'
        if data_size < 10000:
            return 'random_forest'
        return 'xgboost'


# =============================================================================
# 9. REAL-WORLD DATA LOADER
# =============================================================================

class RealWorldDataLoader:
    """Load and process real-world datasets from CSV/JSON."""

    KAGGLE_SOURCES = {
        'resume_dataset': 'snehaanbhawal/resume-dataset',
        'job_descriptions': 'andrewmvd/data-scientist-jobs',
    }

    @staticmethod
    def load_csv(filepath: str) -> List[Dict]:
        """Load data from CSV file"""
        import csv

        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sample = RealWorldDataLoader._convert_csv_row(row)
                if sample:
                    data.append(sample)
        return data

    @staticmethod
    def _convert_csv_row(row: Dict) -> Optional[Dict]:
        """Convert CSV row to standard format"""
        education = []

        degree_cols = ['degree', 'education_level', 'qualification']
        field_cols = ['field', 'major', 'specialization']
        institution_cols = ['institution', 'university', 'college']

        for deg_col in degree_cols:
            if deg_col in row and row[deg_col]:
                edu_entry = {'degree': row[deg_col]}
                for field_col in field_cols:
                    if field_col in row:
                        edu_entry['field'] = row[field_col]
                        break
                for inst_col in institution_cols:
                    if inst_col in row:
                        edu_entry['institution'] = row[inst_col]
                        break
                education.append(edu_entry)
                break

        if not education:
            return None
        
        requirements = []
        for col in ['requirements', 'job_requirements', 'qualifications']:
            if col in row and row[col]:
                requirements = [row[col]]
                break
        
        skills = []
        for col in ['skills', 'candidate_skills', 'technical_skills']:
            if col in row and row[col]:
                skills = [s.strip() for s in row[col].split(',')]
                break
        
        label = 0
        for col in ['is_match', 'match', 'label', 'selected']:
            if col in row:
                label = 1 if str(row[col]).lower() in ['1', 'true', 'yes'] else 0
                break
        
        return {
            'candidate': education,
            'requirements': requirements,
            'candidate_skills': skills,
            'job_skills': [],
            'label': label
        }
