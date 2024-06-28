# ViewbotAnalysisTool 🤖

A Twitch and Kick View bot Analysis tool, Determine if your favorite streamers are view botting.

## **How it works:**

Uses Selenium to webscrape Twitch/Kick chatrooms, and counts unique chatters, then uses the Twitch API to find viewercounts, and selenium to scrape for kicks viewcounts. (Unfortunately Kick has no public API). After Data collection is done, we get an average viewership and compare that to unique chatters, then find a ratio (Viewer Count/Unique Chatters) You can use this metric to determine whether a streamer is using viewbots or not.

## **Installation:**

```bash
#Install Repo
git clone https://github.com/clearlyyy/ViewbotAnalysisTool

#Go into dir
cd ViewbotAnalysisTool

#Install Requirements
pip3 install -r requirements.txt

#Run The tool
python3 main.py
```

After Installation, Replace client_id and client_secret in main.py, with the appropriate values, you can find these in your Twitch Developer Settings by Registering an App.

Note: Chrome is required to be installed on your system. Kick's CloudFlare protection blocks automated firefox browsers.
