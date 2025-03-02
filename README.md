# Resume Analyzer

## Description

The **Resume Analyzer** is a web application that allows users to upload their resumes and get an analysis of their skills compared to a given job title. This project leverages AI-powered APIs to fetch the top skills required for the job and matches those with the skills extracted from the resume. The app processes resumes in PDF and DOCX formats and provides a match percentage along with common and missing skills.

## Features

- **Resume Upload**: Users can upload their resumes in PDF or DOCX formats.
- **Job Skills Analysis**: The app uses OpenAI's GPT API to fetch relevant job skills based on the user's input for the job title.
- **Skill Matching**: The app analyzes the resume's skills and compares them with the required skills for the job, providing a match percentage.
- **Detailed Results**: Users are presented with the common skills found between the resume and the job description, as well as any missing skills.

## Technologies Used

- **Flask**: Python web framework used to build the app and handle the backend.
- **OpenAI GPT-4**: Used to fetch job skills based on job title via the OpenAI API.
- **spaCy**: NLP library used for tokenizing and processing the resume's text to extract meaningful skills.
- **PyPDF2**: Python library for extracting text from PDF files.
- **python-docx**: Used for extracting text from DOCX files.
- **NLTK**: Natural Language Toolkit for tokenization and removing stopwords from text.
- **HTML/CSS**: Frontend technologies used to create the user interface.

## How It Works

1. **User Uploads Resume**: The user uploads their resume file (PDF or DOCX) and enters the job title they are applying for.
2. **Skill Extraction**: The app uses OpenAI's GPT-4 model to fetch the top skills required for the job.
3. **Resume Parsing**: The resume text is extracted using either PyPDF2 (for PDFs) or python-docx (for DOCX files).
4. **Text Preprocessing**: Both the job skills and the resume text are preprocessed by converting to lowercase, tokenizing, and removing unnecessary words (like "skills" or "required").
5. **Skill Matching**: The app compares the extracted resume skills with the required job skills by calculating semantic similarity using spaCy.
6. **Result**: The user is shown the match percentage and a list of common and missing skills.

## API Used

### OpenAI GPT-4

The **OpenAI GPT-4** model is used to fetch job skills based on the job title entered by the user. The API takes a prompt in the form of the job title and returns the top 10 skills associated with the role. This is a key feature that enhances the accuracy and relevance of the skill comparison between the resume and job description.

## How to Run the Application

1. **Clone the Repository**:  
   First, clone the repository to your local machine by running the following command:
   - git clone https://github.com/Jaishan27/Resume-Analyzer.git
   - cd Resume-Analyzer

2. **Install Dependencies**:  
   Make sure you have Python installed. Then, install the required dependencies by running:
   pip install -r requirements.txt

3. **Run the Application**:  
   After installing the dependencies, run the app locally by executing:
   python app.py

   The app will be accessible in your browser at http://127.0.0.1:5000/.

4. **Access the Application**:  
   - Open the app in your browser.
   - Upload your resume (PDF or DOCX) and enter a job title.
   - View the match percentage and the list of common and missing skills.

## Future Improvements

Enhanced Skill Matching: The current skill matching algorithm is based on semantic similarity. In the future, machine learning models could be used to analyze the proficiency level of each skill.

Additional File Formats: Support for other resume formats such as .txt or .rtf could be added to enhance the versatility of the application.

UI Enhancements: The user interface can be improved with features like animations, better styling, or a more responsive layout to enhance user experience.

Job Description Input: The app could allow users to input a detailed job description directly for a more accurate skill match, instead of relying solely on the GPT API to fetch job skills.

Authentication & User Profiles: Future versions could include user authentication, allowing users to save and track their resumes and skill matches over time.

Cloud Deployment: The app could be deployed on platforms like Heroku, AWS, or Google Cloud to allow users to access it online without needing to run it locally.

