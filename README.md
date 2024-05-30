# Trading tools and algorithms
Some trading tools implemented with Python > 3.9

## Bracket Order Tool
### Description
* This is a graphic tool that enables you to create strock orders with stop loss and sell strike limits.
It saves the order ids in a local database.
* After creating an order you can edit it:
   *  update the stop loss 
   *  update the sell strike
   *  cancel stop loss and sell at current market value 

### Setup
* You need to have an alpaca account in order to use/test. You can create a free paper account at https://alpaca.market

* Alpaca credentials must be set as environment variables:
`export APCA_API_KEY_ID=<your_api_key>`
`export APCA_API_SECRET_KEY=<your_secret_key>`
`export APCA_API_BASE_URL=https://paper-api.alpaca.markets`

* It's required to pip install the following python dependencies:
   * alpaca_trade_api
   * guizero
   * sqlite3

### Test
A test function is available in the non graphical files, so dependencies (alpaca api / database interface) can be tested in isolation.

Note: You can change the sqlite database path ``DB_PATH`` in the file `model/OrderDatabase.py`

