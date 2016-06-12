import twitter
from RPLCD import CharLCD
import time
import HTMLParser

lcd = CharLCD(pin_rs=26, pin_e=24, pins_data=[22, 18, 16, 12])

api=twitter.Api(consumer_key='YOUR_CONSUMER_KEY',
	consumer_secret='YOUR_CONSUMER_SECRET',
	access_token_key='YOUR_ACCESS_TOKEN_KEY',
	access_token_secret='YOUR_ACCESS_TOKEN_SECRET')

htmlParser = HTMLParser.HTMLParser()

try:
	while True:
		try:
			homeTimeline=api.GetHomeTimeline(count=1)
		except:
			lcd.clear()
			lcd.write_string(u'An Error occurred! Retrying')
			continue
		tweetUser = homeTimeline[0].user.screen_name
		tweetText = homeTimeline[0].text
		tweetText = htmlParser.unescape(tweetText) # convert HTML symbols like &amp;
		tweetText = tweetText.replace('\n',' ') # replace newlines with space
		
		# Break the tweet into two parts as the LCD screen can display 
		# only 80 characters at a time
		
		seg1_len = 80 - len(tweetUser) - 2 
		tweetText1 = tweetUser+": "+tweetText[:seg1_len]
		tweetText2 = tweetText[seg1_len:]
		lcd.clear()
		lcd.write_string(tweetText1)	
		if tweetText2:
			for i in range(7):
				time.sleep(8)
				lcd.clear()
				lcd.write_string(tweetText2)
				time.sleep(8)
				lcd.clear()
				lcd.write_string(tweetText1)
		else:
			time.sleep(60)
except KeyboardInterrupt:
	pass
finally:
	lcd.clear()
	lcd.write_string(u'Twitter feed stopped')



