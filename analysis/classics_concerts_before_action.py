from data.processed.merged_data import combined_df
from analysis.list_creation import (unique_patrons, unique_concert_attendee,
    unique_donors, unique_subscribers, unique_flex, unique_comp,
    unique_single_paid, unique_single_non_sub, unique_attendee_donated,
    unique_subscribers_donated, unique_single_non_sub_donated)
from analysis.functions.concert_counting import (concerts_before_subscription,
    concerts_before_donation_counter, total_concerts_filtered)
from analysis.functions.ltv import (LTV_basic, LTV_improved)


#### 2) Number of Single Concerts Before Subscription
# Note: Only includes patrons that purchased a subscription
res_concerts_b4_subscribing = concerts_before_subscription(combined_df, unique_subscribers)
########


#### 3) Number of Concerts Before First Donation
# Note: Only includes patrons that made a donation and attended at least one concert
ret_cbfd_all = concerts_before_donation_counter(combined_df, unique_attendee_donated)
res_avg_concerts_cbfd_all = ret_cbfd_all[0]
res_avg_first_donation_cbfd_all = ret_cbfd_all[1]
########



#### 4) Number of Concerts Before First Donation for Subs
# Note: Only includes patrons that purchased a subscription and made a donation
ret_cbfd_sub = concerts_before_donation_counter(combined_df, unique_subscribers_donated)
res_avg_concerts_cbfd_sub = ret_cbfd_sub[0]
res_avg_first_donation_cbfd_sub = ret_cbfd_sub[1]
########



#### 5) Number of Concerts Before First Donation for Singles
# Note: Only includes patrons that never subscribed and made a donation and attended
#   at least one concert
ret_cbfd_sgl = concerts_before_donation_counter(combined_df, unique_single_non_sub_donated)
res_avg_concerts_cbfd_sgl = ret_cbfd_sgl[0]
res_avg_first_donation_cbfd_sgl = ret_cbfd_sgl[1]
######## 


#### 6) Number of Concerts Attended by Singles that Don't Sub
res_avg_concerts_non_subs =\
    total_concerts_filtered(combined_df, unique_single_non_sub)\
    / len(unique_single_non_sub)
########
    
    
#### 7) Number of Concerts Attended by Singles PAID (non sub,flex,comp)
res_avg_concert_paid_singles_only =\
    total_concerts_filtered(combined_df, unique_single_paid)\
    / len(unique_single_paid)
########
    

#### 8) Lifetime Value Basic
ltv_basic = LTV_basic(combined_df, unique_concert_attendee)
ltv_basic_subs = LTV_basic(combined_df, unique_subscribers)
########



#### 9) Lifetime Value Improved
ltv_improved = LTV_improved(combined_df, unique_concert_attendee)
ltv_improved_single = LTV_improved(combined_df, unique_single_non_sub)
ltv_improved_subs = LTV_improved(combined_df, unique_subscribers)
########
