import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify
from flask import render_template
import openai
import PyPDF2
import re
import docx

nlp = spacy.load("en_core_web_md")

nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  


def get_job_skills(job_title):
    """Fetch relevant job skills using OpenAI's GPT API."""
    prompt = f"What are the top 10 skills required for a {job_title} job? List them as a comma-separated list and only give 1 word skills."

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": prompt}]
        )
        skills_text = response.choices[0].message.content
        return preprocess_text_for_skills(skills_text)
    except Exception as e:
        return str(e)

def preprocess_text_for_skills(text):
    
    skills = preprocess_text(text)
    return list(set(skills)) 

def extract_text_from_pdf(file):
    """Extract text from PDF resumes."""
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(file):
    """Extract text from DOCX resumes."""
    doc = docx.Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def preprocess_text(text):
    """Preprocess both job skills and resume text to standardise and clean them for better matching."""
    # Convert to lower case and tokenize
    text = text.lower()
    
    # Remove any unwanted words like "skills", "skills required", etc.
    text = re.sub(r'\bskills?\b', '', text)
    text = re.sub(r'\s+', ' ', text)  # Clean up extra spaces
    
    # Tokenize and remove non-alphanumeric words
    doc = nlp(text)
    words = [token.text for token in doc if token.is_alpha]
    
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    return filtered_words

def extract_skills_from_resume(resume_text, job_skills_list):
    """Find common skills based on semantic similarity."""
    resume_words = preprocess_text(resume_text)
    common_skills = []

    for resume_word in resume_words:
        for job_skill in job_skills_list:
            #Calculate similarity between the resume word and the job skill
            similarity = calculate_similarity(resume_word, job_skill)
            if similarity > 0.7:  # If similarity is above 70%, consider it a match
                if job_skill not in common_skills:
                    common_skills.append(job_skill)
    
    return common_skills

def calculate_similarity(word1, word2):
    """Calculate semantic similarity between two words using spaCy."""
    # If either word is empty, return 0 similarity (no match)
    if not word1 or not word2:
        return 0
    
    doc1 = nlp(word1)
    doc2 = nlp(word2)
    
    # Check if either of the docs is empty (no valid vectors)
    if doc1.vector.any() == False or doc2.vector.any() == False:
        return 0  # Return 0 if there are no valid vectors
    
    return doc1.similarity(doc2)

def calculate_match_percentage(common_skills, total_skills):
    """Calculate match percentage between resume and job skills."""
    match_percentage = (len(common_skills) / len(total_skills)) * 100 if total_skills else 0
    return min(round(match_percentage), 100) 

@app.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume file uploads and analyse skills."""
    resume = request.files['resume']
    job_title = request.form.get('job_title')

    if not job_title:
        return jsonify({"error": "Job title is required!"}), 400
    
    job_skills_list = get_job_skills(job_title)

    if resume.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume)
    elif resume.filename.endswith('.docx'):
        resume_text = extract_text_from_docx(resume)
    else:
        return jsonify({"error": "Invalid file format!"}), 400

    common_skills = extract_skills_from_resume(resume_text, job_skills_list)
    match_percentage = calculate_match_percentage(common_skills, job_skills_list)
    missing_skills = list(set(job_skills_list) - set(common_skills))

    return jsonify({
        "match_percentage": match_percentage,
        "resume_skills": common_skills,
        "missing_skills": missing_skills
    })

if __name__ == "__main__":
    app.run(debug=True)

