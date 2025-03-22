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
    
    secret = request.args.get('secret')
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
    
    try:
   
        #Put prompt through OpenAI API
        client = OpenAI(
         api_key=secret
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
    
    except:
        meal_plan = {"Monday":{"Early Morning":{"Item 1":{"Name":"Lukewarm Fennel Seed Water","Ingredients":["1 glass water","1 tsp fennel seeds (soaked overnight)"],"Recipe":"1. Soak fennel seeds in water overnight. 2. Strain and drink in the morning.","Macronutrients":{"Calories":5,"Carbs":"1","Fats":"0","Protein":"0"},"Benefits":"Aids digestion, reduces bloating, and detoxifies the body. Rich in antioxidants and contains vitamin C."}},"Breakfast":{"Item 1":{"Name":"1 Boiled Egg","Ingredients":["1 egg"],"Recipe":"1. Boil water and cook the egg for 10 minutes. 2. Peel and eat.","Macronutrients":{"Calories":70,"Carbs":"1","Fats":"5","Protein":"6"},"Benefits":"High in protein, supports muscle growth, and provides essential amino acids. Rich in vitamins B12, D, and choline."},"Item 2":{"Name":"1 Whole Wheat Toast with Peanut Butter","Ingredients":["1 slice whole wheat bread","1 tbsp peanut butter"],"Recipe":"1. Toast the bread. 2. Spread peanut butter evenly and serve.","Macronutrients":{"Calories":150,"Carbs":"20","Fats":"7","Protein":"5"},"Benefits":"Provides healthy fats and fiber for sustained energy. Rich in vitamin E, magnesium, and B vitamins."},"Item 3":{"Name":"Green Tea","Ingredients":["1 cup hot water","1 green tea bag"],"Recipe":"1. Steep green tea bag in hot water for 3-5 minutes. 2. Serve warm.","Macronutrients":{"Calories":2,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Boosts metabolism, supports brain function, and contains powerful antioxidants. Rich in polyphenols and vitamin C."}},"Mid Morning":{"Item 1":{"Name":"Apple or a Handful of Almonds","Ingredients":["1 apple or 10 almonds"],"Recipe":"1. Wash the apple and eat whole or slice. 2. If almonds, eat raw or soaked.","Macronutrients":{"Calories":150,"Carbs":"15","Fats":"12","Protein":"4"},"Benefits":"Provides fiber for digestion and heart health, and almonds add healthy fats. Apples are rich in vitamin C, and almonds provide vitamin E and magnesium."}},"Lunch":{"Item 1":{"Name":"2 Chapatis (Whole Wheat)","Ingredients":["1/2 cup whole wheat flour","Water as needed","Salt to taste"],"Recipe":"1. Knead the dough. 2. Roll into thin circles and cook on a hot tawa.","Macronutrients":{"Calories":200,"Carbs":"40","Fats":"2","Protein":"6"},"Benefits":"Provides complex carbohydrates for sustained energy and aids digestion. Rich in fiber, iron, and B vitamins."},"Item 2":{"Name":"1 Serving of Dal (Lentils)","Ingredients":["1/2 cup lentils","1 tsp ghee","Salt and spices to taste"],"Recipe":"1. Cook lentils with water, salt, and spices. 2. Add ghee tempering.","Macronutrients":{"Calories":150,"Carbs":"25","Fats":"2","Protein":"10"},"Benefits":"Excellent plant-based protein source, supports muscle growth, and stabilizes blood sugar. Rich in iron, folate, and B vitamins."},"Item 3":{"Name":"1 Cup Mixed Vegetable Curry (Low Oil)","Ingredients":["1 cup mixed vegetables","1 tsp oil","Salt and spices to taste"],"Recipe":"1. Heat oil, saut\u00e9 vegetables with spices. 2. Cook until tender.","Macronutrients":{"Calories":100,"Carbs":"15","Fats":"4","Protein":"3"},"Benefits":"Provides essential vitamins and minerals for immune health. Rich in vitamins A, C, and K, along with antioxidants."}},"Evening Snack":{"Item 1":{"Name":"1 Cup Buttermilk","Ingredients":["1 cup yogurt","Water","Salt and spices to taste"],"Recipe":"1. Blend yogurt with water and spices.","Macronutrients":{"Calories":50,"Carbs":"6","Fats":"2","Protein":"3"},"Benefits":"Aids digestion and hydration, contains probiotics. Rich in calcium and vitamin B12."}},"Dinner":{"Item 1":{"Name":"1 Serving of Chicken Curry (Lean)","Ingredients":["100g chicken breast","Onion, tomatoes, ginger, garlic, and spices"],"Recipe":"1. Cook chicken with onions, tomatoes, and spices until tender.","Macronutrients":{"Calories":230,"Carbs":"5","Fats":"10","Protein":"30"},"Benefits":"High in lean protein, boosts muscle repair, and contains iron. Supports immune function and is rich in B vitamins."},"Item 2":{"Name":"1 Cup Steamed Broccoli","Ingredients":["1 cup broccoli"],"Recipe":"1. Steam broccoli until tender, but not mushy.","Macronutrients":{"Calories":55,"Carbs":"11","Fats":"0","Protein":"4"},"Benefits":"Rich in vitamins C and K, aids in digestion, and has anti-inflammatory properties."},"Item 3":{"Name":"1/2 Cup Brown Rice","Ingredients":["1/2 cup brown rice","Water as needed"],"Recipe":"1. Boil water and cook rice until soft.","Macronutrients":{"Calories":110,"Carbs":"23","Fats":"1","Protein":"3"},"Benefits":"Provides complex carbs for energy, rich in fiber and minerals, such as magnesium."}}},"Tuesday":{"Early Morning":{"Item 1":{"Name":"Warm Lemon Water","Ingredients":["1 glass water","Juice of 1/2 lemon"],"Recipe":"1. Mix lemon juice in warm water and drink.","Macronutrients":{"Calories":10,"Carbs":"3","Fats":"0","Protein":"0"},"Benefits":"Boosts metabolism and vitamin C intake, aids digestion and detoxification."}},"Breakfast":{"Item 1":{"Name":"Vegetable Upma","Ingredients":["1/2 cup semolina","1/2 cup mixed vegetables (carrot, peas, beans)","1 tsp oil","Spices to taste"],"Recipe":"1. Roast semolina until golden. 2. Saut\u00e9 vegetables and spices, add water, then semolina. Cook until water is absorbed.","Macronutrients":{"Calories":220,"Carbs":"35","Fats":"5","Protein":"6"},"Benefits":"Provides fiber and essential vitamins, promotes fullness."},"Item 2":{"Name":"1 Boiled Egg","Ingredients":["1 egg"],"Recipe":"1. Boil water and cook the egg for 10 minutes. 2. Peel and eat.","Macronutrients":{"Calories":70,"Carbs":"1","Fats":"5","Protein":"6"},"Benefits":"High in protein, supports muscle growth, and provides essential amino acids. Rich in vitamins B12, D, and choline."},"Item 3":{"Name":"Green Tea","Ingredients":["1 cup hot water","1 green tea bag"],"Recipe":"1. Steep green tea bag in hot water for 3-5 minutes. 2. Serve warm.","Macronutrients":{"Calories":2,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Boosts metabolism, supports brain function, and contains powerful antioxidants."}},"Mid Morning":{"Item 1":{"Name":"Banana","Ingredients":["1 ripe banana"],"Recipe":"1. Peel and eat.","Macronutrients":{"Calories":90,"Carbs":"23","Fats":"0","Protein":"1"},"Benefits":"Provides quick energy, potassium, and dietary fiber."}},"Lunch":{"Item 1":{"Name":"2 Roti (Whole Wheat)","Ingredients":["1/2 cup whole wheat flour","Water as needed"],"Recipe":"1. Knead the dough and roll into thin circles. 2. Cook on a hot tawa.","Macronutrients":{"Calories":200,"Carbs":"40","Fats":"2","Protein":"6"},"Benefits":"Provides complex carbohydrates for sustained energy. Rich in fiber."},"Item 2":{"Name":"1 Serving of Chana Masala (Chickpeas)","Ingredients":["1/2 cup chickpeas","Onion, tomato, spices"],"Recipe":"1. Cook chickpeas with onions, tomatoes, and spices.","Macronutrients":{"Calories":180,"Carbs":"30","Fats":"2","Protein":"10"},"Benefits":"Great source of plant protein and fiber. Supports muscle health and digestion."},"Item 3":{"Name":"1 Cup Raita (Yogurt with Cucumber)","Ingredients":["1 cup yogurt","1/2 cucumber","Salt and spices"],"Recipe":"1. Mix yogurt with diced cucumber and spices.","Macronutrients":{"Calories":50,"Carbs":"7","Fats":"2","Protein":"3"},"Benefits":"Contains probiotics for gut health and hydrates the body."}},"Evening Snack":{"Item 1":{"Name":"1 Cup Green Tea","Ingredients":["1 green tea bag","1 cup water"],"Recipe":"1. Steep the tea bag in hot water for 3-5 minutes.","Macronutrients":{"Calories":2,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Boosts metabolism, contains antioxidants."},"Item 2":{"Name":"2 Mathris (Baked Snack)","Ingredients":["Whole wheat flour, spices, and oil"],"Recipe":"1. Roll out dough, cut into shapes, and bake until crisp.","Macronutrients":{"Calories":150,"Carbs":"20","Fats":"4","Protein":"3"},"Benefits":"Provides a healthy crunch and fiber."}},"Dinner":{"Item 1":{"Name":"1 Serving of Fish Curry (Lean)","Ingredients":["100g fish fillet","Onion, tomatoes, spices"],"Recipe":"1. Cook fish with onions, tomatoes, and spices until tender.","Macronutrients":{"Calories":220,"Carbs":"5","Fats":"8","Protein":"30"},"Benefits":"High protein source, contains omega-3 fatty acids, supports heart health."},"Item 2":{"Name":"1 Bowl of Mixed Salad","Ingredients":["Lettuce, tomatoes, cucumber, carrots","Lemon juice, salt"],"Recipe":"1. Toss all ingredients together with lemon juice.","Macronutrients":{"Calories":40,"Carbs":"9","Fats":"0","Protein":"2"},"Benefits":"Rich in fiber, vitamins, and antioxidants."},"Item 3":{"Name":"1/2 Cup Quinoa","Ingredients":["1/2 cup quinoa","Water as needed"],"Recipe":"1. Rinse quinoa, boil it in water until soft.","Macronutrients":{"Calories":110,"Carbs":"19","Fats":"2","Protein":"4"},"Benefits":"Gluten-free, provides complete protein, and is rich in fiber and minerals."}}},"Wednesday":{"Early Morning":{"Item 1":{"Name":"Cinnamon Water","Ingredients":["1 glass water","1 tsp cinnamon powder (soaked overnight)"],"Recipe":"1. Mix soaked cinnamon in water and drink.","Macronutrients":{"Calories":10,"Carbs":"2","Fats":"0","Protein":"0"},"Benefits":"May help regulate blood sugar levels; has antioxidant properties."}},"Breakfast":{"Item 1":{"Name":"Vegetable Paratha","Ingredients":["1 whole wheat dough","Stuffed with chopped vegetables","1 tsp ghee"],"Recipe":"1. Stuff dough with veggies, roll it out, and cook in ghee.","Macronutrients":{"Calories":250,"Carbs":"40","Fats":"10","Protein":"8"},"Benefits":"Provides fiber, vitamins, and minerals from vegetables."},"Item 2":{"Name":"1 Cup Yogurt","Ingredients":["1 cup yogurt"],"Recipe":"1. Serve chilled or at room temperature.","Macronutrients":{"Calories":80,"Carbs":"10","Fats":"4","Protein":"6"},"Benefits":"Rich in probiotics and helps with digestion."},"Item 3":{"Name":"Masala Chai","Ingredients":["1 cup water","1 tea bag or loose tea","Spices (ginger, cardamom)"],"Recipe":"1. Boil water, add chai, and spices. Simmer and serve.","Macronutrients":{"Calories":50,"Carbs":"10","Fats":"2","Protein":"1"},"Benefits":"Aids digestion and contains antioxidants from tea and spices."}},"Mid Morning":{"Item 1":{"Name":"Orange","Ingredients":["1 orange"],"Recipe":"1. Peel and eat.","Macronutrients":{"Calories":60,"Carbs":"15","Fats":"0","Protein":"1"},"Benefits":"Rich in vitamin C, supports the immune system."}},"Lunch":{"Item 1":{"Name":"2 Chapatis (Whole Wheat)","Ingredients":["1/2 cup whole wheat flour","Water as needed"],"Recipe":"1. Knead and roll chapatis, cook on tawa.","Macronutrients":{"Calories":200,"Carbs":"40","Fats":"2","Protein":"6"},"Benefits":"Provides energy-boosting carbohydrates and dietary fiber."},"Item 2":{"Name":"1 Serving of Palak Paneer","Ingredients":["1 cup spinach","50g paneer","Spices"],"Recipe":"1. Cook spinach and paneer with spices until soft.","Macronutrients":{"Calories":220,"Carbs":"10","Fats":"15","Protein":"15"},"Benefits":"Rich in iron, calcium, and protein from paneer."},"Item 3":{"Name":"1 Cup Cucumber Salad","Ingredients":["1 cup cucumber","Lemon juice, salt"],"Recipe":"1. Toss cucumber with lemon juice and salt.","Macronutrients":{"Calories":15,"Carbs":"3","Fats":"0","Protein":"1"},"Benefits":"Low-calorie, hydrating, and provides vitamins."}},"Evening Snack":{"Item 1":{"Name":"1 Cup Masala Chai","Ingredients":["1 cup water","1 tea bag or loose tea","Spices and milk"],"Recipe":"1. Prepare chai with water and spices, add milk if desired.","Macronutrients":{"Calories":60,"Carbs":"10","Fats":"2","Protein":"2"},"Benefits":"Warm tea aids digestion; spices provide anti-inflammatory benefits."},"Item 2":{"Name":"Baked Samosa (1 piece)","Ingredients":["Whole wheat flour","Stuffing of vegetables"],"Recipe":"1. Stuff pastry with seasoned vegetables, bake until golden.","Macronutrients":{"Calories":120,"Carbs":"18","Fats":"4","Protein":"3"},"Benefits":"Provides energy through carbs, filling; baked version is healthier."}},"Dinner":{"Item 1":{"Name":"1 Serving of Chicken Tikka","Ingredients":["100g chicken breast","Yogurt, spices"],"Recipe":"1. Marinate chicken in yogurt and spices, grill or bake.","Macronutrients":{"Calories":230,"Carbs":"5","Fats":"9","Protein":"33"},"Benefits":"High in protein and low in fat, supports muscle maintenance."},"Item 2":{"Name":"1 Cup Mixed Veggies (Steamed)","Ingredients":["Broccoli, carrots, capsicum"],"Recipe":"1. Steam vegetables until tender.","Macronutrients":{"Calories":30,"Carbs":"6","Fats":"0","Protein":"2"},"Benefits":"Provides vitamins A, C, and K; improves digestion."},"Item 3":{"Name":"1/2 Cup Quinoa Pilaf","Ingredients":["1/2 cup quinoa","Vegetables and spices"],"Recipe":"1. Cook quinoa with water and mixed vegetables.","Macronutrients":{"Calories":110,"Carbs":"19","Fats":"2","Protein":"4"},"Benefits":"Gluten-free, high in protein and rich in fiber."}}},"Thursday":{"Early Morning":{"Item 1":{"Name":"Warm Ginger Water","Ingredients":["1 glass water","1 inch ginger (grated)"],"Recipe":"1. Boil water with ginger, strain and drink warm.","Macronutrients":{"Calories":10,"Carbs":"1","Fats":"0","Protein":"0"},"Benefits":"Aids digestion, boosts immunity, and may help reduce inflammation."}},"Breakfast":{"Item 1":{"Name":"2 Egg Whites Omelette","Ingredients":["2 egg whites","Onion, tomato, and spices"],"Recipe":"1. Whisk egg whites, cook with veggies in a non-stick pan.","Macronutrients":{"Calories":50,"Carbs":"2","Fats":"0","Protein":"11"},"Benefits":"Low in calories, high in protein, supports muscle health."},"Item 2":{"Name":"1 Slice Whole Wheat Toast","Ingredients":["1 slice of whole wheat bread"],"Recipe":"1. Toast and serve.","Macronutrients":{"Calories":70,"Carbs":"12","Fats":"1","Protein":"3"},"Benefits":"Provides fiber and helps maintain stable energy levels."},"Item 3":{"Name":"Black Tea","Ingredients":["1 cup hot water","1 tea bag"],"Recipe":"1. Steep tea bag in hot water for 3-5 minutes.","Macronutrients":{"Calories":2,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Contains antioxidants that support health and hydration."}},"Mid Morning":{"Item 1":{"Name":"Mixed Nuts (Handful)","Ingredients":["Almonds, walnuts, and cashews"],"Recipe":"1. Serve a handful as a snack.","Macronutrients":{"Calories":150,"Carbs":"8","Fats":"13","Protein":"4"},"Benefits":"Provides healthy fats, protein, and fiber for sustained energy."}},"Lunch":{"Item 1":{"Name":"2 Roti (Whole Wheat)","Ingredients":["Whole wheat flour","Water, salt"],"Recipe":"1. Knead and roll out, cook on tawa until brown.","Macronutrients":{"Calories":200,"Carbs":"40","Fats":"2","Protein":"6"},"Benefits":"Rich in fiber, provides energy; essential for a balanced diet."},"Item 2":{"Name":"1 Serving of Rajma (Kidney Beans)","Ingredients":["1/2 cup rajma","Onion, tomato, spices"],"Recipe":"1. Cook rajma with onions and spices until soft.","Macronutrients":{"Calories":200,"Carbs":"35","Fats":"2","Protein":"10"},"Benefits":"Excellent source of protein and fiber; aids digestion."},"Item 3":{"Name":"1 Bowl of Cucumber and Tomato Salad","Ingredients":["Cucumber, tomato, lemon juice"],"Recipe":"1. Toss together with lemon juice.","Macronutrients":{"Calories":20,"Carbs":"5","Fats":"0","Protein":"1"},"Benefits":"Hydrating and low-calorie, provides vitamins and minerals."}},"Evening Snack":{"Item 1":{"Name":"1 Cup Herbal Tea","Ingredients":["1 cup water","Herbal tea bag"],"Recipe":"1. Steep tea bag in hot water for a few minutes.","Macronutrients":{"Calories":0,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Aids in relaxation and has several health benefits."},"Item 2":{"Name":"1 Slice Whole Wheat Bread with Avocado","Ingredients":["1 slice whole wheat bread","1/2 avocado"],"Recipe":"1. Mash avocado on bread and season.","Macronutrients":{"Calories":150,"Carbs":"20","Fats":"7","Protein":"3"},"Benefits":"Provides healthy fats and fiber; good for heart health."}},"Dinner":{"Item 1":{"Name":"1 Serving of Methi Fish Curry","Ingredients":["100g fish fillet","Fenugreek leaves, spices"],"Recipe":"1. Cook fish with fenugreek leaves and spices.","Macronutrients":{"Calories":230,"Carbs":"5","Fats":"10","Protein":"30"},"Benefits":"High in omega-3 fatty acids and protein; good for heart health."},"Item 2":{"Name":"1 Cup Steamed Vegetables","Ingredients":["Broccoli, carrots, beans"],"Recipe":"1. Steam until tender.","Macronutrients":{"Calories":30,"Carbs":"6","Fats":"0","Protein":"2"},"Benefits":"Provides fiber and essential vitamins."},"Item 3":{"Name":"1/2 Cup Brown Rice","Ingredients":["1/2 cup brown rice","Water as needed"],"Recipe":"1. Boil and cook until soft.","Macronutrients":{"Calories":110,"Carbs":"23","Fats":"1","Protein":"3"},"Benefits":"Provides complex carbohydrates and fiber, aiding digestion."}}},"Friday":{"Early Morning":{"Item 1":{"Name":"Warm Lemon Water","Ingredients":["1 glass water","Juice of 1/2 lemon"],"Recipe":"1. Mix lemon juice in warm water and drink.","Macronutrients":{"Calories":10,"Carbs":"3","Fats":"0","Protein":"0"},"Benefits":"Boosts metabolism and vitamin C intake, aids digestion and detoxification."}},"Breakfast":{"Item 1":{"Name":"Oatmeal with Fruits","Ingredients":["1/2 cup oats","1/2 cup water","1/2 banana, chopped"],"Recipe":"1. Cook oats in water, add banana.","Macronutrients":{"Calories":150,"Carbs":"27","Fats":"3","Protein":"5"},"Benefits":"Rich in fiber for digestion; banana provides potassium."},"Item 2":{"Name":"1 boiled Egg","Ingredients":["1 egg"],"Recipe":"1. Boil water and cook the egg for 10 minutes. 2. Peel and eat.","Macronutrients":{"Calories":70,"Carbs":"1","Fats":"5","Protein":"6"},"Benefits":"High in protein, supports muscle growth, and provides essential amino acids."},"Item 3":{"Name":"Green Tea","Ingredients":["1 cup hot water","1 green tea bag"],"Recipe":"1. Steep green tea bag in hot water for 3-5 minutes.","Macronutrients":{"Calories":2,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Boosts metabolism, supports brain function, and contains powerful antioxidants."}},"Mid Morning":{"Item 1":{"Name":"Pineapple Chunks","Ingredients":["1/2 cup pineapple"],"Recipe":"1. Peel and cut into chunks.","Macronutrients":{"Calories":40,"Carbs":"10","Fats":"0","Protein":"0"},"Benefits":"Rich in vitamin C and manganese, supports digestion."}},"Lunch":{"Item 1":{"Name":"2 Whole Wheat Roti","Ingredients":["1/2 cup whole wheat flour","Water as needed"],"Recipe":"1. Knead dough, roll out, and cook on tawa.","Macronutrients":{"Calories":200,"Carbs":"40","Fats":"2","Protein":"6"},"Benefits":"Provides energy-boosting carbohydrates and dietary fiber."},"Item 2":{"Name":"1 Serving of Murgh Tikka (Chicken)","Ingredients":["100g chicken breast","Yogurt, spices"],"Recipe":"1. Marinate chicken and grill until cooked.","Macronutrients":{"Calories":230,"Carbs":"5","Fats":"9","Protein":"30"},"Benefits":"High protein meal that helps in muscle repair."},"Item 3":{"Name":"1 Cup Lentil Salad","Ingredients":["1/2 cup cooked lentils","Onion, tomato, lemon juice"],"Recipe":"1. Mix all ingredients together.","Macronutrients":{"Calories":150,"Carbs":"25","Fats":"2","Protein":"11"},"Benefits":"Rich source of plant protein; high in fiber."}},"Evening Snack":{"Item 1":{"Name":"1 Cup Masala Chai","Ingredients":["1 cup water","1 tea bag","Spices (ginger, cardamom)"],"Recipe":"1. Boil water, steep tea with spices and serve.","Macronutrients":{"Calories":50,"Carbs":"10","Fats":"2","Protein":"1"},"Benefits":"Contains antioxidants; enhances digestion and metabolism."},"Item 2":{"Name":"Roasted Chickpeas (Handful)","Ingredients":["1/2 cup chickpeas, roasted"],"Recipe":"1. Roast chickpeas until crunchy.","Macronutrients":{"Calories":150,"Carbs":"25","Fats":"5","Protein":"8"},"Benefits":"High in protein, helps with satiety."}},"Dinner":{"Item 1":{"Name":"1 Serving of Fish Curry","Ingredients":["100g fish fillet","Tomato, onion, spices"],"Recipe":"1. Cook fish in spices until done.","Macronutrients":{"Calories":230,"Carbs":"5","Fats":"10","Protein":"30"},"Benefits":"Rich in omega-3 fatty acids, high protein content."},"Item 2":{"Name":"1 Cup Steamed Green Beans","Ingredients":["1 cup green beans"],"Recipe":"1. Steam until soft.","Macronutrients":{"Calories":30,"Carbs":"6","Fats":"0","Protein":"2"},"Benefits":"Provides fiber, vitamins, and minerals."},"Item 3":{"Name":"1/2 Cup Brown Rice","Ingredients":["1/2 cup brown rice","Water as needed"],"Recipe":"1. Cook brown rice until soft.","Macronutrients":{"Calories":110,"Carbs":"23","Fats":"1","Protein":"3"},"Benefits":"Complex carbohydrates, promotes sustained energy."}}},"Saturday":{"Early Morning":{"Item 1":{"Name":"Warm Turmeric Water","Ingredients":["1 glass water","1/2 tsp turmeric powder"],"Recipe":"1. Mix turmeric in warm water and drink.","Macronutrients":{"Calories":5,"Carbs":"1","Fats":"0","Protein":"0"},"Benefits":"Anti-inflammatory properties, immunity booster."}},"Breakfast":{"Item 1":{"Name":"Pesarattu (Green Moong Dosa)","Ingredients":["1/2 cup green moong dal","Spices and salt"],"Recipe":"1. Soak moong dal overnight, grind, make dosa.","Macronutrients":{"Calories":200,"Carbs":"35","Fats":"5","Protein":"8"},"Benefits":"High in protein and fiber."},"Item 2":{"Name":"1 Bowl of Curd","Ingredients":["1 cup yogurt"],"Recipe":"1. Serve chilled or at room temperature.","Macronutrients":{"Calories":80,"Carbs":"10","Fats":"4","Protein":"6"},"Benefits":"Rich in probiotics, benefits gut health."},"Item 3":{"Name":"1 Cup Coffee","Ingredients":["1 cup water","1 tsp coffee powder"],"Recipe":"1. Boil water, add coffee powder, and serve.","Macronutrients":{"Calories":5,"Carbs":"1","Fats":"0","Protein":"0"},"Benefits":"Boosts energy and metabolism."}},"Mid Morning":{"Item 1":{"Name":"Guava","Ingredients":["1 medium guava"],"Recipe":"1. Wash and eat.","Macronutrients":{"Calories":70,"Carbs":"15","Fats":"0","Protein":"2"},"Benefits":"Rich in vitamin C and dietary fiber."}},"Lunch":{"Item 1":{"Name":"2 Whole Wheat Roti","Ingredients":["Whole wheat flour","Water and salt"],"Recipe":"1. Knead, roll, and cook on tawa.","Macronutrients":{"Calories":200,"Carbs":"40","Fats":"2","Protein":"6"},"Benefits":"Provides energy and prevents constipation."},"Item 2":{"Name":"1 Serving of Baingan Bharta","Ingredients":["1 eggplant","Onion, tomato, and spices"],"Recipe":"1. Roast eggplant, mash with spices and vegetables.","Macronutrients":{"Calories":150,"Carbs":"20","Fats":"8","Protein":"3"},"Benefits":"Rich in vitamins, minerals, and antioxidants."},"Item 3":{"Name":"1 Cup Mixed Salad","Ingredients":["Lettuce, tomato, onion"],"Recipe":"1. Toss all ingredients together.","Macronutrients":{"Calories":20,"Carbs":"4","Fats":"0","Protein":"1"},"Benefits":"Low-calorie, high in nutrients."}},"Evening Snack":{"Item 1":{"Name":"1 Cup Green Tea","Ingredients":["1 cup hot water","1 green tea bag"],"Recipe":"1. Steep green tea bag in hot water for 3-5 minutes.","Macronutrients":{"Calories":2,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Contains antioxidants; helps in weight loss."},"Item 2":{"Name":"Papadum","Ingredients":["1 papadum"],"Recipe":"1. Roast papad to crispy perfection.","Macronutrients":{"Calories":50,"Carbs":"9","Fats":"1","Protein":"2"},"Benefits":"Adds crunch, low-calorie snack option."}},"Dinner":{"Item 1":{"Name":"1 Serving of Chicken Biryani (Small)","Ingredients":["100g chicken, basmati rice, spices"],"Recipe":"1. Pressure cook ingredients together until done.","Macronutrients":{"Calories":300,"Carbs":"50","Fats":"8","Protein":"25"},"Benefits":"Balanced meal with protein, carbs, and flavor."},"Item 2":{"Name":"1 Cup Raita","Ingredients":["1 cup yogurt","Vegetables like cucumber"],"Recipe":"1. Mix yogurt with chopped vegetables.","Macronutrients":{"Calories":100,"Carbs":"8","Fats":"5","Protein":"6"},"Benefits":"Cooling side dish, helps with digestion."},"Item 3":{"Name":"1 Serving of Steamed Peas","Ingredients":["1 Cup peas"],"Recipe":"1. Steam peas until soft.","Macronutrients":{"Calories":70,"Carbs":"12","Fats":"0","Protein":"5"},"Benefits":"High in fiber. Supports digestive health."}}},"Sunday":{"Early Morning":{"Item 1":{"Name":"Warm Cinnamon Water","Ingredients":["1 glass water","1 tsp cinnamon powder"],"Recipe":"1. Mix cinnamon powder in warm water and drink.","Macronutrients":{"Calories":10,"Carbs":"2","Fats":"0","Protein":"0"},"Benefits":"May help regulate blood sugar levels; full of antioxidants."}},"Breakfast":{"Item 1":{"Name":"Masala Oats","Ingredients":["1/2 cup oats","Tomato, onion, spices"],"Recipe":"1. Cook oats; add saut\u00e9ed vegetables.","Macronutrients":{"Calories":180,"Carbs":"30","Fats":"4","Protein":"7"},"Benefits":"High in fiber, keeps you full."},"Item 2":{"Name":"1 Boiled Egg","Ingredients":["1 egg"],"Recipe":"1. Boil water and cook the egg for 10 minutes. 2. Peel and eat.","Macronutrients":{"Calories":70,"Carbs":"1","Fats":"5","Protein":"6"},"Benefits":"High in protein, supports muscle growth."},"Item 3":{"Name":"1 Cup Tea","Ingredients":["1 cup hot water","1 tea bag"],"Recipe":"1. Steep tea bag in hot water for 3-5 minutes.","Macronutrients":{"Calories":2,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Contains antioxidants and boosts metabolism."}},"Mid Morning":{"Item 1":{"Name":"Mixed Fruit Bowl","Ingredients":["Apple, banana, orange"],"Recipe":"1. Chop and mix fruits together.","Macronutrients":{"Calories":100,"Carbs":"25","Fats":"0","Protein":"1"},"Benefits":"Rich in fiber and vitamin C, great for immunity."}},"Lunch":{"Item 1":{"Name":"2 Wheat Roti","Ingredients":["Whole wheat flour","Water and salt"],"Recipe":"1. Knead, roll out, and cook on tawa.","Macronutrients":{"Calories":200,"Carbs":"40","Fats":"2","Protein":"6"},"Benefits":"Complex carbohydrates provide energy."},"Item 2":{"Name":"1 Serving of Chicken Curry","Ingredients":["100g chicken","Onion, tomato, spices"],"Recipe":"1. Cook chicken with spices until tender.","Macronutrients":{"Calories":230,"Carbs":"5","Fats":"10","Protein":"30"},"Benefits":"High protein, aids muscle recovery."},"Item 3":{"Name":"1 Bowl of Spinach Salad","Ingredients":["Spinach, cucumber, lemon juice"],"Recipe":"1. Toss together and serve fresh.","Macronutrients":{"Calories":20,"Carbs":"4","Fats":"0","Protein":"1"},"Benefits":"Low-calorie, high in vitamins and minerals."}},"Evening Snack":{"Item 1":{"Name":"1 Cup Herbal Tea","Ingredients":["1 cup water","Herbal tea bag"],"Recipe":"1. Steep herbal tea in hot water.","Macronutrients":{"Calories":0,"Carbs":"0","Fats":"0","Protein":"0"},"Benefits":"Calming effects, hydrates the body."},"Item 2":{"Name":"1 Khakra (Whole Wheat)","Ingredients":["1 khakra"],"Recipe":"1. Roast until crispy.","Macronutrients":{"Calories":50,"Carbs":"10","Fats":"1","Protein":"2"},"Benefits":"Crunchy, low calorie, and provides fiber."}},"Dinner":{"Item 1":{"Name":"1 Serving of Paneer Tikka","Ingredients":["100g paneer","Yogurt, spices"],"Recipe":"1. Marinate paneer in yogurt and spices, grill or bake.","Macronutrients":{"Calories":200,"Carbs":"5","Fats":"11","Protein":"25"},"Benefits":"High in protein and calcium, supports muscle function."},"Item 2":{"Name":"1 Cup Broccoli","Ingredients":["1 cup broccoli"],"Recipe":"1. Steam broccoli until tender.","Macronutrients":{"Calories":55,"Carbs":"11","Fats":"0","Protein":"4"},"Benefits":"Rich in vitamins C and K, helps immune function."},"Item 3":{"Name":"1/2 Cup Brown Rice","Ingredients":["1/2 cup brown rice","Water"],"Recipe":"1. Cook brown rice until soft.","Macronutrients":{"Calories":110,"Carbs":"23","Fats":"1","Protein":"3"},"Benefits":"Provides healthy carbs and fiber."}}}}
    
    return meal_plan

if __name__ == "__main__":
    app.run()