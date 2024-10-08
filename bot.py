import ccxt
import time

# Configura las credenciales de Binance
api_key = 'API_KEY'
api_secret = 'API_SECRET'

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

# Define los parámetros del bot
symbol = 'BTC/USDT'
investment_amount = 0.01  # USDT
price_drop_percentage = 1.2  # % de caída para comprar, ajustado para obtener ganancia
price_increase_percentage = 1.3  # % de subida para vender, ajustado para obtener ganancia

# Obten el precio inicial
initial_price = exchange.fetch_ticker(symbol)['last']

# Función para realizar intercambios
def perform_trade():
    global initial_price
    current_price = exchange.fetch_ticker(symbol)['last']
    percentage_change = ((current_price - initial_price) / initial_price) * 100

    if percentage_change <= -price_drop_percentage:
        # Intercambia USDT por 1000sats
        order = exchange.create_market_buy_order(symbol, investment_amount / current_price)
        print(f'Compra ejecutada: {order}')
        initial_price = current_price  # Actualiza el precio de referencia

    elif percentage_change >= price_increase_percentage:
        # Intercambia 1000sats por USDT
        amount_to_sell = investment_amount / initial_price
        order = exchange.create_market_sell_order(symbol, amount_to_sell)
        print(f'Venta ejecutada: {order}')
        initial_price = current_price  # Actualiza el precio de referencia

# Loop principal del bot
while True:
    perform_trade()
    time.sleep(60)  # Espera 1 minuto antes de verificar el precio nuevamente
