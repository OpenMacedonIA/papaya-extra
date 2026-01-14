from modules.skills import BaseSkill
import random
import os
from modules.utils import load_json_data

class ContentPlugin(BaseSkill):
    def __init__(self, core):
        super().__init__(core)
        self.chistes = []
        self.datos_curiosos = []
        self.setup()

    def setup(self):
        # 1. Cargar recursos propios (Desacoplamiento del Core)
        self.load_resources()
        
        # 2. Registrar Acciones
        self.core.dynamic_actions['plugin_contar_chiste'] = self.contar_chiste
        self.core.dynamic_actions['plugin_decir_frase'] = self.decir_frase
        self.core.dynamic_actions['plugin_contar_dato'] = self.contar_dato
        self.core.dynamic_actions['plugin_aprender_alias'] = self.aprender_alias
        self.core.dynamic_actions['plugin_consultar_dato'] = self.consultar_dato

        # 3. Registrar Intents (Hacerlo autocontenido)
        # Chistes
        self.register_intent("contar_chiste", ["cuéntame un chiste", "dime una broma", "hazme reír"], "plugin_contar_chiste")
        # Frases
        self.register_intent("decir_frase_celebre", ["dime una frase célebre", "inspírame", "cita famosa"], "plugin_decir_frase")
        # Datos
        self.register_intent("contar_dato_curioso", ["dime un dato curioso", "sabías qué", "curiosidad"], "plugin_contar_dato")
        # Alias
        self.register_intent("aprender_alias", ["aprende que", "enseñar alias"], "plugin_aprender_alias")
        # Consultar
        self.register_intent("consultar_dato", ["qué sabes de", "que sabes de", "dime qué es"], "plugin_consultar_dato")
        
        print(f"✅ [Extension] ContentPlugin cargado (Chistes: {len(self.chistes)}, Datos: {len(self.datos_curiosos)})")

    def register_intent(self, name, triggers, action):
        intent = {
            "name": name,
            "triggers": triggers,
            "action": action,
            "config": {"confidence": "high"}, # High confidence override
            "responses": ["Aquí tienes:", "Escucha esto:", "Ahí va uno:"]
        }
        self.core.intent_manager.intents.append(intent)
        for t in triggers:
            self.core.intent_manager.intent_map[t] = intent
            self.core.intent_manager.triggers_list.append(t)

    def load_resources(self):
        # Intenta cargar de resources/content, si no, usa defaults
        content_dir = "resources/content"
        self.chistes = load_json_data(os.path.join(content_dir, "chistes.json")) or [
            "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
            "¿Cómo se despide un químico? Ácido un placer."
        ]
        self.datos_curiosos = load_json_data(os.path.join(content_dir, "curiosidades.json")) or [
            "Los pulpos tienen 3 corazones.",
            "La miel nunca caduca.",
            "El 20% de la producción de energía eléctrica es de origen nuclear."
        ]

    # --- Acciones ---
    
    def contar_chiste(self, command, response, **kwargs):
        if self.chistes:
            self.speak(f"{random.choice(response) if isinstance(response, list) else response} {random.choice(self.chistes)}")
        else:
            self.speak("No me sé ningún chiste ahora mismo.")

    def decir_frase(self, command, response, **kwargs):
        frases = [
            "El conocimiento es poder.", 
            "Pienso, luego existo.", 
            "A grandes males, grandes remedios.",
            "La tecnología es un siervo útil pero un amo peligroso.",
            "No hay lugar como el 127.0.0.1"
        ]
        self.speak(f"Como dijo el sabio: {random.choice(frases)}")

    def contar_dato(self, command, response, **kwargs):
        if self.datos_curiosos:
            self.speak(f"¿Sabías que... {random.choice(self.datos_curiosos)}")
        else:
            self.speak("No tengo datos curiosos a mano.")

    def aprender_alias(self, command, response, **kwargs):
        # "aprende que X es Y"
        parts = command.split(" es ")
        if len(parts) >= 2:
            trigger = parts[0].replace("aprende que", "").strip()
            # El resto es la acción (puede contener 'es' también)
            action_cmd = " es ".join(parts[1:]).strip()
            
            if self.core.brain:
                self.core.brain.learn_alias(trigger, action_cmd)
                self.speak(f"Entendido. He aprendido que '{trigger}' equivale a '{action_cmd}'.")
            else:
                self.speak("Mi base de datos cerebral no está disponible.")
        else:
            self.speak("No entendí. Di: 'aprende que [comando nuevo] es [comando existente]'")

    def consultar_dato(self, command, response, **kwargs):
        # Heurística simple
        triggers = ["qué sabes de", "que sabes de", "dime qué es", "dime que es"]
        query = command
        for t in triggers:
            if t in query.lower():
                query = re.split(t, query, flags=re.IGNORECASE)[-1].strip()
                break
        
        # Si no se limpió bien, usar todo el comando
        if len(query) > 20 and query == command:
             # Fallback
             pass

        if self.core.brain:
            # Simulamos búsqueda, brain tiene add_fact/search_facts?
            # En NeoCore original se usaba search_facts.
            # Asumimos que la API existe.
            if hasattr(self.core.brain, 'search_facts'):
                results = self.core.brain.search_facts(query)
                if results:
                    self.speak(f"Sobre {query}: {results[0][1]}")
                else:
                    self.speak(f"No sé nada sobre {query}. ¿Qué es?")
                    self.core.waiting_for_learning = query
            else:
                self.speak("Mi cerebro no soporta búsqueda de hechos.")
        else:
            self.speak("No tengo cerebro conectado.")
