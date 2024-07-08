import streamlit as st

# Define dictionaries for scores
issue_classification_scores = {
    'Severe': 125,
    'High': 25,
    'Medium': 5
}

area_impact_scores = {
    'Spread across almost all areas of the Bank': 62.5,
    'Spread across multiple areas of the Bank': 12.5,
    'Spread across limited areas of the Bank': 2.5
}

def key_control_failure_score(value):
    if value >= 80:
        return 62.5
    elif 40 <= value < 80:
        return 12.5
    elif value < 40:
        return 2.5
    else:
        return 0

def calculate_ce_rating(total_issue_classification_score, area_impact_score, key_control_failure_score):
    # Halve the area impact and key control failure scores
    adjusted_area_impact_score = area_impact_score / 2
    adjusted_key_control_failure_score = key_control_failure_score / 2
    # Calculate total CE rating
    total_ce_rating = total_issue_classification_score + adjusted_area_impact_score + adjusted_key_control_failure_score
    return total_ce_rating

def get_ce_rating_definition(ce_rating):
    if ce_rating <= 50:
        return 'Strong'
    elif 51 <= ce_rating <= 99:
        return 'Satisfactory with exceptions'
    elif 100 <= ce_rating <= 250:
        return 'Needs Improvement'
    else:
        return 'Weak'

# Streamlit UI
st.title('CE Rating Calculator')

st.header('Input Data')

num_issues = st.number_input('Number of Issues', min_value=1, value=1)

total_issue_classification_score = 0
for i in range(num_issues):
    st.subheader(f'Issue {i + 1}')
    issue_classification = st.selectbox(
        f'Issue Classification for Issue {i + 1}',
        options=list(issue_classification_scores.keys()),
        key=f'issue_classification_{i}'
    )
    total_issue_classification_score += issue_classification_scores[issue_classification]

area_impact = st.selectbox(
    'Area Impact',
    options=list(area_impact_scores.keys())
)

key_control_failure = st.slider(
    '% of Key controls which have failed and contributed to findings in the audit report',
    min_value=0,
    max_value=100,
    value=50
)

if st.button('Calculate CE Rating'):
    area_impact_score = area_impact_scores[area_impact]
    key_control_failure_score_value = key_control_failure_score(key_control_failure)

    ce_rating = calculate_ce_rating(total_issue_classification_score, area_impact_score, key_control_failure_score_value)
    ce_rating_definition = get_ce_rating_definition(ce_rating)

    st.subheader('Results')
    st.write(f'Total Issue Classification Score: {total_issue_classification_score}')
    st.write(f'CE Rating: {ce_rating}')
    st.write(f'CE Rating Definition: {ce_rating_definition}')
