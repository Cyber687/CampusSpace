# Setup guide

1. Create a virtual environment and install `requirements.txt`.
2. Copy `.env.example` to `.env`; set a unique `JWT_SECRET_KEY`.
3. Run `python scripts/init_db.py` once.
4. Run `python run.py`.
5. Visit `http://127.0.0.1:8000/static/index.html`.
6. Use one of the demo accounts in README, or register a student.
7. API docs: `http://127.0.0.1:8000/docs`.

If the server says the database is not initialized, run the initializer from the project root. The `--reset` option deletes the existing local database and re-seeds it.
