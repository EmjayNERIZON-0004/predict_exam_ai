from flask import Flask, request, render_template
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Initialize Flask app
app = Flask(__name__)

# Sample training data
data = [
    {"study_hours": 1.0, "previous_grade": 45, "quiz_score": 40, "passed": 0},
    {"study_hours": 1.5, "previous_grade": 50, "quiz_score": 35, "passed": 0},
    {"study_hours": 2.0, "previous_grade": 55, "quiz_score": 45, "passed": 0},
    {"study_hours": 2.5, "previous_grade": 58, "quiz_score": 55, "passed": 0},
    {"study_hours": 3.0, "previous_grade": 60, "quiz_score": 60, "passed": 0},
    {"study_hours": 3.5, "previous_grade": 62, "quiz_score": 63, "passed": 0},
    {"study_hours": 4.0, "previous_grade": 64, "quiz_score": 66, "passed": 0},
    {"study_hours": 4.5, "previous_grade": 66, "quiz_score": 68, "passed": 0},
    {"study_hours": 5.0, "previous_grade": 68, "quiz_score": 70, "passed": 0},
    {"study_hours": 5.5, "previous_grade": 70, "quiz_score": 72, "passed": 0},
    {"study_hours": 6.0, "previous_grade": 72, "quiz_score": 74, "passed": 0},
    {"study_hours": 6.5, "previous_grade": 74, "quiz_score": 76, "passed": 0},
    {"study_hours": 7.0, "previous_grade": 76, "quiz_score": 78, "passed": 1},
    {"study_hours": 7.5, "previous_grade": 78, "quiz_score": 80, "passed": 1},
    {"study_hours": 8.0, "previous_grade": 80, "quiz_score": 82, "passed": 1},
    {"study_hours": 2.0, "previous_grade": 40, "quiz_score": 20, "passed": 0},
    {"study_hours": 3.0, "previous_grade": 45, "quiz_score": 35, "passed": 0},
    {"study_hours": 4.0, "previous_grade": 50, "quiz_score": 50, "passed": 0},
    {"study_hours": 5.0, "previous_grade": 55, "quiz_score": 55, "passed": 0},
    {"study_hours": 6.0, "previous_grade": 60, "quiz_score": 60, "passed": 0},
    {"study_hours": 1.5, "previous_grade": 30, "quiz_score": 10, "passed": 0},
    {"study_hours": 2.5, "previous_grade": 35, "quiz_score": 25, "passed": 0},
    {"study_hours": 3.5, "previous_grade": 40, "quiz_score": 30, "passed": 0},
    {"study_hours": 4.5, "previous_grade": 45, "quiz_score": 40, "passed": 0},
    {"study_hours": 5.5, "previous_grade": 50, "quiz_score": 45, "passed": 0},
    {"study_hours": 6.5, "previous_grade": 55, "quiz_score": 50, "passed": 0},
    {"study_hours": 7.5, "previous_grade": 60, "quiz_score": 60, "passed": 0},
    {"study_hours": 8.0, "previous_grade": 65, "quiz_score": 65, "passed": 0},
    {"study_hours": 9.0, "previous_grade": 90, "quiz_score": 95, "passed": 1},
    {"study_hours": 3.0, "previous_grade": 75, "quiz_score": 60, "passed": 1}
]


# Create DataFrame
df = pd.DataFrame(data)

# Features (X) and target (y)
X = df[["study_hours", "previous_grade", "quiz_score"]]
y = df["passed"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Home route
@app.route('/')
def index():
    return render_template('form.html')

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    study_hours = float(request.form['study_hours'])
    previous_grade = float(request.form['previous_grade'])
    quiz_total = float(request.form['quiz_total'])
    quiz_correct = float(request.form['quiz_correct'])

    if quiz_total == 0:
        return render_template('form.html', prediction="⚠️ Total items can't be zero!")

    # Calculate quiz percentage
    quiz_score = (quiz_correct / quiz_total) * 100

    # Prediction
    input_data = [[study_hours, previous_grade, quiz_score]]
    # prediction = model.predict(input_data)[0]
    # probabilities = model.predict_proba(input_data)[0]  # [fail_prob, pass_prob]
    probabilities = model.predict_proba(input_data)[0]
    threshold = 0.75  # 75% confidence required to pass
    predicted_class = 1 if probabilities[1] >= threshold else 0

    pass_percentage = round(probabilities[1] * 100, 2)
    fail_percentage = round(probabilities[0] * 100, 2)
    score = probabilities[1]
    result = "Passed" if predicted_class == 1 else "Failed"

    return render_template(
        'form.html',
        prediction=result,
        pass_pct=pass_percentage,
        fail_pct=fail_percentage,
        score=score,
        study_hours=study_hours,
        previous_grade=previous_grade,
        quiz_total=quiz_total,
        quiz_correct=quiz_correct,
        quiz_score=round(quiz_score, 2)
    )


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
