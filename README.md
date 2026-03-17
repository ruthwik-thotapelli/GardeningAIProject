🌿 Garden AI – Smart Plant Recommendation System

Garden AI is an intelligent web-based application that suggests suitable plants based on real-time weather conditions and user space constraints. It helps users choose the right plants for their environment using AI-driven logic  and live API data.

🚀 Features

🌍 Fetches real-time weather data using Open-Meteo API

🧠 Smart plant recommendations based on:

Temperature

Humidity

Weather conditions

🏡 Supports different spaces:

Balcony

Small rooms

Backyard

Custom dimensions (e.g., 3x3, 4x2)

💬 Interactive chatbot interface

⚡ Fast and lightweight Flask backend

🛠️ Tech Stack

Frontend: HTML, JavaScript

Backend: Python (Flask)

APIs: Open-Meteo (Weather + Geocoding)

Libraries: Flask, Flask-CORS, Requests

Tools: Git, GitHub

📁 Project Structure
Garden/
│── backend.py        # Flask backend (API + logic)
│── frontend.html     # UI for chatbot interaction
│── script.js         # Frontend logic (API calls)
⚙️ How It Works

User enters a location (e.g., weather in Hyderabad)

Backend fetches weather data using Open-Meteo API

Stores temperature, humidity, and weather condition

User provides space details (e.g., balcony, 3x3)

System suggests suitable plants based on conditions

▶️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/Garden-AI.git
cd Garden-AI
2. Install dependencies
pip install flask flask-cors requests
3. Run the backend server
python backend.py
4. Open frontend

Open frontend.html in your browser

💡 Example Usage

Input: weather in Bangalore

Output: Temperature, Humidity, Weather condition

Input: balcony

Output: Suggested plants like Snake Plant, Money Plant, etc.

📌 Future Enhancements

🌱 Add ML-based personalized recommendations

📱 Mobile responsive UI

☁️ Deploy on cloud (AWS / Render)

🗄️ Store user preferences using database

🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

📄 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Ruthwik Thotapelli

Aspiring Full Stack & DevOps Engineer

🔥 Pro Tip (for placement)

After uploading this README, your project will look professional + recruiter-ready 💯
