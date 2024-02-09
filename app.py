import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from urlextract import URLExtract
from textblob import TextBlob
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    
    df=preprocessor.preprocess(data)
    st.title('Top Statitics')
    st.dataframe(df)
    #fetch unique data
    user_list = df['users'].unique().tolist()
    user_list.remove('group notificcation')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show Analysis Wrt ",user_list	)



    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messaages,links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media shared')
            st.title(num_media_messaages)
        with col4:
            st.header('Links shared')
            st.title(links)
        #monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Timeline')
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(daily_timeline['per_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.header('Most Busy Days')
            busy_day=helper.week_activity_map(selected_user ,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Months')
            busy_months=helper.month_activity_map(selected_user ,df)
            fig,ax=plt.subplots()
            ax.bar(busy_months.index,busy_months.values,color='orange')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        st.title('Weekly Activity')
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)


        #finding busiest user 
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df=helper.busy(df)
            fig,ax=plt.subplots()
            
            
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        # creating word_cloud:
        st.title('Word Cloud')
        df_wc=helper.create_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most commom words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commom Words')
        st.pyplot(fig)

        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
        #chat sentiment trend
        st.title('Sentiment Trend Over Time')
        daily_sentiment = helper.calculate_daily_sentiment(df[['per_date','message']])
        st.line_chart(daily_sentiment.set_index('per_date'))

    search_word = st.sidebar.text_input('Search for word:', '')
    if st.sidebar.button('Search'):
        word_count,chat_sentiment,daily_sentiment= helper.count_word_occurrences(df['message'],search_word)
        if word_count:
            st.success(f'The word "{search_word}" appears {word_count[search_word.lower()]} times in the chat.')
            st.success(f'The overall sentiment of the chat is: {chat_sentiment}')
            searched_word_sentiment = TextBlob(search_word).sentiment.polarity
            if chat_sentiment > 0:
                st.success(f'The sentiment of "{search_word}" is positive.')
            elif chat_sentiment < 0:
                st.success(f'The sentiment of "{search_word}" is negative.')
            else:
                st.success(f'The sentiment of "{search_word}" is neutral.')

            

        else:
            st.warning(f'The word "{search_word}" does not appear in the chat.')






