from django.contrib.auth.models import User,Group
from . import models

from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=("id","name") 
        
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['id','username',"first_name","email","groups"] 
        
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MenuItem
        fields='__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    cart_item_price=serializers.SerializerMethodField()
    class Meta:
        model=models.CartItem
        fields='__all__'
        
    def get_cart_item_price(self,obj):
        return obj.get_cart_item_price()


class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.OrderItem
        fields='__all__'
        
        
class OrderSerializer(serializers.ModelSerializer):
    order_item=OrderItemSerializer(many=True, read_only=True, source="order")
    class Meta:
        model=models.Order
        fields=['user','delivery_crew','status','order_item','total']
        
  