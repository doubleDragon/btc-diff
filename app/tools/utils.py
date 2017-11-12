#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import division

import time

from app.api import bfxClient, btbClient
from .rate import Rate

krw_rate_cache = None
krw_rate_last = 0


def get_krw_rate():
    global krw_rate_cache, krw_rate_last

    diff = time.time() - krw_rate_last
    if not krw_rate_cache or (diff < 60 * 60 * 12):
        krw_rate_cache = Rate().query(target='KRW')
        krw_rate_last = time.time()
    if not krw_rate_cache:
        krw_rate_cache = 1300.0
    return krw_rate_cache


def get_diff():
    krw_rate = Rate().query(target='KRW')

    symbol = 'ethusd'
    currency = 'eth'
    t_bfx = bfxClient.ticker(symbol)
    t_btb = btbClient.ticker(currency)

    result = {}
    if t_bfx:
        result['bfx'] = {
            'bid': float(t_bfx['bid']),
            'ask': float(t_bfx['ask'])
        }
    else:
        result['bfx'] = {
            'bid': .0,
            'ask': .0
        }
    if t_btb and 'data' in t_btb:
        t_btb = t_btb['data']
        result['btb'] = {
            'bid': round(float(t_btb['buy_price']) / krw_rate, 2),
            'ask': round(float(t_btb['sell_price']) / krw_rate, 2)
        }
    else:
        result['btb'] = {
            'bid': .0,
            'ask': .0
        }

    bfx_bid = result['bfx']['bid']
    bfx_ask = result['bfx']['ask']

    btb_bid = result['btb']['bid']
    btb_ask = result['btb']['ask']

    result['diff'] = {}
    if bfx_ask > 0.0:
        result['diff']['bfx'] = round((btb_bid - bfx_ask) / bfx_ask * 100, 2)

    if btb_ask > 0.0:
        result['diff']['btb'] = round((bfx_bid - btb_ask) / btb_ask * 100, 2)

    return result
