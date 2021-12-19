import databases
import sqlalchemy

database = None
stock_positions = None
portfolios = None


def prepare_database(db_connect_url):
    global database, stock_positions, portfolios

    database = databases.Database(db_connect_url)
    metadata = sqlalchemy.MetaData()
    engine = sqlalchemy.create_engine(
        db_connect_url
    )
    stock_positions = sqlalchemy.Table("StockPositions", metadata, autoload_with=engine)
    portfolios = sqlalchemy.Table("Portfolios", metadata, autoload_with=engine)
