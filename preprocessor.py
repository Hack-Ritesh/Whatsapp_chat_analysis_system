import re
import pandas as pd

def preprocess(data):
	pattern="\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
	mssg=re.split(pattern,data)[1:]
	dates=re.findall(pattern,data)
	df=pd.DataFrame({'user_message':mssg,'message_dates':dates})
	df['messsage_dates']=pd.to_datetime(df['message_dates'],format='%d/%m/%y, %H:%M - ')
	df.rename(columns={'message_dates':'date'},inplace=True)
	df=df.drop('date',axis=1)
	df.rename(columns = {'messsage_dates':'date'}, inplace = True)
	user=[]
	messages=[]
	for message in df['user_message']:
	    entry=re.split('([\w\W]+?):\s',message)
	    if entry[1:]:
	        user.append(entry[1])
	        messages.append(entry[2])
	    else:
	        user.append('group notificcation')
	        messages.append(entry[0])
	df['users']=user
	df['message']=messages
	df.drop('user_message',axis=1,inplace=True)

	df['year']=df['date'].dt.year
	df['Month']=df['date'].dt.month_name()
	df['Day']=df['date'].dt.day
	df['hour']=df['date'].dt.hour
	df['Minute']=df['date'].dt.minute
	df['day_name'] = df['date'].dt.day_name()
	df['month_num'] = df['date'].dt.month
	df['per_date']=df['date'].dt.date
	df['month'] = df['date'].dt.month_name()

	period = []
	for hour in df[['day_name', 'hour']]['hour']:
	    if hour == 23:
	        period.append(str(hour) + "-" + str('00'))
	    elif hour == 0:
	        period.append(str('00') + "-" + str(hour + 1))
	    else:
	        period.append(str(hour) + "-" + str(hour + 1))

	df['period'] = period

	return df