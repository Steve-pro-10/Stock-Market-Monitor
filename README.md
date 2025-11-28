# Stock-Market-Monitor

Stock-Market-Monitor is a Python application designed to track stock prices in real time.
To begin monitoring, simply enter a ticker symbol in the first field and the target price in the second.
For example, entering “TSLA” as the ticker and “460” as the target price will cause the program to play an alert tone and display a pop-up notification once Tesla’s stock reaches $460.
If the target price has not yet been reached, the interface will show:

-The ticker symbol,

-The current stock price (updated every minute)
-The target price that will trigger the alert.


<img width="432" height="203" alt="immagine" src="https://github.com/user-attachments/assets/a3a60e10-8384-4eaf-8f3c-4e599ff6b87f" />


⚠️ Important

To use this program, you must provide your TwelveData API key.
If you don’t have one, register at the twelvedata.com website and replace the value of the APIKEY constant in the script with your personal key.
