import pandas as pd

import time

from collections import Counter



stopwords = set([

    'the', 'in', 'to', 'of', 'and', 'a', 'an', 'on', 'for', 'with', 'is', 'was', 

    'by', 'at', 'from', 'this', 'that', 'it', 'as', 'be', 'are', 'were', 'or', 'but',

    'not', 'so', 'if', 'then', 'out', 'up', 'down', 'over', 'under', 'about', 'after',

    'before', 'between', 'into', 'through', 'during', 'above', 'below', 'off', 'too', 

    'very', 'can', 'will', 'just', 'than', 'also', 'any', 'all', 'no', 'nor', 'only',

    'own', 'same', 'such', 'until', 'while', 'have', 'what','has', 'i','there', '*', 'would','they','been', 'which',

    'we', '>', 'how', 'their', 'he', 'his', 'who', 'do', 'you', 'these', '-'

])



def main():

    start_time = time.time()



    df = pd.read_csv('datasets/NeutralPolitics_data.csv', engine='python')

    all_text = ' '.join(df['Body'].dropna().tolist())

    words = all_text.lower().split()



    # Filter out stopwords

    filtered_words = [word for word in words if word not in stopwords]

    word_count = Counter(filtered_words)



    end_time = time.time()



    print(f"Top 10 words: {word_count.most_common(10)}")

    print(f"Total unique words: {len(word_count)}")

    print(f"Elapsed time: {end_time - start_time:.2f} seconds")



if __name__ == "__main__":

    main()