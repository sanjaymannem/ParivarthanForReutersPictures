from django.shortcuts import render
import re
import geocoder, geopy
from geopy.geocoders import Nominatim
#from googletrans import Translator
import boto3
import traceback
import os
# Create your views here.
def any_view(request, value = ''):
	translate = boto3.client(service_name='translate',aws_access_key_id='id herer',
         aws_secret_access_key= 'key here', region_name='us-west-1', use_ssl=True)
	
	languages = {'Andhra pradesh':['te', 'Telugu'],'Arunachal Pradesh':['hi','Hindi'],'Assam':['hi','Hindi'],'Bihar':['hi','Hindi'],'Chhattisgarh':['hi','Hindi'],'Goa':['hi','Hindi'],'Gujarat':['gu','Gujarathi'],'Haryana':['hi','Hindi'],
	'Himachal Pradesh':['hi','Hindi'],'Jharkhand':['hi','Hindi'],'Karnataka':['kn', 'kannada'],'Kerala':['ml', 'malayalm'],'Madhya Pradesh':['hi','Hindi'],
	'Maharashtra':['mr', 'Marati'],'Manipur':['hi','Hindi'],'Meghalaya':['hi','Hindi'],'Mizoram':['hi','Hindi'],
	'Nagaland':['hi','Hindi'],'Odisha':['hi','Hindi'],'Punjab':['pa','Punjabi'],'Rajasthan':['hi','Hindi'],'Sikkim':['hi','Hindi'],
	'Tamil Nadu':['ta', 'Tamil'],'Telangana':['te', 'Telugu'],'Tripura':['hi','Hindi'],'Uttarakhand':['hi','Hindi'],
	'Uttar Pradesh':['hi','Hindi'],'West Bengal':['bn', 'Bengali'],'Hyderabad':['te', 'Telugu'],'Vijayawada':['te', 'Telugu'],'Itanagar':['hi','Hindi'],'Dispur':['hi','Hindi'],
	'Patna':['hi','Hindi'],'Raipur':['hi','Hindi'], 'Pune':['mr', 'Marati'],'Panaji':['hi','Hindi'],'Gandhinagar':'gu','Chandigarh':['hi','Hindi'],'Shimla':['hi','Hindi'],'Ranchi':['hi','Hindi'],'Bangalore':['kn', 'kannada'],'Trivandrum':['ml', 'malayalm'],
	'Bhopal':['hi','Hindi'],
	'Mumbai':['mr','Marati'],'Imphal':['hi','Hindi'],'Shillong':['hi','Hindi'],'Aizawl':['hi','Hindi'],'Kohima':['hi','Hindi'],'Bhubaneshwar':['hi','Hindi'],'Chandigarh':['hi','Hindi'],
	'Jaipur':['hi','Hindi'],'Gangtok':['hi','Hindi'],'Chennai':['ta', 'Tamil'],'Agartala':['hi','Hindi'],'Lucknow':['hi','Hindi'],'Dehradun':['hi','Hindi'],'Kolkata':['bn', 'Bengali']
	}

	Hindu = {'caption1':'A Hindu woman worships the Sun god as she stands amidst the foam covering the polluted Yamuna river during the Hindu religious festival of Chhath Puja in New Delhi, India, November 10, 2021. REUTERS/Adnan Abidi',
	 'caption2':'Hindu women worship the Sun god as they stand amidst the polluted Yamuna river during the Hindu religious festival of Chhath Puja in New Delhi, November 11. REUTERS/Anushree Fadnavis', 
	 'caption3':'Hindu devotees worship the Sun god as they stand amidst the foam covering the polluted Yamuna river, November 11. REUTERS/Anushree Fadnavis'}
	
	Diwali = { 'caption1':
		'Reuters / Friday, November 05, 2021 New Delhi residents woke up on Friday under a blanket of smog darkening the city, the most dangerous air pollution of the year after Diwali revellers defied - as usual - a fireworks ban during India\'s annual Hindu festival of lights. REUTERS/Anushree Fadnavis',
		'caption2':'Reuters / Friday, November 05, 2021 New Delhi has the worst air quality of all world capitals, but even by its sorry standards Friday\'s reading - the morning after the end of Diwali - was extra bad, the price for celebrating India\'s biggest festival in the noisiest and smokiest way. REUTERS/Anushree Fadnavis',
		'caption3':
		'Reuters / Friday, November 05, 2021 The Air Quality Index (AQI) surged to 463 on a scale of 500 - the maximum recorded in 2021, indicating "severe" conditions that affect even healthy people let alone those with existing respiratory diseases. REUTERS/Anushree Fadnavis',
		'caption4':'The AQI measures the concentration of poisonous particulate matter PM2.5 in a cubic metre of air. In Delhi, a city of nearly 20 million people, the PM2.5 reading on Friday averaged 706 micrograms, whereas the World Health Organization deems anything above an annual average of 5 micrograms as unsafe. REUTERS/Adnan Abidi',
		'caption5':'Every year, either government authorities or India\'s Supreme Court slap a ban on firecrackers. But the bans only rarely appear to be enforced. REUTERS/Anushree Fadnavis'
		}

	Covid ={ 'caption1':'A woman poses for a picture after being vaccinated against the coronavirus. to celebrate the milestone of administering one billion doses, in Mumbai, October 21. REUTERS/Francis Mascarenhas',
		'caption2':'Supporters of India\'s Prime Minister Narendra Modi pose after lighting candles in a shape of the map of India to celebrate the milestone of administering one billion coronavirus vaccine doses, in Ahmedabad, India, October 21. REUTERS/Amit Dave',
		'caption3':'A healthcare worker decorates a vaccination center to celebrate the milestone of administering one billion coronavirus vaccine doses, in Mumbai, October 21. REUTERS/Francis Mascarenhas',
		'caption4':'Humayun\'s Tomb is lit in tricolor as India celebrates the milestone of administering one billion COVID vaccine doses, in New Delhi, October 21. REUTERS/Anushree Fadnavis',
		'caption4':'A woman poses for a picture after being vaccinated against the coronavirus. to celebrate the milestone of administering one billion doses, in Mumbai, October 21. REUTERS/Francis Mascarenhas'}
	names = {'index.html':Hindu, 'polution.html':Diwali, 'Covid.html':Covid}
	if value:
		captions = names[value]
	else:
		captions = Hindu
		value = 'index.html'

	g = geocoder.ip('me')
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	g = geocoder.ipinfo(ip)
	# calling the nominatim tool
	geoLoc = Nominatim(user_agent="GetLoc")
	# passing the coordinates
	locname = geoLoc.reverse(g.latlng)
	print(str(locname))
	# printing the address/locaAndhra Ption name
	#translator = Translator()
	trans = []
	lang=''
	if request.method == 'POST':
		lang = request.POST.get('Lang', False)
	print(lang)
	try:
		if not lang:
			for key in languages.keys():
				if re.search(key,str(locname)):
					#textlist = text.split('\n')
					#finaltext = [i for i in textlist if i !=' ']
					for cap, text1 in captions.items():
						trans.append(translate.translate_text(Text=text1,SourceLanguageCode="en", TargetLanguageCode=languages[key][0])['TranslatedText'])
						#trans.append(translator.translate(text1, dest=languages[key]).text)
						lang = languages[key][1]
						print(lang)
						#trans = (translator.translate('1111'.join(captions.values()), dest=languages[key]).text)
						print('this is something  1111')
					break
				else:
					continue
			if len(trans)==0:
				for cap, text1 in captions.items():
					#trans = (translator.translate('1111'.join(captions.values()), dest=['te', 'telugu']).text)
					trans.append(translate.translate_text(Text=text1,SourceLanguageCode="en", TargetLanguageCode='te')['TranslatedText'])
					print('this is something 2222')
		else:
			for cap, text1 in captions.items():
				#trans = (translator.translate('1111'.join(captions.values()), dest=['te', 'telugu']).text)
				trans.append(translate.translate_text(Text=text1,SourceLanguageCode="en", TargetLanguageCode=lang)['TranslatedText'])


	except Exception:
		trans = list(captions.values())
		traceback.print_exc()
		print('this is something 3333')
	#trans = trans.split('1111')
	print(len(trans))
	print(trans)
	context = {'text'+str(i):trans[i] for i in range(len(trans))}
	print("################################", context)
	return render(request, value, context)





