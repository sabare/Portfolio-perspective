from flask import Flask, render_template, request , jsonify
import pandas as pd
import matplotlib.pyplot as plt
import ta
import io
import base64
import numpy as np
app = Flask(__name__)
# define a function that takes input and returns output
def my_function(input_string):
    # perform some processing on the input
    output_string = input_string.upper()
    # return the output
    return output_string

df=pd.read_csv('bq-results-20230414-214948-1681509023746.csv')
counts = df['symbol'].value_counts()
names=(counts[counts<600]).index.tolist()
df = df[~df['symbol'].isin(names)]
companies_1=df['symbol'].unique()
df_grouped=df.groupby(['symbol'])

def f1(company_list,capital):
  df_corr=pd.DataFrame()
  dic={}
  for Company_Name in company_list:
    df_company=df_grouped.get_group(Company_Name)
    df_company.sort_values(by='ds',inplace=True)
    dic[Company_Name]=list(df_company['close'])
  for i in dic.keys():
    df_corr[i]=dic[i][:600]
  var=df_corr.var()
  corr=df_corr.corr()
  rho=(sum(np.sum(corr))-len(corr))/6
  i=0
  for (columnName, columnData) in df_corr.items():
    df_corr[columnName]=df_corr[columnName].diff(periods=1)/columnData[i]
    i+=1
  df_corr.dropna()
  c=0
  for (columnName, columnData) in df_corr.items():
    c+=(df_corr[columnName].mean())/var[columnName]
  c1=c*rho/(1-rho+len(corr)*rho)
  w=[]
  for (columnName, columnData) in df_corr.items():
    w.append(((df_corr[columnName].mean())/var[columnName]-c1)/var[columnName])
  
  s=sum([abs(x) for x in w])
  for i in range(len(w)):
    w[i]=w[i]/s
  ans=[]
  for i in w:
    ans.append(i*capital)
  return ans
def analysis(Company_Name, a=-1, b=-1, a1=-1, a2=-1, b2=-1, c2=-1, a3=-1):
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    df_company = df_grouped.get_group(Company_Name)
    ts = df_company[['close', 'ds']]
    ts.sort_values(by='ds', inplace=True)
    ts=ts.tail(300)

    def sma(a, b):
        ts['fast_sma'] = ts['close'].rolling(a).mean()
        ts['slow_sma'] = ts['close'].rolling(b).mean()
        ts['RSI'] = ta.momentum.RSIIndicator(df['close']).rsi()
        ax[0,0].set_title("sma")
        ax[0, 0].plot(ts['ds'], ts['close'], label='close')
        ax[0, 0].plot(ts['ds'], ts['fast_sma'] ,label='Fast')
        ax[0, 0].plot(ts['ds'], ts['slow_sma'] ,label='SLow')
        ax[0, 0].legend()

    def bb(a):
        ts['MA20'] = ts['close'].rolling(window=a).mean()
        ts['std20'] = ts['close'].rolling(window=a).std()
        ts['upper_band'] = ts['MA20'] + 2 * ts['std20']
        ts['lower_band'] = ts['MA20'] - 2 * ts['std20']
        ax[0,1].set_title("Bollinger Bands")
        ax[0, 1].plot(ts['ds'], ts['upper_band'],label='Upper bound')
        ax[0, 1].plot(ts['ds'], ts['lower_band'],label='Lower bound')
        ax[0, 1].plot(ts['ds'], ts['close'], label='close')
        ax[0, 1].legend()

    def macd(a, b, c):
        fast_ema = df['close'].ewm(span=a, adjust=False).mean()
        slow_ema = df['close'].ewm(span=b, adjust=False).mean()
        macd = fast_ema - slow_ema
        signal_line = macd.ewm(span=c, adjust=False).mean()
        histogram = macd - signal_line
        ax[1,0].set_title("MACD")
        ts['Histogram'] = histogram
        ax[1, 0].plot(ts['ds'], ts['Histogram'])

    def rsi():
        ax[1, 1].plot(ts['ds'], ts['RSI'])
        ax[1, 1].set_title("RSI")
        ax[1, 1].axhline(y=70, linestyle='--')
        ax[1, 1].axhline(y=30,linestyle='--')

    if a != -1 and b != -1:
        sma(a, b)
    if a1 != -1:
        bb(a1)
    if a2 != -1 and b2 != -1 and c2 != -1:
        macd(a2, b2, c2)
    if a3 != -1:
        rsi()
    return fig

# define the home page route
@app.route('/')
def home():
    return render_template('index1.html',companies_1=(companies_1))
# define the output page route
@app.route('/output1', methods=['POST'])
def output1():
    Company_Name = request.form['symbol']
    a = int(request.form['sma-small'])
    b = int(request.form['sma-large'])
    a1 = int(request.form['bb-size'])
    a2 = int(request.form['macd-small'])
    b2 = int(request.form['macd-large'])
    c2 = int(request.form['macd-signal'])
    a3 = 1

    ans = analysis(Company_Name, a, b, a1, a2, b2, c2, a3)
    buffer = io.BytesIO()
    ans.savefig(buffer, format='png')
    buffer.seek(0)

    plot_data = base64.b64encode(buffer.getvalue()).decode()
    data_uri = 'data:image/png;base64,' + plot_data
    return render_template('output1.html',plot=data_uri)
# define the output page route
@app.route('/output', methods=['POST'])
def output():
    # num_companies = int(request.form['no-of-stocks'])
    # companies = []
    x=int(request.form['capt_amnt'])
    print(x)
    selected_companies = request.form.getlist('company')
    # for i in range(1, num_companies + 1):
    #     company_name = request.form['company' + str(i)]
    #     companies.append(company_name)
    ans=f1(selected_companies,x)
    company_prices = list(zip(selected_companies, ans))
    return render_template('output.html',companies=company_prices)

if __name__ == '__main__':
    app.run(debug=True)
