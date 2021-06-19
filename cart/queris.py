import graphene
from graphql_jwt.decorators import login_required
from .types import CartType


class CartQuery(graphene.ObjectType):
    carts = graphene.Field(CartType)

    @login_required
    def resolve_carts(parent, info):
        return info.context.user
