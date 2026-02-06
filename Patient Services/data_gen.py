import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuration
NUM_ENCOUNTERS = 5000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

DEPARTMENTS = ['Emergency', 'Inpatient', 'Outpatient', 'Surgery', 'ICU']
PROVIDERS = [f'Dr. {x}' for x in ['Smith', 'Jones', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson']]
HOSPITALS = ['Main Campus', 'North Wing', 'South Clinic']

np.random.seed(42)

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

print("Generating operational data...")
# Generate Operational Data (Encounters)
data = []
for i in range(NUM_ENCOUNTERS):
    dept = np.random.choice(DEPARTMENTS, p=[0.3, 0.2, 0.3, 0.1, 0.1])
    
    # Logic for metrics based on department to make it realistic
    if dept == 'Emergency':
        wait_time = np.random.normal(45, 15) # High wait time
        los = np.random.normal(4, 2) # Hours
        staff_ratio = np.random.uniform(1, 4) # Patients per nurse
    elif dept == 'Inpatient':
        wait_time = np.random.normal(20, 5)
        los = np.random.normal(72, 24) # Hours
        staff_ratio = np.random.uniform(3, 6)
    else:
        wait_time = np.random.normal(15, 5)
        los = np.random.normal(2, 1)
        staff_ratio = np.random.uniform(1, 3)

    # Introduce some seasonality/trend (scores dropping later in year means maybe metrics get worse?)
    # Let's make wait times slightly worse towards end of year
    encounter_date = random_date(START_DATE, END_DATE)
    if encounter_date.month > 9:
        wait_time += np.random.uniform(0, 15)

    data.append({
        'encounter_id': f'ENC-{10000+i}',
        'patient_id': f'PT-{random.randint(1000, 9999)}',
        'encounter_date': encounter_date,
        'hospital': np.random.choice(HOSPITALS),
        'department': dept,
        'provider': np.random.choice(PROVIDERS),
        'visit_type': 'Urgent' if dept == 'Emergency' else np.random.choice(['Scheduled', 'Walk-in']),
        'wait_time_min': max(0, round(wait_time, 1)),
        'length_of_stay_hours': max(0.5, round(los, 1)),
        'staffing_ratio': round(staff_ratio, 1)
    })

operational_df = pd.DataFrame(data)

# Introduce missing data in operational (Data Quality Issue)
# Randomly drop some provider names
mask = np.random.choice([True, False], size=len(operational_df), p=[0.02, 0.98])
operational_df.loc[mask, 'provider'] = np.nan

operational_df.to_csv('operational_data.csv', index=False)
print(f"Saved operational_data.csv with {len(operational_df)} records.")


print("Generating survey data...")
# Generate Survey Data (HCAHPS)
# Not every encounter gets a survey (response rate < 100%)
# Some surveys might be orphan (no encounter_id) - Data Quality Issue

survey_data = []
response_rate = 0.6
num_surveys = int(NUM_ENCOUNTERS * response_rate)

# Base scores on operational metrics to create correlations
for _ in range(num_surveys):
    # Pick a random encounter to link to (mostly)
    if np.random.random() > 0.05: # 95% valid links
        enc_idx = np.random.randint(0, len(operational_df))
        enc_row = operational_df.iloc[enc_idx]
        enc_id = enc_row['encounter_id']
        
        # Driver logic: High wait time -> Low Satisfaction
        wait = enc_row['wait_time_min']
        base_score = 10 - (wait / 10) # Simple linear decay
        
        # Add random noise
        satisfaction = base_score + np.random.normal(0, 1.5)
        satisfaction = max(1, min(10, satisfaction)) # Clamp to 1-10
        
    else:
        # 5% Orphan records (Data Quality Issue)
        enc_id = f'ENC-{random.randint(90000, 99999)}' # Non-existent ID
        satisfaction = np.random.normal(7, 2) # Random distribution
        satisfaction = max(1, min(10, satisfaction))

    # Detailed domains
    comm_nurses = max(1, min(10, satisfaction + np.random.normal(0, 1)))
    comm_doctors = max(1, min(10, satisfaction + np.random.normal(0.5, 1))) # Doctors usually score slightly higher?
    cleanliness = max(1, min(10, satisfaction + np.random.normal(0, 2))) # Less correlated
    
    survey_data.append({
        'survey_id': f'SRV-{random.randint(100000, 999999)}',
        'encounter_id': enc_id,
        'response_date': random_date(START_DATE, END_DATE), # Might differ from encounter date, but simplifying
        'overall_satisfaction': round(satisfaction, 1),
        'communication_with_nurses': round(comm_nurses, 1),
        'communication_with_doctors': round(comm_doctors, 1),
        'cleanliness_score': round(cleanliness, 1),
        'would_recommend': np.random.choice(['Yes', 'No'], p=[satisfaction/12, 1-(satisfaction/12)]) if satisfaction < 10 else 'Yes' 
        # Rough prob logic
    })

survey_df = pd.DataFrame(survey_data)
survey_df.to_csv('survey_results.csv', index=False)
print(f"Saved survey_results.csv with {len(survey_df)} records.")
