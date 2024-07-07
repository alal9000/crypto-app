from ast import Lambda
import matplotlib.pyplot as plt
from tkinter import *
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def red_green(amount):
    if amount >= 0:
        return "green"
    else:
        return "red"

root = Tk()
root.title("Crypto currency portfolio")
# root.iconbitmap(r'C:\\Users\\aaron\\OneDrive\Desktop\\pixel-art\\penguin.PNG')

# create header
header_name = Label(root, text="Name", bg="white", font="Verdana 8 bold")
header_name.grid(row=0, column=0, sticky=N+S+E+W)

header_current_price = Label(root, text="Current Price", bg="white", font="Verdana 8 bold")
header_current_price.grid(row=0, column=1, sticky=N+S+E+W)

header_price_paid = Label(root, text="Price Paid", bg="silver", font="Verdana 8 bold")
header_price_paid.grid(row=0, column=2, sticky=N+S+E+W)

balance = Label(root, text="Balance", bg="white", font="Verdana 8 bold")
balance.grid(row=0, column=3, sticky=N+S+E+W)

header_1_hr_change = Label(root, text="1 HR Change", bg="silver", font="Verdana 8 bold")
header_1_hr_change.grid(row=0, column=4, sticky=N+S+E+W)

header_24_hr_change = Label(root, text="24 HR Change", bg="white", font="Verdana 8 bold")
header_24_hr_change.grid(row=0, column=5, sticky=N+S+E+W)

header_7_day_change = Label(root, text="7 Day Change", bg="silver", font="Verdana 8 bold")
header_7_day_change.grid(row=0, column=6, sticky=N+S+E+W)

header_profit_loss_total = Label(root, text="Profit/Loss Total", bg="silver", font="Verdana 8 bold")
header_profit_loss_total.grid(row=0, column=7, sticky=N+S+E+W)

header_current_value = Label(root, text="Portfolio Value", bg="white", font="Verdana 8 bold")
header_current_value.grid(row=0, column=8, sticky=N+S+E+W)

header_total_paid = Label(root, text="Total Paid", bg="silver", font="Verdana 8 bold")
header_total_paid.grid(row=0, column=9, sticky=N+S+E+W)

def lookup():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {"start": "1", "limit": "5000", "convert": "AUD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "API-KEY-GOES-HERE",
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)

        # Check if the response is successful
        if response.status_code == 200:
            try:
                api_data = response.json()

                # Extract the 'data' list from the API response
                data_list = api_data.get("data", [])

                portfolio_profit_loss = 0
                print("=" * 60)

                # my portfolio
                my_portfolio = [
                    {"sym": "BTC", "amount_owned": 0.18578128, "price_paid_per": 107110.03},
                ]

                portfolio_profit_loss = 0
                total_current_value = 0
                row_count = 1
                pie = []
                pie_size = []
                for x in data_list:
                    for coin in my_portfolio:
                        if coin["sym"] == x["symbol"]:

                          # do some math
                            total_paid = float(coin["amount_owned"]) * float(coin["price_paid_per"])
                            current_value = float(coin["amount_owned"]) * float(x["quote"]["AUD"]["price"])
                            profit_loss = current_value - total_paid
                            portfolio_profit_loss += profit_loss
                            total_current_value += current_value

                            pie.append(x["name"])
                            pie_size.append(coin["amount_owned"])


                            # print(x["name"])
                            # print(f" Current Price (AUD): ${x['quote']['AUD']['price']:.2f}")
                            # print(" Profit/Loss per coin: ${0:.2f}".format(float(profit_loss_per_coin)))
                            # print(" Rank:", x["cmc_rank"])
                            print(" Total Paid: ${0:.2f}".format(float(total_paid)))
                            # print(" Current Value: ${0:.2f}".format(float(current_value)))
                            # print(" Profit/Loss: ${0:.2f}".format(float(profit_loss)))

                            # print("=" * 60)

                            name = Label(root, text=x["name"], bg="white")
                            name.grid(row=row_count, column=0, sticky=N+S+E+W)

                            current_price = Label(root, text=f"${x['quote']['AUD']['price']:.2f}", bg="white")
                            current_price.grid(row=row_count, column=1, sticky=N+S+E+W)

                            price_paid = Label(root, text=f"${coin['price_paid_per']:.2f}", bg="silver")
                            price_paid.grid(row=row_count, column=2, sticky=N+S+E+W)

                            balance = Label(root, text=float(coin["amount_owned"]), bg="white")
                            balance.grid(row=row_count, column=3, sticky=N+S+E+W)

                            one_hr_change = Label(root, text=f"{x['quote']['AUD']['percent_change_1h']:.2f}%", bg="silver", fg=red_green(float(x['quote']['AUD']['percent_change_1h'])))
                            one_hr_change.grid(row=row_count, column=4, sticky=N+S+E+W)

                            tf_hr_change = Label(root, text=f"{x['quote']['AUD']['percent_change_24h']:.2f}%", bg="white", fg=red_green(float(x['quote']['AUD']['percent_change_24h'])))
                            tf_hr_change.grid(row=row_count, column=5, sticky=N+S+E+W)

                            seven_day_change = Label(root, text=f"{x['quote']['AUD']['percent_change_7d']:.2f}%", bg="silver", fg=red_green(float(x['quote']['AUD']['percent_change_7d'])))
                            seven_day_change.grid(row=row_count, column=6, sticky=N+S+E+W)

                            profit_loss_total = Label(root, text="${0:.2f}".format(float(profit_loss)), bg="silver", fg=red_green(float(profit_loss)))
                            profit_loss_total.grid(row=row_count, column=7, sticky=N+S+E+W)

                            current_value_label = Label(root, text="${0:.2f}".format(float(current_value)), bg="white")
                            current_value_label.grid(row=row_count, column=8, sticky=N+S+E+W)

                            total_paid = Label(root, text="${0:.2f}".format(float(total_paid)), bg="silver")
                            total_paid.grid(row=row_count, column=9, sticky=N+S+E+W)

                            row_count += 1
                portfolio_profits = Label(root, text="P/L: ${0:.2f}".format(float(portfolio_profit_loss)), font="Verdana 8 bold", fg=red_green(float(portfolio_profit_loss)))
                portfolio_profits.grid(row=row_count, column=0, sticky=W, padx=10, pady=10)
                
                root.title("Crypto Currency Portfolio - P/L: ${0:.2f}".format(float(profit_loss)))
                data_list = ""
                update_button = Button(root, text="Update Prices", command=lookup)
                update_button.grid(row=row_count, column=9, sticky=E+S, padx=10, pady=10)



                def graph(pie, pie_size):
                  # Defining data for the chart
                  labels = pie
                  sizes = pie_size
                  colors = ['gold']
                  explode = (1)  # explode 1st slice

                  # Plotting the chart
                  plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
                  plt.axis('equal')

                  plt.show()
                  

                graph_button = Button(root, text="Pie Chart", command=lambda: graph(pie, pie_size))
                graph_button.grid(row=row_count, column=8, sticky=E+S, padx=10, pady=10)

            except json.JSONDecodeError as json_error:
                print(f"JSON decoding error: {json_error}")
                print("Response text:")
                print(response.text)

        else:
            print(f"Error: Status Code {response.status_code}")

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"Connection error: {e}")

lookup()
root.mainloop()
