from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *


# Customer CRUD functions (SRP)
@api_view(['GET', 'POST']) 
def customer_list(request):

  if request.method == 'GET':
    return get_customer_list(request)
  
  elif request.method == 'POST':
    return create_customer(request)
  
def get_customer_list(request):
  customers = Customer.objects.all()
  serializer = CustomerSerializer(customers, many=True)
  return Response(serializer.data)

def create_customer(request):
  serializer = CustomerSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_details(request, id):

  try:
    customer = Customer.objects.get(pk=id)
  except Customer.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    return get_one_customer(customer)
  
  elif request.method == 'PUT':
    return update_one_customer(customer, request)
  
  elif request.method == 'DELETE':
    return delete_customer(customer)
  
def get_one_customer(customer):
  serializer = CustomerSerializer(customer)
  return Response(serializer.data)

def update_one_customer(customer, request):
    customer_data = CustomerSerializer(customer, data=request.data)
    if customer_data.is_valid():
      customer_data.save()
      return Response(customer_data.data)
    return Response(customer_data.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_customer(customer):
  customer.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)



# Item CRUD functions (SRP)
@api_view(['GET', 'POST'])
def item_list(request):
  if request.method == 'GET':
    return get_item_list(request)
  elif request.method == 'POST':
    return create_item(request)

def get_item_list(request):
  items = Item.objects.all()
  serializer = ItemSerializer(items, many=True)
  return Response(serializer.data)

def create_item(request):
  serializer = ItemSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def item_details(request, id):
  item = get_item_object(id)

  if request.method == 'GET':
    return get_item_details(item)
  elif request.method == 'PUT':
    return update_item(item, request.data)
  elif request.method == 'DELETE':
    return delete_item(item)

def get_item_object(item_id):
  try:
    return Item.objects.get(pk=item_id)
  except Item.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

def get_item_details(item):
  serializer = ItemSerializer(item)
  return Response(serializer.data)

def update_item(item, data):
  item_data = ItemSerializer(item, data=data)
  if item_data.is_valid():
    item_data.save()
    return Response(item_data.data)
  return Response(item_data.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_item(item):
  item.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)



# Specific vendor's items CRUD functions (SRP)
@api_view(['GET', 'POST'])
def vendor_item_list(request, vendor_id):
  try:
    vendor = Vendor.objects.get(pk=vendor_id)
  except Vendor.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    return get_vendor_item_list(request, vendor)
  elif request.method == 'POST':
    return create_item(request)

def get_vendor_item_list(request, vendor):
  items = Item.objects.filter(vendor=vendor)
  serializer = ItemSerializer(items, many=True)
  return Response(serializer.data)

def create_item(request):
  serializer = ItemSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_item_details(request, vendor_id, item_id):
  try:
    vendor = Vendor.objects.get(pk=vendor_id)
  except Vendor.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  try:
    item = Item.objects.get(pk=item_id, vendor=vendor)
  except Item.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    return get_vendor_item_details(item)
  elif request.method == 'PUT':
    return update_vendor_item(item, request.data)
  elif request.method == 'DELETE':
    return delete_vendor_item(item)
  
def get_vendor_item_details(item):
  serializer = ItemSerializer(item)
  return Response(serializer.data)

def update_vendor_item(item, data):
  item_data = ItemSerializer(item, data=data)
  if item_data.is_valid():
    item_data.save()
    return Response(item_data.data)
  return Response(status=status.HTTP_400_BAD_REQUEST)

def delete_vendor_item(item):
  item.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)



# Vendors 
@api_view(['GET', 'POST']) 
def vendor_list(request):

  if request.method == 'GET':
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)
  
  elif request.method == 'POST':
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
@api_view(['GET', 'PUT', 'DELETE'])
def vendor_details(request, id):
  try:
    vendor = Vendor.objects.get(pk=id)
  except Vendor.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = VendorSerializer(vendor)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    vendor_data = VendorSerializer(vendor, data=request.data)
    if vendor_data.is_valid():
      vendor_data.save()
      return Response(vendor_data.data)
    return Response(vendor_data.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    vendor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Preorders crud functions
@api_view(['GET', 'POST'])
def preorder_list(request):
  if request.method == 'GET':
    
    return get_preorder_list(request)
  elif request.method == 'POST':
    return create_preorder(request)
  
def get_preorder_list(request):
  preorder = Preorder.objects.all()
  serializer = PreorderSerializer(preorder, many=True)
  return Response(serializer.data)
  
def create_preorder(request):
  serializer = PreorderSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def preorder_details(request, id):
  preorder = get_preorder_object(id)

  if request.method == 'GET':
    return get_preorder_details(preorder)
  elif request.method == 'PUT':
    return update_preorder(preorder, request.data)
  elif request.method == 'DELETE':
    return delete_preorder(preorder, request.data)

def get_preorder_object(preorder_id):
  try:
    return Preorder.objects.get(pk=preorder_id)
  except Preorder.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
def get_preorder_details(preorder):
  serializer = PreorderSerializer(preorder)
  return Response(serializer.data)

def update_preorder(preorder, data):
  preorder_data = PreorderSerializer(preorder, data=data)
  if preorder_data.is_valid():
    preorder_data.save()
    return Response(preorder_data.data)
  return Response(preorder_data.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_preorder(preorder):
  preorder.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)
