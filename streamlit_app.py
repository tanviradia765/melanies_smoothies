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

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Retrieve the data from the Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).collect()

# Convert the Snowpark DataFrame into a Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Display the data in Streamlit
st.dataframe(data=pd_df, use_container_width=True)

# Streamlit multiselect for up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# New section to display nutrition information
if ingredients_list:
    for fruit_chosen in ingredients_list:
        # Get the SEARCH_ON value corresponding to the selected fruit
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Display nutrition information for each fruit
        st.subheader(f"{fruit_chosen} Nutrition Information")
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")

        if fruityvice_response.status_code == 200:
            # Display API response as a table
            nutrition_data = fruityvice_response.json()
            st.json(nutrition_data)
        else:
            st.error(f"Failed to fetch data for {fruit_chosen}.")
