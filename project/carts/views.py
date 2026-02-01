from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure cart belongs to the user
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user, is_ordered=False)
        serializer.save(cart=cart)
    
    def get_queryset(self):
        # Only show items from this user's active cart
        user = self.request.user
        return CartItem.objects.filter(cart__user=user, cart__is_ordered=False)
    


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user, is_ordered=False)

