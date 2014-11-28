import sys;
import re

r = open(sys.argv[1]);
t = open(sys.argv[2]);

errors = 0.0;
tokens = 0.0;
wins = 0.0;

feiler = [];

Vowel = re.compile("[аэоуыяеёюи]")

while True: #{

	refline = r.readline();
	tstline = t.readline().replace('\u0300', '');

	if refline == '' or tstline == '': #{
		break;
	#}

	refrow = refline.split(' ');
	tstrow = tstline.split(' ');
	
	if len(refrow) != len(tstrow): #{
		print('ERROR:', file=sys.stderr);
		break;
	#}
	feil = 0.0;
	for i in range(0, len(tstrow)): #{
		if refrow[i].count('\u0301') < 1 or len(Vowel.findall(refrow[i])) < 2 : #{
			continue;
		#}

		if tstrow[i] != refrow[i]: #{
			feil = feil + 1.0;
			errors = errors + 1.0;
		else: #{
			wins = wins + 1.0;
		#}
		tokens = tokens + 1.0 ;
	#}	
	if feil > 0.0: #{
		feiler.append((refline, tstline));
	#}
#}

for feilline in feiler: #{
	print('- %s\n+ %s\n' % (feilline[0].strip(), feilline[1].strip()));
#}

print('err:',errors);
print('cor:',wins);
print('tok:',tokens);

print('acc: %.2f' % (wins/tokens*100.0));

