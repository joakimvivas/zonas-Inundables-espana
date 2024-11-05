# Zonas Inundables

Bla, bla, bla.

## Running the project locally

1. Create the Python virtual environment

```sh
python3 -m venv zonas-inundables
```

```sh
source zonas-inundables/bin/activate
```

2. Install dependencies:

It is recommended, first, upgrade pip:
```sh
pip install --upgrade pip
```

Install dependencies/requirements:
```sh
pip install -r requirements.txt
```

3. (Optional) Have in your Local the `.env` file created with the credentials, you can use the `.env.example` file as a template.

4. Execute the following command:

```sh
uvicorn app.main:app --reload --port 3000 --host 0.0.0.0
```

Or if you want to see the logs:

```sh
uvicorn app.main:app --reload --port 3000 --host 0.0.0.0 --log-level debug
```

Or in background:

```sh
nohup uvicorn main:app --reload --port 8888 --host 0.0.0.0 &
```

5. You should see an output similar to:

```
INFO:     Uvicorn running on http://127.0.0.1:3000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```