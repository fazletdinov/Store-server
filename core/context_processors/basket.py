from products.models import Basket


def baskets(request):
    user = request.user
    baskets = Basket.objects.filter(user=user)
    return {'baskets': baskets if user.is_authenticated else []}
