
# Guosen Option Rds Tools

## Setup

- modify the config file `connection_info.json.bak` to `connection_info.json` and fill the info

# Reference Documents

## Query Cases

```python
from rds_tools.db_executor import FuturexDB

# ALL SELECT
# > Volatility Model
# GetDataMySQL.py

print(FuturexDB.select.get_param_data('DCE', 'C').head())

print(FuturexDB.select.get_param_data_std('DCE', 'C'))

print(FuturexDB.select.get_future_info())

# PyMySQLreadZH.py

print(FuturexDB.select.get_exchange_zh('CBOE'))

print(FuturexDB.select.get_exchange_zh('LME'))

print(FuturexDB.select.get_contract_zh('CFFEX', 'T'))

# GetUnderling.py

print(FuturexDB.select.get_underlying())

print(FuturexDB.select.get_multiplier('rb'))

# > OptionCalc
# GetContract.py

print(FuturexDB.select.get_contract('DCE', 'C'))

# > OrderManagement
# GetModelParamName.py
# replace GetContract

print(FuturexDB.select.get_paramdef_by_model('ovo'))

# GetOrderList.py
# replace GetOrderList

print(FuturexDB.select.get_order_record_otc('13001'))

# GetOrderParam.py

print(FuturexDB.select.get_order_param('13001', 'ovo_13001_11005_1533785827.5574322'))


# GetRoleName.py

print(FuturexDB.select.get_role_by_name('13001'))

# GetRoletype.py | RiskManagement/GetRiskList.py/GetRiskList

print(FuturexDB.select.get_role_by_role_type('13'))

# risk list

print(FuturexDB.select.get_role_by_role_type('14'))


# > RiskManagement
# GetPoSymbol.py

print(FuturexDB.select.get_portfolio_by_id('12001'))


# GetRiskList.py

print(FuturexDB.select.get_order_by_risk_id('14001'))


# GetTraderId.py

# GetSlaveId

print(FuturexDB.select.get_account_id_map_by_master_id('14001'))

# GetTraderId

print(FuturexDB.select.get_trader_id_by_master_id('14001'))

# GetPortDetail.py
# GetPortDetail

print(FuturexDB.select.get_order_record_by_symbol_traderid('OTC-DCE-i', 12001))

# GetPortDetail2

print(FuturexDB.select.get_order_record_by_model_instance(
    'ovo_13001_11005_1533785827.5574322'))

# GetPortSub

print(FuturexDB.select.get_ref_contract())

# show the cache
print(FuturexDB.select._fxdb_cache)

# clear all cache

FuturexDB.select.clear_all_cache()

print(FuturexDB.select._fxdb_cache)

```

## Insert, Update and Delete Cases

```python
from rds_tools.db_executor import FuturexDB

option_1 = {
    'exercise_type': '0',
    'exp_date': '2018-06-13',
    'init_date': '2018-06-13',
    'option_type': '1',
    'ref_contract': 'c1901',
    'ref_exchange': 'DCE',
    'ref_underlying': 'c',
    'strike': '1820'
}

# ordername
model_instance = 'ovo123'  # fk
model_name = 'ovo'
account_id = '13001'  # fk

# new order api
# OrderManagement
# NewOrder.py => NewOrder
FuturexDB.insert.new_order(model_instance, model_name, account_id)

# new param data api
# OrderManagement
# NewParamData.py => NewParamData
FuturexDB.insert.new_param_data(option_1, model_instance, model_name, account_id)

# new create order api
# OrderManagement
# CreateOrder.py => CreateOrder
FuturexDB.insert.create_order(model_instance, model_name, account_id, option_1)

# new order record api
# OrderManagement
# NewOrderRecord.py => NewOrderRecord
order_1 = {'customerid': '11001',
      'riskid': '14001',
      'price': '1234',
      'quantity': '16',
      'quantity_filled': '0',
      'is_buy': '1',
      'is_open': '1',
      'exec_type': '9',
      'tif': '0',
      'status': '14',
      'trading_type': '0',
      'tradingday': '2018-09-01',
      'errorcode': '0'}

FuturexDB.insert.new_order_record(order_1, account_id, model_instance)

# update order_record_otc api
# OrderManagement | RiskManagement=>RiskMgt
# UpdateOrderStatus.py=> UpdateOrderStatus
FuturexDB.update.order_record_otc('status', '1', model_instance)

# update model_params api
# VolatilityModel
# ChangeParamData.py => Writeparamdata
FuturexDB.update.model_params('alpha','0','DCE','C','1')


# delete order api
# OrderManagement
# DelOrder.py => DelOrder
print(FuturexDB.delete.del_order(model_name, model_instance, account_id))

```
