from flask import Flask, render_template, request, session, redirect, url_for
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'X7pL9qT3mW8rZkY2nF6vJ5bC4xD1tN')

# API Keys (replace with your own or use environment variables)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBRX-q1Pm7plCYBibKVQU4j5TWJ6U6Pbr4')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '961bc9e0e9ca4bdcb8b8d504f9799b11')

# Store chat history
chat_history = []

def get_gemini_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": f"You are DisasterAidBot, an expert in disaster management. Provide accurate, concise solutions for disaster-related queries. Use real-time data if available. Query: {prompt}"}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error fetching response: {str(e)}"

def get_real_time_data(query):
    # Fetch weather data from Open-Meteo
    weather_url = "https://my-server.tld/v1/forecast?latitude=13.0384&longitude=80.1997&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,uv_index_clear_sky_max,uv_index_max,daylight_duration,sunshine_duration,sunset,sunrise,precipitation_probability_max,precipitation_hours,precipitation_sum,snowfall_sum,showers_sum,rain_sum,et0_fao_evapotranspiration,shortwave_radiation_sum,wind_direction_10m_dominant,wind_gusts_10m_max,wind_speed_10m_max,temperature_2m_mean,apparent_temperature_mean,cape_mean,cape_max,cape_min,cloud_cover_mean,cloud_cover_max,cloud_cover_min,dew_point_2m_mean,dew_point_2m_max,dew_point_2m_min,pressure_msl_min,pressure_msl_max,pressure_msl_mean,snowfall_water_equivalent_sum,relative_humidity_2m_min,relative_humidity_2m_max,relative_humidity_2m_mean,precipitation_probability_min,precipitation_probability_mean,leaf_wetness_probability_mean,growing_degree_days_base_0_limit_50,et0_fao_evapotranspiration_sum,surface_pressure_mean,surface_pressure_max,surface_pressure_min,updraft_max,visibility_mean,visibility_min,visibility_max,winddirection_10m_dominant,wind_gusts_10m_mean,wind_speed_10m_mean,wind_gusts_10m_min,wind_speed_10m_min,wet_bulb_temperature_2m_mean,wet_bulb_temperature_2m_max,wet_bulb_temperature_2m_min,vapour_pressure_deficit_max&hourly=temperature_2m,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,evapotranspiration,et0_fao_evapotranspiration,temperature_180m,temperature_120m,temperature_80m,wind_gusts_10m,wind_direction_180m,wind_direction_120m,wind_direction_80m,wind_direction_10m,wind_speed_180m,wind_speed_120m,wind_speed_80m,wind_speed_10m,vapour_pressure_deficit,soil_moisture_27_to_81cm,soil_moisture_9_to_27cm,soil_moisture_3_to_9cm,soil_moisture_1_to_3cm,soil_moisture_0_to_1cm,soil_temperature_54cm,soil_temperature_18cm,soil_temperature_6cm,soil_temperature_0cm,snow_depth,snowfall,showers,rain,precipitation,precipitation_probability,apparent_temperature,dew_point_2m,relative_humidity_2m,uv_index,uv_index_clear_sky,is_day,sunshine_duration,wet_bulb_temperature_2m,total_column_integrated_water_vapour,boundary_layer_height,freezing_level_height,convective_inhibition,lifted_index,cape,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,terrestrial_radiation_instant,global_tilted_irradiance_instant,direct_normal_irradiance_instant,diffuse_radiation_instant,direct_radiation_instant,shortwave_radiation_instant,temperature_1000hPa,temperature_925hPa,temperature_800hPa,temperature_500hPa,temperature_250hPa,temperature_100hPa,temperature_30hPa,temperature_70hPa,temperature_200hPa,temperature_400hPa,temperature_700hPa,temperature_900hPa,temperature_975hPa,temperature_50hPa,temperature_150hPa,temperature_300hPa,temperature_600hPa,temperature_850hPa,temperature_950hPa,relative_humidity_1000hPa,relative_humidity_925hPa,relative_humidity_800hPa,relative_humidity_500hPa,relative_humidity_250hPa,relative_humidity_100hPa,relative_humidity_30hPa,relative_humidity_70hPa,relative_humidity_200hPa,relative_humidity_400hPa,relative_humidity_700hPa,relative_humidity_900hPa,relative_humidity_975hPa,relative_humidity_50hPa,relative_humidity_150hPa,relative_humidity_300hPa,relative_humidity_600hPa,relative_humidity_850hPa,relative_humidity_950hPa,cloud_cover_30hPa,cloud_cover_100hPa,cloud_cover_250hPa,cloud_cover_500hPa,cloud_cover_800hPa,cloud_cover_925hPa,cloud_cover_1000hPa,cloud_cover_70hPa,cloud_cover_200hPa,cloud_cover_400hPa,cloud_cover_700hPa,cloud_cover_900hPa,cloud_cover_975hPa,cloud_cover_50hPa,cloud_cover_150hPa,cloud_cover_300hPa,cloud_cover_600hPa,cloud_cover_850hPa,cloud_cover_950hPa,wind_speed_1000hPa,wind_speed_925hPa,wind_speed_800hPa,wind_speed_500hPa,wind_speed_250hPa,wind_speed_100hPa,wind_speed_30hPa,wind_speed_70hPa,wind_speed_200hPa,wind_speed_400hPa,wind_speed_700hPa,wind_speed_900hPa,wind_speed_975hPa,wind_speed_50hPa,wind_speed_300hPa,wind_speed_150hPa,wind_speed_600hPa,wind_speed_850hPa,wind_speed_950hPa,wind_direction_100hPa,wind_direction_30hPa,wind_direction_250hPa,wind_direction_500hPa,wind_direction_800hPa,wind_direction_925hPa,wind_direction_1000hPa,wind_direction_70hPa,wind_direction_200hPa,wind_direction_400hPa,wind_direction_700hPa,wind_direction_900hPa,wind_direction_975hPa,wind_direction_150hPa,wind_direction_50hPa,wind_direction_300hPa,wind_direction_600hPa,wind_direction_850hPa,wind_direction_950hPa,geopotential_height_30hPa,geopotential_height_100hPa,geopotential_height_250hPa,geopotential_height_500hPa,geopotential_height_800hPa,geopotential_height_925hPa,geopotential_height_1000hPa,geopotential_height_70hPa,geopotential_height_200hPa,geopotential_height_400hPa,geopotential_height_700hPa,geopotential_height_900hPa,geopotential_height_975hPa,geopotential_height_50hPa,geopotential_height_150hPa,geopotential_height_300hPa,geopotential_height_600hPa,geopotential_height_850hPa,geopotential_height_950hPa&models=best_match,ecmwf_ifs025,ecmwf_aifs025_single,bom_access_global,cma_grapes_global,icon_seamless,icon_eu,icon_d2,icon_global,metno_seamless,metno_nordic,gem_hrdps_continental,gem_regional,gem_global,gem_seamless,ncep_nbm_conus,gfs_hrrr,gfs_global,gfs_seamless,gfs_graphcast025,jma_seamless,jma_msm,jma_gsm,kma_gdps,kma_ldps,kma_seamless,meteofrance_arpege_world,meteofrance_seamless,meteofrance_arpege_europe,meteofrance_arome_france,meteofrance_arome_france_hd,ukmo_seamless,ukmo_global_deterministic_10km,ukmo_uk_deterministic_2km,knmi_seamless,knmi_harmonie_arome_europe,knmi_harmonie_arome_netherlands,dmi_seamless,dmi_harmonie_arome_europe&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,snowfall,showers,rain,precipitation,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&timezone=America%2FNew_York&latitude=13.0384&longitude=80.1997"
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()['current_weather']
    except:
        weather_data = "Weather data unavailable."

    # Fetch disaster news from NewsAPI
    news_url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}"
    try:
        news_response = requests.get(news_url)
        news_response.raise_for_status()
        news_articles = news_response.json()['articles'][:3]
        news_summary = "\n".join([f"- {article['title']} ({article['source']['name']})" for article in news_articles])
    except:
        news_summary = "News data unavailable."

    return f"Weather: {weather_data}\nRecent News:\n{news_summary}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Temporary credentials
    TEMP_USERNAME = "tempuser"
    TEMP_PASSWORD = "temppass123"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == TEMP_USERNAME and password == TEMP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_input = request.form['message']
        real_time_info = get_real_time_data(user_input)
        full_prompt = f"{user_input}\nReal-time info: {real_time_info}"
        NIGGA_response = get_gemini_response(full_prompt)
        chat_history.append({'user': user_input, 'bot': NIGGA_response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return render_template('chat.html', history=chat_history)
    
    return render_template('chat.html', history=chat_history)

@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('history.html', history=chat_history)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
