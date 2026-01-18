# NEOPapaya Extensions (Papaya Extra)

Este repositorio contiene extensiones y plugins opcionales para **NEOPapaya** (anteriormente COLEGA/NEO).
Estas extensiones añaden funcionalidades extra sin sobrecargar el núcleo (`NeoCore`).

## 🧩 Plugins Disponibles

### 1. **Alarms/Clock (`alarms.py`)** ⏰
*   **Descripción:** Gestiona alarmas y recordatorios horarios básicos.
*   **Comandos:**
    *   "Pon una alarma a las 8"
    *   "¿Qué alarmas tengo?"
    *   "Borra las alarmas"
*   **Nota:** Reemplaza la antigua lógica de alarmas hardcodeada en el Core.

### 2. **Weather (`weather.py`)** 🌦️
*   **Descripción:** Consulta el clima actual y pronóstico usando OpenMeteo (sin API Key).
*   **Comandos:**
    *   "¿Qué tiempo hace?"
    *   "Dime el clima"
    *   "Va a llover hoy"

### 3. **System Control (`sys_control.py`)** 🎛️
*   **Descripción:** Controla funciones del sistema operativo mediante voz.
*   **Comandos:**
    *   "Sube/Baja volumen"
    *   "Reinicia el sistema"
    *   "Apaga el sistema"

### 4. **Content (`content.py`)** 🎭
*   **Descripción:** Contenido de entretenimiento (chistes, frases, curiosidades).
*   **Comandos:**
    *   "Cuéntame un chiste"
    *   "Dime un dato curioso"

## 🛠️ Instalación

Estas extensiones se instalan automáticamente si respondiste "Sí" a la instalación de extensiones opcionales durante el setup de NEOPapaya.

Para instalarlas manualmente:
```bash
git submodule update --init --recursive modules/extensions
# O clonar este repo en modules/extensions
```

## ⚠️ Desarrollo
Las extensiones deben heredar de `BaseSkill` y registrar sus intenciones en `setup()`.
Si requieren tareas en segundo plano, pueden implementar el método `on_tick(self, now)`.
