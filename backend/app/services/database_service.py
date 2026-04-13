import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class DatabaseService:
    def __init__(self, db_path='database/resume_screening.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                education TEXT,
                upload_date TEXT NOT NULL,
                file_path TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                requirements TEXT,
                education_requirements TEXT,
                created_date TEXT NOT NULL,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id TEXT NOT NULL,
                job_id TEXT NOT NULL,
                score REAL NOT NULL,
                match_date TEXT NOT NULL,
                FOREIGN KEY (resume_id) REFERENCES resumes (id),
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT,
                metrics TEXT NOT NULL,
                created_date TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_resume(self, resume_data: Dict) -> bool:
        """Save resume to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO resumes (id, filename, education, upload_date, file_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                resume_data['id'],
                resume_data['filename'],
                json.dumps(resume_data.get('education', [])),
                resume_data.get('upload_date', datetime.now().isoformat()),
                resume_data.get('file_path', '')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving resume: {e}")
            return False
    
    def get_all_resumes(self) -> List[Dict]:
        """Get all resumes from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resumes ORDER BY upload_date DESC')
        rows = cursor.fetchall()
        
        resumes = []
        for row in rows:
            resumes.append({
                'id': row['id'],
                'filename': row['filename'],
                'education': json.loads(row['education']) if row['education'] else [],
                'upload_date': row['upload_date'],
                'file_path': row['file_path']
            })
        
        conn.close()
        return resumes
    
    def get_resume_by_id(self, resume_id: str) -> Optional[Dict]:
        """Get resume by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'filename': row['filename'],
                'education': json.loads(row['education']) if row['education'] else [],
                'upload_date': row['upload_date'],
                'file_path': row['file_path']
            }
        return None
    
    def delete_resume(self, resume_id: str) -> bool:
        """Delete resume from database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM resumes WHERE id = ?', (resume_id,))
            cursor.execute('DELETE FROM matches WHERE resume_id = ?', (resume_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting resume: {e}")
            return False
    
    def save_job(self, job_data: Dict) -> bool:
        """Save job to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO jobs (id, title, description, requirements, 
                                            education_requirements, created_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data['id'],
                job_data['title'],
                job_data.get('description', ''),
                json.dumps(job_data.get('requirements', [])),
                json.dumps(job_data.get('education_requirements', [])),
                job_data.get('created_date', datetime.now().isoformat()),
                job_data.get('status', 'active')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving job: {e}")
            return False
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs ORDER BY created_date DESC')
        rows = cursor.fetchall()
        
        jobs = []
        for row in rows:
            jobs.append({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'requirements': json.loads(row['requirements']) if row['requirements'] else [],
                'education_requirements': json.loads(row['education_requirements']) if row['education_requirements'] else [],
                'created_date': row['created_date'],
                'status': row['status']
            })
        
        conn.close()
        return jobs
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """Get job by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'requirements': json.loads(row['requirements']) if row['requirements'] else [],
                'education_requirements': json.loads(row['education_requirements']) if row['education_requirements'] else [],
                'created_date': row['created_date'],
                'status': row['status']
            }
        return None
    
    def delete_job(self, job_id: str) -> bool:
        """Delete job from database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
            cursor.execute('DELETE FROM matches WHERE job_id = ?', (job_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting job: {e}")
            return False
    
    def save_match(self, match_data: Dict) -> bool:
        """Save match result to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO matches (resume_id, job_id, score, match_date)
                VALUES (?, ?, ?, ?)
            ''', (
                match_data['resume_id'],
                match_data['job_id'],
                match_data['score'],
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving match: {e}")
            return False
    
    def get_matches_by_job(self, job_id: str) -> List[Dict]:
        """Get all matches for a job"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, r.filename
            FROM matches m
            JOIN resumes r ON m.resume_id = r.id
            WHERE m.job_id = ?
            ORDER BY m.score DESC
        ''', (job_id,))
        
        rows = cursor.fetchall()
        
        matches = []
        for row in rows:
            matches.append({
                'id': row['id'],
                'resume_id': row['resume_id'],
                'job_id': row['job_id'],
                'score': row['score'],
                'match_date': row['match_date'],
                'filename': row['filename']
            })
        
        conn.close()
        return matches
    
    def save_evaluation_result(self, experiment_name: str, metrics: Dict) -> bool:
        """Save evaluation results to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO evaluation_results (experiment_name, metrics, created_date)
                VALUES (?, ?, ?)
            ''', (
                experiment_name,
                json.dumps(metrics),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving evaluation result: {e}")
            return False
    
    def get_evaluation_results(self) -> List[Dict]:
        """Get all evaluation results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM evaluation_results ORDER BY created_date DESC')
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'experiment_name': row['experiment_name'],
                'metrics': json.loads(row['metrics']) if row['metrics'] else {},
                'created_date': row['created_date']
            })
        
        conn.close()
        return results
