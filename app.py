from flask import Flask, request
from openai import OpenAI
import json


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/", methods=['GET'])
def home():
    return "<h1>Kanupriya's Flask App</h1>"


# Calculating TDEE
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

#Obtaining Nutrition Prompt

def nutrition_gpt(bmr_final,goal,food_preferences,preferred_cuisines,meal_preference,previous_diets,any_nutritional_deficiences,medication):  
    prompt1 =    f"""Draft a 7-day diet plan from Monday to Sunday for the following profile. Keep in mind that the meal plan is for indians.  
                Calculate daily calories using the following information:
                \n- Total Daily Energy Expenditure : {bmr_final}
                \n- goal : {goal} 
                \n - dietary preference : {food_preferences} 
                \n- cuisines to include : {preferred_cuisines}
                \n- meal preference : {meal_preference}
                \n- previous diets : {previous_diets}
                \n- nutrition deficiences : {any_nutritional_deficiences}
                \n- medication : {medication}
                \n
                
Make sure each meal is a balanced meal. This means that there should be a good mix of carbs, fiber and protein. Make sure there is also a good integration of vitamins and micro nutrients in the meals, such as Vitamin C, D, A, B, and other micronutrients. These can be added through fruits. It is crucial to make sure that the total daily protein, carbs, fat and calorie intakes in the daily plan are within the calories and gram limit every day. Make sure that the Evening Snack has at least a drink (eg: tea, etc). Next to each meal, also indicate the "benefits" highlighting how this meal adds to a balanced diet and what micro, macro nutrients it prosesses.
Make the diet plan for all 7 days, the order of the days should follow from Monday - Sunday. Follow the exact order of meals from early morning to dinner in the following example. Make sure to follow the same dictionary keys in a case senstitive manner. Take the following Monday example and populate it for the remaining days. Each day should have meals in the following order - Early Morning, Breakfast, Mid Morning, Lunch, Evening Snack and Dinner. You can give multiple items in the same meal (eg: Besan Cheela for Breakfast with Green Tea, etc). Make sure that the three main meals - Breakfast, Lunch, Dinner have more than 1 item. Give multiple items in the same meal (eg: Besan Cheela for Breakfast with Green Tea, etc). Make sure that the three main meals - Breakfast, Lunch, Dinner have more than 1 item.  \n"""
    
    prompt2 = """

 {
  "meal_plan": {
  "Monday": {
    "Early Morning": {
      "Item 1": {
        "Name": "Lukewarm Fennel Seed Water",
        "Ingredients": [
          "1 glass water",
          "1 tsp fennel seeds (soaked overnight)"
        ],
        "Recipe": "1. Soak fennel seeds in water overnight. 2. Strain and drink in the morning.",
        "Macronutrients": {
          "Calories": 5,
          "Carbs": "1",
          "Fats": "0",
          "Protein": "0"
        },
        "Benefits": "Aids digestion, reduces bloating, and detoxifies the body. Rich in antioxidants and contains vitamin C."
      }
    },
    "Breakfast": {
      "Item 1": {
        "Name": "1 Boiled Egg",
        "Ingredients": [
          "1 egg"
        ],
        "Recipe": "1. Boil water and cook the egg for 10 minutes. 2. Peel and eat.",
        "Macronutrients": {
          "Calories": 70,
          "Carbs": "1",
          "Fats": "5",
          "Protein": "6"
        },
        "Benefits": "High in protein, supports muscle growth, and provides essential amino acids. Rich in vitamins B12, D, and choline."
      },
      "Item 2": {
        "Name": "1 Whole Wheat Toast with Peanut Butter",
        "Ingredients": [
          "1 slice whole wheat bread",
          "1 tbsp peanut butter"
        ],
        "Recipe": "1. Toast the bread. 2. Spread peanut butter evenly and serve.",
        "Macronutrients": {
          "Calories": 150,
          "Carbs": "20",
          "Fats": "7",
          "Protein": "5"
        },
        "Benefits": "Provides healthy fats and fiber for sustained energy. Rich in vitamin E, magnesium, and B vitamins."
      },
      "Item 3": {
        "Name": "Green Tea",
        "Ingredients": [
          "1 cup hot water",
          "1 green tea bag"
        ],
        "Recipe": "1. Steep green tea bag in hot water for 3-5 minutes. 2. Serve warm.",
        "Macronutrients": {
          "Calories": 2,
          "Carbs": "0",
          "Fats": "0",
          "Protein": "0"
        },
        "Benefits": "Boosts metabolism, supports brain function, and contains powerful antioxidants. Rich in polyphenols and vitamin C."
      }
    },
    "Mid Morning": {
      "Item 1": {
        "Name": "Apple or a Handful of Almonds",
        "Ingredients": [
          "1 apple or 10 almonds"
        ],
        "Recipe": "1. Wash the apple and eat whole or slice. 2. If almonds, eat raw or soaked.",
        "Macronutrients": {
          "Calories": 150,
          "Carbs": "15",
          "Fats": "12",
          "Protein": "4"
        },
        "Benefits": "Provides fiber for digestion and heart health, and almonds add healthy fats. Apples are rich in vitamin C, and almonds provide vitamin E and magnesium."
      }
    },
    "Lunch": {
      "Item 1": {
        "Name": "2 Chapatis (Whole Wheat)",
        "Ingredients": [
          "1/2 cup whole wheat flour",
          "Water as needed",
          "Salt to taste"
        ],
        "Recipe": "1. Knead the dough. 2. Roll into thin circles and cook on a hot tawa.",
        "Macronutrients": {
          "Calories": 200,
          "Carbs": "40",
          "Fats": "2",
          "Protein": "6"
        },
        "Benefits": "Provides complex carbohydrates for sustained energy and aids digestion. Rich in fiber, iron, and B vitamins."
      },
      "Item 2": {
        "Name": "1 Serving of Dal (Lentils)",
        "Ingredients": [
          "1/2 cup lentils",
          "1 tsp ghee",
          "Salt and spices to taste"
        ],
        "Recipe": "1. Cook lentils with water, salt, and spices. 2. Add ghee tempering.",
        "Macronutrients": {
          "Calories": 150,
          "Carbs": "25",
          "Fats": "2",
          "Protein": "10"
        },
        "Benefits": "Excellent plant-based protein source, supports muscle growth, and stabilizes blood sugar. Rich in iron, folate, and B vitamins."
      },
      "Item 3": {
        "Name": "1 Cup Mixed Vegetable Curry (Low Oil)",
        "Ingredients": [
          "1 cup mixed vegetables",
          "1 tsp oil",
          "Salt and spices to taste"
        ],
        "Recipe": "1. Heat oil, sauté vegetables with spices. 2. Cook until tender.",
        "Macronutrients": {
          "Calories": 100,
          "Carbs": "15",
          "Fats": "4",
          "Protein": "3"
        },
        "Benefits": "Provides essential vitamins and minerals for immune health. Rich in vitamins A, C, and K, along with antioxidants."
      }
    },
    "Evening Snack": {
      "Item 1": {
        "Name": "1 Cup Buttermilk",
        "Ingredients": [
          "1 cup yogurt",
          "Water",
          "Salt and spices to taste"
        ],
        "Recipe": "1. Blend yogurt with water and spices.",
        "Macronutrients": {
          "Calories": 50,
          "Carbs": "6",
          "Fats": "2",
          "Protein": "3"
        },
        "Benefits": "Aids digestion and hydration, contains probiotics. Rich in calcium and vitamin B12."
      }
    },
    "Dinner": {
      "Item 1": {
        "Name": "1 Serving of Chicken Curry (Lean)",
        "Ingredients": [
          "100g chicken breast",
          "Onion, tomatoes, ginger, garlic, and spices"
        ],
        "Recipe": "1. Cook chicken with onions, tomatoes, and spices until tender.",
        "Macronutrients": {
          "Calories": 230,
          "Carbs": "5",
          "Fats": "10",
          "Protein": "30"
        },
        "Benefits": "High in lean protein, boosts muscle repair, and contains iron. Supports immune function and is rich in B vitamins."
      },
      "Item 2": {
        "Name": "1 Cup Steamed Broccoli",
        "Ingredients": [
          "1 cup broccoli"
        ],
        "Recipe": "1. Steam broccoli until tender, but not mushy.",
        "Macronutrients": {
          "Calories": 55,
          "Carbs": "11",
          "Fats": "0",
          "Protein": "4"
        },
        "Benefits": "Rich in vitamins C and K, aids in digestion, and has anti-inflammatory properties."
      },
      "Item 3": {
        "Name": "1/2 Cup Brown Rice",
        "Ingredients": [
          "1/2 cup brown rice",
          "Water as needed"
        ],
        "Recipe": "1. Boil water and cook rice until soft.",
        "Macronutrients": {
          "Calories": 110,
          "Carbs": "23",
          "Fats": "1",
          "Protein": "3"
        },
        "Benefits": "Provides complex carbs for energy, rich in fiber and minerals, such as magnesium."
      }
    }
  }
}
}
           """
    
#     print(prompt1)
   

    return prompt1+prompt2









@app.route('/get_plan', methods=['GET'])
def get_name():
    
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    height = int(request.args.get('height'))
    weight = int(request.args.get('weight'))
    activity_level = request.args.get('activity')
    goal = request.args.get('goal')
    food_preference = request.args.get('food_preference')
    preferred_cuisines = request.args.get('preferred_cuisines')
    meal_preference = request.args.get('meal_preference')
    previous_diets = request.args.get('previous_diets')
    nutritional_deficiences = request.args.get('nutritional_deficiences')
    medication = request.args.get('medication')
    
    if not age:
        return "<h1>Error: Missing 'age' parameter</h1>", 400
    
    if not gender:
        return "<h1>Error: Missing 'gender' parameter</h1>", 400
    
    if not height:
        return "<h1>Error: Missing 'height' parameter</h1>", 400
    
    if not weight:
        return "<h1>Error: Missing 'weight' parameter</h1>", 400
    
    if not activity_level:
        return "<h1>Error: Missing 'activity' parameter</h1>", 400
    
    if not goal:
        return "<h1>Error: Missing 'goal' parameter</h1>", 400
    
    
    
    # Calculate TDEE
    tdee = daily_calories(age, gender, height, weight, activity_level)
    
    print(tdee,food_preference, preferred_cuisines, meal_preference, previous_diets, nutritional_deficiences, medication)
                                
    prompt = nutrition_gpt(tdee,goal,food_preference, 
                             preferred_cuisines, meal_preference,
                                previous_diets, nutritional_deficiences, 
                                medication)
   
    #Put prompt through OpenAI API
    client = OpenAI(
     api_key="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"
    )


    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role":"system", "content":"Provide output in valid JSON"},
          {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            }
          ]
        }
      ],
        response_format={
        "type": "json_object"
      }
    )
    
    # Load Meal Plan
   
    
    plan = completion.choices[0].message.content
    print(type(plan))
    meal_plan = json.loads(plan)['meal_plan']
    
    return meal_plan

if __name__ == "__main__":
    app.run()