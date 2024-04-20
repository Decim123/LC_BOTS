from datetime import datetime, timedelta

def next_day_of_week(day_of_week):
    current_date = datetime.now().date()
    weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    day_of_week_lower = day_of_week.lower().replace(" ", "")
    day_of_week_index = weekdays.index(day_of_week_lower)
    current_day_of_week_index = current_date.weekday()
    days_until_next = (day_of_week_index - current_day_of_week_index) % 7
    if days_until_next <= 0:
        days_until_next += 7

    next_day_date = current_date + timedelta(days=days_until_next)

    return next_day_date

# Пример использования
next_saturday = next_day_of_week("суббота")
print("Дата следующей субботы:", next_saturday)
