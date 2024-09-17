import asyncio
from datetime import datetime, timezone
import os
from binance_margin import BinanceMargin


def datetime_to_milliseconds(dt: datetime) -> int:
    return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

async def main():
    api_key = os.environ.get('BINANCE_API_KEY')
    secret_key = os.environ.get('SECRET_KEY')

    my_margin = BinanceMargin(is_isolated=True)
    await my_margin.initialize_client(api_key=api_key, api_secret=secret_key)

    res = await my_margin.open_market_position(symbol='XRPUSDT', side= 'SELL', quantity=10)
    print(res)

    res = await my_margin.margin_account_info()
    print(res)

    await my_margin.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())