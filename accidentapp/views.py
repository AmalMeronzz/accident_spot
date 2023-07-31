from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.

def login_home(request):
    return render(request,'login_home.html')

def login(request):
    if request.method == 'POST':
        idname = request.POST['name']
        password = request.POST['password']
        print(idname,password)

        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id = '"+str(idname)+"' and password = '"+str(password)+"'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from station where station_id = '" + str(idname) + "' and password = '"+str(password)+"'")
            station = cursor.fetchone()
            if station == None:
                cursor.execute("select * from user_register where user_register = '"+str(idname)+"' and password = '"+str(password)+"'")
                user = cursor.fetchone()
                if user == None:
                    cursor.execute("select * from ambulance where idambulance = '" + str(idname) + "' and password = '" + str(password) + "'")
                    ambulance = cursor.fetchone()
                    if ambulance == None:
                        return redirect('login')
                    else:
                        request.session['ambulanceid'] = idname
                        return redirect('ambulancehome')
                else:
                    request.session["userid"] = idname
                    return redirect('userhome')
            else:
                request.session["stationid"] = idname
                return redirect('stationhome')
        else:
            request.session["adminid"] = idname
            return redirect('adminindex')
    else:
        return render(request,'login.html')

# ambulance
# ---------

def ambulance_home(request):
    return render(request,'ambulance/index.html')

def view_accident_cases(request):
    cursor =  connection.cursor()
    cursor.execute("select * from accident_spot where ambulance = 'pending' and status = 'approved'")
    accident = cursor.fetchall()
    return render(request,'ambulance/view_accident_cases.html',{'data':accident})

def ambulance_view_location(request,lat,lon):
    latitude = lat
    longitude = lon
    return render(request, 'ambulance/view_location.html', {'lat': latitude, 'lon': longitude})

def ambulance_accept(request,id):
    cursor = connection.cursor()
    cursor.execute("update accident_spot set ambulance = 'accepted' where idaccident_spot = '"+id+"'")
    print('----------------------------level 1')
    idambulance = request.session['ambulanceid']
    print(id,idambulance)
    cursor.execute("insert into confirm_request values(null,'"+id+"','"+idambulance+"')")
    print('-----------------------------level 2')
    return redirect('ambulancehome')

def view_accepted_request(request):
    idambulance = request.session['ambulanceid']
    cursor = connection.cursor()
    cursor.execute("select accident_spot.place,accident_spot.details,confirm_request.idambulance from accident_spot join confirm_request where accident_spot.ambulance = 'accepted' and confirm_request.idambulance = '"+idambulance+"' ")
    accepted = cursor.fetchall()
    return render(request,'ambulance/view_accepted_request.html',{'data':accepted})

# admin
# ----------------------------------------------------------------------------------------------------------------------
def logout(request):
    return redirect('loginhome')

def admin_home(request):
    return render(request,'admin/index.html')

def public_report(request):
    cursor = connection.cursor()
    cursor.execute("select * from accident_spot where status = 'pending'")
    accident = cursor.fetchall()
    return render(request,'admin/public_report.html',{'data':accident})

def accident_request_approve(request,id):
    cursor = connection.cursor()
    cursor.execute("update accident_spot set status = 'approved' where idaccident_spot = '"+id+"'")
    return redirect('publicreport')


def add_station(request):
    if request.method == 'POST':
        stationid = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("select * from station where station_id = '" + str(stationid) + "'")
        station = cursor.fetchone()
        if station == None:
            cursor.execute("insert into station values('" + str(stationid) + "','" + str(address) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "')")
            request.session["station_id"] = stationid
            return redirect('addstation')
        else:
            return HttpResponse("<script>alert('User Name already exists');window.location='../addstation';</script>")

    else:
        return render(request,'admin/add_station.html')

def add_ambulance(request):
    if request.method == 'POST':
        ambulanceid = request.POST['name']
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("insert into ambulance values('"+ambulanceid+"','"+name+"','"+address+"','"+email+"','"+phone+"','"+password+"')")
        return redirect('addambulance')
    else:
        return render(request,'admin/add_ambulance.html')

def view_ambulance(request):
    cursor = connection.cursor()
    cursor.execute("select * from ambulance")
    ambulance = cursor.fetchall()
    return render(request,'admin/view_ambulance.html',{'data':ambulance})

def delete_ambulance(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from ambulance where idambulance = '"+id+"'")
    return redirect('viewambulance')


def view_station(request):
    cursor = connection.cursor()
    cursor.execute("select * from station")
    station = cursor.fetchall()
    return render(request,'admin/view_station.html',{'data':station})

def edit_station(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        stationid = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']

        cursor.execute("update station set address = '"+str(address)+"',phone = '"+str(phone)+"',email = '"+str(email)+"',password = '"+str(password)+"' where station_id = '"+id+"'")
        return HttpResponseRedirect('editstation')

    else:
        cursor.execute("select * from station where station_id = '"+id+"'")
        print(id)
        station = cursor.fetchone()
        return render(request,'admin/edit_station.html',{'data':station})


def delete_station(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from station where station_id = '"+str(id)+"'")
    return redirect('viewstation')

def add_fine_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        cursor = connection.cursor()
        cursor.execute("insert into fine values(null,'"+str(name)+"','"+str(amount)+"')")
        return redirect('addfinecategory')
    else:
        return render(request,'admin/add_fine_category.html')

def view_fine_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from fine")
    fine = cursor.fetchall()
    return render(request,'admin/view_fine_category.html',{'data':fine})

def edit_fine_category(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']

        cursor.execute("update fine set name = '"+str(name)+"',amount = '"+str(amount)+"' where idfine ='"+id+"'")
        return redirect('viewfinecategory')
    else:
        cursor.execute("select * from fine where idfine = '"+id+"'")
        fine = cursor.fetchone()
        return render(request,'admin/edit_fine_category.html',{'data':fine})

def delete_fine_category(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from fine where idfine = '" + id + "'")
    return redirect('viewfinecategory')

def aview_station(request):
    cursor = connection.cursor()
    cursor.execute("select station.* from fuel_stations join station where station.station_id = fuel_stations.station_id")
    station = cursor.fetchall()
    return render(request,'admin/view_station1.html',{'data':station})

def aview_fuelstation(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from fuel_stations where station_id = '"+id+"'")
    fuel_station = cursor.fetchall()
    return render(request,'admin/view_fuel_station.html',{'data':fuel_station})

def view_location(request,lat,lon):
    return render(request,'admin/view_location.html',{'lat':lat,'lon':lon})

def delete_fuel_station1(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from fuel_stations where idfuel_stations = '"+id+"'")
    return redirect('aviewstation')

def view_accident_spot(request):
    cursor = connection.cursor()
    cursor.execute("select * from accident_spot where status = 'pending'")
    spot = cursor.fetchall()
    return render(request,'admin/view_accident_spot.html',{'data':spot})

def delete_accident_spot(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from accident_spot where idaccident_spot = '"+id+"'")
    return redirect('viewaccidentspot')


# station
# ---------------------------------------------------------------------------------------------------------------------

def station_home(request):
    return render(request,'station/index.html')

def station_logout(request):
    return render(request,'station/LogOut.html')

def station_add_accident_spot(request):
    if request.method == 'POST':
        place = request.POST['place']
        details = request.POST['details']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        cursor = connection.cursor()
        cursor.execute("insert into accident_spot values(null,'station','"+place+"','"+details+"','"+str(latitude)+"','"+str(longitude)+"','approved',curdate(),'pending')")
        return redirect('saddaccidentspot')
    else:
        return render(request,'station/add_accident_spot.html')

def station_view_accident_spot(request):
    cursor = connection.cursor()
    cursor.execute("select * from accident_spot where status = 'approved'")
    spot = cursor.fetchall()
    print(spot)
    return render(request,'station/view_accident_spot.html',{'data':spot})

def station_view_location(request,lat,lon):
    latitude = lat
    longitude = lon
    return render(request,'station/view_location.html',{'lat':latitude,'lon':longitude})

def add_fuel_station(request):
    if request.method == 'POST':
        station = request.session["stationid"]
        address = request.POST['address']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        cursor = connection.cursor()
        cursor.execute("insert into fuel_stations values(null,'"+station+"','"+address+"','"+str(latitude)+"','"+str(longitude)+"')")
        return redirect('addfuelstation')
    else:
        return render(request,'station/add_fuel_station.html')

def view_fuel_station(request):
    station = request.session["stationid"]
    cursor = connection.cursor()
    cursor.execute("select * from fuel_stations where station_id = '"+station+"'")
    fuel_station = cursor.fetchall()
    return render(request,'station/view_fuel_station.html',{'data':fuel_station})


def edit_fuel_station(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        address = request.POST['address']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        cursor.execute("update fuel_stations set address = '"+str(address)+"',latutude = '"+str(latitude)+"',longitude = '"+str(longitude)+"' where idfuel_stations = '"+id+"'")
        return redirect('viewfuelstation')
    else:
        cursor.execute("select * from fuel_stations where idfuel_stations = '"+id+"'")
        fuel_station = cursor.fetchone()
        return render(request,'station/edit_fuel_station.html',{'data':fuel_station})

def delete_fuel_station(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from fuel_stations where idfuel_stations = '"+id+"'")
    return redirect('viewfuelstation')

def station_view_fine_category(request):
   cursor = connection.cursor()
   cursor.execute("select * from fine")
   fine = cursor.fetchall()
   return render(request,'station/view_fine_category.html',{'data':fine})

def add_fine(request,id):
    if request.method == 'POST':
        date = request.POST['date']
        vehicle_no = request.POST['vehicle_no']

        cursor = connection.cursor()
        cursor.execute("insert into vehicle_fine values(null,'"+id+"','"+date+"','"+vehicle_no+"','not paid','none)")
        return redirect('sviewfinecategory')

    else:
        return render(request,'station/add_fine.html')

def view_fine_notpaid(request):
    cursor = connection.cursor()
    cursor.execute("select * from vehicle_fine where payment_status = 'not paid'")
    fine = cursor.fetchall()
    return render(request,'station/view_fine_notpaid.html',{'data':fine})

def view_fine_paid(request):
    cursor = connection.cursor()
    cursor.execute("select * from vehicle_fine where payment_status = 'paid'")
    fine = cursor.fetchall()
    return render(request,'station/view_fine_paid.html',{'data':fine})


# user
# -----------------------------------------------------------------------------------------------------------------------

def user_home(request):
    return render(request,'user/index.html')

def user_logout(request):
    return render(request,'user/LogOut.html')

def user_registration(request):
    if request.method == 'POST':
        userid = request.POST['name']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']

        cursor =  connection.cursor()
        cursor.execute("select * from user_register where user_register = '"+str(userid)+"'")
        user = cursor.fetchone()
        if user == None:
            cursor.execute("insert into user_register values('"+str(userid)+"','"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(email)+"','"+str(password)+"')")
            request.session["userid"] = userid
            return redirect('userhome')
        else:
            return HttpResponse("<script>alert('User Name already exists');window.location='../userregistration';</script>")

    else:
        return render(request,'user/user_register.html')

def user_add_accident_spot(request):
    if request.method == 'POST':
        userid = request.session["userid"]
        place = request.POST['place']
        details = request.POST['details']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        cursor = connection.cursor()
        cursor.execute("insert into accident_spot values(null,'"+userid+"','"+place+"','"+details+"','"+str(latitude)+"','"+str(longitude)+"','pending',curdate(),'pending')")
        return redirect('uaddaccidentspot')
    else:
        return render(request,'user/add_accident_spot.html')

def user_view_ambulance(request):
    cursor = connection.cursor()
    cursor.execute("select * from ambulance")
    ambulance = cursor.fetchall()
    return render(request,'user/view_ambulance.html',{'data':ambulance})

def user_view_station(request):
    cursor = connection.cursor()
    cursor.execute("select * from station")
    station = cursor.fetchall()
    return render(request,'user/view_station.html',{'data':station})

def user_view_station1(request):
    cursor = connection.cursor()
    cursor.execute("select station.* from fuel_stations join station where station.station_id = fuel_stations.station_id")
    station = cursor.fetchall()
    return render(request,'user/view_station1.html',{'data':station})

def user_view_fuelstation(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from fuel_stations where station_id = '"+id+"'")
    fuel_station = cursor.fetchall()
    return render(request,'user/view_fuel_station.html',{'data':fuel_station})

def user_view_location(request,lat,lon):
    latitude = lat
    longitude = lon
    return render(request,'user/view_location.html',{'lat':latitude,'lon':longitude})

def view_fine_amount(request):
    cursor = connection.cursor()
    cursor.execute("select * from fine")
    fine = cursor.fetchall()
    return render(request,'user/view_fine_amont.html',{'data':fine})

def check_fine(request):
    if request.method == 'POST':
        vehicle_no = request.POST['vehicle_no']
        cursor = connection.cursor()
        cursor.execute("select * from vehicle_fine where vehicle_no = '"+vehicle_no+"' and payment_status = 'not paid'")
        fine = cursor.fetchall()
        if fine == None:
            return HttpResponse("<script>alert('you have no fine');window.location='../checkfine';</script>")
        else:
            cursor.execute("select fine.*,vehicle_fine.fine_date,vehicle_fine.vehicle_no,vehicle_fine.idvehicle_fine  from fine join vehicle_fine where fine.idfine = vehicle_fine.idfine and vehicle_no = '"+vehicle_no+"'")
            fine_details = cursor.fetchall()
            return render(request,'user/check_out.html',{'data':fine_details})
    else:
        return render(request,'user/check_fine.html')

def make_payment(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        card_number = request.POST['card_no']
        cvv = request.POST['cvv']
        date = request.POST['date']
        card_holder =request.POST['card_holder']
        userid =  request.session["userid"]

        cursor.execute("select * from bank where account_no = '"+str(card_number)+"' and cvv = '"+str(cvv)+"' and expiry_date = '"+str(date)+"' and card_holder = '"+str(card_holder)+"'")
        card = cursor.fetchone()
        print("----------------------------------------------------------------------",card_number,date)
        if card == None:
            return redirect('makepayment',id)
        else:
            cursor.execute("update vehicle_fine set payment_status = 'paid',userid = '"+userid+"' where idvehicle_fine = '"+id+"'")
            return render(request,'user/success_page.html')
    else:
        cursor.execute("select * from bank")
        value = cursor.fetchone()
        return render(request,'user/paymentpage.html',{'i':value})


def check_paid_details(request):
    if request.method == 'POST':
        vehicle_no = request.POST['vehicle_no']
        userid =  request.session["userid"]
        cursor = connection.cursor()
        cursor.execute("select * from vehicle_fine where vehicle_no = '" + vehicle_no + "' and payment_status = 'paid' and userid = '"+userid+"'")
        fine = cursor.fetchall()
        if fine == None:
            return HttpResponse("<script>alert('you have no fine');window.location='../checkfine';</script>")
        else:
            cursor.execute("select fine.*,vehicle_fine.fine_date,vehicle_fine.vehicle_no,vehicle_fine.idvehicle_fine  from fine join vehicle_fine where fine.idfine = vehicle_fine.idfine and vehicle_no = '" + vehicle_no + "'")
            fine_details = cursor.fetchall()
            return render(request, 'user/check_out1.html', {'data': fine_details})
    else:
        return render(request,'user/check_paid_details.html')

