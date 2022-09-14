from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dishapp.models import Dishes,Reviews
from dishapp.serializer import DishSerializer,DishModelSerializer,UserSerializer,ReviewSerializer
from rest_framework import status
from rest_framework.viewsets import ViewSet,ModelViewSet
from django.contrib.auth.models import User
from rest_framework import  authentication,permissions
from rest_framework.decorators import action

#m Create your pviews here.

class DishView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        serializer=DishSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=DishSerializer(data=request.data)
        if serializer.is_valid():
            Dishes.objects.create(**serializer.validated_data)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DishDetailView(APIView):
    def get(self, request, *args, **kwargs):
        id=kwargs.get("id")
        qs=Dishes.objects.get(id=id)
        serializer=DishSerializer(qs)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        object=Dishes.objects.filter(id=id)
        serializer=DishSerializer(data=request.data)
        if serializer.is_valid():
            # object.name=serializer.validated_data.get("name")
            # object.price=serializer.validated_data.get("price")
            # object.category=serializer.validated_data.get("category")
            # object.rating=serializer.validated_data.get("rating")
            #
            # object.save()
            object.update(**serializer.validated_data)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        object=Dishes.objects.get(id=id)

        serializer=DishSerializer(object)  #Deserialization
        object.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


#model serializer

class DishModelView(APIView):

    def get(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        if "category" in request.query_params:
            qs=qs.filter(category=request.query_params.get("category"))  #category__contains=request.
        if "price_gt" in request.query_params:
            qs=qs.filter(price__gte=request.query_params.get("price_gt"))

        serializer=DishModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=DishModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DishDetailsModelView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Dishes.objects.get(id=id)
        serializer=DishModelSerializer(qs)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs): #update data
        id=kwargs.get("id")
        object=Dishes.objects.get(id=id)
        serializer=DishModelSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Dishes.objects.get(id=id)
        instance.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


#ViewSet

class DishViewSetView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        serializer=DishModelSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kwargs):
        serializer=DishModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Dishes.objects.get(id=id)
        serializer=DishModelSerializer(qs)
        return Response(data=serializer.data)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Dishes.objects.get(id=id)
        serializer=DishModelSerializer(instance=object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Dishes.objects.get(id=id)
        instance.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


#model view set view
class DishModelViewSetView(ModelViewSet):
    serializer_class = DishModelSerializer
    queryset = Dishes.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #api/v4/dishes/4/get_reviews
    @action(methods=["get"],detail=True)  #custom mthd
    def get_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        dish=Dishes.objects.get(id=id)
        reviews=dish.reviews_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data)

    #secnd ,worst case post
    @action(methods=["post"],detail=True)
    def post_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        dish=Dishes.objects.get(id=id)
        author=request.user
        serializer=ReviewSerializer(data=request.data,context={"author":author,"dish":dish})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    #first, best case post
    # @action(methods=["post"],detail=True)
    # def post_review(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     dish=Dishes.objects.get(id=id)
    #     author=request.user
    #     review=request.data.get("review")
    #     rating=request.data.get("rating")
    #     qs=Reviews.objects.create(author=author,
    #                               dish=dish,
    #                               review=review,
    #                               rating=rating)
    #     serializer=ReviewSerializer(qs)
    #     return Response(data=serializer.data)


class UserModelViewSetView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()