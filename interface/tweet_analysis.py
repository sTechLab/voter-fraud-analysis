import streamlit as st
from data_tools import load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .utils import (
    plot_hourly_coverage,
    lookup_parsed_tweet_data,
    most_common_hashtags,
    most_common_tokens,
    create_crawled_terms_df
)
import numpy as np
import seaborn as sns
from collections import Counter
from PIL import Image

# Plot styles
import matplotlib.style as style
import json
from collections import Counter

style.use("seaborn-poster")
style.use("ggplot")

LIMIT = None

CRAWLED_TERMS = load_crawled_terms("./keywords-3nov.txt")


def get_tweet_analysis_page(shared_state):
    st.header("Tweet Analysis")

    user_df = shared_state.user_df
    old_tweet_df = shared_state.old_tweet_df
    recent_tweet_df = shared_state.recent_tweet_df
    retweet_df = shared_state.retweet_df
    crawled_terms_df = shared_state.crawled_terms_df
    df_counts_by_hour = shared_state.df_counts_by_hour
    df_most_common_hashtags = shared_state.df_most_common_hashtags
    df_cooccurrence = shared_state.df_cooccurrence

    st.subheader("Basic stats")
    st.markdown(
        """
        **Number of tweets:** {:,}  
        **Number of tweets after October 23rd:** {:,}  
        **Number of retweets:** {:,}  
        **Number of users:** {:,}

    """.format(
            len(recent_tweet_df.index) + len(old_tweet_df.index),
            len(recent_tweet_df.index),
            len(retweet_df.index),
            len(user_df.index),
        )
    )

    st.subheader("Infomap Clustering (on 200k retweets)")
    infomap_img = Image.open('./interface/img/infomap-clustering.png')
    st.image(infomap_img, use_column_width=True)

    st.subheader("Coverage")
    st.markdown(
        """
        **Earliest tweet:** {}  
        **Latest tweet:** {}  
        **Earliest retweet:** {}  
        **Latest retweet:** {}  

    """.format(
            old_tweet_df.timestamp.min(),
            recent_tweet_df.timestamp.max(),
            retweet_df.timestamp.min(),
            retweet_df.timestamp.max(),
        )
    )

    st.subheader("Hourly Coverage")
    st.pyplot(plot_hourly_coverage(df_counts_by_hour, 'retweet count', "Retweets"))
    st.pyplot(plot_hourly_coverage(df_counts_by_hour, 'tweet count', "Tweets since Oct 23rd"))

    col1, col2 = st.beta_columns(2)
    col1.subheader("Most common hashtags")
    col1.dataframe(most_common_hashtags(df_most_common_hashtags, "all tweets", 25))

    col2.subheader("Most common tokens")
    col2.dataframe(most_common_tokens(recent_tweet_df, 25))

    st.subheader("All crawled terms (since 3rd of November)")

    st.dataframe(crawled_terms_df)

    # crawled_term_threshold = st.number_input(
    #     "Exclude crawled terms under a certain threshold", value=5000, step=500
    # )

    # crawled_terms_df = crawled_terms_df[
    #     crawled_terms_df["tweet count"] > crawled_term_threshold
    # ]

    # st.markdown(
    #     "Filtered down to {} terms ({} in total)".format(
    #         len(crawled_terms_df.index), len(CRAWLED_TERMS)
    #     )
    # )

    st.subheader("Co-occurrence matrix (for terms with count > 5000)")

    st.dataframe(df_cooccurrence)

    co_occurrence_diagonal = np.diagonal(df_cooccurrence)

    with np.errstate(divide="ignore", invalid="ignore"):
        co_occurrence_fraction = np.nan_to_num(
            np.true_divide(df_cooccurrence, co_occurrence_diagonal[:, None])
        )

    fig = plt.figure()
    st.subheader("Co-occurence heatmap (inverted log-scaling)")
    st.markdown("Closer to 0 means higher correlation")
    with st.echo():
        co_occurrence_heatmap_df = pd.DataFrame(
            np.log(co_occurrence_fraction),
            index=df_cooccurrence.index,
            columns=df_cooccurrence.columns,
        )
    np.fill_diagonal(co_occurrence_heatmap_df.values, np.nan)
    sns.heatmap(
        co_occurrence_heatmap_df,
        cbar=False,
        square=True,
        annot=True,
        vmin=-5,
        vmax=0,
        center=-2,
        cmap="PuBu",
        linecolor="black",
    )

    plt.tick_params(
        axis="both",
        which="major",
        labelsize=10,
        labelbottom=False,
        bottom=False,
        top=False,
        labeltop=True,
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)


if __name__ == "__main__":
    get_tweet_analysis_page()
