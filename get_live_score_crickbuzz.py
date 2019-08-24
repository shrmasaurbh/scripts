__author__ ="saurabh"
"""  need to install bs4,requests,pynotifier(for ubuntu),win10toast(windows)"""
import bs4 as bs            # bs4 library run as bs
# from urllib import request
import requests
# from win10toast import ToastNotifier
from pynotifier import Notification
# toaster = ToastNotifier()

url = "http://www.cricbuzz.com/cricket-match/live-scores"

sauce = requests.get(url)
soup = bs.BeautifulSoup(sauce.text, "lxml")
# print(soup)
score = []
results = []
# for live_matches in soup.find_all('div',attrs={"class":"cb-mtch-lst cb-col cb-col-100 cb-tms-itm"}):
for div_tags in soup.find_all('div', attrs={"class": "cb-lv-scrs-col text-black"}):
    score.append(div_tags.text)
for result in soup.find_all('div', attrs={"class": "cb-lv-scrs-col cb-text-complete"}):
    results.append(result.text)

print(score[0], results[0])
Notification(
	title='Score',
	description=score[0],
	# icon_path='path/to/image/file/icon.png', # On Windows .ico is required, on Linux - .png
	duration=3,                              # Duration in seconds
	urgency=Notification.URGENCY_CRITICAL
).send()
# toaster.show_toast(title=score[0], msg=results[0])