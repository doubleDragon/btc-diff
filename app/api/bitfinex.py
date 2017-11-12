# coding=utf-8
from __future__ import absolute_import
import requests


PROTOCOL = "https"
HOST = "api.bitfinex.com"
VERSION = "v1"

PATH_SYMBOLS = "symbols"
PATH_TICKER = "ticker/%s"
PATH_TODAY = "today/%s"
PATH_STATS = "stats/%s"
PATH_LENDBOOK = "lendbook/%s"
PATH_ORDERBOOK = "book/%s"

# HTTP request timeout in seconds
TIMEOUT = 5.0


class PublicClient(object):
    """
    Client for the bitfinex.com API.
    See https://www.bitfinex.com/pages/api for API documentation.
    """

    @classmethod
    def server(cls):
        return u"{0:s}://{1:s}/{2:s}".format(PROTOCOL, HOST, VERSION)

    def url_for(self, path, path_arg=None, parameters=None):

        # build the basic url
        url = "%s/%s" % (self.server(), path)

        # If there is a path_arh, interpolate it into the URL.
        # In this case the path that was provided will need to have string
        # interpolation characters in it, such as PATH_TICKER
        if path_arg:
            url = url % (path_arg)

        # Append any parameters to the URL.
        if parameters:
            url = "%s?%s" % (url, self._build_parameters(parameters))

        return url

    def symbols(self):
        """
        GET /symbols
        curl https://api.bitfinex.com/v1/symbols
        ['btcusd','ltcusd','ltcbtc']
        """
        return self._get(self.url_for(PATH_SYMBOLS))

    def ticker(self, symbol):
        """
        GET /ticker/:symbol
        curl https://api.bitfinex.com/v1/ticker/btcusd
        {
            'ask': '562.9999',
            'timestamp': '1395552290.70933607',
            'bid': '562.25',
            'last_price': u'562.25',
            'mid': u'562.62495'}
        """
        data = self._get(self.url_for(PATH_TICKER, symbol))

        # convert all values to floats
        if data:
            return self._convert_to_floats(data)

    def today(self, symbol):
        """
        GET /today/:symbol
        curl "https://api.bitfinex.com/v1/today/btcusd"
        {"low":"550.09","high":"572.2398","volume":"7305.33119836"}
        """

        data = self._get(self.url_for(PATH_TODAY, (symbol)))

        # convert all values to floats
        return self._convert_to_floats(data)

    def lendbook(self, currency, parameters=None):
        """
        curl "https://api.bitfinex.com/v1/lendbook/btc"
        {"bids":[{"rate":"5.475","amount":"15.03894663","period":30,"timestamp":"1395112149.0","frr":"No"},{"rate":"2.409","amount":"14.5121868","period":7,"timestamp":"1395497599.0","frr":"No"}],"asks":[{"rate":"6.351","amount":"15.5180735","period":5,"timestamp":"1395549996.0","frr":"No"},{"rate":"6.3588","amount":"626.94808249","period":30,"timestamp":"1395400654.0","frr":"Yes"}]}
        Optional parameters
        limit_bids (int): Optional. Limit the number of bids (loan demands) returned.
        May be 0 in which case the array of bids is empty. Default is 50.
        limit_asks (int): Optional. Limit the number of asks (loan offers) returned.
        May be 0 in which case the array of asks is empty. Default is 50.
        """
        return self._get(self.url_for(PATH_LENDBOOK, path_arg=currency, parameters=parameters))

    def depth(self, symbol, parameters=None):
        """
        curl "https://api.bitfinex.com/v1/book/btcusd"
        {"bids":[{"price":"561.1101","amount":"0.985","timestamp":"1395557729.0"}],"asks":[{"price":"562.9999","amount":"0.985","timestamp":"1395557711.0"}]}
        The 'bids' and 'asks' arrays will have multiple bid and ask dicts.
        Optional parameters
        limit_bids (int): Optional. Limit the number of bids returned.
        May be 0 in which case the array of bids is empty. Default is 50.
        limit_asks (int): Optional. Limit the number of asks returned.
        May be 0 in which case the array of asks is empty. Default is 50.
        eg.
        curl "https://api.bitfinex.com/v1/book/btcusd?limit_bids=1&limit_asks=0"
        {"bids":[{"price":"561.1101","amount":"0.985","timestamp":"1395557729.0"}],"asks":[]}
        """
        if not parameters:
            parameters = {
                'limit_bids': 5,
                'limit_asks': 5
            }
        return self._get(self.url_for(PATH_ORDERBOOK, path_arg=symbol, parameters=parameters))
        # data = self._get(self.url_for(PATH_ORDERBOOK, path_arg=symbol, parameters=parameters))
        #
        # for type_ in data.keys():
        #     for list_ in data[type_]:
        #         for key, value in list_.items():
        #             list_[key] = float(value)
        #
        # return data

    @classmethod
    def _convert_to_floats(cls, data):
        """
        Convert all values in a dict to floats
        """
        for key, value in data.items():
            data[key] = float(value)

        return data

    @classmethod
    def _get(cls, url):
        try:
            resp = requests.get(url, timeout=TIMEOUT)
        except requests.exceptions.RequestException as e:
            print("bitfinex get %s failed: " % url + str(e))
        else:
            if resp.status_code == requests.codes.ok:
                return resp.json()

    @classmethod
    def _build_parameters(cls, parameters):
        # sort the keys so we can test easily in Python 3.3 (dicts are not
        # ordered)
        keys = list(parameters.keys())
        keys.sort()

        return '&'.join(["%s=%s" % (k, parameters[k]) for k in keys])