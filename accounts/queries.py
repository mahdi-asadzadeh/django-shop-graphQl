from graphql_jwt.decorators import login_required
from .types import UserType
from .models import User
import graphene


class AccountsQuery(graphene.ObjectType):
    account = graphene.Field(UserType)

    @login_required
    def resolve_account(parent, info):
        user = info.context.user
        return User.objects.get(id=user.id)
        