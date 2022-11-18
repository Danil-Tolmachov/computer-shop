from django.contrib.auth import login, get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from cart.models import Product, Category
from restapi.permissions import IsAdminOrReadOnly
from restapi.serializers import ProductSerializer, UserSerializer, UserUpdateSerializer


class ShopUserAuthentication(BasicAuthentication):
    def authenticate(self, request):
        user, _ = super(ShopUserAuthentication, self).authenticate(request)
        login(request, user)
        return user, _


#  Own token system view

# class LoginApiView(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (AllowAny,)
#
#     def get(self, request, format=None):
#         content = {
#             'user': str(request.user),  # `django.contrib.auth.User` instance.
#             'auth': str(request.auth),  # None
#         }
#
#         if request.auth:
#             return Response({'user': str(request.user)})
#         else:
#             return Response({'message': 'incorrect token'})
#
#     def post(self, request):
#         serializer = AuthSerializer(data=request.POST)
#
#         if not (str(request.user) == 'AnonymousUser'):
#             return Response({'message': 'you already authorized'})
#
#         if not serializer.is_valid():
#             return Response(serializer.errors)
#         username, password = serializer.data.values()
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             token = Token.objects.get_or_create(user=user)
#
#             return Response({'token': str(token)})
#
#        return Response({'message': 'invalid username or password'})


class ProductsApiViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(methods=['get'], detail=False)
    def category(self, request):
        category = Category.objects.all()
        return Response({'categories': (str(request.user), request.auth)})

    @action(methods=['get'], detail=True)
    def category_detail(self, request, pk=None):
        if pk:
            print('pk')
            category = Category.objects.get(pk=pk)
            return Response({'category': category.category_name})
        else:
            return Response({'message': 'no pk'})


class ShopUserAPIViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    user_model = get_user_model()

    def list_user(self, request):

        queryset = ShopUserAPIViewSet.user_model.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def detail_user(self, request, user_id):
        user = ShopUserAPIViewSet.user_model.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        fields_data = request.POST
        serializer = UserUpdateSerializer(data=fields_data)
        serializer.is_valid()

        user = ShopUserAPIViewSet.user_model.objects.filter(pk=user_id)

        if serializer.validated_data['is_active'] is None:
            del serializer.validated_data['is_active']

        user.update(**serializer.validated_data)
        return self.detail_user(request, user_id)

    def delete(self, request, user_id):
        try:
            user = ShopUserAPIViewSet.user_model.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return Response({'message': 'incorrect id'})

        serializer = UserSerializer(user)
        response = Response(serializer.data)

        try:
            ShopUserAPIViewSet.user_model.objects.get(pk=user_id).delete()
        except ObjectDoesNotExist:
            return Response({'message': 'user already deleted'})

        return response

