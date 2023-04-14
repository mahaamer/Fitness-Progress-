import flask
import json
import math

from flask import request
app = flask.Flask("app")



def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content


# create class meal
class Meal:
        def __init__(self):
            self.id = 0
            self.type = ""
            self.name = ""
            self.fat = 0
            self.protein = 0
            self.calories = 0
            self.carbohydrates = 0

        def calc(self):
            calories = float(self.fat)*9+float(self.protein)*4+float(self.carbohydrates)*4
            return  math.ceil(calories*100)/100
        
        def add_values(self, name, type, fat, protein, carbohydrates):
            self.type = type
            self.name = name
            self.fat = fat
            self.protein = protein
            self.carbohydrates = carbohydrates
            self.calories = self.calc()
            get_data = get_meals()
            id = 0
            if len(get_data)> 0:
                for meal in get_data:
                  if meal["id"] > id:
                      id = meal["id"]
                      self.id = id + 1
            else:
                self.id = 1 

        def convert_to_jsonify(self):
            new_meal = {
            "id": len(get_meals()) + 1,
            "type": self.type,
            "name": self.name,
            "fat": self.fat,
            "protein": self.protein,
            "carbohydrates": self.carbohydrates,
            "calories": self.calories
        }
            return new_meal
        
# create class workout
class Workout:
        def __init__(self):
            self.id = 0
            self.type = ""
            self.name = ""
            self.weight= 0
            self.duration = 0
            self.calories = 0
            

        def calc(self):
            calories = (self.duration *(7.0*3.5 * float(self.weight)) / 200.0 )
            return  math.ceil(calories*100)/100
        
        def add_values_workout(self, name, type, weight,height, duration):
            self.type = type
            self.name = name
            self.duration = duration
            self.weight = weight
            self.height = height
            self.calories = self.calc()
            get_data = get_workout()
            id = 0
            if len(get_data)> 0:
                for work in get_data:
                  if work["id"] > id:
                      id = work["id"]
                      self.id = id + 1
            else:
                self.id = 1 

        def convert_to_jsonify(self):
            new_workout = {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "duration": self.duration,
            "weight": self.weight,
            "height":self.height,
            "calories": self.calories
        }
            return new_workout

# read data from meals.json
def get_meals():
    with open("meals.json") as meals_file:
        meals_data = json.load(meals_file)
        return meals_data
    
# read data from workout.json
def get_workout():
    with open("workout.json") as workout_file:
        workout_data = json.load(workout_file)
        return workout_data


# calculate calories for all meals that added
def calc_all_meals():
  all_meal = get_meals()
  result=0
  for meal in all_meal:
      result += meal["calories"]
  return math.ceil(result *100) /100
      
# calculate calories for all meals that added
def calc_all_workout():
  all_workout = get_workout()
  result=0
  for work in all_workout:
      result += work["calories"]
  return  math.ceil(result*100)/100


#Calculate Total Calories spent 
def calc_spent_calories():
    spent_calories = calc_all_meals() - calc_all_workout()
    return  math.ceil(spent_calories*100)/100


#Calculate BMI by Weight and height
def bmi():
    
    workout_data = get_workout()
    bmi = 0
    if len(workout_data) > 0:
        for workout in workout_data:
            id =  float(workout["id"])
            weight =  float(workout["weight"])
            height = float(workout["height"]) * .01

        bmi = weight / math.pow(height,2)
    return math.ceil(bmi*100)/100  



# route for home page
@app.route("/")
def homepage():
   meals_data = get_meals()
   workout_data = get_workout()
#    function of total calories
   meal_result = calc_all_meals()
   all_workout_result = calc_all_workout()

   result = ""
   workout_result = ""
#    for meals table 
   for meal in meals_data:
            result += f'''

            <tr>
            <td style="font-size: 20px">  {meal["type"]} </td> 
            <td style="font-size: 20px">{meal["name"]} </td>
              <td style="font-size: 20px"> {meal["calories"]} cal </td>
                <td><button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#{meal['id']}mealedit">
 Edit
</button>

<!-- Modal -->
<div class="modal fade" id="{meal['id']}mealedit" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel"> Edit Window</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
       </div>
      <div class="modal-body">
        <form id="edit-form" style="border: 1px solid white   background: linear-gradient(
           90deg,
           rgba(255, 248, 249, 0.4542191876750701) 0%,
           rgba(196, 178, 223, 0.5690651260504201) 59%,
           rgba(108, 114, 115, 0.5886729691876751) 100%
           ); ; height:650px" action="/edit" method="get">
        <input type="text" class="form-control" id="food_type" placeholder="Enter food id" value="{meal['id']}" hidden name="id">
       <div class="mb-3">
        <label for="food_type" class="form-label text-black" style="font-size:30px" >Food Type</label>
   

                 <select
                  class="form-control"
                  id="meal-type"
                  name="meal_type"
                  
                 
                >
                  <option  value="{meal['type']}">{meal['type']}</option>
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="snack">Snack</option>
                  <option value="dinner">Dinner</option>
                </select>
  </div>
  <div class="mb-3">
    <label for="food_name" class="form-label" style="font-size:20px">Food Name</label>
    <input type="text" class="form-control" id="food_name" placeholder="Enter food name" value="{meal['name']}" name="meal_name">
  </div>
  <div class="mb-3">
    <label for="fat" class="form-label" style="font-size:20px">Fat</label>
    <input type="number"
                    step=".1"
                    min="0" class="form-control" id="fat" placeholder="Enter fat amount" value="{meal['fat']}" name="meal_fat">
  </div>
  <div class="mb-3">
    <label for="protein" class="form-label" style="font-size:20px">Protein</label>
    <input type="number"
                    step=".1"
                    min="0" class="form-control" id="protein" placeholder="Enter protein amount" value="{meal['protein']}" name="meal_protein">
  </div>
  <div class="mb-3">
    <label for="carbohydrate" class="form-label" style="font-size:20px">Carbohydrate</label>
    <input type="number"
                    step=".1"
                    min="0" class="form-control" id="carbohydrate" placeholder="Enter carbohydrate amount" value="{meal['carbohydrates']}" name="meal_carbohydrates">
  </div>
   </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <input type="submit" class="btn btn-primary" value=" Save Changes " >
      </div>
      </form>
    </div>
  </div>
</div>
</td> 
<td>
            <form action="/delete" method="get">
            <input name="id" value="{meal["id"]}" hidden>
            <input type="submit" id="meal-delete" value=" X ">
            </form>
            </td>
</tr>'''
   
   #    for workout table 
   for work in workout_data:
            workout_result += f'''<tr><td style="font-size: 20px">  {work["type"]} </td> <td style="font-size: 20px">{work["name"]} </td> <td style="font-size: 20px"> {work["calories"]} cal </td>
            <td><button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#{work['id']}edit">
 Edit
</button>

<!-- Modal -->
<div class="modal fade" id="{work['id']}edit" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Edit Tab</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form id="edit-form" action="/workoutedit" style="border: 1px solid white   background: linear-gradient(
    90deg,
    rgba(255, 248, 249, 0.4542191876750701) 0%,
    rgba(196, 178, 223, 0.5690651260504201) 59%,
    rgba(108, 114, 115, 0.5886729691876751) 100%
  ); ; height:650px" method="get">
        <input type="text" class="form-control" id="workout_type" placeholder="Enter workout id" value="{work['id']}" hidden name="id">
  <div class="mb-3">
    <label for="workout_type" class="form-label text-black" >workout Type</label>
        <label for="workout_type"> workout type:</label>
                  <select
                    class="form-control"
                    id="work_type"
                    name="work_type"
                    
                  >
                    <option value="{work['type']}">{work['type']}</option>
                    <option value="cardio">Cardio</option>
                    <option value="strength-training">Strength Training</option>
                    <option value="flexibility">Flexibility</option>
                  </select>
  </div>
  <div class="mb-3">
    <label for="workout_name" class="form-label">workout Name</label>
    <input type="text" class="form-control" id="workout_name" placeholder="Enter workout name" value="{work['name']}" name="work_name">
  </div>
  <div class="mb-3">
    <label for="weight" class="form-label">weight</label>
    <input type="number"
                    step=".1"
                    min="0" class="form-control" id="weight" placeholder="Enter new weight" value="{work['weight']}" name="work_weight">
  </div>
  <div class="mb-3">
    <label for="height" class="form-label">Height</label>
    <input type="number"
                    step=".1"
                    min="0" class="form-control" id="height" placeholder="Enter new height" value="{work['height']}" name="work_height">
  </div>
  <div class="mb-3">
    <label for="duration" class="form-label">duration</label>
    <input type="number"
                    step=".1"
                    min="0" class="form-control" id="duration" placeholder="Enter new duration" value="{work['duration']}" name="work_duration">
  </div>
   </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <input type="submit" class="btn btn-primary" value=" Save Changes " >
      </div>
      </form>
    </div>
  </div>
</div>
</td> 
<td>
            <form action="/workoutdelete" method="get">
            <input name="id" value="{work["id"]}" hidden>
            <input type="submit" id="workout-delete" value=" X ">
            </form>
            </td>
</tr>'''        
  
   return get_html("index").replace("$$[MAHA]$$", result).replace("$$[[WORKOUT]]$$",workout_result).replace("$$[[ALLMEAL]]$$", str(meal_result)).replace("$$[[ALLWORKOUT]]$$", str(all_workout_result)).replace("$$[[BMI]]$$",str(bmi())).replace("$$[total]$$",str(calc_spent_calories()))

# route for meals submit
@app.route("/submit")
def submit():
    meals_data = get_meals()
  
            

    new_meal = Meal()
    new_meal.add_values(flask.request.args.get("meal_name"), flask.request.args.get("meal_type"), float(flask.request.args.get("meal_fats")), float(flask.request.args.get("meal_protein")), float(flask.request.args.get("carbohydrates")))
    
    meals_data.append(new_meal.convert_to_jsonify())
    with open('meals.json', 'w') as file:
        json.dump(meals_data, file, indent=1)
    file.close()
 
   
    return homepage()

# edit meal route
@app.route("/edit")
def edit():
 meals_data = get_meals()
 for meal in meals_data:
     if meal["id"]== int(flask.request.args.get("id")):
       meal["type"] = flask.request.args.get("meal_type")
       meal["name"] = flask.request.args.get("meal_name")
       meal["fat"] = float(flask.request.args.get("meal_fat"))
       meal["protein"] = float(flask.request.args.get("meal_protein"))
       meal["carbohydrates"] = float(flask.request.args.get("meal_carbohydrates"))
       meal["calories"] =  float(flask.request.args.get("meal_fat"))*9+ float(flask.request.args.get("meal_protein"))*4+ float(flask.request.args.get("meal_carbohydrates"))*4

 with open('meals.json', 'w') as file:
    json.dump(meals_data, file, indent=1)
 file.close()    
 return homepage()

# delete meal route
@app.route("/delete")
def delete():
    id = flask.request.args.get("id")
    meal_data = get_meals()
    for i in range(len(meal_data)):
        if meal_data[i]['id'] == int(id):
            del meal_data[i]
            break
    with open('meals.json', 'w') as file:
        json.dump(meal_data, file, indent=1)
    file.close() 
    return homepage()

# route for workout submit
@app.route("/workout")
def workout():
    workout_data = get_workout()
  
            

    new_workout = Workout()

    new_workout.add_values_workout(flask.request.args.get("workout_name"), flask.request.args.get("workout_type"),  float(flask.request.args.get("workout_weight")),float(flask.request.args.get("workout_height")) , float(flask.request.args.get("workout_duration")))

    
    workout_data.append(new_workout.convert_to_jsonify())
    with open('workout.json', 'w') as file:
        json.dump(workout_data, file, indent=1)
    file.close()
 
   
    return homepage()

# edit workout route
@app.route("/workoutedit")
def workout_edit():
 workout_data = get_workout()
 for work in workout_data:
     if work["id"]== int(flask.request.args.get("id")):
       work["type"] = flask.request.args.get("work_type")
       work["name"] = flask.request.args.get("work_name")
       work["weight"] = float(flask.request.args.get("work_weight"))
       work["height"] = float(flask.request.args.get("work_height"))
       work["duration"] = float(flask.request.args.get("work_duration"))
       work["calories"]= (float(flask.request.args.get("work_duration"))) *(7.0*3.5 * float(flask.request.args.get("work_weight")) / 200.0 )
 with open('workout.json', 'w') as file:
    json.dump(workout_data, file, indent=1)
 file.close()    
 return homepage()

# delete workout route
@app.route("/workoutdelete")
def workout_delete():
    id = flask.request.args.get("id")
    workout_data = get_workout()
    for i in range(len(workout_data)):
        if workout_data[i]['id'] == int(id):
            del workout_data[i]
            break
    with open('workout.json', 'w') as file:
        json.dump(workout_data, file, indent=1)
    file.close() 
    return homepage()

if __name__ == "__main__":
 app.run(debug=True)

