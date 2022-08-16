from flask import Flask, Response
import requests
import json
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)


@app.route("/get_price/<ticker>")
def get_price(ticker):

    header = {
        'User-Agent': 'Mozilla/5.0'
    }
    """ comentario 1 """

    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}&lang=en-US&region=US&quotesCount=6&newsCount=2&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&enableCulturalAssets=true&researchReportsCount=2"
    response = requests.get(url, headers=header)
    app.logger.info(response)
    company_info = response.json()
    app.logger.info(f"Requested ticker: {ticker}")

    if response.status_code > 400:
        app.logger.info(f"Yahoo has problem with ticker: {ticker}.")
        app.logger.info(f"Yahoo status code: {response.status_code}.")
        return Response({}, status=404, mimetype='application/json')


    return Response(json.dumps(company_info), status=200, mimetype='application/json')

    """
    try:
        price = company_info['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
        company_name = company_info['quoteSummary']['result'][0]['price']['longName']
        exchange = company_info['quoteSummary']['result'][0]['price']['exchangeName']
        currency = company_info['quoteSummary']['result'][0]['price']['currency']

        result = {
            "price": price,
            "name": company_name,
            "exchange": exchange,
            "currency": currency
        }
        print(result)

        return Response(json.dumps(result), status=200, mimetype='application/json')
    except (KeyError, TypeError) as e:
        return Response(str(e), status=404, mimetype='application/json')
    except Exception as e:
        app.logger.info(str(e), exc_info=True)
    """


if __name__ == '__main__':
    app.run()
