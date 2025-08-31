import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

print(df.info())
print(df.describe())
# print(df.head())
# print(df.tail())
# print(df.shape)
# print(df.columns)
# print(df.index)
# print(df.dtypes)
# print(df.isnull().sum())