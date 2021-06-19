import graphene
from graphql_jwt.decorators import login_required
from graphene.types.generic import GenericScalar

from django.contrib.contenttypes.models import ContentType

from .models import Comment
from product.models import Product
from blog.models import Article


class CommentInput(graphene.InputObjectType):
    rate = graphene.Int(required=True)
    parent_id = graphene.ID()
    object_id = graphene.ID(required=True)
    body = graphene.String(required=True)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    response = GenericScalar()

    @login_required
    def mutate(parent, info, id):
        try:
            user = info.context.user
            Comment.objects.get(id=id, user=user).delete()
            return DeleteComment(response={'status': 'success', 'message': 'delete comment.'})

        except Comment.DoesNotExist:
            return DeleteComment(response={'status': 'error', 'message': 'Comment does not exist.'})


class UpdateComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID()
        rate = graphene.Int()
        body = graphene.String()
    
    response = GenericScalar()

    @login_required
    def mutate(parent, info, comment_id, rate, body):
        try:
            user = info.context.user
            comment = Comment.objects.get(id=comment_id, user=user)
            comment.rate = rate or comment.rate
            comment.body = body or comment.body
            comment.save()
            return UpdateComment(response={'status': 'success', 'message': 'update comment.'})

        except Exception:
            return UpdateComment(response={'status': 'error', 'message': 'Data is invalid.'})


class CreateComment(graphene.Mutation):
    class Arguments:
        input = CommentInput(required=True)
        typename = graphene.String(required=True)

    response = GenericScalar()

    @login_required
    def mutate(parent, info, input, typename):
        if typename == 'ProductType':
            try:
                if input.parent_id:
                    comment_parent = Comment.objects.get(id=input.parent_id)
                else:
                    comment_parent = None
                user = info.context.user
                product = Product.objects.get(id=input.object_id)
                content_type = ContentType.objects.get_for_model(Product)
                Comment.objects.create(
                    parent=comment_parent,
                    content_type=content_type,
                    object_id=product.id,
                    rate=input.rate,
                    user=user,
                    body=input.body
                )
                product.numbers_rating += 1
                product.scope_avrage += int(input.rate)
                product.rating = product.scope_avrage / product.numbers_rating
                product.save()
                return CreateComment(response={'status': 'success', 'message': 'create comment.'})

            except Exception:
                return CreateComment(response={'status': 'error', 'message': 'Data is invalid.'})
        
        elif typename == 'ArticleType':
            try:
                if input.parent_id:
                    try:
                        comment_parent = Comment.objects.get(id=input.parent_id)
                    except Comment.DoesNotExist:
                        return CreateComment(response={'status': 'error', 'message': 'comment parent dose not exist.'})
                else:
                    comment_parent = None
                    
                user = info.context.user
                article = Article.objects.get(id=input.object_id)
                content_type = ContentType.objects.get_for_model(Article)
                Comment.objects.create(
                    parent=comment_parent,
                    content_type=content_type,
                    object_id=article.id,
                    rate=input.rate,
                    user=user,
                    body=input.body
                )
                article.numbers_rating += 1
                article.scope_avrage += int(input.rate)
                article.rating = article.scope_avrage / article.numbers_rating
                article.save()
                return CreateComment(response={'status': 'success', 'message': 'create comment.'})

            except Exception:
                return CreateComment(response={'status': 'error', 'message': 'Data is invalid.'})

        else:
            return CreateComment(response={'status': 'error', 'message': 'typename is not the found.'})


class CommentMutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
