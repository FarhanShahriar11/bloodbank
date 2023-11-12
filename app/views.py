from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def index(request):
    return render(request, 'index/index.html')


def request_list(request):
    requests = Request.objects.all().exclude(is_fulfilled=True).order_by('id')
    if request.GET.get('group'):
        requests = requests.filter(group=request.GET.get('group'))
    data = {
        'requests': requests
    }
    return render(request, 'index/request_list.html', data)


def request_detail(request, id):
    data = {
        'req': Request.objects.get(id=id),
    }
    return render(request, 'index/request_detail.html', data)


"""
Auth
"""

def login_view(request):
    if request.user and request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff_index')
        return redirect('user_index')
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                username = User.objects.get(email=email).username
            else:
                raise Exception('User does not exist')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                if user.is_staff:
                    return redirect('staff_index')
                return redirect('user_index')
            else:
                raise Exception('Invalid Credentials')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == "POST":
        try:
            username = request.POST.get('email')
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                raise Exception('Email already exists')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
            if password != confirm_password:
                raise Exception('Passwords do not match')
            first_name = request.POST.get('first_name')
            user = User.objects.create(username=username, email=email, password=password, first_name=first_name)
            user.set_password(password)
            user.save()
            if request.POST.get('last_name'):
                user.last_name = request.POST.get('last_name')
            user.save()
            try:
                if Profile.objects.filter(mobile=request.POST.get('mobile')).exists():
                    profile = Profile.objects.get(mobile=request.POST.get('mobile'))
                    profile.user = user
                else:    
                    profile = Profile.objects.create(
                        user=user,
                        mobile = request.POST.get('mobile'),
                        group = request.POST.get('group'),
                    )
                    if request.POST.get('last_donated'):
                        profile.last_donated = request.POST.get('last_donated')
                profile.save()
            except Exception as e:
                user.delete()
                raise Exception(str(e))
            messages.success(request, 'Registration Successful')
            login(request, user)
            if user.is_staff:
                return redirect('staff_index')
            return redirect('user_index')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'auth/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('index')


"""
Donor
"""

@login_required(login_url='login')
def user_index(request):
    data = {
        'requests': Request.objects.filter(requested_by=request.user.profile).exclude(is_fulfilled=True).order_by('-id'),
        'donation': Donation.objects.filter(donor=request.user.profile).order_by('-id').first(),
    }
    data['stats'] = {
        'donations': Donation.objects.filter(donor=request.user.profile).count(),
        'active_requests': Request.objects.filter(requested_by=request.user.profile).exclude(is_fulfilled=True).count(),
        'total_requests': Request.objects.filter(requested_by=request.user.profile).count(),
    }
    return render(request, 'user/index.html', data)

@login_required(login_url='login')
def donor_request_list(request):
    data = {
        'requests': Request.objects.filter(requested_by=request.user.profile).order_by('-id')
    }
    return render(request, 'user/request/list.html', data)


@login_required(login_url='login')
def donor_request_detail(request, pk):
    req = Request.objects.get(id=pk)
    data = {
        'req': req
    }
    if request.method == "POST":
        try:
            req.hospital = request.POST.get('hospital')
            req.reason = request.POST.get('reason')
            req.units_required = int(request.POST.get('units-required'))
            req.units_received = int(request.POST.get('units-received')) if request.POST.get('units-received') else 0
            req.date_time = datetime.strptime(request.POST.get('datetime'), '%Y-%m-%dT%H:%M')
            req.emergency = True if request.POST.get('emergency') else False
            req.save()
            messages.success(request, 'Request Updated Successfully')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'user/request/detail.html', data)


@login_required(login_url='login')
def donor_request_add(request):
    if request.method == "POST":
        print(request.POST)
        try:
            blood_request = Request.objects.create(
                requested_by=request.user.profile,
                group = request.POST.get('group'),
                patient_name = request.POST.get('patient-name'),
                hospital = request.POST.get('hospital'),
                patient_age = int(request.POST.get('patient-age')),
                reason = request.POST.get('reason'),
                units_required = int(request.POST.get('units-required')),
                blood_type = request.POST.get('blood_type'),
                emergency = True if request.POST.get('emergency') else False,
                date_time = datetime.strptime(request.POST.get('datetime'), '%Y-%m-%dT%H:%M'),
            )
            blood_request.save()
            messages.success(request, 'Request Added Successfully')
            return redirect('user_request_list')
        except Exception as e:
            print(e)
            messages.error(request, str(e))
    return render(request, 'user/request/add.html')


@login_required(login_url='login')
def donor_donation_list(request):
    data = {
        'donations': Donation.objects.filter(donor=request.user.profile).order_by('-id')
    }
    return render(request, 'user/donation/list.html', data)


@login_required(login_url='login')
def donor_donation_add(request):
    data = {
        'today': datetime.now().strftime('%Y-%m-%d'),
    }
    if request.method == "POST":
        try:
            donation = Donation.objects.create(
                donor=request.user.profile,
                date = request.POST.get('date'),
                hospital = request.POST.get('hospital'),
            )
            if request.POST.get('comment'):
                donation.comment = request.POST.get('comment')
            donation.save()
            messages.success(request, 'Donation Added Successfully')
            return redirect('user_donation_list')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'user/donation/add.html', data)


@login_required(login_url='login')
def donor_profile(request):
    return render(request, 'user/profile.html')



"""
Staff
"""

@login_required(login_url='login')
def staff_index(request):
    data = {
        'requests': Request.objects.all().exclude(is_fulfilled=True).order_by('id')[:5],
        'stocks': Stock.objects.filter(status='Available').order_by('id')[:5],
    }
    data['stats'] = {
        'stocks': Stock.objects.filter(status='Available').count(),
        'active_requests': Request.objects.filter(is_fulfilled=False).count(),
        'donors': Profile.objects.all().count(),
    }
    return render(request, 'staff/index.html', data)


@login_required(login_url='login')
def staff_request_list(request):
    requests = Request.objects.all().order_by('-id')
    if request.GET.get('group'):
        requests = requests.filter(group=request.GET.get('group'))
    if request.GET.get('status'):
        if request.GET.get('status') == 'fulfilled':
            requests = requests.filter(is_fulfilled=True)
        elif request.GET.get('status') == 'pending':
            requests = requests.filter(is_fulfilled=False)

    else:
        requests= Request.objects.all().order_by('-id')
    data = {
        'requests': requests
    }
    return render(request, 'staff/request/list.html', data)


@login_required(login_url='login')
def staff_request_detail(request, pk):
    req = Request.objects.get(id=pk)
    data = {
        'req': req,
        'stocks': Stock.objects.filter(group=req.group, status='Available'),
    }
    if request.method == "POST":
        try:
            req.hospital = request.POST.get('hospital')
            req.reason = request.POST.get('reason')
            req.units_required = int(request.POST.get('units-required'))
            req.units_received = int(request.POST.get('units-received')) if request.POST.get('units-received') else 0
            req.date_time = datetime.strptime(request.POST.get('datetime'), '%Y-%m-%dT%H:%M') if request.POST.get('datetime') else None
            req.emergency = True if request.POST.get('emergency') else False
            req.save()
            if request.POST.get('stock'):
                stock = Stock.objects.get(id=int(request.POST.get('stock')))
                donation = Donation.objects.create(
                    group = req.group,
                    donor = stock.donor,
                    date = datetime.now(),
                    hospital = "Stock ID #" + str(stock.id),
                    comment = f"Request ID #{req.id}",
                )
                stock.status = 'Used'
                stock.donation = donation
                stock.receiver = req.requested_by
                stock.save()
                req.units_received = req.units_received + 1
                req.save()
                data['stocks'] = Stock.objects.filter(group=req.group, status='Available')
            messages.success(request, 'Request Updated Successfully')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'staff/request/detail.html', data)



@login_required(login_url='login')
def staff_donor_list(request):
    donors = Profile.objects.all()
    data = {
        'donors': donors
    }
    return render(request, 'staff/donor/list.html', data)


@login_required(login_url='login')
def staff_donor_add(request):
    return render(request, 'staff/donor/add.html')


@login_required(login_url='login')
def staff_stock_list(request):
    stocks = Stock.objects.all()
    if request.GET.get('group'):
        stocks = stocks.filter(group=request.GET.get('group'))
    if request.GET.get('status'):
        stocks = stocks.filter(status=request.GET.get('status'))

    data = {
        'stocks': stocks
    }
    return render(request, 'staff/stock/list.html', data)


@login_required(login_url='login')
def staff_stock_detail(request, pk):
    stock = Stock.objects.get(id=pk)
    data = {
        'stock': stock
    }
    if request.method == "POST":
        try:
            if stock.receiver is None and request.POST.get('receiver-mobile'):
                if Profile.objects.filter(mobile=request.POST.get('receiver-mobile')).exists():
                    profile = Profile.objects.get(mobile=request.POST.get('receiver-mobile'))
                elif Profile.objects.filter(mobile2=request.POST.get('receiver-mobile')).exists():
                    profile = Profile.objects.get(mobile=request.POST.get('receiver-mobile'))
                else:
                    profile = Profile.objects.create(
                        mobile = request.POST.get('receiver-mobile'),
                        group = stock.group,
                    )
                stock.receiver = profile
                stock.donation.reciever = profile
                stock.save()
                messages.success(request, 'Stock Updated Successfully')
                return redirect('staff_stock_list')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'staff/stock/detail.html', data)


@login_required(login_url='login')
def staff_stock_add(request):
    data = {
        'today': datetime.now().strftime('%Y-%m-%d'),
    }
    if request.method == "POST":
        # try:
            if Profile.objects.filter(mobile=request.POST.get('donor-mobile')).exists():
                profile = Profile.objects.get(mobile=request.POST.get('donor-mobile'))
            elif Profile.objects.filter(mobile2=request.POST.get('donor-mobile')).exists():
                profile = Profile.objects.get(mobile=request.POST.get('donor-mobile'))
            else:
                profile = Profile.objects.create(
                    mobile = request.POST.get('donor-mobile'),
                    group = request.POST.get('group'),
                )
            profile.last_donated = request.POST.get('date')
            profile.save()
            stock = Stock.objects.create(
                donor = profile,
                group = request.POST.get('group'),
                donated = datetime.strptime(request.POST.get('date'), '%Y-%m-%d'),
            )
            stock.save()
            donation= Donation.objects.create(
                group = request.POST.get('group'),
                donor = profile,
                date = request.POST.get('date'),
                hospital = f"Stock ID #{stock.id}",
            )
            stock.donation = donation
            stock.save()
            messages.success(request, 'Stock Added Successfully')
            return redirect('staff_stock_list')
        # except Exception as e:
        #     messages.error(request, str(e))
    return render(request, 'staff/stock/add.html', data)
