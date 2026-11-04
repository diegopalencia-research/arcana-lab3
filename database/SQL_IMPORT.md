# SQLite import

The file `setup_arcana_lab.sql` is self-contained: it creates the schema, indexes, view, 78 cards, and correspondence metadata.

From the project root, run:

```bash
sqlite3 arcana_lab.sqlite < database/setup_arcana_lab.sql
```

Or open the SQL file in DB Browser for SQLite and execute it. The Streamlit application creates/initializes its own `data/arcana_lab.db` automatically from `schema.sql` and the two CSV seed files, so you normally do not need to execute this script separately.
