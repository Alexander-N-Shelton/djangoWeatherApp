# 🌦️ Weather Forecast Web App  

![Django Weather Forecast Web App](images/django_weather.png)

A **Django-based weather forecast web application** that provides **real-time weather updates** and **7-day forecasts** for any location. Users can enter a **city, state, and country**, and the app fetches accurate weather data, including **temperature, precipitation, wind speed, UV index, and more**.  

## 🚀 Features  

✔ **Real-time Weather Data** – Displays the current temperature, humidity, and conditions.  
✔ **7-Day Forecast** – Get a detailed outlook for the next week.  
✔ **Dynamic Weather Icons** – Animated SVG icons change based on the weather.  
✔ **Sunrise & Sunset Times** – Accurate calculations based on location.  
✔ **Location Search** – Enter any city, state, and country to fetch local weather.  
✔ **Google Geocoding API** – Converts location names into latitude/longitude.  
✔ **Open-Meteo API** – Fetches live weather data.  

## 🛠️ Technologies Used  

- **Django** – Backend framework  
- **Celery + Redis** – Background task processing  
- **Google Geocoding API** – Converts city names to coordinates  
- **Open-Meteo API** – Retrieves weather data  
- **Bootstrap + FontAwesome** – Responsive UI & icons  

## 🔧 Setup Instructions  

1. Clone the repo:

    ```bash
    git clone https://github.com/your-username/weather-app.git
    cd weather-app
    ```

2. Create a virtual environment & install dependencies:

    ```bash
    python -m venv .venv
    source .venv/bin/activate # Linux
    source .venv/Scripts/activate # Windows
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - Create a `.env` file in the project root and add:

    ```ini
    SECRET_KEY=your-django-secret-key
    GOOGLE_API_KEY=your-google-api-key
    WEATHER_API_KEY=your-weather-api-key
    ```

4. Run migrations and start the server:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

5. Start Celery (optional for automatic weather updates)

    - WARNING: If you're using an API that charges be careful when running automatic api requests.

    ```bash
    celery -A your_project_name worker --loglevel=info
    ```

### Modals with detailed info of each day's forecast

![Modal with more info on weather forecast for each day](images/django_weather_modal.png)

### Displays dynamically on small screens

![Dynamic display of Django Weather Web App on small screens](images/django_weather_small_screen.png)

### Full-screen modals for display on small screens

![Dynamic modals that cover full-page on small screens](images/django_weather_modal_small_screen.png)

## Credits

- Credit for the amazing animated icons:
[Makin-Things](https://github.com/Makin-Things/weather-icons)
