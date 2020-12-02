# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import csv
from Restaurant.models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

# 登录
def signin(request):
    if request.method == 'GET':
        if request.session.get('is_login', None):
            # 登录状态直接跳转
            return redirect('/index')
        else:
            return render(request, 'signin.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        print("用户名", username)
        password = request.POST.get('password', None)
        print("密码", password)
        if username and password:  # 确保账号和密码都不为空
            username = username.strip()  # 用户名字符合法性验证
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['id'] = user.id
                    return redirect('/index')
                else:
                    message = "The password Is Incorrect！"
            except:
                message = "User Information Does Not Exist！"
        return render(request, 'signin.html', {"message": message})
    else:
        return HttpResponseRedirect("不支持的请求方法")


# 注册
def signup(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册！
        return redirect('/index')
    if request.method == "POST":
        post = request.POST
        username = post.get('username')
        password = post.get('password')
        repassword = post.get('repassword')
        if username and password and repassword:  # 确保邮箱和密码都不为空
            username = username.strip()
            try:
                if User.objects.filter(username=username):
                    message = "User Information Already Exists,Do Not Register Again！"
                elif password != repassword:
                    message = "The Passwords Do Not Match！"
                else:
                    new_user = User.objects.create(username=username, password=password)
                    return redirect('/signin')
            except:
                return render(request, 'signup.html', {'message': None})
        return render(request, 'signup.html', {"message": message})
    return render(request, 'signup.html')


# 注销
def logout(request):
    # 如果本来就未登录，也就没有登出一说
    if not request.session.get('is_login', None):
        return redirect("/index")
    request.session.flush()
    return redirect("/signin")


# 主页面
def index(request):
    if request.method == 'GET':
        if request.session.get('is_login', None):
            user_id = request.session['id']
            search_info = SearchRecords.objects.filter(user_id=user_id)
            return render(request, 'index.html', {"search_info": search_info})
        # 未登录需先登录
        else:
            return render(request, 'signin.html')

    elif request.method == "POST":
        user_id = request.session['id']
        Search = request.POST.get('Search', None)
        new_Search = SearchRecords.objects.create(SearchInfo=Search, user_id=user_id)
        if is_number(Search):
            restaurant = Restaurant.objects.filter(postal_code__contains=Search)
        else:
            restaurant = Restaurant.objects.filter(name__icontains=Search)
        nCOv_list = []
        for res in restaurant:
            if NewCov.objects.filter(zipcode__icontains=res.postal_code).first() == None:
                nCOv_list.append([res, 0, 0])
            else:
                print(int(NewCov.objects.filter(zipcode__icontains=res.postal_code).first().case_rate))
                nCOv_list.append([res, int(NewCov.objects.filter(zipcode__icontains=res.postal_code).first().cases),
                                  int(NewCov.objects.filter(zipcode__icontains=res.postal_code).first().case_rate)])
        nCOv_list.sort(key=lambda x: (x[1]))
        if len(nCOv_list) > 20:
            nCOv_list = nCOv_list[:20]
        return render(request, 'about.html', {'restaurant': nCOv_list})


# 检索详情
def about(request):
    if request.method == 'GET':
        # print('开始处理数据')
        # sql_load()
        return render(request, 'index.html')
    elif request.method == "POST":
        Search = request.POST.get('Search', None)
        user_id = request.session['id']
        new_Search = SearchRecords.objects.create(SearchInfo=Search, user_id=user_id)
        # restaurant = Restaurant.objects.all()[:20]
        if is_number(Search):
            restaurant = Restaurant.objects.filter(postal_code__contains=Search)
        else:
            restaurant = Restaurant.objects.filter(name__icontains=Search)
        nCOv_list = []
        for res in restaurant:
            if NewCov.objects.filter(zipcode__icontains=res.postal_code).first() == None:
                nCOv_list.append([res, 0, 0])
                # nCOv_list.append(0)
            else:
                print('###')
                print(NewCov.objects.filter(zipcode__icontains=res.postal_code).first().case)
                nCOv_list.append([res, int(NewCov.objects.filter(zipcode__icontains=res.postal_code).first().cases),
                                  int(NewCov.objects.filter(zipcode__icontains=res.postal_code).first().case_rate)])
        nCOv_list.sort(key=lambda x: (x[1]))
        if len(nCOv_list) > 20:
            nCOv_list = nCOv_list[:20]
        return render(request, 'about.html', {'restaurant': nCOv_list})


def index_food(request):
    if request.method == 'GET':
        user_id = request.session['id']
        search_info = SearchRecords.objects.filter(user_id=user_id)
        return render(request, 'index_food.html', {"search_info": search_info})
        # return render(request, 'index_food.html')
    elif request.method == "POST":
        Search = request.POST.get('Search', None)
        user_id = request.session['id']
        new_Search = SearchRecords.objects.create(SearchInfo=Search, user_id=user_id)
        if is_number(Search):
            foods = Foods.objects.filter(energy_100g__lte=int(Search))
        else:
            foods = Foods.objects.filter(product_name__icontains=Search)
        food_list = []
        for food in foods:
            food_list.append([food, food.energy_100g])
        food_list.sort(key=lambda x: (x[1]), reverse=True)
        if len(food_list) > 20:
            food_list = food_list[:20]
        return render(request, 'about_food.html', {'food_list': food_list})


# 检索详情
def about_food(request):
    if request.method == 'GET':
        # print('开始处理数据')
        # sql_load()
        return render(request, 'index_food.html')
    elif request.method == "POST":
        Search = request.POST.get('Search', None)
        user_id = request.session['id']
        new_Search = SearchRecords.objects.create(SearchInfo=Search, user_id=user_id)
        if is_number(Search):
            foods = Foods.objects.filter(energy_100g__lte=int(Search))
        else:
            foods = Foods.objects.filter(product_name__icontains=Search)
        food_list = []
        for food in foods:
            food_list.append([food, food.energy_100g])
        food_list.sort(key=lambda x: (x[1]), reverse=True)
        if len(food_list) > 20:
            food_list = food_list[:20]
        return render(request, 'about_food.html', {'food_list': food_list})


def read_csv(path):
    data = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


def sql_load():
    main_path = '/Users/leigao/Downloads/RestaurantPoll/data'
    foods = read_csv(main_path + '/foods.csv')
    data_item = read_csv(main_path + '/yelp/data_item.csv')
    attributes = read_csv(main_path + '/yelp/attributes.csv')
    nCov_data = read_csv(main_path + '/yelp/nCov_data.csv')
    print('读取数据处理完毕')
    Foods.objects.all().delete()
    Restaurant.objects.all().delete()
    Atttributes.objects.all().delete()
    Hours.objects.all().delete()
    NewCov.objects.all().delete()
    for food in foods[1:]:
        try:
            int_1, int_2 = int(food[5]), int(food[5])
        except Exception:
            int_1, int_2 = 0, 0
        Foods.objects.create(code=food[0], creator=food[1], created_datetime=food[2], product_name=food[3],
                             countries=food[4], energy_100g=int_1, fat_100g=int_2)
    print('食物数据处理完毕')
    for i, data in enumerate(data_item[1:]):
        attribute = attributes[i]
        try:
            res = Restaurant.objects.create(business_id=data[0], name=data[1], address=data[2], city=data[3],
                                            state=data[4],
                                            postal_code=data[5], latitude=data[6], longitude=data[7], stars=data[8],
                                            review_count=data[9], is_open=data[10], categories=data[11])
            Atttributes.objects.create(business_id=res, BusinessAcceptsCreditCards=attribute[0],
                                       BikeParking=attribute[1], GoodForKids=attribute[2], BusinessParking=attribute[3],
                                       ByAppointmentOnly=attribute[4], RestaurantsPriceRange2=attribute[5])
            if i % 1000 == 0:
                print(i / len(data_item) * 100, "%")
        except Exception:
            continue
    print('餐厅数据处理完毕')
    for data in nCov_data[1:]:
        NewCov.objects.create(city=data[0], case_rate=data[1], cases=data[2], zipcode=data[3])
    print('新冠数据处理完毕')


def del_searchInfo(request):
    try:
        user_id = request.session['id']
        SearchRecords.objects.filter(user_id=user_id).delete()
        search_info = SearchRecords.objects.filter(user_id=user_id)
        return render(request, 'index.html', {"search_info": search_info})
        # return redirect('/index')
    except Exception:
        return HttpResponse("操作失败！")


#sql_load()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
