import pickle
from text_preprocessing import to_lower, remove_punctuation, lemmatize_word, remove_stopword, lemmatize_word, preprocess_text
from gensim import corpora, models, similarities
from gensim.models.coherencemodel import CoherenceModel

class LDA:
    def __init__(self, docs):
        self.model = None
        self.no_of_topics = 20

        # Create a dictionary from the corpus
        self.docs = docs
        self.preprocess_functions = [to_lower, remove_punctuation, lemmatize_word, remove_stopword, lemmatize_word]
        
        self.corpus = [preprocess_text(doc["text"], self.preprocess_functions).split() for doc in docs]

        self.dictionary = corpora.Dictionary(self.corpus)

        # Convert the corpus to a bag-of-words representation
        self.corpus_bow = [self.dictionary.doc2bow(doc) for doc in self.corpus]

        self.max_no_results = 10

    def predict(self, query):
        # Convert the query to a bag-of-words representation
        split_query = preprocess_text(query, self.preprocess_functions).split()
        query_bow = self.dictionary.doc2bow(split_query)

        # Calculate the topic distribution for the query
        query_lda = self.model[query_bow]

        # Calculate the similarity between the query and each document
        index = similarities.MatrixSimilarity(self.model[self.corpus_bow])
        sims = index[query_lda]

        # Rank the documents by similarity and limit it to 10
        ranked_docs = sorted(enumerate(sims), key=lambda item: -item[1])

        ranked_docs = ranked_docs[: min(self.max_no_results, len(ranked_docs))]
        # Return the ranked documents as a list of dictionaries with id and similarity score

        return [self.docs[idx] for idx, _score in ranked_docs]

    def train_and_save(self):
        # Train the LDA model
        self.model = models.ldamodel.LdaModel(
            self.corpus_bow,
            num_topics=self.no_of_topics,
            id2word=self.dictionary,
            passes=10,
        )

        topics = self.model.top_topics(corpus=self.corpus_bow, topn=self.no_of_topics)
        cm = CoherenceModel(model=self.model, corpus=self.corpus_bow, dictionary=self.dictionary, coherence='u_mass')
        coherence = cm.get_coherence_per_topic()

        print("Topics learned", topics)
        print("Coherence metrics ", coherence)


        # Save the trained model to a file
        with open("../../lda_model.pkl", "wb") as f:
            pickle.dump(self.model, f)

    def load_model(self):
        # Model name shall be lda_model.pkl
        with open("../../lda_model.pkl", "rb") as f:
            self.model = pickle.load(f)
        
        topics = self.model.top_topics(corpus=self.corpus_bow, topn=self.no_of_topics)
        cm = CoherenceModel(model=self.model, corpus=self.corpus_bow, dictionary=self.dictionary, coherence='u_mass')
        coherence = cm.get_coherence_per_topic()

        print("Topics learned", topics)
        print("Coherence metrics ", coherence)


if __name__ == "__main__":
    # Test the function with sample data
    docs = [
        {"id": 1, "text": "The cat in the hat"},
        {"id": 2, "text": "The cat in the tree"},
        {"id": 3, "text": "The dog in the tree"},
        {"id": 4, "text": "The dog in the house"},
        {"id": 5, "text": "The bird in the tree"},
    ]
    query = "bird"
    model = LDA(docs=docs)
    model.train_and_save()
    ranked_docs = model.predict(query)
    print(ranked_docs)
