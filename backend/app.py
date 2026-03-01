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

    return db.get_all_students()


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    # Assume id increments by 1
    # Getting the request body
    if not isinstance(request.json, dict):
        return jsonify({"error": error_msg.ERROR_JSON}), 404

    student_data: dict = request.json
    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if not isinstance(name, str) or name is None:
        return jsonify({"error": error_msg.ERROR_NAME}), 400

    if not isinstance(course, str) or course is None:
        return jsonify({"error": error_msg.ERROR_COURSE}), 400

    if not isinstance(mark, int) or mark is None or mark > 100 or mark < 0:
        return jsonify({"error": error_msg.ERROR_MARK}), 400

    app.logger.info(type(student_data))

    # TODO: THIS DOES NOT CHECK IF DATA HAS DUPLICATE IN DB
    # EG SAME NAME, COURSE AND MARK
    db.insert_student(name, course, mark)
    return jsonify(student_data), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """

    student = db.get_student_by_id(student_id)
    if student is None:
        app.logger.info(error_msg.ERROR_ID)
        return jsonify({"error": error_msg.ERROR_ID}), 400

    # NOTE: The front end sends the student data in the json body.
    # ASSUME THAT this will be the case for api usage
    # DO FUCKING Error checking
    if not isinstance(request.json, dict):
        return jsonify({"error": error_msg.ERROR_JSON}), 400

    student_data: dict = request.json
    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if not isinstance(name, str) or name is None:
        return jsonify({"error": error_msg.ERROR_NAME}), 400

    if not isinstance(course, str) or course is None:
        return jsonify({"error": error_msg.ERROR_COURSE}), 400

    if not isinstance(mark, int) or mark is None or mark > 100 or mark < 0:
        return jsonify({"error": error_msg.ERROR_MARK}), 400

    db.update_student(student_id, name, course, mark)
    return student_data, 200


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
    return student, 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    # NOTE: You cant have a student with no fucking marks
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
