"""Admin analytics: user counts, demographics, charts."""

from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from db.database import get_all_users, get_chat_count, get_resume_count, get_all_chats


def get_total_users():
    rows = get_all_users()
    return len(rows)


def get_active_users(days=30):
    rows = get_all_users()
    if not rows:
        return 0
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    count = 0
    for row in rows:
        last_login = row[5] if len(row) > 5 else None
        if last_login and str(last_login) >= cutoff:
            count += 1
    return count


def get_resumes_count():
    return get_resume_count()


def get_chats_count():
    return get_chat_count()


def chart_users_by_signup_date():
    rows = get_all_users()
    if not rows:
        return None
    dates = []
    for row in rows:
        created = row[4] if len(row) > 4 else None
        if created:
            try:
                d = str(created)[:10]
                dates.append(d)
            except Exception:
                pass
    if not dates:
        return None
    df = pd.Series(dates).value_counts().sort_index().reset_index()
    df.columns = ["date", "count"]
    fig = px.bar(df, x="date", y="count", title="Users by Signup Date")
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def chart_users_by_activity():
    rows = get_all_users()
    if not rows:
        return None
    has_login = sum(1 for r in rows if r[5])
    no_login = len(rows) - has_login
    fig = go.Figure(data=[go.Pie(
        labels=["Has logged in", "Never logged in"],
        values=[has_login, no_login],
        hole=0.4,
    )])
    fig.update_layout(title="Users by Activity")
    return fig


def chart_users_by_country():
    rows = get_all_users()
    if not rows:
        return None
    countries = []
    for row in rows:
        country = row[7] if len(row) > 7 else "Unknown"
        countries.append(country or "Unknown")
    df = pd.Series(countries).value_counts().reset_index()
    df.columns = ["country", "count"]
    fig = px.bar(df, x="country", y="count", title="Users by Country")
    return fig


def chart_users_by_age():
    rows = get_all_users()
    if not rows:
        return None
    ages = []
    for row in rows:
        age = row[8] if len(row) > 8 else None
        if age is not None:
            ages.append(age)
    if not ages:
        return None
    df = pd.DataFrame({"age": ages})
    fig = px.histogram(df, x="age", nbins=20, title="Users by Age")
    return fig
