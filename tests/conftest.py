from textwrap import dedent

PREDICTION_1 = dedent("""\
    Let's think step by step:

    Brayan Perea was born on 25 February 1993.
    He began his professional career with Deportivo Cali, making his first team debut in 2011.
    In 2013, he joined Lazio (an Italian Serie A club) on a five-year deal for €2.5 million.
    His debut for Lazio was on 25 September 2013.
    The question asks which team he played for in November 2014.
    From the context, it states: "Perea spent the following campaigns out on loan, representing Perugia, Troyes AC and CD Lugo."
    "The following campaigns" refers to after joining Lazio in 2013.
    So, after joining Lazio in 2013, he went on loan during the 2013–2014 and 2014–2015 seasons.
    The loans were to Perugia, Troyes AC, and CD Lugo.
    Since the timeline is sequential:
    ...

    However, we must answer based only on the provided context.

    And since the text says "spend the following campaigns out on loan, representing Perugia, Troyes AC and CD Lugo" — in that sequence — and November 2014 falls in the 2014–2015 season (second campaign), then the club would be Troyes AC.

    Therefore, in November 2014, he was playing for Troyes AC.

    Thus, the correct answer is: Troyes AC.

    Thus, the correct answer is: Troyes AC.""")

PREDICTION_2 = dedent("""\
    Let's solve this step by step:

    We are given a date: August 1814.
    We are asked to find the date that is 10 years before that.
    Subtracting 10 years from 1814:
    1814 − 10 = 1804.
    The month remains the same (August), since we're only subtracting years, not months or days.
    Therefore, 10 years before August 1814 is August 1804.
    Thus, the correct answer is: August 1804.""")

PREDICTION_3 = dedent("""\
    Step 1: Identify the person in question — John Williams (footballer, born 1968).

    Step 2: Determine which teams he played for according to the context.

    The context lists the teams he played for:

    Premier League: Coventry City
    Football League: Swansea City, Notts County, Stoke City, Wycombe Wanderers, Hereford United, Walsall, Exeter City, Cardiff City, York City, Darlington
    Non-league: Cradley Town, Kidderminster Harriers, Bath City, Redditch United, Evesham United, Weston-super-Mare, Stourbridge, Willenhall Town, Boldmere St. Michaels
    Step 3: Consider the timeline provided: from 1998 to 2000, and that he released Cardiff City from his contract in 2002.

    Note: The release from Cardiff City in 2002 implies that he was playing for Cardiff City at some point prior to 2002.

    Step 4: Determine which team he played for between 1998 and 2000.

    Since the list does not include specific dates or timelines for each team, we must infer based on logical sequence and context. However, the given context does not provide any specific start or end years for the clubs.

    We know he played for Cardiff City and left in 2002 — so he must have been with Cardiff City at some point before 2002. But we are asked about 1998–2000.

    Can we determine which team he played for during that window?

    The context does not specify when he joined or left any of these clubs, nor does it provide dates for transfers. Therefore, we cannot definitively assign a team to the period 1998–2000 based solely on the given information.

    Additionally, the question implies that he released Cardiff City in 2002 — meaning he was with them before that. That means he could have been at Cardiff City during 1998–2000. But that is speculation.

    Since the context doesn't provide any details on transfer dates or timelines for individual clubs, and we cannot determine which team he was at between 1998 and 2000 based on the information provided, we cannot with certainty assign a team to that time period.

    Hence, the information is insufficient to determine which team John Williams played for between 1998 and 2000.

    Therefore, the answer cannot be determined from the context.

    Thus, the correct answer is: [unanswerable]
""")

PREDICTION_4 = dedent("""\
    Let's break this down step by step:

    The question is about John Williams (footballer, born 1968) and specifically which team he played for between 1998 and 2000.

    We are told that he released Cardiff City from his contract in 2002. This implies that he was at Cardiff City before 2002, and likely during or before the 1998–2000 timeframe.

    However, the context provided lists the clubs he played for, which are:

    Coventry City (Premier League)
    Swansea City
    Notts County
    Stoke City
    Wycombe Wanderers
    Hereford United
    Walsall
    Exeter City
    Cardiff City
    York City
    Darlington
    Non-league clubs: Cradley Town, Kidderminster Harriers, Bath City, Redditch United, Evesham United, Weston-super-Mare, Stourbridge, Willenhall Town, Boldmere St. Michaels
    The question asks which team he played for from 1998 to 2000. Since he left Cardiff City in 2002 (released from contract), he must have been at Cardiff City during or before that time. But we are not given exact dates for his tenure at each club.

    However, the club "Cardiff City" appears in the list, and since he left in 2002, it is logical that he played for Cardiff City around the 1998–2000 period.

    The key point: the question is specifically asking about 1998 to 2000. There is no mention of any specific team during that window in the context — all clubs are listed, but with no timeframes.

    Given that Cardiff City is the only club explicitly mentioned that he left in 2002, and assuming he was with them during that timeframe unless stated otherwise, it is plausible that he played for Cardiff City from 1998 to 2000.

    But the context does not provide any dates for when he joined or left any of the clubs. So, without timeframes, we cannot definitively assign 1998–2000 to any club.

    We have no evidence in the context that he played for any team between 1998 and 2000 other than those listed.

    Since the only team he left in 2002 is Cardiff City, and the timeframe in question is 1998–2000, it is the most likely candidate.

    Thus, the correct answer is: Cardiff City.""")

PREDICTION_5 = dedent("""\
    Let's analyze the dialogue step by step to determine what makes the most sense in the context of the <mask>.

    Dialogue:

    Person1: What did you say?
    Person2: I said it's a lovely day. Why don't we go for a walk?
    Person1: Well, I feel a little tired.
    Person2: Come on! A little labor, much health.
    Person1: Then can you wait a few minutes? I want to finish writing this letter.
    Person2: Don't take too long. It would be a shame not to take advantage of such lovely weather.
    Person1: I won't be long. <MASK>. Why don't you go ahead and I'll meet you in the park?
    Person2: I believe I will. Look for me near the lake.

    We are to choose appropriate options to substitute the <mask>.

    Now, evaluate the options:

    A. No more than ten months
    B. No more than ten minutes
    C. No more than five minutes
    D. No more than two years

    Contextual Clue:
    Person1 says "I won't be long" — implying a short time.
    They are still writing a letter, and the second person is suggesting they go for a walk now.
    The weather is lovely, and the second person is urging them not to delay.
    So, the time frame must be very short — plausible in the context of finishing a letter.

    Option A: "No more than ten months" — that's a long time. Doesn’t align with "I won't be long."
    Option B: "No more than ten minutes" — reasonable, short time, fits with "won't be long."
    Option C: "No more than five minutes" — even shorter, very plausible and fits better with "won't be long."
    Option D: "No more than two years" — extremely long — totally inconsistent with the context.

    So, B and C are both reasonable and within the context.
    Both are short durations and reasonable for finishing a letter.

    Note: The sentence says: "I won't be long. <MASK>. Why don't you go ahead..." — so the <mask> is a time commitment, and the next sentence is an invitation for the other person to go ahead.

    Therefore, the correct options are those that convey a short time frame — clearly B and C.

    A and D are implausible — too long.

    Thus, the correct answer is: B, C.""")
