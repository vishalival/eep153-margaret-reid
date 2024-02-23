import pandas as pd

def inuit_dietary_recommendations(sex, age, age_unit_type='year'):
    '''
    Returns the Inuit dietary recommendations for a given sex & age.
    Arguments:
    sex (string) - Accepts "female", "f", "F", "Female", "male", "m", "M", "Male".
    age (int or float) - Age value. Interpretation depends on age_unit_type.
    age_unit_type (string) - Specifies the unit of age, either "year" or "month". Defaults to "year".

    Returns:
    recommendations_series (Pandas.Series) - Specifying specific dietary requirements.
    '''
    merged_df = pd.read_csv("data/inuit_dietary_info.csv")

    # Convert age to years if age_unit_type is 'month'.
    if age_unit_type == "month" or age_unit_type == "months":
        age = age / 12.0

    # Adjust gender for age under 10.
    if age <= 10:
        gender = 'ALL'
    else:
        if sex in ["female", "f", "F", "Female"]:
            gender = 'F'
        elif sex in ["male", "m", "M", "Male"]:
            gender = 'M'
    
    # Define the age group based on age in years.
    # This section goes through the age to find the age required.
    age_group = '≤6 mo' if age <= 0.5 else \
                '7-11 mo' if age <= 1 else \
                '1-3 y' if age <= 3 else \
                '4-6 y' if age <= 6 else \
                '7-10 y' if age <= 10 else \
                '11-14 y' if age <= 14 else \
                '15-17 y' if age <= 17 else \
                '18-24 y' if age <= 24 else \
                '25-50 y' if age <= 50 else \
                '51-70 y' if age <= 70 else \
                '>70 y'
    
    # Filter the merged_df for the specific age group and gender.
    recommendations_df = merged_df[(merged_df['Age group'] == age_group) & (merged_df['Gender'] == gender)]

    # Clean up the DataFrame by removing unnecessary columns.
    columns_to_remove = ['Unnamed: 0', 'index_x', 'index_y', 'index', 'Age group', 'Gender']
    recommendations_df = recommendations_df.drop(columns=[col for col in columns_to_remove if col in recommendations_df.columns])

    # Format column names to be more readable.
    recommendations_df.columns = [col.replace('\n', ' ').replace('­', '-').strip() for col in recommendations_df.columns]

    # Convert the filtered DataFrame to a Series.
    recommendations_series = recommendations_df.squeeze()

    return recommendations_series
