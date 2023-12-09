import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List
import service.userservice as users

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

@strawberry.type
class User:
    id: int
    name: str
    email: str
    date: str    

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        userlst = []
        dbuser = users.list_users(100)
        for user_data in dbuser:
            user = User(id=user_data["id"], name=user_data["name"], email=user_data["email"], date=user_data["date"])
            userlst.append(user)
        return userlst

schema = strawberry.Schema(Query)


graphql_app = GraphQLRouter(schema)