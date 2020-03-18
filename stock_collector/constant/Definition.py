class ColumnsDefinition:
    DATE = '日付'
    OPENING_PRICE = '始値'
    CLOSING_PRICE = '終値'
    HIGH_PRICE = '高値'
    LOW_PRICE = '安値'


class UrlsDefinition:
    kabutan_jp = {
        'url': 'https://kabutan.jp/stock/kabuka?code={stock_code}&ashi={period}&page={offset}',
        'next_page': 'https://kabutan.jp/stock/kabuka{next_page}'
    }


class PeriodDefinition:
    period = {
        'daily': 'day',
        'weekly': 'wek',
        'monthly': 'mon',
        'yearly': 'yar'
    }
