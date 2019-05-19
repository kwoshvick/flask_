import re
import string
import html

class Cleaner:
    def __init__(self):
        self.remove_punctuations = str.maketrans('', '', string.punctuation)


    def clean_tweets(self,tweet):
        html_escaped = html.unescape(tweet)
        comma_replacement = html_escaped.replace(';', '')
        # harmonize the cases
        lower_case_text = comma_replacement.lower()
        # remove urls
        removed_url = re.sub(r'http\S+', '', lower_case_text)
        # remove hashtags
        removed_hash_tag = re.sub(r'#\w*', '', removed_url)  # hastag
        # remove usernames from tweets
        removed_username = re.sub(r'@\w*\s?','',removed_hash_tag)
        # removed retweets
        removed_retweet = removed_username.replace("rt", "", True)  # remove to retweet
        # removing punctuations
        removed_punctuation = removed_retweet.translate(self.remove_punctuations)
        # remove spaces
        remove_g_t = removed_punctuation.replace("&gt", "", True)
        remove_a_m_p = remove_g_t.replace("&amp", "", True)
        final_text = remove_a_m_p
        return final_text




