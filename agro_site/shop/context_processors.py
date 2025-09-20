from agro_site.shop.cart import Cart

def cart(request):
    return {'cart': Cart(request)}
