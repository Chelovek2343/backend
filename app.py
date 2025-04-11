from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS with environment variables
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, resources={
    r"/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
ALLOWED_EXTENSIONS = {'csv'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Please upload a CSV file"}), 400
    
    try:
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read and process the CSV file
        df = pd.read_csv(filepath)
        
        # Generate sample dates for the next 3 months
        start_date = datetime.now()
        dates = [(start_date + timedelta(days=30*i)).strftime('%Y-%m-%d') for i in range(3)]
        
        # Create schedule data that matches frontend expectations
        schedule = {
            "metrics": {
                "total_payments": df['Total Income'].sum(),
                "average_payment": df['Total Income'].mean(),
                "min_payment": df['Total Income'].min(),
                "max_payment": df['Total Income'].max(),
                "completion_date": df['Date'].iloc[-1],
                "total_months": len(df)
            },
            "data": [
                {
                    "date": row['Date'],
                    "payment": row['Total Income'] - row['Fixed Expenses'],
                    "remaining_balance": df['Total Income'].sum() - df['Total Income'][:i+1].sum()
                }
                for i, row in df.iterrows()
            ]
        }
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return jsonify(schedule)
        
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({"error": "Error processing file"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 