# Trading tools and algorithms
Some trading tools implemented with Python > 3.9

## DISCLAIMER
Trading leveraged tools carries a high degree of risk and you could lose more than your initial deposit. Any code,opinions, chats, messages, news, research, analyses, prices, or other information contained on this repository are provided as general market information for educational and entertainment purposes only, and do not constitute investment advice neither investment assurance. The code in this repository should not be relied upon as a substitute for extensive independent market research before making your actual trading decisions.

THE AUTHOR OF THIS REPOSITORY will not accept liability for any loss or damage, including without limitation any loss of profit, which may arise directly or indirectly from use of THE CODE SOFTWARE WITHIN THIS REPOSITORY.

THE AUTHOR OF THIS REPOSITORY do not recommend the use of technical analysis as a sole means of trading decisions. THE AUTHOR OF THIS REPOSITORY do not recommend making hurried trading decisions. You should always understand that PAST PERFORMANCE IS NOT NECESSARILY INDICATIVE OF FUTURE RESULTS.


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

## LICENSE
Bracket Order Tool is part of tradingTools.

tradingTools is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

tradingTools is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with tradingTools. If not, see <https://www.gnu.org/licenses/>.

#### Author: Miguel Espiga


#### Copyright 2024 to the author Miguel Espiga. All Rights Reserved

