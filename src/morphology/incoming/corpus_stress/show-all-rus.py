import sys, subprocess;

# INPUT: 
#  ^Все/весь¹<det><mfn><nn><pl><acc>/весь¹<det><nt><sg><acc>/весь¹<det><nt><sg><nom>/весь¹<det><pl><nom>/все<prn><pl><nom>/всё<prn><nt><sg><acc>/всё<prn><nt><sg><nom>$ ^счастливые/счастливый<adj><mfn><an><pl><nom>/счастливый<adj><mfn><nn><pl><acc>$ ^семьи/семья<n><f><nn><pl><acc>/семья<n><f><nn><pl><nom>/семья<n><f><nn><sg><gen>$ ^похожи/похожий<adj><short><mfn><pl>$ ^друг на друга/на<pr>+друг друга<prn><recip><acc>$^,/,<cm>$ ^каждая/каждая<prn><f><sg><nom>/каждый<det><f><sg><nom>$ ^несчастливая/несчастливый<adj><f><an><sg><nom>$ ^семья/семья<n><f><nn><sg><nom>$ ^несчастлива/несчастливый<adj><short><f><sg>$ ^по-своему/по-своему<adv>$^./.<sent>$^./.<sent>$[][
#
#]
#
# OUTPUT:
#  Все счастли́вые семьи похо́жи дру̀г на дру́га, ка́ждая несчастли́вая семья́ несча́стлива по-сво́ему..[][
#
#]
#
#
# USAGE:
#  $ cat inputfile | python3 show-all-rus.py generator-mt-apertium-norm.hfstol 2>/dev/null
# 

c = sys.stdin.read(1);

cache = {};
generator = sys.argv[1];
state = 0;
surface = '';
analyses = [];
analyysi = '';
while c != '': #{
	if not c: #{
		break;
	#}

	if c == '^': #{
		state = 1;
		c = sys.stdin.read(1);
		continue;
	elif c == '/': #{
		if analyysi != '': #{
			analyses.append(analyysi.strip('/'));
		#}
		analyysi = '';
		state = 2;
	elif c == '$': #{
		if analyysi != '': #{
			analyses.append(analyysi.strip('/'));
		#}
		analyysit = list(set(analyses));
		# generate forms here.
		results = set();
		for analyysi in analyysit: #{
			analyysi = analyysi.replace('"', '\\"');
			result = '';
			if analyysi not in cache: #{
				result = subprocess.check_output('echo ' + '"^'+analyysi+'$"' + ' | hfst-proc -n ' + generator , shell=True)
				result = result.decode('utf-8').strip();
				cache[analyysi] = result;
			else: #{
				result = cache[analyysi];
			#}
			if result.count('/') > 0: #{
				for res in result.split('/'): #{
					res = res.strip('\/');
					if res != '': #{
						results.add(res);
					#}
				#}
			else: #{
				results.add(result);
			#}
		#}
		results = list(results);
		print('!', surface, '|||', analyysit, '|||', results, file=sys.stderr);
		if len(results) == 1: #{
			sys.stdout.write(results[0]);
		else: #{
			sys.stdout.write(surface);
		#}
		sys.stdout.flush();
		state = 0;
		analyysi = '';
		analyses = [];
		surface = '';
		c = sys.stdin.read(1);
		continue;
	#}

	if state == 0: #{
		sys.stdout.write(c);
	elif state == 1: #{
		surface = surface + c;
	elif state == 2: #{
		analyysi = analyysi + c;	
	#}	

	c = sys.stdin.read(1);
#}
