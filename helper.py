from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import emoji




def fetch_stats(selected_user,df):

	if selected_user!='Overall':
		df=df[df['users']==selected_user]
		#fecth the no. of messages
	num_messages= df.shape[0]
	#fetch the no. of words
	words=[]
	for message in df['message']:
	    words.extend(message.split(" "))
    #fetch the no. of media
	num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]
	#fetch no. of links
	extractor=URLExtract()
	links=[]
	for message in df['message']:
	    links.extend(extractor.find_urls(message))

	return num_messages,len(words),num_media_messages,len(links)
#fetch most busy users
def busy(df):
	x=df['users'].value_counts().head()
	df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
	return x,df
def create_cloud(selected_user,df):
	
	f=open('hinglish.txt','r')
	stop_words=f.read()

	if selected_user!='Overall':
		df=df[df['users']==selected_user]

	temp=df[df['users']!='group notificcation']
	temp=temp[temp['message']!='<Media omitted>\n']
	temp=temp[temp['message']!='(file attached)\n']
	def remove_stop_words(message):
		y=[]
		for word in message.lower().split():
		    if word not in stop_words:
		        y.append(word)
		return " ".join(y)


	wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
	temp['message']=temp['message'].apply(remove_stop_words)
	df_wc=wc.generate(temp['message'].str.cat(sep=" "))

	return df_wc

def most_common_words(selected_user,df): 
	f=open('hinglish.txt','r')
	stop_words=f.read()

	if selected_user!='Overall':
		df=df[df['users']==selected_user]

	temp=df[df['users']!='group notificcation']
	temp=temp[temp['message']!='<Media omitted>\n']
	temp=temp[temp['message']!='(file attached)\n']

	words=[]
	for message in temp['message']:
	    for word in message.lower().split():
	        if word not in stop_words:
	            words.append(word)
	return_df=pd.DataFrame(Counter(words).most_common(20))
	return return_df
def emoji_helper(selected_user,df):
	if selected_user!='Overall':
		df=df[df['users']==selected_user]

	emojis=[]
	for message in df['message']:
		emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
	emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

	return emoji_df
def monthly_timeline(selected_user,df):
	if selected_user!='Overall':
		df=df[df['users']==selected_user]
	timeline=df.groupby(['year','month_num','Month']).count()['message'].reset_index()
	time=[]
	for i in range(timeline.shape[0]):
	    
	    time.append((timeline['Month'][i]+"-"+str(timeline['year'][i])))
	timeline['time']=time
	return timeline

def daily_timeline(selected_user,df):
	if selected_user!='Overall':
		df=df[df['users']==selected_user]
	daily_timeline=df.groupby(['per_date']).count()['message'].reset_index()
	return daily_timeline
def week_activity_map(selected_user,df):
	if selected_user!='Overall':
		df=df[df['users']==selected_user]
	return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
	if selected_user!='Overall':
		df=df[df['users']==selected_user]
	return df['month'].value_counts()
def activity_heatmap(selected_user,df):
	if selected_user!='Overall':
		df=df[df['users']==selected_user]
	user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

	return user_heatmap
def count_word_occurrences(chat_series, search_word):
    # Combine all messages into a single string
    all_messages = ' '.join(chat_series)
    days_of_week = re.findall(r'\[(.*?)\]', all_messages)
    day_counts = Counter(days_of_week)

    # Counting occurrences of the search word
    chat_sentiment = TextBlob(all_messages).sentiment.polarity

    word_count = Counter(re.findall(r'\b{}\b'.format(search_word), all_messages, flags=re.IGNORECASE))

    return word_count,chat_sentiment,day_counts
def calculate_daily_sentiment(df):
    sia = SentimentIntensityAnalyzer()
    df['SentimentScore'] = df['message'].apply(lambda x: sia.polarity_scores(x)['compound'])
    daily_sentiment = df.groupby(df['per_date'])['SentimentScore'].mean().reset_index()
    return daily_sentiment


		

