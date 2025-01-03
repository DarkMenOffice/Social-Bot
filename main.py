import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init

# تهيئة colorama
init(autoreset=True)

def print_dark_men_logo():
    """ طباعة الشعار "Dark Men" باستخدام # """
    # مجموعة الألوان
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    color_choice = random.choice(colors)  # اختيار اللون العشوائي
    
    # الشعار المصنوع من # لكتابة "Dark Men"
    logo = """
 DDDDD   AAAAA  RRRRR   K   K   M   M  EEEEE  N   N
 D   D  A     A R   R   K  K    MM MM  E      NN  N
 D   D  AAAAAAA RRRRR   KKK     M M M  EEEE   N N N
 D   D  A     A R  R    K  K    M   M  E      N  NN
 DDDDD  A     A R   R   K   K   M   M  EEEEE  N   N
    """
    
    # طباعة الشعار
    print(f"{color_choice}{logo}")
    print(f"{Fore.WHITE}Made by Dark Men Office")
    print("-" * 50)  # خط فاصل بعد الشعار

def get_credentials(file_path):
    """ قراءة بيانات تسجيل الدخول من ملف نصي """
    with open(file_path, 'r') as file:
        credentials = file.readlines()
    return credentials[0].strip(), credentials[1].strip()  # البريد أو الرقم وكلمة السر

def login_to_facebook(driver, username, password):
    """ تسجيل الدخول إلى فيسبوك باستخدام Selenium """
    driver.get("https://www.facebook.com/login")
    time.sleep(3)
    
    username_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "pass")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

def login_to_instagram(driver, username, password):
    """ تسجيل الدخول إلى إنستغرام باستخدام Selenium """
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

def search_account(driver, search_query, site):
    """ البحث عن حساب في الموقع بعد تسجيل الدخول """
    time.sleep(5)
    if site == "facebook":
        # الانتقال إلى الرابط مباشرة
        driver.get(search_query)
    elif site == "instagram":
        # استخدام شريط البحث
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

def report_user(driver, site):
    """ الضغط على ثلاث نقاط، واختيار بلاغ """
    time.sleep(3)
    if site == "facebook":
        three_dots_button = driver.find_element(By.XPATH, "//div[@aria-label='Actions for this post']")
        three_dots_button.click()
        time.sleep(2)
        report_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Find Support or Report')]")
        report_button.click()
        time.sleep(2)
        first_report_option = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Report')]")
        first_report_option.click()
    elif site == "instagram":
        try:
            # انتظر حتى يظهر زر "More options"
            three_dots_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='More options']"))
            )
            three_dots_button.click()
            time.sleep(2)
            
            # انتظر حتى يظهر زر "Report"
            report_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Report')]"))
            )
            report_button.click()
            time.sleep(2)
            
            # تقرير
            first_report_option = driver.find_element(By.XPATH, "//button[contains(text(), 'Report')]")
            first_report_option.click()

        except Exception as e:
            print(f"An error occurred while reporting the user: {e}")

def main():
    # طباعة الشعار
    print_dark_men_logo()

    while True:
        # طلب اختيار الموقع
        site = input("Choose a site to log in to (facebook/instagram): ").strip().lower()
        
        if site not in ["facebook", "instagram"]:
            print("Invalid site selected!")
            continue

        # طلب رابط الحساب إذا كان فيسبوك، أو اليوزر نيم إذا كان إنستغرام
        if site == "facebook":
            search_query = input("Enter the Facebook profile URL you want to report: ").strip()
        elif site == "instagram":
            search_query = input("Enter the Instagram username you want to report: ").strip()
        
        # طلب عدد مرات التكرار
        try:
            repeat_count = int(input("How many times do you want to repeat this process? ").strip())
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        # تحديد مسار الملف بناءً على الموقع المختار
        file_name = f"{site}.txt"
        file_path = input(f"Enter the path to the {file_name}: ").strip()

        # قراءة بيانات الدخول من الملف
        username, password = get_credentials(file_path)
        
        # إعداد متصفح Selenium باستخدام Firefox و GeckoDriver
        options = Options()
        options.headless = True  # تشغيل المتصفح في وضع headless (بدون واجهة رسومية)
        driver = webdriver.Firefox(options=options)

        try:
            # تكرار العملية بعدد المرات المطلوبة
            for i in range(repeat_count):
                print(f"Starting process {i + 1}/{repeat_count}...")
                
                # تسجيل الدخول
                if site == "facebook":
                    login_to_facebook(driver, username, password)
                elif site == "instagram":
                    login_to_instagram(driver, username, password)
                
                # البحث عن الحساب
                search_account(driver, search_query, site)
                
                # القيام بالبلاغ
                report_user(driver, site)
                
                # انتظار بسيط قبل بدء العملية التالية
                time.sleep(5)

            print("All processes completed successfully!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()

        # طلب إعادة تشغيل الأداة
        while True:
            user_choice = input("Do you want to restart the tool, continue, or exit? (restart/continue/exit): ").strip().lower()
            if user_choice == "restart":
                main()
                return
            elif user_choice == "continue":
                break
            elif user_choice == "exit":
                print("Exiting the tool.")
                return
            else:
                print("Invalid choice! Please enter 'restart', 'continue', or 'exit'.")

if __name__ == "__main__":
    main()