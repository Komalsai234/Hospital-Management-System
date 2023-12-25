import streamlit as st
import pandas as pd
from secret.credentials import *
from utils import *
from SQL_connection import *
from streamlit_extras.switch_page_button import switch_page

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Pharmacy'


db_connection = create_server_connection(host, username, password, database)


st.title('Welcome to Hospital Pharmacy')
st.header("")

medicine_name = get_medicine_names(db_connection)

with st.form(key='search_medicine'):
    st.subheader('Search for Medicine')
    search_query = st.selectbox(
        'Enter the name of the medicine', ['']+medicine_name)
    submit_search = st.form_submit_button('Search')
    if submit_search and search_query:
        stock_info = get_medicine_stock(db_connection, search_query)
        if stock_info:
            df_stock = pd.DataFrame(stock_info, columns=[
                                    'Medicine Name', 'Available Quantity', 'Manufacturer Name', 'Price per Unit'])

            patient_info_df = df_stock.to_html(index=False, border=0)
            st.markdown(patient_info_df, unsafe_allow_html=True)
            st.header(" ")
        else:
            st.error('Medicine not found or no stock available.')

st.header("")


with st.form(key='update_stock'):
    st.subheader('Update Medicine Stock')
    medicine_name = st.selectbox(
        'Enter the name of the medicine', ['']+medicine_name)

    medicine_id_to_update = get_medicine_id_for_names(
        db_connection, medicine_name)

    type_of_update = st.selectbox('Stock Updation', [' ', 'Sales', 'Re-Stock'])

    current_stock = get_medicine_available(
        db_connection, medicine_id_to_update)

    new_quantity = st.number_input('Enter Quantity', min_value=0)

    if type_of_update == 'Re-Stock':
        update_quantity = current_stock + new_quantity
    elif type_of_update == 'Sales':
        if new_quantity > current_stock:
            st.error("Error: Selling quantity is greater than current stock.")
        else:
            update_quantity = current_stock - new_quantity

    update_stock_button = st.form_submit_button('Update Stock')

    if update_stock_button and medicine_id_to_update > 0:
        if type_of_update != 'Sales' or new_quantity <= current_stock:
            update_stock(db_connection, medicine_id_to_update, update_quantity)
            st.success("Medicine Stock Updated Successfully")
st.header("")

with st.form(key='add_medicine'):
    st.subheader('Add New Medicine Entry')
    new_medicine_name = st.text_input('Medicine Name')
    new_description = st.text_area('Description')
    new_quantity_in_sheets = st.number_input('Quantity in Sheets', min_value=0)
    new_price = st.number_input('Price', min_value=0.0)
    add_medicine_button = st.form_submit_button('Add Medicine')
    if add_medicine_button and new_medicine_name:
        inserted_rows = add_medicine(
            db_connection, new_medicine_name, new_description, new_quantity_in_sheets, new_price)
        if inserted_rows:
            st.success(f'Medicine {new_medicine_name} added successfully.')
        else:
            st.error('Failed to add the medicine. Please check the details.')


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_info_back_button = st.button(label='Go Back to ADMIN Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "ADMIN"
        switch_page("ADMIN")
