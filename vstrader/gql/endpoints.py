import strawberry
from strawberry.asgi import GraphQL

from vstrader import portfolio_manager
from vstrader.gql import data as gql


@strawberry.type
class Query:
    @strawberry.field
    async def portfolio(self, user_id: int) -> gql.Portfolio:
        portfolio_data = await portfolio_manager.load_portfolio(user_id)
        return gql.Portfolio(portfolio_data)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)
