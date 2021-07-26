from flask import Flask,render_template,request,flash,redirect,session
from flask_session import Session
from flask_mysqldb import MySQL
import datetime
from werkzeug import secure_filename
import os



mgm = Flask(__name__)
mgm.secret_key = "secret key"
mgm.config['MYSQL_HOST'] = 'localhost'
mgm.config['MYSQL_USER'] = 'mgm_user'
mgm.config['MYSQL_PASSWORD'] = 'pass4mgm_user@^%$'
mgm.config['MYSQL_DB'] = 'abdulla_garage_mgm'
mgm.config['UPLOAD_FOLDER']='static/images'
mgm.config["SESSION_PERMANENT"] = False
mgm.config["SESSION_TYPE"] = "filesystem"
Session(mgm)

mysql = MySQL(mgm)






@mgm.route('/')
def index():
    if session.get('CURRENT_TAB')==None:
        session["CURRENT_TAB"] = "garage"
    return render_template('index.html',CURRENT_TAB=session["CURRENT_TAB"])
        
@mgm.route('/add_category')
def add_category():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    current_fn=str(request.url_rule).split('/')[1]
    if not session.get('LOGGED_IN'):
        flash("Login First","info")
        return redirect("/login")
    elif session.get('ALLOWED_FUNCTIONS') is None:
        flash("Login First","info")
        return redirect("/login")
    elif current_fn not in session.get('ALLOWED_FUNCTIONS'):
        flash("You are not allowed to use that function","info")
        return redirect("/")

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT CATEGORY FROM CATEGORIES;")
    mysql.connection.commit()
    resp=cursor.fetchall()
    cursor.close()
    response=[]
    for item in resp:
        response.append(item[0])
    cursor.close()
    return render_template('add_category.html',CURRENT_TAB=session["CURRENT_TAB"],existing_category_list=response)
    


@mgm.route('/add_manufacturer')
def add_manufacturer():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT MANUFACTURER FROM MANUFACTURERS;")
    mysql.connection.commit()
    resp=cursor.fetchall()
    response=[]
    for item in resp:
        response.append(item[0])
    cursor.close()
    return render_template('add_manufacturer.html',CURRENT_TAB=session["CURRENT_TAB"],existing_manufacturers_list=response)

@mgm.route('/add_vendor')
def add_vendor():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT VENDOR FROM VENDORS;")
    mysql.connection.commit()
    resp=cursor.fetchall()
    response=[]
    for item in resp:
        response.append(item[0])
    cursor.close()
    return render_template('add_vendor.html',CURRENT_TAB=session["CURRENT_TAB"],existing_vendors_list=response)



@mgm.route('/add_product')
def add_product():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT CID,CATEGORY FROM CATEGORIES;")
    mysql.connection.commit()
    unsorted_categories=cursor.fetchall()
    
    cursor.execute("SELECT MID,MANUFACTURER FROM MANUFACTURERS;")
    mysql.connection.commit()
    unsorted_manufacturers=cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT PRODUCT_NAME FROM PRODUCT_TABLE;")
    mysql.connection.commit()
    unsorted_product_names=cursor.fetchall()
    
    cursor.close()
    categories=[]
    for item in unsorted_categories:
        categories.append([item[0],item[1]])
    manufacturers=[]
    for item in unsorted_manufacturers:
        manufacturers.append([item[0],item[1]])
    product_names=[]
    for item in unsorted_product_names:
        product_names.append(item[0])
    return render_template('add_product.html',CURRENT_TAB=session["CURRENT_TAB"],categories=categories,manufacturers=manufacturers,existing_product_names_list=product_names)




@mgm.route('/add_purchase')
def add_purchase():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT CATEGORY FROM CATEGORIES;")
    mysql.connection.commit()
    unsorted_categories=cursor.fetchall()
    
    cursor.execute("SELECT MANUFACTURER FROM MANUFACTURERS;")
    mysql.connection.commit()
    unsorted_manufacturers=cursor.fetchall()
    
    
    cursor.execute("SELECT VENDOR FROM VENDORS;")
    mysql.connection.commit()
    unsorted_vendors=cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT PID,PRODUCT_NAME FROM PRODUCT_TABLE;")
    mysql.connection.commit()
    unsorted_product_names=cursor.fetchall()
    cursor.close()
    
    date_today=str(datetime.date.today())
    categories=[]
    for item in unsorted_categories:
        categories.append(item[0])
    manufacturers=[]
    for item in unsorted_manufacturers:
        manufacturers.append(item[0])
    vendors=[]
    for item in unsorted_vendors:
        vendors.append(item[0])
    products=[]
    for item in unsorted_product_names:
        product_id=item[0]
        product_name=item[1]
        products.append([product_id,product_name])
    
    return render_template('add_purchase.html',CURRENT_TAB=session["CURRENT_TAB"],date_today=date_today,categories=categories,manufacturers=manufacturers,vendors=vendors,products=products)




@mgm.route('/add_category_return',methods = ['POST'])
def add_category_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    new_category=request.form['new_category']
    cursor = mysql.connection.cursor()
    cmnd='INSERT INTO CATEGORIES (CATEGORY) VALUES(%s);'
    cursor.execute(cmnd,(new_category,))
    mysql.connection.commit()
    cursor.close()
    flash("Category Added Successfully","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])


@mgm.route('/add_manufacturer_return',methods = ['POST'])
def add_manufacturer_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    new_manufacturer=request.form['new_manufacturer']
    cursor = mysql.connection.cursor()
    cmnd="INSERT INTO MANUFACTURERS (MANUFACTURER) VALUES(%s);"
    cursor.execute(cmnd,(new_manufacturer,))
    mysql.connection.commit()
    cursor.close()
    flash("Manufacturer Added Successfully","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])


@mgm.route('/add_vendor_return',methods = ['POST'])
def add_vendor_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    new_vendor=request.form['new_vendor']
    cursor = mysql.connection.cursor()
    cmnd="INSERT INTO VENDORS (VENDOR) VALUES(%s);"
    response=cursor.execute(cmnd,(new_vendor,))
    mysql.connection.commit()
    cursor.close()
    flash("Vendor Added Successfully","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])


@mgm.route('/add_product_return',methods = ['POST'])
def add_product_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    product_name=request.form['product_name']
    category_id=int(request.form['category'])
    
    manufacturer_id=int(request.form['manufacturer'])
    description=request.form['description']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT CATEGORY FROM CATEGORIES WHERE CID=%d"%category_id)
    category=cursor.fetchall()[0][0]
    
    if "'" in product_name:
        product_name=product_name.replace("'","''")
    
    if "'" in description:
        description=description.replace("'","''")
    
    
    cursor.execute("SELECT MANUFACTURER FROM MANUFACTURERS WHERE MID=%d"%manufacturer_id)
    manufacturer=cursor.fetchall()[0][0]
    
    mid=manufacturer_id
    cid=category_id
    cmnd="INSERT INTO PRODUCT_TABLE (PRODUCT_NAME,CATEGORY,MANUFACTURER,DESCRIPTION,CID,MID) VALUES(%s,%s,%s,%s,%s,%s)"
    
    cursor.execute(cmnd,(product_name,category,manufacturer,description,str(cid),str(mid)))
    
    
    mysql.connection.commit()
    cursor.close()
    flash("Product Added Successfully","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
    
    


@mgm.route('/add_purchase_return',methods = ['POST'])
def add_purchase_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    product_id=int(request.form['product_id'])
    category=request.form['category']
    manufacturer=request.form['manufacturer']
    remarks=request.form['remarks']
    vendor=request.form['vendor']
    invoice_number=request.form['invoice_number']
    
    date=request.form['date_of_purchase']
    units=float(request.form['units'])
    pricing_option=request.form['pricing_option']
    if pricing_option=='price_per_box':
        cp=float(request.form['cp'])/units
        sp=float(request.form['sp'])/units
    if pricing_option=='price_per_unit':
        cp=float(request.form['cp'])
        sp=float(request.form['sp'])
    cursor = mysql.connection.cursor()
    cmnd="SELECT PRODUCT_NAME FROM PRODUCT_TABLE WHERE PID=%s"
    cursor.execute(cmnd,(str(product_id),))
    
    product_name=cursor.fetchall()[0][0]
    cmnd="INSERT INTO PURCHASE_DATA (CATEGORY,VENDOR,MANUFACTURER,PRODUCT_NAME,INVOICE_NUMBER,DATE,CP,SP,UNITS,REMARKS,PID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(cmnd,(category,vendor,manufacturer,product_name,str(invoice_number),date,str(cp),str(sp),str(units),remarks,str(product_id)))
    
    
    cmnd="SELECT EXISTS(SELECT * FROM CURRENT_STOCK_TABLE WHERE CATEGORY=%s AND MANUFACTURER=%s AND PRODUCT_NAME=%s)"
    cursor.execute(cmnd,(category,manufacturer,product_name))
    
    flag=cursor.fetchall()[0][0]
    if flag==0:
        lot=1
        cmnd="INSERT INTO CURRENT_STOCK_TABLE (CATEGORY,MANUFACTURER,PRODUCT_NAME,LOT,UNITS,CP,SP,REMARKS,PID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(cmnd,(category,manufacturer,product_name,str(lot),str(units),str(cp),str(sp),remarks,str(product_id)))
    if flag==1:
        sub_cmnd="SELECT EXISTS(SELECT * FROM CURRENT_STOCK_TABLE WHERE CATEGORY=%s AND MANUFACTURER=%s AND PRODUCT_NAME=%s AND CP=%s AND SP=%s)"
        cursor.execute(sub_cmnd,(category,manufacturer,product_name,str(cp),str(sp)))
        mysql.connection.commit()
        inner_flag=cursor.fetchall()[0][0]
        if inner_flag==0:
            sub_cmnd="SELECT MAX(LOT) FROM CURRENT_STOCK_TABLE WHERE CATEGORY=%s AND MANUFACTURER=%s AND PRODUCT_NAME=%s"
            cursor.execute(sub_cmnd,(category,manufacturer,product_name))
            mysql.connection.commit()
            max_lot=int(cursor.fetchall()[0][0])
            new_lot=max_lot+1
            cmnd="INSERT INTO CURRENT_STOCK_TABLE (CATEGORY,MANUFACTURER,PRODUCT_NAME,LOT,UNITS,CP,SP,REMARKS,PID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(cmnd,(category,manufacturer,product_name,str(new_lot),str(units),str(cp),str(sp),remarks,str(product_id)))
        if inner_flag==1:
            sub_cmnd="SELECT MAX(INVENTORY_ID) FROM CURRENT_STOCK_TABLE WHERE CATEGORY='%s' AND MANUFACTURER='%s' AND PRODUCT_NAME='%s' AND CP=%f AND SP=%f"%(category,manufacturer,product_name,cp,sp)
            cursor.execute(sub_cmnd)
            mysql.connection.commit()
            inv_id=int(cursor.fetchall()[0][0])
            cmnd="UPDATE CURRENT_STOCK_TABLE SET UNITS=UNITS+%d WHERE INVENTORY_ID=%d"%(units,inv_id)
            cursor.execute(cmnd,(str(units),str(inv_id)))
    
    
    mysql.connection.commit()
  
    cursor.close()
    flash("Purchase Recorded Successfully","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])

@mgm.route('/show_current_stock')
def show_current_stock():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM CURRENT_STOCK_TABLE;")
    mysql.connection.commit()
    unsorted_stocks=cursor.fetchall()
    unsorted_headings=cursor.description
    cursor.close()
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0])
    for row in unsorted_stocks:
        stock_row=[]
        for col in row:
            stock_row.append(col)
        data.append(stock_row)
    return render_template('show_current_stock.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)



@mgm.route('/show_purchase_data')
def show_purchase_data():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM PURCHASE_DATA;")
    mysql.connection.commit()
    unsorted_purchase_data=cursor.fetchall()
    unsorted_headings=cursor.description
    cursor.close()
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0])
    for row in unsorted_purchase_data:
        stock_row=[]
        for col in row:
            stock_row.append(col)
        data.append(stock_row)
    return render_template('show_purchase_data.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)


@mgm.route('/remove_spoils')
def remove_spoils():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM CURRENT_STOCK_TABLE;")
    mysql.connection.commit()
    unsorted_stocks=cursor.fetchall()
    unsorted_headings=cursor.description
    cursor.close()
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0])
    for row in unsorted_stocks:
        stock_row=[]
        for col in row:
            stock_row.append(col)
        data.append(stock_row)
    return render_template('remove_spoils.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)


@mgm.route('/remove_spoils_return')
@mgm.route('/remove_spoils_return/<inv_id>')
def remove_spoils_return(inv_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if inv_id!=None:
       inv_id=int(inv_id)
       return render_template('remove_spoils_number.html',CURRENT_TAB=session["CURRENT_TAB"],inv_id=inv_id)
    else:
        return "Nothing Selected"

@mgm.route('/remove_spoils_return_second',methods=['POST'])
def remove_spoils_return_second():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    inv_id=int(request.form['inv_id'])
    units=float(request.form['units'])
    remarks=request.form['remarks']
    cursor = mysql.connection.cursor()
    cmnd="UPDATE CURRENT_STOCK_TABLE SET UNITS=UNITS-%s WHERE INVENTORY_ID=%s"
    cursor.execute(cmnd,(str(units),str(inv_id)))
    cmnd="INSERT INTO SPOILS_TABLE (CATEGORY,MANUFACTURER,PRODUCT_NAME,LOT,UNITS,CP,SP,REMARKS,PID,INVENTORY_ID) SELECT CATEGORY,MANUFACTURER,PRODUCT_NAME,LOT,%s,CP,SP,%s,PID,INVENTORY_ID FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%s"
    cursor.execute(cmnd,(str(units),remarks,str(inv_id)))
    mysql.connection.commit()
    cursor.close()
    flash("Spoils Removed Successfully","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
    
    

@mgm.route('/show_spoils')
def show_spoils():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM SPOILS_TABLE;")
    mysql.connection.commit()
    unsorted_spoils=cursor.fetchall()
    unsorted_headings=cursor.description
    cursor.close()
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0])
    for row in unsorted_spoils:
        stock_row=[]
        for col in row:
            stock_row.append(col)
        data.append(stock_row)
    return render_template('show_spoils.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)


@mgm.route('/edit_job_card/<job_id>')
def edit_job(job_id=None):
    if job_id !=None:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATE_IN,TIME_IN,CUSTOMER_NAME,CUSTOMER_ID_NUM,CUSTOMER_PHONE_NUM,COMPANY,MODEL,VARIANT,MAKE,REGISTRATION_NUM,KM,ESTIMATED_DATE_OF_COMPLETION,ESTIMATED_TIME_OF_COMPLETION,ESTIMATED_COST,DISCOUNTED_PRICE,ADVANCE,DASH_IND,DASH_CMNT,CUSTOMER_PROBLEMS,TIME_ASSIGNED,TIME_COMPLETION,TIME_OUT,DATE_COMPLETION,DATE_OUT,STATUS,EMPLOYEE_ASSIGNED,DATE_ASSIGNED,CUSTOMER_EMAIL,CHASIS_NUMBER,ENGINE_NUMBER,TASKS,JOB_TYPE,NOTE,ESTIMATED_PARTS_COST,ESTIMATED_LABOUR_CHARGE,INSURANCE,INSURANCE_FILE_NUMBER FROM JOB_CARDS WHERE JOB_ID=%s",(job_id,))
        details=cursor.fetchall()
        time_in=str(details[0][1])
        estimated_time_of_completion=str(details[0][12])
        time_out=str(details[0][21])
        time_assigned=str(details[0][19])
        time_completion=str(details[0][20])
        if time_in is not None:
            time_in=time_in.split(":")
            if int(time_in[0])<10 and int(time_in[0])!=0:
                time_in[0]="0"+time_in[0]
            time_in=time_in[0]+":"+time_in[1]
            
        
        if estimated_time_of_completion is not None:
            estimated_time_of_completion=estimated_time_of_completion.split(":")
            if int(estimated_time_of_completion[0])<10 and int(estimated_time_of_completion[0])!=0:
                estimated_time_of_completion[0]="0"+estimated_time_of_completion[0]
            estimated_time_of_completion=estimated_time_of_completion[0]+":"+estimated_time_of_completion[1]
            
        
            
        form_data={
        "date_in":details[0][0],
        "time_in":time_in,
        "customer_name":details[0][2],
        "customer_id_num":details[0][3],
        "customer_phone_num":details[0][4],
        "company":details[0][5],
        "model":details[0][6],
        "variant":details[0][7],
        "make":details[0][8],
        "registration_num":details[0][9],
        "km":details[0][10],
        "estimated_date_of_completion":details[0][11],
        "estimated_time_of_completion":estimated_time_of_completion,
        "estimated_cost":details[0][13],
        "discounted_price":details[0][14],
        "advance":details[0][15],
        "dash_ind":details[0][16],
        "dash_cmnt":details[0][17],
        "customer_problems":details[0][18],
        "time_assigned":time_assigned,
        "time_completion":time_completion,
        "time_out":time_out,
        "date_completion":details[0][22],
        "date_out":details[0][23],
        "status":details[0][24],
        "employee_assigned":details[0][25],
        "date_assigned":details[0][26],
        "customer_email":details[0][27],
        "chasis_number":details[0][28],
        "engine_number":details[0][29],
        "tasks":details[0][30],
        "job_type":details[0][31],
        "note":details[0][32],
        "estimated_parts_cost":details[0][33],
        "estimated_labour_charge":details[0][34],
        "insurance":details[0][35],
        "insurance_file_number":details[0][36]
        }
        
        cursor.close()
        return render_template('edit_job_card.html',CURRENT_TAB=session["CURRENT_TAB"],form_data=form_data,job_id=job_id)
    
@mgm.route('/add_job_card')
def add_job_card(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    date_today=str(datetime.date.today())
    time_now=datetime.datetime.now().strftime("%H:%M")
    
    return render_template('add_job_card.html',CURRENT_TAB=session["CURRENT_TAB"],time_now=time_now,date_today=date_today)
    

@mgm.route('/add_job_card_return/edit',endpoint='edit',methods=['POST'])
@mgm.route('/add_job_card_return',endpoint='new',methods=['POST'])
def add_job_card_return():
    
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    date_in=request.form['date_in']
    time_in=request.form['time_in']
    customer_name=request.form['customer_name']
    customer_id_num=request.form['customer_id_num']
    customer_phone_num=request.form['phone_num']
    customer_email=request.form['email']
    company=request.form['company']
    model=request.form['model']
    variant=request.form['variant']
    make=0
    insurance_file_number=request.form['insurance_file_number']
    if request.form['make']!='':
        make=int(request.form['make'])
    registration_num=request.form['reg_number']
    engine_number=request.form['engine_number']
    chasis_number=request.form['chasis_number']
    km=0
    if request.form['km']!='':
        km=int(request.form['km'])
    
    estimated_time=request.form['estimated_time']
    estimated_delivery_date=request.form['estimated_delivery_date']
    estimated_labour_charge=0
    discount=0
    advance=0
    estimated_part_cost=0
    if request.form['estimated_labour_charge']!='':
        estimated_labour_charge=float(request.form['estimated_labour_charge'])
    if request.form['estimated_part_cost']!='':
        estimated_part_cost=float(request.form['estimated_part_cost'])
    estimated_cost=estimated_labour_charge+estimated_part_cost
    if request.form['discount']!='':
        discount=float(request.form['discount'])
    if request.form['advance']!='':
        advance=float(request.form['advance'])
    dashboard_cmnt=request.form['dashboard_cmnt']
    customer_complaints=request.form['customer_complaints']
    notes=request.form['notes']
    insurance=request.form['insurance']
    estimated_parts_cost=request.form['estimated_part_cost']
    estimated_labour_charge=request.form['estimated_labour_charge']
    raw_dashboard_ind=request.form.getlist('dash_ind[]')
    raw_tasks=request.form.getlist('tasks[]')
    raw_job_type=request.form.getlist('type_of_job[]')
    
    dashboard_ind=""
    for item in raw_dashboard_ind:
        dashboard_ind+=str(item)+","
        
    tasks=""
    for item in raw_tasks:
        tasks+=str(item)+"," 
    
    job_type=""
    for item in raw_job_type:
        job_type+=str(item)+","
    cursor = mysql.connection.cursor()
    car_images=request.files.getlist('img_files[]')
    edit=0
    if "edit" in request.form:
        if request.form['edit']=="1":
            edit=1
            job_id=int(request.form['job_id'])
            cmnd="UPDATE JOB_CARDS SET DATE_IN=%s,TIME_IN=%s,CUSTOMER_NAME=%s,CUSTOMER_ID_NUM=%s,CUSTOMER_PHONE_NUM=%s,CUSTOMER_EMAIL=%s,COMPANY=%s,MODEL=%s,VARIANT=%s,MAKE=%s,REGISTRATION_NUM=%s,CHASIS_NUMBER=%s,ENGINE_NUMBER=%s,KM=%s,JOB_TYPE=%s,ESTIMATED_TIME_OF_COMPLETION=%s,ESTIMATED_DATE_OF_COMPLETION=%s,ESTIMATED_COST=%s,DISCOUNTED_PRICE=%s,ADVANCE=%s,DASH_IND=%s,DASH_CMNT=%s,CUSTOMER_PROBLEMS=%s,TASKS=%s,NOTE=%s,ESTIMATED_PARTS_COST=%s,ESTIMATED_LABOUR_CHARGE=%s,INSURANCE=%s,INSURANCE_FILE_NUMBER=%s WHERE JOB_ID=%s;"
            cursor.execute(cmnd,(date_in,time_in,customer_name,customer_id_num,str(customer_phone_num),customer_email,company,model,variant,str(make),registration_num,chasis_number,engine_number,str(km),job_type,estimated_time,estimated_delivery_date,str(estimated_cost),str(discount),str(advance),dashboard_ind,dashboard_cmnt,customer_complaints,tasks,notes,estimated_parts_cost,estimated_labour_charge,insurance,insurance_file_number,str(job_id)))
    else:        
        cmnd="INSERT INTO JOB_CARDS (DATE_IN,TIME_IN,CUSTOMER_NAME,CUSTOMER_ID_NUM,CUSTOMER_PHONE_NUM,CUSTOMER_EMAIL,COMPANY,MODEL,VARIANT,MAKE,REGISTRATION_NUM,CHASIS_NUMBER,ENGINE_NUMBER,KM,JOB_TYPE,ESTIMATED_TIME_OF_COMPLETION,ESTIMATED_DATE_OF_COMPLETION,ESTIMATED_COST,DISCOUNTED_PRICE,ADVANCE,DASH_IND,DASH_CMNT,CUSTOMER_PROBLEMS,TASKS,NOTE,ESTIMATED_PARTS_COST,ESTIMATED_LABOUR_CHARGE,INSURANCE,INSURANCE_FILE_NUMBER) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(cmnd,(date_in,time_in,customer_name,customer_id_num,str(customer_phone_num),customer_email,company,model,variant,str(make),registration_num,chasis_number,engine_number,str(km),job_type,estimated_time,estimated_delivery_date,str(estimated_cost),str(discount),str(advance),dashboard_ind,dashboard_cmnt,customer_complaints,tasks,notes,estimated_parts_cost,estimated_labour_charge,insurance,insurance_file_number))
        cursor.execute("SELECT LAST_INSERT_ID();")
        job_id=cursor.fetchall()[0][0]
    fil_ind=1
    image_names=[]
    
    for file in car_images:
        ext=os.path.splitext(file.filename)[-1]
        filename = str(job_id)+"-"+str(date_in)+"-"+str(time_in)+customer_name+company+model+variant+str(make)+"-"+str(fil_ind)+ext
        file.save(os.path.join(mgm.config['UPLOAD_FOLDER'],filename))
        fil_ind+=1
        image_names.append(os.path.join(mgm.config['UPLOAD_FOLDER'],filename))
    for img in image_names:
        cmnd="INSERT INTO IMAGE_DB (JOB_ID,FILENAME) VALUES (%s,%s)"
        cursor.execute(cmnd,(str(job_id),img))
    mysql.connection.commit()
    cursor.close()
    if edit==0:
        msg="Job Added Successfully"
    elif edit==1:
        msg="Job Edited Successfully"
        
    flash(msg,"info")
    
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
    
@mgm.route('/show_job/<job_id>')
def show_job(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        job_id=int(job_id)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM JOB_CARDS WHERE JOB_ID=%d;"%job_id)
        mysql.connection.commit()
        result=cursor.fetchall()
        unsorted_headings=cursor.description
        cursor.close()
        data=[]
        i=0
        for head in unsorted_headings:
            if isinstance(result[0][i], str) and "," in result[0][i]:
                temp=result[0][i].split(",")
                if "" in temp:
                    temp.remove("")
                data.append([head[0].replace("_"," "),temp])
            else:
                data.append([head[0].replace("_"," "),result[0][i]])
            i=i+1
        return render_template('show_job.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,job_id=job_id)
    else:
        flash("No job Selected","info")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
    
@mgm.route('/select_for_work')
@mgm.route('/select_for_work/<job_id>')
def select_for_work(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        job_id=int(job_id)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM EMPLOYEE_TABLE;")
        mysql.connection.commit()
        result=cursor.fetchall()
        emp_lst=[]
        for item in result:
            emp_id=item[0]
            emp_name=item[1]
            emp_lst.append([emp_id,emp_name])
        cursor.close()
        date_today=str(datetime.date.today())
        time_now=datetime.datetime.now().strftime("%H:%M")
        return render_template('select_for_work.html',CURRENT_TAB=session["CURRENT_TAB"],emp_lst=emp_lst,job_id=job_id,date_today=date_today,time_now=time_now)    
    else:
        flash("No job selected for working")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
 

@mgm.route('/select_for_work_return',methods=['POST'])
@mgm.route('/select_for_work_return/<job_id>',methods=['POST'])
def select_for_work_return(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        employee_id=int(request.form['employee_id'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT EMPLOYEE_NAME FROM EMPLOYEE_TABLE WHERE EMPLOYEE_ID=%d;"%(int(employee_id)))
        result=cursor.fetchall()
        employee_name=result[0][0]
        date_assigned=str(request.form['date_assigned'])
        time_assigned=str(request.form['time_assigned'])
        cmnd="UPDATE JOB_CARDS SET EMPLOYEE_ASSIGNED=%s,DATE_ASSIGNED=%s, TIME_ASSIGNED=%s, STATUS='ASSIGNED' WHERE JOB_ID=%s ;"
        cursor.execute(cmnd,(str(employee_id),date_assigned,time_assigned,str(job_id)))
        flash("Job "+str(job_id)+" Assigned to "+str(employee_name),"info")
        mysql.connection.commit()
        cursor.close()
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
    else:
        flash("No job selected for working")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
    
@mgm.route('/show_unassigned_jobs')
def show_unassigned_jobs():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT JOB_ID,DATE_IN,MODEL,REGISTRATION_NUM,JOB_TYPE,ESTIMATED_DATE_OF_COMPLETION,STATUS FROM JOB_CARDS WHERE EMPLOYEE_ASSIGNED=0 ORDER BY JOB_ID DESC;")
    mysql.connection.commit()
    result=cursor.fetchall()
    unsorted_headings=cursor.description
    cursor.close()
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0].replace("_"," "))
    for row in result:
        job_row=[]
        for col in row:
            job_row.append(col)
        data.append(job_row)
    return render_template('show_unassigned_jobs.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)
    
@mgm.route('/show_assigned_jobs')
def show_assigned_jobs():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT JOB_ID,DATE_IN,TIME_IN,CUSTOMER_NAME,COMPANY,MODEL,JOB_TYPE,EMPLOYEE_ASSIGNED,TIME_ASSIGNED,STATUS FROM JOB_CARDS WHERE STATUS='ASSIGNED' AND EMPLOYEE_ASSIGNED!=0 ORDER BY JOB_ID DESC;")
    mysql.connection.commit()
    result=cursor.fetchall()
    unsorted_headings=cursor.description
    
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0].replace("_"," "))
    for row in result:
        job_id=row[0]
        date_in=row[1]
        time_in=row[2]
        customer_name=row[3]
        company=row[4]
        model=row[5]
        job_type=row[6]
        employee_id=row[7]
        time_assigned=row[8]
        status=row[9]
        cursor.execute("SELECT EMPLOYEE_NAME FROM EMPLOYEE_TABLE WHERE EMPLOYEE_ID=%s",(employee_id,))
        employee_name=cursor.fetchall()[0][0]
        data.append([job_id,date_in,time_in,customer_name,company,model,job_type,employee_name,time_assigned,status])
    cursor.close()
    return render_template('show_assigned_jobs.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)
    
            
 
@mgm.route('/add_employee')
def add_employee():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT EMPLOYEE_ID,EMPLOYEE_NAME,JOB_ROLE FROM EMPLOYEE_TABLE;")
    
    resp=cursor.fetchall()
    emp_lst=[]
    for item in resp:
        emp_id=item[0]
        emp_name=item[1]
        job_role_id=item[2]
        cursor.execute("SELECT JOB_ROLE FROM JOB_ROLES WHERE RID=%s",(job_role_id,))
        job_role=cursor.fetchall()[0][0]
        emp_lst.append([emp_id,emp_name,job_role])
    cursor.execute("SELECT RID,JOB_ROLE FROM JOB_ROLES")
    resp=cursor.fetchall()
    job_roles=[]
    for item in resp:
        job_roles.append([item[0],item[1]])
    cursor.close()
    return render_template('add_employee.html',CURRENT_TAB=session["CURRENT_TAB"],existing_employee_list=emp_lst,job_roles=job_roles)
      
@mgm.route('/add_employee_return',methods=['POST'])
def add_employee_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    new_employee=request.form['new_employee']
    username=request.form['username']
    password=request.form['password']
    job_role=request.form['job_role']
    cursor = mysql.connection.cursor()
    cmnd="INSERT INTO EMPLOYEE_TABLE (EMPLOYEE_NAME,USERNAME,PASSWORD,JOB_ROLE) VALUES(%s,%s,PASSWORD(%s),%s);"
    response=cursor.execute(cmnd,(new_employee,username,password,job_role))
    mysql.connection.commit()
    cursor.close()
    flash("Employee Added Successfully","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
        

@mgm.route('/view_images')
@mgm.route('/view_images/<job_id>')
def view_images(job_id=1):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT FILENAME FROM IMAGE_DB WHERE JOB_ID=%d"%int(job_id))
    mysql.connection.commit()
    result=cursor.fetchall()
    filepaths=[]
    for item in result:
        filepaths.append(item[0])
    cursor.close()
    return render_template('show_images.html',CURRENT_TAB=session["CURRENT_TAB"],filepaths=filepaths)


@mgm.route('/delete_work')
@mgm.route('/delete_work/<job_id>')
def delete_work(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    #modify code to check if the status is unassigned. in assigned jobs section, put opstion to 
    #unassign, while unassigning, make sure spare cart is empty. this is to ensure that deleting work 
    #is done after returning all items to store
    
    cursor = mysql.connection.cursor()
    if job_id:
        cursor.execute("SELECT STATUS FROM JOB_CARDS WHERE JOB_ID=%s",(job_id,))
        status=cursor.fetchall()[0][0]
        if status=="UNASSIGNED" or status=="STATUS NOT SET":
            cursor.execute("SELECT FILENAME FROM IMAGE_DB WHERE JOB_ID=%d"%int(job_id))
            mysql.connection.commit()
            result=cursor.fetchall()
            files=[]
            for item in result:
                files.append(item[0].split('/')[2])
            for file in files:
                os.remove(os.path.join(mgm.config['UPLOAD_FOLDER'], file))
            cursor.execute("DELETE FROM JOB_CARDS WHERE JOB_ID=%d"%int(job_id))
            cursor.execute("DELETE FROM IMAGE_DB WHERE JOB_ID=%d"%int(job_id))
            mysql.connection.commit()
            cursor.close()
            flash("Job "+str(job_id)+" Deleted")
            return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
        else:
            cursor.close()
            flash("Unassign the job first")
            return redirect('/show_assigned_jobs')
            
    else:
        flash("No job selected for deletion")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
        
        
    
@mgm.route('/request_spare_store/<job_id>',methods=['POST','GET'])
def request_spare_store(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        products=[]
        cursor.execute("SELECT DISTINCT CATEGORY FROM CURRENT_STOCK_TABLE")
        results=cursor.fetchall()
        categories=[]
        for category in results:
            categories.append(category[0])

        job_id=int(job_id)
        #show items in cart for the job
        cursor.execute("SELECT INVENTORY_ID,UNITS FROM PART_REQUESTS_STORE WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_store=[]
        for item in results:
            inv_id=int(item[0])
            units=float(item[1])
            cursor.execute("SELECT PRODUCT_NAME,LOT FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%d"%(inv_id))
            resp=cursor.fetchall()
            product_name=resp[0][0]
            lot=resp[0][1]
            cart_items_store.append([inv_id,product_name,lot,units])
        cursor.execute("SELECT RID,PART,UNITS,STATUS FROM PART_REQUESTS_OUT WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_out=[]
        i=0
        for item in results:
            request_id=item[0]
            part=item[1]
            units=int(item[2])
            status=item[3]
            cart_items_out.append([request_id,part,units,status])
            
        #if category is already chosen, list the items from current stock
        if 'category' in request.form:
            category=request.form['category']
            #list inventory(current stock)with add to cart option
            cursor.execute("SELECT INVENTORY_ID,MANUFACTURER,PRODUCT_NAME,LOT FROM CURRENT_STOCK_TABLE WHERE CATEGORY='%s'"%(category))
            results=cursor.fetchall()
            products=[]
            for item in results:
                inv_id=int(item[0])
                manufacturer=item[1]
                product_name=item[2]
                lot=item[3]
                products.append([inv_id,manufacturer,product_name,lot])
        cursor.close()
        return render_template('request_spare_store.html',CURRENT_TAB=session["CURRENT_TAB"],cart_items_store=cart_items_store,cart_items_out=cart_items_out,job_id=job_id,products=products,categories=categories)
        
    else:
        flash("No job selected","info")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])


@mgm.route('/add_to_cart_from_store/<job_id>/<inv_id>')
def add_to_cart_from_store(job_id=None,inv_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id and inv_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        inv_id=int(inv_id)
        cursor.execute("SELECT PRODUCT_NAME FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%d"%(inv_id))
        current_product=cursor.fetchall()[0][0]
        cursor.close()
        return render_template("add_to_cart_from_store.html",CURRENT_TAB=session["CURRENT_TAB"],current_product=current_product,inv_id=inv_id,job_id=job_id)
    else:
        flash("No job or product chosen!","info")
        


@mgm.route('/add_to_cart_from_store_return/<job_id>/<inv_id>',methods=['POST'])
def add_to_cart_from_store_return(job_id=None,inv_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id and inv_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        inv_id=int(inv_id)
        units=float(request.form['units'])
        cursor.execute("SELECT UNITS,PID,CP,SP,PRODUCT_NAME FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%d"%(inv_id))
        res=cursor.fetchall()
        existing_units=float(res[0][0])
        pid=int(res[0][1])
        cp=float(res[0][2])
        sp=float(res[0][3])
        product_name=res[0][4]
        date_today=str(datetime.date.today())
        time_now=datetime.datetime.now().strftime("%H:%M")
        if existing_units-units>=0:
            #check if item already in cart
            cursor.execute("SELECT UNITS FROM PART_REQUESTS_STORE WHERE JOB_ID=%d AND INVENTORY_ID=%d"%(job_id,inv_id))
            if len(cursor.fetchall())>0:
                cursor.execute("UPDATE CURRENT_STOCK_TABLE SET UNITS=UNITS-%f WHERE INVENTORY_ID=%d"%(units,inv_id))
                cursor.execute("UPDATE PART_REQUESTS_STORE SET UNITS=UNITS+%f WHERE JOB_ID=%d AND INVENTORY_ID=%d"%(units,job_id,inv_id))
                cmnd="INSERT INTO CONSUMPTION_FROM_STORE (DATE,TIME,INVENTORY_ID,JOB_ID,PID,UNITS_CONSUMED,CP,SP,PRODUCT_NAME) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(cmnd,(date_today,time_now,str(inv_id),str(job_id),str(pid),str(units),str(cp),str(sp),product_name))
            else:
                cursor.execute("UPDATE CURRENT_STOCK_TABLE SET UNITS=UNITS-%f WHERE INVENTORY_ID=%d"%(units,inv_id))
                cmnd="INSERT INTO PART_REQUESTS_STORE (DATE_OF_REQUEST,TIME_OF_REQUEST,JOB_ID,INVENTORY_ID,UNITS,PRODUCT_NAME) VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(cmnd,(date_today,time_now,str(job_id),str(inv_id),str(units),product_name))
                cmnd="INSERT INTO CONSUMPTION_FROM_STORE (DATE,TIME,INVENTORY_ID,JOB_ID,PID,UNITS_CONSUMED,CP,SP,PRODUCT_NAME) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(cmnd,(date_today,time_now,str(inv_id),str(job_id),str(pid),str(units),str(cp),str(sp),product_name))
            mysql.connection.commit()
            flash("Part Successfully added to Cart")
            url="/request_spare_store/"+str(job_id)
            cursor.close()
            return redirect(url)
        else:
            flash("Insufficient stock available for the request!","info")
            url="/request_spare_store/"+str(job_id)
            cursor.close()
            return redirect(url)
    else:
        flash("No job or part selected!","info")
        return redirect('/show_assigned_jobs')

@mgm.route('/return_to_stock/<job_id>/<inv_id>/<units>')
def return_to_stock(job_id=None,inv_id=None, units=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id and inv_id and units:
        cursor = mysql.connection.cursor()
        inv_id=int(inv_id)
        units=float(units)
        job_id=int(job_id)
        cursor.execute("DELETE FROM PART_REQUESTS_STORE WHERE JOB_ID=%d AND INVENTORY_ID=%d AND UNITS=%f"%(job_id,inv_id,units))
        cursor.execute("DELETE FROM CONSUMPTION_FROM_STORE WHERE JOB_ID=%d AND INVENTORY_ID=%d"%(job_id,inv_id))
        cursor.execute("UPDATE CURRENT_STOCK_TABLE SET UNITS=UNITS+%f WHERE INVENTORY_ID=%d"%(units,inv_id))
        mysql.connection.commit()
        flash("Part returned to Stock","info")
        url="/request_spare_store/"+str(job_id)
        cursor.close()
        return redirect(url)
    else:
        flash("No Part or Units selected to return","info")
        url="/request_spare_store/"+str(job_id)
        return redirect(url)
        
        
@mgm.route('/request_spare_out/<job_id>')
def request_spare_out(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        cursor.execute("SELECT INVENTORY_ID,UNITS FROM PART_REQUESTS_STORE WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_store=[]
        for item in results:
            inv_id=int(item[0])
            units=float(item[1])
            cursor.execute("SELECT PRODUCT_NAME,LOT FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%d"%(inv_id))
            resp=cursor.fetchall()
            product_name=resp[0][0]
            lot=resp[0][1]
            cart_items_store.append([inv_id,product_name,lot,units])
        cursor.execute("SELECT RID,PART,UNITS,STATUS FROM PART_REQUESTS_OUT WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_out=[]
        i=0
        for item in results:
            request_id=item[0]
            part=item[1]
            units=int(item[2])
            status=item[3]
            cart_items_out.append([request_id,part,units,status])
        
        cursor.close()
        return render_template('request_spare_out.html',CURRENT_TAB=session["CURRENT_TAB"],cart_items_store=cart_items_store,cart_items_out=cart_items_out,job_id=job_id)
    else:
        flash("No job selected for ordering parts","info")
        return redirect('/show_assigned_jobs')
        
        
@mgm.route('/add_to_cart_from_out/<job_id>',methods=['POST'])
def add_to_cart_from_out(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        part=request.form['part']
        units=float(request.form['units'])
        date_today=str(datetime.date.today())
        time_now=datetime.datetime.now().strftime("%H:%M")
        cmnd="INSERT INTO PART_REQUESTS_OUT (JOB_ID,PART,UNITS,DATE_OF_REQUEST,TIME_OF_REQUEST) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(cmnd,(str(job_id),part,str(units),date_today,time_now))
        mysql.connection.commit()
        flash("Part requested successfully!","info")
        cursor.close()
        url='/request_spare_out/'+str(job_id)
        
        return redirect(url)
    else:
        flash("No job selected for ordering parts","info")
        return redirect('/show_assigned_jobs')

@mgm.route('/delete_part_request_out/<job_id>/<rid>/<part>')
def delete_part_request_out(job_id=None,rid=None,part=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id and rid:
        cursor = mysql.connection.cursor()
        cmnd="DELETE FROM PART_REQUESTS_OUT WHERE JOB_ID=%s AND RID=%s"
        cursor.execute(cmnd,(job_id,rid))
        cmnd="INSERT INTO REMOVED_OUT_REQUESTS (JOB_ID,PART) VALUES(%s,%s)"
        cursor.execute(cmnd,(job_id,part))
        mysql.connection.commit()
        flash("Part request Removed successfully!","info")
        cursor.close()
        url='/request_spare_out/'+str(job_id)
        return redirect(url)
    else:
        flash("No job selected for Removing parts","info")
        return redirect('/show_assigned_jobs')
   
@mgm.route('/view_cart/<job_id>')
def view_cart(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        cursor.execute("SELECT INVENTORY_ID,UNITS FROM PART_REQUESTS_STORE WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_store=[]
        total_amount_store=0
        for item in results:
            inv_id=int(item[0])
            units=float(item[1])
            cursor.execute("SELECT PRODUCT_NAME,LOT,SP FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%d"%(inv_id))
            resp=cursor.fetchall()
            product_name=resp[0][0]
            lot=resp[0][1]
            sp=float(resp[0][2])*units
            total_amount_store+=float(sp)
            cart_items_store.append([inv_id,product_name,lot,units,sp])
        cursor.execute("SELECT RID,PART,UNITS,SELLING_PRICE,STATUS FROM PART_REQUESTS_OUT WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_out=[]
        i=0
        total_amount_out=0
        for item in results:
            request_id=item[0]
            part=item[1]
            units=item[2]
            selling_price=float(item[3])
            status=item[4]
            total_amount_out+=selling_price
            cart_items_out.append([request_id,part,units,selling_price,status])
        
        total_amount=total_amount_out+total_amount_store
        cursor.close()
        return render_template('view_cart.html',CURRENT_TAB=session["CURRENT_TAB"],cart_items_store=cart_items_store,cart_items_out=cart_items_out,job_id=job_id,total_amount_out=total_amount_out,total_amount_store=total_amount_store,total_amount=total_amount)
   
    else:
        flash("No job selected to view Cart","info")
        return redirect('/show_assigned_jobs')
    


def spare_cart_sum(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        cursor.execute("SELECT INVENTORY_ID,UNITS FROM PART_REQUESTS_STORE WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        total_amount_store=0
        for item in results:
            inv_id=int(item[0])
            units=float(item[1])
            cursor.execute("SELECT SP FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%d"%(inv_id))
            resp=cursor.fetchall()
            sp=float(resp[0][0])*units
            total_amount_store+=float(sp)
            
        cursor.execute("SELECT SELLING_PRICE FROM PART_REQUESTS_OUT WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        total_amount_out=0
        for item in results:
            selling_price=float(item[0])
            total_amount_out+=selling_price
        
        total_amount=total_amount_out+total_amount_store
        cursor.close()
        return total_amount
    else:
        return -1



@mgm.route('/show_consumption_store',methods=['POST','GET'])
def show_consumption_store():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    entries=[]
    total_margin=0
    if 'date_start' and 'date_end' in request.form:
        date_start=request.form['date_start']
        date_end=request.form['date_end']
        cursor.execute("SELECT DATE,TIME,PID,INVENTORY_ID,JOB_ID,PRODUCT_NAME,UNITS_CONSUMED,CP,SP FROM CONSUMPTION_FROM_STORE WHERE DATE BETWEEN '%s' AND '%s'"%(date_start,date_end))
        results=cursor.fetchall()
        for row in results:
            date=row[0]
            time=row[1]
            pid=int(row[2])
            inv_id=int(row[3])
            job_id=int(row[4])
            product_name=row[5]
            units=float(row[6])
            cp=float(row[7])
            sp=float(row[8])
            total_cp=cp*units
            total_sp=sp*units
            margin_on_entry=total_sp-total_cp
            total_margin+=margin_on_entry
            entries.append([date,time,inv_id,job_id,product_name,units,cp,sp,margin_on_entry])
        
    cursor.close()
    return render_template('show_consumption_store.html',CURRENT_TAB=session["CURRENT_TAB"],entries=entries,total_margin=total_margin)
    
@mgm.route('/show_unfulfilled_out_requests')
def show_unfulfilled_out_requests():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT JOB_ID FROM PART_REQUESTS_OUT")
    result=cursor.fetchall()
    job_ids=[]
    for row in result:
        job_ids.append(int(row[0]))
    requests=[]
    for job_id in job_ids:
        cursor.execute("SELECT RID,DATE_OF_REQUEST,PART,UNITS FROM PART_REQUESTS_OUT WHERE JOB_ID=%d AND STATUS!='PROCURED'"%(job_id)) 
        single_result=cursor.fetchall()
        cursor.execute("SELECT MODEL,MAKE FROM JOB_CARDS WHERE JOB_ID=%d"%(job_id)) 
        vehicle_dets=cursor.fetchall()
        model=vehicle_dets[0][0]
        make=vehicle_dets[0][1]
        
        table=[]
        for row in single_result:
            sorted_row=[]
            rid=row[0]
            date_of_request=row[1]
            part=row[2]
            units=row[3]
            table.append([job_id,rid,date_of_request,model,make,part,units])
        requests.append(table)
    cursor.close()
    return render_template('/show_unfulfilled_out_requests.html',CURRENT_TAB=session["CURRENT_TAB"],requests=requests)
    
    
@mgm.route('/requests_to_print')
def requests_to_print():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    date_today=str(datetime.date.today())
    time_now=datetime.datetime.now().strftime("%H:%M")    
    title=date_today+time_now
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT JOB_ID FROM PART_REQUESTS_OUT")
    result=cursor.fetchall()
    job_ids=[]
    for row in result:
        job_ids.append(int(row[0]))
    requests=[]
    for job_id in job_ids:
        cursor.execute("SELECT RID,PART,UNITS FROM PART_REQUESTS_OUT WHERE JOB_ID=%d AND STATUS!='PROCURED'"%(job_id)) 
        single_result=cursor.fetchall()
        cursor.execute("SELECT COMPANY,MODEL,VARIANT,MAKE,CHASIS_NUMBER,ENGINE_NUMBER FROM JOB_CARDS WHERE JOB_ID=%d"%(job_id)) 
        vehicle_dets=cursor.fetchall()
        company=vehicle_dets[0][0]
        model=vehicle_dets[0][1]
        variant=vehicle_dets[0][2]
        make=vehicle_dets[0][3]
        chasis_number=vehicle_dets[0][4]
        engine_number=vehicle_dets[0][5]
        table=[]
        for row in single_result:
            sorted_row=[]
            rid=row[0]
            part=row[1]
            units=row[2]
            table.append([job_id,rid,company,model,variant,make,chasis_number,engine_number,part,units])
        requests.append(table)
    cursor.close()
    return render_template('/requests_to_print.html',CURRENT_TAB=session["CURRENT_TAB"],requests=requests,title=title)



@mgm.route('/procured_out_order/<request_id>',methods=['GET','POST'])
def procured_out_order(request_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if request_id:
        cursor = mysql.connection.cursor()
        request_id=int(request_id)
        cp_request='cp_'+str(request_id)
        sp_request='sp_'+str(request_id)
        bought_price=float(request.form[cp_request])
        selling_price=float(request.form[sp_request])
        
        cursor.execute("UPDATE PART_REQUESTS_OUT SET BOUGHT_PRICE=%f,SELLING_PRICE=%f,STATUS='PROCURED' WHERE RID=%d"%(bought_price,selling_price,request_id))
        
        mysql.connection.commit()
        flash("Procurement successfully recorded","info")
        cursor.close()
        return redirect('/show_unfulfilled_out_requests')
        
    else:
        flash("No request selected for marking as procured","info")
        return redirect('/show_unfulfilled_out_requests')
        

@mgm.route('/add_type_of_labour_charge')
def add_type_of_labour_charge():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT TYPE FROM TYPE_OF_LABOUR_CHARGES;")
    results=cursor.fetchall()
    types=[]
    for item in results:
        types.append(item)
    cursor.close()
    return render_template('add_type_of_labour_charge.html',CURRENT_TAB=session["CURRENT_TAB"],types=types)
    
@mgm.route('/add_type_of_labour_charge_return',methods=['POST'])
def add_type_of_labour_charge_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    new_type=request.form['new_type']
    cursor.execute("SELECT TYPE FROM TYPE_OF_LABOUR_CHARGES;")
    results=cursor.fetchall()
    
    types=[]
    for item in results:
        types.append(item)
    if new_type not in types:
        cmnd="INSERT INTO TYPE_OF_LABOUR_CHARGES (TYPE) VALUES (%s);"
        cursor.execute(cmnd,(new_type,))
        mysql.connection.commit()
        flash("Type Added","info")
        cursor.close()
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])

    else:
        flash("Type already exists","info")
        cursor.close()
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
        
        
        
@mgm.route('/add_to_charges_cart/<job_id>')
def add_to_charges_cart(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        job_id=int(job_id)
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT CID,TYPE,AMOUNT,DESCRIPTION FROM CHARGES_CART WHERE JOB_ID=%d;"%job_id)
        results=cursor.fetchall()
        data=[]
        total=0
        for row in results:
            cid=int(row[0])
            charge_type=row[1]
            amount=float(row[2])
            description=row[3]
            total+=amount
            data.append([cid,charge_type,description,amount])
        cursor.execute("SELECT TID,TYPE FROM TYPE_OF_LABOUR_CHARGES")
        results=cursor.fetchall()
        types=[]
        for item in results:
            types.append([item[0],item[1]])
        cursor.close()
        return render_template('add_to_charges_cart.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,total=total,types=types,job_id=job_id)
    else:
        flash("No job selected","info")
        return redirect('/show_assigned_jobs')
        
            
@mgm.route('/add_to_charges_cart_return/<job_id>',methods=["GET","POST"])
def add_to_charges_cart_return(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        job_id=int(job_id)
        tid=int(request.form['type'])
        amount=float(request.form['amount'])
        description=request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT TYPE FROM TYPE_OF_LABOUR_CHARGES WHERE TID=%d"%tid)
        charge_type=cursor.fetchall()[0][0]
        cmnd="INSERT INTO CHARGES_CART (TID,JOB_ID,TYPE,AMOUNT,DESCRIPTION) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(cmnd,(str(tid),str(job_id),charge_type,str(amount),description))
        mysql.connection.commit()
        flash("Charge Added to Cart","info")
        url='/add_to_charges_cart/'+str(job_id)
        cursor.close()
        return redirect(url)
        
    else:
        flash("No job selected","info")
        return redirect('/show_assigned_jobs')
        

@mgm.route('/view_charges_cart/<job_id>')
def view_charges_cart(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        job_id=int(job_id)
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT CID,TYPE,AMOUNT,DESCRIPTION FROM CHARGES_CART WHERE JOB_ID=%d;"%job_id)
        results=cursor.fetchall()
        data=[]
        total=0
        for row in results:
            cid=int(row[0])
            charge_type=row[1]
            amount=float(row[2])
            description=row[3]
            total+=amount
            data.append([cid,charge_type,description,amount])
        cursor.close()
        return render_template('view_charges_cart.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,total=total,job_id=job_id)
    else:
        flash("No job selected","info")
        return redirect('/show_assigned_jobs')



def charge_cart_sum(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        job_id=int(job_id)
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT AMOUNT FROM CHARGES_CART WHERE JOB_ID=%d;"%job_id)
        results=cursor.fetchall()
        total=0
        for row in results:
            amount=float(row[0])
            total+=amount
            
        cursor.close()
        return total
    else:
        return -1

def cart_details(job_id=None):
    if job_id:
        spare_cost=spare_cart_sum(job_id)
        charges=charge_cart_sum(job_id)
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT RID FROM PART_REQUESTS_OUT WHERE JOB_ID=%s",(job_id))
        num_out_requests=cursor.rowcount
        cursor.execute("SELECT INVENTORY_ID FROM PART_REQUESTS_STORE WHERE JOB_ID=%s",(job_id))
        num_store_requests=cursor.rowcount
    return spare_cart_sum,charge_cart_sum,num_out_requests,num_store_requests
    

@mgm.route('/unassign_work/<job_id>')
def unassign_work(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        flash(str(request.url_rule).split('/')[1],"info")
        return redirect('/')
    if job_id:
        spare_cost=spare_cart_sum(job_id)
        charges=charge_cart_sum(job_id)
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT RID FROM PART_REQUESTS_OUT WHERE JOB_ID=%s",(job_id,))
        num_out_requests=cursor.rowcount
        cursor.execute("SELECT INVENTORY_ID FROM PART_REQUESTS_STORE WHERE JOB_ID=%s",(job_id,))
        num_store_requests=cursor.rowcount
        if spare_cost==0 and charges==0 and num_out_requests==0 and num_store_requests==0:
           cmnd="UPDATE JOB_CARDS SET EMPLOYEE_ASSIGNED=0,DATE_ASSIGNED=NULL, TIME_ASSIGNED=NULL, STATUS='UNASSIGNED' WHERE JOB_ID=%s ;"
           cursor.execute(cmnd,(job_id,))
           mysql.connection.commit()
           cursor.close()
           flash("Job Unassigned","info")
           return redirect('/show_assigned_jobs')
        else:
            flash("Empty both remove/return parts and charges from cart before unassigning","info")
            return redirect('/show_assigned_jobs')
    else:
        flash("No job selected","info")
        return redirect('/show_assigned_jobs')
        

@mgm.route('/remove_from_charges_cart/<cid>')
def remove_from_charges_cart(cid=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if cid:
        cid=int(cid)
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT JOB_ID FROM CHARGES_CART WHERE CID=%d"%cid)
        job_id=int(cursor.fetchall()[0][0])
        cursor.execute("DELETE FROM CHARGES_CART WHERE CID=%d;"%cid)
        mysql.connection.commit()
        cursor.close()
        flash("Charge Removed","Info")
        url='/add_to_charges_cart/'+str(job_id)
        return redirect(url)
    else:
        flash("No charge selected for removal","info")
        return redirect('/show_assigned_jobs')


@mgm.route('/finish_work/<job_id>')
def finish_work(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        date_today=str(datetime.date.today())
        time_now=datetime.datetime.now().strftime("%H:%M")
        cursor.close()
        return render_template('finish_work.html',CURRENT_TAB=session["CURRENT_TAB"],date_today=date_today,time_now=time_now,job_id=job_id)
    else:
        flash("No job selected for marking as finished","info")
        return redirect('/show_assigned_jobs')

@mgm.route('/finish_work_return/<job_id>',methods=['GET','POST'])
def finish_work_return(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        finishing_date=request.form['finishing_date']
        finishing_time=request.form['finishing_time']
        finishing_notes=request.form['finishing_notes']
        cursor.execute("UPDATE JOB_CARDS SET DATE_COMPLETION=%s,TIME_COMPLETION=%s,FINISHING_NOTES=%s, STATUS='FINISHED' WHERE JOB_ID=%s",(finishing_date,finishing_time,finishing_notes,str(job_id)))
        mysql.connection.commit()
        cursor.close()
        flash("Job marked as finished","info")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])

    else:
        flash("No job selected for marking as finished","info")
        return redirect('/show_assigned_jobs')
        
@mgm.route('/show_finished_jobs')
def show_finished_jobs():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT JOB_ID,CUSTOMER_NAME,REGISTRATION_NUM,COMPANY,MODEL,JOB_TYPE,EMPLOYEE_ASSIGNED,STATUS FROM JOB_CARDS WHERE STATUS='FINISHED' ORDER BY JOB_ID DESC;")
    mysql.connection.commit()
    result=cursor.fetchall()
    unsorted_headings=cursor.description
    
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0].replace("_"," "))
    for row in result:
        job_id=row[0]
        customer_name=row[1]
        reg_number=row[2]
        company=row[3]
        model=row[4]
        job_type=row[5]
        employee_id=row[6]
        status=row[7]
        cursor.execute("SELECT EMPLOYEE_NAME FROM EMPLOYEE_TABLE WHERE EMPLOYEE_ID=%s",(employee_id,))
        employee_name=cursor.fetchall()[0][0]
        data.append([job_id,customer_name,reg_number,company,model,job_type,employee_name,status])
    cursor.close()
    return render_template('show_finished_jobs.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)


@mgm.route('/unfinish_work/<job_id>',methods=['GET','POST'])
def unfinish_work(job_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        cursor = mysql.connection.cursor()
        job_id=int(job_id)
        cursor.execute("UPDATE JOB_CARDS SET DATE_COMPLETION=NULL,TIME_COMPLETION=NULL, STATUS='ASSIGNED' WHERE JOB_ID=%d"%(job_id))
        mysql.connection.commit()
        cursor.close()
        flash("Job marked as unfinished","info")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])

    else:
        flash("No job selected for marking as unfinished","info")
        return redirect('/show_assigned_jobs')

@mgm.route('/generate_invoice/<job_id>/<option>')
def generate_invoice(job_id=None,option=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if job_id:
        job_id=int(job_id)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT PART,UNITS,SELLING_PRICE FROM PART_REQUESTS_OUT WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_out=[]
        i=0
        total_amount_out=0
        for item in results:
            i=i+1
            part=item[0]
            units=item[1]
            selling_price=float(item[2])
            total_amount_out+=selling_price
            cart_items_out.append([str(i),part,units,selling_price])
        
        #CHECK IF PRODUCT BELONGS TO RESTRICTED CATEGORY(IE CLUBBABLE CATEGORY) WHICH NEEDS TO BE CLUBBED IN INVOICE
        cursor.execute("SELECT CID FROM CLUBBABLE_CATEGORIES")
        results=cursor.fetchall()
        clubbable=[]
        for row in results:
            clubbable.append(row[0])
        
        cursor.execute("SELECT INVENTORY_ID,UNITS FROM PART_REQUESTS_STORE WHERE JOB_ID=%d"%(job_id))
        results=cursor.fetchall()
        cart_items_store=[]
        total_amount_store=0
        i=0
        for item in results:
            i=i+1
            inv_id=int(item[0])
            units=float(item[1])
            cursor.execute("SELECT PID,PRODUCT_NAME,LOT,SP FROM CURRENT_STOCK_TABLE WHERE INVENTORY_ID=%d"%(inv_id))
            resp=cursor.fetchall()
            pid=int(resp[0][0])
            product_name=resp[0][1]
            lot=resp[0][2]
            sp=float(resp[0][3])*units
            
            cursor.execute("SELECT CID FROM PRODUCT_TABLE WHERE PID=%d"%pid)
            cid=int(cursor.fetchall()[0][0])
            
            if cid not in clubbable:
                total_amount_store+=float(sp)
                cart_items_store.append([str(i),product_name,units,sp])
                
                
        cursor.execute("SELECT CID,TYPE,AMOUNT,DESCRIPTION FROM CHARGES_CART WHERE JOB_ID=%d;"%job_id)
        results=cursor.fetchall()
        labour_charge_data=[]
        total_labour_charge=0
        i=0
        for row in results:
            i=i+1
            cid=int(row[0])
            charge_type=row[1]
            amount=float(row[2])
            description=row[3]
            total_labour_charge+=amount
            labour_charge_data.append([str(i),charge_type,description,amount])
        #fetch job details
        cursor.execute("SELECT CUSTOMER_NAME,COMPANY,MODEL,VARIANT,MAKE,INSURANCE,INSURANCE_FILE_NUMBER,REGISTRATION_NUM,CUSTOMER_PHONE_NUM,ADVANCE FROM JOB_CARDS WHERE JOB_ID=%s",(str(job_id),))
        details=cursor.fetchall()
        customer_name=details[0][0]
        company=details[0][1]
        model=details[0][2]
        variant=details[0][3]
        make=details[0][4]
        
        insurance=details[0][5]
        insurance_file_number=details[0][6]
        registration_num=details[0][7]
        
        phone_num=details[0][8]
        advance=float(details[0][9])
        
        #Take previous discounted price if available
        cursor.execute("SELECT DISCOUNTED_PRICE FROM INVOICE_DATA WHERE JOB_ID=%s",(job_id,))
        if cursor.rowcount>0:
            discounted_price=float(cursor.fetchall()[0][0])
        else:
            discounted_price=0

        
        job_details=[job_id,customer_name,company,model,variant,make,insurance,insurance_file_number,registration_num,phone_num,advance]
        cursor.close()
        total_amount=total_amount_out+total_amount_store+total_labour_charge
        return render_template("invoice_temp.html",CURRENT_TAB=session["CURRENT_TAB"],discounted_price=discounted_price,option=option,advance=advance,job_details=job_details,total_amount_out=total_amount_out,total_amount_store=total_amount_store,total_labour_charge=total_labour_charge,cart_items_out=cart_items_out,cart_items_store=cart_items_store,labour_charge_data=labour_charge_data,total_amount=total_amount)
    else:
        flash("No job selected","info")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
        





@mgm.route('/generate_invoice_return/<option>',methods=['POST'])
def generate_invoice_return(option=None):
    cursor=mysql.connection.cursor()
    job_details=request.form.getlist('job_details[]')
    job_id=request.form['job_id']
    customer_name=request.form['customer_name']
    company=request.form['company']
    model=request.form['model']
    variant=request.form['variant']
    make=request.form['make']
    advance=float(request.form['advance'])
        
    insurance=''
    insurance_file_number=''
    is_insured=False
    if request.form['insurance']!="Not Insured":
        insurance=request.form['insurance']
        insurance_file_number=request.form['insurance_file_number']
        is_insured=True
    registration_number=request.form['registration_number']
    phone_number=request.form['phone_number']
    cart_items_store_name=request.form.getlist('cart_items_store_name[]')
    cart_items_store_units=request.form.getlist('cart_items_store_units[]')
    cart_items_store_price=request.form.getlist('cart_items_store_price[]')
    items_from_store=False
    if len(cart_items_store_name)!=0:
        items_from_store=True
    cart_items_out_name=request.form.getlist('cart_items_out_name[]')
    cart_items_out_units=request.form.getlist('cart_items_out_units[]')
    cart_items_out_price=request.form.getlist('cart_items_out_price[]')
    
    items_from_out=False
    if len(cart_items_out_name)!=0:
        items_from_out=True
    
    labour_charge_name=request.form.getlist('labour_charge_name[]')
    labour_charge_description=request.form.getlist('labour_charge_description[]')
    labour_charge_price=request.form.getlist('labour_charge_price[]')
    
    labour_charges=False
    if len(labour_charge_name)!=0:
        labour_charges=True
    
    
    print(labour_charge_name,labour_charge_description,labour_charge_price)
    total_amount_store=request.form['total_amount_store']
    total_amount_out=request.form['total_amount_out']
    total_labour_charge=request.form['total_labour_charge']
    total_amount=request.form['total_amount']
    
    discounted_price=request.form['discounted_price']
    discount=float(total_amount)-float(discounted_price)
    discounted=False
    if discount>0:
        discounted=True
    date_today=str(datetime.date.today())
    
    invoice_note="Note: "+request.form['invoice_note']
    if invoice_note=="Note: ":
        invoice_note=""
    
    advance_paid=False
    if advance>0:
        advance_paid=True
    print(advance)    
    actual_total=float(total_amount_store)+float(total_amount_out)+float(total_labour_charge)
    amount_paid=float(advance)
    amount_due=float(discounted_price)-amount_paid
    print(discounted_price,amount_paid,amount_due)
    #check if invoice for job already exists. add if not. update if yes
    cmnd="SELECT INVOICE_NUMBER FROM INVOICE_DATA WHERE JOB_ID=%s"
    cursor.execute(cmnd,(job_id,))
    result=cursor.fetchall()
    rowcount=cursor.rowcount
    print(option)
    if rowcount==0 and option=="generate":
        cmnd="INSERT INTO INVOICE_DATA (JOB_ID,DATE_OF_INVOICE,TOTAL_AMOUNT,DISCOUNTED_PRICE,AMOUNT_DUE,AMOUNT_PAID) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(cmnd,(job_id,date_today,actual_total,discounted_price,amount_due,amount_paid))
        cmnd="UPDATE JOB_CARDS SET STATUS='INVOICE GENERATED',DISCOUNTED_PRICE=%s  WHERE JOB_ID=%s"
        cursor.execute(cmnd,(discounted_price,job_id))
        mysql.connection.commit()
        cursor.close()
        return render_template('/invoice.html',advance_paid=advance_paid,amount_paid=amount_paid,amount_due=amount_due,items_from_store=items_from_store,items_from_out=items_from_out,labour_charges=labour_charges,discount=discount,invoice_note=invoice_note,total_amount_out=total_amount_out,total_labour_charge=total_labour_charge,total_amount_store=total_amount_store,labour_charge_name=labour_charge_name,labour_charge_description=labour_charge_description,labour_charge_price=labour_charge_price,cart_items_store_name=cart_items_store_name,cart_items_store_units=cart_items_store_units,cart_items_store_price=cart_items_store_price,cart_items_out_name=cart_items_out_name,cart_items_out_units=cart_items_out_units,cart_items_out_price=cart_items_out_price,discounted=discounted,is_insured=is_insured,total_amount=total_amount,discounted_price=discounted_price,customer_name=customer_name,company=company,model=model,insurance=insurance,insurance_file_number=insurance_file_number,registration_number=registration_number,phone_number=phone_number,date_of_generation_of_invoice=date_today)
    elif rowcount!=0 and option=="generate":
        flash("Invoice Generated Already, You can either Update or View it","info")
        cursor.close()
        return redirect('/')
    elif rowcount!=0 and option=="update":
        cmnd="UPDATE INVOICE_DATA SET DATE_OF_INVOICE=%s,TOTAL_AMOUNT=%s,DISCOUNTED_PRICE=%s,AMOUNT_DUE=%s, AMOUNT_PAID=%s WHERE JOB_ID=%s"
        cursor.execute(cmnd,(str(date_today),str(actual_total),str(discounted_price),str(amount_due),str(amount_paid),str(job_id)))
        cmnd="UPDATE JOB_CARDS SET STATUS='INVOICE UPDATED' WHERE JOB_ID=%s"
        cursor.execute(cmnd,(job_id,))
        mysql.connection.commit()
        cursor.close()
        return render_template('/invoice.html',advance_paid=advance_paid,amount_paid=amount_paid,amount_due=amount_due,items_from_store=items_from_store,items_from_out=items_from_out,labour_charges=labour_charges,discount=discount,invoice_note=invoice_note,total_amount_out=total_amount_out,total_labour_charge=total_labour_charge,total_amount_store=total_amount_store,labour_charge_name=labour_charge_name,labour_charge_description=labour_charge_description,labour_charge_price=labour_charge_price,cart_items_store_name=cart_items_store_name,cart_items_store_units=cart_items_store_units,cart_items_store_price=cart_items_store_price,cart_items_out_name=cart_items_out_name,cart_items_out_units=cart_items_out_units,cart_items_out_price=cart_items_out_price,discounted=discounted,is_insured=is_insured,total_amount=total_amount,discounted_price=discounted_price,customer_name=customer_name,company=company,model=model,insurance=insurance,insurance_file_number=insurance_file_number,registration_number=registration_number,phone_number=phone_number,date_of_generation_of_invoice=date_today)
    elif rowcount!=0 and option=="view":
        print("here")
        print(str(date_today),str(actual_total),str(discounted_price),str(amount_due),str(job_id))
        cursor.close()
        return render_template('/invoice.html',advance_paid=advance_paid,amount_paid=amount_paid,amount_due=amount_due,items_from_store=items_from_store,items_from_out=items_from_out,labour_charges=labour_charges,discount=discount,invoice_note=invoice_note,total_amount_out=total_amount_out,total_labour_charge=total_labour_charge,total_amount_store=total_amount_store,labour_charge_name=labour_charge_name,labour_charge_description=labour_charge_description,labour_charge_price=labour_charge_price,cart_items_store_name=cart_items_store_name,cart_items_store_units=cart_items_store_units,cart_items_store_price=cart_items_store_price,cart_items_out_name=cart_items_out_name,cart_items_out_units=cart_items_out_units,cart_items_out_price=cart_items_out_price,discounted=discounted,is_insured=is_insured,total_amount=total_amount,discounted_price=discounted_price,customer_name=customer_name,company=company,model=model,insurance=insurance,insurance_file_number=insurance_file_number,registration_number=registration_number,phone_number=phone_number,date_of_generation_of_invoice=date_today)
    else:
        flash("Wrong option for invoice selected, Try again","info")
        return redirect('/')
        
        


@mgm.route('/show_invoices')
def show_invoices():
    #if not is_allowed(str(request.url_rule).split('/')[1]):
        #return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT JOB_ID,CUSTOMER_NAME,REGISTRATION_NUM,COMPANY,MODEL,STATUS FROM JOB_CARDS WHERE STATUS='INVOICE GENERATED' OR STATUS='INVOICE UPDATED' ORDER BY JOB_ID DESC;")
    mysql.connection.commit()
    result=cursor.fetchall()
    unsorted_headings=cursor.description
    
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0].replace("_"," "))
    for row in result:
        job_id=row[0]
        customer_name=row[1]
        reg_number=row[2]
        company=row[3]
        model=row[4]
        status=row[5]
        
        data.append([job_id,customer_name,reg_number,company,model,status])
    cursor.close()
    return render_template('show_invoices.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)
  


@mgm.route('/add_clubbable_category')
def add_clubbable_category():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT CID,CATEGORY FROM CLUBBABLE_CATEGORIES;")
    resp=cursor.fetchall()
    existing=[]
    for item in resp:
        existing.append([item[0],item[1]])
    
    cursor.execute("SELECT CID,CATEGORY FROM CATEGORIES;")
    resp=cursor.fetchall()
    
    response=[]
    
    for item in resp:
        if item[1] not in existing:
            response.append([item[0],item[1]])
        
    
    cursor.close()
    return render_template('add_clubbable_category.html',CURRENT_TAB=session["CURRENT_TAB"],existing_category_list=response,existing_clubbable=existing)

@mgm.route('/add_clubbable_category_return',methods=['POST','GET'])
def add_clubbable_category_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    category_id=int(request.form['cat_id'])
    cursor.execute("SELECT CATEGORY FROM CATEGORIES WHERE CID=%d;"%category_id)
    category=cursor.fetchall()[0][0]
    cmnd="INSERT INTO CLUBBABLE_CATEGORIES (CID,CATEGORY) VALUES(%s,%s)"
    cursor.execute(cmnd,(str(category_id),category))
    mysql.connection.commit()
    cursor.close()
    flash("Clubbable Category Added","info")
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])

@mgm.route('/remove_clubbable/<club_id>')
def remove_clubbable(club_id=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if club_id:
        cid=int(club_id)
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM CLUBBABLE_CATEGORIES WHERE CID=%d"%cid)
        mysql.connection.commit()
        cursor.close()
        flash("Category removed from clubbables","info")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
    else:
        flash("No Category selected to unclub","info")
        return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
        
@mgm.route('/store')
def store_front():
    session["CURRENT_TAB"]='store'
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])
        
@mgm.route('/back_end')
def store_back():
    session["CURRENT_TAB"]='back_end'
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])



@mgm.route('/garage')
def garage():
    session["CURRENT_TAB"]='garage'
    return render_template('/index.html',CURRENT_TAB=session["CURRENT_TAB"])



@mgm.route('/add_job_role')
def add_job_role():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT GID,NAME,FUNCTIONS,DESCRIPTION FROM FUNCTION_GROUPS;")
    raw_function_groups=cursor.fetchall()
    cursor.execute("SELECT RID,JOB_ROLE,FUNCTION_GROUPS FROM JOB_ROLES;")
    raw_job_roles=cursor.fetchall()
    function_groups=[]
    existing_job_roles=[]
    for row in raw_function_groups:
        gid=row[0]
        name=row[1]
        functions=row[2].replace("?",", ")
        description=row[3]
        function_groups.append([gid,name,functions,description])
    for row in raw_job_roles:
        rid=row[0]
        job_role=row[1]
        groups=row[2].split("?")
       
        descriptions=[]
        for gid in groups:
            if gid!='':
                cursor.execute("SELECT DESCRIPTION FROM FUNCTION_GROUPS WHERE GID=%s",(gid,))
                description=cursor.fetchall()[0][0]
                descriptions.append(description)
        existing_job_roles.append([rid,job_role,descriptions])
    cursor.close()
    return render_template('add_job_role.html',CURRENT_TAB=session["CURRENT_TAB"],existing_job_roles=existing_job_roles,function_groups=function_groups)


@mgm.route('/add_job_role_return',methods = ['POST'])
def add_job_role_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    new_job_role=request.form['new_job_role']
    function_groups=request.form.getlist('function_groups')
    cursor = mysql.connection.cursor()
    final_string=""
    gid_string=""
    for gid in function_groups:
        gid_string+=gid+"?"
    
    cmnd='INSERT INTO JOB_ROLES (JOB_ROLE,FUNCTION_GROUPS) VALUES(%s,%s);'
    cursor.execute(cmnd,(new_job_role,gid_string))
    mysql.connection.commit()
    cursor.close()
    flash("Job role added Successfully","info")
    return render_template('index.html',CURRENT_TAB=session["CURRENT_TAB"])

@mgm.route('/edit_job_role/<rid>')
def edit_job_role(rid=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if rid:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT GID,NAME,FUNCTIONS,DESCRIPTION FROM FUNCTION_GROUPS;")
        raw_function_groups=cursor.fetchall()
        function_groups=[]
        for row in raw_function_groups:
            gid=row[0]
            name=row[1]
            functions=row[2].replace("?",", ")
            description=row[3]
            function_groups.append([gid,name,functions,description])
        cursor.execute("SELECT JOB_ROLE,FUNCTION_GROUPS FROM JOB_ROLES WHERE RID=%s;",(rid,))
        raw_job_roles=cursor.fetchall()
        job_role=raw_job_roles[0][0]
        existing_function_groups=raw_job_roles[0][1].split("?")
        
    return render_template("edit_job_role.html",existing_function_groups=existing_function_groups,function_groups=function_groups,CURRENT_TAB=session["CURRENT_TAB"],rid=rid,job_role=job_role)
    
@mgm.route('/edit_job_role_return/<rid>',methods = ['POST'])
def edit_job_role_return(rid=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    if rid:
        new_job_role=request.form['new_job_role']
        function_groups=request.form.getlist('function_groups')
        cursor = mysql.connection.cursor()
        final_string=""
        gid_string=""
        for gid in function_groups:
            gid_string+=gid+"?"
        
        cmnd='UPDATE JOB_ROLES SET JOB_ROLE=%s,FUNCTION_GROUPS=%s WHERE RID=%s;'
        cursor.execute(cmnd,(new_job_role,gid_string,rid))
        mysql.connection.commit()
        cursor.close()
        flash("Job role edited Successfully","info")
        return render_template('index.html',CURRENT_TAB=session["CURRENT_TAB"])
            
        
        

@mgm.route('/show_function_groups')
def show_function_groups(test=None):
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM FUNCTION_GROUPS;")
    result=cursor.fetchall()
    unsorted_headings=cursor.description
    
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0].replace("_"," "))
    for row in result:
        raw_row=[]
        for item in row:
            raw_row.append(item)
        data.append(raw_row)
    cursor.close()
    return render_template('show_function_groups.html',CURRENT_TAB=session["CURRENT_TAB"],data=data,headings=headings)

@mgm.route('/login')
def login():
    user='NA'
    if session.get('LOGGED_IN'):
        user=session.get('EMPLOYEE_NAME')
    return render_template("login.html",CURRENT_TAB=session["CURRENT_TAB"],user=user)

@mgm.route('/login_return',methods=['POST'])
def login_return():
    username=request.form['username']
    password=request.form['password']
    if username and password:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT PASSWORD FROM EMPLOYEE_TABLE WHERE USERNAME=%s",(username,))
        if cursor.rowcount>0:
            actual_password_hash=cursor.fetchall()[0][0]
            cursor.execute("SELECT PASSWORD(%s)",(password,))
            entered_password_hash=cursor.fetchall()[0][0]
            if entered_password_hash==actual_password_hash:
                cursor.execute("SELECT JOB_ROLE,EMPLOYEE_NAME FROM EMPLOYEE_TABLE WHERE USERNAME=%s",(username,))
                resp=cursor.fetchall()
                job_role=resp[0][0]
                employee_name=resp[0][1]
                
                cursor.execute("SELECT FUNCTION_GROUPS FROM JOB_ROLES WHERE RID=%s",(job_role,))
                fngrps=cursor.fetchall()[0][0].split("?")
                allowed_string=""
                for gid in fngrps:
                    if gid!='':
                        cursor.execute("SELECT FUNCTIONS FROM FUNCTION_GROUPS WHERE GID=%s",(gid,))
                        allowed_string+=cursor.fetchall()[0][0]+"?"
                allowed_functions=allowed_string.split("?")
                cursor.close()
                session['LOGGED_IN']=True
                session['USERNAME']=username
                session['EMPLOYEE_NAME']=employee_name
                session['JOB_ROLE']=job_role
                session['ALLOWED_FUNCTIONS']=allowed_functions
                flash("Welcome "+session.get('EMPLOYEE_NAME'),"info")
                return redirect('/')
            else:
                cursor.close()
                flash("Enter Correct Username and Password","info")
                return redirect("/login")
            
        else:
            cursor.close()
            flash("Enter correct Username and Password","info")
            return redirect("/login")
            
    else:
        flash("Enter Correct Username and Password","info")
        return redirect("/login")
    
@mgm.route('/logout')
def logout():
    if session.get('LOGGED_IN') is not None:
        session.pop('LOGGED_IN')
        session.pop('USERNAME')
        session.pop('ALLOWED_FUNCTIONS')
        session.pop('JOB_ROLE')
    flash("Logged Out","info")
    return redirect('/login')
    


def get_functions_list():
    fns=[]
    with open('main.py','r') as file:
        prev=""
        for line in file:
            for word in line.split():
                if prev=="def":
                    fnname=""
                    for letter in word:
                        if letter=="(":
                            break
                        else:
                            fnname+=letter
                    fns.append(fnname)
                prev=word
    return fns

@mgm.route('/add_function_group')
def add_function_group():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    functions_list=get_functions_list()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM FUNCTION_GROUPS;")
    result=cursor.fetchall()
    unsorted_headings=cursor.description
    
    headings=[]
    data=[]
    for head in unsorted_headings:
        headings.append(head[0].replace("_"," "))
    for row in result:
        raw_row=[]
        for item in row:
            raw_row.append(item)
        data.append(raw_row)
    cursor.close()
    
    return render_template('add_function_group.html',functions_list=functions_list,headings=headings,data=data,CURRENT_TAB=session["CURRENT_TAB"])
            
@mgm.route('/add_function_group_return',methods=['POST'])
def add_function_group_return():
    if not is_allowed(str(request.url_rule).split('/')[1]):
        return redirect('/')
    name=request.form['function_group_name']
    description=request.form['description']
    functions=request.form.getlist('functions')
    final_string=""
    for fn in functions:
        final_string+=fn+"?"
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO FUNCTION_GROUPS(NAME,FUNCTIONS,DESCRIPTION) VALUES(%s,%s,%s)",(name,final_string,description))
    mysql.connection.commit()
    flash("Function Group Added")
    return redirect('/show_function_groups')

def is_allowed(current_fn):
    if not session.get('LOGGED_IN'):
        flash("Login First","info")
        return False
    elif session.get('ALLOWED_FUNCTIONS') is None:
        flash("Login First","info")
        return False
    elif current_fn not in session.get('ALLOWED_FUNCTIONS'):
        
        flash("You are not allowed to use that function","info")
        return False
    else:
        return True
 
if __name__ == '__main__':
    mgm.run(debug=True, host='0.0.0.0')

idle
