from django.shortcuts import render
from django.views.generic import View, DetailView
from django.contrib.auth import authenticate, login
from mainapp.utils import recalc_bunker, calc_bunker
from .models import *
from .forms import BunkerForm, TransactionForm, GrainForm, LoginForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class BaseView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        
        add_bunker_form = BunkerForm()
        bunkers = Bunker.objects.all()
        transactions = Transaction.objects.all().order_by('-id')[:10]
        context={
            'transactions': transactions,
            'bunkers': bunkers,
            'add_bunker_form': add_bunker_form
        }
        return render(request, 'base.html', context)

class AddBunkerView(LoginRequiredMixin, View):

    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = BunkerForm(request.POST or None)
        if form.is_valid():
            new_bunker = form.save(commit=False)
            new_bunker.name = form.cleaned_data['name']
            new_bunker.max_qty = form.cleaned_data['max_qty']
            new_bunker.grain_type = form.cleaned_data['grain_type']
            new_bunker.save()
            messages.add_message(request, messages.SUCCESS, 'Бункер успішно додано!')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/admin')

class BunkerDetailView(LoginRequiredMixin, DetailView):

    login_url = '/login/'
    context_object_name = 'bunker'
    template_name = 'bunker_detail.html'


    def dispatch(self, request, *args, **kwargs):
        self.model = Bunker
        self.queryset = Bunker.objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        bunker = self.get_object()
        context = super().get_context_data(**kwargs)
        context['transactions'] = bunker.transactions.all().order_by('-id')
        add_bunker_form = BunkerForm()
        edit_bunker_form = BunkerForm(initial={
            'name': bunker.name,
            'max_qty': bunker.max_qty,
            'qty': bunker.qty,
            'grain_type': bunker.grain_type
        })
        transaction_form = TransactionForm(initial={
            'bunker': bunker
        })
        context['transaction_form'] = transaction_form
        context['add_bunker_form'] = add_bunker_form
        context['edit_bunker_form'] = edit_bunker_form
        return context

class DeleteBunkerView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        bunker = Bunker.objects.get(id=id)
        bunker.delete()
        messages.add_message(request, messages.SUCCESS, "Бункер успішно видалено!")
        return HttpResponseRedirect('/')


class AddTransactionView(LoginRequiredMixin, View):

    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST or None)
        id = self.kwargs.get('pk')
        bunker = Bunker.objects.get(id=id)
        if form.is_valid():
            final_qty = form.cleaned_data['qty'] + calc_bunker(bunker)
            if final_qty>=0 and final_qty <=bunker.max_qty:
                new_transaction = form.save(commit=False)
                new_transaction.title = form.cleaned_data['title']
                new_transaction.qty = form.cleaned_data['qty']
                new_transaction.transaction_date = date.today()
                new_transaction.bunker = bunker
                new_transaction.grain_type = bunker.grain_type
                new_transaction.save()
                bunker.transactions.add(new_transaction)
                bunker.save()
                recalc_bunker(bunker)
                messages.add_message(request, messages.SUCCESS, 'Транзакцію успішно додано!')
                return HttpResponseRedirect('/bunker/'+str(id))
            elif final_qty<0:
                messages.add_message(request, messages.WARNING, 'Транзакцію не виконано! В бункері недостатньо зерна для цієї транзакції.')
                return HttpResponseRedirect('/bunker/'+str(id))
            else:
                messages.add_message(request, messages.WARNING, 'Транзакцію не виконано! В бункері недостатньо місця для цієї транзакції.')
                return HttpResponseRedirect('/bunker/'+str(id))
        messages.add_message(request, messages.WARNING, 'Транзакцію не додано! Перевірте правильність введенних данних.')
        return HttpResponseRedirect('/bunker/'+str(id))

class GrainView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        
        add_bunker_form = BunkerForm()
        add_grain_form = GrainForm()
        grains = Grain.objects.all()
        context={
            'grains': grains,
            'add_grain_form': add_grain_form,
            'add_bunker_form': add_bunker_form
        }
        return render(request,'grain_detail.html', context)

class DeleteGrainView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        grain = Grain.objects.get(id=id)
        grain.delete()
        messages.add_message(request, messages.SUCCESS, "Культуру успішно видалено!")
        return HttpResponseRedirect('/grains/')

class AddGrainView(LoginRequiredMixin, View):

    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = GrainForm(request.POST or None)
        if form.is_valid():
            new_grain = form.save(commit=False)
            new_grain.name = form.cleaned_data['name']
            new_grain.save()
            messages.add_message(request, messages.SUCCESS, 'Культуру успішно додано!')
            return HttpResponseRedirect('/grains/')
        messages.add_message(request, messages.WARNING, 'Культуру не додано!')
        return HttpResponseRedirect('/grains/')

class EditBunkerView(LoginRequiredMixin, View):

    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        bunker = Bunker.objects.get(id=id)
        form = BunkerForm(request.POST or None)
        if form.is_valid():
            if bunker.qty<=form.cleaned_data['max_qty']:
                bunker.name = form.cleaned_data['name']
                bunker.max_qty = form.cleaned_data['max_qty']
                if bunker.grain_type != form.cleaned_data['grain_type']:
                    new_transaction = Transaction()
                    new_transaction.title = '(РЕД) Очистка бункеру: зміна культури з {0} на {1}'.format(bunker.grain_type.name, form.cleaned_data['grain_type'].name)
                    new_transaction.qty = -1 * bunker.qty
                    new_transaction.transaction_date = date.today()
                    new_transaction.bunker = bunker
                    new_transaction.grain_type = bunker.grain_type
                    new_transaction.save()
                    bunker.transactions.add(new_transaction)
                bunker.grain_type = form.cleaned_data['grain_type']
                bunker.save()
                recalc_bunker(bunker)
                messages.add_message(request, messages.SUCCESS, 'Бункер відредаговано!')
                return HttpResponseRedirect('/bunker/'+str(id))
        messages.add_message(request, messages.WARNING, 'Сталася помилка! В бункері зерна більше, чим вказано в місткості!')
        return HttpResponseRedirect('/bunker/'+str(id))

class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'] 
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')

        context = {
            'form': form
            }
        return render(request, 'login.html', context)