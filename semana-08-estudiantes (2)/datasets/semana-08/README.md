# Datos de movilidad · semana 8

Fuente inmediata: archivo `uber (1).csv` suministrado por el docente. Proveedor original y licencia no verificados.
Preparado para los materiales de la semana 8 del curso. No se atribuye a Uber o TLC por su nombre.
El original no se copia ni modifica. Su SHA-256 y el protocolo se registran en `manifest.json`.

## Archivos

| Archivo | Contenido |
|---|---|
| recogidas_desarrollo.csv | 6.000 filas de enero–septiembre de 2014; semilla 42 |
| recogidas_test_temporal.csv | 7.311 filas de octubre–diciembre de 2014 |
| recogidas_jerarquico.csv | 500 filas de la muestra de desarrollo; semilla 42 |
| auditoria.csv | Conteos secuenciales sobre los 200.000 registros originales |
| manifest.json | Huella, reglas, tamaños y contexto |
| diccionario.csv | Variables y unidades |

Unidad: una recogida registrada. No se identifican trayectorias de conductores ni se estima demanda total.
Se excluyen coordenadas imposibles; ceros se separan por no pertenecer a este caso. El recorte
[-74.30, -73.65] × [40.45, 40.95] es una decisión de estudio, no una frontera administrativa.
Las tarifas no positivas y pasajeros extraños se auditan, pero no eliminan observaciones del modelo espacial.
Coordenadas repetidas pueden ser eventos válidos; el original no contiene claves ni filas completas duplicadas.

Proyección: EPSG:4326 → EPSG:32618, con orden longitud/latitud explícito. Se resta el origen fijo
(585000, 4510000) metros y se divide por 1000. Ambos ejes están en km. El calendario conserva UTC
tal como se codificó en la fuente; no hacemos inferencias sobre franjas de hora local.

## Reconstrucción

Desde la raíz del repositorio, con las dependencias de `requirements-week8.txt`:

```powershell
python scripts/prepare_week8_data.py --source 'C:\Users\legion\Downloads\uber (1).csv'
```

El script falla si faltan columnas requeridas. Conserva identificadores de fila para comprobar la separación
y recuperar registros originales. La muestra se ordena por fecha antes de crear folds temporales.
No hay imputación de coordenadas. Un dato fuera del área puede ser legítimo y no se etiqueta como fraude.
