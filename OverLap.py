import pandas as pd


def overlap(df1, df2):
    df3 = pd.DataFrame(columns=['GENE', 'Mark', 'Flag'])
    df3.loc[:, 'GENE'] = df1.loc[:, 'GENE']
    df3.loc[:, 'Mark'] = 0
    df3.loc[:, 'Flag'] = 1  # Flag = 1则是情形1，不重叠
    print("Program is initiating.")
    k = 1
    for i in range(0, df1.shape[0]):
        if i + 1 == round(k * df1.shape[0] / 10):
            print("{}% has been processed.".format(k * 10))
            k += 1
        if not (df1.loc[i, 'GENE'] in list(df2.loc[:, 'GENE'])):
            continue
        for j in range(0, df2.shape[0]):
            if ((df1.loc[i, 'GENE'] == df2.loc[j, 'GENE']) and (
                    max(df1.loc[i, 'start'], df2.loc[j, 'start']) < min(df1.loc[i, 'end'],
                                                                        df2.loc[j, 'end']))):  # 两者有重叠
                df3.loc[i, 'Flag'] = 2  # 交叉就是首先满足情形2，特殊情形后面再改变
                if (df1.loc[i, 'start'] > df2.loc[j, 'start']) and (df1.loc[i, 'end'] < df2.loc[j, 'end']):
                    df3.loc[i, 'Flag'] = 5  # 情形5
                if (df1.loc[i, 'start'] < df2.loc[j, 'start']) and (df1.loc[i, 'end'] > df2.loc[j, 'end']):
                    df3.loc[i, 'Flag'] = 6  # 情形6
                if df3.loc[i, 'Mark'] == 0:  # 情形4以外
                    df3.loc[i, 'Mark'] = (min(df1.loc[i, 'end'], df2.loc[j, 'end']) - max(df1.loc[i, 'start'],
                                                                                          df2.loc[j, 'start'])) / (
                                                 max(df1.loc[i, 'end'], df2.loc[j, 'end']) - min(df1.loc[i, 'start'],
                                                                                                 df2.loc[j, 'start']))
                else:  # 情形4
                    df3.loc[i, 'Mark'] = str(df3.loc[i, 'Mark']) + ',' + str(
                        (min(df1.loc[i, 'end'], df2.loc[j, 'end']) - max(df1.loc[i, 'start'], df2.loc[j, 'start'])) / (
                                max(df1.loc[i, 'end'], df2.loc[j, 'end']) - min(df1.loc[i, 'start'],
                                                                                df2.loc[j, 'start'])))
    return df3


OL_df1 = pd.read_excel('Gene1.xlsx')
OL_df2 = pd.read_excel('Gene2.xlsx')
OL_df3 = overlap(OL_df1, OL_df2)
OL_df3.to_csv('Overlap.csv')
