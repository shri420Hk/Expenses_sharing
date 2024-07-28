from flask import request, jsonify, Response
import csv
import io
from models import User, Expense, Split
from utils import calculate_splits, generate_balance_sheet
from database import db

def init_routes(app):
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data or 'email' not in data or 'name' not in data or 'mobile_number' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        new_user = User(
            email=data['email'],
            name=data['name'],
            mobile_number=data['mobile_number'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({'email': user.email, 'name': user.name, 'mobile_number': user.mobile_number})

    @app.route('/expenses', methods=['POST'])
    def add_expense():
        data = request.get_json()
        if not data or 'amount' not in data or 'paid_by' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
            return jsonify({'error': 'Invalid amount'}), 400

        new_expense = Expense(
            amount=data['amount'],
            description=data.get('description'),
            paid_by_user_id=data['paid_by'])
        db.session.add(new_expense)
        db.session.commit()

        if 'splits' in data:
            try:
                splits = calculate_splits(new_expense, data['splits'])
                db.session.add_all(splits)
                db.session.commit()
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        return jsonify({'message': 'Expense added successfully', 'expense_id': new_expense.id}), 201

    @app.route('/expenses/user/<int:user_id>', methods=['GET'])
    def get_user_expenses(user_id):
        expenses = Expense.query.filter_by(paid_by_user_id=user_id).all()
        return jsonify([expense.to_dict() for expense in expenses])

    @app.route('/expenses', methods=['GET'])
    def get_all_expenses():
        expenses = Expense.query.all()
        return jsonify([expense.to_dict() for expense in expenses])

    @app.route('/balance_sheet', methods=['GET'])
    def download_balance_sheet():
        balance_sheet_data = generate_balance_sheet()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['User ID', 'Balance'])
        for user_id, balance in balance_sheet_data.items():
            writer.writerow([user_id, balance])

        csv_data = output.getvalue()
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=balance_sheet.csv"})