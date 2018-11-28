# How to run
Please clone project in git hub using git@github.com:MarioFabre/Marketing-Funnel.git
To RUN the application, you need to install Docker, because there's a postgres database container in order to manipulate data.
After Docker installed, Please go into project Folder and execute below:
- docker-compose up -d

Warning:    That project was created in Linux environment. Locale configuration in file 3 can not works in Windows.

I kept in project the zip file from Kaggle. But if you want to replace it, please download respective files from Kaggle using link below. https://www.kaggle.com/olistbr/marketing-funnel-olist/downloads/marketing-funnel-olist.zip/2
Remember to include zip file in data project folder (app/data).

After that, you'll be able to run 1-unzipFile.py to get all csv files.

Please run 2-database.py to create all tables in postgres

Please run 3-insertData.py to insert al data from csv in table created in above step

Please run 4-insertConsolidate.py to create the OLIST_CONSOLIDATE table based on link between 2 tables created above.

Please run 5-analysis.py to plot a image that show all different origin and your respective quantity. It's a very good way to understand the 
greater flow of client origin, it allow Marketing to take some actions based on it

Please run 6-analysis to plot the general Qualified Leads (MQL) per Month in 2018

Please run 7-analysis to plot a comparison between all MQL and Closed Deals, in order to know how many wins for each Lead and all rejection rate. First step to analyze why it happens.

Please run 8-analysis to plot more advanced detail from Origin. Here we can see how many Closed Deals for each Origin. It's not enough to know best origin if this origin has a bad convertion.

Please run 9-downReport to generate a report with bad indicators like Origin, Sales development Representative, Sales Representative, business segment and landing page

Please run 10-topReport to generate a report with best indicators like Origin, Sales development Representative, Sales Representative, business segment and landing page
1. That type of report, we'll get the opportunity to create a new marketing campaign. For example, home_decor or health_beauty in Social Media, besides focusing on SEO key-words envolving those segments listed.
2. We don't have enough information if client has company or not. It could be a great opportunity to create a new marketing campaign incentivating your clients about all benefits to legalize a company. It'll transmit confidence and credibility saying that Olist is not worry just about new clients, but their performance and development as well.
3. In "Best Origin" we can see a lot of qualified leads opportunities in "unknown" origin, that there's no specific origin, anyway, a alert shoud be given here to discover where that leads came from

Please run 11-analysis to plot an image containing a total "Closed Deal'  per week day. It's great to know whats going on next week.

If you have any question, feel free in contact me! :)

