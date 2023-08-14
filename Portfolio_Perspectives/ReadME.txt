Dependencies:
– Matplotlib_version==3.7.0
– Install Flask,ta, io, base_64
– Install Prophet,plotly,streamlit


Steps to have this model work properly:
 Download the complete folder
 save all files in a single folder and then upload the dataset in that folder
 dataset link: '''https://drive.google.com/file/d/1FmS75CarVlVPRVbCAR2p3yWNQnEMmQ_v/view?usp=sharing'''
1. 1st have all dependencies run and then run the app.py file 
2. Then run the command “streamlit run main.py for the main.py in a new terminal under that same folder 
3. Remember to install all required dependencies


Functionalities:
* Portfolio Management:
* Given the Capital and the list of stocks, we predict the amount that can be invested in each stock. 
* It is done by arranging the stocks based on the Sortino ratio, assuming the risk-free interest rate to be 0
* Negative values denote short-selling scenarios and we use Lintner's definition to normalise the weights which account for the collateral during short selling


* Chart Analysis:
* For a given stock and corresponding parameters, we provide charts having a good mix of necessary technical indicators such as SMA, MACD for predicting trends, BB for volatility and RSI for momentum prediction
* These charts are plotted using the last 300-day prices of the last data set in the price column


* Price prediction:
* Using the Yahoo finance data set, to predict the future price movements of a given stock using the LSTM model and the pre-trained Prophet API


Data sets used:
* The latest dataset in the prices folder
* Yahoo finance dataset


Technologies used:
* Python for Analysis, and Flask for integration
* Packages such as Simulit, 
* HTML, CSS for the frontend


Inbuilt Models Used:
* Prophet: A Trained model for millions of time series data to predict trends and seasonal forecasting where it was modelled by facebook  employees to take or capture the trend of the stock price and to predict the future price .
* It is basically a Time series model with very high accuracy and prediction capabilities
