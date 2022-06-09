from email import message
import profile
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Order
from .forms import FormOrdine
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render

def homepage(request):

    return render(request, 'homepage.html')

@login_required(login_url='login')
def wallet(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    return render(request, 'wallet.html', {'profile': profile})

@login_required(login_url='login')
def nuovo_ordine(request):
    x = Order()
    x = x.media_pric()
    if request.method == 'POST':
        form = FormOrdine(request.POST)
        user = request.user
        if form.is_valid():
            new_order_prof = Profile.objects.get(user=user)
            if form.instance.type == 'BUY':
                total_cash = float(form.instance.price) * float(form.instance.quantity)
                if total_cash <= new_order_prof.cash_wallet:
                    order_sell = Order.objects.filter(type='SELL').filter(active=True)\
                        .filter(price__lte=form.instance.price).filter(~Q(user=user)).order_by('price', 'date')
                    form.instance.user = user
                    form.save()
                    messages.success(request, 'creato')
                    if len(order_sell) > 0:
                        messages.success(request, 'cerca ordini')
                        for order in order_sell:
                            prof_sell = Profile.objects.get(user=order.user)
                            if order.quantity == form.instance.quantity:
                                prof_sell.btc_wallet -= order.quantity
                                prof_sell.cash_wallet += total_cash
                                new_order_prof.cash_wallet -= total_cash
                                new_order_prof.btc_wallet += order.quantity
                                form.instance.active = False
                                order.active = False
                                order.save()
                                new_order_prof.save()
                                form.save()
                                prof_sell.save()
                                messages.success(request, 'BTC acquistati')
                                return redirect('/nuovo_ordine')
                            elif order.quantity < form.instance.quantity:
                                form.instance.quantity -= order.quantity
                                prof_sell.btc_wallet -= order.quantity
                                prof_sell.cash_wallet += (order.quantity * order.price)
                                new_order_prof.cash_wallet -= (order.quantity * order.price)
                                new_order_prof.btc_wallet += order.quantity
                                order.active = False
                                order.save()
                                new_order_prof.save()
                                form.save()
                                prof_sell.save()
                                messages.success(request, 'BTC acquistati parzialmente')
                                continue
                            elif order.quantity > form.instance.quantity:
                                order.quantity -= form.instance.quantity
                                prof_sell.btc_wallet -= form.instance.quantity
                                prof_sell.cash_wallet += (form.instance.quantity * order.price)
                                new_order_prof.cash_wallet -= (form.instance.quantity * order.price)
                                new_order_prof.btc_wallet += form.instance.quantity
                                form.instance.active = False
                                order.save()
                                new_order_prof.save()
                                form.save()
                                prof_sell.save()
                                messages.success(request, 'BTC acquistati')
                                return redirect('/nuovo_ordine')
                            else:
                                return redirect('/nuovo_ordine')
                    else:
                        messages.info(request, 'Nessuna controparte')
                        return redirect('/nuovo_ordine')
                else:
                    messages.error(request, 'BTC Insufficienti!!')
                    return redirect('/nuovo_ordine')
            elif form.instance.type == 'SELL':
                total_cash = float(form.instance.price) * float(form.instance.quantity)
                if new_order_prof.btc_wallet >= form.instance.quantity:
                    form.instance.user = user
                    form.save()
                    messages.success(request, 'creato')
                    order_buy = Order.objects.filter(type='BUY').filter(active=True)\
                        .filter(price__gte=form.instance.price).filter(~Q(user=user)).order_by('-price', 'date')
                    if len(order_buy) > 0:
                        messages.success(request, 'cerca ordini')
                        for order in order_buy:
                            prof_buyer = Profile.objects.get(user=order.user)
                            if order.quantity == form.instance.quantity:
                                prof_buyer.btc_wallet += order.quantity
                                prof_buyer.cash_wallet -= total_cash
                                new_order_prof.cash_wallet += total_cash
                                new_order_prof.btc_wallet -= order.quantity
                                form.instance.active = False
                                order.active = False
                                order.save()
                                new_order_prof.save()
                                form.save()
                                prof_buyer.save()
                                messages.success(request, 'BTC venduti')
                                return redirect('/nuovo_ordine')
                            elif order.quantity < form.instance.quantity:
                                form.instance.quantity -= order.quantity
                                prof_buyer.btc_wallet += order.quantity
                                prof_buyer.cash_wallet -= (order.quantity * order.price)
                                new_order_prof.cash_wallet += (order.quantity * order.price)
                                new_order_prof.btc_wallet -= order.quantity
                                order.active = False
                                order.save()
                                new_order_prof.save()
                                form.save()
                                prof_buyer.save()
                                messages.success(request, 'BTC venduti parzialmente')
                                continue
                            elif order.quantity > form.instance.quantity:
                                order.quantity -= form.instance.quantity
                                prof_buyer.btc_wallet += form.instance.quantity
                                prof_buyer.cash_wallet -= (form.instance.quantity * order.price)
                                new_order_prof.cash_wallet += (form.instance.quantity * order.price)
                                new_order_prof.btc_wallet -= form.instance.quantity
                                form.instance.active = False
                                order.save()
                                new_order_prof.save()
                                form.save()
                                prof_buyer.save()
                                messages.success(request, 'BTC venduti')
                                return redirect('/nuovo_ordine')
                        else:
                            return redirect('/nuovo_ordine')
                    else:
                        return render(request, 'nessuna_controparte.html')
                else:
                    return render(request, 'btc_insufficiente.html')
        else:
            messages.error(request, "Inserisci quantita' o prezzo corretti!")
            return redirect('/nuovo_ordine')
    else:
        form = FormOrdine()
        messages.info(request, f"prezzo medio buy: {x[0]}")
        messages.info(request, f"prezzo medio sell: {x[1]}")
        return render(request, 'nuovo_ordine.html', {'form': form})

class AllOrder(ListView):
    model = Order
    template_name = 'all_order.html'
    context_object_name = 'orders'


@login_required(login_url='login')
def profit(request):
    lis = []
    profiles = Profile.objects.all()
    user = request.user
    for prof in profiles:
        profitt = float(prof.btc_wallet or 0) - float(prof.btc_original or 0)
        lis.append(
            {
                'User': f"{prof.user}",
                'BTC Profit': profitt,
                'Cash Profit': int(prof.cash_wallet or 0) - 100000
            }
        )
    return JsonResponse(lis, safe=False)

