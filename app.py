"""
🎯 ATS-Friendly Resume Analyzer - Professional Recruiter Edition
=================================================================
An interactive and innovative resume analysis tool built with Streamlit.
This tool analyzes resumes and provides comprehensive recruiter-style feedback.
"""

import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import re
from io import BytesIO
import docx
import PyPDF2
from textblob import TextBlob
import random
import time
from difflib import SequenceMatcher

# Page Configuration
st.set_page_config(
    page_title="🎯 ATS Resume Analyzer - Professional",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colorful and interactive UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }
    .main-header h1 {
        color: white;
        text-align: center;
        font-size: 2.8em;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    .main-header p {
        color: #f0f0f0;
        text-align: center;
        font-size: 1.3em;
        margin-top: 15px;
    }
    .score-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 35px;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin: 25px 0;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }
    .score-card h2 {
        font-size: 5em;
        margin: 0;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.3);
    }
    .score-card p {
        font-size: 1.6em;
        margin-top: 15px;
    }
    .checklist-item {
        padding: 18px;
        margin: 12px 0;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    .checklist-item:hover {
        transform: translateX(15px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .success-check {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    .warning-check {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
        color: white;
    }
    .error-check {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }
    .section-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 18px;
        border-radius: 12px;
        color: white;
        margin: 25px 0;
        font-size: 1.4em;
        font-weight: bold;
    }
    .section-header-purple {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 18px;
        border-radius: 12px;
        color: white;
        margin: 25px 0;
        font-size: 1.4em;
        font-weight: bold;
    }
    .section-header-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 18px;
        border-radius: 12px;
        color: white;
        margin: 25px 0;
        font-size: 1.4em;
        font-weight: bold;
    }
    .section-header-orange {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
        padding: 18px;
        border-radius: 12px;
        color: white;
        margin: 25px 0;
        font-size: 1.4em;
        font-weight: bold;
    }
    .quote-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        font-style: italic;
        font-size: 1.3em;
        margin: 25px 0;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }
    .tip-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 25px;
        border-radius: 18px;
        margin: 18px 0;
        border-left: 6px solid #667eea;
    }
    .tech-term {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        display: inline-block;
        margin: 6px;
        font-size: 0.95em;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
    }
    .verdict-hire {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        margin: 20px 0;
    }
    .verdict-borderline {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        margin: 20px 0;
    }
    .verdict-reject {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        margin: 20px 0;
    }
    .bullet-before {
        background: #ffebee;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    .bullet-after {
        background: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .stAlert {
        border-radius: 15px;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .recruiter-note {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Motivational Quotes
MOTIVATIONAL_QUOTES = [
    "🌟 Your resume is your personal marketing document. Make it shine!",
    "💪 Every expert was once a beginner. Keep learning, keep growing!",
    "🚀 The job market is competitive, but so are you!",
    "🌈 Your potential is limitless. Let your resume tell that story!",
    "⭐ Success is not final, failure is not fatal. Keep pushing forward!",
    "💡 Your resume is the first impression. Make it count!",
    "🎯 Dream big, work hard, stay focused. Your dream job awaits!",
    "🌺 Every setback is a setup for a comeback. Never give up!",
    "⭐ The only way to do great work is to love what you do!",
    "💪 Your resume is not just a document, it's your career story!"
]

# Tech Skills Database
TECH_SKILLS = {
    'programming_languages': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'scala', 'kotlin', 'typescript', 'php', 'swift', 'r', 'matlab', 'perl', 'bash', 'shell'],
    'frontend': ['html', 'css', 'react', 'vue', 'angular', 'jquery', 'bootstrap', 'tailwind', 'sass', 'less', 'webpack', 'vite', 'nextjs', 'nuxt', 'svelte'],
    'backend': ['node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net', 'fastapi', 'nestjs', 'gin', 'echo', 'play'],
    'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'oracle', 'sqlite', 'mariadb', 'firebase'],
    'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'ci/cd', 'git', 'github', 'gitlab', 'bitbucket', 'circleci', 'travis'],
    'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn', 'data analysis', 'statistics', 'nlp', 'computer vision', 'data visualization', 'tableau', 'power bi'],
    'testing': ['unit testing', 'integration testing', 'selenium', 'pytest', 'jest', 'mocha', 'testing', 'test-driven development', 'tdd', 'BDD', 'cypress'],
    'soft_skills': ['communication', 'teamwork', 'leadership', 'problem-solving', 'time management', 'agile', 'scrum', 'project management', 'collaboration', 'analytical', 'creative']
}

# Job Role Categories
JOB_ROLES = {
    'Software Developer': {
        'required_skills': ['python', 'java', 'javascript', 'git', 'sql', 'problem-solving'],
        'preferred_skills': ['docker', 'aws', 'react', 'agile', 'ci/cd']
    },
    'Data Analyst': {
        'required_skills': ['python', 'sql', 'data analysis', 'statistics', 'tableau'],
        'preferred_skills': ['pandas', 'numpy', 'machine learning', 'power bi', 'excel']
    },
    'Data Scientist': {
        'required_skills': ['python', 'machine learning', 'statistics', 'sql', 'data analysis'],
        'preferred_skills': ['tensorflow', 'pytorch', 'deep learning', 'nlp', 'data visualization']
    },
    'Frontend Developer': {
        'required_skills': ['html', 'css', 'javascript', 'react', 'git'],
        'preferred_skills': ['vue', 'angular', 'typescript', 'webpack', 'testing']
    },
    'Backend Developer': {
        'required_skills': ['python', 'java', 'sql', 'git', 'api'],
        'preferred_skills': ['docker', 'aws', 'microservices', 'ci/cd', 'redis']
    },
    'Full Stack Developer': {
        'required_skills': ['javascript', 'react', 'python', 'sql', 'git'],
        'preferred_skills': ['docker', 'aws', 'node.js', 'mongodb', 'ci/cd']
    },
    'DevOps Engineer': {
        'required_skills': ['docker', 'kubernetes', 'aws', 'ci/cd', 'terraform'],
        'preferred_skills': ['python', 'linux', 'jenkins', 'ansible', 'git']
    },
    'Machine Learning Engineer': {
        'required_skills': ['python', 'machine learning', 'tensorflow', 'sql', 'deep learning'],
        'preferred_skills': ['pytorch', 'docker', 'aws', 'mlops', 'kubernetes']
    }
}

# Comprehensive Action Verbs Organized by Category
ACTION_VERBS = {
    # Leadership & Management
    'leadership': ['led', 'managed', 'directed', 'coordinated', 'supervised', 'mentored', 'coached', 'spearheaded', 'championed', 'overseen'],
    
    # Technical & Development
    'technical': ['developed', 'created', 'designed', 'implemented', 'built', 'engineered', 'architected', 'coded', 'programmed', 'constructed', 'fabricated', 'assembled'],
    
    # Optimization & Improvement
    'optimization': ['optimized', 'improved', 'enhanced', 'streamlined', 'refined', 'upgraded', 'transformed', 'modernized', 'revamped', 'restructured'],
    
    # Achievement & Results
    'achievement': ['achieved', 'delivered', 'exceeded', 'accomplished', 'completed', 'finished', 'concluded', 'finalized', 'executed', 'produced'],
    
    # Analysis & Research
    'analysis': ['analyzed', 'investigated', 'evaluated', 'assessed', 'examined', 'reviewed', 'studied', 'researched', 'audited', 'diagnosed', 'identified'],
    
    # Problem Solving
    'problem_solving': ['solved', 'resolved', 'fixed', 'repaired', 'troubleshot', 'debugged', 'corrected', 'rectified', 'remedied', 'mitigated'],
    
    # Communication
    'communication': ['communicated', 'presented', 'communicated', 'collaborated', 'negotiated', 'facilitated', 'mediated', 'presented', 'demonstrated', 'explained'],
    
    # Innovation & Creation
    'innovation': ['innovated', 'pioneered', 'initiated', 'introduced', 'established', 'launched', 'instigated', 'originated', 'conceived', 'devised'],
    
    # Efficiency & Reduction
    'efficiency': ['increased', 'decreased', 'reduced', 'lowered', 'minimized', 'maximized', 'eliminated', 'cut', 'slashed', 'condensed'],
    
    # Automation & Integration
    'automation': ['automated', 'integrated', 'deployed', 'configured', 'installed', 'implemented', 'customized', 'modified', 'adapted', 'converted'],
    
    # Strategic & Planning
    'strategic': ['planned', 'organized', 'strategized', 'prioritized', 'scheduled', 'forecasted', 'projected', 'budgeted', 'allocated', 'assigned'],
    
    # Training & Development
    'training': ['trained', 'taught', 'educated', 'instructed', 'developed', 'certified', 'qualified', 'prepared', ' onboarded', 'guided']
}

# Flattened list for checking
ACTION_VERBS_ALL = [verb for verbs in ACTION_VERBS.values() for verb in verbs]

# Project Keywords
PROJECT_KEYWORDS = ['project', 'developed', 'built', 'created', 'designed', 'implemented', 'launched', 'deployed', 'worked on']

# Problem Solving Keywords
PROBLEM_SOLVING_KEYWORDS = ['solved', 'optimized', 'improved', 'enhanced', 'reduced', 'increased', 'achieved', 'troubleshot', 'debugged', 'analyzed', 'identified', 'resolved']

# Learning Keywords
LEARNING_KEYWORDS = ['learned', 'studied', 'certified', 'course', 'workshop', 'training', 'self-taught', 'bootcamp', 'mooc', 'udemy', 'coursera', 'internship']


def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file (PDF or DOCX)"""
    try:
        if uploaded_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif uploaded_file.name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        else:
            return str(uploaded_file.read(), 'utf-8')
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None


def calculate_keyword_match(text, required_skills, preferred_skills):
    """Calculate keyword matching with job description"""
    text_lower = text.lower()
    
    matched_required = []
    missing_required = []
    matched_preferred = []
    missing_preferred = []
    
    for skill in required_skills:
        if skill.lower() in text_lower:
            matched_required.append(skill)
        else:
            missing_required.append(skill)
    
    for skill in preferred_skills:
        if skill.lower() in text_lower:
            matched_preferred.append(skill)
        else:
            missing_preferred.append(skill)
    
    return {
        'matched_required': matched_required,
        'missing_required': missing_required,
        'matched_preferred': matched_preferred,
        'missing_preferred': missing_preferred
    }


def analyze_tech_skills(text):
    """Analyze and extract technical skills from text"""
    text_lower = text.lower()
    found_skills = []
    skill_categories = {}
    
    for category, skills in TECH_SKILLS.items():
        found_in_category = []
        for skill in skills:
            if skill.lower() in text_lower:
                found_in_category.append(skill)
                found_skills.append(skill)
        if found_in_category:
            skill_categories[category] = found_in_category
    
    return list(set(found_skills)), skill_categories


def analyze_projects(text):
    """Analyze project descriptions"""
    text_lower = text.lower()
    lines = text.split('\n')
    project_indicators = []
    action_verb_usage = []
    quantified_results = []
    
    # Check for project descriptions
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in PROJECT_KEYWORDS):
            project_indicators.append(line.strip())
        
        # Check for action verbs
        for verb in ACTION_VERBS_ALL:
            if verb in line_lower:
                action_verb_usage.append((verb, line.strip()))
                break
        
        # Check for quantified results (numbers, percentages)
        numbers = re.findall(r'\d+%|\$\d+|\d+\s*(?:x|times|users|clients)', line_lower)
        if numbers:
            quantified_results.append((line.strip(), numbers))
    
    return project_indicators, action_verb_usage, quantified_results


def analyze_formatting(text):
    """Analyze resume formatting quality"""
    score = 0
    feedback = []
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    # Check for section headers
    section_headers = ['experience', 'education', 'skills', 'projects', 'summary', 'objective', 'certifications', 'work experience', 'professional experience', 'technical skills']
    header_count = sum(1 for header in section_headers if header in text.lower())
    
    if header_count >= 4:
        score += 20
        feedback.append("✅ Excellent section organization")
    elif header_count >= 2:
        score += 12
        feedback.append("⚠️ Basic section organization")
    else:
        score += 5
        feedback.append("❌ Missing clear section headers")
    
    # Check for bullet points
    bullet_patterns = ['•', '-', '*', '·', '○', '▪', '›', '→']
    bullet_count = sum(1 for line in non_empty_lines[:30] if any(bullet in line for bullet in bullet_patterns))
    
    if bullet_count >= 10:
        score += 15
        feedback.append("✅ Good use of bullet points")
    elif bullet_count >= 5:
        score += 10
        feedback.append("⚠️ Some bullet points used")
    else:
        score += 3
        feedback.append("❌ Consider using bullet points")
    
    # Check for consistent formatting
    line_lengths = [len(line) for line in non_empty_lines[:30] if len(line) < 100]
    avg_length = np.mean(line_lengths) if line_lengths else 0
    
    if 30 <= avg_length <= 80:
        score += 15
        feedback.append("✅ Good line length consistency")
    else:
        score += 7
        feedback.append("⚠️ Varying line lengths")
    
    # Check for contact information
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    linkedin_pattern = r'linkedin\.com/in/'
    
    has_email = bool(re.search(email_pattern, text))
    has_phone = bool(re.search(phone_pattern, text))
    has_linkedin = bool(re.search(linkedin_pattern, text.lower()))
    
    contact_score = 0
    if has_email:
        contact_score += 7
    if has_phone:
        contact_score += 7
    if has_linkedin:
        contact_score += 6
    score += contact_score
    
    # Check for graphics/tables (basic detection)
    if '|' in text or '  ' * 5 in text:
        score -= 10
        feedback.append("⚠️ Potential table/column structure detected (ATS risk)")
    
    return score, feedback


def analyze_experience_level(text, found_skills):
    """Estimate experience level based on skills and content"""
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Experience indicators
    junior_keywords = ['intern', 'trainee', 'junior', 'entry', 'fresher', 'graduate', 'student']
    senior_keywords = ['senior', 'lead', 'architect', 'manager', 'director', 'principal', 'staff']
    
    junior_count = sum(1 for keyword in junior_keywords if keyword in text_lower)
    senior_count = sum(1 for keyword in senior_keywords if keyword in text_lower)
    
    # Skill depth analysis
    skill_depth = len(found_skills)
    
    if junior_count > senior_count:
        level = "Fresher/Entry Level"
    elif senior_count > junior_count:
        level = "Senior/Experienced Level"
    else:
        if skill_depth >= 10 and word_count >= 500:
            level = "Mid to Senior Level"
        elif skill_depth >= 5 and word_count >= 300:
            level = "Junior to Mid Level"
        else:
            level = "Fresher/Entry Level"
    
    return level


def generate_improvements(checks, keyword_match, project_analysis, improvements_list):
    """Generate prioritized improvement suggestions"""
    suggestions = []
    
    # High priority
    if keyword_match['missing_required']:
        suggestions.append({
            'priority': 'high',
            'title': '🎯 Add Missing Required Skills',
            'description': f"Critical skills missing from your resume: {', '.join(keyword_match['missing_required'][:5])}. Add these to your skills section or highlight in experience.",
            'section': 'Skills'
        })
    
    if not project_analysis[0] or len(project_analysis[0]) < 2:
        suggestions.append({
            'priority': 'high',
            'title': '📁 Strengthen Project Section',
            'description': 'Add at least 2-3 detailed project descriptions with measurable outcomes. Use the STAR method.',
            'section': 'Projects'
        })
    
    if checks['contact']['score'] < 14:
        suggestions.append({
            'priority': 'high',
            'title': '📞 Complete Contact Information',
            'description': 'Ensure your email, phone, and LinkedIn URL are present and professional.',
            'section': 'Contact'
        })
    
    # Medium priority
    if keyword_match['missing_preferred']:
        suggestions.append({
            'priority': 'medium',
            'title': '⭐ Add Preferred Skills',
            'description': f"Consider adding these nice-to-have skills: {', '.join(keyword_match['missing_preferred'][:5])}",
            'section': 'Skills'
        })
    
    if not project_analysis[2]:
        suggestions.append({
            'priority': 'medium',
            'title': '📈 Quantify Your Achievements',
            'description': 'Add specific metrics, percentages, or numbers to demonstrate impact (e.g., "Improved performance by 40%").',
            'section': 'Experience'
        })
    
    if not project_analysis[1]:
        suggestions.append({
            'priority': 'medium',
            'title': '💪 Use Action Verbs',
            'description': 'Start bullet points with strong action verbs like "Developed," "Optimized," "Led," "Achieved."',
            'section': 'Experience'
        })
    
    # Format suggestions
    if len(suggestions) > 5:
        suggestions = suggestions[:5]
    
    return suggestions


def generate_bullet_improvements(text):
    """Generate specific bullet point improvements"""
    improvements = []
    lines = text.split('\n')
    
    weak_bullets = []
    strong_bullets = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for weak patterns
        weak_patterns = [
            r'(responsible for|duties include|task was|job involved)',
            r'(helped|assisted|participated in)',
            r'(some|various|different)',
            r'^[^•\-\*]*[a-z]',  # Not starting with action or bullet
        ]
        
        is_weak = any(re.search(pattern, line.lower()) for pattern in weak_patterns)
        
        # Check for strong patterns
        strong_patterns = [
            r'(developed|created|designed|implemented|led|managed)',
            r'\d+%|\$\d+|\d+\s*(?:users|clients|hours|days)',
            r'(improved|optimized|increased|decreased|reduced)',
        ]
        
        is_strong = any(re.search(pattern, line.lower()) for pattern in strong_patterns)
        
        if is_weak and not is_strong:
            weak_bullets.append(line)
        elif is_strong:
            strong_bullets.append(line)
    
    # Generate improvements
    for weak in weak_bullets[:3]:
        improved = weak
        
        # Add action verb if missing
        if not any(verb in weak.lower() for verb in ACTION_VERBS_ALL):
            improved = f"Developed and {improved.lower()}"
        
        # Add metric placeholder if missing
        if not re.search(r'\d+%|\$\d+|\d+', weak):
            improved = improved + " resulting in measurable impact"
        
        improvements.append({
            'before': weak,
            'after': improved
        })
    
    return improvements[:3]


def calculate_ats_score(text, keyword_match, formatting_score):
    """Calculate overall ATS score"""
    score = 0
    max_score = 100
    
    # Keyword matching (30 points)
    required_match_rate = len(keyword_match['matched_required']) / max(len(keyword_match['matched_required']) + len(keyword_match['missing_required']), 1)
    preferred_match_rate = len(keyword_match['matched_preferred']) / max(len(keyword_match['matched_preferred']) + len(keyword_match['missing_preferred']), 1)
    
    keyword_score = (required_match_rate * 20) + (preferred_match_rate * 10)
    score += keyword_score
    
    # Formatting (20 points)
    score += min(formatting_score, 20)
    
    # Skills coverage (20 points)
    found_skills, _ = analyze_tech_skills(text)
    skill_score = min(len(found_skills) * 2, 20)
    score += skill_score
    
    # Experience/Projects (20 points)
    project_indicators, action_usage, quantified = analyze_projects(text)
    exp_score = min(len(project_indicators) * 5 + len(quantified) * 3 + len(action_usage) * 2, 20)
    score += exp_score
    
    # Contact & Completeness (10 points)
    word_count = len(text.split())
    if 300 <= word_count <= 1000:
        score += 10
    elif 200 <= word_count < 300 or 1000 < word_count <= 1500:
        score += 7
    else:
        score += 3
    
    return min(int(score), 100)


def calculate_shortlist_probability(ats_score, skill_match, project_quality):
    """Calculate shortlisting probability"""
    base_score = ats_score
    
    # Adjust for skill match
    if skill_match >= 80:
        base_score += 10
    elif skill_match >= 60:
        base_score += 5
    elif skill_match < 40:
        base_score -= 10
    
    # Adjust for project quality
    if project_quality >= 80:
        base_score += 10
    elif project_quality >= 60:
        base_score += 5
    elif project_quality < 40:
        base_score -= 10
    
    return min(max(base_score, 5), 95)


def main():
    """Main application function"""
    
    # Display header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 ATS Resume Analyzer</h1>
        <p>Expert Recruiter Analysis for Your Resume | Get Hired Faster!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. Select your target job role
        2. Optionally paste job description
        3. Upload your resume (PDF/DOCX)
        4. Wait for recruiter analysis
        5. Implement improvements
        6. Re-upload to check progress!
        """)
        
        st.header("💼 Select Job Role")
        job_role = st.selectbox(
            "Target Position",
            list(JOB_ROLES.keys()) + ["Custom"]
        )
        
        if job_role == "Custom":
            custom_skills = st.text_area("Enter required skills (comma-separated)", "python, sql, git, communication")
            st.session_state['custom_role'] = {
                'required_skills': [s.strip() for s in custom_skills.split(',')],
                'preferred_skills': []
            }
        
        st.header("📝 Job Description (Optional)")
        job_description = st.text_area("Paste job description for better analysis", height=150)
        
        st.header("💪 Action Verbs by Category")
        
        # Create expander for each category
        with st.expander("🎯 Leadership & Management", expanded=False):
            st.write(", ".join(ACTION_VERBS['leadership']))
        
        with st.expander("💻 Technical & Development", expanded=False):
            st.write(", ".join(ACTION_VERBS['technical']))
        
        with st.expander("⚡ Optimization & Improvement", expanded=False):
            st.write(", ".join(ACTION_VERBS['optimization']))
        
        with st.expander("🏆 Achievement & Results", expanded=False):
            st.write(", ".join(ACTION_VERBS['achievement']))
        
        with st.expander("🔍 Analysis & Research", expanded=False):
            st.write(", ".join(ACTION_VERBS['analysis']))
        
        with st.expander("🧠 Problem Solving", expanded=False):
            st.write(", ".join(ACTION_VERBS['problem_solving']))
        
        with st.expander("📢 Communication", expanded=False):
            st.write(", ".join(ACTION_VERBS['communication']))
        
        with st.expander("🚀 Innovation & Creation", expanded=False):
            st.write(", ".join(ACTION_VERBS['innovation']))
        
        st.header("💡 Quick Tips")
        st.markdown("""
        - Keep it concise (1-2 pages)
        - Use action verbs
        - Quantify achievements
        - Tailor to each job
        - Proofread carefully
        - ATS-friendly formatting
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header-purple">📤 Upload Your Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drag and drop your resume here", type=['pdf', 'docx'])
    
    # Get job role skills
    if job_role != "Custom" and job_role in JOB_ROLES:
        role_skills = JOB_ROLES[job_role]
        required_skills = role_skills['required_skills']
        preferred_skills = role_skills['preferred_skills']
    elif 'custom_role' in st.session_state:
        required_skills = st.session_state['custom_role']['required_skills']
        preferred_skills = st.session_state['custom_role']['preferred_skills']
    else:
        required_skills = ['python', 'java', 'sql', 'git', 'communication']
        preferred_skills = ['docker', 'aws', 'agile']
    
    if uploaded_file is not None:
        with st.spinner('🔍 Conducting recruiter-style analysis...'):
            # Extract text
            text = extract_text_from_file(uploaded_file)
            
            if text:
                time.sleep(1.5)  # For dramatic effect
                
                # Perform all analyses
                keyword_match = calculate_keyword_match(text, required_skills, preferred_skills)
                found_skills, skill_categories = analyze_tech_skills(text)
                project_indicators, action_usage, quantified = analyze_projects(text)
                formatting_score, formatting_feedback = analyze_formatting(text)
                ats_score = calculate_ats_score(text, keyword_match, formatting_score)
                
                # Calculate skill match percentage
                total_required = len(required_skills) + len(preferred_skills)
                matched = len(keyword_match['matched_required']) + len(keyword_match['matched_preferred'])
                skill_match_pct = (matched / total_required * 100) if total_required > 0 else 50
                
                # Project quality score
                project_quality = min(len(project_indicators) * 20 + len(quantified) * 15 + len(action_usage) * 10, 100)
                
                # Shortlist probability
                shortlist_prob = calculate_shortlist_probability(ats_score, skill_match_pct, project_quality)
                
                # Experience level
                experience_level = analyze_experience_level(text, found_skills)
                
                # Generate improvements
                improvements_list = []
                suggestions = generate_improvements(
                    {'contact': {'score': formatting_score // 3}},
                    keyword_match,
                    (project_indicators, action_usage, quantified),
                    improvements_list
                )
                
                # Generate bullet improvements
                bullet_improvements = generate_bullet_improvements(text)
                
                # Determine verdict
                if shortlist_prob >= 70:
                    verdict = "HIRE"
                    verdict_class = "verdict-hire"
                    verdict_icon = "✅"
                elif shortlist_prob >= 50:
                    verdict = "BORDERLINE"
                    verdict_class = "verdict-borderline"
                    verdict_icon = "⚠️"
                else:
                    verdict = "REJECT"
                    verdict_class = "verdict-reject"
                    verdict_icon = "❌"
                
                # Display results
                st.markdown("---")
                st.markdown('<div class="section-header-green">📊 ATS Score & Recruiter Verdict</div>', unsafe_allow_html=True)
                
                # Score and Verdict
                col_score, col_verdict = st.columns([1, 1.5])
                
                with col_score:
                    if ats_score >= 80:
                        score_color = '#38ef7d'
                        score_msg = '🌟 Excellent!'
                    elif ats_score >= 60:
                        score_color = '#f2c94c'
                        score_msg = '👍 Good!'
                    elif ats_score >= 40:
                        score_color = '#f2994a'
                        score_msg = '📝 Needs Work'
                    else:
                        score_color = '#f45c43'
                        score_msg = '🚨 Critical Issues'
                    
                    st.markdown(f"""
                    <div class="score-card" style="background: linear-gradient(135deg, {score_color} 0%, #11998e 100%);">
                        <h2>{ats_score}</h2>
                        <p>{score_msg}</p>
                        <p style="font-size: 0.9em;">/ 100</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="{verdict_class}" style="font-size: 1.8em;">
                        {verdict_icon} {verdict}
                    </div>
                    <p style="text-align: center; margin-top: 10px; font-weight: bold;">
                        Shortlist Probability: {shortlist_prob}%
                    </p>
                    """, unsafe_allow_html=True)
                
                with col_verdict:
                    # Experience Level
                    st.markdown(f"""
                    <div class="tip-card">
                        <h4>📈 Experience Level Assessment</h4>
                        <p style="font-size: 1.2em; font-weight: bold;">{experience_level}</p>
                        <p>Based on your skills and experience descriptions.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Motivational quote
                    st.markdown(f"""
                    <div class="quote-box">
                        {random.choice(MOTIVATIONAL_QUOTES)}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Skill Match Summary
                st.markdown('<div class="section-header">🎯 Skill Match Analysis</div>', unsafe_allow_html=True)
                
                col_skills1, col_skills2 = st.columns(2)
                
                with col_skills1:
                    st.markdown("### ✅ Matched Skills")
                    if keyword_match['matched_required'] or keyword_match['matched_preferred']:
                        all_matched = keyword_match['matched_required'] + keyword_match['matched_preferred']
                        for skill in all_matched:
                            st.markdown(f'<span class="tech-term" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.info("No matching skills found")
                
                with col_skills2:
                    st.markdown("### ❌ Missing Skills")
                    all_missing = keyword_match['missing_required'] + keyword_match['missing_preferred']
                    if all_missing:
                        priority_missing = keyword_match['missing_required'][:5]
                        for skill in priority_missing:
                            st.markdown(f'<span class="tech-term" style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.success("All required skills matched!")
                
                # Skill Match Progress Bar
                st.markdown("### 📊 Skill Match Score")
                st.progress(min(skill_match_pct / 100, 1.0))
                st.caption(f"Skill Match: {int(skill_match_pct)}% ({len(keyword_match['matched_required'])}/{len(required_skills)} required, {len(keyword_match['matched_preferred'])}/{len(preferred_skills)} preferred)")
                
                # Project & Experience Analysis
                st.markdown('<div class="section-header-orange">📁 Project & Experience Analysis</div>', unsafe_allow_html=True)
                
                col_proj1, col_proj2 = st.columns(2)
                
                with col_proj1:
                    st.markdown("#### ✅ Strong Points")
                    strong_points = []
                    if project_indicators:
                        strong_points.append(f"• {len(project_indicators)} project descriptions found")
                    if action_usage:
                        strong_points.append(f"• {len(set([v[0] for v in action_usage]))} action verbs used")
                    if quantified:
                        strong_points.append(f"• {len(quantified)} quantified achievements")
                    if len(found_skills) >= 5:
                        strong_points.append(f"• {len(found_skills)} technical skills listed")
                    
                    if strong_points:
                        for point in strong_points:
                            st.markdown(f"<div class='recruiter-note'>{point}</div>", unsafe_allow_html=True)
                    else:
                        st.warning("No strong points detected")
                
                with col_proj2:
                    st.markdown("#### ⚠️ Areas for Improvement")
                    weak_points = []
                    if not project_indicators or len(project_indicators) < 2:
                        weak_points.append("• Add more project descriptions")
                    if not quantified:
                        weak_points.append("• Include quantified results/metrics")
                    if len(action_usage) < 3:
                        weak_points.append("• Use more action verbs")
                    if len(found_skills) < 5:
                        weak_points.append("• Expand technical skills section")
                    
                    if weak_points:
                        for point in weak_points:
                            st.markdown(f"<div class='tip-card'>{point}</div>", unsafe_allow_html=True)
                    else:
                        st.success("Excellent project descriptions!")
                
                # Project Quality Score
                st.markdown("### 📈 Project Quality Score")
                st.progress(min(project_quality / 100, 1.0))
                st.caption(f"Project Quality: {int(project_quality)}%")
                
                # Resume Quality Review
                st.markdown('<div class="section-header-purple">📝 Resume Quality Review</div>', unsafe_allow_html=True)
                
                col_qual1, col_qual2 = st.columns(2)
                
                with col_qual1:
                    st.markdown("#### 🏆 Formatting & Structure")
                    for feedback in formatting_feedback:
                        if '✅' in feedback:
                            st.success(feedback)
                        elif '❌' in feedback:
                            st.error(feedback)
                        else:
                            st.warning(feedback)
                
                with col_qual2:
                    st.markdown("#### 📋 ATS Safety Check")
                    word_count = len(text.split())
                    if 300 <= word_count <= 1000:
                        st.success(f"✅ Optimal length ({word_count} words)")
                    else:
                        st.warning(f"⚠️ Word count: {word_count} (aim for 300-1000)")
                    
                    # Check for common issues
                    if '|' not in text and '  ' * 5 not in text:
                        st.success("✅ No tables/columns detected (ATS safe)")
                    else:
                        st.error("❌ Potential table formatting (ATS risk)")
                
                # Detailed Checklist
                st.markdown("#### 📊 Detailed Checklist")
                
                checklist_items = [
                    ("Contact Information", "Complete" if len(keyword_match['matched_required']) > 0 else "Missing", len(keyword_match['matched_required']) > 0),
                    ("Skills Section", f"{len(found_skills)} skills found", len(found_skills) >= 3),
                    ("Project Descriptions", f"{len(project_indicators)} projects", len(project_indicators) >= 2),
                    ("Action Verbs", f"{len(action_usage)} used", len(action_usage) >= 3),
                    ("Quantified Results", f"{len(quantified)} metrics", len(quantified) >= 1),
                    ("ATS Formatting", "Clean" if '|' not in text else "Complex", '|' not in text),
                ]
                
                for item_name, item_status, item_passed in checklist_items:
                    icon = '✅' if item_passed else '❌'
                    status_class = 'success-check' if item_passed else 'error-check'
                    st.markdown(f"""
                    <div class="checklist-item {status_class}">
                        <span style="font-size: 1.4em; margin-right: 10px;">{icon}</span>
                        <strong>{item_name}:</strong> {item_status}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Top 5 Improvements
                st.markdown('<div class="section-header">🏆 Top 5 Improvements to Get Shortlisted Faster</div>', unsafe_allow_html=True)
                
                for i, improvement in enumerate(suggestions[:5], 1):
                    priority_icon = '🔴' if improvement['priority'] == 'high' else ('🟡' if improvement['priority'] == 'medium' else '🟢')
                    st.markdown(f"""
                    <div class="tip-card">
                        <h4>{priority_icon} {i}. {improvement['title']}</h4>
                        <p>{improvement['description']}</p>
                        <small><strong>Section:</strong> {improvement['section']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Bullet Point Improvements
                if bullet_improvements:
                    st.markdown('<div class="section-header-orange">💡 Optimized Resume Bullet Examples</div>', unsafe_allow_html=True)
                    
                    for i, improvement in enumerate(bullet_improvements, 1):
                        st.markdown(f"""
                        <div style="margin: 15px 0;">
                            <div class="bullet-before">
                                <strong>❌ Before:</strong><br>{improvement['before']}
                            </div>
                            <div class="bullet-after">
                                <strong>✅ After:</strong><br>{improvement['after']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Technical Skills Found
                if found_skills:
                    st.markdown('<div class="section-header">🛠️ Technical Skills Detected</div>', unsafe_allow_html=True)
                    
                    # Group by category
                    for category, skills in skill_categories.items():
                        category_name = category.replace('_', ' ').title()
                        st.markdown(f"**{category_name}:**")
                        skills_html = '<div style="margin-bottom: 15px;">'
                        for skill in skills:
                            skills_html += f'<span class="tech-term">{skill}</span>'
                        skills_html += '</div>'
                        st.markdown(skills_html, unsafe_allow_html=True)
                
                # Recruiter's Final Verdict
                st.markdown('<div class="section-header-green">🎯 Overall Recruiter Verdict</div>', unsafe_allow_html=True)
                
                # Generate verdict reasoning
                reasons = []
                if ats_score >= 70:
                    reasons.append("✅ Strong ATS score indicating good keyword optimization")
                else:
                    reasons.append("⚠️ ATS score below optimal - needs keyword improvements")
                
                if skill_match_pct >= 70:
                    reasons.append("✅ Good skill alignment with job requirements")
                else:
                    reasons.append("⚠️ Skill gaps identified that need addressing")
                
                if project_quality >= 60:
                    reasons.append("✅ Solid project experience demonstrated")
                else:
                    reasons.append("⚠️ Project descriptions need more detail and metrics")
                
                for reason in reasons:
                    st.markdown(f"<div class='recruiter-note'>{reason}</div>", unsafe_allow_html=True)
                
                # Final recommendation
                st.markdown(f"""
                <div class="{verdict_class}" style="margin-top: 20px;">
                    <h2>{verdict_icon} {verdict}</h2>
                    <p>Shortlisting Probability: {shortlist_prob}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                if verdict == "HIRE":
                    st.success("🎉 Congratulations! Your resume is well-positioned for this role. Consider tailoring it slightly for each application.")
                elif verdict == "BORDERLINE":
                    st.warning("📝 Your resume has potential but needs improvements. Focus on the suggestions above to increase your chances.")
                else:
                    st.error("📚 Your resume needs significant improvements. Don't be discouraged - follow the actionable suggestions above to transform your resume!")
                
                # Encouragement
                st.markdown(f"""
                <div class="quote-box">
                    {random.choice(MOTIVATIONAL_QUOTES)}
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2 style="color: #667eea;">👋 Welcome to Professional ATS Resume Analyzer!</h2>
            <p style="font-size: 1.2em; color: #666;">
                Get expert recruiter feedback on your resume with detailed analysis.
            </p>
            <div style="margin-top: 30px;">
                <h3 style="color: #f093fb;">What We Analyze:</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px;">
                    <div class="metric-card">
                        <h4>📊 ATS Score</h4>
                        <p>Keyword optimization & compatibility</p>
                    </div>
                    <div class="metric-card">
                        <h4>🎯 Skill Match</h4>
                        <p>Required vs preferred skills</p>
                    </div>
                    <div class="metric-card">
                        <h4>📁 Projects</h4>
                        <p>Quality & quantified impact</p>
                    </div>
                    <div class="metric-card">
                        <h4>📈 Shortlist Probability</h4>
                        <p>Recruiter perspective</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Motivational quote
        st.markdown(f"""
        <div class="quote-box">
            {random.choice(MOTIVATIONAL_QUOTES)}
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Professional ATS Resume Analyzer </p>
        <p>💼 Your success is our priority! Get hired faster!</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
