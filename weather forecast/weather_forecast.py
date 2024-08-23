import customtkinter
import tkinter as tk
import requests
import json
from datetime import datetime
from customtkinter import filedialog
import pandas as pd
from PIL import Image, ImageTk
from collections import defaultdict, Counter
import sys
import os

# Definition of path function to be able to import pictures in case of both the application and the .py script inside VS code
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS # Temporary folder created while the .exe app is running
    except Exception:
        base_path = os.path.abspath(".") # Active folder where the .py file is located

    return os.path.join(base_path, relative_path)

#------------------------------------------------------------------------------------------------------------------------- APP GUI -------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.title("Weather Forecast Application")
        self.geometry(f"540x900")
        self.minsize(540, 900)
        self.bind("<1>", lambda event: event.widget.focus_set())
        self.resizable(False, False)
        self.main = Main(self)      

class Main:
    def __init__(self, parent):
        self.parent = parent
        self.user_text = tk.StringVar()
        
        # Background, font settings etc.
        self.background_color = "lightcyan"

        # Main widget settings
        self.mainframe = customtkinter.CTkFrame(self.parent, fg_color = self.background_color)
        self.mainframe.pack(fill = "both", expand = "True")
        
        self.image = Image.open(resource_path("assets//weather.png"))
        self.image = self.image.resize((150, 150), Image.LANCZOS)
        self.image_photo = ImageTk.PhotoImage(self.image)
        
        self.image_label = tk.Label(self.mainframe, image = self.image_photo, text = "", bg = self.background_color)
        self.image_label.grid(row = 0, column = 0, pady = (0, 0))
        
        self.title = customtkinter.CTkLabel(self.mainframe, text="Weather Forecast Application", font=("Calibri", 20), width=50, bg_color = self.background_color)
        self.title.grid(row=0, column=0, sticky="nsew", padx=143, pady=(150, 0))

        self.underline = customtkinter.CTkFrame(self.mainframe, height=2, fg_color="lightgrey", width = 250)
        self.underline.grid(row = 1, column = 0, padx = 0, pady = (10, 0))
        
        self.user_input = customtkinter.CTkEntry(self.mainframe, width = 200, font = ("Calibri", 14), border_width = 2, corner_radius = 10, fg_color = "lightgrey", placeholder_text_color = "darkgrey", textvariable=self.user_text, placeholder_text = "Enter city name")
        self.user_input.grid(row = 2, column = 0, padx = (0, 50), pady = 0)
        
        self.magnify_icon = Image.open(resource_path("assets//magnify_icon.png"))
        self.magnify_icon = self.magnify_icon.resize((20, 20), Image.LANCZOS) 
        self.magnify_icon_photo = customtkinter.CTkImage(self.magnify_icon)
        
        self.magnify_button = customtkinter.CTkButton(self.mainframe, image = self.magnify_icon_photo, text = "", command = self.search, width = 20, height = 20, corner_radius = 10, fg_color = "lightgrey", hover_color = "darkgrey")
        self.magnify_button.grid(row = 2, column = 0, padx = (0, 145), pady = 20, sticky = "e")     

        self.underline2 = customtkinter.CTkFrame(self.mainframe, height = 2, fg_color = "lightgrey", width = 450)
        self.underline2.grid(row = 2, column = 0, padx = 0, pady = (70, 10))
    
    # Definition of search function
    def search(self):
        self.city_name = self.user_text.get()
        self.fetching_weather_data(self.city_name)
    
    # Definition of time update function
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M")
        self.city.configure(text = f"{current_time}")
        self.city.after(1000, self.update_time)
    
    # Definition of data fetching function
    def fetching_weather_data(self, city):
        
        # Load and resize weather icons
        self.weather_pictures = {
            "clear sky": ImageTk.PhotoImage(Image.open(resource_path("assets//clear sky.png")).resize((100, 100), Image.LANCZOS)),
            "few clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//small cloudy.png")).resize((100, 100), Image.LANCZOS)),
            "scattered clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//cloudy.png")).resize((100, 100), Image.LANCZOS)),
            "broken clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//cloudy2.png")).resize((100, 100), Image.LANCZOS)),
            "overcast clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//big cloudy.png")).resize((100, 100), Image.LANCZOS)),
            "shower rain": ImageTk.PhotoImage(Image.open(resource_path("assets//shower rain.png")).resize((100, 100), Image.LANCZOS)),
            "rain": ImageTk.PhotoImage(Image.open(resource_path("assets//rain.png")).resize((100, 100), Image.LANCZOS)),
            "moderate rain": ImageTk.PhotoImage(Image.open(resource_path("assets//moderate rain.png")).resize((100, 100), Image.LANCZOS)),
            "light rain": ImageTk.PhotoImage(Image.open(resource_path("assets//light rain.png")).resize((100, 100), Image.LANCZOS)),
            "light intensity shower rain": ImageTk.PhotoImage(Image.open(resource_path("assets//light intensity shower rain.png")).resize((100, 100), Image.LANCZOS)),
            "thunderstorm": ImageTk.PhotoImage(Image.open(resource_path("assets//thunderstorm.png")).resize((100, 100), Image.LANCZOS)),
            "snow": ImageTk.PhotoImage(Image.open(resource_path("assets//snow.png")).resize((100, 100), Image.LANCZOS)),
            "mist": ImageTk.PhotoImage(Image.open(resource_path("assets//mist.png")).resize((100, 100), Image.LANCZOS)),
            "smoke": ImageTk.PhotoImage(Image.open(resource_path("assets//smoke.png")).resize((100, 100), Image.LANCZOS)),
            "haze": ImageTk.PhotoImage(Image.open(resource_path("assets//haze.png")).resize((100, 100), Image.LANCZOS)),
            "dust": ImageTk.PhotoImage(Image.open(resource_path("assets//dust.png")).resize((100, 100), Image.LANCZOS)),
            "fog": ImageTk.PhotoImage(Image.open(resource_path("assets//fog.png")).resize((100, 100), Image.LANCZOS)),
            "sand": ImageTk.PhotoImage(Image.open(resource_path("assets//sand.png")).resize((100, 100), Image.LANCZOS)),
            "volcanic ash": ImageTk.PhotoImage(Image.open(resource_path("assets//volcanic ash.png")).resize((100, 100), Image.LANCZOS)),
            "squalls": ImageTk.PhotoImage(Image.open(resource_path("assets//squalls.png")).resize((100, 100), Image.LANCZOS)),
            "tornado": ImageTk.PhotoImage(Image.open(resource_path("assets//tornado.png")).resize((100, 100), Image.LANCZOS))
        }
        
        # Load and resize weather icons
        self.weather_pictures_small = {
            "clear sky": ImageTk.PhotoImage(Image.open(resource_path("assets//clear sky.png")).resize((50, 50), Image.LANCZOS)),
            "few clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//small cloudy.png")).resize((50, 50), Image.LANCZOS)),
            "scattered clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//cloudy.png")).resize((50, 50), Image.LANCZOS)),
            "broken clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//cloudy2.png")).resize((50, 50), Image.LANCZOS)),
            "overcast clouds": ImageTk.PhotoImage(Image.open(resource_path("assets//big cloudy.png")).resize((50, 50), Image.LANCZOS)),
            "shower rain": ImageTk.PhotoImage(Image.open(resource_path("assets//shower rain.png")).resize((50, 50), Image.LANCZOS)),
            "rain": ImageTk.PhotoImage(Image.open(resource_path("assets//rain.png")).resize((50, 50), Image.LANCZOS)),
            "moderate rain": ImageTk.PhotoImage(Image.open(resource_path("assets//moderate rain.png")).resize((50, 50), Image.LANCZOS)),
            "light rain": ImageTk.PhotoImage(Image.open(resource_path("assets//light rain.png")).resize((50, 50), Image.LANCZOS)),
            "light intensity shower rain": ImageTk.PhotoImage(Image.open(resource_path("assets//light intensity shower rain.png")).resize((50, 50), Image.LANCZOS)),
            "thunderstorm": ImageTk.PhotoImage(Image.open(resource_path("assets//thunderstorm.png")).resize((50, 50), Image.LANCZOS)),
            "snow": ImageTk.PhotoImage(Image.open(resource_path("assets//snow.png")).resize((50, 50), Image.LANCZOS)),
            "mist": ImageTk.PhotoImage(Image.open(resource_path("assets//mist.png")).resize((50, 50), Image.LANCZOS)),
            "smoke": ImageTk.PhotoImage(Image.open(resource_path("assets//smoke.png")).resize((50, 50), Image.LANCZOS)),
            "haze": ImageTk.PhotoImage(Image.open(resource_path("assets//haze.png")).resize((50, 50), Image.LANCZOS)),
            "dust": ImageTk.PhotoImage(Image.open(resource_path("assets//dust.png")).resize((50, 50), Image.LANCZOS)),
            "fog": ImageTk.PhotoImage(Image.open(resource_path("assets//fog.png")).resize((50, 50), Image.LANCZOS)),
            "sand": ImageTk.PhotoImage(Image.open(resource_path("assets//sand.png")).resize((50, 50), Image.LANCZOS)),
            "volcanic ash": ImageTk.PhotoImage(Image.open(resource_path("assets//volcanic ash.png")).resize((50, 50), Image.LANCZOS)),
            "squalls": ImageTk.PhotoImage(Image.open(resource_path("assets//squalls.png")).resize((50, 50), Image.LANCZOS)),
            "tornado": ImageTk.PhotoImage(Image.open(resource_path("assets//tornado.png")).resize((50, 50), Image.LANCZOS))
        }
        
        # Load and resize weather icons
        self.data_icons = {
            "sunrise": ImageTk.PhotoImage(Image.open(resource_path("assets//sunrise.png")).resize((25, 25), Image.LANCZOS)),
            "sunset": ImageTk.PhotoImage(Image.open(resource_path("assets//sunset.png")).resize((25, 25), Image.LANCZOS)),
            "date": ImageTk.PhotoImage(Image.open(resource_path("assets//date.png")).resize((25, 25), Image.LANCZOS)),
            "pressure": ImageTk.PhotoImage(Image.open(resource_path("assets//pressure.png")).resize((20, 20), Image.LANCZOS)),
            "humidity": ImageTk.PhotoImage(Image.open(resource_path("assets//humidity.png")).resize((20, 20), Image.LANCZOS)),
            "wind speed": ImageTk.PhotoImage(Image.open(resource_path("assets//wind speed.png")).resize((25, 25), Image.LANCZOS))
        }
        
        # Definition of month names
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        # Main part of the code
        if city:
            # Getting today weather data from Weather Open
            api_key = "7e98bcf1d9762dcbdff6ca6fcb7df04f"
            weather_url = "http://api.openweathermap.org/data/2.5/weather?"
            url = f"{weather_url}q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            weather_data = response.json()
            
            # Getting next days weather data from Weather Open
            weather_url2 = "http://api.openweathermap.org/data/2.5/forecast?"
            url2 = f"{weather_url2}q={city}&appid={api_key}&units=metric"
            response2 = requests.get(url2)
            weather_data2 = response2.json()
            
            # 200 means successful data request
            if int(weather_data["cod"]) == 200 and int(weather_data2["cod"]) == 200:
                
                # Current weather information
                today_date = datetime.fromtimestamp(weather_data["dt"]).strftime("%d").replace("0", "")
                month_num = datetime.fromtimestamp(weather_data["dt"]).strftime("%m").replace("0", "")
                day_name = datetime.fromtimestamp(weather_data["dt"]).strftime("%A")
                temperature = int(weather_data["main"]["temp"])
                temperature_max = int(weather_data["main"]["temp_max"])
                temperature_min = int(weather_data["main"]["temp_min"])
                temperature_feels = int(weather_data["main"]["feels_like"])
                pressure = weather_data["main"]["pressure"]
                humidity = weather_data["main"]["humidity"]
                weather_description = weather_data["weather"][0]["description"]
                wind_speed = weather_data["wind"]["speed"]
                sunrise_time = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%H:%M")
                sunset_time = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%H:%M")                                  
                
                # Upcoming weather information
                forecast_list = weather_data2["list"]
                today_date2 = datetime.now().strftime('%Y-%m-%d')
                
                # Old information removal
                for widget in self.mainframe.grid_slaves():
                    if int(widget.grid_info()["row"]) >= 3:
                        widget.destroy()

                # Main current weather information
                self.city = customtkinter.CTkLabel(self.mainframe, text = f"{city.title()}, {day_name}", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Calibri", 25))
                self.city.grid(row = 3, column = 0, padx = (0, 0), pady = (5, 0), sticky = "n")
            
                if weather_description:
                    self.icon = tk.Label(self.mainframe, image = self.weather_pictures[weather_description], text = "", bg = self.background_color)
                    self.icon.grid(row = 3, column = 0, padx = (85, 10), pady = (50, 0), sticky = "nw")

                self.temperature = customtkinter.CTkLabel(self.mainframe, text = f"{temperature} °C", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 30))
                self.temperature.grid(row = 3, column = 0, padx = (85, 10), pady = (165, 0), sticky = "nw")
                
                self.weather_description = customtkinter.CTkLabel(self.mainframe, text = f"{weather_description}", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 10))
                self.weather_description.grid(row = 3, column = 0, padx = (85, 10), pady = (200, 0), sticky = "nw")
                
                self.temperature_feels = customtkinter.CTkLabel(self.mainframe, text = f"feels like {temperature_feels} °C (L: {temperature_min} °C / H: {temperature_max} °C)", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 10))
                self.temperature_feels.grid(row = 3, column = 0, padx = (65, 10), pady = (215, 0), sticky = "nw")
                
                # Other current weather information
                self.date_icon = tk.Label(self.mainframe, image = self.data_icons["date"], text = "", bg = self.background_color)
                self.date_icon.grid(row = 3, column = 0, padx = (10, 150), pady = (50 + 5, 0), sticky = "ne")
                self.date = customtkinter.CTkLabel(self.mainframe, text = f"{month_names[int(month_num) - 1]} {today_date}", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 15))
                self.date.grid(row = 3, column = 0, padx = (10, 50), pady = (53 + 5, 0), sticky = "ne")
                
                self.sunrise_icon = tk.Label(self.mainframe, image = self.data_icons["sunrise"], text = "", bg = self.background_color)
                self.sunrise_icon.grid(row = 3, column = 0, padx = (10, 150), pady = (80 + 5, 0), sticky = "ne")
                self.sunrise = customtkinter.CTkLabel(self.mainframe, text = sunrise_time, text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 15))
                self.sunrise.grid(row = 3, column = 0, padx = (10, 50), pady = (83 + 5, 0), sticky = "ne")
                
                self.sunset_icon = tk.Label(self.mainframe, image = self.data_icons["sunset"], text = "", bg = self.background_color)
                self.sunset_icon.grid(row = 3, column = 0, padx = (10, 150), pady = (110 + 5, 0), sticky = "ne")
                self.sunset = customtkinter.CTkLabel(self.mainframe, text = sunset_time, text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 15))
                self.sunset.grid(row = 3, column = 0, padx = (10, 50), pady = (113 + 5, 0), sticky = "ne")    
                
                self.pressure_icon = tk.Label(self.mainframe, image = self.data_icons["pressure"], text = "", bg = self.background_color)
                self.pressure_icon.grid(row = 3, column = 0, padx = (10, 152), pady = (140 + 5, 0), sticky = "ne")
                self.pressure = customtkinter.CTkLabel(self.mainframe, text = f"{pressure} hPa", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 15))
                self.pressure.grid(row = 3, column = 0, padx = (10, 50), pady = (143 + 5, 0), sticky = "ne")
                
                self.humidity_icon = tk.Label(self.mainframe, image = self.data_icons["humidity"], text = "", bg = self.background_color)
                self.humidity_icon.grid(row = 3, column = 0, padx = (10, 150), pady = (170 + 5, 0), sticky = "ne")
                self.humidity = customtkinter.CTkLabel(self.mainframe, text = f"{humidity} %", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 15))
                self.humidity.grid(row = 3, column = 0, padx = (10, 50), pady = (173 + 5, 0), sticky = "ne")
                
                self.wind_speed_icon = tk.Label(self.mainframe, image = self.data_icons["wind speed"], text = "", bg = self.background_color)
                self.wind_speed_icon.grid(row = 3, column = 0, padx = (10, 150), pady = (200 + 5, 0), sticky = "ne")
                self.wind_speed = customtkinter.CTkLabel(self.mainframe, text = f"{wind_speed} m/s", text_color = "black", fg_color = self.background_color, width = 100, height = 20, font = ("Nirmala UI", 15))
                self.wind_speed.grid(row = 3, column = 0, padx = (10, 50), pady = (203 + 5, 0), sticky = "ne")
                
                # Today upcoming weather information
                self.weather_labels = []
                self.weather_icons = []
                self.weather_labels2 = []
                self.temp_labels = []
                i = 0
                counter = 0
                
                for forecast in forecast_list:
                    forecast_time = forecast['dt_txt']
                    if forecast_time.startswith(today_date2):
                        counter += 1
                for forecast in forecast_list:
                    forecast_time = forecast['dt_txt']
                    if forecast_time.startswith(today_date2):
                        
                        # Window design handling
                        label = customtkinter.CTkLabel(self.mainframe, text = f"{datetime.strptime(forecast_time, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')}", text_color = "black", fg_color = self.background_color, width = 80, height = 20, font = ("Nirmala UI", 15))
                        self.weather_labels.append(label)
                        icon = tk.Label(self.mainframe, image = self.weather_pictures_small[forecast['weather'][0]['description']], text = "", bg = self.background_color)
                        self.weather_icons.append(icon)
                        temp_label = customtkinter.CTkLabel(self.mainframe, text = f"{int(forecast['main']['temp'])} °C", text_color = "black", fg_color = self.background_color, width = 80, height = 10, font = ("Nirmala UI", 15))
                        self.temp_labels.append(temp_label)
                        description_label = customtkinter.CTkLabel(self.mainframe, text = f"{forecast['weather'][0]['description']}", text_color = "black", fg_color = self.background_color, width = 80, height = 10, font = ("Nirmala UI", 10))
                        self.weather_labels2.append(description_label)

                        if counter == 6:
                            label.grid(row = 4, column = 0, padx = (32 + i, 10), pady = (40, 0), sticky = "w")
                            icon.grid(row = 5, column = 0, padx = (45 + i, 10), pady = (10, 0), sticky = "w")
                            temp_label.grid(row = 6, column = 0, padx = (32 + i, 10), pady = (10, 0), sticky = "w")
                            description_label.grid(row = 7, column = 0, padx = (32 + i, 10), pady = (0, 0), sticky = "w")
                            i += 77 

                        if counter == 5:                            
                            label.grid(row = 4, column = 0, padx = (50 + i, 10), pady = (40, 0), sticky = "w")
                            icon.grid(row = 5, column = 0, padx = (63 + i, 10), pady = (10, 0), sticky = "w")
                            temp_label.grid(row = 6, column = 0, padx = (50 + i, 10), pady = (10, 0), sticky = "w")
                            description_label.grid(row = 7, column = 0, padx = (50 + i, 10), pady = (0, 0), sticky = "w")
                            i += 89 
                            
                        if counter == 4:                           
                            label.grid(row = 4, column = 0, padx = (62 + i, 10), pady = (40, 0), sticky = "w")
                            icon.grid(row = 5, column = 0, padx = (75 + i, 10), pady = (10, 0), sticky = "w")
                            temp_label.grid(row = 6, column = 0, padx = (62 + i, 10), pady = (10, 0), sticky = "w")
                            description_label.grid(row = 7, column = 0, padx = (62 + i, 10), pady = (0, 0), sticky = "w")
                            i += 110  
                             
                        if counter == 3:                           
                            label.grid(row = 4, column = 0, padx = (80 + i, 10), pady = (40, 0), sticky = "w")
                            icon.grid(row = 5, column = 0, padx = (93 + i, 10), pady = (10, 0), sticky = "w")
                            temp_label.grid(row = 6, column = 0, padx = (80 + i, 10), pady = (10, 0), sticky = "w")
                            description_label.grid(row = 7, column = 0, padx = (80 + i, 10), pady = (0, 0), sticky = "w")
                            i += 135
                            
                        if counter == 2:                           
                            label.grid(row = 4, column = 0, padx = (160 + i, 10), pady = (40, 0), sticky = "w")
                            icon.grid(row = 5, column = 0, padx = (173 + i, 10), pady = (10, 0), sticky = "w")
                            temp_label.grid(row = 6, column = 0, padx = (160 + i, 10), pady = (10, 0), sticky = "w")
                            description_label.grid(row = 7, column = 0, padx = (160 + i, 10), pady = (0, 0), sticky = "w")
                            i += 135   
                            
                        if counter == 1:                           
                            label.grid(row = 4, column = 0, padx = (213 + i, 10), pady = (40, 0), sticky = "w")
                            icon.grid(row = 5, column = 0, padx = (28 + i, 10), pady = (10, 0), sticky = "w")
                            temp_label.grid(row = 6, column = 0, padx = (200 + i, 10), pady = (10, 0), sticky = "w")
                            description_label.grid(row = 7, column = 0, padx = (200 + i, 10), pady = (0, 0), sticky = "w")
                            i += 60 
                    
                self.underline3 = customtkinter.CTkFrame(self.mainframe, height = 2, fg_color = "lightgrey", width = 450)
                self.underline3.grid(row = 8, column = 0, padx = 0, pady = (20, 10)) 
                
                # Next days upcoming weather information
                daily_data = defaultdict(list)
                
                for forecast in forecast_list:
                    forecast_date = forecast['dt_txt'].split()[0]
                    daily_data[forecast_date].append(forecast)
                    
                self.next_weather_labels = []
                self.next_weather_icons = []
                self.next_weather_labels2 = []
                self.next_temp_labels = []
                counter_next = 1
                i = 0
                
                for date, data in daily_data.items():
                    if counter_next < 5:
                        if date == today_date2:
                            continue  
                        
                        next_day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
                        max_temp = max(item['main']['temp'] for item in data)
                        descriptions = [item['weather'][0]['description'] for item in data]
                        most_common_description = Counter(descriptions).most_common(1)[0][0]        

                        label_next = customtkinter.CTkLabel(self.mainframe, text = f"{next_day_name}", text_color = "black", fg_color = self.background_color, width = 80, height = 20, font = ("Nirmala UI", 15))
                        label_next.grid(row = 9, column = 0, padx = (63 + i, 10), pady = (25, 0), sticky = "w")
                        self.next_weather_labels.append(label_next)
                        
                        icon_next = tk.Label(self.mainframe, image = self.weather_pictures_small[most_common_description], text = "", bg = self.background_color)
                        icon_next.grid(row = 10, column = 0, padx = (76 + i, 10), pady = (10, 0), sticky = "w")
                        self.next_weather_icons.append(icon_next)
                        
                        max_temp_next = customtkinter.CTkLabel(self.mainframe, text = f"{int(max_temp)} °C", text_color = "black", fg_color = self.background_color, width = 80, height = 10, font = ("Nirmala UI", 15))
                        max_temp_next.grid(row = 11, column = 0, padx = (63 + i, 10), pady = (10, 0), sticky = "w")
                        self.next_temp_labels.append(max_temp_next)
                        
                        most_common_description_label = customtkinter.CTkLabel(self.mainframe, text = f"{most_common_description}", text_color = "black", fg_color = self.background_color, width = 80, height = 10, font = ("Nirmala UI", 10))
                        most_common_description_label.grid(row = 12, column = 0, padx = (63 + i, 10), pady = (0, 0), sticky = "w")
                        self.next_weather_labels2.append(most_common_description_label)
                    
                        i += 110  
                        counter_next += 1                   
            else:
                # Old information removal
                for widget in self.mainframe.grid_slaves():
                    if int(widget.grid_info()["row"]) >= 3:
                        widget.destroy()
                
                # Bad input handling
                bad_input = ["Either you typed the city\n" 
                             "name wrong or this city is\n" 
                             "not available in the forecast,\n" 
                             "try again."]
                self.bad_input = customtkinter.CTkLabel(self.mainframe, text = bad_input[0], text_color = "red", fg_color = self.background_color, width = 100, height = 20, font = ("Calibri", 20))
                self.bad_input.grid(row = 3, column = 0, padx = (0, 0), pady = (20, 0), sticky = "n")        

if __name__ == "__main__":
    app = App()
    app.mainloop()