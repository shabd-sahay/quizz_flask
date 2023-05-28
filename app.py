from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta, date
import mysql.connector
import mysql.connector.pooling


app = Flask(__name__)

# Connect to MySQL
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    host="localhost",
    user="root",
    password="Shabd@2003..",
    database="quizzes"
)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/quizzes', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'GET':
        return render_template('quiz-create.html')
    elif request.method == 'POST':
        # Retrieve the form data
        question = request.form.get('question')
        options = request.form.get('options')
        right_answer = request.form.get('right-answer')
        start_date_str = request.form.get('start-date')
        end_date_str = request.form.get('end-date')

        # Convert the start_date_str and end_date_str to date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Check if all required fields are provided
        if not question or not options or not right_answer or not start_date or not end_date:
            return 'Please fill in all fields'

        # Create a connection from the pool
        cnx = cnx_pool.get_connection()

        # Insert quiz data into the database
        cursor = cnx.cursor()
        insert_query = "INSERT INTO quizzes (question, options, rightAnswer, startDate, endDate) VALUES (%s, %s, %s, %s, %s)"
        values = (question, options, right_answer, start_date, end_date)
        cursor.execute(insert_query, values)
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        return 'Quiz created successfully!'


@app.route('/quizzes/active', methods=['GET'])
def get_active_quiz():
    # Get the current time
    current_time = datetime.now()

    # Create a connection from the pool
    cnx = cnx_pool.get_connection()

    # Query the database to find the active quiz based on the current time
    select_query = """
    SELECT * FROM quizzes
    WHERE startDate <= %s AND endDate >= %s
    """
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(select_query, (current_time, current_time))
    active_quiz = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Check if active quiz exists
    if active_quiz:
        return render_template('quiz-active.html', quiz=active_quiz)
    else:
        return render_template('quiz-active.html', quiz=None)

@app.route('/quizzes/<quiz_id>/result', methods=['GET'])
def get_quiz_result(quiz_id):
    # Create a connection from the pool
    cnx = cnx_pool.get_connection()

    # Check if the connection is established successfully
    if not cnx:
        return jsonify({'message': 'Failed to establish database connection'}), 500

    try:
        # Create a cursor
        cursor = cnx.cursor(dictionary=True)

        # Query the database to find the quiz by its ID
        select_query = "SELECT * FROM quizzes WHERE id = %s"
        cursor.execute(select_query, (quiz_id,))
        quiz = cursor.fetchone()
        if not quiz:
            return jsonify({'message': 'Quiz not found'}), 404

        # Check if the quiz result is available (5 minutes after the end time)
        current_time = datetime.now().date()
        end_time = quiz['endDate']
        result_available_time = end_time + timedelta(minutes=5)
        if current_time < result_available_time:
            return jsonify({'message': 'Quiz result not available yet'})

        # Retrieve the quiz result from the database
        select_result_query = "SELECT * FROM quizzes WHERE id = %s"
        cursor.execute(select_result_query, (quiz_id,))
        quiz_result = cursor.fetchone()

        if not quiz_result:
            return jsonify({'message': 'Quiz result not found'})

        # Return the quiz result as a JSON response
        return render_template('quiz-result.html', result=quiz_result['rightAnswer'], quiz_id=quiz_result['id'])

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.route('/quizzes/all', methods=['GET'])
def get_all_quizzes():
    # Create a connection from the pool
    cnx = cnx_pool.get_connection()

    # Create a cursor
    cursor = cnx.cursor(dictionary=True)

    # Query the database to retrieve all quizzes
    select_query = "SELECT * FROM quizzes"
    cursor.execute(select_query)
    all_quizzes = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Render the quiz-all.html template and pass the quizzes data
    return render_template('quiz-all.html', quizzes=all_quizzes)

if __name__ == '__main__':
    app.run(debug=True)
