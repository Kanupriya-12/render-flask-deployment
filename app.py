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
    prompt1 =    f"""Draft a 7-day diet plan for the following profile.
                The meal plan should have breakfast, lunch, snack, dinner. 
                Keep in mind that the meal plan is for indians. 
                You calculate daily calories using the following information:
                \n- Total Caloric Intake : {bmr_final}
                \n- goal : {goal} 
                \n - dietary preference : {food_preferences} 
                \n- cuisines to include : {preferred_cuisines}
                \n- meal preference : {meal_preference}
                \n- previous diets : {previous_diets}
                \n- nutrition deficiences : {any_nutritional_deficiences}
                \n- medication : {medication}
                
                \n Calculate the total daily calory intake based on the provided TDEE and Goal. 
                Show your detailed calculations in a json format before showing the meal plan. 
                The key for this should be 'calorie_calculation'. 
                In the calorie calculation, include the calories, protein, fat and carb intake for the day as well.
                Include the TDEE too. 
                
                \n 
        Make sure each meal is a balanced meal. This means that there should be a good mix of carbs and fiber (eg: multigrain roti), protein and fiber (eg: daal tadka,
                bhindi sabzi), fiber and micronutrients, protein and probiotics (eg: curd, raw salad).
                
                Makes sure there is also a good integration of vitamins and micro nutrients in the meals, such as Vitamin C, D, A, B, and other micronutrients. These can be added through fruits. 
                
                \nGive the 7-day diet plan in the following example json dictionary format. 
                It is crucial to make sure that the total daily protein, carbs, fat and calorie intakes in the daily plan are within the calories and gram limit every day. 
                Make sure to follow the same dictionary keys in a case senstitive manner. 
                You can give multiple items in the same meal (eg: Besan Cheela for Breakfast with Green Tea, etc). Make sure that the three main meals - Breakfast, Lunch, Dinner have more than 1 item.
                Make sure that the Evening Snack has at least a drink (eg: tea, etc).
                
                Divide calorie breakdown for the meals can be as follows:
                - Breakfast : 25-30% of daily calories
                - Lunch : 30-35% of daily calories
                - Dinner : 25-30% of daily calories
                - Morning, Mid-Day, Evening Snacks : 5-15% of daily calories 
            
                
                These three meals should also be balanced - they should have different colours and different ingredients that include a mix of protein and veggies. 
                
                Next to each meal, also indicate the "benefits" highlighting how this meal adds to a balanced diet and what micro, macro nutrients it prosesses. This helps justify why this diet plan is suitable for this specific customer. 
               
               Make the diet plan for all 7 days from Monday - Sunday.
               Provide the output strictly in JSON format. Use consistent keys and nesting structure. The JSON should look like this:
                """
    prompt2 = """ 
  {
  "meal_plan": {
    "Monday": {
      "Early Morning": {
        "Item 1": {
          "Name": "Lukewarm Fennel Seed Water",
          "Macronutrients": {
            "Calories": 5,
            "Protein": "0",
            "Carbs": "1",
            "Fats": "0"
          },
          "Ingredients": [
            "1 glass (250 ml) water",
            "1 tsp fennel seeds (soaked overnight)"
          ],
          "Recipe": "Total Time: 5 minutes. 1. Take the fennel seeds soaked overnight in 1 glass of water. 2. Strain the water into a cup. 3. Slightly warm the strained water on the stove or microwave (do not boil). 4. Drink on an empty stomach.",
          "Benefits": "Aids digestion, reduces bloating, detoxifies the body. Rich in antioxidants and contains vitamin C."
        }
      },
      "Breakfast": {
        "Item 1": {
          "Name": "1 Boiled Egg",
          "Macronutrients": {
            "Calories": 70,
            "Protein": "6",
            "Carbs": "1",
            "Fats": "5"
          },
          "Ingredients": [
            "1 egg",
            "Water for boiling"
          ],
          "Recipe": "Total Time: 12 minutes. 1. Fill a saucepan with enough water to cover the egg. 2. Bring the water to a boil on medium heat. 3. Once boiling, gently add the egg and boil for 10 minutes. 4. Remove the egg and place it in cold water for 1-2 minutes. 5. Peel and serve.",
          "Benefits": "High in protein, supports muscle growth, provides essential amino acids. Rich in vitamins B12, D, and choline."
        },
        "Item 2": {
          "Name": "1 Whole Wheat Toast with Peanut Butter",
          "Macronutrients": {
            "Calories": 150,
            "Protein": "5",
            "Carbs": "20",
            "Fats": "7"
          },
          "Ingredients": [
            "1 slice whole wheat bread",
            "1 tbsp peanut butter"
          ],
          "Recipe": "Total Time: 5 minutes. 1. Toast the bread slice in a toaster or on a hot pan until golden brown. 2. Spread 1 tbsp of peanut butter evenly on the toasted bread. 3. Serve immediately.",
          "Benefits": "Provides healthy fats and fiber for sustained energy. Rich in vitamin E, magnesium, and B vitamins."
        },
        "Item 3": {
          "Name": "Green Tea",
          "Macronutrients": {
            "Calories": 2,
            "Protein": "0",
            "Carbs": "0",
            "Fats": "0"
          },
          "Ingredients": [
            "1 cup hot water",
            "1 green tea bag"
          ],
          "Recipe": "Total Time: 5 minutes. 1. Boil water and pour it into a cup. 2. Steep the green tea bag in hot water for 3–5 minutes. 3. Remove the tea bag and serve warm.",
          "Benefits": "Boosts metabolism, supports brain function, and contains powerful antioxidants. Rich in polyphenols and vitamin C."
        },
        "Item 4": {
          "Name": "1 Small Bowl of Curd",
          "Macronutrients": {
            "Calories": 80,
            "Protein": "5",
            "Carbs": "6",
            "Fats": "4"
          },
          "Ingredients": [
            "1/2 cup curd"
          ],
          "Recipe": "Total Time: 2 minutes. 1. Serve fresh curd in a bowl as a side.",
          "Benefits": "Improves gut health with probiotics, strengthens bones, and aids digestion. Rich in calcium, vitamin B12, and riboflavin."
        }
      },
      "Mid Morning": {
        "Item 1": {
          "Name": "Apple or a Handful of Almonds",
          "Macronutrients": {
            "Calories": 150,
            "Protein": "4",
            "Carbs": "15",
            "Fats": "12"
          },
          "Ingredients": [
            "1 apple or 10 almonds"
          ],
          "Recipe": "Total Time: 3 minutes. 1. Wash the apple thoroughly and eat whole or slice into pieces. 2. If opting for almonds, eat raw or soak them overnight for better digestion.",
          "Benefits": "Provides fiber for digestion and heart health, and almonds add healthy fats. Apples are rich in vitamin C, and almonds provide vitamin E and magnesium."
        }
      },
      "Lunch": {
        "Item 1": {
          "Name": "2 Chapatis (Whole Wheat)",
          "Macronutrients": {
            "Calories": 200,
            "Protein": "6",
            "Carbs": "40",
            "Fats": "2"
          },
          "Ingredients": [
            "1/2 cup whole wheat flour",
            "Water as needed",
            "Salt to taste"
          ],
          "Recipe": "Total Time: 20 minutes. 1. In a bowl, mix flour and a pinch of salt. 2. Gradually add water and knead into a soft dough. 3. Divide into two equal balls and roll out into thin circles. 4. Cook each on a hot tawa (griddle) for about 1 minute per side until golden spots appear.",
          "Benefits": "Provides complex carbohydrates for sustained energy and aids digestion. Rich in fiber, iron, and B vitamins."
        },
        "Item 2": {
          "Name": "1 Serving of Dal (Lentils)",
          "Macronutrients": {
            "Calories": 150,
            "Protein": "10",
            "Carbs": "25",
            "Fats": "2"
          },
          "Ingredients": [
            "1/2 cup lentils",
            "1 tsp ghee",
            "Salt and spices to taste"
          ],
          "Recipe": "Total Time: 25 minutes. 1. Rinse lentils and add to a pressure cooker with 1.5 cups water, salt, and turmeric. 2. Cook for 3–4 whistles. 3. In a separate pan, heat ghee and add cumin seeds, garlic, and chili for tempering. 4. Add the tempering to the cooked dal and mix well.",
          "Benefits": "Excellent plant-based protein source, supports muscle growth, and stabilizes blood sugar. Rich in iron, folate, and B vitamins."
        },
        "Item 3": {
          "Name": "1 Cup Mixed Vegetable Curry (Low Oil)",
          "Macronutrients": {
            "Calories": 100,
            "Protein": "3",
            "Carbs": "15",
            "Fats": "4"
          },
          "Ingredients": [
            "1 cup chopped mixed vegetables (carrot, beans, peas, etc.)",
            "1 tsp oil",
            "Salt and spices to taste"
          ],
          "Recipe": "Total Time: 20 minutes. 1. Heat oil in a pan, add cumin seeds and chopped onion. 2. Sauté until golden, then add chopped vegetables. 3. Add salt, turmeric, and garam masala. 4. Cover and cook on low heat until vegetables are tender.",
          "Benefits": "Provides essential vitamins and minerals for immune health. Rich in vitamins A, C, and K, along with antioxidants."
        },
        "Item 4": {
          "Name": "Small Bowl of Curd",
          "Macronutrients": {
            "Calories": 80,
            "Protein": "5",
            "Carbs": "6",
            "Fats": "4"
          },
          "Ingredients": [
            "1/2 cup curd"
          ],
          "Recipe": "Total Time: 2 minutes. 1. Serve fresh curd in a small bowl as a side dish.",
          "Benefits": "Supports gut health and improves digestion. Rich in probiotics, calcium, and vitamin B12."
        }
        }
        }
        }
        }
           """
   

    return prompt1 + prompt2




@app.route('/get_nutrition_plan', methods=['GET'])
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


def fitness_gpt(age, gender, height, weight, activity_level, goal, equipment, workout_pref, target_zones, skill_level, struggles, time):  
    
    prompt1 = f"""You are a fitness coach that generates a 7-day personalized workout plan using only the exercises listed below. Use the provided user information to curate the most appropriate daily workouts including warm-ups, main exercises, and cooldown stretches. Tailor the intensity, duration, and progression based on the user’s profile.
    User Info:
    Age: {age}
    Gender: {gender}
    Height: {height}
    Weight: {weight}
    Activity Level: {activity_level}
    Fitness Goal: {goal}
    Available Equipment: {equipment}
    Workout Preference: {workout_pref}
    Target Zones: {target_zones}
    Skill Level: {skill_level}
    Struggles: {struggles}
    Time per day : {time}
    
    Instructions:
    Output should be in JSON format
    Keys must be "Day 1" through "Day 7"
    Each day must contain a list of 6–10 exercises as dictionaries with:
    "Name of Exercise": Name from the workout bank below.
    "Number of Reps": E.g. "12 reps", "3 sets of 10 reps"
    Avoid repeating the same exercise more than twice across the 7 days.
    If "dumbbells" are not included in equipment, exclude all dumbbell exercises.
    Always include warm-up stretches at the start of each day.
    Ensure the plan aligns with user goal, target_zones, and skill_level.
    
    Workout Bank:
    Stretches: Ankle rotations (left), Ankle rotations (right), Arm circles (backward), Arm circles (forward), Arm swings (up and down), Arm swings (open and close), 90-90 hip switches, Butterfly stretch, Calf stretch (left), Calf stretch (right), Cat cow, Child's pose, Deep squat rotations, Figure four stretch (left), Figure four stretch (right), Forearm stretch (left), Forearm stretch (right), Frog squats, Half split (left), Half split (right), Hamstring stretch (left), Hamstring stretch (right), Hip circles (clockwise), Hip circles (counter clockwise), Hip flexor stretch (left), Hip flexor stretch (right), Inch worm, Knee to chest (left), Knee to chest (right), Leg swings (left), Leg swings (right), Low lunge with revolved rotation (left), Low lunge with revolved rotation (right), Low lunge with rotation (left), Low lunge with rotation (right), Neck rotations (clockwise), Neck rotations (counter clockwise), Neck stretch (left), Neck stretch (right), Piriformis stretch (left), Piriformis stretch (right), Quad stretch (left), Quad stretch (right), Scapular push ups, Seated forward fold, Shoulder rolls (backward), Shoulder rolls (forward), Side bend (left), Side bend (right), Side to side lunges, Sideways leg swings (left), Sideways leg swings (right), Spine twist (left), Spine twist (right), Straight arm stretch (left), Straight arm stretch (right), Supine twist (right), Thread the needle (left), Thread the needle (right), Tricep stretch (left), Tricep stretch (right), Wide legged straddle, Wrist rotations (clockwise), Wrist rotations (counter clockwise)
    Bodyweight Exercises: A steps, Bear hold, Bicycles, Burpees, Butt kicks, Clamshells (left), Clamshells (right), Commando planks, Criss cross jacks, Cross body crunches (left), Cross body crunches (right), Cross body mountain climbers, Crunches, Curtsy lunges (left), Curtsy lunges (right), Curtsy lunges, Dead bugs, Donkey kicks (left), Donkey kicks (right), Donkey kicks, Fire hydrants (left), Fire hydrants (right), Fire hydrants, Forearm plank, Froggers, Glute bridges, Glute kickbacks (left), Glute kickbacks (right), Glute kickbacks, Half burpee, Heel touches, High knees, High plank, Hip lift and abduction (left), Hip lift with abductions (right), In and out squats, Jogging in place, Jumping jacks, Kick throughs, Knee push ups, Leg lifts, Lunge jumps, Marching glute bridges, Mountain climbers, Pike push ups, Plank jacks, Plank leg lifts, Pop squats, Power lunges (left), Power lunges (right), Push ups, Reverse lunges (left), Reverse lunges (right), Reverse lunges, Russian twists, Seal jacks, Shoulder taps, Side lunges (left), Side lunges (right), Side plank (left), Side plank (right), Side to side lunges, Single leg deadlifts (left), Single leg deadlifts (right), Single leg glute bridges (left), Single leg glute bridges (right), Sit ups, Skaters, Split squats (left), Split squats (right), Squat jumps, Squat pulses, Squat to lunges, Squats, Staggered squats (left), Staggered squats (right), Sumo squat pulses, Sumo squats, Surrender squats, Toe touch crunches, Tricep dips, V ups
    Dumbell: Bent over rows, Bicep Curls, Bicep to shoulder press, Chest flyes, Arnold press, Crunch to press, Curtsy lunges to lateral shoulder raises, Curtsy lunge to lateral raises (right), Curtsy Lunges (alternating), Curtsy lunges (left), Curtsy lunges (right), Curtsy lunges to lateral raises (left), Deadbugs, Deadlift to bent over row, Dumbbell Swings, External rotations, Floor chest press, Forward lunges, Front squats, Frontal shoulder raises, Glute bridges, Goblet Squat, Goblet squat jumps, Halo Circles, Hammer curls, Kneeling shoulder press, Lateral Shoulder Raises, Pendulum lunge (left), Pendulum lunges (right), Plank pull throughs, Plank T rotations (left), Plank T Rotations (right), Rainbow bicep curls, Renegade row, Reverse flyes, Reverse lunge to curls (left), Reverse Lunges (alternating), Reverse Lunges (left), Reverse Lunges (right), Reverse lunges to bicep curls, Reverse lunges to bicep curls (right), Romanian Deadlifts, Russian Twists, Shoulder Press, Shrugs, Side bends (left), Side bends (right), Side lunge (left), Side lunge (right), Side to side lunges, Single arm overhead squat (left), Single arm overhead squat (right), Single leg assisted deadlifts (left), Single leg assisted deadlifts (right), Single leg deadlifts (left), Single leg deadlifts (right), Single leg glute bridge (left), Single leg glute bridge (right), Sit up cross punches, Snatches (alternating), Split squats (left), Split squats (right), Sumo squat pulses, Sumo squats, Sumo squats to upright row, Thrusters, Tricep extensions, Upright rows, V Sit cross jab, Windmill (left), Windmill (right), Wood chop (left), Wood chop (right)

"""
    
    prompt2='Output in JSON format with keys from "Day 1" to "Day 7" : {"Name of Exercise": "Exercise Name", "Number of Reps": "X sets of Y reps", "Estimated Time":"3 minutes"}'
    
    return prompt1+prompt2


@app.route('/get_fitness_plan', methods=['GET'])
def generate_fitness_plan():

    api_key = request.args.get('api_key')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    height = int(request.args.get('height'))
    weight = int(request.args.get('weight'))
    activity_level = request.args.get('activity')
    goal = request.args.get('goal')
    equipment = request.args.get('equipment')
    workout_pref = request.args.get('workout_pref')
    skill_level = request.args.get('skill_level')
    struggles = request.args.get('struggles')
    target_zone = request.args.get('target_zone')
    time = request.args.get('time')

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
    


    prompt = fitness_gpt(age, gender, height, weight, activity_level, goal, equipment, workout_pref, target_zone, skill_level, struggles, time)



    print(prompt)

    client = OpenAI(
      api_key=api_key
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

    plan = completion.choices[0].message.content


    fitness_plan = json.loads(plan)
    
    return fitness_plan

if __name__ == "__main__":
    app.run()
