import os
import PyPDF2 



            #year, month, edition
TOP_DATE = (2022, 7, 5)
FIRST_DATE = (2014,5,4)

######################
# name missing files #
######################
def get_date_from_file(elem):
    return elem.split('.')[0].split('_')[0]

def get_tuple_from_date(elem):
    aux = map(int,elem.split('-'))
    list = []
    for a in aux:
        list.append(a)
    return tuple(list)

def get_set(dir = r'corpus\downloads'):
    l = os.listdir(dir)
    t = map(get_date_from_file, l)
    s = set(t)
    t = map(get_tuple_from_date, s)
    s = set(t)
    return s

def get_next(date):
    old_edition = int(date[2])
    old_month = int(date[1])
    old_year = int(date[0])
    if old_edition < 5:
        edition = old_edition + 1
        month = old_month
        year = old_year
    else:
        edition = 1
        if old_month == 12:
            month = 1
            year = old_year + 1
        else:
            month = old_month + 1
            year = old_year
    return(year,month, edition)

def in_range(date):
    year, month, edition = TOP_DATE
    current_year, current_month, current_edition = date
    if current_year == year:
        if current_month == month:
            return current_edition <= edition
        else:
            return current_month < month
    else:
        return current_year < year

def to_string(date):
    year, month, edition = map(str, date)
    return'-'.join([year, month, edition])

def write_date(date, filepath= 'missing.txt'):
    with open(filepath, 'a') as file:
        file.write(to_string(date)+'\n')

def choose_missing(dates, filepath= 'missing.txt'):
    start = FIRST_DATE
    while in_range(start):
        if start not in dates:
            write_date(start)
        start = get_next(start)

def write_missing():
    dates = get_set()
    choose_missing(dates)
    print('Done')





     
