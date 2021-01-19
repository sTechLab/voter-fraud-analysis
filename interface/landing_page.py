import streamlit as st
from collections import defaultdict
import pandas as pd
import numpy as np
from PIL import Image

img_retweet_graph = Image.open("./interface/img/retweet-graph.png")
img_retweet_graph_suspended = Image.open(
    "./interface/img/retweet-graph-suspended-orange-min.jpg"
)


def get_landing_page(shared_state):
    coverage_stats = shared_state.coverage_stats

    st.header("VoterFraud2020")
    st.markdown(
        """
        We are making publicly available [VoterFraud2020](https://github.com/sTechLab/VoterFraud2020), a multi-modal Twitter 
        dataset with 7.6M tweets and 25.6M retweets that include key phrases 
        and hashtags related to voter fraud claims between October 23rd and December 16th. 
        The data also includes the full set of links and YouTube videos shared in these tweets, 
        with data about their spread in different Twitter sub-communities. 

        The methodology for our data collection including the tracked keywords is detailed in [the paper 
        available from Arxiv](link-to-paper). 
        
        Our hope is that the dataset will be used to study the spread, reach, and 
        dynamics of the voter fraud claims campaign on Twitter. The data can help expose, for example, how different 
        public figures spread different claims, and what kind of engagement various narratives received. 
        

        The paper, dataset, and the initial analysis provided here is a collaboration between the 
        [Social Technologies Lab](https://s.tech.cornell.edu/) at Cornell Tech and Technion. 
        
        The project was led by Anton Abilov, [Yiqing Hua](http://yiqing-hua.com/), and Hana Matatov. Inquiries should go to Professor Mor Naaman at [mor.naaman@cornell.edu](mailto:mor.naaman@cornell.edu).

        ### Key Takeaways
        - Community detection performed on the dataset reveals that there are 5 main sub-communities involved in the discussion: 
        four communities that seem to promote such claims (*"promoters"*) and one community of *"detractors"* (blue in Figure 1 on this page).
        - The dataset is enhanced with community labels to enable quick study of how URLs, images and youtube videos spread within these sub-communities.
        The navigation on this page provides a quick summary of the top users, tweets, videos and links shared.
        - We identified 99,884 suspended users, allowing the investigation of [Twitter's response](https://blog.twitter.com/en_us/topics/company/2021/protecting--the-conversation-following-the-riots-in-washington--.html) to voter fraud claims.
        Preliminary analyses show that Twitter’s ban actions mostly affected a specific community within the cluster of voter fraud claim promoters (orange in Figure 2).
        - Many of the top YouTube videos shared by promoters of voter fraud claims are still available on YouTube as on 
        January 18th, 2021; all the top ten videos shared by the promoter communities were still online on January 10th. Explore the list on [this page](/?page=Explore+The+Dataset).
        - Additional information about the data and analysis is available in [the paper](link-to-paper).

        ### Privacy and Ethical Considerations
        The dataset was collected and made available according to Twitter's Terms of Service for academic researchers, following 
        established guidelines for ethical Twitter data use. We do not directly share content of individual tweets. 
        By using Tweet IDs as the main data element the dataset does not expose information about users whose data had been removed from the service. 

        *Anton Abilov, Yiqing Hua ([@yiqqqing](https://twitter.com/yiqqqing)), Hana Matatov, Ofra Amir ([@ofraam](https://twitter.com/ofraam)) & Mor Naaman ([@informor](https://twitter.com/informor)).*

    """.format(
            coverage_stats["recent_tweet_count"] - coverage_stats["quote_tweet_count"],
            coverage_stats["quote_tweet_count"],
            coverage_stats["retweet_count"],
        )
    )
    st.subheader("")
    col1, col2 = st.beta_columns(2)
    
    st.image(img_retweet_graph, use_column_width=True)
    st.markdown("""
        **Figure 1:** Five communities in the retweet graph of people posting about voter-fraud claims; the blue cluster on the left side is mostly of detractors of the claim.
    """)
    
    st.image(img_retweet_graph_suspended, use_column_width=True)
    st.markdown("""
        **Figure 2:** Where suspended users were located in the retweet graph (orange); they mostly came from a specific subcommunity of claim promoters.
    """)


if __name__ == "__main__":
    get_landing_page()
