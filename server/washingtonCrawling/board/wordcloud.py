import pickle 
import re
from nltk.corpus import stopwords ##많이 사용하여 감성적인 의미가 미미한 단어를 없애는 부분  ex>the,a, is 

import nltk


def getWordCloud() :

    conora119_content = []

    ####  title , contents  내용 가져오기 #########

        
    with open("data/sample_twitter_data_2020-06-20_to_2020-08-06.pk",'rb') as f : 
        conora19_content = pickle.load(f)
        
        
    conora19_content = [str(doc) for doc in conora19_content]  ### LIST(str) 을 변환시키는 부분 
    print(type(conora19_content))


    #### "https://" 제거하기 
    pattern1 = re.compile(r"\b(https?:\/\/)?([\w.]+){1,2}(\.[\w]{2,4}){1,2}(.*)")
    clean_conora19_content = [pattern1.sub("", doc) for doc in conora19_content]


    #####  "\n"  제거하기 
    pattern2 = re.compile("\n")
    clean_conora19_content = [pattern2.sub("",doc) for doc in clean_conora19_content]

    #### "특수문자"  제거하기 ex> ?,*, !...... 
    pattern3 = re.compile("[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]") ##특수 문자 제거
    clean_conora19_content = [pattern3.sub("",doc) for doc in clean_conora19_content]



    #########  english 보기 
    stops = set(stopwords.words("english"))

    ######## customer 단어도 정제하기 (일반적인 단어가 아니라,불필요한 단어 찾기 )

    stops.add('The')
    stops.add('the')
    stops.add('said')
    stops.add('people')
    stops.add('also')
    stops.add('would')
    stops.add('may')
    stops.add('ANALYSIS/OPINION:') 
    stops.add('may')
    stops.add('could')
    stops.add('would')
    stops.add("it’s")
    stops.add("it's") 

    clean_conora19_content = [word for word in clean_conora19_content if word not in stops and len(word) > 1]

    clean_conora19_all = []

    ##### 대문자를 소문자로 바뀌기 
    for text in clean_conora19_content :
        clean_conora19_all.append(text.lower()) ## lower() 소문자로 변환하기
        
    ### 데이터 처리를 이용하기 위한 특징을 단어별로 정리하기
    total_conora19 = []
    total_conora19 = [token for msg in clean_conora19_all for token in str(msg).split()]



    ### customer 단어도 정제하기 (일반적인 단어가 아니라,불필요한 단어 찾기 )
    clean_total_conora19 = [word for word in total_conora19 if word not in stops and len(word) > 1]

    text = nltk.Text(clean_total_conora19, name='NMSC')
    print("nltk Number:",len(set(text.tokens)))
    print(text.vocab().most_common(30)) ### 제일 많이 나온 횟수로 적용하기 
    print('\n\n')

    text_vocab = text.vocab().most_common(30)
    dict_text = dict(text_vocab)
    print("dict:",dict(text_vocab)) 
    
    return dict_text 

if __name__ == '__main__':
    
    dictText = getWordCloud()
    print(dictText)


##### 단어, 사용한 횟수로 표시함 