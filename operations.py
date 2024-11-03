from flask import request, jsonify, session
from init import app, db
from models import User, BankDetail

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, password_hash=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password_hash == password:
        session.permanent = True
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/bank_details', methods=['POST'])
def create_bank_detail():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    bank_name = data.get('bank_name')
    bic = data.get('bic')
    account_number = data.get('account_number')

    new_bank_detail = BankDetail(
        user_id=session['user_id'],
        bank_name=bank_name,
        bic=bic,
        account_number=account_number
    )
    db.session.add(new_bank_detail)
    db.session.commit()

    return jsonify({"message": "Bank details added successfully"}), 201

@app.route('/bank_details', methods=['GET'])
def get_bank_details():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']
    bank_details = BankDetail.query.filter_by(user_id=user_id).all()
    result = [
        {
            "id": detail.id,
            "bank_name": detail.bank_name,
            "bic": detail.bic,
            "account_number": detail.account_number,
            "is_active": detail.is_active
        }
        for detail in bank_details
    ]

    return jsonify(result), 200

@app.route('/bank_details/<int:detail_id>', methods=['PUT'])
def update_bank_detail(detail_id):
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    bank_detail = BankDetail.query.filter_by(id=detail_id, user_id=session['user_id']).first()

    if not bank_detail:
        return jsonify({"message": "Bank detail not found"}), 404

    bank_detail.bank_name = data.get('bank_name', bank_detail.bank_name)
    bank_detail.bic = data.get('bic', bank_detail.bic)
    bank_detail.account_number = data.get('account_number', bank_detail.account_number)
    db.session.commit()

    return jsonify({"message": "Bank details updated successfully"}), 200

@app.route('/bank_details/<int:detail_id>', methods=['DELETE'])
def delete_bank_detail(detail_id):
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    bank_detail = BankDetail.query.filter_by(id=detail_id, user_id=session['user_id']).first()

    if not bank_detail:
        return jsonify({"message": "Bank detail not found"}), 404

    db.session.delete(bank_detail)
    db.session.commit()

    return jsonify({"message": "Bank detail deleted successfully"}), 200

@app.route('/bank_details/<int:detail_id>/activate', methods=['PUT'])
def set_active_bank_detail(detail_id):
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    bank_detail = BankDetail.query.filter_by(id=detail_id, user_id=session['user_id']).first()
    if not bank_detail:
        return jsonify({"message": "Bank detail not found"}), 404

    BankDetail.query.filter_by(user_id=session['user_id']).update({'is_active': False})
    db.session.commit()

    bank_detail.is_active = True
    db.session.commit()

    return jsonify({"message": "Bank detail set as active"}), 200
