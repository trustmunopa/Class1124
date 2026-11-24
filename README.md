# Garden App (template)

A small Streamlit app over a SQLite database, built in MAT 3050 (Databases for Data Science) at Warren Wilson College. Use it as a starting point and as a menu of Streamlit patterns to borrow for your own project.

## Start your own copy

1. Click **Use this template** (top right), then **Create a new repository**. Name it `my-garden`, keep it Public, click **Create repository**.
2. In your new repo: **Code** (green button), **Codespaces** tab, **Create codespace on main**.
3. Wait for the terminal to finish `pip install -r requirements.txt`. Then:

```
streamlit run app.py
```

## What's in here

```
app.py                 home page: metrics, tables, a chart, Reset garden
db.py                  connect(): bakes garden.db from the migrations if it's missing
queries.py             every SQL statement, one function each
rebuild.py             python rebuild.py throws garden.db away and bakes a new one
migrations/            the recipe: numbered .sql files, run in order
pages/                 one file per page in the sidebar
.devcontainer/         tells GitHub how to set up your codespace
.streamlit/config.toml Streamlit settings (so you don't need the long run command)
```

## Streamlit patterns to borrow

| Pattern | Where |
|---|---|
| `st.metric` tiles in `st.columns` | app.py |
| `st.bar_chart` from a DataFrame | app.py, pages/1_History.py |
| `st.sidebar` | pages/1_History.py |
| `st.tabs` | pages/1_History.py |
| `st.download_button` (CSV) | pages/1_History.py |
| `st.form` with validation | pages/2_Add_Visit.py |
| Catching a database error and showing `st.error` | pages/4_Remove_Bed.py, pages/5_Edit_Logs.py |
| `st.data_editor` (edit a table, save it back) | pages/5_Edit_Logs.py |

## The rules of migrations

- Numbered with three digits (001, 002...). `rebuild.py` runs them in that order.
- Never edit a migration after you've pushed it. Want a change? Add the next number.
- Never commit the database. `.gitignore` already says `*.db`. Commit the recipe, not the cake.
