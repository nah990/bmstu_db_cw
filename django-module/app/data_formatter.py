from calendar import monthrange


def date_conversion(date):
    months = [('january', '01'), ('february', '02'), ('march', '03'),
              ('april', '04'), ('may', '05'), ('june', '06'),
              ('july', '07'), ('august', '08'), ('september', '09'),
              ('october', '10'), ('november', '11'), ('december', '12')]
    day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday',
                   'friday', 'saturday', 'sunday']
    date = date.lower()
    date = date.replace(',', '')
    for k in day_of_week:
        date = date.replace(k, '')
    for k, v in months:
        date = date.replace(k, v)
    date = date.strip()
    date = date.replace(' ', '-')
    return date


def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]


def float_conversion(float_num):
    float_num = float_num.strip()
    float_num = float(float_num)
    return float_num
