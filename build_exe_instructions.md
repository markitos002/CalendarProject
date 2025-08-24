# Generar ejecutable (.exe)

## 1. Crear/activar entorno (opcional si ya existe .venv)
```
python -m venv .venv
.\.venv\Scripts\activate
```

## 2. Instalar dependencias
```
pip install -r requirements.txt
pip install pyinstaller
```

## 3. Generar el ejecutable
Ejecutar desde la raíz del proyecto:
```
pyinstaller --name CalendarioClases ^
  --onefile ^
  --noconsole ^
  --add-data "calendario_backup.json;." ^
  generar_calendario_gui.py
```

Notas:
- Si `calendario_backup.json` no existe aún, puedes omitir la línea --add-data o crear un archivo vacío.
- En Windows, el separador de datos en --add-data usa `;`, en Linux/Mac usar `:`.
- El ejecutable quedará en `dist/CalendarioClases.exe`.

## 4. Incluir librerías de fuentes (opcional)
ReportLab puede necesitar recursos adicionales (normalmente se incluye todo). Si falta algo, ejecuta sin `--onefile` para depurar:
```
pyinstaller --name CalendarioClases --noconsole generar_calendario_gui.py
```

## 5. Limpieza de carpetas temporales
- `build/` y `*.spec` se generan automáticamente.
- Puedes volver a compilar modificando opciones en el archivo `.spec`.

## 6. Atajos útiles
Regenerar rápido (después de editar código):
```
pyinstaller CalendarioClases.spec
```

## 7. Errores comunes
- ModuleNotFoundError: Asegúrate de ejecutar dentro del venv correcto.
- Problemas con tk: Verifica que tu instalación de Python incluye tkinter.
- Ventana de consola aparece: quita `--noconsole` si necesitas ver logs.

## 8. Distribución
Entrega el contenido de `dist/CalendarioClases.exe` y (si usas `--onefile`) ningún otro archivo es necesario salvo que quieras pre-cargar un `calendario_backup.json` inicial.
