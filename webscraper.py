# -*- coding: utf-8 -*-
# BeautifulSoup Web PlugIn
from bs4 import BeautifulSoup
# Datum PlugIn
from datetime import datetime
# Internet-Check
from urllib.request import urlopen
from urllib.error import URLError
# Import von Web-Requests, CSV-Export,
import requests, csv, os, signal, time, sys

file_log = 0
# Ctrl-C Handler
def exit_successful(signal, frame):
	if file_log == 1:
		csv_file_comments.close()
		print('Alle Dateien werden geschlossen')
	elif file_log == 2:
		csv_file_comments.close()
		csv_file_posts.close()
		print('Alle Dateien werden geschlossen')
	elif file_log == 3:
		csv_file_comments.close()
		csv_file_posts.close()
		csv_file_categories.close()
		print('Alle Dateien werden geschlossen')
	elif file_log == 4:
		csv_file_comments.close()
		csv_file_posts.close()
		csv_file_categories.close()
		csv_file_external_links.close()
		print('Alle Dateien werden geschlossen')
	print('\nDas Programm wird sicher beendet...')
	time.sleep(2)
	sys.exit(0)

# Prüfen ob Verbindung besteht
def internet_access():
    try:
        urlopen('https://kuechenchaotin.de/', timeout=10)
        return True
    except URLError as err:
    	return False

def run_scraper():
	# Benutzerübersicht im Terminal
	print()
	print('+-------------------------------------------------------------------------+')
	print('| WEBSCRAPER von Lukas B. und Felix H.        [5. Semester/Web-Analytics] |')
	print('| BLOG: kuechenchaotin.de                    (Rezepte aus der Chaosküche) |')
	print('+-------------------------------------------------------------------------+')
	print('| BENUTZUNG: webscraper.exe ausführen                        (Windows 10) |')
	print('| OUTPUT:    [datum]_posts_scrape.csv            (Blogpost-Informationen) |')
	print('|            [datum]_comments_scrape.csv       (Kommentare der Blogposts) |')
	print('|            [datum]_categories_scrape.csv     (Kategorien der Blogposts) |')
	print('+-------------------------------------------------------------------------+')
	print('| EXIT:      Ctrl+C                                (Frühzeitiges Beenden) |')
	print('+-------------------------------------------------------------------------+')
	print()

	# Abfrage zum Starten des Programms
	print('Möchtest du starten ' + '"kuechenchaotin.de"' + ' zu scannen?')
	print('Drücke y um den Vorgang zu starten.')
	start_programm = input('EINGABE: ')
	if start_programm == 'y':
		print('\nVerbindung wird hergestellt...')
	else:
		print('\nDas Programm wird sicher beendet...')
		time.sleep(2)
		sys.exit(0)

	# Aktuelles Datum für Ausgabedateien ermitteln
	current_date = datetime.now()
	current_date = current_date.strftime("%y.%m.%d_")

	# CSV-Dateien überprüfen
	if os.path.isfile(current_date + 'posts_scrape.csv'):
		print('\nWARNUNG: '+ current_date + 'posts_scrape.csv existiert bereits')
		print('Drücke y um diese Datei zu überschreiben.')
		file_exists_1 = input('EINGABE: ')
		if file_exists_1 != 'y':
			print('\nDas Programm wird sicher beendet...')
			time.sleep(2)
			sys.exit(0)
	if os.path.isfile(current_date + 'comments_scrape.csv'):
		print('\nWARNUNG: '+ current_date + 'comments_scrape.csv existiert bereits')
		print('Drücke y um diese Datei zu überschreiben.')
		file_exists_2 = input('EINGABE: ')
		if file_exists_2 != 'y':
			print('\nDas Programm wird sicher beendet...')
			time.sleep(2)
			sys.exit(0)
	if os.path.isfile(current_date + 'categories_scrape.csv'):
		print('\nWARNUNG: '+ current_date + 'categories_scrape.csv existiert bereits')
		print('Drücke y um diese Datei zu überschreiben.')
		file_exists_3 = input('EINGABE: ')
		if file_exists_3 != 'y':
			print('\nDas Programm wird sicher beendet...')
			time.sleep(2)
			sys.exit(0)
	if os.path.isfile(current_date + 'external_links_scrape.csv'):
		print('\nWARNUNG: '+ current_date + 'external_links_scrape.csv existiert bereits')
		print('Drücke y um diese Datei zu überschreiben.')
		file_exists_4 = input('EINGABE: ')
		if file_exists_4 != 'y':
			print('\nDas Programm wird sicher beendet...')
			time.sleep(2)
			sys.exit(0)

	# CSV-Dateien anlegen
	csv_file_posts = open(current_date + 'posts_scrape.csv', 'w', newline='', encoding="utf-8")
	file_log=1
	csv_file_comments = open(current_date + 'comments_scrape.csv', 'w', newline='', encoding="utf-8")
	file_log=2
	csv_file_categories = open(current_date + 'categories_scrape.csv', 'w', newline='', encoding="utf-8")
	file_log=3
	csv_file_external_links = open(current_date + 'external_links_scrape.csv', 'w', newline='', encoding="utf-8")
	file_log=4


	# CSV-Dateien öffnen
	csv_writer_posts = csv.writer(csv_file_posts, delimiter=' ', escapechar=' ', quoting=csv.QUOTE_NONE)
	csv_writer_comments = csv.writer(csv_file_comments, delimiter=' ', escapechar=' ',  quoting=csv.QUOTE_NONE)
	csv_writer_categories = csv.writer(csv_file_categories, delimiter=' ', escapechar=' ', quoting=csv.QUOTE_NONE)
	csv_writer_external_links = csv.writer(csv_file_external_links, delimiter=' ', escapechar=' ', quoting=csv.QUOTE_NONE)
	csv_writer_posts.writerow(['Postnumber' + ';' + 'Picture' + ';' + 'Title' + ';' + 'Appetizer' + ';' + 'Date' + ';' + 'URL' + ';' + 'Text' + ';' + 'Commentcount' + ';' +'Sitelinkscount'])
	csv_writer_comments.writerow(['Postnumber' + ';' + 'Date' + ';' + 'Author' + ';' + 'Comment'])
	csv_writer_categories.writerow(['Postnumber' + ';' + 'Date' + ';' + 'Allgemein' + ';' + 'Vorspeisen' + ';' + 'Hauptspeisen' + ';' + 'Frühstück' + ';' + 'Beilagen' + ';' + 'Süßes' + ';' + 'Getränke' + ';' + 'Frühling' + ';' + 'Sommer' + ';' + 'Herbst' + ';' + 'Winter' + ';' + 'on Tour' + ';' + 'Nachspeisen' + ';' + 'Pasta und Risotto' + ';' + 'Suppen' + ';' + 'aus der Backstube' + ';' + 'Kleinigkeiten' + ';' + 'kleine Geschenke' + ';' + 'Wie macht man eigentlich...?' + ';' + 'Fit & Healthy Friday' + ';' + '\"Stiftung Chaosküchen-Test\"' + ';' + 'Blogs that rock' + ';' + 'aus dem Eisfach' + ';' + 'Selfmade Sunday' + ';' + 'Eat like a Swabian' + ';' + 'Books that rock'])
	csv_writer_external_links.writerow(['Postnumber' + ';' + 'External Link' + ';' + 'Partner'])

	# Startseite: Seite 1- Home
	page_number = 1

	# Indikator zum Finden des Blogpost-Endes
	body_class = 'home'

	# Intwert für Progressbar im Terminal
	progress = 0

	print()
	# Solange neue Blogseiten geladen werden können
	while body_class != 'error404':
		# Verbindung zur Blog-Seiten-Übersicht aufbauen
		url = 'https://kuechenchaotin.de/'
		url_page = 'page'
		offset = '/'
		full_url = url+url_page+str(page_number)+offset

		# Verbindung aufbauen
		if internet_access():
			post_source = requests.get(full_url).text
		else:
			print('WARNUNG: Keine Internetverbindung zur Postübersicht möglich')
			break
		post_soup = BeautifulSoup(post_source, 'lxml')
		error_message = post_soup.find('body', class_='error404')

		# Falls keine Weitere Seite gefunden wird
		if error_message != None:
			# Scrapen abbrechen
			body_class='error404'
			print('\nKeine Weiteren Blogpost-Seiten verfügbar')
			break

		# Falls keine Blogposts auf der Seite
		if post_soup.find('article') == None:
			#Scrapen abbrechen
			print('Keine Blogposts gefunden')
			break

		# Seiten-Status im Terminal
		print('INFO: aktuelle Seite: ' + str(page_number))

		# Alle Blogposts auf aktueller Seite scrapen
		for post in post_soup.find_all('article'):

			# Standardattribute der Einträge
			print('INFO: gesammelte Blogposts: ' + str(progress))
			post_header = ''
			post_img = ''
			post_entry = ''
			post_id = ''
			post_date = ''
			post_link = ''
			site_content = ['false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false','false']
			site_text = ''
			post_comment_count = 0
			site_comments_date = ''
			site_comments_author = ''
			site_comments = ''
			site_links = ''
			site_links_count = 0

			# Fehlervariable, falls Element nicht gefunden
			elem = None

			# Header lesen
			elem = post.find('div', class_='post-header')
			if elem is not None:
				elem = elem.find('h2')
				if elem is not None:
					post_header = post.find('div', class_='post-header').h2.text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
					#print(post_header)
					#print()

			# Image lesen
			elem = post.find('div', class_='post-img')
			if elem is not None:
				elem = elem.find('a')
				if elem is not None:
					elem = elem.find('img')
					if elem is not None:
						post_img = post.find('div', class_='post-img').a.img['data-lazy-src']
						post_img, sep, tail = post_img.partition(' ')
						#print(post_img)
						#print()

			# Entry lesen
			elem = post.find('div', class_='post-entry')
			if elem is not None:
				elem = elem.find('p')
				if elem is not None:
					post_entry = post.find('div', class_='post-entry').p.text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
					#print(post_entry)
					#print()

			# ID lesen
			elem = post['id']
			if elem is not None:
				post_id = post['id']
				#print(post_id)
				#print()

			# Date lesen
			elem = post.find('div', class_='post-meta')
			if elem is not None:
				elem = elem.find('span', class_='meta-text')
				if elem is not None:
					elem.find('a')
					if elem is not None:
						post_date_raw = post.find('div', class_='post-meta').find('span', class_='meta-text').a.text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
						post_date_array = post_date_raw.replace('.', '').split()
						if len(post_date_array[0]) == 2:
							post_date_1 = post_date_array[0]
						else:
							post_date_1 = '0' + post_date_array[0]
						if post_date_array[1] == 'Januar':
							post_date_2 = '01'
						if post_date_array[1] == 'Februar':
							post_date_2 = '02'
						if post_date_array[1] == 'März':
							post_date_2 = '03'
						if post_date_array[1] == 'April':
							post_date_2 = '04'
						if post_date_array[1] == 'Mai':
							post_date_2 = '05'
						if post_date_array[1] == 'Juni':
							post_date_2 = '06'
						if post_date_array[1] == 'Juli':
							post_date_2 = '07'
						if post_date_array[1] == 'August':
							post_date_2 = '08'
						if post_date_array[1] == 'September':
							post_date_2 = '09'
						if post_date_array[1] == 'Oktober':
							post_date_2 = '10'
						if post_date_array[1] == 'November':
							post_date_2 = '11'
						if post_date_array[1] == 'Dezember':
							post_date_2 = '12'
						post_date_3 = post_date_array[2]

						post_date = post_date_1 + '/' + post_date_2 + '/' + post_date_3
						# print(post_date)
						# print()

			# Link lesen
			elem = post.find('div', class_='post-meta')
			if elem is not None:
				elem = elem.find('span', class_='meta-text')
				if elem is not None:
					elem = elem.find('a')
					if elem is not None:
						post_link = post.find('div', class_='post-meta').find('span', class_='meta-text').a['href']
						# print(post_link)
						# print()

			# Unterseiten der Posts aufrufen

			# Verbindung aufbauen
			if internet_access():
				site_source = requests.get(post_link).text
			else:
				print('WARNUNG: Keine Internetverbindung zum Blogpost möglich')
				break
			site_soup = BeautifulSoup(site_source, 'lxml')
			site = site_soup.find('div', id='content')

			# Category lesen
			elem = site.find('span', class_='cat')
			if elem is not None:
				elem = elem.find_all('a', rel='category tag')
				if elem is not None:
					site_content_raw = site.find('span', class_='cat').find_all('a', rel='category tag')
					nu=0
					for x in site_content_raw:
						if site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Allgemein':
							site_content[0] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Vorspeisen':
							site_content[1] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Hauptspeisen':
							site_content[2] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Frühstück':
							site_content[3] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Beilagen':
							site_content[4] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Süßes':
							site_content[5] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Getränke':
							site_content[6] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Frühling':
							site_content[7] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Sommer':
							site_content[8] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Herbst':
							site_content[9] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Winter':
							site_content[10] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'on Tour':
							site_content[11] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Nachspeisen':
							site_content[12] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Pasta und Risotto':
							site_content[13] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Suppen':
							site_content[14] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'aus der Backstube':
							site_content[15] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Kleinigkeiten':
							site_content[16] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'kleine Geschenke':
							site_content[17] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Wie macht man eigentlich...?':
							site_content[18] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Fit & Healthy Friday':
							site_content[19] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == '\"Stiftung Chaosküchen-Test\"':
							site_content[20] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Blogs that rock':
							site_content[21] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'aus dem Eisfach':
							site_content[22] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Selfmade Sunday':
							site_content[23] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Eat like a Swabian':
							site_content[24] = 'true'
						elif site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') == 'Books that rock':
							site_content[25] = 'true'
						else:
							print('new content category: ' + site_content_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ')).replace(';', '-')
						nu=nu+1
			# Text lesen
			elem = site.find('div', class_='post-entry')
			if elem is not None:
				elem = elem.find('p')
				if elem is not None:
					site_text_raw = site.find('div', class_='post-entry').find_all('p')
					nu=0
					# Alle Elemente der Textelemente des Posts lesen
					for x in site_text_raw:
						new = site_text_raw[nu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-') + ' '
						site_text += new
						nu= nu+1
					site_text = site_text.rstrip(' ')
					# print(site_text)
					# print()

			# External Links lesen
			elem = site.find('div', class_='post-entry')
			if elem is not None:
				elem = elem.find('p')
				if elem is not None:
					elem = elem.find_all('a')
					if elem is not None:
						site_links_container = []
						site_links_raw = site.find('div', class_='post-entry').find_all('p')
						nu=0
						# Alle Elemente der Textelemente des Posts lesen
						for x in site_links_raw:
							site_links_deep = site_links_raw[nu].find_all('a')
							mu=0
							for y in site_links_deep:
								site_links = site_links_deep[mu]['href']
								mu = mu+1
								if site_links.startswith('https://kuechenchaotin.de') == False:
									if site_links.startswith('#') == False:
										if site_links not in site_links_container:
											site_links_container.append(site_links)
											site_links_count = site_links_count +1
											partner_raw=''
											if site_links.startswith('http://'):
												partner_raw = site_links[7:]
											elif site_links.startswith('https://'):
												partner_raw = site_links[8:]

											if partner_raw.startswith('www.'):
												partner_raw = partner_raw[4:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('de.'):
												partner_raw = partner_raw[3:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('de-store.'):
												partner_raw = partner_raw[9:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('store.'):
												partner_raw = partner_raw[6:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('lp.'):
												partner_raw = partner_raw[3:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('l.'):
												partner_raw = partner_raw[2:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('files.'):
												partner_raw = partner_raw[6:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('blog.'):
												partner_raw = partner_raw[5:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('uk.'):
												partner_raw = partner_raw[3:]
												partner = partner_raw.split('.', 1)[0]
											elif partner_raw.startswith('amzn'):
												partner = 'amazon'
											else:
												partner = partner_raw.split('.', 1)[0]
											csv_writer_external_links.writerow([ post_id + ';' + site_links + ';' + partner])

							nu= nu+1
						# print(site_text)
						# print()

			# Kommentarelemente lesen
			elem = site.find('div', class_='comment-text')
			if elem is not None:
				site_comments_raw = site.find_all('div', class_='comment-text')

			# Kommentaranzahl lesen
			elem = post.find('div', class_='meta-comments')
			if elem is not None:
				elem = elem.find('a')
				if elem is not None:
					post_comment_count = post.find('div', class_='meta-comments').a.text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
					# print(post_comment_count)
					# print()
			nu=0

			# Falls mehr als 0 Kommentare verfügbar
			if int(post_comment_count) != 0:

				# Wenn mehr als ein Kommentar
				if len(site_comments_raw) > 1:

					# Durch alle Kommentare iterieren
					for x in site_comments_raw:

						# Date auslesen
						elem = site_comments_raw[nu].find('span', class_='date')
						if elem is not None:
							site_comments_date_raw = site_comments_raw[nu].find('span', class_='date').text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
							site_comments_date_string = site_comments_date_raw.replace(' at ', ' ')
							site_comments_date_array = site_comments_date_string.replace('.', '').split()
							if len(site_comments_date_array[0]) == 2:
								site_comments_date_1 = site_comments_date_array[0]
							else:
								site_comments_date_1 = '0' + site_comments_date_array[0]
							if site_comments_date_array[1] == 'Januar':
								site_comments_date_2 = '01'
							if site_comments_date_array[1] == 'Februar':
								site_comments_date_2 = '02'
							if site_comments_date_array[1] == 'März':
								site_comments_date_2 = '03'
							if site_comments_date_array[1] == 'April':
								site_comments_date_2 = '04'
							if site_comments_date_array[1] == 'Mai':
								site_comments_date_2 = '05'
							if site_comments_date_array[1] == 'Juni':
								site_comments_date_2 = '06'
							if site_comments_date_array[1] == 'Juli':
								site_comments_date_2 = '07'
							if site_comments_date_array[1] == 'August':
								site_comments_date_2 = '08'
							if site_comments_date_array[1] == 'September':
								site_comments_date_2 = '09'
							if site_comments_date_array[1] == 'Oktober':
								site_comments_date_2 = '10'
							if site_comments_date_array[1] == 'November':
								site_comments_date_2 = '11'
							if site_comments_date_array[1] == 'Dezember':
								site_comments_date_2 = '12'

							site_comments_date_3 = site_comments_date_array[2]
							site_comments_date_4 = site_comments_date_array[3]

							site_comments_date = site_comments_date_1 + '/' + site_comments_date_2 + '/' + site_comments_date_3 + ' ' + site_comments_date_4
						else:
							continue

						# Author auslesen
						elem = site_comments_raw[nu].find('h6', class_='author')
						if elem is not None:
							site_comments_author = site_comments_raw[nu].find('h6', class_='author').text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
						else:
							continue

						# Alle Kommentareinheiten lesen
						elem = site_comments_raw[nu].find('p')
						if elem is not None:
							site_comments_p = site_comments_raw[nu].find_all('p')
						else:
							continue

						# Text der Kommentareinheiten
						# auslesen und zusammenfügen
						mu=0
						site_comments=''
						for y in site_comments_p:
							site_comments += site_comments_p[mu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
							mu= mu+1
						csv_writer_comments.writerow([ post_id + ';' + site_comments_date + ';' + site_comments_author + ';' + site_comments])
						# nächster Kommentar
						nu= nu+1
					# print(site_comments)
					# print()

				# Falls genau ein Kommentar
				if int(post_comment_count) == 1:
					elem = site.find('div', class_='comment-text')
					if elem is not None:
						site_comments_raw = site.find('div', class_='comment-text')

					# Date auslesen
					elem = site_comments_raw.find('span', class_='date')
					if elem is not None:
						site_comments_date_raw = site_comments_raw.find('span', class_='date').text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
						site_comments_date_string = site_comments_date_raw.replace(' at ', ' ')
						site_comments_date_array = site_comments_date_string.replace('.', '').split()
						if len(site_comments_date_array[0]) == 2:
							site_comments_date_1 = site_comments_date_array[0]
						else:
							site_comments_date_1 = '0' + site_comments_date_array[0]
						if site_comments_date_array[1] == 'Januar':
							site_comments_date_2 = '01'
						if site_comments_date_array[1] == 'Februar':
							site_comments_date_2 = '02'
						if site_comments_date_array[1] == 'März':
							site_comments_date_2 = '03'
						if site_comments_date_array[1] == 'April':
							site_comments_date_2 = '04'
						if site_comments_date_array[1] == 'Mai':
							site_comments_date_2 = '05'
						if site_comments_date_array[1] == 'Juni':
							site_comments_date_2 = '06'
						if site_comments_date_array[1] == 'Juli':
							site_comments_date_2 = '07'
						if site_comments_date_array[1] == 'August':
							site_comments_date_2 = '08'
						if site_comments_date_array[1] == 'September':
							site_comments_date_2 = '09'
						if site_comments_date_array[1] == 'Oktober':
							site_comments_date_2 = '10'
						if site_comments_date_array[1] == 'November':
							site_comments_date_2 = '11'
						if site_comments_date_array[1] == 'Dezember':
							site_comments_date_2 = '12'

						site_comments_date_3 = site_comments_date_array[2]
						site_comments_date_4 = site_comments_date_array[3]

						site_comments_date = site_comments_date_1 + '/' + site_comments_date_2 + '/' + site_comments_date_3 + ' ' + site_comments_date_4

					# Author auslesen
					elem = site_comments_raw.find('h6', class_='author')
					if elem is not None:
						site_comments_author = site_comments_raw.find('h6', class_='author').text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')

					# Kommentareinheiten auslesen
					elem = site_comments_raw.find('p')
					if elem is not None:
						site_comments_p = site_comments_raw.find_all('p')

					# Text der Kommentareinheiten
					# auslesen und zusammenfügen
					mu=0
					for x in site_comments_p:
						site_comments += site_comments_p[mu].text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(';', '-')
						mu= mu+1
					csv_writer_comments.writerow([ post_id + ';' + site_comments_date + ';' + site_comments_author + ';' + site_comments])
					# print(site_comments)
					# print()
			# Falls keine Kommentare verfügbar
			else:
				site_comments=''

			# Postinformationen und Kategorien des
			# Blogposts in die CSV-Dateien schreiben
			csv_writer_posts.writerow([ post_id + ';' + post_img + ';' + post_header + ';' + post_entry + ';' + post_date + ';' + post_link + ';' + site_text + ';' + post_comment_count + ';' + str(site_links_count) ])
			csv_writer_categories.writerow([ post_id + ';' + post_date +';' + site_content[0] + ';' + site_content[1] + ';' + site_content[2] + ';' + site_content[3] + ';' + site_content[4] + ';' + site_content[5] + ';' + site_content[6] + ';' + site_content[7] + ';' + site_content[8] + ';' + site_content[9] + ';' + site_content[10] + ';' + site_content[11] + ';' + site_content[12] + ';' + site_content[13] + ';' + site_content[14] + ';' + site_content[15] + ';' + site_content[16] + ';' + site_content[17] + ';' + site_content[18] + ';' + site_content[19] + ';' + site_content[20] + ';' + site_content[21] + ';' + site_content[22] + ';' + site_content[23] + ';' + site_content[24] + ';' + site_content[25]])

			# Post-Fortschritt in Terminal erhöhen
			progress = progress+1
		# Seiten-Fortschritt im Terminal erhöhen
		page_number = page_number+1

	# Alle Dateien schließen
	csv_file_comments.close()
	csv_file_posts.close()
	csv_file_categories.close()
	csv_file_external_links.close()
	file_log=0
	print('Vorgang abgeschlossen.')
	print('Programm kann mit Ctrl+C oder über das Fenster beendet werden.')

def wait_user_input():
	while True:
		time.sleep(1)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_successful)
    run_scraper()
    wait_user_input()
