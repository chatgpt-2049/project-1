#!/usr/bin/env python3
"""
Binance Connector CLI - Python 3
Connect to Binance API and execute trading operations
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from binance.spot import Spot
from binance.lib.utils import config_logging

# Load environment variables
load_dotenv()

# Configure logging
config_logging(logging_level="INFO")


class BinanceConnector:
    """Binance API Connector Class"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        testnet: bool = False
    ):
        """
        Initialize Binance Connector
        
        Args:
            api_key: Binance API Key (or from env: BINANCE_API_KEY)
            api_secret: Binance API Secret (or from env: BINANCE_SECRET_KEY)
            testnet: Use testnet (default: False)
        """
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_SECRET_KEY")
        self.uid = os.getenv("BINANCE_ID_UID")
        self.wallet_uid = os.getenv("BINANCE_UID_WALLET")
        self.ip_list = os.getenv("BINANCE_API_LIST_IP")
        self.testnet = testnet

        if not self.api_key or not self.api_secret:
            raise ValueError("BINANCE_API_KEY and BINANCE_SECRET_KEY must be set")

        # Initialize Spot client
        if testnet:
            self.client = Spot(
                api_key=self.api_key,
                api_secret=self.api_secret,
                base_url="https://testnet.binance.vision"
            )
        else:
            self.client = Spot(
                api_key=self.api_key,
                api_secret=self.api_secret
            )

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        try:
            response = self.client.account()
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_balance(self, asset: str = "USDT") -> Dict[str, Any]:
        """Get balance for specific asset"""
        try:
            account = self.client.account()
            for balance in account["balances"]:
                if balance["asset"] == asset:
                    return {
                        "asset": asset,
                        "free": balance["free"],
                        "locked": balance["locked"]
                    }
            return {"error": f"Asset {asset} not found"}
        except Exception as e:
            return {"error": str(e)}

    def get_ticker(self, symbol: str = "BTCUSDT") -> Dict[str, Any]:
        """Get ticker price for a symbol"""
        try:
            response = self.client.ticker_price(symbol=symbol)
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_all_tickers(self) -> Dict[str, Any]:
        """Get all ticker prices"""
        try:
            response = self.client.ticker_price()
            return {"symbols": response, "count": len(response)}
        except Exception as e:
            return {"error": str(e)}

    def get_order_book(self, symbol: str = "BTCUSDT", limit: int = 5) -> Dict[str, Any]:
        """Get order book for a symbol"""
        try:
            response = self.client.depth(symbol=symbol, limit=limit)
            return response
        except Exception as e:
            return {"error": str(e)}

    def place_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Place an order
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            type: LIMIT or MARKET
            quantity: Order quantity
            price: Price (required for LIMIT orders)
        """
        try:
            if type == "LIMIT" and price is None:
                return {"error": "Price required for LIMIT orders"}

            params = {
                "symbol": symbol,
                "side": side,
                "type": type,
                "quantity": quantity
            }

            if type == "LIMIT":
                params["price"] = price
                params["timeInForce"] = "GTC"

            response = self.client.new_order(**params)
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_open_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get open orders"""
        try:
            if symbol:
                response = self.client.get_open_orders(symbol=symbol)
            else:
                response = self.client.get_open_orders()
            return {"orders": response, "count": len(response)}
        except Exception as e:
            return {"error": str(e)}

    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Cancel an order"""
        try:
            response = self.client.cancel_order(symbol=symbol, orderId=order_id)
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_trade_history(self, symbol: str, limit: int = 10) -> Dict[str, Any]:
        """Get trade history"""
        try:
            response = self.client.my_trades(symbol=symbol, limit=limit)
            return {"trades": response, "count": len(response)}
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Binance Connector CLI - Python 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python binance_connector.py account
  python binance_connector.py balance --asset USDT
  python binance_connector.py ticker --symbol BTCUSDT
  python binance_connector.py order-book --symbol ETHUSDT --limit 10
  python binance_connector.py tickers
  python binance_connector.py open-orders
  python binance_connector.py trade-history --symbol BTCUSDT
        """
    )

    parser.add_argument("--testnet", action="store_true", help="Use testnet")
    parser.add_argument("--api-key", help="Binance API Key")
    parser.add_argument("--api-secret", help="Binance API Secret")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Account info
    subparsers.add_parser("account", help="Get account information")

    # Balance
    balance_parser = subparsers.add_parser("balance", help="Get balance")
    balance_parser.add_argument("--asset", default="USDT", help="Asset symbol")

    # Ticker
    ticker_parser = subparsers.add_parser("ticker", help="Get ticker price")
    ticker_parser.add_argument("--symbol", default="BTCUSDT", help="Trading pair")

    # All tickers
    subparsers.add_parser("tickers", help="Get all ticker prices")

    # Order book
    orderbook_parser = subparsers.add_parser("order-book", help="Get order book")
    orderbook_parser.add_argument("--symbol", default="BTCUSDT", help="Trading pair")
    orderbook_parser.add_argument("--limit", type=int, default=5, help="Order book depth")

    # Place order
    order_parser = subparsers.add_parser("order", help="Place an order")
    order_parser.add_argument("--symbol", required=True, help="Trading pair")
    order_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    order_parser.add_argument("--type", required=True, choices=["LIMIT", "MARKET"], help="Order type")
    order_parser.add_argument("--quantity", type=float, required=True, help="Order quantity")
    order_parser.add_argument("--price", type=float, help="Order price (for LIMIT orders)")

    # Open orders
    open_orders_parser = subparsers.add_parser("open-orders", help="Get open orders")
    open_orders_parser.add_argument("--symbol", help="Trading pair (optional)")

    # Cancel order
    cancel_parser = subparsers.add_parser("cancel-order", help="Cancel an order")
    cancel_parser.add_argument("--symbol", required=True, help="Trading pair")
    cancel_parser.add_argument("--order-id", type=int, required=True, help="Order ID")

    # Trade history
    history_parser = subparsers.add_parser("trade-history", help="Get trade history")
    history_parser.add_argument("--symbol", required=True, help="Trading pair")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of trades")

    args = parser.parse_args()

    try:
        # Initialize connector
        connector = BinanceConnector(
            api_key=args.api_key,
            api_secret=args.api_secret,
            testnet=args.testnet
        )

        result = None

        if args.command == "account":
            result = connector.get_account_info()
        elif args.command == "balance":
            result = connector.get_balance(args.asset)
        elif args.command == "ticker":
            result = connector.get_ticker(args.symbol)
        elif args.command == "tickers":
            result = connector.get_all_tickers()
        elif args.command == "order-book":
            result = connector.get_order_book(args.symbol, args.limit)
        elif args.command == "order":
            result = connector.place_order(
                args.symbol,
                args.side,
                args.type,
                args.quantity,
                args.price
            )
        elif args.command == "open-orders":
            result = connector.get_open_orders(args.symbol)
        elif args.command == "cancel-order":
            result = connector.cancel_order(args.symbol, args.order_id)
        elif args.command == "trade-history":
            result = connector.get_trade_history(args.symbol, args.limit)
        else:
            parser.print_help()
            sys.exit(0)

        # Print result
        print(json.dumps(result, indent=2))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
