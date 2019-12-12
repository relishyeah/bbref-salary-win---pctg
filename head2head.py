from urllib import request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

data = request.urlopen("https://www.basketball-reference.com/contracts")
soup = BeautifulSoup(data, 'html.parser')
salaryList = []
preList= (soup.find_all("tr"))
for i in range(len(preList)):
	y = preList[i].getText()
	z = y.split("$", 2)[:2]
	if len(z)>1:
		salaryList.append(z)

for i in salaryList:
	i[0] = i[0].lstrip('0123456789')
	i[1] = int(i[1].replace(',', ''))

data = request.urlopen("https://www.basketball-reference.com/leagues/NBA_2020_standings.html")
soup = BeautifulSoup(data, 'html.parser')
pct= (soup.find_all("td",attrs={"data-stat":"win_loss_pct"}))
tName = (soup.find_all("th",attrs={"data-stat":"team_name"}))
teamList = []

for j in range(32):
	tName[j] = (tName[j].getText())
	if "(" in tName[j]:
		x = tName[j].split(u'\xa0')[0]
		if x not in teamList:
			teamList.append([x])

for k in range(len(teamList)):
	teamList[k].append(pct[k].getText())

teamList = sorted(teamList)
salaryList = sorted(salaryList)
yAxis = [float(i[1]) for i in teamList] 
xAxis = [i[1] for i in salaryList] 
names = [i[0] for i in salaryList] 
fig, ax = plt.subplots()
ax.scatter(xAxis, yAxis,color='red')

for i, txt in enumerate(names):
    ax.annotate(names[i][:3].upper(), (xAxis[i], yAxis[i]))

plt.plot(np.unique(xAxis), np.poly1d(np.polyfit(xAxis, yAxis, 1))(np.unique(xAxis)))
plt.ylabel('Winning Percentage')
plt.xlabel('Team Salary For 19-20 Season (in 100s of millions)')
plt.show()