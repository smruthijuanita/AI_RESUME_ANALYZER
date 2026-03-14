# Reusable Features Reference

Code grouped by feature for reuse in another project. Includes integration fixes and admin-only restrictions.

---

## 1. Login & Auth

### `config/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "resume_analyzer.db")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")  # Comma-separated for multiple admins
```

### `utils/auth.py`

```python
import sqlite3
import bcrypt
from config.config import DB_PATH


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_user(email: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, _hash_password(password)),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(email: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user and _check_password(password, user[2]):
        return user
    return None


def is_admin(email: str) -> bool:
    from config.config import ADMIN_EMAIL
    admins = [e.strip() for e in ADMIN_EMAIL.split(",") if e.strip()]
    return email in admins
```

### Database schema (`database/db.py`)

```python
import sqlite3
from config.config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_analysis(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        role TEXT,
        extracted_skills TEXT,
        missing_skills TEXT,
        roadmap TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
```

### Streamlit login/signup UI (in `app.py`)

```python
from utils.auth import create_user, login_user, is_admin
from database.db import init_db

# Initialize DB at startup
init_db()

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# LOGIN / SIGNUP PAGE
if st.session_state.user is None:
    st.header("Login / Signup")
    menu = st.selectbox("Select Option", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if menu == "Signup":
        if st.button("Create Account"):
            if create_user(email, password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("User already exists.")

    elif menu == "Login":
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = email
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    st.stop()

# Sidebar - show logged in user and logout
st.sidebar.write(f"Logged in as: **{st.session_state.user}**")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()
```

---

## 2. Admin Dashboard (Admin-only)

### `database/save_analysis.py`

```python
import sqlite3
import json
from config.config import DB_PATH


def save_analysis(email: str, role: str, skills: list, missing: list, roadmap: list | dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO resume_analysis
    (user_email, role, extracted_skills, missing_skills, roadmap)
    VALUES (?, ?, ?, ?, ?)
    """, (
        email,
        role,
        json.dumps(skills),
        json.dumps(missing),
        json.dumps(roadmap),
    ))
    conn.commit()
    conn.close()
```

### Admin dashboard UI (in `app.py`)

**Important:** Only show Admin Dashboard and Knowledge Graph to admin users.

```python
from utils.auth import is_admin
from config.config import DB_PATH

# Page options - hide Admin from non-admins
pages = ["Resume Analysis", "Chat"]  # or your main pages
if is_admin(st.session_state.user):
    pages.append("Admin Dashboard")

page = st.sidebar.selectbox("Page", pages)

# ... other pages ...

elif page == "Admin Dashboard":
    if not is_admin(st.session_state.user):
        st.error("Access denied. Admin only.")
        st.stop()

    st.title("Admin Dashboard")

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM resume_analysis", conn)
    conn.close()

    if df.empty:
        st.warning("No data available yet.")
    else:
        st.subheader("All Resume Analyses")
        st.dataframe(df)

        st.subheader("System Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Analyses", len(df))
        with col2:
            st.metric("Total Users", df["user_email"].nunique())

        st.subheader("Most Selected Roles")
        st.bar_chart(df["role"].value_counts())

        st.subheader("Most Common Missing Skills")
        all_missing = []
        for item in df["missing_skills"]:
            try:
                skills = json.loads(item)
                all_missing.extend(skills)
            except (json.JSONDecodeError, TypeError):
                pass

        if all_missing:
            missing_df = pd.Series(all_missing).value_counts()
            st.bar_chart(missing_df)

        # --- Knowledge Graph (Admin-only) ---
        st.subheader("Skill Knowledge Graph")
        # Aggregate data for global graph or show per-role
        role_filter = st.selectbox("Role for graph", ["All"] + df["role"].unique().tolist())
        if role_filter == "All":
            sample = df.iloc[-1]  # or aggregate
        else:
            sample = df[df["role"] == role_filter].iloc[-1]

        try:
            skills = json.loads(sample["extracted_skills"])
            missing = json.loads(sample["missing_skills"])
            role = sample["role"]
            from utils.graph import build_skill_graph
            graph = build_skill_graph(role, skills, missing)
            st.plotly_chart(graph)
        except (json.JSONDecodeError, KeyError) as e:
            st.warning(f"Could not build graph: {e}")
```

---

## 3. Knowledge Graph (Admin-only)

**Note:** The knowledge graph is shown only on the Admin Dashboard. Regular users do not see it.

### `utils/graph.py`

```python
import networkx as nx
import plotly.graph_objects as go


def build_skill_graph(role: str, skills: list, missing: list):
    G = nx.Graph()
    for s in skills:
        G.add_edge(role, s)
    for m in missing:
        G.add_edge(role, m)

    pos = nx.spring_layout(G)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines")

    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(G.nodes()),
    )

    return go.Figure(data=[edge_trace, node_trace])
```

---

## Dependencies

Add to `requirements.txt`:

```txt
streamlit
networkx
plotly
pandas
python-dotenv
bcrypt
```

---

## Integration Checklist

| Item | Status |
|------|--------|
| Passwords hashed with bcrypt | ✅ |
| Use `config.config.DB_PATH` everywhere | ✅ |
| Call `init_db()` at startup | ✅ |
| Admin-only access for Admin Dashboard | ✅ |
| Knowledge graph only on Admin side | ✅ |
| `save_analysis` VALUES placeholder fix (5 params) | ✅ |

---

## Environment Variables

```env
DB_PATH=resume_analyzer.db
ADMIN_EMAIL=admin@example.com
# Multiple admins: ADMIN_EMAIL=admin1@example.com,admin2@example.com
```
