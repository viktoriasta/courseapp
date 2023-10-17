import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from flask import Flask, request, jsonify

# Отримайте доступ до Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', scope)
gc = gspread.authorize(credentials)
spreadsheet_key = 'analog-campus-402318-167ad4c7367e.json'  # Вставте ключ вашого Google Sheets

# Отримайте доступ до API для отримання курсу валют
API_URL = 'https://api.monobank.ua/docs/#tag/Publichni-dani:~:text=https%3A//api.monobank.ua/bank/currency'  # Замініть на URL API для отримання курсу валют

app = Flask(currency_name)

@app.route('/update_currency', methods=['POST'])
def update_currency():
    update_from = request.form.get('update_from', '2023-10-01')
    update_to = request.form.get('update_to', '2023-10-16')

    # Отримати курси валют за вказаний період
    params = {'from': update_from, 'to': update_to}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        currency_data = response.json()
        worksheet = gc.open_by_key(spreadsheet_key).sheet1

        # Оновіть дані в Google Sheets
        for item in currency_data:
            worksheet.append_row([item['date'], item['currency'], item['rate']])

        return 'Курси валют оновлені успішно.'
    else:
        return 'Не вдалося оновити курси валют.', 500

if __name__ == '__main__':
    app.run()
