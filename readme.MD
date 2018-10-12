
# Guosen Option Rds Tools

## Usages

- modify the config file `connection_info.json.bak` to `connection_info.json` and fill the info

## Cases

```python
from rds_tools.select import FuturexDB

# Reference Documents

# ALL SELECT
# > Volatility Model
# GetDataMySQL.py

print(FuturexDB.get_param_data('DCE', 'C').head())

print(FuturexDB.get_param_data_std('DCE', 'C'))

print(FuturexDB.get_future_info())

# PyMySQLreadZH.py

print(FuturexDB.get_exchange_zh('CBOE'))

print(FuturexDB.get_exchange_zh('LME'))

print(FuturexDB.get_contract_zh('CFFEX', 'T'))

# GetUnderling.py

print(FuturexDB.get_underlying())

print(FuturexDB.get_multiplier('rb'))

# > OptionCalc
# GetContract.py

print(FuturexDB.get_contract('DCE', 'C'))

# > OrderManagement
# GetModelParamName.py
# replace GetContract

print(FuturexDB.get_paramdef_by_model('ovo'))

# GetOrderList.py
# replace GetOrderList

print(FuturexDB.get_order_record_otc('13001'))

# GetOrderParam.py

print(FuturexDB.get_order_param('13001', 'ovo_13001_11005_1533785827.5574322'))


# GetRoleName.py

print(FuturexDB.get_role_by_name('13001'))

# GetRoletype.py | RiskManagement/GetRiskList.py/GetRiskList

print(FuturexDB.get_role_by_role_type('13'))

# risk list

print(FuturexDB.get_role_by_role_type('14'))


# > RiskManagement
# GetPoSymbol.py

print(FuturexDB.get_portfolio_by_id('12001'))


# GetRiskList.py

print(FuturexDB.get_order_by_risk_id('14001'))


# GetTraderId.py

# GetSlaveId

print(FuturexDB.get_account_id_map_by_master_id('14001'))

# GetTraderId

print(FuturexDB.get_trader_id_by_master_id('14001'))

# GetPortDetail.py
# GetPortDetail

print(FuturexDB.get_order_record_by_symbol_traderid('OTC-DCE-i', 12001))

# GetPortDetail2

print(FuturexDB.get_order_record_by_model_instance(
    'ovo_13001_11005_1533785827.5574322'))

# GetPortSub

print(FuturexDB.get_ref_contract())

# show the cache
print(FuturexDB._fxdb_cache)

# clear all cache

FuturexDB.clear_all_cache()

print(FuturexDB._fxdb_cache)

```
