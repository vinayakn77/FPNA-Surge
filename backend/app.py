from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

app = Flask(__name__)
CORS(app)

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    # Save the uploaded file to the specified folder
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
    
    return 'File uploaded successfully'

def calculation_logic(updated_data, post):
    # file_path = 'C:\\Users\\Manish\\Downloads\\SurgeDataLab\\Simulation of FPA Model\\vinayak_code\\Surge-FPA-Simulation\\backend\\uploads\\FPA Model Input File.csv'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "FPA Model Input File.csv")
    # './uploads/FPA Model Input File.csv'
    model1 = pd.read_csv(file_path, index_col='Driver Model') #model1 is dataframe
    m1 = model1.head(25) #m1 is dataframe
    print('\n\n\nreading data success\n\n')

    for i in range(1,13):
        month = 'Month ' + str(i)
        m1[month] = m1[month].str.replace(",","").str.replace("(","-").str.replace(")","")     
        m1[month] = m1[month].astype(float)


    m1.loc['Days in Month'] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m1.loc['Days in Year'] = [365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365]
    m1.loc['Balcon CC Sales'] = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    m1.loc['Interest Margin Percentage'] = m1.loc[['Customer Interest Percentage', 'MDR Percentage', 'Funding Cost Percentage']].sum()
    m1.loc['Interchange'] = 0.0175 * m1.loc['External Sales']

    new_row = []
    for i in range(1,13):
        month = 'Month ' + str(i)
        total = m1.loc['Internal Sales', month] + m1.loc['External Sales', month] + m1.loc['Balcon CC Sales', month]
        new_row.append(total)
    m1.loc['Total Sales'] = new_row

    new_row_eop = []
    for i in range(1,13):
        month = 'Month ' + str(i)
        month_next = 'Month ' + str(i+1)
        eop = m1.loc['BOP Balance', month] + m1.loc['Total Sales', month] - m1.loc['Payments', month] + m1.loc['Other Fees', month]
        new_row_eop.append(eop)
        if i+1<13:
            m1.loc['BOP Balance', month_next] = eop
    m1.loc['EOP Balance'] = new_row_eop

    m1.loc['Internal Sales Derived'] = m1.loc['Internal Sales']

    new_row_avg_balance = []
    new_row_payment_rate = []
    new_row_sales_turn = []
    new_row_floating_apr = []
    new_row_fixed_apr = []
    new_row_promo_apr = []
    new_row_total_avg_balance = []
    new_row_tabr = []
    new_row_transactors_per = []
    new_row_transactor = []
    new_row_eop_accounts = []
    new_row_attrition_rate = []
    new_row_active_rate = []
    new_row_balance_per_active = []
    new_row_sales_per_active = []
    new_row_credit_penetration_rate = []
    new_row_average_ticket = []

    for i in range(1, 13):
        month = 'Month ' + str(i)
        avg = m1.loc[['BOP Balance','EOP Balance'], month].mean()
        new_row_avg_balance.append(avg)
        
        if m1.loc['BOP Balance', month]==0:
            pr = 0
        else:
            pr = m1.loc['Payments', month]/m1.loc['BOP Balance', month]
        new_row_payment_rate.append(pr)
        
        st  = 12 * m1.loc['Total Sales', month]/avg
        new_row_sales_turn.append(st)
        
        fapr = m1.loc['Floating APR Rate', month]*avg
        new_row_floating_apr.append(fapr)
        
        fixed_apr = m1.loc['Fixed APR Rate', month] * avg
        new_row_fixed_apr.append(fixed_apr)
        
        promo_apr = m1.loc['Promo APR Rate', month] * avg
        new_row_promo_apr.append(promo_apr)
        
        total_avg_balance = avg
        new_row_total_avg_balance.append(total_avg_balance)
        
        tabr = 0
        if total_avg_balance!=0:
            tabr = total_avg_balance/total_avg_balance
        new_row_tabr.append(tabr)
        
        transactors_per = tabr-(m1.loc['Floating APR Rate', month] + m1.loc['Fixed APR Rate', month] + m1.loc['Promo APR Rate', month] )
        new_row_transactors_per.append(transactors_per)
        
    #     transactors = transactors_per * m1.loc['Avg Balance', month]
        transactors = transactors_per * avg
        new_row_transactor.append(transactors)
        
        eop_accounts = m1.loc['BOP Accounts', month] + m1.loc['New Accounts', month] - m1.loc['Closed Accounts', month]
        new_row_eop_accounts.append(eop_accounts)
        if i<12:
            m1.loc['BOP Accounts', 'Month '+str(i+1)] = eop_accounts 
        
        attrition_rate = m1.loc['Closed Accounts', month]/m1.loc['BOP Accounts', month]
        new_row_attrition_rate.append(attrition_rate)
        
        active_rate = 0
        if eop_accounts!=0:
            active_rate = m1.loc['Active Accounts', month]/eop_accounts
        new_row_active_rate.append(active_rate)
        
        balance_per_active = avg/m1.loc['Active Accounts', month]
        new_row_balance_per_active.append(balance_per_active)
        
        sales_per_active = m1.loc['Total Sales', month] / m1.loc['Active Accounts', month]
        new_row_sales_per_active.append(sales_per_active)
        
        credit_penetration_rate = m1.loc['Internal Sales Derived', month]/m1.loc['Merchant Sales', month]
        new_row_credit_penetration_rate.append(credit_penetration_rate)
        
        average_ticket = m1.loc['Total Sales',month]/m1.loc['Transactions', month]
        new_row_average_ticket.append(average_ticket)
        
        

    m1.loc['Avg Balance'] = new_row_avg_balance
    m1.loc['Payment Rate'] = new_row_payment_rate
    m1.loc['Sales Turn'] = new_row_sales_turn
    m1.loc['Floating APR'] = new_row_floating_apr
    m1.loc['Fixed APR'] = new_row_fixed_apr
    m1.loc['Promo APR'] = new_row_promo_apr
    m1.loc['Total Average Balance'] = new_row_total_avg_balance
    m1.loc['Total Average Balance Percentage'] = new_row_tabr
    m1.loc['Transactors Percentage'] = new_row_transactors_per
    m1.loc['Transactors'] = new_row_transactor
    m1.loc['EOP Accounts'] = new_row_eop_accounts
    m1.loc['Attrition Rate'] = new_row_attrition_rate
    m1.loc['Active Rate'] = new_row_active_rate
    m1.loc['Balance Per Active'] = new_row_balance_per_active
    m1.loc['Sales Per Active'] = new_row_sales_per_active
    m1.loc['Credit Penetration Rate'] = new_row_credit_penetration_rate
    m1.loc['Average Ticket'] = new_row_average_ticket

    m1.loc['Customer Interest'] = m1.loc['Customer Interest Percentage']*m1.loc['Avg Balance']*m1.loc['Days in Month']/m1.loc['Days in Year']

    m1.loc['MDR'] = m1.loc['MDR Percentage'] * m1.loc['Avg Balance']*m1.loc['Days in Month']/m1.loc['Days in Year']

    m1.loc['Funding Cost'] = m1.loc['Funding Cost Percentage']* m1.loc['Avg Balance']*m1.loc['Days in Month']/m1.loc['Days in Year']

    m1.loc['Interest Margin'] = m1.loc['Interest Margin Percentage'] * m1.loc['Avg Balance']*m1.loc['Days in Month']/m1.loc['Days in Year']

    m1.loc['CVP'] = m1.loc['CVP Percentage'] * m1.loc['Avg Balance']*m1.loc['Days in Month']/m1.loc['Days in Year']

    m1.loc['Total Revenue'] = m1.loc[['Interest Margin','CVP','Interchange']].sum()

    m1.loc['NCL'] = m1.loc['NCL Percentage'] * m1.loc['Avg Balance']*m1.loc['Days in Month']/m1.loc['Days in Year']

    m1.loc['Net Credit Margin'] = m1.loc['Total Revenue'] - m1.loc['NCL']

    m1.loc['Total Revenue Percentage'] = m1.loc[['Interest Margin Percentage', 'CVP Percentage', 'Interchange Percentage']].sum()

    new_row_front_office_expenses = []
    new_row_back_office_expesnes = []
    for i in range(1, 13):
        month = 'Month ' + str(i)
        foe = m1.loc['Front Office Expenses Percentage', month] * m1.loc['Avg Balance','Month 1'] * m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        new_row_front_office_expenses.append(foe)
        
        boe = m1.loc['Back Office Expenses Percentage', month] * m1.loc['Avg Balance', 'Month 1']* m1.loc['Days in Month', month]/ m1.loc['Days in Year', month]
        new_row_back_office_expesnes.append(boe)
        
    m1.loc['Front Office Expenses'] = new_row_front_office_expenses
    m1.loc['Back Office Expenses'] = new_row_back_office_expesnes
        
    m1.loc['Total Expenses'] = m1.loc[['Front Office Expenses', 'Back Office Expenses']].sum() 
    m1.loc['Operating Income'] = m1.loc['Net Credit Margin'] - m1.loc['Total Expenses']
    m1.loc['Net Credit Margin Percentage'] = m1.loc['Total Revenue Percentage'] - m1.loc['NCL Percentage']
    m1.loc['Total Expenses Percentage'] = m1.loc[['Front Office Expenses Percentage','Back Office Expenses Percentage']].sum()
    m1.loc['Operating Income Percentage'] = m1.loc['Net Credit Margin Percentage'] - m1.loc['Total Expenses Percentage']
    # I 3
    # external_sales_summary_yn = [0.000, 0.1000, 0.02000]
    external_sales_summary_yn = [0.000, 0.0000, 0.0000]         
    # I 5
    payment_rate_summary_yn = [0.000, 0.000, 0.00]          
    # I 9
    merchant_sales_summary_yn = [0, 0, 0.0]           
    # I 10
    credit_penetration_summary_yn = [0, 0, 0]    
    # I 11
    transaction_k_summary_yn = [0.0, 0.0, 0.0]           
    # I 19
    applications_summary_yn = [0.0, 0.0, 0.0]
    # I 20
    approval_rate_summary_yn = [0.000, 0.00, 0.00]
    # I 22
    active_rate_summary_yn = [0.000, 0.00, 0.00] 
    # I 25
    floating_apr_summary_yn = [0.000, 0.00, 0.00]
    # I 26
    fixed_apr_summary_yn = [0.000, 0.00, 0.0]
    # I 27
    promo_apr_summary_yn = [0.000, 0.00, 0.00]

    zero_count = 33
    if post:
        for i in range(3):
            if updated_data[0]['values'][i]!=0 or updated_data[1]['values'][i]!=0 or updated_data[2]['values'][i]!=0 or updated_data[3]['values'][i]!=0 or updated_data[4]['values'][i]!=0 or updated_data[5]['values'][i]!=0:
                zero_count -=1
            if updated_data[6]['values'][i]!=0 or updated_data[7]['values'][i]!=0 or updated_data[8]['values'][i]!=0 or updated_data[9]['values'][i]!=0 or updated_data[10]['values'][i]!=0:
                zero_count -=1    

            external_sales_summary_yn[i] = updated_data[0]['values'][i]
            payment_rate_summary_yn[i] = updated_data[1]['values'][i]
            merchant_sales_summary_yn[i] = updated_data[2]['values'][i]      
            credit_penetration_summary_yn[i] =updated_data[3]['values'][i]
            transaction_k_summary_yn[i] = updated_data[4]['values'][i]
            applications_summary_yn[i] = updated_data[5]['values'][i]
            approval_rate_summary_yn[i] =updated_data[6]['values'][i]
            active_rate_summary_yn[i] = updated_data[7]['values'][i]
            floating_apr_summary_yn[i] = updated_data[8]['values'][i]
            fixed_apr_summary_yn[i] = updated_data[9]['values'][i]
            promo_apr_summary_yn[i] = updated_data[10]['values'][i]

    print("\n\n\nwelcome manish you are outside of post!!!!\n\n") 
    print(external_sales_summary_yn)
    print(payment_rate_summary_yn)
    print(merchant_sales_summary_yn)
    print(credit_penetration_summary_yn)
    print(transaction_k_summary_yn)
    print(applications_summary_yn)
    print(approval_rate_summary_yn)
    print(active_rate_summary_yn)
    print(floating_apr_summary_yn)
    print(fixed_apr_summary_yn)
    print(promo_apr_summary_yn)
    print('\n\n')  

    for i in range(13, 49):
        month = 'Month '+ str(i)
        prev_month = 'Month ' + str(i-1)
        prev_yr_month = 'Month ' + str(i-12)
    #     print(prev_yr_month)
        m1.loc['BOP Balance', month] = m1.loc['EOP Balance', prev_month]

        
        year =  ((i-1)//12) - 1
        
        m1.loc['Merchant Sales', month] = m1.loc['Merchant Sales', prev_yr_month]*(1+merchant_sales_summary_yn[year])
        m1.loc['Credit Penetration Rate', month] = m1.loc['Credit Penetration Rate', prev_yr_month] + credit_penetration_summary_yn[year]/10000
        m1.loc['Internal Sales Derived', month] = m1.loc['Merchant Sales', month] * m1.loc['Credit Penetration Rate', month]
        m1.loc['Internal Sales', month] = m1.loc['Internal Sales Derived',month]
        m1.loc['External Sales', month] = m1.loc['External Sales', prev_yr_month]*(1+external_sales_summary_yn[year])
        m1.loc['Balcon CC Sales', month] = 0
        m1.loc['Total Sales', month] = m1.loc[['Internal Sales','External Sales', "Balcon CC Sales"],month].sum()
        m1.loc['Payment Rate', month] = m1.loc['Payment Rate', prev_yr_month] + payment_rate_summary_yn[year] / 10000
        m1.loc['Payments', month] =  m1.loc['Payment Rate', month] * m1.loc['BOP Balance', month]
        m1.loc['Other Fees', month] = m1.loc['Other Fees', prev_yr_month] 
        m1.loc['EOP Balance', month] = m1.loc['BOP Balance', month] + m1.loc['Total Sales', month] - m1.loc['Payments', month] + m1.loc['Other Fees', month]
        m1.loc['Avg Balance', month] = m1.loc[['BOP Balance', 'EOP Balance'],month].mean()
        m1.loc['Sales Turn', month] = 12*m1.loc['Total Sales', month]/m1.loc['Avg Balance', month]
        m1.loc['Floating APR Rate', month] = m1.loc['Floating APR Rate', prev_yr_month] +  floating_apr_summary_yn[year]/10000
        m1.loc['Floating APR', month] = m1.loc['Floating APR Rate', month] * m1.loc['Avg Balance', month]
        
        m1.loc['Fixed APR Rate', month] = m1.loc['Fixed APR Rate', prev_yr_month] +  fixed_apr_summary_yn[year]/10000
        m1.loc['Fixed APR', month] = m1.loc['Fixed APR Rate', month] * m1.loc['Avg Balance', month]
        
        m1.loc['Promo APR Rate', month] = m1.loc['Promo APR Rate', prev_yr_month] +  promo_apr_summary_yn[year]/10000
        m1.loc['Promo APR', month] = m1.loc['Promo APR Rate', month] * m1.loc['Avg Balance', month]
        
        m1.loc['Total Average Balance Percentage', month] = 1
        m1.loc['Transactors Percentage', month] = m1.loc['Total Average Balance Percentage', month] - m1.loc[['Floating APR Rate', 'Fixed APR Rate', "Promo APR Rate"], month].sum()
        m1.loc['Transactors', month] = m1.loc['Transactors Percentage', month] * m1.loc['Avg Balance', month]
        m1.loc['Total Average Balance', month] = m1.loc['Avg Balance', month]
        
        m1.loc['BOP Accounts', month] = m1.loc['EOP Accounts', prev_month]
        m1.loc['Applications', month] = m1.loc['Applications', prev_yr_month] *(1+applications_summary_yn[year])
        m1.loc['Approval Rate', month] = m1.loc['Approval Rate', prev_yr_month] + approval_rate_summary_yn[year]/10000
        m1.loc['New Accounts', month] = m1.loc['Applications', month] *  m1.loc['Approval Rate', month]
        m1.loc['Attrition Rate', month] = m1.loc['Attrition Rate', prev_yr_month]
        m1.loc['Closed Accounts', month] = m1.loc['Attrition Rate', month] * m1.loc['BOP Accounts', month]
        m1.loc['EOP Accounts', month] = m1.loc['BOP Accounts', month] + m1.loc['New Accounts', month] - m1.loc['Closed Accounts', month]
        
        m1.loc['Active Rate', month] = m1.loc['Active Rate', prev_yr_month] + active_rate_summary_yn[year]/10000
        m1.loc['Active Accounts', month] = m1.loc['EOP Accounts', month]*m1.loc['Active Rate', month]
        
        m1.loc['Balance Per Active', month] = m1.loc['Avg Balance', month]/m1.loc['Active Accounts', month]
        m1.loc['Sales Per Active', month] = m1.loc['Total Sales', month]/m1.loc['Active Accounts', month]
        m1.loc['Transactions', month] = m1.loc['Transactions',prev_yr_month]*(1+transaction_k_summary_yn[year])
        
        m1.loc['Average Ticket', month] = m1.loc['Total Sales', month]/ m1.loc['Transactions', month]
        m1.loc['Days in Month', month] = m1.loc['Days in Month', prev_yr_month]
        m1.loc['Days in Year', month] = m1.loc['Days in Year', prev_yr_month]
        
        m1.loc['Customer Interest Percentage', month] = m1.loc['Customer Interest Percentage', prev_yr_month]
        m1.loc['Customer Interest', month] = m1.loc['Customer Interest Percentage', month]*m1.loc['Avg Balance', month]*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        
        m1.loc['MDR Percentage', month] = m1.loc['MDR Percentage', prev_yr_month]
        m1.loc['MDR', month] = m1.loc['MDR Percentage', month]*m1.loc['Avg Balance', month]*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]

        m1.loc['Funding Cost Percentage', month] = m1.loc['Funding Cost Percentage', prev_yr_month]
        m1.loc['Funding Cost', month] = m1.loc['Funding Cost Percentage', month]*m1.loc['Avg Balance', month]*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        
        m1.loc['Interest Margin Percentage', month] = m1.loc[['Customer Interest Percentage','MDR Percentage','Funding Cost Percentage'], month].sum()
        m1.loc['Interest Margin', month] = m1.loc['Interest Margin Percentage', month] * m1.loc['Avg Balance', month]*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        
        m1.loc['CVP Percentage', month] = m1.loc['CVP Percentage', prev_yr_month]
        m1.loc['CVP', month] = m1.loc['CVP Percentage', month] *m1.loc['Avg Balance', month]*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        m1.loc['Interchange', month] = 0.0175*m1.loc['External Sales', month]
        
        m1.loc['Total Revenue', month] = m1.loc[['Interest Margin','CVP','Interchange'],month].sum()
        
        m1.loc['NCL Percentage', month] = m1.loc['NCL Percentage', prev_yr_month]
        m1.loc['NCL', month] = m1.loc['NCL Percentage', month] * m1.loc['Avg Balance', month]*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        
        m1.loc['Net Credit Margin', month] = m1.loc['Total Revenue', month] - m1.loc['NCL', month]
        
        m1.loc['Front Office Expenses Percentage', month] = m1.loc['Front Office Expenses Percentage', prev_yr_month]
        m1.loc['Front Office Expenses', month] = m1.loc['Front Office Expenses Percentage', month]*m1.loc['Avg Balance', 'Month 1']*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        m1.loc['Back Office Expenses Percentage', month] = m1.loc['Back Office Expenses Percentage', prev_yr_month]
        m1.loc['Back Office Expenses', month] = m1.loc['Back Office Expenses Percentage', month] *m1.loc['Avg Balance', 'Month 1' ]*m1.loc['Days in Month', month]/m1.loc['Days in Year', month]
        m1.loc['Total Expenses',month] = m1.loc[['Front Office Expenses', 'Back Office Expenses'], month].sum()
        
        m1.loc['Operating Income', month] = m1.loc['Net Credit Margin', month] - m1.loc['Total Expenses', month]
        
    #     if i==13:
    #         m1.loc['LLR Balance','Month 1'] = 0.05 * m1.loc['Avg Balance', 'Month 1'] * 20/12    
    #     if i>12:   
    #         if (i % 12 == 2) or (i % 12 == 5) or (i % 12 == 8) or (i % 12 == 11):
    #             m1.loc['Loan Loss Reserve', prev_yr_month] =  m1.loc['NCL', prev_yr_month:prev_month].sum()*20/12 - m1.loc['LLR Balance', prev_yr_month]
    #         else:
    #             m1.loc['Loan Loss Reserve', prev_yr_month] = 0            
                
        
    #     if i>13:
    #         prev_yr_prev_month = "Month "+ str(i-13)
    # #         print(prev_yr_prev_month)
    #         m1.loc['LLR Balance', prev_yr_month] = m1.loc['LLR Balance', prev_yr_prev_month] + m1.loc['Loan Loss Reserve', prev_yr_month]

    #     m1.loc['Total EBIT', prev_yr_month] = m1.loc['Operating Income', prev_yr_month] - m1.loc['Loan Loss Reserve', prev_yr_month]
        
    #     m1.loc['Interchange Percentage', month] = m1.loc['Interchange', month]/m1.loc['Avg Balance', month]*m1.loc['Days in Year', month]/m1.loc['Days in Month', month]
    #     m1.loc['Total Revenue Percentage', month] = m1.loc[['Interest Margin Percentage','CVP Percentage','Interchange Percentage'], month].sum()
    #     m1.loc['Net Credit Margin Percentage', month] = m1.loc['Total Revenue Percentage', month] - m1.loc['NCL Percentage', month]
    #     m1.loc['Total Expenses Percentage', month] = m1.loc[['Front Office Expenses Percentage','Back Office Expenses Percentage'], month].sum()
    #     m1.loc['Operating Income Percentage', month] = m1.loc['Net Credit Margin Percentage', month] - m1.loc['Total Expenses Percentage',month]
        
    #     m1.loc['Loan Loss Reserve Percentage', prev_yr_month] =  m1.loc['Loan Loss Reserve', prev_yr_month] / m1.loc['Avg Balance', prev_yr_month] * m1.loc['Days in Year', prev_yr_month]/m1.loc['Days in Month', prev_yr_month] 
    #     m1.loc['Total EBIT Percentage', prev_yr_month] = m1.loc['Operating Income Percentage', prev_yr_month] - m1.loc['Loan Loss Reserve Percentage', prev_yr_month]

        if i==13:
            m1.loc['LLR Balance','Month 1'] = 0.05 * m1.loc['Avg Balance', 'Month 1'] * 20/12    
        if i>12:
            prev_yr_prev_month = "Month "+ str(i-13)
            if (i % 12 == 2) or (i % 12 == 5) or (i % 12 == 8) or (i % 12 == 11):
                m1.loc['Loan Loss Reserve', prev_yr_month] =  m1.loc['NCL', prev_yr_month:prev_month].sum()*(20/12) - m1.loc['LLR Balance', prev_yr_prev_month]
    #             print(m1.loc['NCL', prev_yr_month:prev_month].sum())
    #             print(prev_yr_prev_month)
    #             print(m1.loc['LLR Balance', prev_yr_prev_month])
            else:
                m1.loc['Loan Loss Reserve', prev_yr_month] = 0                     
        
        if i>13:
            prev_yr_prev_month = "Month "+ str(i-13)
    #         print(prev_yr_prev_month)
            m1.loc['LLR Balance', prev_yr_month] = m1.loc['LLR Balance', prev_yr_prev_month] + m1.loc['Loan Loss Reserve', prev_yr_month]
        
    #     print(m1.loc['Loan Loss Reserve', prev_yr_month])
        m1.loc['Total EBIT', prev_yr_month] = m1.loc['Operating Income', prev_yr_month] - m1.loc['Loan Loss Reserve', prev_yr_month]
        
        m1.loc['Interchange Percentage', month] = m1.loc['Interchange', month]/m1.loc['Avg Balance', month]*m1.loc['Days in Year', month]/m1.loc['Days in Month', month]
        m1.loc['Total Revenue Percentage', month] = m1.loc[['Interest Margin Percentage','CVP Percentage','Interchange Percentage'], month].sum()
        m1.loc['Net Credit Margin Percentage', month] = m1.loc['Total Revenue Percentage', month] - m1.loc['NCL Percentage', month]
        m1.loc['Total Expenses Percentage', month] = m1.loc[['Front Office Expenses Percentage','Back Office Expenses Percentage'], month].sum()
        m1.loc['Operating Income Percentage', month] = m1.loc['Net Credit Margin Percentage', month] - m1.loc['Total Expenses Percentage',month]
        
        m1.loc['Loan Loss Reserve Percentage', prev_yr_month] =  m1.loc['Loan Loss Reserve', prev_yr_month] / m1.loc['Avg Balance', prev_yr_month] * m1.loc['Days in Year', prev_yr_month]/m1.loc['Days in Month', prev_yr_month] 
        m1.loc['Total EBIT Percentage', prev_yr_month] = m1.loc['Operating Income Percentage', prev_yr_month] - m1.loc['Loan Loss Reserve Percentage', prev_yr_month]
        
        
    for i in range(37,49):
        month = 'Month '+str(i)
        prev_month = 'Month '+str(i-1)
        prev_yr_month = 'Month '+str(i-12)
        m1.loc['Loan Loss Reserve', month] = m1.loc['Loan Loss Reserve', prev_yr_month]
        m1.loc['LLR Balance', month] = m1.loc['LLR Balance', prev_month] + m1.loc['Loan Loss Reserve', month]
        m1.loc['Loan Loss Reserve Percentage', month] = m1.loc['Loan Loss Reserve', month]/m1.loc['Avg Balance', month]*m1.loc['Days in Year', month]/m1.loc['Days in Month', month]
        m1.loc['Total EBIT', month] = m1.loc['Operating Income', month] - m1.loc['Loan Loss Reserve', month]
        m1.loc['Total EBIT Percentage', month] = m1.loc['Operating Income Percentage', month] - m1.loc['Loan Loss Reserve Percentage', month]



    summary_dict = {}
    #output Validation
    if zero_count==33:
        for i in range(1,2):
            yr = 'bs'
            # yr = str(i-1)
            starting_month = 'Month '+ str(i*12-11)
            endind_month = 'Month ' + str(i*12)
            
            internal_sales_summary = m1.loc['Internal Sales',starting_month : endind_month].sum() / 1000000
            summary_dict['internal_sales_summary_' + yr] = "$"+ str(round(internal_sales_summary, 0))
            
            external_sales_summary = m1.loc['External Sales',starting_month : endind_month].sum() / 1000000
            summary_dict['external_sales_summary_' + yr] = "$"+ str(round(external_sales_summary, 0))

            sales_summary = m1.loc['Total Sales', starting_month : endind_month].sum() / 1000000
            summary_dict['sales_summary_' + yr] = "$"+ str(round(sales_summary, 0))

            payment_rate_summary = m1.loc['Payments',starting_month : endind_month].sum() / m1.loc['BOP Balance', starting_month : endind_month].sum()
            summary_dict['payment_rate_summary_' + yr] = str(round(payment_rate_summary*100, 0))+"%"
            
            enr_summary = m1.loc['EOP Balance', endind_month] / 1000000
            summary_dict['enr_summary_' + yr] = "$"+ str(round(enr_summary, 0))

            
            anr_summary = m1.loc['Avg Balance', starting_month : endind_month].mean() / 1000000
            summary_dict['anr_summary_' + yr] = "$"+ str(round(anr_summary, 0))

            merchant_sales_summary = m1.loc['Merchant Sales', starting_month : endind_month].sum() / 1000000
            summary_dict['merchant_sales_summary_' + yr] = "$"+ str(round(merchant_sales_summary, 0))

            credit_penetration_summary = internal_sales_summary / merchant_sales_summary
            summary_dict['credit_penetration_summary_' + yr] = str(round(credit_penetration_summary*100, 0)) + "%"
            
            transactions_k_summary = m1.loc['Transactions',starting_month : endind_month].sum()/1000
            summary_dict['transactions_k_summary_' + yr] = round(transactions_k_summary, 0)
            
            average_ticket_summary = 1000 * sales_summary / transactions_k_summary    
            summary_dict['average_ticket_summary_' +yr] = "$"+ str(round(average_ticket_summary, 0))

            new_accounts_summary = m1.loc['New Accounts', starting_month : endind_month].sum()
            summary_dict['new_accounts_summary_' +yr] = round(new_accounts_summary, 0)
            
            eop_accounts_summary = m1.loc['EOP Accounts', endind_month]
            summary_dict['eop_accounts_summary_' +yr] = round(eop_accounts_summary, 0)
            
            applications_summary = m1.loc['Applications',starting_month : endind_month].sum()
            summary_dict['applications_summary_' +yr] = round(applications_summary, 0)
            
            approval_rate_summary = new_accounts_summary / applications_summary
            summary_dict['approval_rate_summary_' +yr] = str(round(approval_rate_summary*100, 0)) + "%"
            
            average_actives_summary = m1.loc['Active Accounts', starting_month : endind_month].mean()
            summary_dict['average_actives_summary_' +yr] = round(average_actives_summary, 0)
            
            sales_per_active_summary = 1000000 * sales_summary / average_actives_summary
            summary_dict['sales_per_active_summary_' +yr] = "$"+ str(round(sales_per_active_summary, 0))
            
            balance_per_active_summary = 1000000 * anr_summary / average_actives_summary
            summary_dict['balance_per_active_summary_' +yr] = "$"+ str(round(balance_per_active_summary, 0))
            
            active_rate_summary = average_actives_summary / eop_accounts_summary
            summary_dict['active_rate_summary_' +yr] = str(round(active_rate_summary*100, 0)) + "%"
            
            floating_apr_summary = m1.loc['Floating APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
            summary_dict['floating_apr_summary_' +yr] = str(round(floating_apr_summary*100, 0)) + "%"
            
            fixed_apr_summary = m1.loc['Fixed APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
            summary_dict['fixed_apr_summary_' +yr] = str(round(fixed_apr_summary*100, 0)) + "%"
            
            promo_apr_summary = m1.loc['Promo APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
            summary_dict['promo_apr_summary_' +yr] = str(round(promo_apr_summary*100, 0)) + "%"
            
            transactors_summary = m1.loc['Transactors', starting_month : endind_month].sum() / m1.loc['Total Average Balance',starting_month : endind_month].sum()
            summary_dict['transactors_summary_' +yr] = str(round(transactors_summary*100, 0)) + "%"
            
            total_average_balance_summary = floating_apr_summary + fixed_apr_summary + promo_apr_summary + transactors_summary
            summary_dict['total_average_balance_summary_' +yr] = str(round(total_average_balance_summary*100, 0)) + "%"
        print(summary_dict)
        for i in range(2,5):
            yr = str(i-1)
            starting_month = 'Month '+ str(i*12-11)
            endind_month = 'Month ' + str(i*12)
            
            summary_dict['internal_sales_summary_' + yr] = summary_dict['internal_sales_summary_bs']
            summary_dict['external_sales_summary_' + yr] = summary_dict['external_sales_summary_bs']
            summary_dict['sales_summary_' + yr] = summary_dict['sales_summary_bs']
            summary_dict['payment_rate_summary_' + yr] = summary_dict['payment_rate_summary_bs']
            summary_dict['enr_summary_' + yr] = summary_dict['enr_summary_bs']
            summary_dict['anr_summary_' + yr] = summary_dict['anr_summary_bs']
            summary_dict['merchant_sales_summary_' + yr] = summary_dict['merchant_sales_summary_bs'] 
            summary_dict['credit_penetration_summary_' + yr] = summary_dict['credit_penetration_summary_bs'] 
            summary_dict['transactions_k_summary_' + yr] = summary_dict['transactions_k_summary_bs'] 
            summary_dict['average_ticket_summary_' +yr] =  summary_dict['average_ticket_summary_bs']
            summary_dict['new_accounts_summary_' +yr] =  summary_dict['new_accounts_summary_bs']
            summary_dict['eop_accounts_summary_' +yr] = summary_dict['eop_accounts_summary_bs'] 
            summary_dict['applications_summary_' +yr] = summary_dict['applications_summary_bs']
            summary_dict['approval_rate_summary_' +yr] = summary_dict['approval_rate_summary_bs']
            summary_dict['average_actives_summary_' +yr] = summary_dict['average_actives_summary_bs']
            summary_dict['sales_per_active_summary_' +yr] = summary_dict['sales_per_active_summary_bs']
            summary_dict['balance_per_active_summary_' +yr] = summary_dict['balance_per_active_summary_bs']
            summary_dict['active_rate_summary_' +yr] = summary_dict['active_rate_summary_bs']
            summary_dict['floating_apr_summary_' +yr] = summary_dict['floating_apr_summary_bs']
            summary_dict['fixed_apr_summary_' +yr] = summary_dict['fixed_apr_summary_bs']
            summary_dict['promo_apr_summary_' +yr] = summary_dict['promo_apr_summary_bs']
            summary_dict['transactors_summary_' +yr] = summary_dict['transactors_summary_bs']
            summary_dict['total_average_balance_summary_' +yr] = summary_dict['total_average_balance_summary_bs']
    
    elif zero_count!=33:
        for i in range(1,5):
            yr = ''
            if i==1:
                # print("Baseline Year")
                yr = 'bs'
            else:
                # print("Year "+str(i-1))
                yr = str(i-1)
            starting_month = 'Month '+ str(i*12-11)
            endind_month = 'Month ' + str(i*12)
            
            internal_sales_summary = m1.loc['Internal Sales',starting_month : endind_month].sum() / 1000000
            summary_dict['internal_sales_summary_' + yr] = "$"+ str(round(internal_sales_summary, 0))
            
            external_sales_summary = m1.loc['External Sales',starting_month : endind_month].sum() / 1000000
            summary_dict['external_sales_summary_' + yr] = "$"+ str(round(external_sales_summary, 0))

            sales_summary = m1.loc['Total Sales', starting_month : endind_month].sum() / 1000000
            summary_dict['sales_summary_' + yr] = "$"+ str(round(sales_summary, 0))

            payment_rate_summary = m1.loc['Payments',starting_month : endind_month].sum() / m1.loc['BOP Balance', starting_month : endind_month].sum()
            summary_dict['payment_rate_summary_' + yr] = str(round(payment_rate_summary*100, 0))+"%"
            
            enr_summary = m1.loc['EOP Balance', endind_month] / 1000000
            summary_dict['enr_summary_' + yr] = "$"+ str(round(enr_summary, 0))

            
            anr_summary = m1.loc['Avg Balance', starting_month : endind_month].mean() / 1000000
            summary_dict['anr_summary_' + yr] = "$"+ str(round(anr_summary, 0))

            merchant_sales_summary = m1.loc['Merchant Sales', starting_month : endind_month].sum() / 1000000
            summary_dict['merchant_sales_summary_' + yr] = "$"+ str(round(merchant_sales_summary, 0))

            credit_penetration_summary = internal_sales_summary / merchant_sales_summary
            summary_dict['credit_penetration_summary_' + yr] = str(round(credit_penetration_summary*100, 0)) + "%"
            
            transactions_k_summary = m1.loc['Transactions',starting_month : endind_month].sum()/1000
            summary_dict['transactions_k_summary_' + yr] = round(transactions_k_summary, 0)
            
            average_ticket_summary = 1000 * sales_summary / transactions_k_summary    
            summary_dict['average_ticket_summary_' +yr] = "$"+ str(round(average_ticket_summary, 0))

            new_accounts_summary = m1.loc['New Accounts', starting_month : endind_month].sum()
            summary_dict['new_accounts_summary_' +yr] = round(new_accounts_summary, 0)
            
            eop_accounts_summary = m1.loc['EOP Accounts', endind_month]
            summary_dict['eop_accounts_summary_' +yr] = round(eop_accounts_summary, 0)
            
            applications_summary = m1.loc['Applications',starting_month : endind_month].sum()
            summary_dict['applications_summary_' +yr] = round(applications_summary, 0)
            
            approval_rate_summary = new_accounts_summary / applications_summary
            summary_dict['approval_rate_summary_' +yr] = str(round(approval_rate_summary*100, 0)) + "%"
            
            average_actives_summary = m1.loc['Active Accounts', starting_month : endind_month].mean()
            summary_dict['average_actives_summary_' +yr] = round(average_actives_summary, 0)
            
            sales_per_active_summary = 1000000 * sales_summary / average_actives_summary
            summary_dict['sales_per_active_summary_' +yr] = "$"+ str(round(sales_per_active_summary, 0))
            
            balance_per_active_summary = 1000000 * anr_summary / average_actives_summary
            summary_dict['balance_per_active_summary_' +yr] = "$"+ str(round(balance_per_active_summary, 0))
            
            active_rate_summary = average_actives_summary / eop_accounts_summary
            summary_dict['active_rate_summary_' +yr] = str(round(active_rate_summary*100, 0)) + "%"
            
            floating_apr_summary = m1.loc['Floating APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
            summary_dict['floating_apr_summary_' +yr] = str(round(floating_apr_summary*100, 0)) + "%"
            
            fixed_apr_summary = m1.loc['Fixed APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
            summary_dict['fixed_apr_summary_' +yr] = str(round(fixed_apr_summary*100, 0)) + "%"
            
            promo_apr_summary = m1.loc['Promo APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
            summary_dict['promo_apr_summary_' +yr] = str(round(promo_apr_summary*100, 0)) + "%"
            
            transactors_summary = m1.loc['Transactors', starting_month : endind_month].sum() / m1.loc['Total Average Balance',starting_month : endind_month].sum()
            summary_dict['transactors_summary_' +yr] = str(round(transactors_summary*100, 0)) + "%"
            
            total_average_balance_summary = floating_apr_summary + fixed_apr_summary + promo_apr_summary + transactors_summary
            summary_dict['total_average_balance_summary_' +yr] = str(round(total_average_balance_summary*100, 0)) + "%"

    # m1.to_csv('C:\\Users\\Manish\\Downloads\\SurgeDataLab\\Simulation of FPA Model\\vinayak_code\\Surge-FPA-Simulation\\backend\\outputfiles\\Output.csv')
    DOWNLOAD_FOLDER = 'outputfiles'
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
    m1.to_csv(os.path.join(app.config['DOWNLOAD_FOLDER'], "Output.csv"))
    for key, values in summary_dict.items():
        print(key, values)
        print("\n")
    return summary_dict



@app.route('/calcm', methods=['GET', 'POST'])
def calculate():

    # fetching data from frontend form using POST method
    post = False
    if request.method == "POST":  #for POST request
        
        post = True
        updated_data = request.json  # Get the updated data from the request
    
        # print('Manish, You have successfully received data', updated_data)  # Log the received data for debugging
        manish_data = calculation_logic(updated_data, post)
        return jsonify(manish_data)
    
    elif request.method == 'GET':
        manish_data = calculation_logic([], False)
        return  jsonify(manish_data) #for GET request


@app.route('/ucs', methods=["POST"])
def ucs():
    data = request.get_json()
    input_field_value = data.get('inputField')
    print("received data: "+ data[0]['col1'])

    
OUTPUT_FOLDER = 'outputfiles'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/calculate', methods=['GET'])
def calculate_File():
    calculate()
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'Output.csv')
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Send the file as a response with appropriate headers
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404
    

@app.route('/members')
def members():
 
    # Returning an api for showing in  reactjs
    return {'members':["member1manish", "member2", "member3"]}

 

@app.route('/outputfiles/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Send the file as a response with appropriate headers
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404
    

@app.route('/execute', methods=['POST'])
def execute_data():
    try:
        print('Received POST request to /execute')
        
        data = request.get_json()
        # input_text = data['data']
        # print(input_text)

        # If you want to decode it as a UTF-8 string (assuming it's a JSON string)
        data_str = data.decode('utf-8')

        # Now you can parse the JSON string (assuming it's JSON data)
        json_data = json.loads(data_str)

        # Print the JSON data 
        print('Data received:', json_data)

        # Perform your calculations or processing with the JSON data
        # summary_dict = calculate(json_data)

        # Return a response (for demonstration, just returning 'hello')
        return jsonify({'message': 'Data received successfully'})
    except Exception as e:
        print('Error during calculation:', str(e))
        return jsonify({"error": "An error occurred during calculation"}), 500


# Create a route to serve the uploaded file
@app.route('/get_uploaded_file/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    except FileNotFoundError:
        return 'File not found'

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

@app.route('/update-data', methods=['POST'])
def update_data():
    try:
        updated_data = request.json  # Get the updated data from the request
        # Validate and sanitize the updated_data if necessary
        # print('Received data:', [i*2 for i in updated_data])  # Log the received data for debugging
        print('Received data:',  updated_data)  # Log the received data for debugging

        return jsonify({'message': 'External sales summary updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)