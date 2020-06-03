from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from collections import defaultdict
from django.apps import apps



#class BulkCreateManager(object):
#    """
#    This helper class keeps track of ORM objects to be created for multiple
#    model classes, and automatically creates those objects with `bulk_create`
#    when the number of objects accumulated for a given model class exceeds
#    `chunk_size`.
#    Upon completion of the loop that's `add()`ing objects, the developer must
#    call `done()` to ensure the final set of objects is created for all models.
#    """

#    def __init__(self, chunk_size=100):
#        self._create_queues = defaultdict(list)
#        self.chunk_size = chunk_size

#    def _commit(self, model_class):
#        model_key = model_class._meta.label
#        model_class.objects.bulk_create(self._create_queues[model_key])
#        self._create_queues[model_key] = []

#    def add(self, obj):
#        """
#        Add an object to the queue to be created, and call bulk_create if we
#        have enough objs.
#        """
#        model_class = type(obj)
#        model_key = model_class._meta.label
#        self._create_queues[model_key].append(obj)
#        if len(self._create_queues[model_key]) >= self.chunk_size:
#            self._commit(model_class)

#    def done(self):
#        """
#        Always call this upon completion to make sure the final partial chunk
#        is saved.
#        """
#        for model_name, objs in self._create_queues.items():
#            if len(objs) > 0:
#                self._commit(apps.get_model(model_name))


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
			check = clients.objects.all().filter(client=currClient,priority=currPriority)
			if check.count() != 0 :
				#bulk_mgr = BulkCreateManager(chunk_size=20)
				#loop through all clients order by priority
				for index ,  val in enumerate(clients.objects.all().order_by('priority')):
					#condition to exclude all lower priorities
					if (val.client == currClient) and (val.priority >= currPriority):
						print(val.client, val.priority, '----',currClient,currPriority)
						#check for last available slot of client list present 
						check2 = clients.objects.all().filter(client=currClient,priority=val.priority+1)
						if check2.count() == 0:
							#increment priority of last client
							val.priority += 1
							#bulk_mgr.add(clients(val))
							val.save()
							break;
							
						else :
							val.priority += 1
							#bulk_mgr.add(clients(val))
							val.save() 
					else:
						print(val.client, val.priority, '----else--',currClient,currPriority)
			#bulk_mgr.done()
			serializer.save()
			return Response(serializer.data , status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
