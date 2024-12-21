from database.connection import client


def get_data_by_ticker(ticker: str):
    result = client.query(f"SELECT * FROM records WHERE ticker = '{ticker}'")
    return result.result_rows