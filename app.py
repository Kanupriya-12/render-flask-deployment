from flask import Flask, request, jsonify
from openai import OpenAI
import json


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1>Kanupriya's Flask App</h1>"



def daily_calories(age, gender, height, weight, activity):
    
    activity_factors = {'sedentary' : 1.2, 'lightly_active' : 1.375, 'moderately_active' : 1.55,
                   'active' : 1.725, 'very_active' : 1.9}
    
    
    if gender == 'female':
        bmr = (10*weight) + (6.25*height) - (5*age) - 161
    else:
        bmr = (10*weight) + (6.25*height) - (5*age) + 5
    
    activity_factor = activity_factors[activity]
    bmr_final = bmr*activity_factor
    
    return bmr_final

@app.route('/get_name', methods=['GET'])
def get_name():
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    height = int(request.args.get('height'))
    weight = int(request.args.get('weight'))
    activity_level = request.args.get('activity')
    goal = request.args.get('goal')
    meal_type = request.args.get('meal_type')
    food_preference = request.args.get('food_preference')
    tdee = daily_calories(age, gender, height, weight, activity_level)
    if not age:
        return "<h1>Error: Missing 'age' parameter</h1>", 400

    return jsonify({"tdee": f"{tdee}'s Flask app"})

if __name__ == "__main__":
    app.run()