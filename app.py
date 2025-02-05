from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, auth
import logging

# Firebase konfiguratsiyasi
cred = credentials.Certificate('coffe-shop-e6629-firebase-adminsdk-y6bne-c69897601b.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Flask ilovasini yaratish
app = Flask(__name__)

# Loglashni sozlash
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Foydalanuvchi ro'yxatdan o'tkazish
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']

        # Foydalanuvchi yaratish
        user = auth.create_user(
            email=email,
            password=password,
            display_name=f"{first_name} {last_name}",
            phone_number=phone_number
        )
        
        # Foydalanuvchi ma'lumotlarini Firebaseda saqlash
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'role': 'student'  # Yoki 'teacher' bo'lishi mumkin
        })

        app.logger.info(f"User created: {first_name} {last_name} ({email})")

        return jsonify({"message": "User created successfully!"}), 201

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Foydalanuvchi tizimga kirishi (autentifikatsiya)
@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        # Email va parol orqali foydalanuvchini tekshirish
        user = auth.get_user_by_email(email)
        # Parolni tekshirish (Firebase Admin SDK bilan amalga oshirilmaydi, front-endda qilish kerak)
        
        app.logger.info(f"User logged in: {email}")
        
        return jsonify({"message": "Login successful!"}), 200

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Kurs yaratish
@app.route('/create_course', methods=['POST'])
def create_course():
    try:
        data = request.get_json()
        course_name = data['course_name']
        teacher_id = data['teacher_id']
        schedule = data['schedule']  # Masalan, dars vaqti va joyi
        
        # Kursni Firebaseda saqlash
        course_ref = db.collection('courses').add({
            'course_name': course_name,
            'teacher_id': teacher_id,
            'schedule': schedule
        })

        app.logger.info(f"Course created: {course_name} by teacher {teacher_id}")

        return jsonify({"message": "Course created successfully!"}), 201

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Kursni yangilash
@app.route('/update_course/<course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.get_json()
        course_name = data['course_name']
        teacher_id = data['teacher_id']
        schedule = data['schedule']

        # Kursni yangilash
        course_ref = db.collection('courses').document(course_id)
        course_ref.update({
            'course_name': course_name,
            'teacher_id': teacher_id,
            'schedule': schedule
        })

        app.logger.info(f"Course updated: {course_id}")

        return jsonify({"message": "Course updated successfully!"}), 200

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Dars jadvalini yaratish
@app.route('/create_schedule', methods=['POST'])
def create_schedule():
    try:
        data = request.get_json()
        course_id = data['course_id']
        start_time = data['start_time']
        end_time = data['end_time']
        location = data['location']
        
        # Dars jadvalini Firebaseda saqlash
        schedule_ref = db.collection('schedules').add({
            'course_id': course_id,
            'start_time': start_time,
            'end_time': end_time,
            'location': location
        })

        app.logger.info(f"Schedule created for course {course_id} from {start_time} to {end_time}")

        return jsonify({"message": "Schedule created successfully!"}), 201

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

# To'lov qabul qilish
@app.route('/payment', methods=['POST'])
def handle_payment():
    try:
        data = request.get_json()
        student_id = data['student_id']
        course_id = data['course_id']
        amount = data['amount']

        # Talaba to'lovini saqlash
        payment_ref = db.collection('payments').add({
            'student_id': student_id,
            'course_id': course_id,
            'amount': amount,
            'status': 'paid'
        })

        app.logger.info(f"Payment recorded for student {student_id} for course {course_id}")

        return jsonify({"message": "Payment recorded successfully!"}), 201

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    ip_address = '127.0.0.1'
    app.logger.info(f"Running Flask server on {ip_address}:5000")
    app.run(debug=False, host=ip_address, port=5000)
