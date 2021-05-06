import logging
import os
from dotenv import load_dotenv
import datetime
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger('telegram_bot_api.info')

load_dotenv()


def parse_json(result):
	output = []
	centers = result['centers']
	for center in centers:
		sessions = center['sessions']
		for session in sessions:
			if int(session['available_capacity']) > 0:
				res = { 'name': center['name'], 
                        'block_name': center['block_name'],
                        'age_limit': session['min_age_limit'], 
                        'vaccine_type': session['vaccine'] , 
                        'date': session['date'],
                        'available_capacity': session['available_capacity'],
                        'fee' : center['fee_type']
                    }
				output.append(res)
	return output

def form_str(response):
    try:
        if response.status_code == 200:
            print("Status 200 success")
            result = response.json()
            output = parse_json(result)
            str1 = ""
            if len(output) > 0:
                str1+="Vaccines available \n\n"
                str1+="-------------------------------------------------------------\n"
                print('\007')
                for center in output:
                    # if(int(center['available_capacity'])!=0):
                    str1+=center['name']+"\n"
                    str1+="Block: "+center['block_name']+"\n"
                    str1+="Vaccine Available Count: "+str(int(center['available_capacity']))+"\n"
                    str1+="Vaccine Type: " + center['vaccine_type']+"\n"
                    str1+="Slot Date: "+center['date']+"\n"
                    str1+="Age Group: "+ str(center['age_limit'])+"\n"
                    str1+="Fee: "+ str(center['fee'])+"\n"
                    str1+="-------------------------------------------------------------\n"
            else:
                str1+="Vaccine Unavailable.\n"
        
            return str1
        else:
            str1 = "CoWin API Down\n"
        return str1
    except Exception as e:
        print(e)
        return False


def fetch_values(district_code):
    try:
        date = datetime.date.today()
        print(date)
        fetch_url = os.getenv('FETCH_URL')+"district_id="+str(district_code)+ "&date="+ str(date.day)+"-"+str(date.month)+"-"+str(date.year)
        print(fetch_url)
        response = requests.get(fetch_url)
        lis = form_str(response)
        if lis==False:
            print(response)
        return lis
    except Exception as e:
        print("Fetch Values failed..")
        logger.error(e)

