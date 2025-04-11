from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    try:
        data = request.get_json()
        if not data or 'incomeData' not in data:
            return jsonify({"error": "No income data provided"}), 400

        income_data = data['incomeData']
        
        # Calculate metrics
        total_income = sum(item['totalIncome'] for item in income_data)
        average_payment = total_income / len(income_data)
        min_payment = min(item['totalIncome'] for item in income_data)
        max_payment = max(item['totalIncome'] for item in income_data)
        
        # Calculate remaining balance for each month
        remaining_balance = total_income
        schedule_data = []
        
        for item in income_data:
            payment = item['totalIncome'] - item['fixedExpenses']
            remaining_balance -= payment
            schedule_data.append({
                "date": item['date'],
                "payment": float(payment),
                "remaining_balance": float(remaining_balance)
            })
        
        schedule = {
            "metrics": {
                "total_payments": float(total_income),
                "average_payment": float(average_payment),
                "min_payment": float(min_payment),
                "max_payment": float(max_payment),
                "completion_date": income_data[-1]['date'],
                "total_months": len(income_data)
            },
            "data": schedule_data
        }
        
        return jsonify(schedule)
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return jsonify({"error": f"Error processing data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 