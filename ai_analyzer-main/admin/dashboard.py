"""Admin dashboard: analytics and knowledge graph."""

import streamlit as st

from admin.analytics import (
    get_total_users,
    get_active_users,
    get_resumes_count,
    get_chats_count,
    chart_users_by_signup_date,
    chart_users_by_activity,
    chart_users_by_country,
    chart_users_by_age,
)
from admin.knowledge_graph import render_knowledge_graph


def render_dashboard():
    st.title("Admin Dashboard")

    # 4.1 User Analytics
    st.subheader("User Analytics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", get_total_users())
    with col2:
        st.metric("Active Users (30d)", get_active_users())
    with col3:
        st.metric("Resumes Uploaded", get_resumes_count())
    with col4:
        st.metric("Total Chats", get_chats_count())

    # 4.2 Demographics
    st.subheader("Demographics")
    c1, c2 = st.columns(2)
    with c1:
        fig = chart_users_by_signup_date()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        fig2 = chart_users_by_country()
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
    with c2:
        fig3 = chart_users_by_activity()
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
        fig4 = chart_users_by_age()
        if fig4:
            st.plotly_chart(fig4, use_container_width=True)

    # 4.3 Knowledge Graph
    st.subheader("Knowledge Graph")
    st.caption("User → Resume, User → Chat, Resume → VectorDB, Chat → LLM")
    kg = render_knowledge_graph()
    if kg:
        st.plotly_chart(kg, use_container_width=True)
    else:
        st.info("No data yet. Users, resumes, and chats will appear here.")
