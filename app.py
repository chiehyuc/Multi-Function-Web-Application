from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bmi(weight, height, weight_unit, height_unit):
    if weight_unit == 'kg':
        weight = float(weight)
        if height_unit == 'cm':
            height = float(height) / 100  # Convert height from cm to meters
        elif height_unit == 'ft.inches':
            height = (float(height) * 30.48) / 100
            # height = float(height) * 0.0254
    elif weight_unit == 'lbs':
        weight = float(weight) * 0.453592  # Convert weight from lbs to kg
        # height = float(height) * 0.0254    # Convert height from inches to meters
        if height_unit == 'cm':
            height = float(height) / 100  # Convert height from cm to meters
        elif height_unit == 'ft.inches':
            # feet, inches = height.split('.')
            height = (float(height) * 30.48) / 100
            # height = float(height) * 0.0254
    else:
        return None
    
    bmi = round(weight / (height ** 2), 2)
    min_target_weight = round(18.5 * (height ** 2), 2)
    max_target_weight = round(24.9 * (height ** 2), 2)
    
    return bmi, (min_target_weight, max_target_weight)


def calculate_water_intake(weight, bottle_size, unit, bottle_unit):
    if bottle_unit == 'ml' or unit == 'cc':
        if unit == 'kg':
            water_intake = float(weight) * 0.033 * 1000 / float(bottle_size)
        elif unit == 'lbs':
            weight = float(weight) * 0.45359237
            water_intake = float(weight) * 0.033 * 1000 / float(bottle_size)
    elif bottle_unit == 'l':
        if unit == 'kg':
            water_intake = float(weight) * 0.033 / float(bottle_size)
        elif unit == 'lbs':
            weight = float(weight) * 0.45359237
            water_intake = float(weight) * 0.033 / float(bottle_size)
    elif bottle_unit == 'oz':
        if unit == 'kg':
            water_intake = float(weight) * 0.033 * 33.814/ float(bottle_size)
        elif unit == 'lbs':
            weight = float(weight) * 0.45359237
            water_intake = float(weight) * 0.033 * 33.814 / float(bottle_size)
    else:
        return None
    water_intake = round(water_intake + 0.4)
    return water_intake


def check_blood_pressure(systolic, diastolic):
    pressure_result = ""
    if int(systolic) < 120 and int(diastolic) < 80:
         if ((int(systolic) >= 90) and (int(diastolic)  >= 60)):
            pressure_result = "Your blood pressure is normal."
            return pressure_result
         else:
             pressure_result = "Your blood pressure is lower than normal. Please seek medical advice for more information."
             return pressure_result
    elif 120 <= int(systolic) < 129 and int(diastolic)  < 80:
        pressure_result = "Your blood pressure is elevated. You are at risk but is not yet considered to have hypertension. Please seek medical advice for more information."
        return pressure_result
    elif int(systolic) >= 130 or int(diastolic)  >= 80:
        pressure_result = "Your blood pressure is higher than normal, you are highly likely to have hypertension. Please seek medical advice for more information."
        return pressure_result




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        program_choice = request.form['program_choice']
        if program_choice == 'bmi':
            return render_template('bmi.html')
        elif program_choice == 'blood_pressure':
            return render_template('blood_pressure.html')
        elif program_choice == 'water_intake':
            return render_template('water_intake.html')
    return render_template('index.html')

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi_result():
    weight = request.form['weight']
    weight_unit = request.form['weight_unit']
    height = request.form['height']
    height_unit = request.form['height_unit']

    bmi, target_weight_range = calculate_bmi(weight, height, weight_unit, height_unit)
    if bmi is None or target_weight_range is None:
        return render_template('bmi.html', error='Invalid unit')
    
    min_target_weight, max_target_weight = target_weight_range
    return render_template('bmi_result.html', bmi=bmi, min_target_weight=min_target_weight, max_target_weight=max_target_weight)




@app.route('/calculate_water_intake', methods=['POST'])
def calculate_water_intake_result():
    weight = request.form['weight']
    unit = request.form['unit']
    bottle_size = request.form['bottle_size']
    bottle_unit = request.form['bottle_unit']
    
    water_intake = calculate_water_intake(weight, bottle_size, unit, bottle_unit)
    if water_intake is None:
        return render_template('water_intake.html', error='Invalid unit')
    
    return render_template('water_intake_result.html', water_intake=water_intake)


@app.route('/check_blood_pressure', methods=['POST'])
def check_blood_pressure_result():
    systolic = request.form['systolic']
    diastolic = request.form['diastolic']
    
    pressure_result = check_blood_pressure(systolic, diastolic)

    return render_template('blood_pressure_result.html', pressure_result=pressure_result)



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port = '8080', debug=True)
    app.run(debug=True)
