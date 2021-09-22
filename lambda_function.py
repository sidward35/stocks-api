import json
from botocore.vendored import requests
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_json(ticker):
    output = {}
    output['ticker'] = ticker

    quote = requests.get('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token={TOKEN}')
    quote_json = json.loads(str(quote.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
    output['quote'] = quote_json
        
    aggr = requests.get('https://finnhub.io/api/v1/scan/technical-indicator?symbol='+ticker+'&resolution=D&token={TOKEN}')
    aggr_json = json.loads(str(aggr.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
    output['technicalAnalysis'] = aggr_json

    senti = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol='+ticker+'&token={TOKEN}')
    senti_json = json.loads(str(senti.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
    output['sentiment'] = senti_json
        
    fins = requests.get('https://finnhub.io/api/v1/stock/metric?symbol='+ticker+'&metric=all&token={TOKEN}')
    fins_json = json.loads(str(fins.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
    fins_json = fins_json["metric"]
    output['financials'] = fins_json

    return output
	
def lambda_handler(event, context):
	return get_json(event['symbol'])
