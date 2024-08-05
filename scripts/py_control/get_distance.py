from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variable to store distance
distance_value = None

@app.route('/upload', methods=['POST'])
def upload_string():
    global distance_value
    try:
        if 'distance' not in request.form:
            print("Checking JSON data")
            data = request.get_json()
            if not data or 'distance' not in data:
                print("Missing distance key")
                return 'Missing distance', 400
            distance_value = float(data['distance'])
        else:
            distance_value = float(request.form['distance'])
        
        if distance_value == '':
            print("Distance is empty")
            return 'Distance is empty', 400
        print("Received distance:", distance_value)
        return 'Text successfully received and sent', 200
    except ValueError:
        print("Invalid distance value received")
        return 'Invalid distance value', 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 'Internal Server Error', 500

@app.route('/get_distance', methods=['GET'])
def get_distance():
    try:
        global distance_value
        if distance_value is None:
            raise ValueError("Distance value has not been set yet")
        return jsonify({"distance": distance_value})
    except Exception as e:
        print(f"An error occurred while getting the distance: {e}")
        return jsonify({"error": str(e)}), 500

def run_distance_app():
    app.run(port=6000, host="0.0.0.0")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
