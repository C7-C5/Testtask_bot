import decimal
import os
import random
from binance.client import Client
from dotenv import load_dotenv
from utils.request import request
from utils.parse_data import Parser
from logging import getLogger, StreamHandler
from datetime import datetime

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel('INFO')
load_dotenv()


class Trader:
    """
    main script which places order(s) if collected data is valid and no exeptions was found
    flag self.stop blocks process of placing orders
    """
    def __init__(self):
        self.__api_key = os.getenv('API_KEY')
        self.__secret_key = os.getenv('SECRET_KEY')
        self.client = Client(api_key=self.__api_key, api_secret=self.__secret_key)
        self.data = Parser()
        self.stop = False

    def setup(self, response):
        """
        setting up validator
        :param response: usually response is a JSON file or something, but for simplification i use ordinary dict.
        Let's imagine, that i use json.loads() etc etc
        :return:
        """
        logger.info('Start setup data')
        try:
            self.data.setup(response)

        except Exception as e:
            error_message = self.error_handler(e)
            logger.error(error_message)
            self.stop = True


    def get_price(self):
        """
        collecting info about price of chosen trade pair
        """
        logger.info('Getting price for a trade pair')
        try:
            ticker = self.client.get_symbol_ticker(symbol=self.data.pair)
            pair_price = float(ticker['price'])

            if pair_price:
                return float(round(pair_price, 2))

        except Exception as e:
            error_message = self.error_handler(e)
            logger.error(error_message)
            self.stop = True

    def randomize_price(self, min_value, max_value):
        logger.info('Randomizing price')
        try:
            return float(round(random.uniform(min_value, max_value), 2))

        except Exception as e:
            error_message = self.error_handler(e)
            logger.error(error_message)
            self.stop = True

    def amount_calculation(self, amount, btc_price):
        """
        calculating order qty
        :param amount: order qty in USDT
        :param btc_price:
        :return: order qty in BTC or other coin
        """
        logger.info('Calculating amount of order')
        try:
            return float(round((amount / btc_price), 2))
        except Exception as e:
            error_message = self.error_handler(e)
            logger.error(error_message)
            self.stop = True

    def randomize_amount(self, volume, difference):
        logger.info('Randomizing amount')
        try:
            result = random.uniform(volume - difference, volume + difference)

            return float(round(result, 2))

        except Exception as e:
            error_message = self.error_handler(e)
            logger.error(error_message)
            self.stop = True

    def calculate_volume(self, volume, divider):
        logger.info('Calculating volume for order')
        try:
            return volume / divider

        except Exception as e:
            error_message = self.error_handler(e)
            logger.error(error_message)
            self.stop = True

    def set_price(self, main_value, additional_value):
        """
        Calculating price for placing an order
        :param main_value: current price of token
        :param additional_value: correction value
        :return:
        """
        logger.info('Setting price conditions for order')
        try:
            return float(round((main_value + additional_value), 2))

        except Exception as e:
            error_message = self.error_handler(e)
            logger.error(error_message)
            self.stop = True

    def error_handler(self, error):
        """
        function for an error message formatting
        """
        return f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ::: {error.__class__} ::: {error}'

    def place_orders(self):
        """
        main function that sync all others and places trading orders if stop flag wasn't initiated
        :return:
        """
        logger.info('Placing orders')
        order_volume = self.calculate_volume(self.data.volume, self.data.number)
        pair_price = self.get_price()
        minimal_price = self.set_price(pair_price, self.data.price_min)
        maximal_price = self.set_price(pair_price, self.data.price_max)

        if not self.stop:
            try:

                for i in range(self.data.number):
                    price = self.randomize_price(minimal_price, maximal_price)
                    order_amount_in_usd = self.randomize_amount(order_volume, self.data.amount_dif)
                    order_amount = self.amount_calculation(order_amount_in_usd, price)

                    order = self.client.create_test_order(
                        symbol=self.data.pair,
                        side=Client.SIDE_SELL if self.data.side == 'SELL' else Client.SIDE_BUY,
                        type=Client.ORDER_TYPE_LIMIT,
                        timeInForce=Client.TIME_IN_FORCE_GTC,
                        quantity=order_amount,
                        price=price
                    )
                    logger.info(f'Placed order: {order}')

            except Exception as e:
                error_message = self.error_handler(e)
                logger.error(error_message)
                self.stop = True


if __name__ == '__main__':
    trader = Trader()
    trader.setup(request)
    trader.place_orders()






