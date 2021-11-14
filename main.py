import requests
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QMovie

from PIL import Image

import json
api_key='c93136bc6728999e61f7ee420d29c72d'

class Main_window(QMainWindow):
    def __init__(self,error=0):
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load('main_window.ui',None)
        self.ui.show()
        self.ui.btn_next.clicked.connect(self.weather)
        self.ui.text_city.returnPressed.connect(self.weather)
        if error==1:
            self.error()
    def weather(self):
        self.ui=Show_weather(self.ui.text_city.text())
    def error(self):
        self.ui.error_message.setText('The desired city was not found, please try again')

class Show_weather(QWidget):
    def __init__(self,city):
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load('show_weather.ui',None)
        self.ui.show()
        self.city_name=city
        self.ui.setWindowTitle(f'Climate of {self.city_name}')
        self.ui.btn_back.clicked.connect(self.back)
        self.loading()



    def loading(self):
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city_name}&units=metric&appid={api_key}'
            response = requests.get(url)
            dic = response.json()
            self.info_weather = [None for i in range(8)]
            self.info_weather[0] = dic["name"]
            self.info_weather[1] = dic['weather'][0]['icon']
            self.info_weather[2] = dic['timezone']
            self.info_weather[3] = dic['weather'][0]['description']
            self.info_weather[4] = dic["wind"]['speed']
            self.info_weather[5] = dic['main']['temp']
            self.info_weather[6] = dic['main']['humidity']
            self.info_weather[7] = dic['main']['pressure']

            self.url_icon = f"http://openweathermap.org/img/wn/{self.info_weather[1]}.png"

            img = requests.get(self.url_icon).content
            with open("images/icon-weather.png", "wb") as file:
                file.write(img)
            return self.show_info()
        except:
            self.error_message()



    def show_info(self):
        self.ui.city_name.setText(self.info_weather[0])
        self.ui.timezone.setText(f'timezone: {self.info_weather[2]}')
        self.ui.icon_weather.setPixmap(QtGui.QPixmap('images/icon-weather.png'))
        self.ui.icon_weather_main.setPixmap(QtGui.QPixmap('images/icon-weather.png'))
        self.ui.weather_temp.setText(f"{self.info_weather[5]} °C")
        weather_row_number=[ None for i in range(6)]
        for i in range(3,8,1):
            weather_row_number[i-3]=QLabel()
            weather_row_number[i-3].setText(str(self.info_weather[i]))
            weather_row_number[i-3].setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.ui.gridLayout.addWidget(weather_row_number[i-3], 2, i-3)
    def back(self):
        self.ui=Main_window()

    def error_message(self):
        self.ui=Main_window(1)

app=QApplication([])
window=Main_window()
app.exec()