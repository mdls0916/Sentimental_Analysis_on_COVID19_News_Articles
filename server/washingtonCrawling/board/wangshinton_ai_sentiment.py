import pickle 
import re
from nltk.corpus import stopwords ##많이 사용하여 감성적인 의미가 미미한 단어를 없애는 부분  ex>the,a, is 

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer ### NLTK Sentiment Lib 가져오기 

import argparse





conora19_title = []
conora119_content = []

def getSentiment() : 
        
    with open("data/sample_twitter_data_2020-06-20_to_2020-08-06.pk",'rb') as f : 
        conora19_content = pickle.load(f)
        
    conora19_content = [str(doc) for doc in conora19_content]  ### LIST(str) 을 변환시키는 부분 
    print(type(conora19_content))


    #### "https://" 제거하기 
    pattern2 = re.compile(r"\b(https?:\/\/)?([\w.]+){1,2}(\.[\w]{2,4}){1,2}(.*)")
    clean_conora19_content = [pattern2.sub("", doc) for doc in conora19_content]


    #####  "\n"  제거하기 
    pattern1 = re.compile("\n")
    clean_conora19_content = [pattern1.sub("",doc) for doc in clean_conora19_content]

    #### "특수문자"  제거하기 ex> ?,*, !...... 
    pattern4 = re.compile("[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]") ##특수 문자 제거
    clean_conora19_content = [pattern4.sub("",doc) for doc in clean_conora19_content]



    #########  english 보기 
    stops = set(stopwords.words("english"))

    ######## customer 단어도 정제하기 (일반적인 단어가 아니라,불필요한 단어 찾기 )

    stops.add('The')
    stops.add('said')
    stops.add('people')
    stops.add('also')
    stops.add('would')
    stops.add('\n')
    stops.add('ANALYSIS/OPINION:') 

    clean_conora19_content = [word for word in clean_conora19_content if word not in stops and len(word) > 1]

    clean_conora19 = []

    ##### 대문자를 소문자로 바뀌기 
    for text in clean_conora19_content :
        clean_conora19.append(text.lower()) ## lower() 소문자로 변환하기
        
    print(clean_conora19[1])

    ########### 감성 분류 

    nltk.download('vader_lexicon')  ## 감성적인 분류 Lib 가져오기
    sid = SentimentIntensityAnalyzer() ### NLTK Sentiment class 만들기

    sentiment = sid.polarity_scores(clean_conora19[1]) ## 기사 contents 하나만 적용하기 
    print("neg sum:{}, neu sum:{}, pos sum:{}".format(sentiment['neg'],sentiment['neu'],sentiment['pos']))

    #### 기사 전체 sentiment 적용하고 저장하기

    total_sentiment = []
    for content in clean_conora19 :
        total_sentiment.append(sid.polarity_scores(content))
        
    #### 기사 전체 Sentiment 합계 구하기

    total_neg = 0.0
    total_neu = 0.0 
    total_pos = 0.0
    print("len:",len(total_sentiment))

    for sentiment in total_sentiment : 
        total_neg = total_neg + float(sentiment['neg'])
        total_neu = total_neu + float(sentiment['neu'])
        total_pos = total_pos + float(sentiment['pos'])

    print("neg sum:{}, neu sum:{}, pos sum:{}".format(total_neg/len(total_sentiment),total_neu/len(total_sentiment),total_pos/len(total_sentiment)))
    
    return [len(total_sentiment),total_neg/len(total_sentiment),total_neu/len(total_sentiment),total_pos/len(total_sentiment)]

