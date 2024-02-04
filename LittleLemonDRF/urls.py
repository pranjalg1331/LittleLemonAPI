from django.urls import path,include
from . import views

urlpatterns = [
    path("menu-item/",views.MenuItem.as_view()),
    path("menu-item/<int:pk>",views.SingleMenuItem.as_view()),
    path("groups/manager/users/",views.ManageManagers.as_view({"get": "list","post":"create","delete": "destroy"})),
    path("groups/delivery-crew/users/",views.ManageDeliveryCrew.as_view({"get": "list","post":"create","delete": "destroy"})),
    path("cart/menuitems/",views.ManageCart.as_view({"get": "list","post":"create","delete": "destroy"})),
    path("orders/",views.OrderView.as_view({"get": "list","post":"create"})),
    path("orders/<int:pk>",views.SingleOrderItem.as_view({"delete": "destroy","patch":"partial_update","get":"retrieve","put":"update"})),
]
