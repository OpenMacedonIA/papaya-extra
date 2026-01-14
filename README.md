# NeoCore Plugins Registry 🧩

Este repositorio contiene la colección de **Plugins y Extensiones** para el ecosistema NeoCore.
Estos plugins están diseñados para ser cargados dinámicamente por el sistema sin necesidad de modificar el código base.

## Instalación

Simplemente descarga el archivo `.py` del plugin que desees y colócalo en tu carpeta de extensiones:

```bash
/home/usuario/NEOPapaya/modules/extensions/
```

Reinicia NeoCore y el plugin se activará automáticamente.

## Plugins Actuales

### 1. Hello World (`hello_world.py`)
Un plugin de demostración que saluda al usuario y prueba que el sistema de inyección dinámica funciona.
*   **Comandos:** "prueba de plugin", "funciona el plugin"

### 2. Content Pack (`content.py`)
Módulo de entretenimiento y conocimiento general.
*   **Funciones:** Chistes, frases, datos curiosos, aprendizaje de alias.
*   **Comandos:** "cuéntame un chiste", "dime una frase", "sabías que", "aprende que X es Y".

## Contribuir

Para añadir tu propio plugin:
1.  Crea un archivo `.py` que herede de `BaseSkill`.
2.  Implementa la función `setup()` o `__init__`.
3.  Registra tus acciones en `core.dynamic_actions`.
4.  Haz un Pull Request a este repositorio.
