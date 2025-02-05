from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
import hashlib

# Flask ilovasi yaratish
app = Flask(__name__)
CORS(app)

# Firebase adminni ishga tushirish
cred = credentials.Certificate("coffe-shop-e6629-firebase-adminsdk-y6bne-c69897601b.json")
firebase_admin.initialize_app(cred)

# Firestore databasega ulanish
db = firestore.client()

# Foydalanuvchi ro'yxatdan o'tkazish
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Foydalanuvchi ma'lumotlarini olish
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not name or not surname or not email or not phone or not password:
        return jsonify({'error': 'All fields are required'}), 400

    # Parolni xavfsiz saqlash uchun hashing
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Firebase Authentication bilan foydalanuvchini yaratish
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        # Foydalanuvchi ma'lumotlarini Firestore ga saqlash
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({
            'name': name,
            'surname': surname,
            'email': email,
            'phone': phone,
            'password': hashed_password
        })

        return jsonify({'message': 'User registered successfully', 'user_id': user.uid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Foydalanuvchining profilini olish va tahrirlash
@app.route('/profile', methods=['GET', 'PUT'])
def manage_profile():
    uid = request.args.get('uid')  # User ID from query params

    if not uid:
        return jsonify({'error': 'User ID is required'}), 400

    if request.method == 'GET':
        user_ref = db.collection('users').document(uid)
        user = user_ref.get()
        if user.exists:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        phone = data.get('phone')

        if not name or not surname or not email or not phone:
            return jsonify({'error': 'All fields are required to update'}), 400

        user_ref = db.collection('users').document(uid)
        user_ref.update({
            'name': name,
            'surname': surname,
            'email': email,
            'phone': phone
        })

        return jsonify({'message': 'Profile updated successfully'}), 200

# Kurs yaratish
@app.route('/create_course', methods=['POST'])
def create_course():
    data = request.get_json()

    course_name = data.get('course_name')
    teacher_id = data.get('teacher_id')
    schedule = data.get('schedule')

    if not course_name or not teacher_id or not schedule:
        return jsonify({'error': 'Course name, teacher ID, and schedule are required'}), 400

    try:
        course_ref = db.collection('courses').document()
        course_ref.set({
            'course_name': course_name,
            'teacher_id': teacher_id,
            'schedule': schedule
        })

        return jsonify({'message': 'Course created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Kurslarni olish
@app.route('/get_courses', methods=['GET'])
def get_courses():
    try:
        courses_ref = db.collection('courses').stream()
        courses = []
        for course in courses_ref:
            courses.append(course.to_dict())
        return jsonify(courses), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Kursni yangilash
@app.route('/update_course/<course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    
    course_ref = db.collection('courses').document(course_id)
    course_ref.update(data)
    
    return jsonify({'message': 'Course updated successfully'}), 200

# Kursni o'chirish
@app.route('/delete_course/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    course_ref = db.collection('courses').document(course_id)
    course_ref.delete()
    
    return jsonify({'message': 'Course deleted successfully'}), 200

# To'lovni qabul qilish
@app.route('/payment', methods=['POST'])
def create_payment():
    data = request.get_json()

    student_id = data.get('student_id')
    course_id = data.get('course_id')
    amount = data.get('amount')
    payment_method = data.get('payment_method')

    if not student_id or not course_id or not amount or not payment_method:
        return jsonify({'error': 'Student ID, course ID, amount, and payment method are required'}), 400

    try:
        payment_ref = db.collection('payments').document()
        payment_ref.set({
            'student_id': student_id,
            'course_id': course_id,
            'amount': amount,
            'payment_method': payment_method,
            'status': 'Paid'
        })

        return jsonify({'message': 'Payment processed successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# To'lovlar ro'yxatini olish
@app.route('/get_payments', methods=['GET'])
def get_payments():
    try:
        payments_ref = db.collection('payments').stream()
        payments = []
        for payment in payments_ref:
            payments.append(payment.to_dict())
        return jsonify(payments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Flask serverni ishga tushirish
if __name__ == '__main__':
    app.run(debug=True)
