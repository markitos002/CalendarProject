# Generador de Calendario de Clases — Documentación

Este proyecto proporciona una aplicación de escritorio (Tkinter) para planear y exportar un calendario de clases por semanas, con soporte para festivos de Colombia, marcadores de exámenes y exportación a Excel/PDF. Además, guarda automáticamente un respaldo de tus entradas para precargarlas al abrir de nuevo la aplicación.

## Características principales
- Selección de fecha de inicio (debe ser lunes) y número de semanas (por defecto 18).
- Días soportados: Lunes, Martes, Miércoles (2 sesiones en Miércoles).
- Detección de festivos en Colombia (biblioteca `holidays`) con fallback mínimo para 2025 (Ago–Dic).
- Marcación de hasta 8 fechas de exámenes (con resaltado en exportaciones y etiqueta en la grilla).
- Exportación a:
  - Excel (.xlsx) con estilos, encabezados semanales y resaltados.
  - PDF (.pdf) en disposición apaisada con tablas por semana y resaltados.
- Respaldo automático de entradas en `calendario_backup.json` y precarga al iniciar.

## Archivos relevantes
- `generar_calendario_gui.py`: Aplicación principal (GUI + lógica + exportaciones).
- `calendario_backup.json`: Respaldo automático de datos (se genera/actualiza al usar la app).
- `test.xlsx` (opcional): Archivo de ejemplo de pruebas previas.

## Requisitos
- Python 3.10+
- Dependencias:
  - Requeridas: `openpyxl`, `holidays`
  - Opcionales: `reportlab` (PDF), `tkcalendar` (selector de fecha)

Instalación recomendada (PowerShell):
```powershell
pip install openpyxl holidays
# Opcionales
pip install reportlab tkcalendar
```

## Cómo ejecutar
Desde la carpeta del proyecto:
```powershell
python generar_calendario_gui.py
```

## Flujo de uso
1. Define Título/Subtítulo.
2. Elige la fecha de inicio (lunes) y el número de semanas; pulsa “Actualizar calendario”.
3. (Opcional) Registra hasta 8 fechas de exámenes.
4. Completa el contenido por semana/día en la grilla:
   - Si un día es festivo, la celda aparece bloqueada con “No hay clase”.
   - Si un día coincide con un examen, la celda muestra “Examen” (puedes añadir notas).
5. Exporta a Excel o PDF con los botones inferiores.
6. Cierra la aplicación; se guardará un respaldo automático.

## Persistencia (Respaldo)
- Archivo: `calendario_backup.json` (junto a `generar_calendario_gui.py`).
- Se guarda automáticamente al exportar y al cerrar la ventana.
- Contiene: título, subtítulo, fecha de inicio, semanas, fechas de exámenes y entradas por semana.
- Al iniciar, la aplicación intenta cargarlo y precargar los datos.
- Para “empezar de cero”, elimina el archivo `calendario_backup.json`.

## Colores y estilos
- Festivos: Verde claro (#C6EFCE) en Excel y PDF.
- Exámenes: Naranja claro (#F8CBAD) en Excel y PDF.
- La grilla deshabilita celdas de festivo (no editables) y marca las de exámenes con “Examen”.

## Arquitectura (resumen)
- Datos
  - `WeekDates`: dataclass con `semana`, `lunes`, `martes`, `miercoles`.
  - `compute_weeks(start_monday, weeks)`: genera las semanas desde un lunes.
  - `get_colombia_holidays(start, end)`: usa `holidays` (si está) o fallback 2025.
- Exportación
  - `build_excel(out_path, title, subtitle, week_dates, entries, holidays_map, exam_dates)`.
  - `build_pdf(out_path, title, subtitle, week_dates, entries, holidays_map, exam_dates)`.
- GUI (`CalendarGUI`)
  - Entrada de Título/Subtítulo, fecha de inicio, semanas.
  - Sección para 8 fechas de exámenes.
  - Grilla con 4 columnas (Lu, Ma, Mié1, Mié2) y filas por semana.
  - Botones para exportar Excel/PDF.
  - Respaldo: `_save_backup()`, `_load_backup()`, `_apply_saved_entries()`.

## Decisiones clave
- Tkinter + ttk por simplicidad y portabilidad.
- `openpyxl` para Excel por control de estilos, merges y bordes.
- `reportlab` opcional para PDF; si no está instalado, se muestra un error controlado al exportar.
- `tkcalendar` mejora la UX de fechas, pero hay fallback con Combobox/Entry.
- Fallback de festivos: conjunto mínimo para el 2025 (Ago–Dic) en ausencia de `holidays`.

## Extender o personalizar
- Más días de clase: añadir campos en `WeekDates`, ajustar `_build_weeks_ui`, `build_excel` y `build_pdf`, y actualizar `_collect_entries`.
- Número de exámenes: cambiar la iteración de 8 en la sección de exámenes de la GUI y en el respaldo si deseas almacenarlos todos.
- Colores: modificar los códigos hex en `build_excel` y `build_pdf`.

## Problemas conocidos / Solución de problemas
- “Import could not be resolved” en el editor: instala las dependencias indicadas; son advertencias de entorno.
- PDF falla: instala `reportlab`.
- Selector de fecha no aparece: instala `tkcalendar` (si no, usa el fallback).
- La fecha de inicio debe ser lunes; si no, la app lo avisará.

## Historial de cambios (alto nivel)
- Versión inicial: GUI con 18 semanas desde 18/08/2025; exportación a Excel; festivos CO.
- Mejoras: selector de fecha, ajuste de semanas, alineación de encabezados, comentarios extensivos.
- Exportación PDF (opcional) y fallback festivos 2025.
- Resaltado de festivos (verde) y exámenes (naranja) en Excel/PDF.
- Sección de 8 exámenes y marcado en grilla.
- Respaldo automático en JSON con precarga al iniciar.

---
Si necesitas ampliar funcionalidades (p. ej., más días, otro idioma, formatos adicionales), abre un issue o indica los cambios deseados.
