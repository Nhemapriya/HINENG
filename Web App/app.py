from flask import Flask, render_template, request
from translate import Translator
from nltk.translate.bleu_score import sentence_bleu
from codeswitch.codeswitch import NER
from codeswitch.codeswitch import POS
from codeswitch.codeswitch import LanguageIdentification
import re
import pickle


app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/check")
def check():
    return render_template("index.html")

@app.route("/calculate", methods=['POST'])
def calculate():
    text = request.form['text']
    original_list = [text.split(" ")]
    translator= Translator(from_lang="hindi",to_lang="english")
    translation = translator.translate(text)
    destination_list = translation.split(" ")
    score = sentence_bleu(original_list, destination_list)
    return render_template("result.html", score=score, inter=translation, text=text)

@app.route("/shortform")
def show():
    return render_template("emoShortForm.html")


@app.route("/esf", methods=["POST"])
def esf():
    messages = { "AFAIK" : "As Far As I Know",
        "AFK" : "Away From Keyboard",
        "ASAP" : "As Soon As Possible",
        "ATK" : "At The Keyboard",
        "ATM" : "At The Moment",
        "A3" : "Anytime, Anywhere, Anyplace",
        "BAK" : "Back At Keyboard",
        "BBL" : "Be Back Later",
        "BBS" : "Be Back Soon",
        "BFN" : "Bye For Now",
        "B4N" : "Bye For Now",
        "BRB" : "Be Right Back",
        "BRT" : "Be Right There",
        "BTW" : "By The Way",
        "B4" : "Before",
        "B4N" : "Bye For Now",
        "CU" : "See You",
        "CUL8R" : "See You Later",
        "CYA" : "See You",
        "FAQ" : "Frequently Asked Questions",
        "FC" : "Fingers Crossed",
        "FWIW" : "For What It's Worth",
        "FYI" : "For Your Information",
        "GAL" : "Get A Life",
        "GG" : "Good Game",
        "GN" : "Good Night",
        "GMTA":"Great Minds Think Alike",
        "GR8" : "Great!",
        "G9" : "Genius",
        "IC" : "I See",
        "ICQ" : "I Seek you",
        "ILU": "I Love You",
        "ILY": "I Love You",
        "IMHO" : "In My Honest/Humble Opinion",
        "IMO" : "In My Opinion",
        "IOW" : "In Other Words",
        "IRL" : "In Real Life",
        "KISS" : "Keep It Simple, Stupid",
        "LDR" : "Long Distance Relationship",
        "LMAO" : "Laugh My A.. Off",
        "LOL" : "Laughing Out Loud",
        "LTNS" : "Long Time No See",
        "L8R" : "Later",
        "MTE" : "My Thoughts Exactly",
        "M8" : "Mate",
        "NRN" : "No Reply Necessary",
        "OIC" : "Oh I See",
        "PITA" : "Pain In The A",
        "PRT" : "Party",
        "PRW" : "Parents Are Watching",
        "QPSA?" : 	"Que Pasa?",
        "ROFL" : "Rolling On The Floor Laughing",
        "ROFLOL" : "Rolling On The Floor Laughing Out Loud",
        "ROTFLMAO" : "Rolling On The Floor Laughing My A.. Off",
        "SK8" : "Skate",
        "STATS" : "Your sex and age",
        "ASL" : "Age, Sex, Location",
        "THX" : "Thank You",
        "TTFN" : "Ta-Ta For Now!",
        "TTYL" : "Talk To You Later",
        "U" : "You",
        "U2" : "You Too",
        "U4E" : "Yours For Ever",
        "WB" : "Welcome Back",
        "WTF": "What The F...",
        "WTG" : "Way To Go!",
        "WUF" : "Where Are You From?",
        "W8"  : "Wait..."
}

    with open('Emoji_Dict.p', 'rb') as fp:
        Emoji_Dict = pickle.load(fp)
    Emoji_Dict = {v: k for k, v in Emoji_Dict.items()}
    

    #get sentence
    my_sent = request.form["text"]
    sent = my_sent
    for emot in Emoji_Dict:
        sent = re.sub(r'('+emot+')', "_".join(Emoji_Dict[emot].replace(",","").replace(":","").split()), sent)

    new_sent = ""
    words = sent.split(" ")
    for word in words:
        if word.upper() in messages.keys():
            new_sent+= messages[word.upper()]
        else:
            new_sent+=word
        new_sent+=" "
    return render_template("smsShow.html", text=my_sent, answer=new_sent)

@app.route("/analytics")
def graph():
    return render_template("displayGraph.html")

@app.route("/mainFeatures")
def feature():
    return render_template("mainFeatures.html")

@app.route("/bot")
def bot():
    return render_template("bot.html")

@app.route("/ner")
def ner():
    return render_template("ner.html")

@app.route("/langauge")
def lang():
    return render_template("pos.html")

@app.route("/nerresult", methods=["POST"])
def nerresult():
    text = request.form['text']
    ner = NER('hin-eng')
    result = ner.tag(text)
    return render_template("nerResult.html", result=result)


@app.get("/pos")
def postag():
    return render_template("pos.html")

@app.route("/posresult", methods=["POST"])
def posres():
    text = request.form['text']
    pos = POS('hin-eng')
    result = pos.tag(text)
    return render_template("posResult.html", result=result)


@app.route("/identify")
def ident():
    return render_template("langIdentify.html")

@app.route("/langresult", methods=["POST"])
def langres():
    text = request.form['text']
    lid = LanguageIdentification('hin-eng') 
    result = lid.identify(text)
    return render_template("langResult.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)