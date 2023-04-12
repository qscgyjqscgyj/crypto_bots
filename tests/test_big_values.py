import asyncio
import unittest
from unittest.mock import MagicMock, patch
from bots.big_values import (
    get_all_usdt_tickers,
    get_klines_average_volume,
    get_order_book_high_values,
)


class TestBinanceFunctions(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()

    def test_get_all_usdt_tickers(self):
        self.client.get_all_tickers.return_value = [
            {"symbol": "BTCUSDT", "price": "50000.0"},
            {"symbol": "ETHUSDT", "price": "4000.0"},
            {"symbol": "ADAUSDT", "price": "2.0"},
            {"symbol": "SOLUSDT", "price": "50.0"},
            {"symbol": "XRPUSDT", "price": "1.0"},
            {"symbol": "DOGEUSDT", "price": "0.2"},
            {"symbol": "BUSDUSDT", "price": "1.0"},
            {"symbol": "USDTBUSD", "price": "1.0"},
            {"symbol": "BNBBUSD", "price": "500.0"},
            {"symbol": "BUSD", "price": "1.0"},
        ]

        usdt_tickers = get_all_usdt_tickers(self.client)

        self.assertEqual(len(usdt_tickers), 7)

    # @patch("bots.big_values.MIN_ORDER_VALUE", 100)
    # @patch("bots.big_values.THRESHOLD_PERCENT", 0.5 / 100)
    # def test_get_order_book_high_values(self):
    #     order_book = {
    #         "bids": [
    #             ["100", "1"],
    #             ["99", "2"],
    #             ["98", "3"],
    #         ],
    #         "asks": [
    #             ["102", "4"],
    #             ["103", "5"],
    #             ["104", "6"],
    #         ],
    #     }
    #     current_price = 101
    #     expected_high_values = [
    #         {"position": "LONG", "value": 10000.0, "price": "100"},
    #         {"position": "SHORT", "value": 408.0, "price": "104"},
    #     ]

    #     high_values = get_order_book_high_values(order_book, current_price)

    #     for high_value in high_values:
    #         self.assertIn(high_value, expected_high_values)

    @patch("my_module.time")
    @patch("my_module.Client.futures_klines")
    async def test_returns_correct_average_volume(self, mock_klines, mock_time):
        # Arrange
        mock_klines.return_value = [
            [
                0,
                "1.0",
                "2.0",
                "3.0",
                "4.0",
                "5.0",
                "6.0",
                "7.0",
                "8.0",
                "9.0",
                "10.0",
                "11.0",
                "12.0",
                "13.0",
                "14.0",
                "15.0",
                "16.0",
                "17.0",
                "18.0",
                "19.0",
                "20.0",
                "21.0",
                "22.0",
            ]
        ]
        mock_time.return_value = 1618556147000  # Some arbitrary timestamp
        expected_average_volume = 7.0

        client_mock = MagicMock()

        # Act
        result = await get_klines_average_volume(client_mock, {"symbol": "BTCUSDT"})

        # Assert
        self.assertEqual(result, expected_average_volume)
