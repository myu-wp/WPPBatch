import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'


iFilePath = None
resultsFilePath = None

if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
	print 'Drop a CSV file containing raw JSON results onto this program to use it.'
	print '(you need to run SearchPhone.bat first)'
	var = raw_input("Hit enter to quit")
	quit()

iFilePath = sys.argv[1]
resultsFilePath = sys.argv[1][:-15]+'_results.csv'
print 'Extracting Phone Intelligence results from '+str(iFilePath)

csvReader = csv.reader(open(iFilePath,'rbU'), delimiter=',', quotechar = '"')
csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	rowNum += 1
	
	if rowNum == 1:
		headers = ['Error']
		headers.append('Line Type')
		headers.append('Carrier')
		headers.append('Is Valid')
		headers.append('Is Connected')
		headers.append('Is Prepaid')
		headers.append('Do Not Call Registered')
		headers.append('Reputation Level')
		headers.append('Reputation Details')
		headers.append('Report Count')
		headers.append('Volume Score')
		csvWriter.writerow(row[:-2]+headers)
	else:
		data = {}
		try:
			data = json.loads(row[-1])
		except:
			print 'Error reading JSON on row '+str(rowNum)
			csvWriter.writerow(row[:-2]+['Failed to load JSON results','','','',''])
			continue
		
		error = wppbatchlib.nvl(data.get('error',{}),{}).get('message','')
		results = wppbatchlib.nvl(data.get('results',[{}]),[{}])[0]
		lineType = results.get('line_type','')
		carrier = results.get('carrier','')
		isValid = results.get('is_valid','')
		isConnected = results.get('is_connected','')
		isPrepaid = results.get('is_prepaid','')
		dncRegistered = results.get('do_not_call','')
		rep = wppbatchlib.nvl(results.get('reputation',{}),{})
		repLevel = rep.get('level','')
		repVolume = rep.get('volume_score','')
		repReport = rep.get('report_count','')
		repDetails = ''
		numDetails = 0
		for x in rep.get('details',[]):
			numDetails += 1
			if numDetails > 1:
				repDetails += '|'
			repDetails += x.get('type','')
			repDetails += ';'
			repDetails += x.get('category','')
			repDetails += ';'
			repDetails += str(x.get('score',''))
		resultRow = [error]
		resultRow.append(lineType)
		resultRow.append(carrier)
		resultRow.append(isValid)
		resultRow.append(isConnected)
		resultRow.append(isPrepaid)
		resultRow.append(dncRegistered)
		resultRow.append(repLevel)
		resultRow.append(repDetails)
		resultRow.append(repReport)
		resultRow.append(repVolume)
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

