# Environment Opzetten (LET OP: Dit hoeft maar een keer)

Environment opzetten: `python -m venv venv`
Environment activeren: `.\venv\Scripts\Activate.ps1`

# Library's installeren

Installeren van tools: `python -m pip install -r requirements.txt`
**Als het bovenstaande niet werkt, doe dan dit:**
goslate: `python -m pip install goslate`
itemadapter: `python -m pip install itemadapter`
Scrapy: `python -m pip install Scrapy`

# Start je script (Kies jouw script)

Ga naar jouw folder: `cd <vliegvelden | vliegtuigen | brandstoffen>`
Start jouw script <Brandstoffen>: `scrapy crawl olieonline`
Start jouw script <Vliegtuigen>: `scrapy crawl koopvliegtuig`
Start jouw script <Vliegvelden>: `scrapy crawl vliegvelden_lijst`
