from modules.BlueberrySkills import BaseSkill

class HelloWorldSkill(BaseSkill):
    def __init__(self, core):
        super().__init__(core)
        self.register_skill()

    def register_skill(self):
        # 1. Definir la acción (función)
        # Esto permite que NeoCore ejecute 'self.say_hello' cuando se llame a 'custom_hello_world'
        self.core.dynamic_actions['custom_hello_world'] = self.say_hello
        
        # 2. Inyección dinámica de intents (NLP)
        new_intent = {
            "name": "hello_world_plugin",
            "triggers": ["prueba de plugin", "funciona el plugin", "test extension", "di hola mundo"],
            "action": "custom_hello_world", # Debe coincidir con la clave en dynamic_actions
            "responses": [] # Dejamos vacío para que la acción decida qué decir
        }
        
        # Registrar en IntentManager
        self.core.intent_manager.intents.append(new_intent)
        for trigger in new_intent['triggers']:
            self.core.intent_manager.intent_map[trigger] = new_intent
            self.core.intent_manager.triggers_list.append(trigger)
            
        print("✅ [Plugin] HelloWorldSkill registrado: Acciones y NLP inyectados.")

    def say_hello(self, command, response, **kwargs):
        """Esta es la función que ejecuta la lógica real."""
        import random
        saludos = [
            "¡Hola mundo! Soy un plugin cargado dinámicamente.",
            "¡Funciona! El sistema de extensiones está operativo.",
            "Saludos desde el archivo hello_world.py externo."
        ]
        text = random.choice(saludos)
        self.speak(text)
