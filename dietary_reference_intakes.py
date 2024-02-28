import pandas as pd

def dietary_recommendations_1(sex, age, age_unit_type='year'):
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


def dietary_recommendations_2(sex, age, age_unit_type='year'):
    '''
    Returns dietary recommendations for a given sex & age based on a new CSV structure.
    
    Arguments:
    sex (string) - Accepts "female", "f", "F", "Female", "male", "m", "M", "Male".
    age (int or float) - Age value. Interpretation depends on age_unit_type.
    age_unit_type (string) - Specifies the unit of age, either "year" or "month". Defaults to "year".
    
    Returns:
    recommendations_series (Pandas.Series) - Specifying specific dietary requirements.
    '''
    df = pd.read_csv("data/Dietary Requirements - diet_minimums - Dietary Requirements - diet_minimums.csv")
    
    # Convert age to years if specified in months
    if age_unit_type in ["month", "months"]:
        age = age / 12.0
    
    # Define the appropriate age group column based on age and sex
    if age <= 3:
        age_group = 'C 1-3'
    elif 4 <= age <= 8:
        age_group = 'F 4-8' if sex.lower().startswith('f') else 'M 4-8'
    elif 9 <= age <= 13:
        age_group = 'F 9-13' if sex.lower().startswith('f') else 'M 9-13'
    elif 14 <= age <= 18:
        age_group = 'F 14-18' if sex.lower().startswith('f') else 'M 14-18'
    elif 19 <= age <= 30:
        age_group = 'F 19-30' if sex.lower().startswith('f') else 'M 19-30'
    elif 31 <= age <= 50:
        age_group = 'F 31-50' if sex.lower().startswith('f') else 'M 31-50'
    elif age >= 51:
        age_group = 'F 51+' if sex.lower().startswith('f') else 'M 51+'
    
    # Select only the relevant column for the age group
    recommendations = df[['Nutrition', age_group]]
    recommendations.columns = ['Nutrition', 'Recommendation']  # Rename columns for clarity
    
    # Convert DataFrame to Series with Nutrition as index
    recommendations_series = recommendations.set_index('Nutrition')['Recommendation']
    
    return recommendations_series

def inuit_dietary_reference_intakes(sex, age, age_unit_type='year'):
    '''
    Combines dietary recommendations from two sources for a given sex & age.
    
    Arguments:
    sex (string) - Accepts various forms of identifying gender (male/female).
    age (int or float) - Age value.
    age_unit_type (string) - Specifies the unit of age, either "year" or "month". Defaults to "year".
    
    Returns:
    combined_recommendations_series (Pandas.Series) - Combined dietary recommendations.
    '''
    # Assuming these functions are defined in your environment and return Series with the same index or compatible indices.
    inuit_recommendations = dietary_recommendations_1(sex, age, age_unit_type)
    dietary_recommendations = dietary_recommendations_2(sex, age, age_unit_type)
    
    # Combine the two Series. This simple approach adds them together;
    # if they have identical indices and numeric values, they will be summed.
    # For non-numeric types or to handle conflicts differently, additional logic is needed.
    combined_recommendations = pd.concat([inuit_recommendations, dietary_recommendations], axis=0)
    
    return combined_recommendations