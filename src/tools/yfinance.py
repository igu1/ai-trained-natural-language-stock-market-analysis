import json
import requests
import yfinance as yf


def get_current_stock_price(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.info.get(
            "regularMarketPrice", stock.info.get("currentPrice")
        )
        return (
            f"{current_price:.4f}"
            if current_price
            else f"Could not fetch current price for {symbol}"
        )
    except Exception as e:
        return f"Error fetching current price for {symbol}: {e}"


def get_company_info(symbol: str) -> str:
    try:
        company_info_full = yf.Ticker(symbol).info
        if company_info_full is None:
            return f"Could not fetch company info for {symbol}"

        company_info_cleaned = {
            "Name": company_info_full.get("shortName"),
            "Symbol": company_info_full.get("symbol"),
            "Current Stock Price": f"{company_info_full.get('regularMarketPrice', company_info_full.get('currentPrice'))} {company_info_full.get('currency', 'USD')}",
            "Market Cap": f"{company_info_full.get('marketCap', company_info_full.get('enterpriseValue'))} {company_info_full.get('currency', 'USD')}",
            "Sector": company_info_full.get("sector"),
            "Industry": company_info_full.get("industry"),
            "Address": company_info_full.get("address1"),
            "City": company_info_full.get("city"),
            "State": company_info_full.get("state"),
            "Zip": company_info_full.get("zip"),
            "Country": company_info_full.get("country"),
            "EPS": company_info_full.get("trailingEps"),
            "P/E Ratio": company_info_full.get("trailingPE"),
            "52 Week Low": company_info_full.get("fiftyTwoWeekLow"),
            "52 Week High": company_info_full.get("fiftyTwoWeekHigh"),
            "50 Day Average": company_info_full.get("fiftyDayAverage"),
            "200 Day Average": company_info_full.get("twoHundredDayAverage"),
            "Website": company_info_full.get("website"),
            "Summary": company_info_full.get("longBusinessSummary"),
            "Analyst Recommendation": company_info_full.get("recommendationKey"),
            "Number Of Analyst Opinions": company_info_full.get(
                "numberOfAnalystOpinions"
            ),
            "Employees": company_info_full.get("fullTimeEmployees"),
            "Total Cash": company_info_full.get("totalCash"),
            "Free Cash flow": company_info_full.get("freeCashflow"),
            "Operating Cash flow": company_info_full.get("operatingCashflow"),
            "EBITDA": company_info_full.get("ebitda"),
            "Revenue Growth": company_info_full.get("revenueGrowth"),
            "Gross Margins": company_info_full.get("grossMargins"),
            "Ebitda Margins": company_info_full.get("ebitdaMargins"),
        }
        return json.dumps(company_info_cleaned, indent=2)
    except Exception as e:
        return f"Error fetching company profile for {symbol}: {e}"


def get_historical_stock_prices(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        historical_price = stock.history(period="1mo", interval="1w")
        return historical_price.to_json(orient="index")
    except Exception as e:
        return f"Error fetching historical prices for {symbol}: {e}"

def get_stock_fundamentals(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        fundamentals = {
            "symbol": symbol,
            "company_name": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("forwardPE", "N/A"),
            "pb_ratio": info.get("priceToBook", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "beta": info.get("beta", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        }
        return json.dumps(fundamentals, indent=2)
    except Exception as e:
        return f"Error getting fundamentals for {symbol}: {e}"


def get_income_statements(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        financials = stock.financials
        return financials.to_json(orient="index")
    except Exception as e:
        return f"Error fetching income statements for {symbol}: {e}"


def get_key_financial_ratios(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        key_ratios = stock.info
        return json.dumps(key_ratios, indent=2)
    except Exception as e:
        return f"Error fetching key financial ratios for {symbol}: {e}"


def get_analyst_recommendations(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        recommendations = stock.recommendations
        return recommendations.to_json(orient="index")
    except Exception as e:
        return f"Error fetching analyst recommendations for {symbol}: {e}"


def get_company_news(symbol: str) -> str:

    try:
        news = yf.Ticker(symbol).news
        return json.dumps(news[:3], indent=2)
    except Exception as e:
        return f"Error fetching company news for {symbol}: {e}"


def get_technical_indicators(symbol: str) -> str:
    try:
        indicators = yf.Ticker(symbol).history(period="1mo")
        return indicators.to_json(orient="index")
    except Exception as e:
        return f"Error fetching technical indicators for {symbol}: {e}"


def get_ticker_by_name(company_name: str) -> str:
    try:
        search_url = f"https://query1.finance.yahoo.com/v1/finance/search"
        params = {
            "q": company_name,
            "quotesCount": 1,
            "newsCount": 0,
            "fields": "symbol",
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, params=params, headers=headers)
        data = response.json()
        print(data["quotes"][0]["symbol"])
        if "quotes" in data and data["quotes"]:
            return data["quotes"][0]["symbol"]
        else:
            return None
    except Exception as e:
        return f"Error fetching ticker for {company_name}: {e}"
