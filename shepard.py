import spacy
nlp = spacy.load('en')


# What is in the sentence
def recognize(query):
    doc = nlp(query)

    # Parts of Language
    noun_chunks = list()
    nouns = list()

    words = {'noun_chunks':list(),'nouns':list()}

    for sentence in doc.sents:
        # Analyze the sentence
        sentence = nlp(str(sentence))
        for np in sentence.noun_chunks:
            noun_chunks.append(np)

        for t in sentence:
            if t.pos_ == 'NOUN':
                nouns.append(t)

        # Creating a new sentence structure
        words['noun_chunks'] = words['noun_chunks'] + noun_chunks
        words['nouns'] = words['nouns'] + nouns

        # Clearing all our nouns,adjectives,verbs
        noun_chunks = list()
        nouns = list()

    #print(words)
    return words
