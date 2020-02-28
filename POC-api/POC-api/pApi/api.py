from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class Clients(APIView):
	#get api logic
	def get(self,request):
		#getting all the clients available in db
		data = clients.objects.all()
		serializer = ClientSerializer(data,many=True)
		return Response(serializer.data)
	#post api logic
	def post(self, request):
		serializer = ClientSerializer(data=request.data)
		dbdata = clients.objects.all()
		print (request.data)
		#currClient is client from request an currPriority is priority posted by user
		currClient = request.data.get('client','')
		currPriorityS = request.data.get('priority','')
		currPriority = int(currPriorityS)
		#if req valid
		if serializer.is_valid():
			#import pdb;pdb.set_trace()
			#check the request client is present in db or not
			check = clients.objects.all().filter(client = currClient , priority = currPriority)
			if check.count() != 0 :
				#loop through all clients order by priority
				for index ,  val in enumerate(clients.objects.all().order_by('priority')):
					#condition to exclude all lower priorities
					if (val.client == currClient) and (val.priority >= currPriority):
						print(val.client, val.priority, '----',currClient,currPriority)
						#check for last available slot of client list present 
						check2 = clients.objects.all().filter(client = currClient , priority = val.priority+1)
						if(check2.count() == 0):
							#increment priority of last client
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
