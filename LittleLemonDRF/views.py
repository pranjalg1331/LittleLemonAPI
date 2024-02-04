from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User,Group
from . import serializer,permissions,models
from .serializer import OrderSerializer
from rest_framework import generics,status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle




# Create your views here.
class MenuItem(generics.ListCreateAPIView):
    
    queryset=models.MenuItem.objects.all()
    serializer_class=serializer.MenuItemSerializer
    ordering=['price']
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser | permissions.isManager]
        return super(MenuItem, self).get_permissions()
    # filter_backends = [OrderingFilter]  # Add OrderingFilter to enable ordering
    ordering_fields = ['price']
    
class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.MenuItem.objects.all()
    serializer_class=serializer.MenuItemSerializer
    def get_permissions(self):
        if (
            self.request.method == "POST"
            or self.request.method == "PUT"
            or self.request.method=="PATCH"
            or self.request.method == "DELETE"
        ):
            self.permission_classes = [permissions.isManager]
        return super(SingleMenuItem,self).get_permissions()
    
    
class ManageManagers(ViewSet):
    permission_classes = [IsAdminUser | permissions.isManager]
    def list(self, request):
        queryset = User.objects.filter(groups__name="Manager")
        print(queryset)
        ser=serializer.UserSerializer(queryset,many=True)
        return Response(ser.data)
    def create(self,request):
        username=request.data.get("username")
        user=get_object_or_404(User,username=username)
        managers_group=Group.objects.get(name="Manager")
        managers_group.user_set.add(user)
        return Response(
            {"message": "user added to the 'Manager' group"},
            status=status.HTTP_201_CREATED,
        )
    def destroy(self,request):
        username = request.data.get("username")
        
        user = get_object_or_404(User, username=username)
        
        managers_group = Group.objects.get(name="Manager")
        managers_group.user_set.remove(user)  
        return Response(
            {"message": "User removed from the 'Manager' group"},
            status=status.HTTP_200_OK
            
        ) 
        
class ManageDeliveryCrew(ViewSet):
    permission_classes = [IsAdminUser | permissions.isManager]
    def list(self, request):
        queryset = User.objects.filter(groups__name="Delivery Crew")
        print(queryset)
        ser=serializer.UserSerializer(queryset,many=True)
        return Response(ser.data)
    def create(self,request):
        username=request.data.get("username")
        user=get_object_or_404(User,username=username)
        delivery_crew=Group.objects.get(name="Delivery Crew")
        delivery_crew.user_set.add(user)
        return Response(
            {"message": "user added to the 'Delivery' group"},
            status=status.HTTP_201_CREATED,
        )
    def destroy(self,request):
        username = request.data.get("username")
        
        user = get_object_or_404(User, username=username)
        
        delivery_crew=Group.objects.get(name="Delivery Crew")
        delivery_crew.user_set.remove(user)  
        return Response(
            {"message": "User removed from the 'Delivery' group"},
            status=status.HTTP_200_OK
            
        ) 
        

    
    
    
class ManageCart(ViewSet):   
    def list(self,request):
        user=self.request.user
        cart_items=models.CartItem.objects.filter(user=user)
        ser=serializer.CartItemSerializer(cart_items,many=True)
        return Response(ser.data)
    def create(self,request):
        user=self.request.user
        cart_items=models.CartItem.objects.filter(user=user)
        item_title=request.data.get("title")
        item=get_object_or_404(models.MenuItem,title=item_title)
        # cart.menuitem.add(item)
        models.CartItem(user=user,menuitem=item,quantity=request.data.get("quantity"),unit_price=item.price).save()
        return Response(
            {"message": "item added to the Cart"},
            status=status.HTTP_201_CREATED,
        )
    def destroy(self,request):
        user=self.request.user
        cart_items=models.CartItem.objects.filter(user=user).all().delete()
        
        return Response(
            {"message": "Cart is empty"},
            status=status.HTTP_200_OK
            
        ) 
        
def assign_delivery():
    man=User.objects.filter(groups__name='Delivery Crew').all().order_by('?')[0]
    print(man)
    return man
    
def cart_total_price(user):
    sum=0
    cartitems=models.CartItem.objects.filter(user=user)
    for item in cartitems:
        sum=sum+item.get_cart_item_price()
    return sum
        
class OrderView(ViewSet):
    
    
    def list(self,request):
        if self.request.user.groups.filter(name="Delivery Crew"):
            orders=models.Order.objects.filter(delivery_crew=self.request.user)
        elif (self.request.user.groups.filter(name="Manager") or self.request.user.is_superuser):
            orders=models.Order.objects.all()
        else:
            orders=models.Order.objects.filter(user=self.request.user)
        ser=serializer.OrderSerializer(orders,many=True)
        return Response(ser.data)
    def create(self,request):
        order=models.Order(user=self.request.user,delivery_crew=assign_delivery(),total=cart_total_price(self.request.user))
        order.save()
        cartitems=models.CartItem.objects.filter(user=self.request.user)
        for item in cartitems:
            orderitem=models.OrderItem(order=order,menuitem=item.menuitem,quantity=item.quantity,unit_price=item.unit_price,price=item.quantity*item.unit_price)
            orderitem.save()
        models.CartItem.objects.filter(user=self.request.user).all().delete()
        return Response(
            {"message": "Order created"},
            status=status.HTTP_201_CREATED,
        )



class SingleOrderItem(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            order = models.Order.objects.get(pk=pk)
            
        except models.Order.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        if order.user==self.request.user:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"detail": "Forbidden."},status=401)
    def partial_update(self, request, pk=None):
        try:
            order = models.Order.objects.get(pk=pk)
            
        except models.Order.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        
        if self.request.user.groups.filter(name="Delivery Crew"):
            orders=models.Order.objects.filter(delivery_crew=self.request.user)
            if order in orders:
                serializer = OrderSerializer(order, data={'status': request.data.get("status")}, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Forbidden."},status=401)
                
        elif (self.request.user.groups.filter(name="Manager") or self.request.user.is_superuser):
            serializer = OrderSerializer(order,data={'status': request.data.get("status")}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Forbidden."},status=401)
    
    def update(self,request,pk=None):
        permission_classes = [IsAdminUser | permissions.isManager]
        self.check_permissions(request)
        try:
            order = models.Order.objects.get(pk=pk)
        except models.Order.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        
        serializer = OrderSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self,request,pk=None):
        permission_classes = [IsAdminUser | permissions.isManager]
        self.check_permissions(request)
        try:
            order = models.Order.objects.get(pk=pk)
        except models.Order.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        
        order.delete()
        return Response({"message":"Order deleted"},status=status.HTTP_200_OK)
        
        
            
    
        

    
        
        
