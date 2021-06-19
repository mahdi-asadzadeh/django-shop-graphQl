import graphene
from graphql_jwt import mutations
from product.queries import ProductQuery
from comment.mutations import CommentMutation
from accounts.mutations import AccountsMutation
from accounts.queries import AccountsQuery
from category.queries import CategoryQuery
from cart.queris import CartQuery
from cart.mutations import CartMutation
from order.queries import OrderQuery
from order.mutations import OrderMutations
from search.queries import SearchQuery
from blog.querice import ArticleQuery


class Query(ArticleQuery, SearchQuery, OrderQuery, CartQuery, CategoryQuery, AccountsQuery, ProductQuery, graphene.ObjectType):
    pass


class Mutation(OrderMutations, CartMutation, CommentMutation, AccountsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
