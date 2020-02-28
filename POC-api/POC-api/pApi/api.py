from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class Clients(APIView):
	def get(self,request):
		data = clients.objects.all()
		serializer = ClientSerializer(data,many=True)
		return Response(serializer.data)
	def post(self, request):
		serializer = ClientSerializer(data=request.data)
		dbdata = clients.objects.all()
		print (request.data)
		currClient = request.data.get('client','')
		currPriorityS = request.data.get('priority','')
		currPriority = int(currPriorityS)
		if serializer.is_valid():
			#import pdb;pdb.set_trace()
			check = clients.objects.all().filter(client = currClient , priority = currPriority)
			if check.count() != 0 :
				for index ,  val in enumerate(clients.objects.all().order_by('priority')):
					
					if (val.client == currClient) and (val.priority >= currPriority):
						print(val.client, val.priority, '----',currClient,currPriority)
						check2 = clients.objects.all().filter(client = currClient , priority = val.priority+1)
						if(check2.count() == 0):
							val.priority += 1
							val.save()
							break;
							
						else :
							val.priority += 1
							val.save() 
					else:
						print(val.client, val.priority, '----else--',currClient,currPriority)

			serializer.save()
			return Response(serializer.data , status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
