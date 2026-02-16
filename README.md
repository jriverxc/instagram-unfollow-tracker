# Instagram Unfollow Tracker

Ahora el proyecto funciona como servicio web.

## ¿Qué hace?

1. Subes `followers_1.json` y `following.json`.
2. Procesa los archivos y te muestra la lista de inmediato en pantalla.
3. Si quieres, desde el mismo resultado puedes descargar el CSV.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar

```bash
python manage.py runserver 0.0.0.0:5000
```

Abrir en navegador:

- http://localhost:5000

## Uso

1. Descarga tus datos de Instagram en formato JSON.
2. Ubica los archivos:
   - `followers_1.json`
   - `following.json`
3. Súbelos en la página y presiona **Procesar archivos**.
4. Verás la lista directamente en pantalla y tendrás botón **Descargar CSV**.

## Tests

```bash
python manage.py test
```

## Privacidad

El servicio corre localmente y procesa los archivos en tu equipo.
