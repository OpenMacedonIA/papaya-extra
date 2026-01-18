from modules.skills import BaseSkill
from modules.utils import load_json_data
import json
import os
import datetime
from datetime import datetime as dt

class AlarmsSkill(BaseSkill):
    def __init__(self, core):
        super().__init__(core)
        # Use local config for portability, or shared config? 
        # Plan said: "config/alarms.json is safer". Let's stick to core config path to preserve data.
        self.data_file = "config/alarms.json" 
        self.alarms = self._load_alarms()
        self.setup()

    def setup(self):
        # Intents
        self.register_intent("crear_alarma", ["pon una alarma", "despiértame", "alarma a las"], "plugin_create_alarm")
        self.register_intent("listar_alarmas", ["qué alarmas tengo", "lista de alarmas"], "plugin_list_alarms")
        self.register_intent("borrar_alarma", ["borra la alarma", "quita la alarma"], "plugin_delete_alarm")

        # Actions
        self.core.dynamic_actions['plugin_create_alarm'] = self.create_alarm
        self.core.dynamic_actions['plugin_list_alarms'] = self.list_alarms
        self.core.dynamic_actions['plugin_delete_alarm'] = self.delete_alarm
        
        print("✅ [Extension] AlarmsSkill cargado. Escuchando 'system:tick'...")

    def on_tick(self, now):
        """Called by NeoCore every second/loop."""
        # Simple debounce or minute check to avoid spamming?
        # NeoCore loop has sleep(1), so it's roughly every second.
        # Let's check only if seconds == 0 to run logic once per minute.
        if now.second != 0:
            return

        current_time_str = now.strftime("%H:%M")
        current_date_str = now.date().isoformat()
        today_weekday = now.weekday() # 0=Monday

        dirty = False
        for alarm in self.alarms:
            # Check conditions
            is_today = (today_weekday in alarm['days_of_week']) or (len(alarm['days_of_week']) == 0) # Empty = Once/Today (implied)
            # Or handle 'days_of_week' legacy logic? 
            # Original code: if today_weekday in alarm['days_of_week']
            # Let's stick to original strict logic
            
            if today_weekday in alarm['days_of_week'] and alarm['time'] == current_time_str:
                if alarm.get('last_triggered_date') != current_date_str:
                    
                    self.speak(f"¡Din don! Son las {alarm['time']}. Alarma: {alarm['label']}")
                    
                    alarm['last_triggered_date'] = current_date_str
                    dirty = True
        
        if dirty:
            self._save_alarms()

    # --- Actions ---

    def create_alarm(self, command, response, **kwargs):
        # Simple heuristic parsing (since we removed OrganizerSkill logic from core)
        # "alarma a las 8 y media" -> "08:30"
        import re
        
        # Regex for HH:MM
        match = re.search(r'(\d{1,2})[:\s]?(\d{2})?', command)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            
            # Basic validation
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                # Default to Everyday or Today? Let's say Everyday for simplicity or ask.
                # For "One Shot":
                # days = [dt.now().weekday()] 
                # For this plugin v1, let's make it daily (0-6)
                days = list(range(7)) 
                
                self.add_alarm(hour, minute, days)
                self.speak(f"Vale, alarma puesta a las {hour:02d}:{minute:02d}.")
            else:
                 self.speak("Esa hora no existe, relojero.")
        else:
            self.speak("No entendí la hora. Di 'Alarma a las 8' por ejemplo.")

    def list_alarms(self, command, response, **kwargs):
        if not self.alarms:
            self.speak("No tienes alarmas.")
            return
            
        cnt = len(self.alarms)
        self.speak(f"Tienes {cnt} alarmas configuradas.")

    def delete_alarm(self, command, response, **kwargs):
        # Delete ALL for now or first one?
        # "Borra todas" check?
        if "todas" in command:
            self.alarms = []
            self._save_alarms()
            self.speak("Todas las alarmas borradas.")
        else:
            self.speak("Para borrar, di 'borra todas las alarmas'. Aún estoy aprendiendo a borrar una específica.")

    # --- Helpers ---

    def add_alarm(self, hour, minute, days_of_week, label="Alarma"):
        new_alarm = {
            'time': f"{hour:02d}:{minute:02d}",
            'days_of_week': days_of_week,
            'label': label,
            'last_triggered_date': None
        }
        self.alarms.append(new_alarm)
        self._save_alarms()

    def register_intent(self, name, triggers, action):
        intent = {
            "name": name,
            "triggers": triggers,
            "action": action,
            "config": {"confidence": "high"},
            "responses": []
        }
        self.core.intent_manager.intents.append(intent)
        for t in triggers:
            self.core.intent_manager.intent_map[t] = intent
            self.core.intent_manager.triggers_list.append(t)

    def _load_alarms(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_alarms(self):
        # Ensure dir
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.alarms, f, indent=4, ensure_ascii=False)
