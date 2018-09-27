from selenium import webdriver
import time
import getpass
import sys

driver = webdriver.Chrome()
driver.get("https://10.17.10.23/GCL/web")
time.sleep(1)
not_loggined = driver.find_elements_by_xpath("//table[@id='day_main']//td[@class = 'new']")
loggined = driver.find_elements_by_xpath("//table[@id='day_main']//td[@class = 'I']")

slots = driver.find_elements_by_xpath("//table[@id='day_main']//tr")[2:]

data = []
name = ""
hour = 12
minute = 0
for slot in slots:
    in_data = slot.find_elements_by_tag_name("td")
    curr_data = []
    curr_data.append(hour)
    curr_data.append(minute)
    minute = minute+30
    hour = (hour+minute//60)%12
    minute = minute%60
    if(len(in_data)==1):
        curr_data.append(name)
    elif(len(slot.find_elements_by_class_name("I"))):
        name = in_data[1].find_element_by_tag_name("a")
        name = name.text
        curr_data.append(name)
    else:
        curr_data.append("not_booked")
    data.append(curr_data)
last_booked = -1
for i in range(48):
    if(data[47-i][2] != "not_booked"):
        last_booked =47- i
        break

if(last_booked!=-1):
    hr = str(data[last_booked][0])
    if(len(hr)==1): hr = '0'+hr
    mi = str(data[last_booked][1])
    if(len(mi)==1): mi = '0'+mi
    print("[@] Last Booked: "+hr+":"+mi+"     "+data[last_booked][2])


login_slot = slots[i+1]
url = login_slot.find_elements_by_tag_name("td")[1]
url.click()
print()
print("Enter your GCL User Name and password to book the lab for an hour.")
login_id = input("Enter GCL login ID (leave empty to exit): ")
if(len(login_id)==0):
    driver.close()
    sys.exit()
password = getpass.getpass("Enter password: ")

id_field = driver.find_element_by_id("NewUserName")
id_field.send_keys(login_id)
password_field = driver.find_element_by_id("NewUserPassword")
password_field.send_keys(password+"\n")

time.sleep(1)
name_field = driver.find_elements_by_id("name")
if(len(name_field)==0):
    print("Login failed! Invalid credentials or you are not a GCL representative.")
    driver.close()
else:
    intro = input("Enter your brief intro: ")
    name_field[0].send_keys(intro+"\n")

driver.close()




