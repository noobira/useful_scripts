//Maya ASCII 2018ff09 scene
//Name: footRoll_setup.ma
//Last modified: Thu, Apr 29, 2021 10:24:40 PM
//Codeset: 1251
requires maya "2018ff09";
requires "stereoCamera" "10.0";
requires -nodeType "floatMath" "lookdevKit" "1.0";
requires "mtoa" "4.0.4.2";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201807191615-2c29512b8a";
fileInfo "osv" "Microsoft Windows 8 , 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "2C16EFF3-4BCF-712F-328E-EDA10447E986";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1.2282365027784661 12.529888008117652 8.1955587134355738 ;
	setAttr ".r" -type "double3" -60.338352729607145 7.4000000000023309 -1.2027253093481334e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "B8A514FF-4848-6A63-27F6-4B9DA60E651D";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 15.05087325423483;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "569A3930-4A60-9096-9B62-25B32076637C";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "FAF445FC-4345-5F4E-9A2B-698447D31817";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "ED2FB09C-41D7-B0CF-EBE0-91A28E91AB3F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "0FC7E1D2-4E24-2AE1-84D4-468C15F9F3DC";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "58E6399C-4A0A-8F59-ACE1-7A98841F819E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "6944123C-4AA9-CE7D-0640-93B619AA6083";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "Rt_IKLeg_align";
	rename -uid "D6C052E2-4F75-0AC6-8F96-998AF99CF5EC";
	setAttr ".t" -type "double3" 0 0.84983532411011953 -0.068643641764144156 ;
createNode transform -n "Rt_IKFootRoll_CON_GRP" -p "Rt_IKLeg_align";
	rename -uid "44E3FBBC-4E11-05A6-10D1-F48AE03FBA11";
createNode transform -n "Rt_IKFootRoll_CON" -p "Rt_IKFootRoll_CON_GRP";
	rename -uid "5DCD3BA1-4CC1-E20C-43DF-2883259FE874";
	addAttr -ci true -sn "rotate_pivot" -ln "rotate_pivot" -at "double";
	addAttr -ci true -sn "foot_to_ball" -ln "foot_to_ball" -min 0 -max 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".ry";
	setAttr ".ro" 3;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mnrl" -type "double3" -90 -45 -45 ;
	setAttr ".mxrl" -type "double3" 90 45 45 ;
	setAttr ".mrxe" yes;
	setAttr ".mrze" yes;
	setAttr ".xrxe" yes;
	setAttr ".xrze" yes;
	setAttr -k on ".rotate_pivot";
	setAttr -k on ".foot_to_ball" 0.7;
createNode nurbsCurve -n "Rt_IKFootRoll_CONShape" -p "Rt_IKFootRoll_CON";
	rename -uid "CE80F064-44E7-8497-3C7B-E3824B28FA3D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.48993103095342388 2.9999623443003649e-17 -0.48993103095342438
		4.2425874339181583e-17 4.2425874339181583e-17 -0.6928671086017637
		-0.48993103095342388 2.9999623443003649e-17 -0.48993103095342366
		-0.69286710860176426 2.1993648175911648e-33 -3.5918353261078192e-17
		-0.48993103095342388 -2.9999623443003649e-17 0.48993103095342388
		-6.9404972142152179e-17 -4.2425874339181638e-17 0.69286710860176437
		0.48993103095342388 -2.9999623443003649e-17 0.48993103095342366
		0.69286710860176426 -5.7856015039986627e-33 9.4486042964009309e-17
		0.48993103095342388 2.9999623443003649e-17 -0.48993103095342438
		4.2425874339181583e-17 4.2425874339181583e-17 -0.6928671086017637
		-0.48993103095342388 2.9999623443003649e-17 -0.48993103095342366
		;
createNode nurbsCurve -n "Rt_IKFootRoll_CONShape1" -p "Rt_IKFootRoll_CON";
	rename -uid "120E2543-4134-C973-CFD0-DE9DEED81544";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.48993103095342388 0.48993103095342438 -7.8786918765562655e-17
		4.2425874339181583e-17 0.6928671086017637 -1.11421529055846e-16
		-0.48993103095342388 0.48993103095342366 -7.878691876556263e-17
		-0.69286710860176426 3.5918353261078192e-17 -5.7761117418226462e-33
		-0.48993103095342388 -0.48993103095342388 7.8786918765562655e-17
		-6.9404972142152179e-17 -0.69286710860176437 1.11421529055846e-16
		0.48993103095342388 -0.48993103095342366 7.878691876556263e-17
		0.69286710860176426 -9.4486042964009309e-17 1.5194514576874302e-32
		0.48993103095342388 0.48993103095342438 -7.8786918765562655e-17
		4.2425874339181583e-17 0.6928671086017637 -1.11421529055846e-16
		-0.48993103095342388 0.48993103095342366 -7.878691876556263e-17
		;
createNode nurbsCurve -n "Rt_IKFootRoll_CONShape2" -p "Rt_IKFootRoll_CON";
	rename -uid "818FBEC2-47A9-79C8-7E3B-8590C228411E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.8786918765562655e-17 0.48993103095342388 -0.48993103095342438
		-4.2425874339181583e-17 4.2425874339181589e-17 -0.6928671086017637
		-1.3878616565156978e-16 -0.48993103095342388 -0.48993103095342366
		-1.5384740339502751e-16 -0.69286710860176426 -3.5918353261078192e-17
		-7.8786918765562655e-17 -0.48993103095342388 0.48993103095342388
		4.2425874339181589e-17 -6.9404972142152203e-17 0.69286710860176437
		1.3878616565156978e-16 0.48993103095342388 0.48993103095342366
		1.5384740339502751e-16 0.69286710860176426 9.4486042964009309e-17
		7.8786918765562655e-17 0.48993103095342388 -0.48993103095342438
		-4.2425874339181583e-17 4.2425874339181589e-17 -0.6928671086017637
		-1.3878616565156978e-16 -0.48993103095342388 -0.48993103095342366
		;
createNode transform -n "Rt_nearestGuide" -p "Rt_IKFootRoll_CON";
	rename -uid "77F59780-4DCB-017D-99EC-1B93EF78822F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -7.4593109467002705e-17 1.5 -4.2329963319265307e-16 ;
createNode locator -n "Rt_nearestGuideShape" -p "Rt_nearestGuide";
	rename -uid "0230AEF3-45C2-15CF-AA18-F49AD528D040";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 0.1 0.1 0.1 ;
createNode transform -n "Rt_infoCircle" -p "Rt_IKFootRoll_CON_GRP";
	rename -uid "8536775C-4697-B01B-C8BF-7BAF676DB585";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
createNode nurbsCurve -n "Rt_infoCircleShape" -p "Rt_infoCircle";
	rename -uid "8902E209-413F-6C52-03A8-47BC2A08A53E";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.45325421887794304 2.7753816417445336e-17 0.26168644528051466
		0.52337289056102843 3.2047346759303072e-17 -2.6457602145538006e-16
		0.45325421887794326 2.7753816417445355e-17 -0.26168644528051416
		0.26168644528051421 1.6023673379651542e-17 -0.45325421887794348
		5.5914140731335072e-17 1.0539694123750137e-32 -0.5233728905610282
		-0.26168644528051421 -1.602367337965153e-17 -0.45325421887794354
		-0.45325421887794326 -2.7753816417445349e-17 -0.26168644528051427
		-0.52337289056102831 -3.2047346759303066e-17 -2.1414667154201641e-16
		-0.45325421887794348 -2.775381641744537e-17 0.26168644528051399
		-0.26168644528051438 -1.6023673379651555e-17 0.45325421887794332
		-3.7726795888689437e-16 -3.021694036364945e-32 0.52337289056102831
		0.26168644528051394 1.6023673379651512e-17 0.45325421887794354
		0.45325421887794304 2.7753816417445336e-17 0.26168644528051466
		0.52337289056102843 3.2047346759303072e-17 -2.6457602145538006e-16
		0.45325421887794326 2.7753816417445355e-17 -0.26168644528051416
		;
createNode transform -n "Rt_footRollLimitLoc_GRP" -p "Rt_IKLeg_align";
	rename -uid "61B9AA37-403D-A9A3-9474-F39C807E477E";
	setAttr ".t" -type "double3" 1.0867024199147393 -0.84983532411011953 0.068643641764144156 ;
createNode transform -n "Rt_footRollLimitLoc" -p "Rt_footRollLimitLoc_GRP";
	rename -uid "6CC62375-4FB8-0EFB-841C-059E6E0EC89F";
	setAttr ".it" no;
createNode locator -n "Rt_footRollLimitLocShape" -p "Rt_footRollLimitLoc";
	rename -uid "60E7C418-416F-6847-67C0-2984CF9A5FDC";
	setAttr -k off ".v";
	setAttr ".tmp" yes;
	setAttr ".los" -type "double3" 0.2 0.2 0.2 ;
createNode transform -n "Rt_FootRollLimitCrv" -p "Rt_IKLeg_align";
	rename -uid "45EC1BCB-4D33-FA5D-65C7-1B892B8AFC39";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 0 4.7626297211555979e-09 ;
createNode nurbsCurve -n "Rt_FootRollLimitCrvShape" -p "Rt_FootRollLimitCrv";
	rename -uid "435E5DFE-41ED-EEE9-B9F3-928849D44C26";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9.0000000000000018 10 11 12 13 14
		15
		0.56887395084012471 -0.8498350977897644 1.5612275715278177
		0.52626023194430049 -0.8498350977897644 0.9108213670123706
		0.52325504800920741 -0.8498350977897644 -0.078127545066675963
		0.50242185017412377 -0.8498350977897644 -0.48892111072254485
		-4.8122506361056315e-16 -0.8498350977897644 -0.67653416640316666
		-0.41542780736995288 -0.8498350977897644 -0.48892107616107305
		-0.45993190827866243 -0.8498350977897644 -0.16039426402594648
		-0.60690409419344127 -0.8498350977897644 0.76553286722838509
		-0.63802510406199753 -0.8498350977897644 1.750589163399805
		-0.36480968460619273 -0.8498350977897644 1.9471002164803664
		0.017906785011291209 -0.8498350977897644 2.0559358878623888
		0.50661595287158612 -0.8498350977897644 1.8761190241802876
		0.56887395084012471 -0.8498350977897644 1.5612275715278177
		0.52626023194430049 -0.8498350977897644 0.9108213670123706
		0.52325504800920741 -0.8498350977897644 -0.078127545066675963
		;
createNode transform -n "Rt_IKRollToes_GRP" -p "Rt_IKLeg_align";
	rename -uid "8A727540-470F-E67A-674E-F9B0463C65FB";
	setAttr ".t" -type "double3" 0.016254344635476814 -0.66611707947155818 1.3423192111827451 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 0.99999999999999967 ;
createNode transform -n "Rt_IKRollToes_CON" -p "Rt_IKRollToes_GRP";
	rename -uid "8E15A3EF-41EF-24FE-70F7-EA8AA06C7FFE";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "Rt_IKRollToes_CONShape" -p "Rt_IKRollToes_CON";
	rename -uid "4D5D8F39-401A-C471-0B8D-B0A72F5CF7C5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 28 0 no 3
		29 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28
		29
		-9.1120725305798121e-16 0.63174610077927562 -0.19493899247333202
		-9.6477323716491073e-16 0.85745017897934939 -0.11728055371015325
		-9.3581683312575491e-16 0.72950344775557574 -0.1324451584721475
		-9.4459727479226384e-16 0.76321027134568131 -0.10485442988863516
		-9.6094698817493688e-16 0.82341431487942862 -0.041915394426811699
		-9.7970592187257932e-16 0.88418944279746625 0.067788806884556879
		-9.9139745459941087e-16 0.91126620118698953 0.18494987034331772
		-9.9514370594364484e-16 0.90258435860653174 0.30089304836118397
		-9.9067083120579266e-16 0.85879215109309226 0.4070816248662405
		-9.7830619052442271e-16 0.78310602939602758 0.49569242651842693
		-9.5897740751309088e-16 0.68117849473888681 0.56019349991790401
		-9.4234397816548456e-16 0.60048553508998848 0.58398759972555947
		-9.334516403498542e-16 0.55869798607664789 0.59060398328355812
		-9.6228290982205408e-16 0.67760796239049426 0.64402273880661975
		-9.0862513121874042e-16 0.44527482566057403 0.59442625446539021
		-9.3521079657315304e-16 0.59753676602106576 0.45120775154154658
		-9.2869993929964011e-16 0.54605176282188628 0.55040195611622733
		-9.3674349266746026e-16 0.5838510507805047 0.54441525680678249
		-9.5179946392722678e-16 0.65689059439801556 0.52288118273497219
		-9.6928074879137803e-16 0.7490782617534022 0.46453334623991249
		-9.8047194762321848e-16 0.81757656865876815 0.38435443826815979
		-9.8451598166242221e-16 0.85718497045667186 0.28827989022283018
		-9.8112934131177348e-16 0.86505110587438694 0.18338648881506892
		-9.705472240782725e-16 0.84053841598032364 0.077366651635446648
		-9.5358139866186604e-16 0.78557532070068481 -0.02186358125340139
		-9.3878221406678331e-16 0.73107995886997956 -0.078830244767581353
		-9.3083988833048552e-16 0.70059095552129913 -0.10378924802086575
		-9.3665394169532443e-16 0.70175536137396788 0.010032362978443475
		-9.1120725305798121e-16 0.63174610077927562 -0.19493899247333202
		;
createNode transform -n "Rt_IKToes_GRP" -p "Rt_IKLeg_align";
	rename -uid "E84A30E1-4137-3BE9-8103-6B950908D73F";
	setAttr ".t" -type "double3" 0.016254344635476592 -0.6661170794715584 1.3423192111827462 ;
	setAttr ".s" -type "double3" 0.99999999999999956 1 0.99999999999999956 ;
createNode transform -n "Rt_IKToes_CON" -p "Rt_IKToes_GRP";
	rename -uid "F1AFAB18-4482-6A09-8D6B-BCAB8B2048BB";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "Rt_IKToes_CONShape" -p "Rt_IKToes_CON";
	rename -uid "A6B89062-492A-8A38-2635-559D9FDFE99E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32
		33
		-1.558525483392996e-16 0.34481237149472277 0.8211689817392761
		-0.11589533911884144 0.25860919255281795 0.93405124447349075
		-0.033044517500440657 0.25860919255281795 0.93405124447349075
		-0.033044517500440657 0.1724060136109134 0.99346310665903281
		-0.033044517500440657 0.034002319124031927 1.0291101551157795
		-0.17240601361091368 0.03400231912403192 0.99346310665903281
		-0.25860919255281822 0.034002319124031899 0.93405124447349075
		-0.25860919255281822 0.11589533911884124 0.93405124447349075
		-0.34481237149472282 6.550273462419568e-17 0.8211689817392761
		-0.25860919255281822 -0.11589533911884106 0.93405124447349075
		-0.25860919255281822 -0.034002319124031753 0.93405124447349075
		-0.17240601361091368 -0.034002319124031739 0.99346310665903281
		-0.033044517500440657 -0.034002319124031732 1.0291101551157795
		-0.033044517500440657 -0.17240601361091323 0.99346310665903281
		-0.033044517500440657 -0.25860919255281778 0.93405124447349097
		-0.11589533911884144 -0.25860919255281778 0.93405124447349097
		-1.558525483392996e-16 -0.34481237149472266 0.82116898173927633
		0.11589533911884096 -0.25860919255281778 0.93405124447349097
		0.0330445175004404 -0.25860919255281778 0.93405124447349097
		0.0330445175004404 -0.17240601361091323 0.99346310665903281
		0.0330445175004404 -0.034002319124031732 1.0291101551157795
		0.17240601361091304 -0.034002319124031739 0.99346310665903281
		0.25860919255281772 -0.034002319124031753 0.93405124447349075
		0.25860919255281772 -0.11589533911884106 0.93405124447349075
		0.3448123714947226 6.550273462419568e-17 0.8211689817392761
		0.25860919255281772 0.11589533911884124 0.93405124447349075
		0.25860919255281772 0.034002319124031899 0.93405124447349075
		0.17240601361091304 0.03400231912403192 0.99346310665903281
		0.0330445175004404 0.034002319124031927 1.0291101551157795
		0.0330445175004404 0.1724060136109134 0.99346310665903281
		0.0330445175004404 0.25860919255281795 0.93405124447349075
		0.11589533911884096 0.25860919255281795 0.93405124447349075
		-1.558525483392996e-16 0.34481237149472277 0.8211689817392761
		;
createNode transform -n "Lf_IKLeg_align";
	rename -uid "84476A4B-417E-9A4E-305E-92A013024626";
	setAttr ".t" -type "double3" 0 0.84983532411011953 -0.068643641764144156 ;
createNode transform -n "Lf_IKFootRoll_CON_GRP" -p "Lf_IKLeg_align";
	rename -uid "9AE24F80-4D78-44D6-3F73-AA80C01EA8CD";
createNode transform -n "Lf_IKFootRoll_CON" -p "Lf_IKFootRoll_CON_GRP";
	rename -uid "1704F5CB-441B-4AA5-F8BD-B884876D1F0F";
	addAttr -ci true -sn "rotate_pivot" -ln "rotate_pivot" -at "double";
	addAttr -ci true -sn "foot_to_ball" -ln "foot_to_ball" -min 0 -max 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".ry";
	setAttr ".ro" 3;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mnrl" -type "double3" -90 -45 -45 ;
	setAttr ".mxrl" -type "double3" 90 45 45 ;
	setAttr ".mrxe" yes;
	setAttr ".mrze" yes;
	setAttr ".xrxe" yes;
	setAttr ".xrze" yes;
	setAttr -k on ".rotate_pivot";
	setAttr -k on ".foot_to_ball" 0.7;
createNode nurbsCurve -n "Lf_IKFootRoll_CONShape" -p "Lf_IKFootRoll_CON";
	rename -uid "230751EC-4EE8-971E-5A73-2E921849E44C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.48993103095342388 2.9999623443003649e-17 -0.48993103095342438
		4.2425874339181583e-17 4.2425874339181583e-17 -0.6928671086017637
		-0.48993103095342388 2.9999623443003649e-17 -0.48993103095342366
		-0.69286710860176426 2.1993648175911648e-33 -3.5918353261078192e-17
		-0.48993103095342388 -2.9999623443003649e-17 0.48993103095342388
		-6.9404972142152179e-17 -4.2425874339181638e-17 0.69286710860176437
		0.48993103095342388 -2.9999623443003649e-17 0.48993103095342366
		0.69286710860176426 -5.7856015039986627e-33 9.4486042964009309e-17
		0.48993103095342388 2.9999623443003649e-17 -0.48993103095342438
		4.2425874339181583e-17 4.2425874339181583e-17 -0.6928671086017637
		-0.48993103095342388 2.9999623443003649e-17 -0.48993103095342366
		;
createNode nurbsCurve -n "Lf_IKFootRoll_CONShape1" -p "Lf_IKFootRoll_CON";
	rename -uid "B7BADBFC-4DC3-0EC2-B179-E0BCA10D2E40";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.48993103095342388 0.48993103095342438 -7.8786918765562655e-17
		4.2425874339181583e-17 0.6928671086017637 -1.11421529055846e-16
		-0.48993103095342388 0.48993103095342366 -7.878691876556263e-17
		-0.69286710860176426 3.5918353261078192e-17 -5.7761117418226462e-33
		-0.48993103095342388 -0.48993103095342388 7.8786918765562655e-17
		-6.9404972142152179e-17 -0.69286710860176437 1.11421529055846e-16
		0.48993103095342388 -0.48993103095342366 7.878691876556263e-17
		0.69286710860176426 -9.4486042964009309e-17 1.5194514576874302e-32
		0.48993103095342388 0.48993103095342438 -7.8786918765562655e-17
		4.2425874339181583e-17 0.6928671086017637 -1.11421529055846e-16
		-0.48993103095342388 0.48993103095342366 -7.878691876556263e-17
		;
createNode nurbsCurve -n "Lf_IKFootRoll_CONShape2" -p "Lf_IKFootRoll_CON";
	rename -uid "98727935-48D0-D81E-05D6-3893F99AB10A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.8786918765562655e-17 0.48993103095342388 -0.48993103095342438
		-4.2425874339181583e-17 4.2425874339181589e-17 -0.6928671086017637
		-1.3878616565156978e-16 -0.48993103095342388 -0.48993103095342366
		-1.5384740339502751e-16 -0.69286710860176426 -3.5918353261078192e-17
		-7.8786918765562655e-17 -0.48993103095342388 0.48993103095342388
		4.2425874339181589e-17 -6.9404972142152203e-17 0.69286710860176437
		1.3878616565156978e-16 0.48993103095342388 0.48993103095342366
		1.5384740339502751e-16 0.69286710860176426 9.4486042964009309e-17
		7.8786918765562655e-17 0.48993103095342388 -0.48993103095342438
		-4.2425874339181583e-17 4.2425874339181589e-17 -0.6928671086017637
		-1.3878616565156978e-16 -0.48993103095342388 -0.48993103095342366
		;
createNode transform -n "Lf_nearestGuide" -p "Lf_IKFootRoll_CON";
	rename -uid "4AC93CEA-4A84-DD2F-9B52-6ABC0228A7D7";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -7.4593109467002705e-17 1.5 -4.2329963319265307e-16 ;
createNode locator -n "Lf_nearestGuideShape" -p "Lf_nearestGuide";
	rename -uid "B302260B-4C34-CFAA-74C7-3F85723215C8";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 0.1 0.1 0.1 ;
createNode transform -n "Lf_infoCircle" -p "Lf_IKFootRoll_CON_GRP";
	rename -uid "75598A43-4717-86F7-1128-6A85F6D4C97C";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
createNode nurbsCurve -n "Lf_infoCircleShape" -p "Lf_infoCircle";
	rename -uid "F7F96A7D-49E4-8BA8-ECCD-2480F9408D15";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.45325421887794304 2.7753816417445336e-17 0.26168644528051466
		0.52337289056102843 3.2047346759303072e-17 -2.6457602145538006e-16
		0.45325421887794326 2.7753816417445355e-17 -0.26168644528051416
		0.26168644528051421 1.6023673379651542e-17 -0.45325421887794348
		5.5914140731335072e-17 1.0539694123750137e-32 -0.5233728905610282
		-0.26168644528051421 -1.602367337965153e-17 -0.45325421887794354
		-0.45325421887794326 -2.7753816417445349e-17 -0.26168644528051427
		-0.52337289056102831 -3.2047346759303066e-17 -2.1414667154201641e-16
		-0.45325421887794348 -2.775381641744537e-17 0.26168644528051399
		-0.26168644528051438 -1.6023673379651555e-17 0.45325421887794332
		-3.7726795888689437e-16 -3.021694036364945e-32 0.52337289056102831
		0.26168644528051394 1.6023673379651512e-17 0.45325421887794354
		0.45325421887794304 2.7753816417445336e-17 0.26168644528051466
		0.52337289056102843 3.2047346759303072e-17 -2.6457602145538006e-16
		0.45325421887794326 2.7753816417445355e-17 -0.26168644528051416
		;
createNode transform -n "Lf_footRollLimitLoc_GRP" -p "Lf_IKLeg_align";
	rename -uid "D1522614-4629-77AF-95CC-FF9827491188";
	setAttr ".t" -type "double3" 1.0867024199147393 -0.84983532411011953 0.068643641764144156 ;
createNode transform -n "Lf_footRollLimitLoc" -p "Lf_footRollLimitLoc_GRP";
	rename -uid "5C7FC322-412A-05FF-CF8F-D1BD0630B205";
	setAttr ".it" no;
createNode locator -n "Lf_footRollLimitLocShape" -p "Lf_footRollLimitLoc";
	rename -uid "76B7AD30-467D-785E-E0D4-728E0240F2E7";
	setAttr -k off ".v";
	setAttr ".tmp" yes;
	setAttr ".los" -type "double3" 0.2 0.2 0.2 ;
createNode transform -n "Lf_FootRollLimitCrv" -p "Lf_IKLeg_align";
	rename -uid "C3D2B6D8-4B9E-AC78-7394-03ABF62FBFBC";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 0 4.7626297211555979e-09 ;
createNode nurbsCurve -n "Lf_FootRollLimitCrvShape" -p "Lf_FootRollLimitCrv";
	rename -uid "23787B1F-46CD-E652-A63E-B79B00A9BE07";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9.0000000000000018 10 11 12 13 14
		15
		-0.56887395084012471 -0.8498350977897644 1.5612275715278177
		-0.52626023194430049 -0.8498350977897644 0.9108213670123706
		-0.52325504800920741 -0.8498350977897644 -0.078127545066675963
		-0.50242185017412377 -0.8498350977897644 -0.48892111072254485
		4.8122506361056315e-16 -0.8498350977897644 -0.67653416640316666
		0.41542780736995288 -0.8498350977897644 -0.48892107616107305
		0.45993190827866243 -0.8498350977897644 -0.16039426402594648
		0.60690409419344127 -0.8498350977897644 0.76553286722838509
		0.63802510406199753 -0.8498350977897644 1.750589163399805
		0.36480968460619273 -0.8498350977897644 1.9471002164803664
		-0.017906785011291209 -0.8498350977897644 2.0559358878623888
		-0.50661595287158612 -0.8498350977897644 1.8761190241802876
		-0.56887395084012471 -0.8498350977897644 1.5612275715278177
		-0.52626023194430049 -0.8498350977897644 0.9108213670123706
		-0.52325504800920741 -0.8498350977897644 -0.078127545066675963
		;
createNode transform -n "Lf_IKRollToes_GRP" -p "Lf_IKLeg_align";
	rename -uid "7CB12080-40A0-6869-5320-72BB1F134B86";
	setAttr ".t" -type "double3" 0.016254344635476814 -0.66611707947155818 1.3423192111827451 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 0.99999999999999967 ;
createNode transform -n "Lf_IKRollToes_CON" -p "Lf_IKRollToes_GRP";
	rename -uid "B3D41391-4FE5-9DA1-DA6C-36A2DF6C67E1";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "Lf_IKRollToes_CONShape" -p "Lf_IKRollToes_CON";
	rename -uid "A3DA1A58-4104-A68F-67CC-5F94A9CDB3F5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 28 0 no 3
		29 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28
		29
		-9.1120725305798121e-16 0.63174610077927562 -0.19493899247333202
		-9.6477323716491073e-16 0.85745017897934939 -0.11728055371015325
		-9.3581683312575491e-16 0.72950344775557574 -0.1324451584721475
		-9.4459727479226384e-16 0.76321027134568131 -0.10485442988863516
		-9.6094698817493688e-16 0.82341431487942862 -0.041915394426811699
		-9.7970592187257932e-16 0.88418944279746625 0.067788806884556879
		-9.9139745459941087e-16 0.91126620118698953 0.18494987034331772
		-9.9514370594364484e-16 0.90258435860653174 0.30089304836118397
		-9.9067083120579266e-16 0.85879215109309226 0.4070816248662405
		-9.7830619052442271e-16 0.78310602939602758 0.49569242651842693
		-9.5897740751309088e-16 0.68117849473888681 0.56019349991790401
		-9.4234397816548456e-16 0.60048553508998848 0.58398759972555947
		-9.334516403498542e-16 0.55869798607664789 0.59060398328355812
		-9.6228290982205408e-16 0.67760796239049426 0.64402273880661975
		-9.0862513121874042e-16 0.44527482566057403 0.59442625446539021
		-9.3521079657315304e-16 0.59753676602106576 0.45120775154154658
		-9.2869993929964011e-16 0.54605176282188628 0.55040195611622733
		-9.3674349266746026e-16 0.5838510507805047 0.54441525680678249
		-9.5179946392722678e-16 0.65689059439801556 0.52288118273497219
		-9.6928074879137803e-16 0.7490782617534022 0.46453334623991249
		-9.8047194762321848e-16 0.81757656865876815 0.38435443826815979
		-9.8451598166242221e-16 0.85718497045667186 0.28827989022283018
		-9.8112934131177348e-16 0.86505110587438694 0.18338648881506892
		-9.705472240782725e-16 0.84053841598032364 0.077366651635446648
		-9.5358139866186604e-16 0.78557532070068481 -0.02186358125340139
		-9.3878221406678331e-16 0.73107995886997956 -0.078830244767581353
		-9.3083988833048552e-16 0.70059095552129913 -0.10378924802086575
		-9.3665394169532443e-16 0.70175536137396788 0.010032362978443475
		-9.1120725305798121e-16 0.63174610077927562 -0.19493899247333202
		;
createNode transform -n "Lf_IKToes_GRP" -p "Lf_IKLeg_align";
	rename -uid "7826CEB6-4A8C-FE35-F855-458E965F98FD";
	setAttr ".t" -type "double3" 0.016254344635476592 -0.6661170794715584 1.3423192111827462 ;
	setAttr ".s" -type "double3" 0.99999999999999956 1 0.99999999999999956 ;
createNode transform -n "Lf_IKToes_CON" -p "Lf_IKToes_GRP";
	rename -uid "DE53D5E9-4100-CD9C-1259-BDB622DD60A6";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "Lf_IKToes_CONShape" -p "Lf_IKToes_CON";
	rename -uid "7EDC8395-4A20-895E-75A9-BB89CFD0409E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32
		33
		-1.558525483392996e-16 0.34481237149472277 0.8211689817392761
		-0.11589533911884144 0.25860919255281795 0.93405124447349075
		-0.033044517500440657 0.25860919255281795 0.93405124447349075
		-0.033044517500440657 0.1724060136109134 0.99346310665903281
		-0.033044517500440657 0.034002319124031927 1.0291101551157795
		-0.17240601361091368 0.03400231912403192 0.99346310665903281
		-0.25860919255281822 0.034002319124031899 0.93405124447349075
		-0.25860919255281822 0.11589533911884124 0.93405124447349075
		-0.34481237149472282 6.550273462419568e-17 0.8211689817392761
		-0.25860919255281822 -0.11589533911884106 0.93405124447349075
		-0.25860919255281822 -0.034002319124031753 0.93405124447349075
		-0.17240601361091368 -0.034002319124031739 0.99346310665903281
		-0.033044517500440657 -0.034002319124031732 1.0291101551157795
		-0.033044517500440657 -0.17240601361091323 0.99346310665903281
		-0.033044517500440657 -0.25860919255281778 0.93405124447349097
		-0.11589533911884144 -0.25860919255281778 0.93405124447349097
		-1.558525483392996e-16 -0.34481237149472266 0.82116898173927633
		0.11589533911884096 -0.25860919255281778 0.93405124447349097
		0.0330445175004404 -0.25860919255281778 0.93405124447349097
		0.0330445175004404 -0.17240601361091323 0.99346310665903281
		0.0330445175004404 -0.034002319124031732 1.0291101551157795
		0.17240601361091304 -0.034002319124031739 0.99346310665903281
		0.25860919255281772 -0.034002319124031753 0.93405124447349075
		0.25860919255281772 -0.11589533911884106 0.93405124447349075
		0.3448123714947226 6.550273462419568e-17 0.8211689817392761
		0.25860919255281772 0.11589533911884124 0.93405124447349075
		0.25860919255281772 0.034002319124031899 0.93405124447349075
		0.17240601361091304 0.03400231912403192 0.99346310665903281
		0.0330445175004404 0.034002319124031927 1.0291101551157795
		0.0330445175004404 0.1724060136109134 0.99346310665903281
		0.0330445175004404 0.25860919255281795 0.93405124447349075
		0.11589533911884096 0.25860919255281795 0.93405124447349075
		-1.558525483392996e-16 0.34481237149472277 0.8211689817392761
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "FDD99F40-4771-6710-06CE-B2A123A2AB2C";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "2E8E1FEB-400A-EC02-53D5-1293B7CD0A0F";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "F2EC3306-440F-67FB-6BC7-B19951286C5A";
createNode displayLayerManager -n "layerManager";
	rename -uid "4EB24DCA-4F94-0B64-4AB7-829CFDBB95C3";
createNode displayLayer -n "defaultLayer";
	rename -uid "7F4B0F0C-4582-81DA-4576-C4B8E27FA13D";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "06D858AD-4F31-B3EB-2B9E-CC80A20D9B96";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "1DC9E2C7-4603-E985-0489-D2A938BC095A";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "8AC3B139-4C20-AD84-095C-C28C0BE22379";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode pointOnCurveInfo -n "Rt_pointOnCurveInfo_Roll";
	rename -uid "3DFBA805-480F-C729-8466-9F9742FD4FA1";
createNode nearestPointOnCurve -n "nearestPointOnCurve1";
	rename -uid "9A4354BC-4C63-232B-9214-E1AD7C0C619F";
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "24376073-47FE-DDAD-0410-64B2ED8EE374";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -474.99998112519665 -251.19046620906389 ;
	setAttr ".tgi[0].vh" -type "double2" 454.76188669129095 261.90475149760215 ;
createNode floatMath -n "Rt_floatMath2";
	rename -uid "DD25B7FA-4FB9-EB70-7FA1-0983F00090FB";
	setAttr "._fb" 180;
	setAttr "._cnd" 2;
createNode remapValue -n "Rt_remapValue_ToeEnd";
	rename -uid "873AFC3F-4944-E86A-0343-6097E50EA8B7";
	setAttr ".imx" 90;
	setAttr ".omn" -90;
	setAttr ".omx" 0;
	setAttr -s 3 ".vl[0:2]"  0 1 1 1 1 1 0.5 0.5 1;
	setAttr -s 2 ".cl";
	setAttr ".cl[0].cli" 1;
	setAttr ".cl[1].clp" 1;
	setAttr ".cl[1].clc" -type "float3" 1 1 1 ;
	setAttr ".cl[1].cli" 1;
createNode unitConversion -n "Rt_unitConversion202";
	rename -uid "7C08B554-4342-7165-A3BB-BB8F0BA92F63";
	setAttr ".cf" 57.295779513082323;
createNode remapValue -n "Rt_remapValue_Toe";
	rename -uid "05D1E022-4F7F-F3B5-4463-91BD0DA3CA24";
	setAttr ".imx" 90;
	setAttr -s 3 ".vl[2:4]"  0 0 1 0.5 0.5 1 1 0 1;
	setAttr -s 2 ".cl";
	setAttr ".cl[0].cli" 1;
	setAttr ".cl[1].clp" 1;
	setAttr ".cl[1].clc" -type "float3" 1 1 1 ;
	setAttr ".cl[1].cli" 1;
createNode unitConversion -n "Rt_unitConversion203";
	rename -uid "84C0428B-43AF-05CB-A2E2-67857E16DD25";
	setAttr ".cf" 57.295779513082323;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "46ABB5DA-4AE2-B6AB-FAB7-9F848FE31523";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 447.16679415540415 11.59849803931804 ;
	setAttr ".tgi[0].vh" -type "double2" 2047.1667492766144 788.06906449519943 ;
	setAttr -s 3 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 842.85711669921875;
	setAttr ".tgi[0].ni[0].y" 425.71429443359375;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 1457.142822265625;
	setAttr ".tgi[0].ni[1].y" 425.71429443359375;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 1150;
	setAttr ".tgi[0].ni[2].y" 425.71429443359375;
	setAttr ".tgi[0].ni[2].nvs" 18304;
createNode pointOnCurveInfo -n "Lf_pointOnCurveInfo_Roll";
	rename -uid "35DF3D34-4D39-9B70-7F34-0CB562CA5D85";
createNode nearestPointOnCurve -n "nearestPointOnCurve2";
	rename -uid "FE54F093-414A-C692-A83D-F08317C8F46F";
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo1";
	rename -uid "85BE6795-4B36-259E-AE6D-83BAC23DDFBD";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -474.99998112519665 -251.19046620906389 ;
	setAttr ".tgi[0].vh" -type "double2" 454.76188669129095 261.90475149760215 ;
createNode floatMath -n "Lf_floatMath2";
	rename -uid "338E6950-48C7-FA63-F29A-D490DEADCE6B";
	setAttr "._fb" 180;
	setAttr "._cnd" 2;
createNode remapValue -n "Lf_remapValue_ToeEnd";
	rename -uid "A53FD4F7-4D1D-B1B1-864A-B18CFB159197";
	setAttr ".imx" 90;
	setAttr ".omn" -90;
	setAttr ".omx" 0;
	setAttr -s 3 ".vl[0:2]"  0 1 1 1 1 1 0.5 0.5 1;
	setAttr -s 2 ".cl";
	setAttr ".cl[0].cli" 1;
	setAttr ".cl[1].clp" 1;
	setAttr ".cl[1].clc" -type "float3" 1 1 1 ;
	setAttr ".cl[1].cli" 1;
createNode unitConversion -n "Lf_unitConversion202";
	rename -uid "9078DBD2-40F2-4013-1151-58AF3DCC1EFD";
	setAttr ".cf" 57.295779513082323;
createNode remapValue -n "Lf_remapValue_Toe";
	rename -uid "1482E374-45F2-CC8C-3BA3-F2BADD9EAF7C";
	setAttr ".imx" 90;
	setAttr -s 3 ".vl[2:4]"  0 0 1 0.5 0.5 1 1 0 1;
	setAttr -s 2 ".cl";
	setAttr ".cl[0].cli" 1;
	setAttr ".cl[1].clp" 1;
	setAttr ".cl[1].clc" -type "float3" 1 1 1 ;
	setAttr ".cl[1].cli" 1;
createNode unitConversion -n "Lf_unitConversion203";
	rename -uid "CDF22707-49EF-5F9C-ED07-4587E0427B23";
	setAttr ".cf" 57.295779513082323;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av -k on ".unw" 1;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av ".ta";
	setAttr -av ".tq";
	setAttr -av ".tmr";
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -av ".hfd";
	setAttr -av ".hfs";
	setAttr -av ".hfe";
	setAttr -av ".hfcr";
	setAttr -av ".hfcg";
	setAttr -av ".hfcb";
	setAttr -av ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr ".msaa" yes;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".u";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -cb on ".ren" -type "string" "arnold";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".an";
	setAttr -cb on ".ar";
	setAttr -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -cb on ".me";
	setAttr -cb on ".se";
	setAttr -av -k on ".be";
	setAttr -av -cb on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -av -cb on ".pff";
	setAttr -av -cb on ".peie";
	setAttr -av -cb on ".ifp";
	setAttr -k on ".rv";
	setAttr -av -k on ".comp";
	setAttr -av -k on ".cth";
	setAttr -av -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -av -k on ".rd";
	setAttr -av -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -av -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -av -k on ".uf";
	setAttr -av -k on ".oi";
	setAttr -av -k on ".rut";
	setAttr -av -k on ".mot";
	setAttr -av -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -k on ".pram";
	setAttr -k on ".poam";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -cb on ".prm";
	setAttr -cb on ".pom";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -av -k on ".tlwd";
	setAttr -av -k on ".tlht";
	setAttr -av -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -av -k on ".ope";
	setAttr -av -k on ".oppf";
	setAttr -av -k on ".rcp";
	setAttr -av -k on ".icp";
	setAttr -av -k on ".ocp";
	setAttr -cb on ".hbl";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -av -k off -cb on ".fbfm";
	setAttr -av -k off -cb on ".ehql";
	setAttr -av -k off -cb on ".eams";
	setAttr -av -k off -cb on ".eeaa";
	setAttr -av -k off -cb on ".engm";
	setAttr -av -k off -cb on ".mes";
	setAttr -av -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -av -k off -cb on ".mbs";
	setAttr -av -k off -cb on ".trm";
	setAttr -av -k off -cb on ".tshc";
	setAttr -av -k off -cb on ".enpt";
	setAttr -av -k off -cb on ".clmt";
	setAttr -av -k off -cb on ".tcov";
	setAttr -av -k off -cb on ".lith";
	setAttr -av -k off -cb on ".sobc";
	setAttr -av -k off -cb on ".cuth";
	setAttr -av -k off -cb on ".hgcd";
	setAttr -av -k off -cb on ".hgci";
	setAttr -av -k off -cb on ".mgcs";
	setAttr -av -k off -cb on ".twa";
	setAttr -av -k off -cb on ".twz";
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "Rt_pointOnCurveInfo_Roll.p" "Rt_footRollLimitLoc.t";
connectAttr "Lf_pointOnCurveInfo_Roll.p" "Lf_footRollLimitLoc.t";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "nearestPointOnCurve1.pr" "Rt_pointOnCurveInfo_Roll.pr";
connectAttr "Rt_infoCircleShape.ws" "nearestPointOnCurve1.ic";
connectAttr "Rt_nearestGuideShape.wp" "nearestPointOnCurve1.ip";
connectAttr "Rt_IKFootRoll_CON.foot_to_ball" "Rt_floatMath2._fa";
connectAttr "Rt_unitConversion202.o" "Rt_remapValue_ToeEnd.i";
connectAttr "Rt_IKFootRoll_CON.rx" "Rt_unitConversion202.i";
connectAttr "Rt_unitConversion203.o" "Rt_remapValue_Toe.i";
connectAttr "Rt_floatMath2.of" "Rt_remapValue_Toe.omx";
connectAttr "Rt_IKFootRoll_CON.rx" "Rt_unitConversion203.i";
connectAttr "Rt_IKFootRoll_CON.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "Rt_remapValue_ToeEnd.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "Rt_unitConversion202.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "nearestPointOnCurve2.pr" "Lf_pointOnCurveInfo_Roll.pr";
connectAttr "Lf_infoCircleShape.ws" "nearestPointOnCurve2.ic";
connectAttr "Lf_nearestGuideShape.wp" "nearestPointOnCurve2.ip";
connectAttr "Lf_IKFootRoll_CON.foot_to_ball" "Lf_floatMath2._fa";
connectAttr "Lf_unitConversion202.o" "Lf_remapValue_ToeEnd.i";
connectAttr "Lf_IKFootRoll_CON.rx" "Lf_unitConversion202.i";
connectAttr "Lf_unitConversion203.o" "Lf_remapValue_Toe.i";
connectAttr "Lf_floatMath2.of" "Lf_remapValue_Toe.omx";
connectAttr "Lf_IKFootRoll_CON.rx" "Lf_unitConversion203.i";
connectAttr "Rt_remapValue_Toe.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_remapValue_ToeEnd.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_floatMath2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_remapValue_Toe.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_remapValue_ToeEnd.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_floatMath2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "Rt_remapValue_Toe.ov" ":internal_standInShader.ir";
connectAttr "Rt_remapValue_Toe.ov" ":internal_standInShader.ig";
connectAttr "Rt_remapValue_Toe.ov" ":internal_standInShader.ib";
// End of footRoll_setup.ma
