from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Dish, Category, Review, Order, DishesinOrder
from .forms import ReviewForm, OrderCreateForm

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
    messages.info(request, "Функціонал кошика буде реалізовано пізніше.")
    return redirect('home_page')

def cart_add(request, dish_id):
    messages.info(request, "Додавання в кошик ще не реалізовано.")
    return redirect('home_page')

def cart_remove(request, dish_id):
    messages.info(request, "Видалення з кошика ще не реалізовано.")
    return redirect('home_page')

def cart_update(request, dish_id):
    messages.info(request, "Оновлення кошика ще не реалізовано.")
    return redirect('home_page')

def order_create(request):
    messages.info(request, "Оформлення замовлення буде реалізовано пізніше.")
    return redirect('home_page')

def order_confirmation(request, order_id):
    messages.info(request, f"Замовлення №{order_id} успішно створено.")
    return redirect('home_page')