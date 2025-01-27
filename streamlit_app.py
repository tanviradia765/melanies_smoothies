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
    st.write("Fetching data from the Snowflake table...")
    # Selecting columns from the Snowflake table
    snowpark_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
    st.write("Data fetched successfully!")

    # Step 2: Convert Snowpark DataFrame to Pandas DataFrame
    st.write("Converting Snowpark DataFrame to Pandas DataFrame...")
    pd_df = snowpark_df.to_pandas()
    st.write("Conversion successful!")
    st.dataframe(data=pd_df, use_container_width=True)

except Exception as e:
    st.error("An error occurred while fetching or converting data from Snowflake.")
    st.exception(e)
    st.stop()

# Step 3: Allow user to select ingredients
try:
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        pd_df['FRUIT_NAME'].tolist(),  # Convert column to list for Streamlit multiselect
        max_selections=5
    )

    # Step 4: Fetch nutrition information from the API
    if ingredients_list:
        for fruit_chosen in ingredients_list:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

            st.subheader(f"{fruit_chosen} Nutrition Information")
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")

            if fruityvice_response.status_code == 200:
                nutrition_data = fruityvice_response.json()
                st.json(nutrition_data)
            else:
                st.error(f"Failed to fetch data for {fruit_chosen}. Response code: {fruityvice_response.status_code}")

except Exception as e:
    st.error("An error occurred while processing ingredients or fetching API data.")
    st.exception(e)
    st.stop()
