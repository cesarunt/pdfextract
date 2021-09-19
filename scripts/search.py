import re

text = """
Method
Participants and procedures
Our study was conducted among ﬁve small- and medium-sized ﬁrms (with less than 500
employees) in Zhejiang Province of Eastern China. With management support, one of the
authors distributed 500 matched questionnaires to mainly manufacturing manual workers
and their supervisors. Participants completed the survey on a voluntary basis and were
given a ten-yuan gift as a token of gratitude. Most employees completed the survey in the
canteen or in the dormitory after working hours. The surveys included demographic

)
T
P
(
 
9
1
0
2
 
l
i
r
p
A
 
8
1
 
8
1
:
9
1
 
t

A
 
y
t
i
s
r
e
v
i
n
U

 
l
a
m
r
o
N
 
g
n
i
j
i
e
B
 
y
b
 
d
e
d
a
o
l
n
w
o
D


Page_06
CMS
12,3

596

variables and a cover letter that summarized the study’s purpose and assured the
respondents conﬁdentiality and anonymity. The data were collected independently: one
survey completed by employees and the other by their supervisors. In addition, data
collection was time-lagged to reduce common method bias (Podsakoff et al., 2003). In the
ﬁrst round, employees answered the survey about HR practice and 473 valid surveys were
collected with an initial response rate of 94.6 per cent. Then two weeks later, all employees
who participated in the ﬁrst survey were invited to complete the second survey on work
engagement and job crafting. Their immediate supervisors responded to a shorter
questionnaire regarding employees’ task performance and OCB.

In total, 455 subordinate–supervisor dyads were matched, resulting in a response rate of
91.0 per cent. Nearly two-thirds of the employees were male (34.3 per cent female
employees). Of note, 20 per cent of the sample included younger generation employees below
25 years old. About half the employees had worked in their organizations for more than
three years (46.3 per cent above three years). Four-ﬁfths of the sample were educated at high
school
level and below (only 9.9 per cent were graduates). The questionnaire was
anonymous and did not require respondents to divulge any kind of identifying information
except an ID number, which enabled matching with their supervisors’ evaluation of their
performance.
"""

text_parser = text
# text_parser = text.split("\n")
# text_parser = (''.join(text))
sample = "sample"

# for value in text_parser:
    # doc = docx.Document()
    # p = document.add_paragraph()
patt = re.search(rf"\b{sample}\b", text_parser, re.IGNORECASE)
# print("value "+ str(patt))
if patt != None:
    print("UBICATED ... ")
    print(patt)
    print(text_parser[patt.end(0):patt.end(0)+10])

    value_1 = text_parser[:patt.start(0)]
    value_2 = sample.upper()
    value_3 = text_parser[patt.end(0):]
    values = [tuple(["N", value_1]), tuple(["I", value_2]), tuple(["N", value_3])]

print("Values")
for item in values :
    print("\n" + str(item))