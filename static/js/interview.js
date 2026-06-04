/* =========================
VARIABLES
========================= */

let currentQuestion = 0;

let totalScore = 0;

let technicalScore = 0;

let communicationScore = 0;

let weakAreas = [];

let answerReview = [];

let categoryScores = {};

let totalTime = 15 * 60;

/* =========================
START APP
========================= */

window.onload = function(){

    loadQuestion();

    startTimer();
};

/* =========================
LOAD QUESTION
========================= */

function loadQuestion(){

    let current =
    interviewData[currentQuestion];

    // QUESTION NUMBER

    document.getElementById(
    "question-number"
    ).innerText =
    `Question ${currentQuestion + 1}
    / ${interviewData.length}`;

    // QUESTION

    document.getElementById(
    "question"
    ).innerText =
    current.question;

    // CATEGORY

    document.getElementById(
    "category"
    ).innerText =
    current.category;

    // DIFFICULTY

    document.getElementById(
    "difficulty"
    ).innerText =
    current.difficulty;

    // MARKS

    document.getElementById(
    "marks"
    ).innerText =
    current.marks;

    // CLEAR TEXTAREA

    document.getElementById(
    "answer-input"
    ).value = "";

    // PROGRESS

    let progress =

    ((currentQuestion + 1)
    / interviewData.length) * 100;

    document.querySelector(
    ".interview-progress-fill"
    ).style.width =
    progress + "%";
}

/* =========================
NEXT QUESTION
========================= */

function nextQuestion(){

    let answer =
    document.getElementById(
    "answer-input"
    ).value.trim();

    // VALIDATION

    if(answer === ""){

        alert(
        "Please enter your answer."
        );

        return;
    }

    evaluateAnswer(answer);

    currentQuestion++;

    // NEXT

    if(currentQuestion < interviewData.length){

        loadQuestion();
    }

    // RESULT

    else{

        showResult();
    }
}

/* =========================
EVALUATE ANSWER
========================= */

function evaluateAnswer(answer){

    let current =
    interviewData[currentQuestion];

    let keywords =
    current.keywords;

    let matched = 0;

    // KEYWORD MATCHING

    keywords.forEach(keyword => {

        if(

            answer.toLowerCase()
            .includes(
            keyword.toLowerCase()
            )

        ){

            matched++;
        }
    });

    // MATCH PERCENTAGE

    let matchPercent =

    (matched / keywords.length) * 100;

    // TECHNICAL SCORE

    let questionScore =

    Math.round(

        (matchPercent / 100)
        * current.marks

    );

    totalScore += questionScore;

    technicalScore += questionScore;

    // COMMUNICATION SCORE

    if(answer.length > 120){

        communicationScore += 10;
    }

    else if(answer.length > 60){

        communicationScore += 5;
    }

    // CATEGORY ANALYTICS

    if(!categoryScores[
    current.category
    ]){

        categoryScores[
        current.category
        ] = 0;
    }

    categoryScores[
    current.category
    ] += questionScore;

    // WEAK AREAS

    if(matchPercent < 50){

        weakAreas.push(
        current.category
        );
    }

    // STORE REVIEW

    answerReview.push({

        question:
        current.question,

        userAnswer:
        answer,

        modelAnswer:
        current.modelAnswer,

        feedback:
        current.feedback,

        match:
        Math.round(matchPercent)
    });
}

/* =========================
SHOW RESULT
========================= */

function showResult(){

    let performanceMessage = "";

    // PERFORMANCE

    if(totalScore >= 70){

        performanceMessage =
        "Excellent Interview Performance 🚀";
    }

    else if(totalScore >= 40){

        performanceMessage =
        "Good Attempt 👍";
    }

    else{

        performanceMessage =
        "Needs Improvement 📚";
    }

    // RESULT HTML

    let finalHTML = `

    <div class="result-box">

        <h1>
        🎉 Interview Completed
        </h1>

        <h2>
        Technical Score:
        ${technicalScore}
        </h2>

        <h2>
        Communication Score:
        ${communicationScore}
        </h2>

        <h2>
        Total Score:
        ${totalScore + communicationScore}
        </h2>

        <h3 style="color:#00c6ff;">

            ${performanceMessage}

        </h3>

        <h2 style="margin-top:40px;">

            Category Analytics

        </h2>
    `;

    // CATEGORY SCORES

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

        <h2 style="margin-top:40px;">

            Weak Areas

        </h2>
        `;

        weakAreas.forEach(area => {

            finalHTML += `

            <div class="feedback-card">

                <h4>
                ${area}
                </h4>

                <p>
                Improve concepts related to
                ${area}
                </p>

            </div>
            `;
        });
    }

    // ANSWER REVIEW

    finalHTML += `

    <h2 style="margin-top:40px;">

        Interview Review

    </h2>
    `;

    answerReview.forEach(item => {

        finalHTML += `

        <div class="feedback-card">

            <h4>

                ${item.question}

            </h4>

            <p>

                <strong>
                Match Percentage:
                </strong>

                ${item.match}%

            </p>

            <p>

                <strong>
                Your Answer:
                </strong>

                ${item.userAnswer}

            </p>

            <div class="model-answer">

                <strong>
                Model Answer:
                </strong>

                <p>

                    ${item.modelAnswer}

                </p>

            </div>

            <div class="model-answer">

                <strong>
                Feedback:
                </strong>

                <p>

                    ${item.feedback}

                </p>

            </div>

        </div>
        `;
    });

    // RESTART BUTTON

    finalHTML += `

    <div style="margin-top:40px;">

        <a href="/interview">

            <button>

                Restart Interview

            </button>

        </a>

    </div>

    </div>
    `;

    // RENDER

    document.querySelector(
    ".interview-card"
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
        "timer"
        );

        if(timerElement){

            timerElement.innerText =
            `${minutes}:${seconds}`;
        }

        totalTime--;

        // TIME UP

        if(totalTime < 0){

            clearInterval(timer);

            showResult();
        }

    }, 1000);
}