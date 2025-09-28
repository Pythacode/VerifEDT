import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import Options
from colorama import init, Fore
from datetime import datetime
import re
from datetime import datetime, time, timedelta
from selenium.common.exceptions import NoSuchElementException
import requests
from urllib.parse import urlencode

init(autoreset=True) # RESET automatiquement la couleur à la fin d'un # print


def log(message) :

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{Fore.YELLOW}[{now}] {message}")

def update_info(user_data) :

    username = user_data["username"]
    password  = user_data["password"]
    url = user_data["url"]

    log("Open driver")

    options = Options()
    #options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    log('Driver opened')

    driver.get(url)
    assert "Authentification" in driver.title

    log("Conection")

    #Élève ou parent
    elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div[1]/div/div/form/fieldset[1]/legend/button")
    elem.click()

    # De l'académie de montpellier
    elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div[1]/div/div/form/fieldset[1]/ul/li[1]/div/label")
    elem.click()

    #Valider
    elem = driver.find_element(By.ID, "button-submit")
    elem.click()

    log('Éduconnect')

    ## Éduconnect
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bouton_eleve")))


    assert "ÉduConnect" in driver.title

    #Éleve
    elem = driver.find_element(By.ID, "bouton_eleve")
    elem.click()

    #Username
    username_entry = driver.find_element(By.ID, "username")
    username_entry.clear()
    username_entry.send_keys(username)

    #Password
    password_entry = driver.find_element(By.ID, "password")
    password_entry.clear()
    password_entry.send_keys(password)

    # Valider
    elem = driver.find_element(By.ID, "bouton_valider")
    elem.click()

    log('Bot log !')

    """

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "services-shortcut__link")))

    # Open pronote
    elems = driver.find_elements(By.CLASS_NAME, "services-shortcut__link")

    for elem in elems :
        if elem.get_attribute("target") == "_blank":
            break
    elem.click()

    """

    log('Pronote')

    def highlight(element, driver, color="yellow", border="2px solid red"):
        """Surligne un élément dans le navigateur."""
        driver.execute_script(
            "arguments[0].style.backgroundColor = arguments[1];"
            "arguments[0].style.border = arguments[2];",
            element, color, border
        )

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "IE.Identite.collection.g5.cellule_Edit")))

    elem = driver.find_element(By.ID, "IE.Identite.collection.g5.cellule_Edit")
    """
    if elem.text != "Aujourd'hui" :
        print('Pas ajd')
        driver.close()
        return
    """
    now = datetime.now()

    data = {
        "date" : now.date().isoformat(),
        "time" : now.time().isoformat(),
        "cours" : []
    }

    for c in driver.find_elements(By.CSS_SELECTOR, "ul.liste-cours > li.flex-contain") :
        # print("---")
        """if len(li.text.splitlines()) <= 1 :
            # print('--')
            # print(li.text.splitlines(), len(li.text.splitlines()))
            continue

        else :
            # print(li.text)
            continue"""

        # text = li.find_elements(By.CSS_SELECTOR, "span.sr-only")[0].text

        # match = re.match(r'de ([0-9]{2})h([0-9]{2}) à ([0-9]{2})h([0-9]{2}) (.*)', text)

        start_hour = end_hour = title = info = room = None

        span_text = c.find_element(By.CSS_SELECTOR, "span.sr-only").text

        # print(span_text, '\n--')

        match = re.match(r"de (\d{1,2})h(\d{2}) à (\d{1,2})h(\d{2}) (.*)", span_text)

        # print('-', match)

        if match:
            start_hour = time(int(match.group(1)), int(match.group(2))).isoformat()
            end_hour = time(int(match.group(3)), int(match.group(4))).isoformat()
            title = match.group(5)
            # print(start_hour, end_hour)
        else:
            start_hour = end_hour = title = None

        # Récupère la liste des infos du cours
        infos = c.find_elements(By.CSS_SELECTOR, "ul.container-cours > li")

        # Vérifie qu'on a assez d'éléments pour récupérer prof et salle
        if len(infos) >= 4:
            # title = infos[0].text
            teacher = infos[1].text
            group = infos[2].text
            room = infos[3].text
            if len(infos) >= 5 :
                info = infos[4].text
            else :
                room = infos[3].text
            # # print([(id, i.text) for id, i in enumerate(infos)])
        else:
            teacher = group = salle = None

        cour = {
            "title": title,
            "room": room,
            "info": info,
            "start_hour": start_hour,
            "end_hour": end_hour,
            "group": group,
            "teacher": teacher
        }

        # print(cour)

        data["cours"].append(cour)
        """

        if match:
            start_hour = time(hour=int(match.group(1)), minute=int(match.group(2))).isoformat()
            end_hour = time(hour=int(match.group(3)), minute=int(match.group(4))).isoformat()
            title = match.group(5)

            if not title in ["Pause Déjeuner", "Pas de cours"] :
                lis2 = li.find_elements(By.TAG_NAME, "li")
                room = ' '.join(lis2[len(lis2)-1].text.split(' ')[:2])

            cour = {
                "title":title,
                "room":room,
                "info":info,
                "start_hour":start_hour,
                "end_hour":end_hour
            }

            data["cours"].append(cour)"""




    with open("cours.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    if True : #finally :

        driver.quit()

for file in ['nath.json'] :

    with open("login_info/" + file, 'r') as f :
        user_data = json.load(f)

    update_info(user_data)

    now = datetime.now()

    if now.hour == 7 and now.minute == 20 :
        api_key = user_data["API_key"]
        id = user_data["ID"]
        requests.get(f"https://smsapi.free-mobile.fr/sendmsg?user={id}&pass={api_key}&{urlencode({'msg' : "Fonctionement du script"})}")
        exit()

    with open("cours.json", "r", encoding="utf-8") as f:
        edt = json.load(f)


    """h, m, s = 11, 50, 0
    now = time(hour=h, minute=m, second=s)
    now = datetime.combine(datetime.today(), now)"""

    for cour in edt["cours"] :
        start = datetime.combine(now.today(), datetime.strptime(cour["start_hour"], "%H:%M:%S").time())
        end = datetime.combine(now.today(), datetime.strptime(cour["end_hour"], "%H:%M:%S").time())

        diff = start - now

        # print(now.hour, now.minute, cour["start_hour"], diff, ' - ', diff <= timedelta(minutes=15), start > now)

        if True : #start > now and diff <= timedelta(minutes=15):

            api_key = user_data["API_key"]
            id = user_data["ID"]

            info = cour['info']

            data = ((f"[{info}] " if info else '') +
                    cour['title'] + '\n' +
                    (f"Salle : {cour['room']}\n" if cour['room'] else '') +
                    (f"Info complémentaire : {cour['info']}\n" if cour['info'] else '') +
                    f"Heure de début : {cour['start_hour']}\n" +
                    f"Heure de fin : {cour['end_hour']}\n" +
                    (f"Groupe : {cour['group']}\n" if cour['group'] else '') +
                    (f"Prof : {cour['teacher']}\n" if cour['teacher'] else '')
                )

            # print(data)

            requet = requests.get(f"https://smsapi.free-mobile.fr/sendmsg?user={id}&pass={api_key}&{urlencode({'msg' : data})}")

            # print(requet.status_code)

            exit()

    print("aucuns cour dans 15 minutes")


