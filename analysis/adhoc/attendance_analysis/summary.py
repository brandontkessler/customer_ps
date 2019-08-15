from data.interim.all_tickets import tix_prep
import pandas as pd

clx = tix_prep('Clx')
pop = tix_prep('Pops')
chbr = tix_prep('Chamber')
con = tix_prep('Connections')
fam = tix_prep('Family')
org = tix_prep('Organ')
spc = tix_prep('Specials')
smr = tix_prep('Summer')

tix_copy = pd.concat([clx,pop,chbr,con,fam,org,spc], ignore_index=True)

tix_to_manip = tix_copy.copy()

def fy_check(month_number):
    if month_number < 7:
        return 0
    else:
        return 1


tix_to_manip['year'] = [i.timetuple().tm_year + fy_check(i.timetuple().tm_mon)\
            for i in tix_to_manip['performance_date']]


attendance_dict = {i: [0,0,0,0] for i in tix_to_manip['year']}
# Each key is assigned to a value which is a list of four values. 
#   The first represents total available tickets. The second 
#   value represents total attended concerts. The third represents the total
#   tickets sold. The fourth represents the % attended of available tickets.


# Total Available
for i in tix_to_manip['year']:
    attendance_dict[i][0] += 1

# Total Attended
for i in zip(tix_to_manip['year'],tix_to_manip['attended']):
    if i[1] == 'Attended':
        attendance_dict[i[0]][1] += 1

# Total Purchased Tickets
for i in zip(tix_to_manip['year'],tix_to_manip['transaction_amount']):
    if i[1] > 0:
        attendance_dict[i[0]][2] += 1

# Percent of Total Available
for k,v in attendance_dict.items():
    v[3] = v[1] / v[0]
    
pd.DataFrame(attendance_dict).to_excel("attendance.xlsx", engine='xlsxwriter', index=False)

