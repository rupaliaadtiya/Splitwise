from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account import serializers, models

class AddUserApiView(APIView):
    serializer_class = serializers.AddUserSerializer
    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User added successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginApiView(APIView):
    serializer_class = serializers.LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            response_data = {
                'user_id': user.id,
                'email': user.email,
                'name': user.name,
                'refresh_token': serializer.validated_data['refresh_token'],
                'access_token': serializer.validated_data['access_token'],
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

