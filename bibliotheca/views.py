from django.shortcuts import render
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from bibliotheca.models import *
from bibliotheca.forms import ReadersForm, UserCreateForm
from django.db.models import Q
from django.shortcuts import RequestContext, redirect
import datetime
from django.conf import settings
import math

# Create your views here.
def flatten(nested):
    flat = list()
    def flatten_in(nested, flat):
       for i in nested:
           flatten_in(i, flat) if isinstance(i, list) else flat.append(i)
       return flat
    flatten_in(nested, flat)
    return flat

def isUserBlocked(u):
    if u and u.is_authenticated():
        reader = Readers.objects.get(user=u)
        if reader.is_blocked:
            return True
        return False

class MsgBlockedView(View):
    template = 'msgs/blocked.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template)

class NewsView(View):
    template = 'news.html'
    def get(self, request, *args, **kwargs):
        latest_news = News.objects.order_by('-creation_date')
        context = {
            'latest_news' : latest_news
        }
        return render(request,self.template, context)

class ContactView(View):
    template = 'contact.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template)

class UserRegister(View):
    template = 'registration/register.html'
    def get(self, request):

        form_creation = UserCreateForm()
        form_readers = ReadersForm()

        context = {
            'form_creation' : form_creation,
            'form_readers' : form_readers,
        }

        return render(request, self.template, context)

    def post(self, request):
        form_creation = UserCreateForm(request.POST)
        form_readers = ReadersForm(request.POST)

        if form_creation.is_valid() and form_readers.is_valid():
            user = form_creation.save()
            profile = form_readers.save(commit=False)
            profile.user = user
            profile.save()
            return render(request, 'registration/registerSuccess.html')

        context = {
            'form_creation' : form_creation,
            'form_readers' : form_readers,
        }

        return render(request, self.template, context)

class CategoryView(ListView):
    template = 'categories.html'

    def get(self, request, cid = 1, page = 1, *args, **kwargs):
        current = Categories.objects.get(id=cid)
        related_cats = current.get_all_children()
        relcats = flatten(related_cats)

        queries = [Q(category=value) for value in relcats]

        query = queries.pop()

        for item in queries:
            query |= item

        books = Books.objects.filter(query)

        page = (int)(page)
        maxpages = math.ceil(books.count() / settings.BOOKS_PER_PAGE)
        if page <= maxpages:
            books = books[(page - 1) * settings.BOOKS_PER_PAGE: (page - 1) + settings.BOOKS_PER_PAGE]

        obj = current
        breadcrumbs = []
        while obj != None:
            breadcrumbs.append(obj)
            obj = obj.top_category

        breadcrumbs.reverse()

        children = Categories.objects.filter(top_category=current)

        if children.count() == 0:
            current = current.top_category
            children = Categories.objects.filter(top_category=current)

        context = {
            'books' : books,
            'breadcrumbs' : breadcrumbs,
            'current' : current,
            'children' : children,
            'cid' : int(cid),
            'maxpages': maxpages,
            'page': page,
        }

        return render(request,self.template, context)

class BookView(View):
    template = 'book.html'

    def get(self, request, bid, *args, **kwargs):
        book = Books.objects.get(id=bid)

        warehouse = Warehouse.objects.get(book=bid)
        borrowed_reserved_number = 0
        is_limit_reached = False
        all_reservations = None
        reservations = None
        borrowings = None
        if request.user.is_authenticated():
            user = request.user
            try:
                reservations = Reservations.objects.get(book = bid, reader = user.readers)
            except Reservations.DoesNotExist:
                reservations = None


            try:
                all_reservations = Reservations.objects.filter(reader = user.readers)
            except Reservations.DoesNotExist:
                all_reservations = None

            try:
                borrowings = Borrowings.objects.filter(reader = user.readers)
            except Borrowings.DoesNotExist:
                borrowings = None

        if all_reservations:
            borrowed_reserved_number += len(all_reservations)
        if borrowings:
            borrowed_reserved_number += len(borrowings)

        if borrowed_reserved_number >= settings.BOOKS_LIMIT:
            is_limit_reached = True

        breadcrumbs = []
        breadcrumbs.append(book)

        obj = book.category
        while obj != None:
            breadcrumbs.append(obj)
            obj = obj.top_category
        breadcrumbs.reverse()

        context = {
            'book': book,
            'breadcrumbs': breadcrumbs,
            'reservations' : reservations,
            'warehouse' : warehouse,
            'is_limit_reached' : is_limit_reached
        }
        return render(request,self.template, context)

class AuthorView(View):
    template = 'author.html'
    def get(self, request, aid, page = 1, *args, **kwargs):

        author = Authors.objects.get(id=aid)
        books = Books.objects.filter(authors=author)

        page = (int)(page)
        maxpages = math.ceil(books.count() / settings.BOOKS_PER_PAGE)
        if page <= maxpages:
            books = books[(page - 1) * settings.BOOKS_PER_PAGE: (page - 1) + settings.BOOKS_PER_PAGE]

        context = {
            'books': books,
            'author': author,
            'maxpages': maxpages,
            'page': page,
        }
        return render(request,self.template, context)

class PublisherView(View):
    template = 'publisher.html'
    def get(self, request, pid, page = 1, *args, **kwargs):

        pub = Publishers.objects.get(id=pid)
        books = Books.objects.filter(publisher=pub)

        page = (int)(page)
        maxpages = math.ceil(books.count() / settings.BOOKS_PER_PAGE)
        if page <= maxpages:
            books = books[(page - 1) * settings.BOOKS_PER_PAGE: (page - 1) + settings.BOOKS_PER_PAGE]

        context = {
            'books': books,
            'publisher': pub,
            'maxpages': maxpages,
            'page': page,
        }
        return render(request,self.template, context)


class BorrowingsView(View):
    template = 'borrowings.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            borrowings = Borrowings.objects.filter(reader = user.readers)
        except Reservations.DoesNotExist:
            borrowings = None

        context = {
            'borrowings' : borrowings
        }
        return render(request, self.template, context)



class ReservationsView(View):
    template = 'reservations.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            reservations = Reservations.objects.filter(reader = user.readers)
        except Reservations.DoesNotExist:
            reservations = None

        context = {
            'reservations' : reservations,
        }
        return render(request, self.template, context)


class ReservedView(View):
    template = 'reserved.html'

    def get(self, request, bid, *args, **kwargs):
        if isUserBlocked(request.user):
            return redirect('msg_blocked')

        warehouse = Warehouse.objects.get(book=bid)
        warehouse.books_reserved += 1
        warehouse.books_available -= 1
        warehouse.save()
        try:
            is_reserved = Reservations.objects.get(book = bid, reader = request.user.readers)
        except Reservations.DoesNotExist:
            is_reserved = None
        if is_reserved == None:
            reservation = Reservations()
            reservation.book = Books.objects.get(id=bid)
            reservation.reader = Readers.objects.get(user=request.user)
            reservation.reservation_date = datetime.datetime.now()
            reservation.save()

            context = {}
            return render(request,self.template, context)
        else:
            context = {
                'reservation' : is_reserved,
                'warehouse' : warehouse
            }
            return render(request,self.template,context)

class UnreservedView(View):
    template = 'unreserved.html'

    def get(self, request, bid, *args, **kwargs):
        if isUserBlocked(request.user):
            return redirect('msg_blocked')

        warehouse = Warehouse.objects.get(book=bid)
        warehouse.books_reserved -= 1
        warehouse.books_available += 1
        warehouse.save()
        try:
            is_reserved = Reservations.objects.get(book = bid, reader = request.user.readers)
        except Reservations.DoesNotExist:
            is_reserved = None
        if is_reserved != None:
            reservation = Reservations.objects.get(book = bid, reader = request.user.readers)
            reservation.delete()
            context = {}
            return render(request,self.template, context)
        else:
            context = {
                'reservation' : is_reserved
            }
            return render(request, self.template, context)

class SearchResultsView(View):
    template = 'search_results.html'
    def get(self, request, *args, **kwargs):
        if request.GET['q']:

            k = int(request.GET['k'])
            s = int(request.GET['s'])
            cid = int(request.GET['cat'])

            current = Categories.objects.get(id=cid)
            related_cats = current.get_all_children()
            relcats = flatten(related_cats)

            queries = [Q(category=value) for value in relcats]

            query = queries.pop()

            for item in queries:
                query |= item

            if k == 1:
                books = Books.objects.filter(query, title__contains=request.GET['q'])
            elif k == 2:
                a = Authors.objects.filter(last_name__contains=request.GET['q'])
                books = Books.objects.filter(query, authors=a)
            else:
                books = None

            if s == 1:
                books = books.order_by('title')
            elif s == 2:
                books = books.order_by('-title')
        else:
            return redirect('category_null')

        formdata = {
            'q' : request.GET['q'],
            'k' : k,
            's' : s,
            'cid' : cid
        }
        context = {
                'books' : books,
                'formdata' : formdata
            }
        return render(request, self.template, context)
