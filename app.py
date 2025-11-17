from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import skillscape

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_skills():
    try:
        data = request.get_json()
        
        if not data or 'skills' not in data:
            return jsonify({'error': 'Skills input is required'}), 400
        
        skills_input = data['skills']
        user_skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        
        if not user_skills:
            return jsonify({'error': 'No valid skills provided'}), 400
        
        # REAL ANALYSIS
        result = skillscape.analyze_user_skills(user_skills)

        # REMAP KEYS FOR FRONTEND
        formatted = {
            "all_required_skills": result.get("fitting_jobs", {}),
            "missing_1_skill": result.get("skills_missing_1", {}),
            "missing_2_skills": result.get("skills_missing_2", {}),
            "missing_3_skills": result.get("skills_missing_3", {}),
        }

        return jsonify(formatted), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("🚀 Server running at http://localhost:5000")
