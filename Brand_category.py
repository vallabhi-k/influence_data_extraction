import pandas as pd

df = pd.read_csv (r'Brands.csv',header=0,names=['Username','Category'])
df = df.iloc[1:]
UN = df['Category'].unique()
beautyUN=list(df['Username'][df['Category'] == 'beauty'])
familyUN=list(df['Username'][df['Category'] == 'family'])
fashionUN=list(df['Username'][df['Category'] == 'fashion'])
fitnessUN=list(df['Username'][df['Category'] == 'fitness'])
foodUN=list(df['Username'][df['Category'] == 'food'])
interiorUN=list(df['Username'][df['Category'] == 'interior'])
petUN=list(df['Username'][df['Category'] == 'pet'])
travelUN=list(df['Username'][df['Category'] == 'travel'])
otherUN=list(df['Username'][df['Category'] == 'other'])

dictUN = {}
dictUN['beautyUN'] = beautyUN
dictUN['familyUN'] = familyUN
dictUN['fashionUN'] = fashionUN
dictUN['fitnessUN'] = fitnessUN
dictUN['foodUN'] = foodUN
dictUN['interiorUN'] = interiorUN
dictUN['petUN'] = petUN
dictUN['travelUN'] = travelUN
dictUN['otherUN'] = otherUN