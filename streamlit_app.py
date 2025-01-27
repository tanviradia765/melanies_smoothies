# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
# session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the snowpark dataframe to pandas dataframe so we can use LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

# Streamlit text input for the user's name on the order
name_on_order = st.text_input("Enter your name for the order:")
st.write("The name on your Smoothie will be ", name_on_order)

# Streamlit multiselect for up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# # Convert the Snowflake DataFrame to a list of fruit names
# fruit_names = [row['FRUIT_NAME'] for row in my_dataframe]

# # Streamlit text input for the user's name on the order
# name_on_order = st.text_input("Enter your name for the order:")
# st.write("The name on your Smoothie will be ", name_on_order)

# # # Streamlit multiselect for up to 5 ingredients
# # ingredients_list = st.multiselect(
# #     'Choose up to 5 ingredients:',
# #     fruit_names
# # )

# if ingredients_list and name_on_order:
#     # Create a single string of selected ingredients
#     ingredients_string = ' '.join(ingredients_list)

#     # Button for submitting the order
#     time_to_insert = st.button('Submit Order', key="submit_order_button")

#     if time_to_insert:
#         # Insert the order into the database
#         my_insert_stmt = f"""
#         INSERT INTO smoothies.public.orders (ingredients, name_on_order)
#         VALUES ('{ingredients_string}', '{name_on_order}')
#         """
#         session.sql(my_insert_stmt).collect()
#         # st.success(f"Thank you {name_on_order}, your smoothie order has been placed!", icon="✅")
#         st.success(f"Your Smoothie is ordered, {name_on_order}", icon="✅")

# New section to display smoothiefroot nutrition information
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)

        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        # st.text(smoothiefroot_response.json())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    # st.write(ingredients_string)
