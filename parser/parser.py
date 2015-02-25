import simplejson as json
from textblob import TextBlob
import sys

# ============================= business ====================================

json_data = open('yelp_academic_dataset_business.json')
business_tbl = open('business_tbl', 'w')

for line in json_data:
    try:
        data = json.loads(line)

        # extract data from yelp-business-dataset
        business_id = data['business_id']
        review_cnt  = data['review_count']
        stars       = data['stars']

        output = business_id + '#' + str(review_cnt) + '#' + str(stars) + '\n'
        # print output
        business_tbl.write(output)

    except ValueError as e:
        print e

business_tbl.close()
json_data.close()

# ============================= review ======================================

json_data = open('yelp_academic_dataset_review.json')
review_tbl = open('review_tbl', 'w')

for line in json_data:
    try:
        data = json.loads(line)

        business_id = data['business_id']
        text = data['text']
        testimonial = TextBlob(text)
        polarity = "{:.2f}".format(testimonial.sentiment.polarity)
        subjectivity = "{:.2f}".format(testimonial.sentiment.subjectivity)
        vote_cnt = data['votes']['funny'] + data['votes']['useful'] + data['votes']['cool']

        output = business_id + '#' + polarity + '#' + subjectivity + '#' + str(vote_cnt) + '\n'

        review_tbl.write(output)

    except ValueError as e:
        print e

review_tbl.close()
json_data.close()

# ============================= tips ======================================

json_data = open('yelp_academic_dataset_tip.json')
tips_tbl = open('tips_tbl', 'w')

for line in json_data:
    try:
        data = json.loads(line)
        business_id = data['business_id']
        likes       = data['likes']
        text = data['text']
        testimonial = TextBlob(text)
        polarity = "{:.2f}".format(testimonial.sentiment.polarity)
        subjectivity = "{:.2f}".format(testimonial.sentiment.subjectivity)

        output = business_id + '#' + str(likes) + '#' + polarity + '#' + subjectivity + '\n'
        tips_tbl.write(output)

    except ValueError as e:
        print e

tips_tbl.close()
json_data.close()


