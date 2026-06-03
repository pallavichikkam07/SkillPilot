/* =========================
   VARIABLES
========================= */

let currentQuestion = 0;

let totalScore = 0;

let weakAreas = [];

let feedbackList = [];

let modelAnswers = [];

/* CATEGORY SCORES */

let categoryScores = {};

/* =========================
   INITIAL PROGRESS
========================= */

document.querySelector(
".interview-progress-fill"
).style.width = "20%";

/* =========================
   NEXT QUESTION
========================= */

function nextQuestion(){

    const answer =
    document.getElementById("answer-box")
    .value
    .trim()
    .toLowerCase();

    // EMPTY CHECK

    if(answer === ""){

        alert("Please type an answer.");

        return;
    }

    evaluateAnswer(answer);

    currentQuestion++;

    // NEXT QUESTION

    if(currentQuestion < interviewData.length){

        loadQuestion();
    }

    // FINAL RESULT

    else{

        showFinalResult();
    }
}

/* =========================
   LOAD QUESTION
========================= */

function loadQuestion(){

    let current =
    interviewData[currentQuestion];

    // QUESTION

    document.getElementById(
    "question-text"
    ).innerText =
    current.question;

    // QUESTION NUMBER

    document.getElementById(
    "question-number"
    ).innerText =
    `Question ${currentQuestion + 1}
    / ${interviewData.length}`;

    // CATEGORY

    document.getElementById(
    "question-category"
    ).innerText =
    current.category;

    // DIFFICULTY

    document.getElementById(
    "question-difficulty"
    ).innerText =
    current.difficulty;

    // MARKS

    document.getElementById(
    "question-marks"
    ).innerText =
    current.marks;

    // PROGRESS BAR

    let progress =
    ((currentQuestion + 1)
    / interviewData.length) * 100;

    document.querySelector(
    ".interview-progress-fill"
    ).style.width =
    progress + "%";

    // CLEAR ANSWER

    document.getElementById(
    "answer-box"
    ).value = "";
}

/* =========================
   EVALUATE ANSWER
========================= */

function evaluateAnswer(answer){

    let data =
    interviewData[currentQuestion];

    let keywords =
    data.keywords;

    let matched = 0;

    keywords.forEach(keyword => {

        if(answer.includes(
        keyword.toLowerCase())){

            matched++;
        }
    });

    // QUESTION MARKS

    let marks =
    data.marks;

    // SCORE CALCULATION

    let questionScore =
    (matched / keywords.length)
    * marks;

    totalScore +=
    Math.round(questionScore);

    // CATEGORY SCORE

    let category =
    data.category;

    if(!categoryScores[category]){

        categoryScores[category] = 0;
    }

    categoryScores[category] +=
    Math.round(questionScore);

    // WEAK AREA

    if(matched < 2){

        weakAreas.push(
        data.question
        );

        feedbackList.push(
        data.feedback
        );

        modelAnswers.push(
        data.modelAnswer
        );
    }
}

/* =========================
   FINAL RESULT
========================= */

function showFinalResult(){

    let performanceMessage = "";

    // PERFORMANCE LEVEL

    if(totalScore >= 40){

        performanceMessage =
        "Excellent Performance 🚀";
    }

    else if(totalScore >= 20){

        performanceMessage =
        "Good Attempt 👍";
    }

    else{

        performanceMessage =
        "Needs Improvement 📚";
    }

    // HTML

    let finalHTML = `

    <div class="result-box">

        <h1>
        🎉 Interview Completed
        </h1>

        <h2>
        Final Score:
        ${totalScore}
        </h2>

        <h3 style="color:#00c6ff;">
        ${performanceMessage}
        </h3>

        <h2 class="weak-heading">
        Skill Analytics
        </h2>

    `;

    // CATEGORY ANALYTICS

    for(let category in categoryScores){

        finalHTML += `

        <div class="feedback-card">

            <h4>
            ${category}
            </h4>

            <p>
            Score:
            ${categoryScores[category]}
            </p>

        </div>

        `;
    }

    // WEAK AREAS

    if(weakAreas.length > 0){

        finalHTML += `

        <h2 class="weak-heading">

            Weak Areas

        </h2>

        `;

        weakAreas.forEach((area, index) => {

            finalHTML += `

            <div class="feedback-card">

                <h4>
                ${area}
                </h4>

                <p>
                ${feedbackList[index]}
                </p>

                <div class="model-answer">

                    <strong>
                    Recommended Answer:
                    </strong>

                    <p>
                    ${modelAnswers[index]}
                    </p>

                </div>

            </div>

            `;
        });
    }

    // NO WEAK AREAS

    else{

        finalHTML += `

        <div class="feedback-card">

            <h4 style="color:#22c55e;">

                Excellent Work 🎉

            </h4>

            <p>

                You answered all
                questions very well.

            </p>

        </div>

        `;
    }

    // RESTART BUTTON

    finalHTML += `

    <div style="margin-top:40px;">

        <a href="/interview">

            <button class="restart-btn">

                Restart Interview

            </button>

        </a>

    </div>

    </div>

    `;

    // RENDER RESULT

    document.querySelector(
    ".interview-card"
    ).innerHTML =
    finalHTML;
}

/* =========================
   TIMER
========================= */

let totalTime = 15 * 60;

const timer = setInterval(function(){

    let minutes =
    Math.floor(totalTime / 60);

    let seconds =
    totalTime % 60;

    seconds =
    seconds < 10
    ? "0" + seconds
    : seconds;

    document.getElementById(
    "timer"
    ).innerText =
    `${minutes}:${seconds}`;

    totalTime--;

    // TIME UP

    if(totalTime < 0){

        clearInterval(timer);

        showFinalResult();
    }

}, 1000);