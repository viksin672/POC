from django.test import TestCase
from .models import clients
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ModelTestCase(TestCase):
    """This class defines the test suite for the clients model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.clients_title = "Great title"
        self.clients_priority = 1
        self.clients_client = "Client A"
        self.clients_description = " Some great description"
        self.clients_date = "2020-02-02"
        self.clients_area = "Claims"
        self.clients = clients(title=self.clients_title,priority=self.clients_priority,client=self.clients_client,description=self.clients_description,date=self.clients_date,area=self.clients_area)
        
    def test_model_can_create_a_client(self):
        """Test the client model can create a client."""
        old_count = clients.objects.count()
        self.clients.save()
        new_count = clients.objects.count()
        self.assertNotEqual(old_count, new_count)
        
    def test_get_client_req_data(self):
        """
        get client api test.
        """
        response = self.client.get('/api/clientlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_client_req_data(self):
        """
        post client api test.
        """

        url = reverse('Clients')
        data = {
        "title": "title1",
        "description": "task description",
        "client": "Client A",
        "priority": 2,
        "date": "2020-02-28",
        "area": "Claims"
    }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
