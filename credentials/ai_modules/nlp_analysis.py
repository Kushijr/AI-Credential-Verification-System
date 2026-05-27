import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_text(text):

    doc = nlp(text)

    for ent in doc.ents:

        print(ent.text, ent.label_)