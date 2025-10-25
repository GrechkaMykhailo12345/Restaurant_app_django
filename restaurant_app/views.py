from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.db import transaction
from .models import Dish, Category, Review, Order, DishesinOrder
from .forms import ReviewForm, OrderCreateForm

def get_cart_data(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')

    dish_ids = [int(id) for id in cart.keys()]
    
    dishes = Dish.objects.filter(id__in=dish_ids)
    dishes_map = {dish.id: dish for dish in dishes}

    for dish_id_str, item in cart.items():
        dish_id_int = int(dish_id_str)
        
        if dish_id_int in dishes_map:
            dish = dishes_map[dish_id_int]
            
            try:
                price = Decimal(item['price'])
                quantity = int(item['quantity'])
                item_total = price * quantity
                total_price += item_total
                
                cart_items.append({
                    'dish': dish,
                    'quantity': quantity,
                    'price': price,
                    'total': item_total
                })
            except (ValueError, TypeError):
                continue

    return {'cart_items': cart_items, 'total_price': total_price}

def home_page(request):
    popular_dishes = Dish.objects.filter(is_popular=True, is_available=True)[:5]
    new_dishes = Dish.objects.filter(is_available=True).order_by('-created_at')[:5]
    return render(request, 'restaurant_app/home.html', {
        'popular_dishes': popular_dishes,
        'new_dishes': new_dishes
    })

def menu_list(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(is_available=True).select_related('category')
    
    category_id = request.GET.get('category')
    if category_id:
        dishes = dishes.filter(category__id=category_id)
        
    return render(request, 'restaurant_app/menu_list.html', {
        'categories': categories,
        'dishes': dishes,
        'selected_category': int(category_id) if category_id else None
    })

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    reviews = Review.objects.filter(dish=dish, is_approved=True).order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    review_form = ReviewForm()
    
    return render(request, 'restaurant_app/dish_detail.html', {
        'dish': dish,
        'reviews': reviews,
        'average_rating': round(average_rating, 1) if average_rating else 'Немає',
        'review_form': review_form,
    })

def dish_search(request):
    query = request.GET.get('q', '')
    dishes = Dish.objects.filter(is_available=True)
    
    if query:
        dishes = dishes.filter(name__icontains=query) | dishes.filter(description__icontains=query)
        
    return render(request, 'restaurant_app/search_results.html', {
        'query': query,
        'dishes': dishes
    })

@login_required 
def add_review(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dish = dish
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш відгук додано і очікує схвалення адміністратором.')
            return redirect('dish_detail', dish_id=dish.id)
        else:
            messages.error(request, 'Помилка: будь ласка, заповніть усі поля.')
            
    return redirect('dish_detail', dish_id=dish.id)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'restaurant_app/order_history.html', {'orders': orders})


def cart_detail(request):
    cart_data = get_cart_data(request)
    return render(request, 'restaurant_app/cart_detail.html', cart_data)

@require_POST
def cart_add(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.session.get('cart', {})
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            quantity = 1
    except ValueError:
        quantity = 1

    dish_id_str = str(dish_id)

    if dish_id_str in cart:
        cart[dish_id_str]['quantity'] += quantity
    else:
        cart[dish_id_str] = {
            'quantity': quantity,
            'price': str(dish.price) 
        }

    request.session['cart'] = cart
    return redirect('cart_detail') 

@require_POST
def cart_update(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    
    if dish_id_str in cart:
        try:
            new_quantity = int(request.POST.get('quantity'))
            
            if new_quantity > 0:
                cart[dish_id_str]['quantity'] = new_quantity
            else:
                del cart[dish_id_str]
                
        except (ValueError, TypeError):
            pass 
    
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)

    if dish_id_str in cart:
        del cart[dish_id_str]
        
    request.session['cart'] = cart
    return redirect('cart_detail')


@login_required
def order_create(request):
    cart_data = get_cart_data(request)
    cart_items = cart_data['cart_items']
    total_price = cart_data['total_price']

    if not cart_items:
        return redirect('menu_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = total_price
                
                order.save()
                
                for item in cart_items:
                    DishesinOrder.objects.create(
                        order=order,
                        dish=item['dish'],
                        price=item['price'],
                        quantity=item['quantity'],
                        total_price=item['total'] 
                    )

                request.session['cart'] = {}
                return redirect('order_confirmation', order_id=order.id)
    
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'restaurant_app/order_create.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    try:
        order = Order.objects.filter(id=order_id).prefetch_related('dishesinorder_set__dish').first()
    except Exception as e:
        print(f"Помилка prefetch: {e}") 
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
    return render(request, 'restaurant_app/order_confirmation.html', {'order': order})