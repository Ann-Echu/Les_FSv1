import os
import pandas as pd

def save_to_csv(response):
    file_path = 'data/survey_responses03.csv'
    df = pd.DataFrame([response])

    # Check if CSV exists
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)