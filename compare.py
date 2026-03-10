import pandas as pd
from integrations.monday_api import MondayClient

deals_csv = pd.read_csv('d:/Skylark/data/Deal_funnel_Data.csv')
wo_csv = pd.read_csv('d:/Skylark/data/Work_Order_Tracker_Data.csv')
common_csv = set(deals_csv.columns).intersection(set(wo_csv.columns))

client = MondayClient()
deals_api = client.get_deals_board_data()
wo_api = client.get_work_orders_board_data()
common_api = set(deals_api.columns).intersection(set(wo_api.columns))

with open('d:/Skylark/col_compare_utf8.txt', 'w', encoding='utf-8') as f:
    f.write(f"CSV COMMON: {common_csv}\n\n")
    f.write(f"API DEALS: {list(deals_api.columns)}\n\n")
    f.write(f"API WO: {list(wo_api.columns)}\n\n")
    f.write(f"API COMMON: {common_api}\n")
