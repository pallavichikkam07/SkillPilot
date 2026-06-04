/* =========================
VARIABLES
========================= */

let currentQuestion = 0;

let totalScore = 0;

let selectedAnswer = "";

let weakAreas = [];

let answerReview = [];

let categoryScores = {};

let totalTime = 10 * 60;

/* =========================
START APP
========================= */

window.onload = function(){

    loadAssessmentQuestion();

    startTimer();
};

/* =========================
SELECT OPTION
========================= */

function selectOption(button){

    // REMOVE OLD SELECTION

    document.querySelectorAll(
    ".option-btn"
    ).forEach(btn => {

        btn.classList.remove(
        "selected-option"
        );

    });

    // ADD NEW SELECTION

    button.classList.add(
    "selected-option"
    );

    selectedAnswer =
    button.innerText;
}

/* =========================
LOAD QUESTION
========================= */

function loadAssessmentQuestion(){

    let current =
    assessmentData[currentQuestion];

    // QUESTION NUMBER

    document.getElementById(
    "assessment-question-number"
    ).innerText =
    `Question ${currentQuestion + 1}
    / ${assessmentData.length}`;

    // QUESTION

    document.getElementById(
    "assessment-question"
    ).innerText =
    current.question;

    // CATEGORY

    document.getElementById(
    "assessment-category"
    ).innerText =
    current.category;

    // DIFFICULTY

    document.getElementById(
    "assessment-difficulty"
    ).innerText =
    current.difficulty;

    // MARKS

    document.getElementById(
    "assessment-marks"
    ).innerText =
    current.marks;

    // OPTIONS

    let optionButtons =
    document.querySelectorAll(
    ".option-btn"
    );

    for(let i = 0; i < 4; i++){

        optionButtons[i].innerText =
        current.options[i];

        optionButtons[i].classList.remove(
        "selected-option"
        );
    }

    // RESET ANSWER

    selectedAnswer = "";

    // UPDATE PROGRESS

    let progress =

    ((currentQuestion + 1)
    / assessmentData.length) * 100;

    document.querySelector(
    ".interview-progress-fill"
    ).style.width =
    progress + "%";
}

/* =========================
NEXT QUESTION
========================= */

function nextAssessmentQuestion(){

    // VALIDATION

    if(selectedAnswer === ""){

        alert(
        "Please select an option."
        );

        return;
    }

    // EVALUATE

    evaluateAnswer();

    currentQuestion++;

    // NEXT

    if(currentQuestion < assessmentData.length){

        loadAssessmentQuestion();
    }

    // FINAL RESULT

    else{

        showAssessmentResult();
    }
}

/* =========================
EVALUATE ANSWER
========================= */

function evaluateAnswer(){

    let current =
    assessmentData[currentQuestion];

    // CORRECT

    if(selectedAnswer ===
    current.correctAnswer){

        totalScore +=
        current.marks;

        // CATEGORY SCORE

        if(!categoryScores[
        current.category
        ]){

            categoryScores[
            current.category
            ] = 0;
        }

        categoryScores[
        current.category
        ] += current.marks;
    }

    // WRONG

    else{

        weakAreas.push(
        current.category
        );
    }

    // STORE REVIEW

    answerReview.push({

        question:
        current.question,

        userAnswer:
        selectedAnswer,

        correctAnswer:
        current.correctAnswer,

        explanation:
        current.explanation
    });
}

function showAssessmentResult(){

    let performanceMessage = "";

    let performanceColor = "";

    // PERFORMANCE LEVEL

    if(totalScore >= 60){

        performanceMessage =
        "Excellent Performance 🚀";

        performanceColor =
        "#22c55e";
    }

    else if(totalScore >= 30){

        performanceMessage =
        "Good Attempt 👍";

        performanceColor =
        "#3b82f6";
    }

    else{

        performanceMessage =
        "Needs Improvement 📚";

        performanceColor =
        "#ef4444";
    }

    // OVERALL PERCENTAGE

    let maxPossibleScore =
    assessmentData.reduce(

        (sum, q) => sum + q.marks,

        0

    );

    let percentage = Math.round(

        (totalScore / maxPossibleScore)
        * 100

    );

    // MAIN HTML

    let finalHTML = `

    <div style="padding:40px; color:white;">

        <!-- TITLE -->

        <h1 style="
        text-align:center;
        font-size:48px;
        margin-bottom:40px;">

            🚀 Assessment Analytics

        </h1>

        <!-- TOP CARDS -->

        <div style="
        display:grid;
        grid-template-columns:
        repeat(auto-fit,minmax(250px,1fr));
        gap:25px;">

            <div class="result-card">

                <h2>
                🏆 Final Score
                </h2>

                <h1 style="
                font-size:60px;
                margin-top:20px;">

                    ${percentage}%

                </h1>

            </div>

            <div class="result-card">

                <h2>
                ✅ Correct Answers
                </h2>

                <h1 style="
                font-size:60px;
                margin-top:20px;">

                    ${answerReview.filter(
                    item =>
                    item.userAnswer ===
                    item.correctAnswer
                    ).length}

                </h1>

            </div>

            <div class="result-card">

                <h2>
                ⚠ Wrong Answers
                </h2>

                <h1 style="
                font-size:60px;
                margin-top:20px;">

                    ${answerReview.filter(
                    item =>
                    item.userAnswer !==
                    item.correctAnswer
                    ).length}

                </h1>

            </div>

        </div>

        <!-- PERFORMANCE -->

        <div class="feedback-card"
        style="margin-top:40px;">

            <h2>

                📈 Performance Analysis

            </h2>

            <h1 style="
            color:${performanceColor};
            margin-top:20px;">

                ${performanceMessage}

            </h1>

            <p style="
            margin-top:20px;
            font-size:20px;
            line-height:1.8;">

                Your assessment performance
                indicates your current
                technical readiness level
                in the selected missing skills.

            </p>

        </div>

        <!-- CATEGORY ANALYTICS -->

        <div class="feedback-card"
        style="margin-top:40px;">

            <h2>

                📚 Skill Analytics

            </h2>
    `;

    // CATEGORY SCORES

    for(let category in categoryScores){

        finalHTML += `

        <div style="
        margin-top:25px;">

            <h3>

                ${category}

            </h3>

            <div style="
            width:100%;
            height:14px;
            background:#1e293b;
            border-radius:10px;
            overflow:hidden;
            margin-top:10px;">

                <div style="
                width:${categoryScores[category] * 5}%;
                height:100%;
                background:
                linear-gradient(
                    90deg,
                    #3b82f6,
                    #8b5cf6
                );">

                </div>

            </div>

        </div>
        `;
    }

    finalHTML += `

        </div>
    `;

    // WEAK AREAS

    if(weakAreas.length > 0){

        finalHTML += `

        <div class="feedback-card"
        style="margin-top:40px;">

            <h2>

                ⚠ Weak Areas

            </h2>
        `;

        weakAreas.forEach(area => {

            finalHTML += `

            <div style="
            margin-top:20px;
            padding:20px;
            border-radius:14px;
            background:
            rgba(255,255,255,0.05);">

                <h3>

                    ${area}

                </h3>

                <p style="
                margin-top:10px;">

                    Improve understanding,
                    practical implementation,
                    and problem-solving
                    concepts related to
                    ${area}.

                </p>

            </div>
            `;
        });

        finalHTML += `

        </div>
        `;
    }

    // ANSWER REVIEW

    finalHTML += `

    <div class="feedback-card"
    style="margin-top:40px;">

        <h2>

            📝 Answer Review

        </h2>
    `;

    answerReview.forEach(item => {

        let isCorrect =
        item.userAnswer ===
        item.correctAnswer;

        finalHTML += `

        <div style="
        margin-top:30px;
        padding:25px;
        border-radius:18px;
        background:
        rgba(255,255,255,0.05);">

            <h3 style="
            line-height:1.6;">

                ❓ ${item.question}

            </h3>

            <p style="
            margin-top:20px;">

                <strong>
                Your Answer:
                </strong>

                ${item.userAnswer}

            </p>

            <p style="
            margin-top:15px;">

                <strong>
                Correct Answer:
                </strong>

                ${item.correctAnswer}

            </p>

            <p style="
            margin-top:15px;
            color:
            ${isCorrect
            ? "#22c55e"
            : "#ef4444"};">

                <strong>

                    ${isCorrect
                    ? "Correct Answer ✅"
                    : "Incorrect Answer ❌"}

                </strong>

            </p>

            <div style="
            margin-top:20px;
            padding:20px;
            border-radius:14px;
            background:
            rgba(255,255,255,0.04);">

                <strong>

                    Explanation:

                </strong>

                <p style="
                margin-top:12px;
                line-height:1.8;">

                    ${item.explanation}

                </p>

            </div>

        </div>
        `;
    });

    finalHTML += `

    </div>

    <!-- BUTTONS -->

    <div style="
    margin-top:50px;
    text-align:center;">

        <a href="/assessment">

            <button class="next-btn">

                Restart Assessment

            </button>

        </a>

        <a href="/">

            <button class="next-btn"
            style="margin-left:20px;">

                Back To Dashboard

            </button>

        </a>

    </div>

    </div>
    `;

    // RENDER

    document.querySelector(
    ".assessment-card"
    ).innerHTML =
    finalHTML;
}
/* =========================
TIMER
========================= */

function startTimer(){

    const timer = setInterval(function(){

        let minutes =
        Math.floor(totalTime / 60);

        let seconds =
        totalTime % 60;

        seconds =
        seconds < 10
        ? "0" + seconds
        : seconds;

        let timerElement =
        document.getElementById(
        "assessment-timer"
        );

        if(timerElement){

            timerElement.innerText =
            `${minutes}:${seconds}`;
        }

        totalTime--;

        // TIME UP

        if(totalTime < 0){

            clearInterval(timer);

            showAssessmentResult();
        }

    }, 1000);
}