import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

def get_dataset():
    file_path = 'C:\\Users\\Vinayak\\Desktop\\Surge Finance Model Simualtion\\backend\\uploads\\FPA Model Input File.csv'
    model1 = pd.read_csv(file_path, index_col='Driver Model') #model1 is dataframe
    m1 = model1.head(25) #m1 is dataframe

    for i in range(1,13):
        month = 'Month ' + str(i)
        m1[month] = m1[month].str.replace(",","").str.replace("(","-").str.replace(")","")     
        m1[month] = m1[month].astype(float)
    return m1

def calculate():
    m1=get_dataset()
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
    external_sales_summary_yn = [0.000, 0.1000, 0.02000]         
    # I 5
    payment_rate_summary_yn = [0.0005, 0.0010, 0.0015]          
    # I 9
    merchant_sales_summary_yn = [0.1, 0.05, 0.02]           
    # I 10
    credit_penetration_summary_yn = [0.0005, 0.001, 0.0015]    
    # I 11
    transaction_k_summary_yn = [0.05, 0.02, 0.02]           
    # I 19
    applications_summary_yn = [0.04, 0.03, 0.02]
    # I 20
    approval_rate_summary_yn = [0.0005, 0.001, 0.0015]
    # I 22
    active_rate_summary_yn = [0.0005, 0.001, 0.0015] 
    # I 25
    floating_apr_summary_yn = [0.0005, 0.001, 0.0015]
    # I 26
    fixed_apr_summary_yn = [0.0005, 0.001, 0.0015]
    # I 27
    promo_apr_summary_yn = [0.0005, 0.001, 0.0015]

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
        
        if i==13:
            m1.loc['LLR Balance','Month 1'] = 0.05 * m1.loc['Avg Balance', 'Month 1'] * 20/12    
        if i>12:   
            if (i % 12 == 2) or (i % 12 == 5) or (i % 12 == 8) or (i % 12 == 11):
                m1.loc['Loan Loss Reserve', prev_yr_month] =  m1.loc['NCL', prev_yr_month:prev_month].sum()*20/12 - m1.loc['LLR Balance', prev_yr_month]
            else:
                m1.loc['Loan Loss Reserve', prev_yr_month] = 0            
                
        
        if i>13:
            prev_yr_prev_month = "Month "+ str(i-13)
    #         print(prev_yr_prev_month)
            m1.loc['LLR Balance', prev_yr_month] = m1.loc['LLR Balance', prev_yr_prev_month] + m1.loc['Loan Loss Reserve', prev_yr_month]

        m1.loc['Total EBIT', prev_yr_month] = m1.loc['Operating Income', prev_yr_month] - m1.loc['Loan Loss Reserve', prev_yr_month]
        
        m1.loc['Interchange Percentage', month] = m1.loc['Interchange', month]/m1.loc['Avg Balance', month]*m1.loc['Days in Year', month]/m1.loc['Days in Month', month]
        m1.loc['Total Revenue Percentage', month] = m1.loc[['Interest Margin Percentage','CVP Percentage','Interchange Percentage'], month].sum()
        m1.loc['Net Credit Margin Percentage', month] = m1.loc['Total Revenue Percentage', month] - m1.loc['NCL Percentage', month]
        m1.loc['Total Expenses Percentage', month] = m1.loc[['Front Office Expenses Percentage','Back Office Expenses Percentage'], month].sum()
        m1.loc['Operating Income Percentage', month] = m1.loc['Net Credit Margin Percentage', month] - m1.loc['Total Expenses Percentage',month]
        
        m1.loc['Loan Loss Reserve Percentage', prev_yr_month] =  m1.loc['Loan Loss Reserve', prev_yr_month] / m1.loc['Avg Balance', prev_yr_month] * m1.loc['Days in Year', prev_yr_month]/m1.loc['Days in Month', prev_yr_month] 
        m1.loc['Total EBIT Percentage', prev_yr_month] = m1.loc['Operating Income Percentage', prev_yr_month] - m1.loc['Loan Loss Reserve Percentage', prev_yr_month]


    #output Validation
    for i in range(1,5):
        if i==1:
            print("Baseline Year")
        else:
            print("Year "+str(i-1))
        starting_month = 'Month '+ str(i*12-11)
        endind_month = 'Month ' + str(i*12)
        
        internal_sales_summary = m1.loc['Internal Sales',starting_month : endind_month].sum() / 1000000
        print("Internal Sales Summary: ",internal_sales_summary)
        
        external_sales_summary = m1.loc['External Sales',starting_month : endind_month].sum() / 1000000
        print("External Sales Summary: ", external_sales_summary)
        
        sales_summary = m1.loc['Total Sales', starting_month : endind_month].sum() / 1000000
        print("Sales Summary: ", sales_summary)
        
        payment_rate_summary = m1.loc['Payments',starting_month : endind_month].sum() / m1.loc['BOP Balance', starting_month : endind_month].sum()
        print("Payment Rate Summary: ", payment_rate_summary)
        
        enr_summary = m1.loc['EOP Balance', endind_month] / 1000000
        print("ENR Summary: ", enr_summary)
        
        anr_summary = m1.loc['Avg Balance', starting_month : endind_month].mean() / 1000000
        print("ANR Summary: ", anr_summary)
        
        merchant_sales_summary = m1.loc['Merchant Sales', starting_month : endind_month].sum() / 1000000
        print("Merchant Sales Summary: ", merchant_sales_summary)
        
        credit_penetration_summary = internal_sales_summary / merchant_sales_summary
        print("Credit Penetration Summary: ", credit_penetration_summary)
        
        transactions_k_summary = m1.loc['Transactions',starting_month : endind_month].sum()/1000
        print("Transactions K summary: ", transactions_k_summary)
        
        average_ticket_summary = 1000 * sales_summary / transactions_k_summary    
        print("Average Ticket Summary: ", average_ticket_summary)
        
        new_accounts_summary = m1.loc['New Accounts', starting_month : endind_month].sum()
        print("New accounts Summary: ", new_accounts_summary)
        
        eop_accounts_summary = m1.loc['EOP Accounts', endind_month]
        print("EOP Accounts Summary: ", eop_accounts_summary)
        
        applications_summary = m1.loc['Applications',starting_month : endind_month].sum()
        print("Applications Summary: ", applications_summary)
        
        approval_rate_summary = new_accounts_summary / applications_summary
        print("Approval Rate Summary: ", approval_rate_summary)
        
        average_actives_summary = m1.loc['Active Accounts', starting_month : endind_month].mean()
        print("Average Actives Summary: ", average_actives_summary)
        
        sales_per_active_summary = 1000000 * sales_summary / average_actives_summary
        print("Sales Per active Summary: ", sales_per_active_summary)
        
        balance_per_active_summary = 1000000 * anr_summary / average_actives_summary
        print("Balance Per Active Summary: ", balance_per_active_summary)
        
        active_rate_summary = average_actives_summary / eop_accounts_summary
        print("Active Rate Summary: ", active_rate_summary)
        
        floating_apr_summary = m1.loc['Floating APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
        print("Floating APR Summary: ", floating_apr_summary)
        
        fixed_apr_summary = m1.loc['Fixed APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
        print("Fixed APR Summary: ", fixed_apr_summary)
        
        promo_apr_summary = m1.loc['Promo APR', starting_month : endind_month].sum() / m1.loc['Total Average Balance', starting_month : endind_month].sum()
        print("Promo APR Summary: ", promo_apr_summary)
        
        transactors_summary = m1.loc['Transactors', starting_month : endind_month].sum() / m1.loc['Total Average Balance',starting_month : endind_month].sum()
        print("Transactors Summary: ", transactors_summary)
        
        total_average_balance_summary = floating_apr_summary + fixed_apr_summary + promo_apr_summary + transactors_summary
        print("Total Average Balance Summary: ", total_average_balance_summary)
        print("\n")
    m1.to_csv("Output.csv") 
        
calculate()
