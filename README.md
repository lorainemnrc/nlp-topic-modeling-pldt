![img_banner2](https://github.com/lorainemnrc/nlp-topic-modeling-pldt/assets/23328647/19eacd06-f0ed-4e89-9513-33150bff0be4)

<h1 style="color: #1048CB"><b>Overview</b></h1>

<p align="justify"> &emsp;
  Internet disconnection will result in disruption in business processes and operations, with the effect trickling down to individual Internet users. It is estimated that for a highly Internet-connected country, the per day impact of a temporary shutdown of the Internet and all of its services would be on average $23.6 million per 10 million population. Apart from the economic consequences of Internet disruptions, it will also result in reduced productivity, unclear messaging and communication, and the focus of this project, which is the increase in customer complaints.
</p>

<p align="justify"> &emsp;
  In this project, we want to identify the underlying characteristics and types of user complaints that would allow internet providers to appropriately assign user concerns to the right handling department. This initiative will speed up the resolution time and effectively improve customer experience. Given this objective in mind, we explore the tweets from the past seven days from November 29, 2022, focusing specifically on the following questions: 

  1.	What are the topics/ types of complaints we uncovered and how will this be interpreted? 
  2.	How can these topics be used by our stakeholders, which in this case the internet providers, in improving customer experience, in terms of effectively and efficiently addressing customer concerns? 
</p>

<h1 style="color: #1048CB"><b>Data Source</b></h1>

This work focuses on uncovering customer concerns based on people's tweets to PLDT's Customer Service Accounts, and only tweets within the last 7 days from 29 November 2022 were considered. The whole extraction, transformation, and loading of data is written in the `tweets_etl.py` file, which is used in this notebook as a module for the data preparation process.

The tweets collected have 14 features and a brief definition of each are listed as follows:

<br>
<center style="font-size:12px;font-style:default;"><b>Table 1. Tweet - Data Dictionary</b></center>

|Feature    | Data Type     | Description                                                                           |
|:--------------|:-------------|:--------------------------------------------------------------------------------------|
|lang|string|The language of a Tweet, if detected by Twitter
|possibly_sensitive|boolean|This field indicates a content may be recognized as sensitive
|id|string|The unique identifier of the requested Tweet
|conversation_id|string|The Tweet ID of the original Tweet of the conversation 
|text|string|The actual UTF-8 text of the Tweet
|created_at|datetime|Creation time of the Tweet
|author_id|string|The unique identifier of the user who posted the Tweet
|in_reply_to_user_id|string|If the represented Tweet is a reply, this field will contain the original Tweet’s author ID
|public_metrics.retweet_count|integer|The number of times a public Tweet was retweeted at the time of the request 
|public_metrics.reply_count|integer|The count of replies to a public Tweet at the time of request
|public_metrics.like_count|integer|The count of likes of a public Tweet at the time of request
|public_metrics.quote_count|integer|The number of times a public Tweet was quoted at the time of the request

<br>
<center style="font-size:12px;font-style:default;"><b>Table 2. Derived Features - Data Dictionary</b></center>


|Feature    | Data Type     | Description                                                                           |
|:--------------|:-------------|:--------------------------------------------------------------------------------------|
|created_at_hour|integer|The hour a Tweet was created
|day_of_week|object|The day a Tweet was created


#### Web API Scraping


1,541 tweets accompanied by 14 selected features such as the text of a user’s tweet to @PLDT_Cares and the time the tweet was tweeted.

The `https://api.twitter.com/2/tweets/search/recent` endpoint was used to get the tweets where we passed `(@PLDT_Cares OR @PLDTEnt_Cares) -from:PLDT_Cares` as the values of our query parameter to contain the scope of our search to tweets made by individuals that are addressed to the PLDT_Cares Twitter account.

   * `(@PLDT_Cares OR @PLDTEnt_Cares)` captures tweets that may only mention the latter but are in fact addressed to the former. Upon visual inspection of several recent tweets to PLDT_Cares, some included @PLDTEnt_Cares, another customer service account managed by PLDT for their other products.
    
  * `-from:PLDT_Cares` and `-from:PLDTEnt_Cares`, on the other hand, excluded tweets made by PLDT in response to tweets that mentioned @PLDT_Cares and @PLDTEnt_Cares.
    
  * `-is_retweet` and `-is_quote`, excluded retweets and quotations of tweets to PLDT.

#### Database Creation

The scraped tweets using the Twitter API were written into a table in an SQL database for further processing and analysis. 

<h1 style="color: #1048CB"><b>Highlights</b></h1>

<p align="justify"> &emsp; 
PLDT customers have become more comfortable with voicing out their grievances about PLDT services online. While official channels such as phone consultations and websites are always available, customers found that it is quicker and easier to complain on Twitter due to their immediate access to the internet and social media. From a study conducted by Customer Care Measurement & Consulting in 2021, the number of customers who preferred airing out grievances in digital space tripled from 2017 to 2020. Specifically, for PLDT customers, the publish time of the tweets revealed that most of them published tweets from midnight until 4:00 a.m. It is important to note that PLDT often conducts its maintenance during this time, to prevent disrupting critical business processes for its subscribers during the day. Although our results revealed that the tweets have common themes and can be grouped into distinct, exhaustive topics, the Twitter users were mostly only concerned about their own connectivity issues and no collective sentiment as observed in the lack of viral tweets in the timeframe.
</p>

<p align="justify"> &emsp; 
Compared to LSA, NMF was able to uncover more relevant topics. In an article by Albanese (2022), he compared multiple topic modeling techniques and mentioned that multiple studies argued the superior results of NMF over LSA in terms of interpretability and clarity of the identified topics. In fact, in this study, most topics generated from LSA were similar to each other and were unable to distinguish customer concerns. Topics generated from NMF were able to identify and distinguish customer concerns: No First Action Response, Long Waiting Time, Automated Responses, Disconnection, Line Relocation Inquiry, Billing Concerns, and Feedback. These topics were verified to coincide with some of the actual categories PLDT uses to segregate customer concerns. Together with LSA, the topics would cover half of the categories used by PLDT. Lastly, although NMF has better results, it should be noted that there would be different approximations of the matrices in NMF for every run of the algorithm. To have reproducible matrices and results, the random state should always be specified.
</p>
