#Clearly
#Viewbot Analysis Software
#Collects data on twitch and kick streams for analysis purposes.
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from TwitchAPI import TwitchAPI

#CLIENT ID AND CLIENT SECRET
#    Change these both in your Twitch Developer Settings,
#    Register an App on Twitch, and you will find these, otherwise viewer count queries wont work for twitch.
#    Kick Doesn't have a Public API, so we webscrape KICK Viewercounts.
##############################################################
client_id = 'CLIENT_ID_HERE'                               ###
client_secret = 'CLIENT_SECRET_HERE'                       ###
##############################################################


#TWITCH HANDLER
def TwitchMain():

    usernames = []
    viewCounts = []
    uniqueChatters = 0

    last_checked = time.time()
    timerStart = time.time()

    TwitchHandler = TwitchAPI(client_id, client_secret)

    streamerName = str(input("Enter Streamer Name: "))
    print('---- Press CTRL + C at any time to end data collection ----')
    print('Booting up Twitch Chat...')

    profile = ChromeOptions()
    profile.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    profile.add_argument("--headless")
    profile.add_argument("--window-size=1920x1080")
    profile.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=profile) 
    driver.get(f"https://www.twitch.tv/popout/{streamerName}/chat?popout=")

    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.chat-author__display-name[data-a-target="chat-message-username"]'))
    )

    try:
        while True:
            try:
                latest_message = driver.find_elements(By.CSS_SELECTOR, 'span.chat-author__display-name[data-a-target="chat-message-username"]')[-1]
                username = latest_message.text
            except KeyboardInterrupt:
                #Exit the Loop, stop monitoring Data
                print("Finishing up data analysis...")
                break
            except:
                print("Error Occurred Trying Again...")
                continue
            

            if username not in usernames:
                usernames.append(username)
                uniqueChatters += 1
                print(f"New User found: {username}")

            if (time.time() - last_checked >= 5):
                viewCounts.append(TwitchHandler.queryViewers(streamerName))
                CurTime = time.time()
                timeSecondsCheck = CurTime - timerStart
                elapsedMinsCheck = int(timeSecondsCheck // 60)
                elapsedSecsCheck = int(timeSecondsCheck % 60)
                print(f"Time Spent: {elapsedMinsCheck}m {elapsedSecsCheck}s")
                last_checked = time.time()

    except KeyboardInterrupt:
        #Exit the Loop, stop monitoring Data
        print("Finishing up data analysis...")

    finally:
        #Calculate Time Spent
        endTime = time.time()
        timeSeconds = endTime - timerStart
        elapsedMins = int(timeSeconds // 60)
        elapsedSecs = int(timeSeconds % 60)
        #Get Average Viewercount during time spent.
        avgViewCount = sum(viewCounts) / len(viewCounts)
        ViewChatRatio = (avgViewCount/uniqueChatters)

        #Print Results
        print("\n\n\n\n\n\n\n")
        print(f"Stats for {streamerName}: ")
        print(f"Average View Count: {avgViewCount:.0f} Viewers")
        print(f"Unique Chatters: {uniqueChatters}")
        print(f"Time Spent: {elapsedMins}m {elapsedSecs}s")
        print("\n" + f"Viewer to Unique Chatter Ratio = {ViewChatRatio:.2f}")

        save_to_spreadsheet("Twitch", streamerName, avgViewCount, uniqueChatters, ViewChatRatio, elapsedMins, elapsedSecs)

        driver.quit()
        #time.wait(30)

#KICK HANDLER
def KickMain():
    usernames = []
    viewCounts = []
    uniqueChatters = 0

    last_checked = time.time()
    timerStart = time.time()

    streamerName = str(input("Enter Streamer Name: "))
    print('---- Press CTRL + C at any time to end data collection ----')
    print('Booting up Kick Chat...')


    profile = ChromeOptions()
    profile.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    profile.add_argument("--headless")
    profile.add_argument("--window-size=1920x1080")
    profile.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=profile) 
    driver.get(f"https://www.kick.com/{streamerName}")

    

    try:
        while True:
            try:
                WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chat-entry-username"))
                )

                latest_message = driver.find_elements(By.CLASS_NAME, 'chat-entry-username')[-1]
                username = latest_message.text.strip()
            except KeyboardInterrupt:
                #Exit the Loop, stop monitoring Data
                print("Finishing up data analysis...")
                break
            except:
                print("Error Occured, trying again...")
                continue

            if username not in usernames:
                usernames.append(username)
                uniqueChatters += 1
                print(f"New User found: {username}")

            if (time.time() - last_checked >= 10):
                #Why does kick do this
                
                container = driver.find_element(By.CLASS_NAME, "o-text")
                viewcountSpans = container.find_elements(By.CSS_SELECTOR, 'span.odometer-value')
                viewerCount = ''
                for span in viewcountSpans:
                    viewerCount += span.text.strip()
                try:
                    viewCounts.append(int(viewerCount))
                except:
                    print("Make Browser Window Bigger to see Viewercount!")
                print(f"Viewer Count for {streamerName}: {viewerCount}")
                CurTime = time.time()
                timeSecondsCheck = CurTime - timerStart
                elapsedMinsCheck = int(timeSecondsCheck // 60)
                elapsedSecsCheck = int(timeSecondsCheck % 60)
                print(f"Time Spent: {elapsedMinsCheck}m {elapsedSecsCheck}s")
                last_checked = time.time()

    except KeyboardInterrupt:
        #Exit the Loop, stop monitoring Data
        print("Finishing up data analysis...")

    finally:
        #Calculate Time Spent
        endTime = time.time()
        timeSeconds = endTime - timerStart
        elapsedMins = int(timeSeconds // 60)
        elapsedSecs = int(timeSeconds % 60)
        #Get Average Viewercount during time spent.
        avgViewCount = sum(viewCounts) / len(viewCounts)
        ViewChatRatio = (avgViewCount/uniqueChatters)

        #Print Results
        print("\n\n\n\n\n\n\n")
        print(f"Stats for {streamerName}: ")
        print(f"Average View Count: {avgViewCount:.0f} Viewers")
        print(f"Unique Chatters: {uniqueChatters}")
        print(f"Time Spent: {elapsedMins}m {elapsedSecs}s")
        print("\n" + f"Viewer to Unique Chatter Ratio = {ViewChatRatio:.2f}\n")

        save_to_spreadsheet("Kick", streamerName, avgViewCount, uniqueChatters, ViewChatRatio, elapsedMins, elapsedSecs)

        driver.quit()

def save_to_spreadsheet(platform, streamer_name, avgViewcount, _uniqueChatters, viewChatRatio, elapsedMins, elapsedSecs):
    #Create a DataFrame
    data = {
        "Platform": [platform],
        "Streamer": [streamer_name],
        "Average View Count": [avgViewcount],
        "Unique Chatters": [_uniqueChatters],
        "Viewers to Unique Chatters Ratio": [viewChatRatio],
        "Time Spent Collecting": [f"{elapsedMins}m {elapsedSecs}s"]
    }

    df = pd.DataFrame(data)
    file_name = "StatsFinal.csv"

    #Save the Data
    if (os.path.exists(file_name)):
        df.to_csv(file_name, mode='a', header=False, index=False)
        print(f"Data Appended to {file_name}")
    else:
        df.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")

if __name__ == "__main__":
    while True:
        inputStr = input("Check Twitch or Kick stats? (Twitch/Kick): ")
        if (inputStr.lower() == "twitch"):
            TwitchMain()
            break
        if (inputStr.lower() == "kick"):
            KickMain()
            break
        else:
            print("Invalid Choice")