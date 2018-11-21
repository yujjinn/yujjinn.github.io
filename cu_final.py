from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
import pymysql.cursors

url = 'http://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N'
driver = webdriver.Chrome('chromedriver')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

# ------------------- initializing variable -------------------

# 1+1 상품 정보 저장
array_name_1 = []
array_price_1 = []
array_img_1 = []
# 2+1 상품 정보 저장
array_name_2 = []
array_price_2 = []
array_img_2 = []
# 3+1 상품 정보 저장
array_name_3 = []
array_price_3 = []
array_img_3 = []

# ------------------- DB 연결 준비 -------------------

hostName = '127.0.0.1'
userName = 'root'
passWord = '1996'


# sql for 1+1 TABLE
sql_one = '''CREATE TABLE cu_OnePlusOne (
    item_img varchar(255) NOT NULL,
    item_name varchar(255) NOT NULL,
    item_price varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8'''
# sql for 2+1 TABLE
sql_two = '''CREATE TABLE cu_TwoPlusOne (
    item_img varchar(255) NOT NULL,
    item_name varchar(255) NOT NULL,
    item_price varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8'''
# sql for 3+1 TABLE
sql_three = '''CREATE TABLE cu_ThreePlusOne (
    item_img varchar(255) NOT NULL,
    item_name varchar(255) NOT NULL,
    item_price varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8'''

conn = pymysql.connect(host= hostName,
                       port = 3306,
                       user= userName ,
                       password= passWord,
                       db='DB',
                       charset='utf8')

# ------------------- DB 생성 -------------------
try:
    with conn.cursor() as cursor:
        cursor.execute(sql_one)
    conn.commit()
except :
    print('already exists')
    with conn.cursor() as cursor:
        sql = '''
            DROP TABLE cu_OnePlusOne
'''
        cursor.execute(sql)
    conn.commit()
    with conn.cursor() as cursor:
        cursor.execute(sql_one)
    conn.commit()

try:
    with conn.cursor() as cursor:
        cursor.execute(sql_two)
    conn.commit()
except :
    print('already exists')
    with conn.cursor() as cursor:
        sql = '''
            DROP TABLE cu_TwoPlusOne
'''
        cursor.execute(sql)
    conn.commit()
    with conn.cursor() as cursor:
        cursor.execute(sql_two)
    conn.commit()


try:
    with conn.cursor() as cursor:
        cursor.execute(sql_three)
    conn.commit()
except :
    print('already exists')
    with conn.cursor() as cursor:
        sql = '''
            DROP TABLE cu_ThreePlusOne
'''
        cursor.execute(sql)
    conn.commit()
    with conn.cursor() as cursor:
        cursor.execute(sql_three)
    conn.commit()

# ------------------- DB 연결 끝 -------------------

count = 1
def more(num) : # 더 보기 개수 찾기
    if num == 1 :
        code = 23
    elif  num == 2 :
        code = 24
    elif num == 3 :
        code = 49
    driver.execute_script("goDepth("+str(code)+");")
    global count
    count = 1
    while True :
        time.sleep(1)
        driver.execute_script("nextPage(1);")
        time.sleep(1)
        try :
            more = driver.find_element_by_class_name('prodListBtn-e')
            if more.text == '맨위로' :
                count = count + 1
        except:
            break
    return count

# ------------------- 1+1 추출 -------------------
def oneFnc():
    print('1+1 추출')
    one = more(1)
    driver.execute_script("goDepth(23);")

    for a in range(1, one):
        time.sleep(1)
        driver.execute_script("nextPage(1);")
        time.sleep(1)

    prodName_one = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[1]/a')
    for name in prodName_one :
        array_name_1.append(name.text)

    prodPrice_one = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[2]/span')
    for price in prodPrice_one :
        array_price_1.append(price.text)

    prodImg_one = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/div/a/img')
    for img in prodImg_one :
        url = img.get_attribute('src')
        array_img_1.append(url)

    print('extract 1+1 item done')
    
# ------------------- 2+1 추출  -------------------

def twoFnc():
    print('2+1 추출')
    two = more(2)

    driver.execute_script("goDepth(24);")


    for a in range(1, two):
        time.sleep(1)
        driver.execute_script("nextPage(1);")
        time.sleep(1)

    time.sleep(1)

    prodName_two = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[1]/a')
    for name in prodName_two :
        array_name_2.append(name.text)
        
    
    prodPrice_two = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[2]/span')
    for price in prodPrice_two :
        array_price_2.append(price.text)
        

    prodImg_two = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/div/a/img')
    for img in prodImg_two :
        url = img.get_attribute('src')
        array_img_2.append(url)

    print('extract 2+1 item done')

# ------------------- 3+1 추출  -------------------

def threeFnc():
    print('3+1 추출')
    three = more(3)
    driver.execute_script("goDepth(49);")

    for a in range(1, three):
        time.sleep(1)
        driver.execute_script("nextPage(1);")
        time.sleep(1)

    prodName_three = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[1]/a')
    for name in prodName_three :
        array_name_3.append(name.text)

    prodPrice_three = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[2]/span')
    for price in prodPrice_three :
        array_price_3.append(price.text)

    prodImg_three = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/div/a/img')
    for img in prodImg_three :
        url = img.get_attribute('src')
        array_img_3.append(url)

    print('extract 3+1 item done')
    
# ------------------- 추출 완료 -------------------

oneFnc()
twoFnc()
threeFnc()

print(array_name_2)

# ------------------- insert into DB -------------------

sql_one_insert = "insert into cu_OnePlusOne(item_img,item_name,item_price) values(%s, %s, %s)"
sql_two_insert = "insert into cu_TwoPlusOne(item_img,item_name,item_price) values(%s, %s, %s)"
sql_three_insert = "insert into cu_ThreePlusOne(item_img,item_name,item_price) values(%s, %s, %s)"

with conn.cursor() as cursor:
    for a in range(0, len(array_name_1),1):
        cursor.execute(sql_one_insert,(array_img_1[a],array_name_1[a],array_price_1[a]))
conn.commit()

with conn.cursor() as cursor:
    for a in range(0, len(array_name_2),1):
        cursor.execute(sql_two_insert,(array_img_2[a],array_name_2[a],array_price_2[a]))
conn.commit()

with conn.cursor() as cursor:
    for a in range(0, len(array_name_3),1):
        cursor.execute(sql_three_insert,(array_img_3[a],array_name_3[a],array_price_3[a]))
conn.commit()


conn.close()
