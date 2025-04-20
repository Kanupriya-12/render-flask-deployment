#!/usr/bin/env python
# coding: utf-8

# In[52]:

from flask import Flask, request
import random
from openai import OpenAI
import json
import pandas as pd


# In[67]:
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/", methods=['GET'])
def home():
    return "<h1>Kanupriya's Flask App</h1>"



# age = 45
# gender = 'female'
# height = 168
# weight = 80
# activity_level = 'Lightly active'
# goal = 'lose weight'
# equipment = 'None'
# workout_pref = 'Cardio'
# target_zones = 'Glutes'
# skill_level = 'Intermediate'
# struggles = 'NA'
# time = '30 minutes'
# api_key={api_key}
# 


# ##### Enter User Details

# In[68]:


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
