# SMA Project

Project structure (root of repository):

	sma-project/
		app.py                 # main Flask entry point
		config.py              # API keys, DB URI, secret key (use env vars in prod)
		sample_data.json       # small test dataset for local testing
		modules/               # one .py file per module (NLP, graph, ML)
		app/                   # Flask package with models, routes, templates
			routes/              # Flask blueprints (one per module)
			models/              # model wrappers (e.g., User)
			templates/           # HTML pages
		models/                # saved .pkl ML model files (trained models)
		static/                # CSS, JS, images
		scripts/               # helper scripts (e.g., training)

Quick start:

1. Install dependencies: `pip install -r requirements.txt`
2. Ensure MongoDB is running and set `MONGO_URI`/`MONGO_DBNAME` as env vars if needed
3. Run the app: `python app.py`

Notes:
- Auth uses `flask-login` + `werkzeug.security` for password hashing.
- `active_case_id` is stored in the Flask session so modules can load case-specific posts.
- Module code lives in `modules/` and each module should expose standalone functions for testing with `sample_data.json`.
- Trained ML models are saved under `models/` as `.pkl` files.

Demo login (quick method):

1. Ensure MongoDB is running locally.
2. Create a demo user by running:

```bash
python scripts/create_demo_user.py
```

3. Open the app at `http://127.0.0.1:5000` and go to `/login`.
	- Username: `muskan`
	- Password: `Password123`

Or register a new user at `/register`.

Verify pages:
- Trending: `http://127.0.0.1:5000/trending`
- Fake news: `http://127.0.0.1:5000/fakenews`


