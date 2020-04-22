import flask
import pickle
import pandas as pd
import numpy as np

#load models at top of app to load into memory only one time
with open('model/xgb_cv_compact.pkl', 'rb') as f:
    clf = pickle.load(f)
          
with open('model/knn_regression.pkl', 'rb') as f:
    knn = pickle.load(f)
    
#load APR table
df_fico_apr = pd.read_csv('model/grade_to_apr.csv')


df_macro_mean  = pd.read_csv('model/df_macro_mean.csv', index_col=0, dtype=np.float64)

df_macro_std = pd.read_csv('model/df_macro_std.csv', index_col=0, dtype=np.float64)

def emp_title_to_dict(e_title):
    #force make string if not and make lower
    title_lower = str(e_title).lower()
    
    #list of employment types to consider
    emp_list = ['e_manager', 'e_educ', 'e_self',
                'e_health', 'e_exec', 'e_driver',
                'e_law', 'e_admin', 'e_fin', 'e_other']
    
    #instantiate title dict
    title_dict = dict(zip(emp_list, len(emp_list)*[0]))
    
    #check and fill out dict
    if any(job in title_lower for job in ['manag', 'superv']):
        title_dict['e_manager'] = 1
        
    elif 'teacher' in title_lower:
        title_dict['e_educ'] = 1

    elif 'owner' in title_lower:
        title_dict['e_self'] = 1
    
    elif any(job in title_lower for job in ['rn', 'registered nurse', 'nurse',
                                          'doctor', 'pharm', 'medic']):
        title_dict['e_health'] = 1
    
    elif any(job in title_lower for job in ['vice president', 'president', 'director',
                                          'exec', 'chief']):
        title_dict['e_exec'] = 1
        
    elif any(job in title_lower for job in ['driver', 'trucker']):
        title_dict['e_driver'] = 1   
    
    elif any(job in title_lower for job in ['lawyer', 'legal', 'judg']):
        title_dict['e_law'] = 1    
    
    elif 'admin' in title_lower:
        title_dict['e_admin'] = 1    
    
    elif any(job in title_lower for job in ['analyst', 'financ', 'sales']):
        title_dict['e_fin'] = 1
    else:
        title_dict['e_other'] = 1
    
    return title_dict



def purp_to_int(title):

    
    #force make string if not and make lower
    title_lower = str(title).lower()
    
    #list of employment types to consider
    title_list = ['purp_car', 'purp_credit_card', 'purp_debt_consolidation',
                  'purp_educational', 'purp_home_improvement',
                  'purp_house', 'purp_major_purchase', 'purp_medical',
                  'purp_moving', 'purp_other', 'purp_renewable_energy',
                  'purp_small_business', 'purp_vacation', 'purp_wedding']
    
    #instantiate title dict
    title_dict = dict(zip(title_list,
                          len(title_list)*[0]))
    #check if any shared items
    for key in title_dict:
        if bool(set(title_lower.split()) & set(key.split('_'))):
            title_dict[key] = 1
    
    return title_dict

home_to_int = {'MORTGAGE': 4,
               'RENT': 3,
               'OWN': 5,         
               'ANY': 2,            
               'OTHER': 1,          
               'NONE':0 }



app = flask.Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def main():
    
    if flask.request.method == 'GET':
        return (flask.render_template('main.html'))
    
    if flask.request.method =='POST':
        
        #get input
        
        #ask for first 2 digits of zip code as integer
        code = int(flask.request.form['code'])
        
        #fico score as integer
        fico = int(flask.request.form['fico'])
        #loan amount as integer
        loan_amnt = float(flask.request.form['loan_amnt'])
        #term as integer: 36 or 60
        term = int(flask.request.form['term'])
        #debt to income as float
        dti = float(flask.request.form['dti'])
        #home ownership as string
        home_ownership = flask.request.form['home_ownership']
        #number or mortgage accounts as integer
        mort_acc = int(flask.request.form['mort_acc'])
        #annual income as float
        annual_inc = float(flask.request.form['annual_inc'])
        #number of open accounts as integer
        open_acc = int(flask.request.form['open_acc'])
        #verification status as 0, 1, 2
        verification_status = int(flask.request.form['verification_status'])
        #revolving balance as float
        revol_bal = float(flask.request.form['revol_bal'])
        #revolving utilization as float
        revol_util = float(flask.request.form['revol_util'])
        # Number of derogatory public records
        pub_rec = int(flask.request.form['pub_rec'])
        #number of public recorded bankruptcies as integer
        pub_rec_bankruptcies = int(flask.request.form['pub_rec_bankruptcies'])
        #employment length as float
        emp_length = float(flask.request.form['emp_length'])
        #0 if solo and 1 if together
        application_type = int(flask.request.form['application_type'])
        #employment title as string
        emp_title = flask.request.form['emp_title']
        #purpose as string
        purpose = flask.request.form['purpose']
        #The total number of credit lines currently in the borrower's credit file
        total_acc = int(flask.request.form['total_acc'])
        #time since first credit line in months
        time_delta = float(flask.request.form['time_delta'])
        
        
        #calculate grade from FICO
        sub_grade = knn.predict(np.reshape([fico], (1,-1)))[0]
        
        #calculate grade
        grade = round(sub_grade/5) + 1
        
        #get purpose of loan
        title_dict = emp_title_to_dict(emp_title)
        
        #get purpose dict
        purp_dict = purp_to_int(purpose)
        
        #get interest rate
        apr_row = df_fico_apr[df_fico_apr['grade_num']==sub_grade]
        
        if term==36:
            int_rate = apr_row['36_mo'].values[0]
            installment = int(loan_amnt/36)
            term = 1
            
        else:
            int_rate = apr_row['60_mo'].values[0]
            installment = int(loan_amnt/60)
            term = 2
            
            
            
            
        #create temporary dataframe for prediction
        title_df = pd.DataFrame({k: [v] for k, v in title_dict.items()})
        purp_df = pd.DataFrame({k: [v] for k, v in purp_dict.items()})
        temp =pd.concat([title_df, purp_df], axis=1)

        #temp['fico'] = fico
        temp['loan_amnt'] = loan_amnt
        temp['term'] = term
        temp['dti'] = dti
        temp['home_ownership'] = home_to_int[home_ownership.upper()]
        temp['mort_acc'] = mort_acc
        temp['annual_inc'] = annual_inc
        temp['open_acc'] = open_acc
        temp['verification_status'] = verification_status
        temp['revol_bal'] = revol_bal
        temp['revol_util'] = revol_util
        temp['pub_rec'] = pub_rec
        temp['emp_length'] = emp_length
        temp['application_type'] = application_type
        temp['int_rate'] = int_rate
        temp['installment'] = installment
        temp['grade'] = grade
        temp['sub_grade'] = sub_grade
        temp['time_delta'] = time_delta * 30 * 12 #years to days
        temp['pub_rec_bankruptcies'] = pub_rec_bankruptcies
        temp['total_acc'] = total_acc

        
        #rearrange
        temp = temp[['pub_rec', 'grade', 'purp_renewable_energy', 'revol_bal', 'open_acc',
       'mort_acc', 'purp_credit_card', 'purp_car', 'e_exec',
       'verification_status', 'purp_other', 'e_other', 'home_ownership',
       'e_educ', 'emp_length', 'e_driver', 'revol_util',
       'purp_moving', 'loan_amnt', 'time_delta', 'e_law', 'e_health', 'e_fin',
       'purp_small_business', 'sub_grade', 'application_type', 'dti',
       'e_manager', 'purp_major_purchase', 'pub_rec_bankruptcies',
       'purp_house', 'term', 'installment', 'total_acc', 'e_admin',
       'purp_medical', 'purp_vacation', 'e_self', 'purp_debt_consolidation',
       'int_rate', 'annual_inc', 'purp_home_improvement']]


        #create original output dict
        output_dict= dict()
        output_dict['Annual Income'] = annual_inc
        output_dict['Self Reported FICO'] = fico
        output_dict['Interest Rate'] = int_rate
        output_dict['Installment']=installment
        output_dict['Sub Grade']=sub_grade
        output_dict['Loan Amount']=loan_amnt
        
        #create deep copy 
        scale = temp.copy()

        for feat in df_macro_mean.columns:
            scale[feat] = (scale[feat] - df_macro_mean.loc[code,feat]) / df_macro_std.loc[code,feat]
            
        #make prediction
        pred = clf.predict(scale.values)[0]
        
        if dti>43:
            res = 'Debt to income too high!'
        elif loan_amnt/annual_inc >=0.43:
            res= 'Debt to income too high!'
        elif revol_util>=90:
            res = 'Amount of credit used up too high!'
            
        elif pred ==1:
            res = 'Congratulations! Approved!'
        else:
            res = 'Loan Denied'
            
        
        
        #render form again and add prediction
        return flask.render_template('main.html',
                                     original_input=output_dict,
                                     result=res,
                                     )
    
if __name__ == '__main__':
    app.run()
    
    
    
    
    
    
    
    