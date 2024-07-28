from models import User, Expense, Split
from app import db

def calculate_splits(expense, split_data):
    splits = []
    split_type = split_data.get('type')
    participants = split_data.get('participants', [])

    if split_type == 'equal':
        split_amount = round(expense.amount / len(participants), 2)
        for user_id in participants:
            splits.append(Split(expense_id=expense.id, user_id=user_id, amount=split_amount))

    elif split_type == 'exact':
        total_owed = sum(amount for amount in participants.values())
        if total_owed != expense.amount:
            raise ValueError("Exact split amounts do not match the total expense amount.")
        for user_id, amount in participants.items():
            splits.append(Split(expense_id=expense.id, user_id=user_id, amount=amount))

    elif split_type == 'percentage':
        total_percentage = sum(percentage for percentage in participants.values())
        if total_percentage != 100:
            raise ValueError("Percentage split must add up to 100%.")
        for user_id, percentage in participants.items():
            amount_owed = round((percentage / 100) * expense.amount, 2)
            splits.append(Split(expense_id=expense.id, user_id=user_id, amount=amount_owed))

    else:
        raise ValueError("Invalid split type. Choose 'equal', 'exact', or 'percentage'.")

    return splits

def generate_balance_sheet():
    all_users = User.query.all()
    balance_sheet = {user.id: 0 for user in all_users}

    for split in Split.query.all():
        balance_sheet[split.user_id] -= split.amount
        balance_sheet[split.expense.paid_by_user_id] += split.amount

    return balance_sheet