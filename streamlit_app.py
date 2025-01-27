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

# Establish a Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Step 1: Fetch data from the Snowflake table
try:
    # Selecting columns from the Snowflake table
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
    
    # Convert Snowflake DataFrame to Pandas DataFrame
    pd_df = my_dataframe.to_pandas()
    
    # Display the fetched data in Streamlit
    st.dataframe(data=pd_df, use_container_width=True)

except Exception as e:
    st.error("An error occurred while fetching data from Snowflake.")
    st.exception(e)
    st.stop()

# Step 2: Streamlit multiselect for up to 5 ingredients
try:
    # Display fruit options for user selection
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        pd_df['FRUIT_NAME'].tolist(),  # Convert column to a list for multiselect
        max_selections=5
    )

except Exception as e:
    st.error("An error occurred while displaying the ingredient selection.")
    st.exception(e)
    st.stop()

# Step 3: Fetch and display nutrition information from the Fruityvice API
if ingredients_list:
    try:
        for fruit_chosen in ingredients_list:
            # Get the corresponding SEARCH_ON value
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

            # Display the fruit name and fetch its nutrition information
            st.subheader(f"{fruit_chosen} Nutrition Information")
            
            # Fetch data from the Fruityvice API
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
            
            # Handle API response
            if fruityvice_response.status_code == 200:
                nutrition_data = fruityvice_response.json()
                st.json(nutrition_data)  # Display the JSON data in Streamlit
            else:
                st.error(f"Failed to fetch data for {fruit_chosen}. Response code: {fruityvice_response.status_code}")

    except Exception as e:
        st.error("An error occurred while fetching or displaying nutrition information.")
        st.exception(e)
