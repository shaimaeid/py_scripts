import datetime

def formatDate(start_date , end_date):
    
    if start_date is None or end_date is None:
        # Calculate the start and end dates for the last 3 months
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=3 * 30)
        end_date = today
    else:
        # Convert the start_date and end_date strings to datetime objects
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    
    return start_date,end_date