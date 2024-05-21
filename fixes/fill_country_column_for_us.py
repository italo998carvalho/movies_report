import pandas as pd
from datetime import datetime

df = pd.read_excel('result_v3_copy.xlsx')

df.loc[(df['release_date_streaming'].notna()) & (df['release_streaming_date_country'].isna()), 'release_streaming_date_country'] = 'US'

df.to_excel('result_v3_final.xlsx')
