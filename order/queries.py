import graphene
from graphql_jwt.decorators import login_required
from .types import  OrderType


class OrderQuery(graphene.ObjectType):
    orders = graphene.List(OrderType)

    @login_required
    def resolve_orders(parent, info):
        user = info.context.user
        return user.orders.all()
        