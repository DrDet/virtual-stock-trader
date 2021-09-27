import httpx
import xml.etree.ElementTree as ET

from vstrader.data import StockInfo


async def load_stock_info(ticker: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml?iss.meta=off&iss.only=securities&securities.columns=SECID,PREVADMITTEDQUOTE')
    respXml = ET.fromstring(resp.text)
    row = respXml.find(f".//row[@SECID='{ticker}']")
    if row is None:
        return None
    return StockInfo(ticker=ticker, price=row.attrib['PREVADMITTEDQUOTE'])
