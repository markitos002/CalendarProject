# Generador de Calendario de Clases (GUI)

Este proyecto incluye `generar_calendario_gui.py`, una app sencilla en Tkinter que te permite registrar las sesiones de clase por 18 semanas a partir del lunes 18/08/2025 (lunes, martes y dos sesiones el miércoles) y exportar a Excel y opcionalmente a PDF.

Características:
- Calcula automáticamente las 18 semanas desde 2025-08-18 (debes partir en lunes).
- Marca festivos de Colombia (usa la librería `holidays`; si no está disponible, trae un fallback mínimo para 2025).
- Interfaz para escribir los contenidos de cada sesión.
- Exporta a Excel (`.xlsx`) y opcionalmente a PDF (`.pdf`).

## Requisitos

Instala dependencias (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`reportlab` es opcional; sin ella sólo Excel estará disponible. Para el selector de fecha con calendario instala también `tkcalendar` (si no, se usan combos de día/mes/año).

## Ejecutar

```powershell
python generar_calendario_gui.py
```

- Ingrese/edite el título del curso y un subtítulo (opcional).
- Llene los cuadros de texto por semana. Si un día es festivo, el cuadro aparece bloqueado con el aviso "No hay clase".
- Use "Exportar a Excel" o "Exportar a PDF" para guardar.

## Notas

- Festivos soportados por defecto (si no instalas `holidays`) para el periodo Aug–Dec 2025: 18/08, 13/10, 03/11, 17/11, 08/12.
- Puedes cambiar la fecha de inicio o el número de semanas modificando el constructor de `CalendarGUI`.
