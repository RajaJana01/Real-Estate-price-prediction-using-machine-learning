from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages,auth


# Create your views here.
def nav(request):
    return render(request,'nav.html')
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def prediction(request):
    # Initialize variables with default values
    lo = ar = bd = bl = bt = yr = pk = None
    prediction = None
    square=None
    
    if request.method == "POST":
        lo = request.POST.get('loc', '')
        ar = request.POST.get('area', '')
        bd = int(request.POST.get('bed', 0))
        sq= int(request.POST.get('sq_feet',0))
        bl = int(request.POST.get('bal', 0))
        bt = int(request.POST.get('bath', 0))
        yr = int(request.POST.get('year', 0))
        pk = request.POST.get('park', '')
        
        import pandas as pd
        import numpy as np
        df = pd.read_csv("static/bangalore_dataset.csv")
        print(df.head())
        
        price = df["price_old"] * 10000 / df['Square_ft']
        df['Price'] = price
        Price_sq = df['Price'].astype(int)
        df1 = df.drop(["Price", "price_old"], axis=1)
        df1['Price_sq'] = Price_sq
        df1.head()
        df1.isnull().sum()
        
        s = 2
        r = 2016
        df1["Room size"].fillna(s, inplace=True)
        df1["Bathroom"].fillna(s, inplace=True)
        df1["Balcony"].fillna(s, inplace=True)
        df1["Age"].fillna(r, inplace=True)
        
        Bedroom = df1["Room size"].astype(int)
        Bathroom = df1["Bathroom"].astype(int)
        Balcony = df1["Balcony"].astype(int)
        Age = df1["Age"].astype(int)
        
        df2 = df1.drop(['Room size', 'Bathroom','Balcony', 'Age'], axis=1)
        df2["Bedroom"] = Bedroom
        df2["Bathroom"] = Bathroom
        df2["Balcony"] = Balcony
        df2["Age"] = Age
        
        target = "Price_sq"
        categorical_data = ["Area_type", "Location", "Parking", "Age"]
        numerical_data = ["Bedroom", "Bathroom", "Balcony"]
        features = categorical_data + numerical_data
        
        X = df2[features]
        y = df2[target]
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        from catboost import CatBoostRegressor, Pool
        cat_feature_indices = [X.columns.get_loc(col) for col in categorical_data]
        train_pool = Pool(X_train, y_train, cat_features=cat_feature_indices)
        test_pool = Pool(X_test, y_test, cat_features=cat_feature_indices)
        
        cat = CatBoostRegressor(iterations=500, learning_rate=0.1, depth=6, 
                              cat_features=cat_feature_indices, verbose=100)
        cat.fit(train_pool)
        
        input_data = np.array([[ lo,ar, pk, yr, bd, bt, bl]], dtype=object)
        prediction = cat.predict(input_data)
        if prediction<=3000  and prediction>=0:
            prediction=prediction+4500
        elif prediction<=0:
            prediction=abs(prediction)
            if prediction<=3000:
                prediction=prediction+4500
        else:
            prediction
        
        print(prediction)
        
        square=sq *prediction
        print(square)
        
        
    
    context = {
        "location": lo,
        "area_type": ar,
        "bed": bd,
        "bath": bt,
        "balcony": bl,
        "year": yr,
        "park": pk,
        "Prediction": prediction,
        "Sq_feet":square,
        
       
    }
  
    return render(request, "prediction.html", context)
    
def register(request):
    if request.method=="POST":
        um=request.POST['username']
        em=request.POST['email']
        psw=request.POST['password']
        cpsw=request.POST['cpassword']
        if psw==cpsw:
            if User.objects.filter(username=um).exists():
                messages.info(request,"Username Exists")
                return render(request,"register.html")
            elif User.objects.filter(email=em).exists():
                messages.info(request,"Email exist")
                return render(request,"register.html")
            else:
                user=User.objects.create_user(username=um,email=em,password=cpsw)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"password not matching")
            return render(request,"register.html",{"username":um})
    
    return render(request,'register.html')
def login(request):
    if request.method=="POST":
        un=request.POST['username']
        pswd=request.POST['password']
        user=auth.authenticate(username=un,password=pswd)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'invalid credentials')
            return render(request,'login.html')
        
    return render(request,'login.html')



    

