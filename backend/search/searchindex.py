import requests
import nltk
from nltk.stem import PorterStemmer
from rank_bm25 import BM25Okapi

def preprocess(text):
    porter = PorterStemmer() 
    tokens = nltk.word_tokenize(text.lower())
    stemmed_tokens = [porter.stem(token) for token in tokens]
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_tokens = [token for token in stemmed_tokens if token not in stop_words]
    return filtered_tokens



nltk.download('punkt') # This downloads the necessary files for tokenization
nltk.download('wordnet') 
nltk.download('stopwords')
porter = PorterStemmer() # Initializing the Porter2 stemmer
API='http://localhost:6400/api/v1/recipe/get_all'# os.environ.get("API")
response = requests.get(API)

recipelist=response.json()
print(recipelist)
with open("recipelist.txt","w") as f:
    f.writelines(str(recipelist))
f.close()

with open("recipelist.txt","r") as f:
    documentstr=f.readlines()
    print(type(documentstr))
f.close()

documents=recipelist
preprocessed_des = [preprocess(doc["description"]) for doc in documents]
preprocessed_cat = [preprocess(doc["category"]) for doc in documents]

bm25 = BM25Okapi(preprocessed_des)

print(bm25)
print(str(bm25))

# def search(query, n=5):
#     preprocessed_query = preprocess(query)
#     scores = bm25.get_scores(preprocessed_query)
#     sorted_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
#     top_indexes = sorted_indexes[:n]
#     return [documents[i] for i in top_indexes]

# results = search('cereals')
# print(results)