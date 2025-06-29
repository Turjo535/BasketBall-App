from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Player
from UserAccount.models import User
from .serializers import Player_Information_Serializers,Report_Serializers
from UserAccount.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permission import Is_Player, Is_Coach
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.

class Player_Information_View(APIView):
    
    permission_classes=[Is_Player, IsAuthenticated]

    def post(self, request):
        
        serializer = Player_Information_Serializers(data=request.data)
        print(serializer)
        print(request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response("Player information saved successfully.", status=201)
        else:
            return Response(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ReportView(APIView):
    permission_classes=[Is_Player,IsAuthenticated]
    def get(self, request):
        # Render empty form
        return render(request, 'report_form.html')
    def post(self, request):
        serializer=Report_Serializers(data=request.data)
        print(serializer)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response("Player Report saved successfully.", status=201)
            # return render(request, 'report_form.html', {
            #     'message': 'Player Report saved successfully!'
            # })
        else:
            return Response(serializer.errors, status=400 )