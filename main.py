from machine import Pin, SPI
import st7789
import vga2_16x32 as font_l
import vga2_8x16 as font_s
import vga2_bold_16x16 as font_bold_l
import time
import urequests

tft_spaces = {
    "top" : 1,
    "bot" : 1,
    "text_s" : 3,
    "text_l" : 6
}
list1 = ["status", "ads_percentage_today", "dns_queries_today", "ads_blocked_today"]
dict1 = {
    "dns_queries_today" : "DNS ",
    "ads_blocked_today" : "ADs ",
    "ads_percentage_today" : "ADs%:",
    "status" : "STATUS:"
}
dict2 = {
    "dns_queries_today" : "QUERIES:",
    "ads_blocked_today" : "BLOCKED:",
    "ads_percentage_today" : "% :"
}
dict_color = {
    "dns_queries_today" : st7789.BLUE,
    "ads_blocked_today" : st7789.RED,
}
# change IP to your Pi's IP
URL = 'http://192.168.1.10/admin/api.php?summary'

def main():
    tft = st7789.ST7789(
        SPI(1, baudrate=30000000, sck=Pin(18), mosi=Pin(19)),
        135,
        240,
        reset=Pin(23, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        dc=Pin(16, Pin.OUT),
        backlight=Pin(4, Pin.OUT),
        rotation=1)
    tft.init()
    stay = True
    while stay:
        try:    
            info = urequests.get(url=URL)
            stay = False
        except:
            pass
    check = [str(info.json()["status"]),
             str(info.json()["ads_percentage_today"]), 
             str(info.json()["dns_queries_today"]),
             str(info.json()["ads_blocked_today"])]
    
    tft.text(font_bold_l, 'Pi Hole', int(tft.width()*0.5 - 8*font_bold_l.WIDTH*0.5 - 30), 1, st7789.RED)
    # STATUS
    tft.text(font_l, dict1["status"], 2, tft_spaces["top"]+tft_spaces["text_l"]+9)
    # STATUS value
    if check[0] == 'enabled':
        tft.text(font_l, check[0], int(tft.width()*0.5 + 54 - len(check[0])*font_l.WIDTH*0.5),
                                        tft_spaces["top"]+tft_spaces["text_l"]+9, st7789.GREEN)
    else:
        tft.text(font_l, check[0], int(tft.width()*0.5 + 54 - len(check[0])*font_l.WIDTH*0.5),
                                        tft_spaces["top"]+tft_spaces["text_l"]+9, st7789.RED)
    # ADs %
    tft.text(font_l, dict1["ads_percentage_today"], 2,
                                        tft_spaces["top"]+font_l.HEIGHT+tft_spaces["text_l"]+6)
    # ADs % value
    tft.text(font_l, check[1], int(tft.width()*0.5 + 40 - len(check[1])*font_l.WIDTH*0.5),
                                        tft_spaces["top"]+font_l.HEIGHT+tft_spaces["text_l"]+6)
    # DNS QUERIES
    tft.text(font_l, dict1["dns_queries_today"], 2,
                                        tft_spaces["top"]+2*font_l.HEIGHT+tft_spaces["text_l"]+3)
    tft.text(font_s, dict2["dns_queries_today"], 55,
                                        tft_spaces["top"]+2*font_l.HEIGHT+tft_spaces["text_l"]+16)
    # DNS QUERIES value
    tft.text(font_l, check[2], int(tft.width()*0.5 + 48 - len(check[2])*font_l.WIDTH*0.5),
                                        tft_spaces["top"]+2*font_l.HEIGHT+tft_spaces["text_l"]+3)
    # ADs BLOCKED
    tft.text(font_l, dict1["ads_blocked_today"], 2,
                                        tft_spaces["top"]+3*font_l.HEIGHT+tft_spaces["text_l"])
    tft.text(font_s, dict2["ads_blocked_today"], 55,
                                        tft_spaces["top"]+3*font_l.HEIGHT+tft_spaces["text_l"]+13)
    # ADs BLOCKED value
    tft.text(font_l, check[3], int(tft.width()*0.5 + 48 - len(check[3])*font_l.WIDTH*0.5),
                                        tft_spaces["top"]+3*font_l.HEIGHT+tft_spaces["text_l"])
    tft.rect(int(tft.width()*0.5 - 8*font_bold_l.WIDTH*0.5)-35, -1, int(7*font_bold_l.WIDTH+10), 19, st7789.BLUE) 
    heartbeat_sent = False
    while True:
        stay = True
        while stay:
            try:    
                info = urequests.get(url=URL)
                stay = False
            except:
                pass
        y = tft_spaces["top"]+tft_spaces["text_l"]+9
        for z, i in enumerate(list1):
            if check[z] != str(info.json()[i]):
                if z == 0:
                    w = 52
                elif z == 1:
                    w = 40
                else:
                    w = 48
                check[z] = str(info.json()[i])
                x = int(tft.width()*0.5 + w - len(check[z])*font_l.WIDTH*0.5)  
                if z == 0:
                    tft.fill_rect(110, 16, 130, font_l.HEIGHT, st7789.BLACK)
                    if check[z] == 'enabled':
                        tft.text(font_l, check[z], x, y, st7789.GREEN)
                    else:
                        tft.text(font_l, check[z], x, y, st7789.RED)
                    tft.rect(int(tft.width()*0.5 - 8*font_bold_l.WIDTH*0.5)-5, -1, int(7*font_bold_l.WIDTH+10), 19, st7789.MAGENTA) 
                elif z == 1:
                    tft.fill_rect(78, 45, 162, font_l.HEIGHT, st7789.BLACK)
                    tft.text(font_l, check[z], x, y)
                elif z == 2:
                    tft.fill_circle(228, y+14, 8, dict_color[i])
                    tft.fill_rect(120, 74, 100, font_l.HEIGHT, st7789.BLACK)
                    tft.text(font_l, check[z], x, y)
                    time.sleep(0.4)
                    tft.fill_circle(228, y+14, 8, st7789.BLACK)
                elif z == 3:
                    tft.fill_circle(228, y+14, 8, dict_color[i])
                    tft.fill_rect(120, 103, 100, font_l.HEIGHT, st7789.BLACK)
                    tft.text(font_l, check[z], x, y)
                    time.sleep(0.4)
                    tft.fill_circle(228, y+14, 8, st7789.BLACK)     
            y += font_l.HEIGHT-3   

   
    
main()
