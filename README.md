## Install Dependency
```bash
pip install -r requirements.txt
```

# Configure
All setting on config.py:
- local database
- FB Messenger 
- IBM Watson Assistant
- IBM Peronality Insight


## First Time deploy
create SQL Lite database

```bash
python db.py
```

## Run server

```bash
python app.py
```
ps: need using ngrok to expose port 5000