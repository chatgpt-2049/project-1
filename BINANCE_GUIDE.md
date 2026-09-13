# Binance Connector Documentation

## Overview

The **Binance Connector CLI** is a Python 3 command-line tool that provides easy access to the Binance Spot Trading API. It supports account management, market data retrieval, and trading operations.

## Installation

### Prerequisites
- Python 3.14+
- pip (Python package manager)

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your Binance API credentials
```

3. **Verify installation:**
```bash
python binance_connector.py --help
```

## Configuration

### Environment Variables

The connector uses the following environment variables (from GitHub Actions):

| Variable | Type | Description |
|----------|------|-------------|
| `BINANCE_API_KEY` | Secret | Your Binance API Key |
| `BINANCE_SECRET_KEY` | Secret | Your Binance API Secret |
| `BINANCE_ID_UID` | Variable | Your Binance Account UID |
| `BINANCE_UID_WALLET` | Variable | Your Binance Wallet UID |
| `BINANCE_API_LIST_IP` | Variable | IP whitelist for API access |

### Loading from .env File

Create a `.env` file in your project root:

```bash
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
BINANCE_ID_UID=your_uid
BINANCE_UID_WALLET=your_wallet_uid
BINANCE_API_LIST_IP=your_ip_list
```

## Usage

### Basic Commands

#### Get Account Information
```bash
python binance_connector.py account
```

Returns account details including balances, trading permissions, etc.

#### Check Balance
```bash
python binance_connector.py balance --asset USDT
python binance_connector.py balance --asset BTC
```

Get balance for a specific asset.

#### Get Ticker Price
```bash
python binance_connector.py ticker --symbol BTCUSDT
python binance_connector.py ticker --symbol ETHUSDT
```

Get current price for a trading pair.

#### Get All Ticker Prices
```bash
python binance_connector.py tickers
```

Get prices for all trading pairs.

#### View Order Book
```bash
python binance_connector.py order-book --symbol BTCUSDT --limit 10
```

Get the order book (bid/ask) for a trading pair.

### Trading Commands

#### Place a BUY Order (LIMIT)
```bash
python binance_connector.py order \
  --symbol BTCUSDT \
  --side BUY \
  --type LIMIT \
  --quantity 0.01 \
  --price 45000
```

#### Place a SELL Order (MARKET)
```bash
python binance_connector.py order \
  --symbol BTCUSDT \
  --side SELL \
  --type MARKET \
  --quantity 0.01
```

#### View Open Orders
```bash
python binance_connector.py open-orders
python binance_connector.py open-orders --symbol BTCUSDT
```

#### Cancel an Order
```bash
python binance_connector.py cancel-order --symbol BTCUSDT --order-id 12345
```

#### Get Trade History
```bash
python binance_connector.py trade-history --symbol BTCUSDT --limit 20
```

## Advanced Usage

### Using Testnet

Test your trading strategies on the Binance testnet without risking real funds:

```bash
python binance_connector.py --testnet account
python binance_connector.py --testnet balance --asset USDT
```

### Custom API Credentials

Override environment variables via command line:

```bash
python binance_connector.py --api-key YOUR_KEY --api-secret YOUR_SECRET account
```

### Python Integration

Use the `BinanceConnector` class in your Python scripts:

```python
from binance_connector import BinanceConnector

# Initialize connector
connector = BinanceConnector()

# Get account info
account = connector.get_account_info()
print(account)

# Check balance
balance = connector.get_balance("USDT")
print(balance)

# Place order
order = connector.place_order(
    symbol="BTCUSDT",
    side="BUY",
    type="LIMIT",
    quantity=0.01,
    price=45000
)
print(order)
```

## Supported Trading Pairs

Common Binance trading pairs (base/quote):

- **Bitcoin:** BTCUSDT, BTCBUSD
- **Ethereum:** ETHUSDT, ETHBUSD
- **Binance Coin:** BNBUSDT, BNBBUSD
- **Ripple:** XRPUSDT, XRPBUSD
- **Cardano:** ADAUSDT, ADABUSD
- **Solana:** SOLUSDT, SOLBUSD
- **Polkadot:** DOTUSDT, DOTBUSD
- **Dogecoin:** DOGEUSDT, DOGEBUSD
- **Litecoin:** LTCUSDT, LTCBUSD

For a complete list, visit: [Binance Trading Pairs](https://www.binance.com/en/trade)

## API Methods Reference

### Account Methods
- `get_account_info()` - Get account details
- `get_balance(asset)` - Get balance for specific asset

### Market Data Methods
- `get_ticker(symbol)` - Get price for one pair
- `get_all_tickers()` - Get prices for all pairs
- `get_order_book(symbol, limit)` - Get order book depth

### Trading Methods
- `place_order(symbol, side, type, quantity, price)` - Place order
- `get_open_orders(symbol)` - Get open orders
- `cancel_order(symbol, order_id)` - Cancel order
- `get_trade_history(symbol, limit)` - Get trade history

## Error Handling

The connector returns error responses in JSON format:

```json
{
  "error": "Error message description"
}
```

Common errors:
- **"BINANCE_API_KEY and BINANCE_SECRET_KEY must be set"** - Missing credentials
- **"Asset XXX not found"** - Asset not in your account
- **"Price required for LIMIT orders"** - Missing price parameter

## Security Best Practices

1. **Never commit credentials** - Use `.env` files and `.gitignore`
2. **Restrict API permissions** - Use IP whitelisting (BINANCE_API_LIST_IP)
3. **Enable 2FA** - On your Binance account
4. **Use API keys carefully** - Regenerate if compromised
5. **Monitor activity** - Check Binance API activity logs

## GitHub Actions Integration

Use this connector in your GitHub Actions workflows:

```yaml
- name: Run Binance Trading Bot
  env:
    BINANCE_API_KEY: ${{ secrets.BINANCE_API_KEY }}
    BINANCE_SECRET_KEY: ${{ secrets.BINANCE_SECRET_KEY }}
    BINANCE_ID_UID: ${{ vars.BINANCE_ID_UID }}
    BINANCE_UID_WALLET: ${{ vars.BINANCE_UID_WALLET }}
  run: |
    python binance_connector.py account
    python binance_connector.py balance --asset USDT
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'binance'"
```bash
pip install binance-connector python-binance
```

### "Authentication failed"
- Verify API Key and Secret are correct
- Check IP whitelist settings
- Ensure credentials are loaded from .env

### "Connection error"
- Check internet connection
- Verify Binance API status at https://status.binance.com
- Try using testnet

## Resources

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Binance Python Connector](https://github.com/binance/binance-connector-python)
- [Python Binance](https://github.com/sammchardy/python-binance)
- [Binance Trading Pairs](https://www.binance.com/en/trade)

## Support

For issues or questions:
1. Check the error message in the output
2. Review the [Binance API Documentation](https://binance-docs.github.io/apidocs/)
3. Open an issue in the GitHub repository

---

**Last Updated:** 2026-09-13
**Version:** 1.0.0
