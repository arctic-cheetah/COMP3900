import json
from functools import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import db, error_msg

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this


@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """

    return jsonify(db.get_all_students())


@app.route("/students", methods=["POST"])
def create_student():
    # EDGE CASE: We are FUCKING NOT MAKING STUDENTS OPTIONALLY MARK
    # THEN how THE FUCK ARE YOU SUPPOSED TO CALCULATE MARKS PROPERLY??
    # FUCK THAT SHIT
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.get_json(silent=True)
    if not isinstance(student_data, dict):
        return jsonify({"error": error_msg.ERROR_JSON}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", None)
    if mark is None:
        mark = 0

    # EDGE CASE 2: We need to FUCKING CHECK for strings that are WHITESPACE
    # Why THE FUCK WOULD THAT HAPPEN? BUT DO SO

    if not isinstance(name, str) or name.strip() == "":
        return jsonify({"error": error_msg.ERROR_NAME}), 400

    if not isinstance(course, str) or course.strip() == "":
        return jsonify({"error": error_msg.ERROR_COURSE}), 400

    if not isinstance(mark, int) or mark is None or mark > 100 or mark < 0:
        return jsonify({"error": error_msg.ERROR_COURSE}), 400

    app.logger.info(type(student_data))

    student_data = db.insert_student(name.strip(), course.strip(), mark)
    return jsonify(student_data), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    if student_id is None:
        app.logger.info(error_msg.ERROR_ID)
        return jsonify({"error": error_msg.ERROR_ID}), 404

    student = db.get_student_by_id(student_id)

    if student is None:
        app.logger.info(error_msg.ERROR_ID)
        return jsonify({"error": error_msg.ERROR_ID}), 404

    student_data = request.get_json(silent=True)
    if not isinstance(student_data, dict):
        return jsonify({"error": error_msg.ERROR_JSON}), 404

    # Allow partial updates: only validate fields provided.
    name = student_data.get("name", None)
    course = student_data.get("course", None)
    mark = student_data.get("mark", None)

    if not isinstance(name, str) or name.strip() == "":
        return jsonify({"error": error_msg.ERROR_NAME}), 400

    if not isinstance(course, str) or course.strip() == "":
        return jsonify({"error": error_msg.ERROR_COURSE}), 400

    # if not isinstance(mark, int) or mark is None or mark > 100 or mark < 0:
    #     return jsonify({"error": error_msg.ERROR_MARK}), 400
    # TODO: decide if we should make mark zero!
    if not isinstance(mark, int) or mark is None or mark > 100 or mark < 0:
        mark = 0
    student_data = db.update_student(student_id, name, course, mark)
    return jsonify(student_data), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student = db.get_student_by_id(student_id)
    if student is None:
        app.logger.info(error_msg.ERROR_ID)
        return jsonify({"error": error_msg.ERROR_ID}), 404

    app.logger.info(f"Student with id: {student_id} delete")
    db.delete_student(student_id)
    return jsonify(student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    # NOTE: You cant have a student with no fucking marks we made this precondition clear
    # above
    all_students = db.get_all_students()
    if len(all_students) == 0:
        return {}, 200

    marks: list[int] = [x["mark"] for x in all_students]
    num_students = len(marks)
    sum_mark = reduce(lambda a, b: a + b, marks)
    avg = sum_mark / num_students
    maxMark = max(marks)
    minMark = min(marks)

    return (
        jsonify(
            {"count": num_students, "average": avg, "min": minMark, "max": maxMark}
        ),
        200,
    )


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5000)
