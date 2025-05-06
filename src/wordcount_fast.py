import pandas as pd

import time

import re

from collections import Counter

from threading import Thread



# Define stopwords



stopwords = set([

    'the', 'in', 'to', 'of', 'and', 'a', 'an', 'on', 'for', 'with', 'is', 'was',

    'by', 'at', 'from', 'this', 'that', 'it', 'as', 'be', 'are', 'were', 'or', 'but',

    'not', 'so', 'if', 'then', 'out', 'up', 'down', 'over', 'under', 'about', 'after',

    'before', 'between', 'into', 'through', 'during', 'above', 'below', 'off', 'too',

    'very', 'can', 'will', 'just', 'than', 'also', 'any', 'all', 'no', 'nor', 'only',

    'own', 'same', 'such', 'until', 'while', 'have', 'what','has', 'i','there', '*', 'would','they','been', 'which',

    'we', '>', 'how', 'their', 'he', 'his', 'who', 'do', 'you', 'these', '-'

])



def process_chunk(chunk, counter):

    text = ' '.join(chunk).lower()

    text = re.sub(r'[^a-z\s]', '', text)

    words = text.split()

    filtered = [w for w in words if w not in stopwords]

    counter.update(filtered)



def main():

    start_time = time.time()



    # Read only 'text' column

    df = pd.read_csv('../data/NeutralPolitics_data.csv', usecols=['Body'], engine='python')



    texts = df['Body'].dropna().values



    # Split data into chunks for each thread

    num_threads = 4

    chunk_size = len(texts) // num_threads



    counters = [Counter() for _ in range(num_threads)]

    threads = []



    for i in range(num_threads):

        chunk = texts[i * chunk_size : (i + 1) * chunk_size]

        thread = Thread(target=process_chunk, args=(chunk, counters[i]))

        threads.append(thread)

        thread.start()



    for thread in threads:

        thread.join()



    # Merge counters

    total_counter = Counter()

    for counter in counters:

        total_counter.update(counter)



    end_time = time.time()



    print(f"Top 10 words: {total_counter.most_common(10)}")

    print(f"Total unique words: {len(total_counter)}")

    print(f"Elapsed time: {end_time - start_time:.2f} seconds")



if __name__ == "__main__":

    main()
