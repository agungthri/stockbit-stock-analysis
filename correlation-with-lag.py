from load_data_price import load_data
import pandas as pd

NUMBER = 50
ALL_CORR_RESULT = []

if __name__ == '__main__':
  code = 'ITMG'
  column = 'close'
  data = pd.concat(load_data(), axis=1)
  all_corr_result = []
  for i in data:
    target = data[code]
    pair = data[i]
    for j in range(NUMBER):
      corr = target.corr(pair.shift(j))
      if corr > 0.8:
        all_corr_result.append({'code': i, 'lag-period': j, 'corr': corr})

  all_corr_result = pd.DataFrame(all_corr_result)
    # group by code and get the row with max corr for each group
  all_corr_result = all_corr_result.loc[all_corr_result.groupby('code')['corr'].idxmax()]
  # create new dataframe with only code and lag-period columns
  all_corr_result = all_corr_result[['code', 'lag-period', 'corr']].reset_index(drop=True).sort_values(by='corr', ascending=False)
  # print the new dataframe
  all_corr_result.to_excel(f'correlation-with-lag.xlsx', index=False)

