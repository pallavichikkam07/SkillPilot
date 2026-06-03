from flask import Flask, render_template, request, redirect, session

import PyPDF2
import json
import random
import sqlite3

app = Flask(__name__)

# =========================
# SECRET KEY
# =========================

app.secret_key = "skillpilot_secret"

# =========================
# DATABASE CONNECTION
# =========================

conn = sqlite3.connect(
    'database.db',
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# CREATE USERS TABLE
# =========================

cursor.execute(

    '''

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        email TEXT,

        password TEXT

    )

    '''

)

conn.commit()

# =========================
# CREATE PROGRESS TABLE
# =========================

cursor.execute(

    '''

    CREATE TABLE IF NOT EXISTS progress (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        role TEXT,

        score INTEGER,

        matched_skills INTEGER,

        missing_skills INTEGER

    )

    '''

)

conn.commit()

# =========================
# LOAD JSON FILES
# =========================

with open('data/skills.json', 'r') as file:

    skills_data = json.load(file)

with open('data/interview_questions.json', 'r') as file:

    interview_data = json.load(file)

with open('data/assessment_questions.json', 'r') as file:

    assessment_data = json.load(file)

with open('data/learning_resources.json', 'r') as file:

    resources_data = json.load(file)

with open('data/professional_tips.json', 'r') as file:

    professional_tips = json.load(file)

with open('data/weak_area_training.json', 'r') as file:

    weak_area_training = json.load(file)

# =========================
# GLOBAL VARIABLES
# =========================

selected_role = ""

selected_missing_skills = []

# =========================
# HOME PAGE
# =========================

@app.route('/')

def home():

    if 'user' in session:

        return render_template('indexi.html')

    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])

def signup():

    if request.method == 'POST':

        username = request.form['username']

        email = request.form['email']

        password = request.form['password']

        cursor.execute(

            '''

            INSERT INTO users (

                username,
                email,
                password

            )

            VALUES (?, ?, ?)

            ''',

            (

                username,
                email,
                password

            )

        )

        conn.commit()

        return redirect('/login')

    return render_template('signup.html')
# =========================
# LOGIN ROUTE
# =========================

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        cursor.execute(

            '''

            SELECT * FROM users

            WHERE email = ?

            AND password = ?

            ''',

            (

                email,
                password

            )

        )

        user = cursor.fetchone()

        if user:

            session['user'] = user[1]

            return redirect('/')

        else:

            return render_template(

                'login.html',

                error="Invalid Email or Password"

            )

    return render_template('login.html')

# =========================
# LOGOUT ROUTE
# =========================

@app.route('/logout')

def logout():

    session.pop(

        'user',

        None

    )

    return redirect('/login')

# =========================
# ANALYZE ROUTE
# =========================

@app.route('/analyze', methods=['POST'])

def analyze():

    global selected_role

    global selected_missing_skills

    # =========================
    # CHECK LOGIN
    # =========================

    if 'user' not in session:

        return redirect('/login')

    # =========================
    # GET ROLE
    # =========================

    role = request.form['role']

    selected_role = role

    # =========================
    # GET RESUME
    # =========================

    resume = request.files['resume']

    # =========================
    # READ PDF
    # =========================

    pdf_reader = PyPDF2.PdfReader(resume)

    resume_text = ""

    for page in pdf_reader.pages:

        text = page.extract_text()

        if text:

            resume_text += text.lower()

    # =========================
    # REQUIRED SKILLS
    # =========================

    required_skills = skills_data.get(role, [])

    matched_skills = []

    missing_skills = []

    # =========================
    # SMART SKILL MATCHING
    # =========================

    related_keywords = {

        "html": [
            "webpage",
            "semantic",
            "forms",
            "structure"
        ],

        "css": [
            "responsive",
            "styling",
            "ui",
            "flexbox",
            "grid"
        ],

        "javascript": [
            "js",
            "dom",
            "es6",
            "frontend"
        ],

        "react": [
            "frontend",
            "components",
            "jsx",
            "spa"
        ],

        "node.js": [
            "backend",
            "server",
            "api",
            "express"
        ],

        "express.js": [
            "routing",
            "middleware",
            "rest api",
            "backend"
        ],

        "mongodb": [
            "database",
            "nosql",
            "mongoose"
        ],

        "sql": [
            "mysql",
            "postgresql",
            "database",
            "queries"
        ],

        "rest api": [
            "api",
            "backend",
            "http"
        ],

        "jwt": [
            "authentication",
            "token",
            "security"
        ],

        "git": [
            "github",
            "version control"
        ],

        "github": [
            "repositories",
            "git"
        ],

        "authentication": [
            "login",
            "security",
            "jwt"
        ],

        "responsive design": [
            "mobile",
            "responsive",
            "ui"
        ],

        "frontend": [
            "react",
            "ui",
            "javascript"
        ],

        "backend": [
            "node",
            "server",
            "api"
        ],

        "api integration": [
            "rest api",
            "http",
            "fetch"
        ],

        "database": [
            "sql",
            "mongodb",
            "mysql"
        ],

        "deployment": [
            "hosting",
            "vercel",
            "render"
        ],

        "json": [
            "api",
            "data exchange"
        ]

    }

    match_points = 0

    total_points = len(required_skills) * 10

    for skill in required_skills:

        skill_lower = skill.lower()

        found = False

        # =========================
        # EXACT MATCH
        # =========================

        if skill_lower in resume_text:

            match_points += 10

            matched_skills.append(skill)

            found = True

        # =========================
        # RELATED KEYWORDS
        # =========================

        elif skill_lower in related_keywords:

            for keyword in related_keywords[skill_lower]:

                if keyword in resume_text:

                    match_points += 6

                    matched_skills.append(skill)

                    found = True

                    break

        # =========================
        # MISSING SKILL
        # =========================

        if not found:

            missing_skills.append(skill)

    # =========================
    # FINAL SCORE
    # =========================

    if total_points > 0:

        score = int(

            (match_points / total_points) * 100

        )

    else:

        score = 0

    # =========================
    # SCORE CALCULATION
    # =========================

    if len(required_skills) > 0:

        score = int(

            (len(matched_skills)
            / len(required_skills)) * 100

        )

    else:

        score = 0

    # =========================
    # SAVE PROGRESS
    # =========================

    cursor.execute(

        '''

        INSERT INTO progress (

            username,
            role,
            score,
            matched_skills,
            missing_skills

        )

        VALUES (?, ?, ?, ?, ?)

        ''',

        (

            session['user'],
            role,
            score,
            len(matched_skills),
            len(missing_skills)

        )

    )

    conn.commit()

    # =========================
    # LEARNING ROADMAP
    # =========================

    roadmap = []

    for skill in missing_skills:

        if skill.lower() == "react":

            roadmap.append(

                "Build modern interactive frontend applications using React and component-based architecture."

            )

        elif skill.lower() == "node.js":

            roadmap.append(

                "Develop scalable backend services and REST APIs using Node.js and asynchronous programming."

            )

        elif skill.lower() == "express.js":

            roadmap.append(

                "Create secure server-side applications and API routing using Express.js framework."

            )

        elif skill.lower() == "mongodb":

            roadmap.append(

                "Design and manage NoSQL databases using MongoDB collections, schemas, and aggregation pipelines."

            )

        elif skill.lower() == "jwt":

            roadmap.append(

                "Implement JWT authentication and secure session management for modern web applications."

            )

        elif skill.lower() == "rest api":

            roadmap.append(

                "Build and integrate RESTful APIs for seamless frontend-backend communication."

            )

        elif skill.lower() == "html":

            roadmap.append(

                "Develop semantic and accessible webpage structures using modern HTML standards."

            )

        elif skill.lower() == "css":

            roadmap.append(

                "Design responsive and visually appealing user interfaces using advanced CSS techniques."

            )

        elif skill.lower() == "javascript":

            roadmap.append(

                "Strengthen JavaScript fundamentals including DOM manipulation, ES6 features, and asynchronous programming."

            )

        elif skill.lower() == "git":

            roadmap.append(

                "Practice version control workflows and collaborative development using Git and GitHub."

            )

        elif skill.lower() == "github":

            roadmap.append(

                "Manage repositories, pull requests, and collaborative software workflows using GitHub."

            )

        elif skill.lower() == "authentication":

            roadmap.append(

                "Learn secure authentication workflows including sessions, password hashing, and access control."

            )

        elif skill.lower() == "deployment":

            roadmap.append(

                "Deploy full-stack applications using modern cloud hosting platforms and production environments."

            )

        elif skill.lower() == "database":

            roadmap.append(

                "Understand database design, CRUD operations, relationships, and scalable data management concepts."

            )

        elif skill.lower() == "frontend":

            roadmap.append(

                "Improve frontend engineering skills including responsive design, accessibility, and UI optimization."

            )

        elif skill.lower() == "backend":

            roadmap.append(

                "Strengthen backend architecture knowledge including APIs, authentication, and server-side logic."

            )

        elif skill.lower() == "api integration":

            roadmap.append(

                "Practice integrating third-party APIs and managing client-server communication efficiently."

            )

        elif skill.lower() == "responsive design":

            roadmap.append(

                "Create responsive applications optimized for desktop, tablet, and mobile devices."

            )

        elif skill.lower() == "json":

            roadmap.append(

                "Understand JSON structures and efficient data exchange between frontend and backend systems."

            )

        elif skill.lower() == "sql":

            roadmap.append(

                "Master SQL queries, joins, aggregations, and relational database management concepts."

            )

        elif skill.lower() == "python":

            roadmap.append(

                "Strengthen Python programming skills including automation, backend logic, and problem solving."

            )

        else:

            roadmap.append(

                f"Strengthen practical implementation skills and real-world project experience in {skill}."

            )
     # =========================
    # RESUME FEEDBACK
    # =========================

    resume_feedback = []

    # =========================
    # PROJECT ANALYSIS
    # =========================

    project_keywords = [

        "project",
        "developed",
        "built",
        "application",
        "system"

    ]

    project_score = 0

    for keyword in project_keywords:

        if keyword in resume_text:

            project_score += 1

    if project_score < 2:

        resume_feedback.append({

            "title":
            "Projects Recommendation",

            "message":
            "Your resume needs stronger project-based experience showcasing practical implementations and technical problem-solving."

        })

    # =========================
    # CERTIFICATION ANALYSIS
    # =========================

    certification_keywords = [

        "certification",
        "course",
        "forage",
        "internship",
        "training"

    ]

    certification_found = False

    for keyword in certification_keywords:

        if keyword in resume_text:

            certification_found = True

            break

    if not certification_found:

        resume_feedback.append({

            "title":
            "Certifications Recommendation",

            "message":
            "Adding certifications, internships, or professional training programs can significantly strengthen your resume credibility."

        })

    # =========================
    # EXPERIENCE ANALYSIS
    # =========================

    experience_keywords = [

        "experience",
        "internship",
        "freelance",
        "developer",
        "engineer"

    ]

    experience_found = False

    for keyword in experience_keywords:

        if keyword in resume_text:

            experience_found = True

            break

    if not experience_found:

        resume_feedback.append({

            "title":
            "Experience Recommendation",

            "message":
            "Your resume would benefit from internships, freelance work, or collaborative development experience."

        })

    # =========================
    # RESUME LENGTH ANALYSIS
    # =========================

    total_words = len(

        resume_text.split()

    )

    if total_words < 300:

        resume_feedback.append({

            "title":
            "Resume Depth Recommendation",

            "message":
            "Your resume appears relatively short. Expanding technical contributions and project explanations can improve recruiter impact."

        })

    # =========================
    # ACTION VERB ANALYSIS
    # =========================

    action_verbs = [

        "developed",
        "built",
        "created",
        "implemented",
        "optimized",
        "designed",
        "engineered"

    ]

    action_found = False

    for verb in action_verbs:

        if verb in resume_text:

            action_found = True

            break

    if not action_found:

        resume_feedback.append({

            "title":
            "Action Verb Suggestion",

            "message":
            "Use stronger action-oriented words like Developed, Built, Implemented, or Designed to improve professional impact."

        })

    # =========================
    # ATS OPTIMIZATION
    # =========================

    if score < 60:

        resume_feedback.append({

            "title":
            "ATS Optimization Suggestion",

            "message":
            "Your resume may benefit from stronger ATS keyword optimization aligned with the selected role requirements."

        })
    # =========================
    # INTERVIEW QUESTIONS
    # =========================

    questions = interview_data.get(role, [])

    # =========================
    # LEARNING RESOURCES
    # =========================

    resources = []

    for skill in missing_skills:

        resource = resources_data.get(skill.lower())

        if resource:

            resources.append(resource)

    # =========================
    # WEAK AREA TRAINING
    # =========================

    weak_training_data = []

    for skill in missing_skills:

        training = weak_area_training.get(

            skill.lower()

        )

        if training:

            weak_training_data.append({

                "skill": skill,

                "practice_tasks":
                training.get(
                    "practice_tasks",
                    []
                ),

                "improvement_tips":
                training.get(
                    "improvement_tips",
                    []
                )

            })

    # =========================
    # FETCH USER HISTORY
    # =========================

    cursor.execute(

        '''

        SELECT score

        FROM progress

        WHERE username = ?

        ORDER BY id DESC

        LIMIT 5

        ''',

        (

            session['user'],

        )

    )

    history = cursor.fetchall()

    history_scores = []

    for item in history:

        history_scores.append(

            item[0]

        )

    # =========================
    # RENDER DASHBOARD
    # =========================

    return render_template(

        'dashboarde.html',

        role=role,

        score=score,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        roadmap=roadmap,

        questions=questions,

        resources=resources,

        resume_feedback=resume_feedback,

        professional_tips=professional_tips,

        weak_training_data=weak_training_data,

        history_scores=history_scores

    )

# =========================
# INTERVIEW ROUTE
# =========================

@app.route('/interview')

def interview():

    if 'user' not in session:

        return redirect('/login')

    global selected_role

    global selected_missing_skills

    role_questions = interview_data.get(
        selected_role,
        []
    )

    filtered_questions = []

    for question in role_questions:

        question_skills = question.get(
            'skills',
            []
        )

        for skill in selected_missing_skills:

            for qskill in question_skills:

                if skill.lower() == qskill.lower():

                    if question not in filtered_questions:

                        filtered_questions.append(
                            question
                        )

                    break

    if len(filtered_questions) == 0:

        filtered_questions = role_questions

    easy_questions = []

    medium_questions = []

    hard_questions = []

    for question in filtered_questions:

        if question['difficulty'] == 'Easy':

            easy_questions.append(question)

        elif question['difficulty'] == 'Medium':

            medium_questions.append(question)

        elif question['difficulty'] == 'Hard':

            hard_questions.append(question)

    selected_questions = []

    selected_questions.extend(

        random.sample(
            easy_questions,
            min(4, len(easy_questions))
        )

    )

    selected_questions.extend(

        random.sample(
            medium_questions,
            min(4, len(medium_questions))
        )

    )

    selected_questions.extend(

        random.sample(
            hard_questions,
            min(4, len(hard_questions))
        )

    )

    if len(selected_questions) < 10:

        remaining_questions = [

            q for q in filtered_questions
            if q not in selected_questions

        ]

        extra_needed = 10 - len(selected_questions)

        if len(remaining_questions) > 0:

            selected_questions.extend(

                random.sample(

                    remaining_questions,

                    min(
                        extra_needed,
                        len(remaining_questions)
                    )

                )

            )

    random.shuffle(selected_questions)

    return render_template(

        'interview.html',

        role=selected_role,

        questions=selected_questions

    )
# =========================
# INTERVIEW RESULT ROUTE
# =========================

@app.route(

    '/interview_result',

    methods=['POST']

)

def interview_result():

    if 'user' not in session:

        return redirect('/login')

    technical_score = 0

    communication_score = 0

    confidence_score = 0

    strong_areas = []

    weak_areas = []

    # =========================
    # RECEIVE JSON DATA
    # =========================

    data = request.get_json()

    submitted_answers = data.get(

        'answers',

        []

    )

    all_answer_text = ""

    for item in submitted_answers:

        all_answer_text += (

            item.get('answer', '')
            + " "

        )

    answers = all_answer_text.lower()

    total_words = len(

        answers.split()

    )

    # =========================
    # ROLE-BASED SKILLS
    # =========================

    if selected_role == "Full Stack Developer":

        all_skills = [

            "react",
            "api",
            "authentication",
            "frontend",
            "backend",
            "mongodb",
            "sql",
            "javascript",
            "deployment",
            "system design"

        ]

    elif selected_role == "Software Engineer":

        all_skills = [

            "encapsulation",
            "inheritance",
            "polymorphism",
            "algorithm",
            "stack",
            "queue",
            "linked list",
            "database",
            "sql",
            "problem solving"

        ]

    elif selected_role == "Data Analyst":

        all_skills = [

            "sql",
            "excel",
            "tableau",
            "power bi",
            "python",
            "visualization",
            "data cleaning",
            "etl",
            "statistics",
            "analytics"

        ]

    else:

        all_skills = [

            "programming",
            "problem solving",
            "database",
            "apis",
            "development"

        ]

    # =========================
    # CONFIDENCE WORDS
    # =========================

    confidence_positive_words = [

        "implemented",
        "developed",
        "optimized",
        "designed",
        "built",
        "created"

    ]

    confidence_negative_words = [

        "maybe",
        "guess",
        "probably",
        "not sure",
        "i think"

    ]

    # =========================
    # TECHNICAL SCORE
    # =========================

    matched_skills = 0

    for skill in all_skills:

        if skill in answers:

            matched_skills += 1

            strong_areas.append(

                skill.title()

            )

        else:

            weak_areas.append(

                skill.title()

            )

    technical_score = min(

        100,

        matched_skills * 10

    )

    # =========================
    # COMMUNICATION SCORE
    # =========================

    communication_score = 50

    if total_words > 150:

        communication_score += 25

    elif total_words > 80:

        communication_score += 15

    elif total_words > 40:

        communication_score += 10

    if "." in answers:

        communication_score += 10

    if "," in answers:

        communication_score += 5

    communication_score = min(

        100,

        communication_score

    )

    # =========================
    # CONFIDENCE SCORE
    # =========================

    confidence_score = 60

    for word in confidence_positive_words:

        if word in answers:

            confidence_score += 5

    for word in confidence_negative_words:

        if word in answers:

            confidence_score -= 7

    confidence_score = max(

        0,

        min(100, confidence_score)

    )

    # =========================
    # OVERALL SCORE
    # =========================

    overall_score = int(

        (

            technical_score
            + communication_score
            + confidence_score

        ) / 3

    )

    # =========================
    # PERFORMANCE LEVEL
    # =========================

    if overall_score >= 85:

        recommendation = (

            f"Highly Recommended for {selected_role} Interviews"

        )

        performance = "Excellent"

    elif overall_score >= 70:

        recommendation = (

            f"Recommended for Junior {selected_role} Roles"

        )

        performance = "Good"

    else:

        recommendation = (

            "Needs Improvement Before Technical Interviews"

        )

        performance = "Average"

    # =========================
    # AI FEEDBACK
    # =========================

    ai_feedback = (

        f"You demonstrated strong understanding in {', '.join(strong_areas[:4])}. "
        f"Focus more on improving {', '.join(weak_areas[:4])} concepts to improve technical readiness and interview confidence."

    )

    return render_template(

    'interview_result.html',

    technical_score=technical_score,

    communication_score=communication_score,

    confidence_score=confidence_score,

    overall_score=overall_score,

    strong_areas=strong_areas,

    weak_areas=weak_areas,

    recommendation=recommendation,

    performance=performance,

    ai_feedback=ai_feedback,

    submitted_answers=submitted_answers

)
# =========================
# ASSESSMENT ROUTE
# =========================

@app.route('/assessment')

def assessment():

    if 'user' not in session:

        return redirect('/login')

    global selected_role

    global selected_missing_skills

    role_questions = assessment_data.get(

        selected_role,

        []

    )

    filtered_questions = []

    # =========================
    # FILTER QUESTIONS
    # BASED ON MISSING SKILLS
    # =========================

    for question in role_questions:

        question_skills = question.get(

            'skills',

            []

        )

        for skill in selected_missing_skills:

            for qskill in question_skills:

                if skill.lower() == qskill.lower():

                    if question not in filtered_questions:

                        filtered_questions.append(

                            question

                        )

                    break

    # =========================
    # FALLBACK
    # =========================

    if len(filtered_questions) == 0:

        filtered_questions = role_questions

    # =========================
    # RANDOMIZE QUESTIONS
    # =========================

    random.shuffle(filtered_questions)

    selected_questions = filtered_questions[:10]

    return render_template(

        'assessment.html',

        questions=selected_questions,

        role=selected_role

    )

# =========================
# ASSESSMENT RESULT ROUTE
# =========================

@app.route(

    '/assessment_result',

    methods=['POST']

)

def assessment_result():

    if 'user' not in session:

        return redirect('/login')

    data = request.get_json()

    submitted_answers = data.get(

        'answers',

        []

    )

    total_questions = len(

        submitted_answers

    )

    correct_answers = 0

    results = []

    for item in submitted_answers:

        selected_answer = item.get(

            'selectedAnswer',

            ''

        )

        correct_answer = item.get(

            'correctAnswer',

            ''

        )

        is_correct = (

            selected_answer == correct_answer

        )

        if is_correct:

            correct_answers += 1

        results.append({

            "question":
            item.get('question'),

            "selected":
            selected_answer,

            "correct":
            correct_answer,

            "difficulty":
            item.get('difficulty'),

            "explanation":
            item.get('explanation'),

            "is_correct":
            is_correct

        })

    if total_questions > 0:

        score = int(

            (

                correct_answers
                / total_questions

            ) * 100

        )

    else:

        score = 0

    return render_template(

        'assessment_result.html',

        score=score,

        correct_answers=correct_answers,

        total_questions=total_questions,

        results=results

    )
# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    app.run(

        debug=True,

        port=5001

    )