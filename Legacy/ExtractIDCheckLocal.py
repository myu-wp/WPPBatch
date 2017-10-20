import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

iFilePath = None
resultsFilePath = None

if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
	print 'Drop a CSV file containing raw JSON results onto this program to use it.'
	print '(you need to run SearchIDCheck.bat first)'
	var = raw_input("Hit enter to quit")
	quit()

iFilePath = sys.argv[1]
resultsFilePath = sys.argv[1][:-15]+'_results.csv'
print 'Extracting Identity Check results from '+str(iFilePath)
try:
	csvReader = csv.reader(open(iFilePath,'rb'), delimiter=',', quotechar = '"')
	csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')
except:
	print 'Error opening files'
	
headerRow = []
headerRow.append("Error")
headerRow.append("Primary Phone IsValid")
headerRow.append("Primary Phone Warning")
headerRow.append("Primary Phone to Name")
headerRow.append("Primary Phone to Address")
headerRow.append("Primary Phone Subscriber Name")
headerRow.append("Primary Phone Country Code")
headerRow.append("Primary Phone Line Type")
headerRow.append("Primary Phone Carrier")
headerRow.append("Primary Phone Is Prepaid")
headerRow.append("Primary Phone Is Connected")
headerRow.append("Primary Phone Is Commercial")
headerRow.append("Primary Address IsValid")
headerRow.append("Primary Address Warning")
headerRow.append("Primary Address Diagnostic")
headerRow.append("Primary Address to Name")
headerRow.append("Primary Address Resident Name")
headerRow.append("Primary Address Type")
headerRow.append("Primary Address Is Active")
headerRow.append("Primary Address Is Commercial")
headerRow.append("Secondary Phone IsValid")
headerRow.append("Secondary Phone Warning")
headerRow.append("Secondary Phone to Name")
headerRow.append("Secondary Phone to Address")
headerRow.append("Secondary Phone Subscriber Name")
headerRow.append("Secondary Phone Country Code")
headerRow.append("Secondary Phone Line Type")
headerRow.append("Secondary Phone Carrier")
headerRow.append("Secondary Phone Is Prepaid")
headerRow.append("Secondary Phone Is Connected")
headerRow.append("Secondary Phone Is Commercial")
headerRow.append("Secondary Address IsValid")
headerRow.append("Secondary Address Warning")
headerRow.append("Secondary Address Diagnostic")
headerRow.append("Secondary Address to Name")
headerRow.append("Secondary Address Resident Name")
headerRow.append("Secondary Address Type")
headerRow.append("Secondary Address Is Active")
headerRow.append("Secondary Address Is Commercial")
headerRow.append("Email Error")
headerRow.append("Email Warning")
headerRow.append("Email Is Valid")
headerRow.append("Email Is Valid Details")
headerRow.append("Email Is Disposable")
headerRow.append("Email Is Auto-Generated")
headerRow.append("Email to Name")
headerRow.append("Email Registered Name")
headerRow.append("Email First Seen Date")
headerRow.append("Email First Seen Days")
headerRow.append("Email Domain Creation Date")
headerRow.append("Email Domain Creation Days")
headerRow.append("IP Warning")
headerRow.append("IP Distance From Address")
headerRow.append("IP Distance From Phone")
headerRow.append("IP Location Postal Code")
headerRow.append("IP Location City")
headerRow.append("IP Location Country")
headerRow.append("IP Location Continent")
headerRow.append("IP Is Proxy")
headerRow.append("IP Connection Type")

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	
	rowNum += 1
	if rowNum == 1:
		csvWriter.writerow(row[:-2]+headerRow)
	else:
		data = {}
		try:
			data = json.loads(row[-1])
		except:
			print 'Error reading JSON on row '+str(rowNum)
			csvWriter.writerow(row[:-2]+['Failed to load JSON results'])
			continue
		resultRow = []
		resultRow.append('')
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.warnings',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.phone_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.phone_to_address',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.subscriber_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.country_code',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.line_type',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.carrier',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.is_prepaid',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.is_connected',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.phone.is_commercial',''),''))
		
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.diagnostics',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.address_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.resident_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.type',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.is_active',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('primary.address.is_commercial',''),''))
		
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.warnings',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.phone_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.phone_to_address',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.subscriber_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.country_code',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.line_type',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.carrier',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.is_prepaid',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.is_connected',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.phone.is_commercial',''),''))
		
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.diagnostics',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.address_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.resident_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.type',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.is_active',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('secondary.address.is_commercial',''),''))
		
		resultRow.append(wppbatchlib.nvl(data.get('email.error',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(data.get('email.syntax_is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.diagnostics',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(data.get('email.is_disposable',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.is_autogenerated',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.email_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.registered_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.email_first_seen_date',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.email_first_seen_days',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.email_domain_creation_date',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('email.email_domain_creation_days',''),''))
		
		resultRow.append(wppbatchlib.nvl(data.get('ip.warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(data.get('ip.distance_from_address',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('ip.distance_from_phone',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('ip.postal_code',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('ip.city_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('ip.country_name',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('ip.continent_code',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('ip.is_proxy',''),''))
		resultRow.append(wppbatchlib.nvl(data.get('ip.connection_type',''),''))
		decodedRow = []
		for a in resultRow:
			if a is None:
				a = ''
			try:
				decodedRow.append(a.encode('utf-8'))
			except:
				try:
					decodedRow.append(str(a))
				except:
					decodedRow.append(a)
			
		try:
			csvWriter.writerow(row[:-2]+decodedRow)
		except:
			csvWriter.writerow(row[:-2]+['Failed to parse API results'])

print 'All done!'
print 'You can find your results file here: '+str(resultsFilePath)
print ''
