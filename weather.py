from modules.skills import BaseSkill
import requests
import json
from datetime import datetime

class WeatherSkill(BaseSkill):
    def __init__(self, core):
        super().__init__(core)
        self.setup()

    def setup(self):
        # Intents
        self.register_intent("clima_actual", 
                             ["qué tiempo hace", "dime el clima", "temperatura actual", "va a llover"], 
                             "plugin_weather_now")
        
        # Actions
        self.core.dynamic_actions['plugin_weather_now'] = self.get_weather 
        print("✅ [Extension] WeatherSkill cargado.")

    def register_intent(self, name, triggers, action):
        intent = {
            "name": name,
            "triggers": triggers,
            "action": action,
            "config": {"confidence": "medium"},
            "responses": []
        }
        self.core.intent_manager.intents.append(intent)
        for t in triggers:
            self.core.intent_manager.intent_map[t] = intent
            self.core.intent_manager.triggers_list.append(t)

    def get_weather(self, command, response, **kwargs):
        self.speak("Consultando satélites meteorológicos...")
        
        # Default Location: Madrid (TODO: Get from config or IP)
        lat = 40.4168
        lon = -3.7038
        
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m&hourly=temperature_2m&daily=precipitation_sum&timezone=Europe%2FMadrid"
            res = requests.get(url, timeout=5)
            data = res.json()
            
            if 'current' in data:
                temp = data['current']['temperature_2m']
                wind = data['current']['wind_speed_10m']
                code = data['current']['weather_code']
                
                # Simple code map
                condition = "despejado"
                if code > 2: condition = "nublado"
                if code > 50: condition = "lluvioso"
                if code > 70: condition = "nevando"
                
                msg = f"Ahora mismo hay {temp} grados y está {condition}. Viento de {wind} kilómetros por hora."
                
                # Check for rain today
                if 'daily' in data and 'precipitation_sum' in data['daily']:
                    rain_sum = data['daily']['precipitation_sum'][0]
                    if rain_sum > 0:
                        msg += f" Se espera una precipitación de {rain_sum} milímetros hoy."
                    else:
                        msg += " No se esperan lluvias hoy."
                
                self.speak(msg)
            else:
                self.speak("No he podido obtener datos del servidor de clima.")
                
        except Exception as e:
            print(f"Weather Error: {e}")
            self.speak("Error conectando con el servicio meteorológico.")
