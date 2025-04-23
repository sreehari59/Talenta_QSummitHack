import pandas as pd

df = pd.read_json("data/profiles copy.json")
# print(df)
# print(df["projectApplication"][0]["projectDetails"])

print(df["projectApplication"][2]["projectDetails"]["projectName"])
print(df["projectApplication"][2]["projectDetails"]["description"])
# print(df["projectApplication"][0]["projectDetails"]["requirements"])

# print("Total Number of unique positions:", len(df["projectApplication"][0]["projectDetails"]["requirements"]))
# for i in range(len(df["projectApplication"][0]["projectDetails"]["requirements"])):
#     print(df["projectApplication"][0]["projectDetails"]["requirements"][i])

# for _, row in df.iterrows():
#     print(', '.join(row['technologies']))
#     metadata={"name": row["name"],
#                                     "role": row["role"],
#                                     "technologies":', '.join(row['technologies'])}
#     break

# print(metadata)