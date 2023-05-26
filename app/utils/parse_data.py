from logging import getLogger, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel('INFO')

class Parser:
    """
    class for collecting and validation info from 'front'
    """
    def __init__(self):
        self.pair = None
        self.volume = None
        self.number = None
        self.amount_dif = None
        self.side = None
        self.price_min = None
        self.price_max = None


    def setup(self, response: dict):
        self.pair = response.get('pair')
        self.volume = response.get('volume')
        self.number = response.get('number')
        self.amount_dif = response.get('amountDif')
        self.side = response.get('side')
        self.price_min = response.get('priceMin')
        self.price_max = response.get('priceMax')
        self.validate()

    def validate(self):
        if not isinstance(self.pair, str):
            logger.error('Pair has no valid value')
            raise ValueError
        if not isinstance(self.volume, float):
            logger.error('Volume has no valid value')
            raise ValueError
        if not isinstance(self.number, int):
            logger.error('Number of orders has no valid value')
            raise ValueError
        if not isinstance(self.amount_dif, float):
            logger.error('Amount difference has no valid value')
            raise ValueError
        if not isinstance(self.side, str):
            logger.error('Side has no valid value')
            raise ValueError
        if not isinstance(self.price_min, float):
            logger.error('Price minimum has no valid value')
            raise ValueError
        if not isinstance(self.price_max, float):
            logger.error('Price maximum has no valid value')
            raise ValueError




