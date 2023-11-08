import pandas as pd

# 读取你的excel文件
df = pd.read_excel("食用菌summary.xlsx")

# 创建一个空的DataFrame来存放结果
new_df = pd.DataFrame()

# 遍历每一行，根据‘频数’重复每一行
for index, row in df.iterrows():
    repeated_row = pd.concat([row]*int(row['频数']), ignore_index=True, axis=1).T
    new_df = pd.concat([new_df, repeated_row], ignore_index=True)

# 将结果保存到一个新的sheet中
with pd.ExcelWriter('食用菌summary.xlsx', mode='a') as writer:
    new_df.to_excel(writer, sheet_name='NewSheet')