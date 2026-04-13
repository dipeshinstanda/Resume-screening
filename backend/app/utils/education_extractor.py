import re

def extract_education(text):
    education_data = []
    
    degree_patterns = [
        r'(Ph\.?D\.?|Doctorate|Doctor of Philosophy)',
        r'(M\.?S\.?|M\.?A\.?|Masters?|MBA|Master of \w+)',
        r'(B\.?S\.?|B\.?A\.?|B\.?Tech\.?|Bachelors?|Bachelor of \w+)',
        r'(Diploma|Associate)',
        r'(High School|Secondary School|12th|10th)'
    ]
    
    degree_mapping = {
        'phd': 'PhD',
        'doctorate': 'PhD',
        'doctor of philosophy': 'PhD',
        'masters': 'Masters',
        'master': 'Masters',
        'mba': 'MBA',
        'bachelors': 'Bachelors',
        'bachelor': 'Bachelors',
        'diploma': 'Diploma',
        'associate': 'Associate',
        'high school': 'High School',
        'secondary': 'High School'
    }
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        for pattern in degree_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                degree = match.group(1)
                
                normalized_degree = degree.lower()
                for key, value in degree_mapping.items():
                    if key in normalized_degree:
                        degree = value
                        break
                
                field = ''
                institution = ''
                year = ''
                
                field_match = re.search(r'in\s+([A-Za-z\s]+)', line, re.IGNORECASE)
                if field_match:
                    field = field_match.group(1).strip()
                
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not any(re.search(p, next_line, re.IGNORECASE) for p in degree_patterns):
                        institution = next_line.strip()
                
                year_match = re.search(r'(19|20)\d{2}', line)
                if year_match:
                    year = year_match.group(0)
                
                education_data.append({
                    'degree': degree,
                    'field': field,
                    'institution': institution,
                    'year': year
                })
    
    return education_data
