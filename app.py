import streamlit as st
import pandas as pd
from db_connect import get_connection

st.set_page_config(page_title="Lost & Found Portal", layout="centered")

st.title("📦 Lost & Found Management System")

# Sidebar menu
menu = ["View Items", "Report Item", "Check Lost Count"]
choice = st.sidebar.radio("Navigate", menu)

# View Items
if choice == "View Items":
    st.subheader("📋 All Reported Items")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT item_id, item_name, status, description, user_id FROM items")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    conn.close()

# Report Item
elif choice == "Report Item":
    st.subheader("📝 Report Lost or Found Item")

    item_id = st.number_input("Item ID", min_value=1, step=1)
    user_id = st.number_input("User ID", min_value=1, step=1)
    report_type = st.selectbox("Report Type", ["lost", "found"])

    if st.button("Submit Report"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.callproc("report_item", (item_id, user_id, report_type))
            conn.commit()
            st.success("✅ Report submitted successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            conn.close()

# Check Lost Count
elif choice == "Check Lost Count":
    st.subheader("🔍 Check How Many Items a User Has Lost")

    user_id = st.number_input("Enter User ID", min_value=1, step=1)
    if st.button("Check Count"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT count_lost_items({user_id});")
            count = cursor.fetchone()[0]
            st.info(f"User {user_id} has lost {count} items.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            conn.close()
