import customtkinter as ctk
from twelvedata import TDClient
import time, threading, json
import miniaudio


APIKEY = "YOUR_API_KEY"
ADVICE_AUDIO_PATH = "lello.mp3"
new_stock_label = None
root = ctk.CTk()

stocks_dict = {}
labels_list = {}
root.iconbitmap("stock.ico")

root.geometry("500x200")
root.title("Stocks Monitor V1.2")

corner_radius=80

def prezzo_raggiunto(stock_price,symbol):
   
    
    threading.Thread(target= ctk.CTkInputDialog(text=f"THE STOCK {symbol} HAS PASS {stock_price} USD",title="!ADVICE!"))
    stream = miniaudio.stream_file(ADVICE_AUDIO_PATH)
    with miniaudio.PlaybackDevice() as device:
        device.start(stream)


def open_saves():
    global value,stocks_dict,new_stock_label
    try:
        with open("save.json", "r") as file:
            datas = json.load(file)
            stocks_dict = datas
            for key, value in datas.items():
                stocks_dict[key] = value
                td = TDClient(APIKEY)
                ts = td.time_series(
                    symbol=key,
                    interval="1min",
                    outputsize=1,
            
                )
                    
                df = ts.as_pandas()
                stock_price =  df["close"].iloc[0] #PRENDE L'ULTIMO PREZZO DELLO STOCK.
                new_stock_label = ctk.CTkLabel(root, text=f"TICKER: {key} | {"CURRENT PRICE: " + str(stock_price)} | 'PRICE TO REACH:  {str(value)}")
                new_stock_label.grid(column=0,padx=20,columnspan=2)
                labels_list[new_stock_label] = [key,value]
        file.close()
    except FileNotFoundError:
        pass
    except Exception as e:
    
        print(e)
        
        

def new_stock():
    global new_stock_label
    prezzo_limitevar_get = prezzo_limitevar.get()
    stock_ticker_entry_text_get = stock_ticker_entry_text.get()
    td = TDClient(apikey=APIKEY)

    ts = td.time_series(symbol=stock_ticker_entry_text_get,interval="1min",outputsize=1)

    df = ts.as_pandas()
    last_price = df["close"].iloc[-1]
    
    
    new_stock_label = ctk.CTkLabel(root, text=f"TICKER: {stock_ticker_entry_text_get} | CURRENT PRICE:  {str(last_price)} | PRICE TO REACH:  {str(prezzo_limitevar_get)}")
    new_stock_label.grid(column=0, padx = 20,columnspan=2)
    
    stocks_dict[stock_ticker_entry_text_get] = prezzo_limitevar_get
    
    
    labels_list[new_stock_label] = [stock_ticker_entry_text_get,prezzo_limitevar_get]

def update_stock():
    while True:
        for label, symbol_price in labels_list.items():
            symbol = symbol_price[0]
            prezzo_da_raggiungere = symbol_price[1]
            td = TDClient(apikey=APIKEY)

            ts = td.time_series(symbol=symbol,interval="1min",outputsize=1)

            df = ts.as_pandas()
            last_price = df["close"].iloc[-1]
            label.configure(text=f"TICKER: {symbol} | CURRENT PRICE: {str(last_price)} | 'PRICE TO REACH:  {str(prezzo_da_raggiungere)}")
                
            print(f"prezzo aggiornato {symbol}  {prezzo_da_raggiungere}")
        
            if float(last_price) > float(prezzo_da_raggiungere):
                prezzo_raggiunto(prezzo_da_raggiungere,symbol)
        time.sleep(30)
          

def remove_stock():
    global stocks_dict,labels_list
    last_key = next(reversed(stocks_dict))
    
    del stocks_dict[last_key]
    
    last_key = next(reversed(labels_list))
    last_key.destroy()
    del labels_list[last_key]

    root.update()
    
def save_stocks():
    global stocks_dict
    with open("save.json","w") as file:
       json.dump(stocks_dict,file, indent=4)
       
       

def price_thread():
    threading.Thread(target=new_stock,daemon=True).start()
threading.Thread(target=update_stock,daemon=True).start()
prezzo_limitevar = ctk.StringVar()
stock_ticker_entry_text = ctk.StringVar()
attualpricelabelvar = ctk.StringVar()

################################################################

label = ctk.CTkLabel(root,text="Write the ticker")
label.grid(row=0,column=0)
label2 = ctk.CTkLabel(root,text="Write the price")
label2.grid(row=0,column=1)

########################################################################à
stock_ticker_entry = ctk.CTkEntry(root,font=("Helvetica",20),width=200,textvariable=stock_ticker_entry_text)
stock_ticker_entry.grid(row=1,column=0)

prezzo_limite = ctk.CTkEntry(root,font=("Helvetica",20),width=200,textvariable=prezzo_limitevar)
prezzo_limite.grid(row=1, column=1)

add_button = ctk.CTkButton(root, text= "+", font=("Arial",16),corner_radius=corner_radius,command=price_thread)
add_button.grid(row=2,column=0)

remove_button = ctk.CTkButton(root, text= "Del", font=("Arial",16),corner_radius=corner_radius,command=remove_stock)
remove_button.grid(row=2,column = 1)
#########################################################################################


    
open_saves()

root.mainloop()


save_stocks()#SALVA IL DIZIONARIO CON TICKER COME CHIAVI E IL PREZZO MAX COME VALORI!

print("program finished")
