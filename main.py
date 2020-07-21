from tkinter import *
from tkinter import messagebox,Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My crypto portfolio")
pycrypto.iconbitmap('favicon.ico')

con = sqlite3.connect('coin1.db')
cobj =con.cursor()

cobj.execute("CREATE TABLE IF NOT EXISTS coin1(id INTEGER PRIMARY KEY ,symbol TEXT,amount INTEGER,price REAL)")
con.commit()

# cobj.execute("DELETE FROM coin where symbol='NEO'")
# con.commit()

# cobj.execute("INSERT INTO coin VALUES(2,'ETH',5 ,120)")
# con.commit()
#
# cobj.execute("INSERT INTO coin VALUES(3,'NEO',5 ,10)")
# con.commit()
#
# cobj.execute("INSERT INTO coin VALUES(4,'XMR',3 ,30)")
# con.commit()

def reset():
    for frame in pycrypto.winfo_children():
        frame.destroy()

    app_nav()
    app_header()
    my_portfolio()

def app_nav():
    def clear_all():
        cobj.execute("DELETE FROM coin1")
        con.commit()

        messagebox.showinfo("Portfolio Notifier", "Portfolio Cleared")
        reset()

    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio',command = clear_all)
    file_item.add_command(label='Close App',command = close_app)
    menu.add_cascade(label="File",menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=5c44960c-5f4d-47be-95b3-64a3702234a3")

    api = json.loads(api_request.content)

    cobj.execute("SELECT * FROM coin1")
    coins= cobj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return 'green'
        else:
            return 'red'

    def insert_coin():
        cobj.execute("INSERT INTO coin1(symbol,price,amount) VALUES(?,?,?)",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notifier","Coin Added Successfully")
        reset()

    def update():
        cobj.execute("UPDATE coin1 SET symbol=?,price=?,amount=? where id=?",(symbol_update.get(),price_update.get(),amount_update.get(),portid_update.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notifier", "Coin updated Successfully")
        reset()

    def delete_coin():
        cobj.execute("DELETE FROM coin1 where symbol=?",(portid_delete.get(),))
        con.commit()

        messagebox.showinfo("Portfolio Notifier", "Coin Deleted Successfully")
        reset()
    # coins = [
    #     {
    #         "symbol":"BTC",
    #         "amount_owned":2,
    #         "price_per_coin":3200
    #     },
    #     {
    #         "symbol":"ETH",
    #         "amount_owned":100,
    #         "price_per_coin":2.05
    #     },
    #     {
    #         "symbol": "LTC",
    #         "amount_owned": 10,
    #         "price_per_coin": 50
    #     },
    #     {
    #         "symbol": "XMR",
    #         "amount_owned": 50,
    #         "price_per_coin": 25
    #     },
    #     {
    #         "symbol": "BCH",
    #         "amount_owned": 20,
    #         "price_per_coin": 40.20
    #     }
    # ]
    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amt_paid = 0

    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_per_coin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_per_coin * coin[2]

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amt_paid += total_paid

                # print(api["data"][i]["name"]+ "-" + api["data"][i]["symbol"])
                # print("Price:" ,"${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Total No of Coins:",coin[2])
                # print("Total amount paid:","${0:.2f}".format(total_paid))
                # print("Current value:", "${0:.2f}".format(current_value))
                # print("P/L coin:", "${0:.2f}".format(pl_per_coin))
                # print("Total P/L with coin:", "${0:.2f}".format(total_pl_coin))

                portfolio_id = Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black", font="Lato 12 bold",padx="5", pady="5", borderwidth="2", relief="groove")
                portfolio_id.grid(row=coin_row, column=0, sticky=N + S + E + W)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
                name.grid(row=coin_row, column=1, sticky=N + S + E + W)
                # name.pack()

                price = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
                price.grid(row=coin_row, column=2, sticky=N + S + E + W)

                no_coin = Label(pycrypto, text=coin[2], bg="#F3F4F6", fg="black",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
                no_coin.grid(row=coin_row, column=3, sticky=N + S + E + W)

                amt_paid = Label(pycrypto, text="${0:.2f}".format(total_paid), bg="#F3F4F6", fg="black",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
                amt_paid.grid(row=coin_row, column=4, sticky=N + S + E + W)

                current_value = Label(pycrypto, text="${0:.2f}".format(current_value), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(current_value))),font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
                current_value.grid(row=coin_row, column=5, sticky=N + S + E + W)

                pl_coin = Label(pycrypto, text="${0:.2f}".format(pl_per_coin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(pl_per_coin))),font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
                pl_coin.grid(row=coin_row, column=6, sticky=N + S + E + W)

                totalpl = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(total_pl_coin))),font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
                totalpl.grid(row=coin_row, column=7, sticky=N + S + E + W)

                coin_row += 1

    # INSERT DATA

    symbol_txt = Entry(pycrypto,borderwidth=2,relief="groove")
    symbol_txt.grid(row=coin_row+1,column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row + 1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row + 1, column=3)

    add_coin = Button(pycrypto, text="ADD COIN", bg="#142E54", fg="white", command=insert_coin, font="Lato 12 bold",padx="5", pady="5", borderwidth="2", relief="groove")
    add_coin.grid(row=coin_row + 1, column=4, sticky=N + S + E + W)

    # UPDATE COIN

    portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_update.grid(row=coin_row + 2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row + 2, column=1)

    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row + 2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row + 2, column=3)

    update_coin = Button(pycrypto, text="UPDATE COIN", bg="#142E54", fg="white", command=update, font="Lato 12 bold",padx="5", pady="5", borderwidth="2", relief="groove")
    update_coin.grid(row=coin_row + 2, column=4, sticky=N + S + E + W)

    # UPDATE COIN

    portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_delete.grid(row=coin_row + 3, column=0)

    delete_coin = Button(pycrypto, text="DELETE COIN", bg="#142E54", fg="white", command=delete_coin, font="Lato 12 bold",padx="5", pady="5", borderwidth="2", relief="groove")
    delete_coin.grid(row=coin_row + 3, column=4, sticky=N + S + E + W)

    totalap = Label(pycrypto, text="${0:.2f}".format(total_amt_paid), bg="#F3F4F6", fg="black",font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove")
    totalap.grid(row=coin_row, column=4, sticky=N + S + E + W)

    totalcv = Label(pycrypto, text="${0:.2f}".format(total_current_value), bg="#F3F4F6", fg="black", font="Lato 12 bold",padx="5", pady="5", borderwidth="2", relief="groove")
    totalcv.grid(row=coin_row, column=5, sticky=N + S + E + W)
    # print("Total P/L for PortFolio:","${0:.2f}".format(total_pl))

    totalpll = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(total_pl))), font="Lato 12 bold",padx="5", pady="5", borderwidth="2", relief="groove")
    totalpll.grid(row=coin_row, column=7, sticky=N + S + E + W)

    api = ""

    refresh = Button(pycrypto, text="Refresh", bg="#142E54",fg="white", command=reset, font="Lato 12 bold", padx="5", pady="5",borderwidth="2", relief="groove")
    refresh.grid(row=coin_row + 1, column=7, sticky=N + S + E + W)

def app_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",borderwidth="2", relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N + S + E + W)

    name = Label(pycrypto,text="Coin Name",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
    name.grid(row= 0,column=1,sticky=N+S+E+W)
    # name.pack()a

    price = Label(pycrypto,text="Price",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
    price.grid(row= 0,column=2,sticky=N+S+E+W)

    no_coin = Label(pycrypto,text="Coins Owned",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
    no_coin.grid(row= 0,column=3,sticky=N+S+E+W)

    amt_paid = Label(pycrypto,text="Total Amount Paid",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
    amt_paid.grid(row= 0,column=4,sticky=N+S+E+W)

    current_value = Label(pycrypto,text="Current Value",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
    current_value.grid(row= 0,column=5,sticky=N+S+E+W)

    pl_coin = Label(pycrypto,text="P/L per Coin",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
    pl_coin.grid(row= 0,column=6,sticky=N+S+E+W)

    totalpl = Label(pycrypto,text="Total P/L with Coin",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth="2",relief="groove")
    totalpl.grid(row= 0,column=7,sticky=N+S+E+W)

app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

cobj.close()
con.close()

print("Program Completed")