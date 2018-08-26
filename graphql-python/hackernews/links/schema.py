import graphene
from graphene_django import DjangoObjectType

from .models import Link

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

#Defines a mutation class, data server can send to client after mutation
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    #2Defines the data you can send to the server
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3The mutation method
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )
#Creates a mutation class with a field to be resolved
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()