from payment_gateway.models import *
from LandingPage.models import *
import json
import razorpay
client = razorpay.Client(auth=("rzp_test_0G5HtLCg0WpC26", "y8iPiSBFRf8w2Y1W0L6Q7F55"))
def CreateOrder(request,productId,action=None):
    customer = request.user
    product = Course.objects.get(Cid=productId)
    order, created = Order.objects.get_or_create(customer=customer, status=False)
    orderItem, created = OrderCourses.objects.get_or_create(order=order, course=product)
    if action == 'add':
        orderItem.save()
    if action == 'remove':
        #print(orderItem)
        orderItem.delete()
        #print(orderItem)
        
        
    
def CreateOrderWithAnonymousCart(request,cart):
    for productId in cart:
        CreateOrder(request,productId)



def cookieCart(request):
    
	# Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']

			product = Course.objects.get(Cid=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.Cid,
				'course':{'Cid':product.Cid,'title':product.title, 'price':product.price, 
				'thumbnail':product.thumbnail},
				'get_total':total
				}
			items.append(item)


		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}


def cartData(request):
    context={}
   
    if request.user.is_authenticated and  request.user.groups.filter(name='Visiters').exists():
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        if bool(cart):
            print(cart,"c 1") 
            CreateOrderWithAnonymousCart(request,cart)
        print(cart," c 2")
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, status=False)
        items = order.ordercourses_set.all()
        cartItems = order.get_cart_items
        name = request.user.first_name+" "+request.user.last_name
    
        email = request.user.email
    
        amount =order.get_cart_total

        order_amount = amount*100
        checkout=request.GET.get('checkout',None)
       
        if checkout=='true':
            order_currency = 'INR'
            order_receipt = str(order.id)
            notes = {
                'Shipping address': ''}

            # CREAING ORDER
            
            response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))

            order_id = response['id']
            order_status = response['status']

            if order_status=='created':

                # Server data for user convinience
                
                context['total'] = order_amount
                context['name'] = name
                context['email'] = email

                # data that'll be send to the razorpay for
                context['order_id'] = order_id

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    context['cartItems']=cartItems
    context['order']=order
    context['items']=items
    return context

