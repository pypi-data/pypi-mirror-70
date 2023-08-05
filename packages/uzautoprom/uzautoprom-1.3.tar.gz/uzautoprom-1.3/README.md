## What's it?
It is a simple contracts loader with storage and filtering functionality for official UzAuto dealers.
## Basic use case
```python
from uzautoprom import InMemoryDB, RLoader, CField

import local_settings


db = InMemoryDB(
  RLoader(local_settings.LOGIN, local_settings.PASSWORD).contracts()
)

spark_contracts = db.contracts(
  CField("Модель", "SPARK")
)
print(spark_contracts)
```

## About
uzautoprom produce 3 abstract classes:
- [Field](https://github.com/IlhomBahoraliev/uzautoprom/blob/master/uzautoprom/abc/field.py) — representation of contract field used for flexible filtering
- [Database](https://github.com/IlhomBahoraliev/uzautoprom/blob/master/uzautoprom/abc/database.py) — storage and filter contracts
- [Loader](https://github.com/IlhomBahoraliev/uzautoprom/blob/master/uzautoprom/abc/loader.py) — load contracts
### Built-in realizations:
- [RLoader](https://github.com/IlhomBahoraliev/uzautoprom/blob/master/uzautoprom/rloader.py) - based on requests sessions loader
- [CField](https://github.com/IlhomBahoraliev/uzautoprom/blob/master/uzautoprom/cfield.py) - simple implementation of Field abc.
- [InMemoryDB](https://github.com/IlhomBahoraliev/uzautoprom/blob/master/uzautoprom/imdb.py) - simple in memory database.
## Install
```bash
pip install uzautoprom
```
