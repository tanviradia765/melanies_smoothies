# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
# session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Convert the Snowflake DataFrame to a list of fruit names
fruit_names = [row['FRUIT_NAME'] for row in my_dataframe]

# Streamlit text input for the user's name on the order
name_on_order = st.text_input("Enter your name for the order:")
st.write("The name on your Smoothie will be ", name_on_order)

# Streamlit multiselect for up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names
)

if ingredients_list and name_on_order:
    # Create a single string of selected ingredients
    ingredients_string = ' '.join(ingredients_list)
    
    # Button for submitting the order
    time_to_insert = st.button('Submit Order', key="submit_order_button")
    
    if time_to_insert:
        # Insert the order into the database
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(my_insert_stmt).collect()
        # st.success(f"Thank you {name_on_order}, your smoothie order has been placed!", icon="✅")
        st.success(f"Your Smoothie is ordered, {name_on_order}", icon="✅")

# New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
