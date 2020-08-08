from flask import Flask, render_template, request,redirect,flash,url_for
from sentiment import getSentiment
from wordcloud import getWordCloud
import os

app = Flask(__name__)

@app.route('/board')
def board_list() : 
    
    
    sentiment_result = getSentiment() 
    world_result = getWordCloud() 
    
    print(sentiment_result)
    
    return render_template("spray.html")



if __name__ == '__main__':
    #서버 실행
   port = int(os.getenv('PORT',5000))
   print("Starting app on port %d" % port)
   app.run(debug=True, port=port, host='0.0.0.0')