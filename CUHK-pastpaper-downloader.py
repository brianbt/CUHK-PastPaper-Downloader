# imported the requests library
import requests
import getpass
from bs4 import BeautifulSoup
count = 0
start = 2009
end = 2030
print("################")
print("This program helps you to download CUHK past paper easily.")
print("Only for CUHK students, you will need to login to your CUHK @link account.")
print("We only use your personal information to login to CUHK library, no information will be stored.")
print("################")
name = input("Please enter your @link email: ")
while "@link.cuhk.edu.hk" not in name:
    name = input("Please enter a *valid* @link email: ")
pw = getpass.getpass()
coursecode = input("Enter the corse code: ").upper()
while (len(coursecode) < 8):
    coursecode = input("Enter a *valid* corse code: ").upper()
while True:
    try:
        start = int(input("You want to download FROM (year,eg:2015): "))
        end = int(input("You want to download TO (year,eg:2020): "))
        if end < start: 
            raise("FROM should be earlier than END")
        break
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        exit()
    except:
        print("Invalid Inputs.")

sem = 1
data = {'UserName': name,
        'Password': pw,
        "submit": "Enter",
        "lang": "en",
        "action": "login"}
head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
with requests.Session() as c:
    t = c.get(f'https://authweb.lib.cuhk.edu.hk/examdb/pdf/{start}/1/{coursecode}.pdf')
    url = t.url
    c.post(url, data=data, headers=head)
    r = c.post(f"https://authweb.lib.cuhk.edu.hk/examdb/pdf/{start}/1/{coursecode}.pdf")
    soup = BeautifulSoup(r.content, "lxml")
    try:
        SAMLResponse = soup.find('input', {'name': 'SAMLResponse'})['value']
        RelayState = soup.find('input', {'name': 'RelayState'})['value']
    except:
        print("Wrong SID or password. Please re-run the program with correct account information")
        exit()
    finalsend = {"SAMLResponse": SAMLResponse,
                 "RelayState": RelayState}
    pdf = c.post(
        "https://authweb.lib.cuhk.edu.hk:443/Shibboleth.sso/SAML2/POST", data=finalsend)
    print("Processing please wait...")
    if(pdf.reason != "Not Found"):
        with open(f"{coursecode}-{start}-sem1.pdf", 'wb') as f:
            f.write(pdf.content)
        count += 1
    i = start
    while (True):
        sem = sem % 2
        semx = 0
        if (sem == 0):
            semx = 1
            i+=1
        if (sem == 1):
            semx = 2
        sem += 1
        r1 = c.post(
            f"https://authweb.lib.cuhk.edu.hk/examdb/pdf/{i}/{semx}/{coursecode}.pdf")
        if(r1.reason != "Not Found"):
            with open(f"{coursecode}-{i}-sem{semx}.pdf", 'wb') as f:
                f.write(r1.content)
            count += 1
        if (i >= end):
            break
    if (count == 0):
        print("No Past Paper was found within the years OR you have Enter invalid course code.")
    else:
        print(f"{count} Past Papers downloaded! Good Luck on your exam.")
