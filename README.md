# Movie Taste Similarity Analysis using Letterboxd profiles

Streamlit app that analyses the cinema taste similarity of pairs of users of the social media Letterboxd 

### How to run
This app is not deployed on Streamlit's cloud, so needs to be run locally. To do so, follow the following steps:
Clone the repository and install dependencies. Run the following command: 
`cd streamlit_app`
`streamlit run strealit_app.py`

### Functionality and quick tutorial:
The page **User selection** allows to introduce two Letterboxd usernames. The app checks if the usernames have already been searched (in this case loads the already saved tables) and scraps the data out of Letterboxd if necessarily. It displays the table of all see and rated films for both users.
![user_selection](https://user-images.githubusercontent.com/38510928/216833056-2c92bd80-ad07-4efb-a9c8-d6fcd6890a18.png)


The page **Analysis** displays a dashboard with the user comparison analysis. Individual indicators (movies watched, rated...) and also comparative indicators (movies in common, movie selection similarity, rating similarity...) are computed and displayed.
![analysis](https://user-images.githubusercontent.com/38510928/216833062-feddd504-c45c-42d8-a6cd-4a86ddb55079.png)
