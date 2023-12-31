from datetime import datetime, timedelta


class Holiday:
    """
    the Holiday class tracks which days are market holidays or weekends.
    in general, there are about 252 trading days per year for equities
    """
    def __init__(self):
        self.m_holiday_map = Holiday.form_holiday_map()

        self.DATE_WEEKDAY = 100
        self.DATE_OPTION_EXPIRATION = 101
        self.DATE_OPTION_EXPIRATION_HOLIDAY = 102
        self.DATE_LAST_DAY_OF_MONTH = 103
        self.DATE_WEEKEND = 200
        self.DATE_HOLIDAY = 201

    def next_business_day(self, curr_date):
        while True:
            curr_date = curr_date + timedelta(1, 0, 0, 0)
            b_business_day = self.is_business_day(curr_date)
            if b_business_day:
                break

        return curr_date

    def prev_business_day(self, curr_date):
        while True:
            curr_date = curr_date - timedelta(1, 0, 0, 0)
            b_business_day = self.is_business_day(curr_date)
            if b_business_day:
                break

        return curr_date

    def is_business_day(self, curr_date):
        week_day = curr_date.weekday()
        # Monday = 0, Friday = 4, Saturday = 5, Sunday = 6

        if (5 == week_day) or (6 == week_day):
            return False

        try:
            str_date = curr_date.strftime("%Y-%m-%d")
            b_holiday = self.m_holiday_map[str_date]
        except KeyError:
            b_holiday = False

        return not b_holiday

    @staticmethod
    def form_holiday_map():
        holiday_map = {'1971-01-01': True, '1971-02-15': True, '1971-04-09': True, '1971-05-31': True,
                       '1971-07-05': True, '1971-09-06': True, '1971-11-25': True, '1971-12-24': True,
                       '1972-02-21': True, '1972-03-31': True, '1972-05-29': True, '1972-07-04': True,
                       '1972-09-04': True, '1972-11-23': True, '1972-12-25': True, '1973-01-01': True,
                       '1973-02-19': True, '1973-04-20': True, '1973-05-28': True, '1973-07-04': True,
                       '1973-09-03': True, '1973-11-22': True, '1973-12-25': True, '1974-01-01': True,
                       '1974-02-18': True, '1974-04-12': True, '1974-05-27': True, '1974-07-04': True,
                       '1974-09-02': True, '1974-11-28': True, '1974-12-25': True, '1975-01-01': True,
                       '1975-02-17': True, '1975-03-28': True, '1975-05-26': True, '1975-07-04': True,
                       '1975-09-01': True, '1975-11-27': True, '1975-12-25': True, '1976-01-01': True,
                       '1976-02-16': True, '1976-04-16': True, '1976-05-31': True, '1976-07-05': True,
                       '1976-09-06': True, '1976-11-25': True, '1976-12-24': True, '1977-02-21': True,
                       '1977-04-08': True, '1977-05-30': True, '1977-07-04': True, '1977-09-05': True,
                       '1977-11-24': True, '1977-12-26': True, '1978-01-02': True, '1978-02-20': True,
                       '1978-03-24': True, '1978-05-29': True, '1978-07-04': True, '1978-09-04': True,
                       '1978-11-23': True, '1978-12-25': True, '1979-01-01': True, '1979-02-19': True,
                       '1979-04-13': True, '1979-05-28': True, '1979-07-04': True, '1979-09-03': True,
                       '1979-11-22': True, '1979-12-25': True, '1980-01-01': True, '1980-02-18': True,
                       '1980-04-04': True, '1980-05-26': True, '1980-07-04': True, '1980-09-01': True,
                       '1980-11-27': True, '1980-12-25': True, '1981-01-01': True, '1981-02-16': True,
                       '1981-04-17': True, '1981-05-25': True, '1981-07-03': True, '1981-09-07': True,
                       '1981-11-26': True, '1981-12-25': True, '1982-01-01': True, '1982-02-15': True,
                       '1982-04-09': True, '1982-05-31': True, '1982-07-05': True, '1982-09-06': True,
                       '1982-11-25': True, '1982-12-24': True, '1983-02-21': True, '1983-04-01': True,
                       '1983-05-30': True, '1983-07-04': True, '1983-09-05': True, '1983-11-24': True,
                       '1983-12-26': True, '1984-01-02': True, '1984-02-20': True, '1984-04-20': True,
                       '1984-05-28': True, '1984-07-04': True, '1984-09-03': True, '1984-11-22': True,
                       '1984-12-25': True, '1985-01-01': True, '1985-02-18': True, '1985-04-05': True,
                       '1985-05-27': True, '1985-07-04': True, '1985-09-02': True, '1985-11-28': True,
                       '1985-12-25': True, '1986-01-01': True, '1986-02-17': True, '1986-03-28': True,
                       '1986-05-26': True, '1986-07-04': True, '1986-09-01': True, '1986-11-27': True,
                       '1986-12-25': True, '1987-01-01': True, '1987-02-16': True, '1987-04-17': True,
                       '1987-05-25': True, '1987-07-03': True, '1987-09-07': True, '1987-11-26': True,
                       '1987-12-25': True, '1988-01-01': True, '1988-02-15': True, '1988-04-01': True,
                       '1988-05-30': True, '1988-07-04': True, '1988-09-05': True, '1988-11-24': True,
                       '1988-12-26': True, '1989-01-02': True, '1989-02-20': True, '1989-03-24': True,
                       '1989-05-29': True, '1989-07-04': True, '1989-09-04': True, '1989-11-23': True,
                       '1989-12-25': True, '1990-01-01': True, '1990-02-19': True, '1990-04-13': True,
                       '1990-05-28': True, '1990-07-04': True, '1990-09-03': True, '1990-11-22': True,
                       '1990-12-25': True, '1991-01-01': True, '1991-02-18': True, '1991-03-29': True,
                       '1991-05-27': True, '1991-07-04': True, '1991-09-02': True, '1991-11-28': True,
                       '1991-12-25': True, '1992-01-01': True, '1992-02-17': True, '1992-04-17': True,
                       '1992-05-25': True, '1992-07-03': True, '1992-09-07': True, '1992-11-26': True,
                       '1992-12-25': True, '1993-01-01': True, '1993-02-15': True, '1993-04-09': True,
                       '1993-05-31': True, '1993-07-05': True, '1993-09-06': True, '1993-11-25': True,
                       '1993-12-24': True, '1994-02-21': True, '1994-04-01': True, '1994-04-27': True,
                       '1994-05-30': True, '1994-07-04': True, '1994-09-05': True, '1994-11-24': True,
                       '1994-12-26': True, '1995-01-02': True, '1995-02-20': True, '1995-04-14': True,
                       '1995-05-29': True, '1995-07-04': True, '1995-09-04': True, '1995-11-23': True,
                       '1995-12-25': True, '1996-01-01': True, '1996-02-19': True, '1996-04-05': True,
                       '1996-05-27': True, '1996-07-04': True, '1996-09-02': True, '1996-11-28': True,
                       '1996-12-25': True, '1997-01-01': True, '1997-02-17': True, '1997-03-28': True,
                       '1997-05-26': True, '1997-07-04': True, '1997-09-01': True, '1997-11-27': True,
                       '1997-12-25': True, '1998-01-01': True, '1998-01-19': True, '1998-02-16': True,
                       '1998-04-10': True, '1998-05-25': True, '1998-07-03': True, '1998-09-07': True,
                       '1998-11-26': True, '1998-12-25': True, '1999-01-01': True, '1999-01-18': True,
                       '1999-02-15': True, '1999-04-02': True, '1999-05-31': True, '1999-07-05': True,
                       '1999-09-06': True, '1999-11-25': True, '1999-12-24': True, '2000-01-17': True,
                       '2000-02-21': True, '2000-04-21': True, '2000-05-29': True, '2000-07-04': True,
                       '2000-09-04': True, '2000-11-23': True, '2000-12-25': True, '2001-01-01': True,
                       '2001-01-15': True, '2001-02-19': True, '2001-04-13': True, '2001-05-28': True,
                       '2001-07-04': True, '2001-09-03': True, '2001-09-11': True, '2001-09-12': True,
                       '2001-09-13': True, '2001-09-14': True, '2001-11-22': True, '2001-12-25': True,
                       '2002-01-01': True, '2002-01-21': True, '2002-02-18': True, '2002-03-29': True,
                       '2002-05-27': True, '2002-07-04': True, '2002-09-02': True, '2002-11-28': True,
                       '2002-12-25': True, '2003-01-01': True, '2003-01-20': True, '2003-02-17': True,
                       '2003-04-18': True, '2003-05-26': True, '2003-07-04': True, '2003-09-01': True,
                       '2003-11-27': True, '2003-12-25': True, '2004-01-01': True, '2004-01-19': True,
                       '2004-02-16': True, '2004-04-09': True, '2004-05-31': True, '2004-06-11': True,
                       '2004-07-05': True, '2004-09-06': True, '2004-11-25': True, '2004-12-24': True,
                       '2005-01-17': True, '2005-02-21': True, '2005-03-25': True, '2005-05-30': True,
                       '2005-07-04': True, '2005-09-05': True, '2005-11-24': True, '2005-12-26': True,
                       '2006-01-02': True, '2006-01-16': True, '2006-02-20': True, '2006-04-14': True,
                       '2006-05-29': True, '2006-07-04': True, '2006-09-04': True, '2006-11-23': True,
                       '2006-12-25': True, '2007-01-01': True, '2007-01-02': True, '2007-01-15': True,
                       '2007-02-19': True, '2007-04-06': True, '2007-05-28': True, '2007-07-04': True,
                       '2007-09-03': True, '2007-11-22': True, '2007-12-25': True, '2008-01-01': True,
                       '2008-01-21': True, '2008-02-18': True, '2008-03-21': True, '2008-05-26': True,
                       '2008-07-04': True, '2008-09-01': True, '2008-11-27': True, '2008-12-25': True,
                       '2009-01-01': True, '2009-01-19': True, '2009-02-16': True, '2009-04-10': True,
                       '2009-05-25': True, '2009-07-03': True, '2009-09-07': True, '2009-11-26': True,
                       '2009-12-25': True, '2010-01-01': True, '2010-01-18': True, '2010-02-15': True,
                       '2010-04-02': True, '2010-05-31': True, '2010-07-05': True, '2010-09-06': True,
                       '2010-11-25': True, '2010-12-24': True, '2011-01-17': True, '2011-02-21': True,
                       '2011-04-22': True, '2011-05-30': True, '2011-07-04': True, '2011-09-05': True,
                       '2011-11-24': True, '2011-12-26': True, '2012-01-02': True, '2012-01-16': True,
                       '2012-02-20': True, '2012-04-06': True, '2012-05-28': True, '2012-07-04': True,
                       '2012-09-03': True, '2012-10-29': True, '2012-10-30': True, '2012-11-22': True,
                       '2012-12-25': True, '2013-01-01': True, '2013-01-21': True, '2013-02-18': True,
                       '2013-03-29': True, '2013-05-27': True, '2013-07-04': True, '2013-09-02': True,
                       '2013-11-28': True, '2013-12-25': True, '2014-01-01': True, '2014-01-20': True,
                       '2014-02-17': True, '2014-04-18': True, '2014-05-26': True, '2014-07-04': True,
                       '2014-09-01': True, '2014-11-27': True, '2014-12-25': True, '2015-01-01': True,
                       '2015-01-19': True, '2015-02-16': True, '2015-04-03': True, '2015-05-25': True,
                       '2015-07-03': True, '2015-09-07': True, '2015-11-26': True, '2015-12-25': True,
                       '2016-01-01': True, '2016-01-18': True, '2016-02-15': True, '2016-03-25': True,
                       '2016-05-30': True, '2016-07-04': True, '2016-09-05': True, '2016-11-24': True,
                       '2016-12-26': True, '2017-01-02': True, '2017-01-16': True, '2017-02-20': True,
                       '2017-04-14': True, '2017-05-29': True, '2017-07-04': True, '2017-09-04': True,
                       '2017-11-23': True, '2017-12-25': True, '2018-01-01': True, '2018-01-15': True,
                       '2018-02-19': True, '2018-03-30': True, '2018-05-28': True, '2018-07-04': True,
                       '2018-09-03': True, '2018-11-22': True, '2018-12-05': True, '2018-12-25': True,
                       '2019-01-01': True, '2019-01-21': True, '2019-02-18': True, '2019-04-19': True,
                       '2019-05-27': True, '2019-07-04': True, '2019-09-02': True, '2019-11-28': True,
                       '2019-12-25': True, '2020-01-01': True, '2020-01-20': True, '2020-02-17': True,
                       '2020-04-10': True, '2020-05-25': True, '2020-07-03': True, '2020-09-07': True,
                       '2020-11-26': True, '2020-12-25': True, '2021-01-01': True, '2021-01-18': True,
                       '2021-02-15': True, '2021-04-02': True, '2021-05-31': True, '2021-07-05': True,
                       '2021-09-06': True, '2021-11-25': True, '2021-12-24': True, '2022-01-17': True,
                       '2022-02-21': True, '2022-04-15': True, '2022-05-30': True, '2022-06-20': True,
                       '2022-07-04': True, '2022-09-05': True, '2022-11-24': True, '2022-12-26': True,
                       '2023-01-02': True, '2023-01-16': True, '2023-02-20': True, '2023-04-07': True,
                       '2023-05-29': True, '2023-06-19': True, '2023-07-04': True, '2023-09-04': True,
                       '2023-11-23': True, '2023-12-25': True, '2024-01-01': True, '2024-01-15': True,
                       '2024-02-19': True, '2024-03-29': True, '2024-05-27': True, '2024-07-04': True,
                       '2024-09-02': True, '2024-11-28': True, '2024-12-25': True}

        return holiday_map
