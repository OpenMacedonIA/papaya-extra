from modules.skills import BaseSkill
import os
import subprocess

class SysControlSkill(BaseSkill):
    def __init__(self, core):
        super().__init__(core)
        self.setup()

    def setup(self):
        # 1. Volumen
        self.register_intent("subir_volumen", ["sube el volumen", "más alto", "no oigo nada"], "vol_up")
        self.register_intent("bajar_volumen", ["baja el volumen", "más bajo", "mucho ruido"], "vol_down")
        
        # 2. Sistema
        self.register_intent("reiniciar_sistema", ["reinicia el sistema", "reboot system"], "sys_reboot")
        self.register_intent("apagar_sistema", ["apaga el sistema", "shutdown system"], "sys_shutdown")
        
        # 3. Acciones
        self.core.dynamic_actions['vol_up'] = self.volume_up
        self.core.dynamic_actions['vol_down'] = self.volume_down
        self.core.dynamic_actions['sys_reboot'] = self.reboot
        self.core.dynamic_actions['sys_shutdown'] = self.shutdown
        
        print("✅ [Extension] SysControlSkill cargado.")

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

    def volume_up(self, command, response, **kwargs):
        # Try ALSA/Pulse
        try:
            subprocess.run("amixer -D pulse sset Master 10%+", shell=True)
            self.speak("Subiendo volumen.")
        except:
            self.speak("No pude ajustar el volumen.")

    def volume_down(self, command, response, **kwargs):
        try:
            subprocess.run("amixer -D pulse sset Master 10%-", shell=True)
            self.speak("Bajando volumen.")
        except:
            self.speak("No pude ajustar el volumen.")

    def reboot(self, command, response, **kwargs):
        self.speak("Reiniciando el sistema en 3 segundos...")
        os.system("sleep 3 && sudo reboot")

    def shutdown(self, command, response, **kwargs):
        self.speak("Apagando el sistema. Hasta luego.")
        os.system("sleep 3 && sudo poweroff")
