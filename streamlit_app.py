# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

from snowflake.snowpark.functions import col

# session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)

# ingredients_list = st.multiselect(
#     'Choose upto 5 ingredients:'
#     ,my_dataframe
# )

# if ingredients_list:
#     ingredients_string = ''
    
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '
        
#         my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
#             values ('""" + ingredients_string + """')"""
        
#         time_to_insert = st.button('Submit Order')
        
#         if time_to_insert:
#             session.sql(my_insert_stmt).collect()
            
#             st.success('Your Smoothie is ordered!', icon="✅")



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Convert the Snowflake DataFrame to a list of fruit names
fruit_names = [row['FRUIT_NAME'] for row in my_dataframe]

# Streamlit multiselect for up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names
)

if ingredients_list:
    # Create a single string of selected ingredients
    ingredients_string = ' '.join(ingredients_list)
    
    # Button for submitting the order
    time_to_insert = st.button('Submit Order', key="submit_order_button")
    
    if time_to_insert:
        # Insert the order into the database
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients)
        VALUES ('{ingredients_string}')
        """
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

