# Instagram Unfollow Tracker (Django)

Ahora el proyecto funciona como **servicio web con Django**.

## ¿Qué hace?

1. Subes `followers_1.json` y `following.json`.
2. Calcula qué usuarios sigues y no te siguen de vuelta.
3. Puedes:
   - Ver el resultado online.
   - Descargar el resultado como CSV.

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
3. Súbelos desde la página principal.
4. Elige:
   - **Ver resultado online**
   - **Descargar CSV**

## Tests

```bash
python manage.py test
```

## Privacidad

El servicio corre localmente y procesa los archivos en tu equipo.
