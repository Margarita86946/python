from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)


DATA_FILE = os.path.join(os.path.dirname(__file__), 'cars.json')



def load_cars():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as file:
            file.write('[]')
    with open(DATA_FILE, 'r') as file:
        try:
            data = file.read().strip()
            return json.loads(data) if data else []
        except json.JSONDecodeError:
            print(f"Error: Failed to load {DATA_FILE}, invalid JSON format")
            return []



def save_cars(cars):
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(cars, file, indent=4)
            print(f"Successfully saved {len(cars)} cars to {DATA_FILE}")
    except Exception as e:
        print(f"Error saving to {DATA_FILE}: {e}")



@app.route('/cars', methods=['GET'])
def get_cars():
    cars = load_cars()
    return jsonify(cars), 200


@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    cars = load_cars()
    car = next((car for car in cars if car['id'] == car_id), None)
    if car is None:
        return jsonify({'error': 'Car not found'}), 404
    return jsonify(car), 200

@app.route('/cars', methods=['POST'])
def create_car():
    cars = load_cars()
    new_car = request.json


    required_fields = ['make', 'model', 'year', 'price']
    if not all(field in new_car for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if not isinstance(new_car['year'], int) or not isinstance(new_car['price'], (int, float)):
        return jsonify({'error': 'Invalid data types for year or price'}), 400

    new_id = max((car['id'] for car in cars), default=0) + 1
    new_car['id'] = new_id
    cars.append(new_car)

    try:
        save_cars(cars)
        print(f"New car added: {new_car}")
    except Exception as e:
        print(f"Failed to save car: {e}")
        return jsonify({'error': 'Failed to save the car'}), 500

    return jsonify(new_car), 201



@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    cars = load_cars()
    car = next((car for car in cars if car['id'] == car_id), None)

    if car is None:
        return jsonify({'error': 'Car not found'}), 404

    update_data = request.json
    if 'year' in update_data and not isinstance(update_data['year'], int):
        return jsonify({'error': 'Invalid data type for year'}), 400
    if 'price' in update_data and not isinstance(update_data['price'], (int, float)):
        return jsonify({'error': 'Invalid data type for price'}), 400

    car.update(update_data)

    try:
        save_cars(cars)
        print(f"Updated car: {car}")
    except Exception as e:
        print(f"Failed to update car: {e}")
        return jsonify({'error': 'Failed to update the car'}), 500

    return jsonify(car), 200



@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    cars = load_cars()
    car_index = next((index for index, car in enumerate(cars) if car['id'] == car_id), None)

    if car_index is None:
        return jsonify({'error': 'Car not found'}), 404

    deleted_car = cars.pop(car_index)

    try:
        save_cars(cars)
        print(f"Deleted car: {deleted_car}")
    except Exception as e:
        print(f"Failed to delete car: {e}")
        return jsonify({'error': 'Failed to delete the car'}), 500

    return jsonify(deleted_car), 200



@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Car API!'}), 200



@app.route('/favicon.ico')
def favicon():
    return '', 204  



if __name__ == '__main__':
    app.run(debug=True)