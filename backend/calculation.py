import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

file_path = 'C:\\Users\\Vinayak\\Desktop\\Surge Finance Model Simualtion\\backend\\uploads\\FPA Model Input File.csv'
model1 = pd.read_csv(file_path, index_col='Driver Model') #model1 is dataframe
m1 = model1.head(25) #m1 is dataframe

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

m1.to_csv('C:\\Users\\Vinayak\\Desktop\\Surge Finance Model Simualtion\\backend\\outputfiles\\Output.csv')

