import rticonnextdds_connector as rti
import time
import xmltodict
import sys
import socket
import random
import string
import requests

#print topics;
output=[];
input=[];
gen=[];
topic=[];
topic_subscribe=[];

def g1(arg1, arg2):
    gen1(arg1,arg2);
def g2(arg1, arg2):
   gen2(arg1,arg2);
def g3(arg1, arg2):
   gen3(arg1, arg2);
def g4(arg1,arg2):
   gen4(arg1, arg2);
def g5():
   gen5();

#list of generators
g={1: g1,
   2: g2,
   3: g3,
   4: g4,
   5: g5,};

#len(sys.argv) to get the entire length of the argument list
xml_file=sys.argv[1]; # gets the first argument
with open(xml_file) as file1: #xml file should be in the same root folder as this file else provide full path name
    doc = xmltodict.parse(file1.read());

domain_participant_library=doc['dds']['domain_participant_library']['@name'];
domain_participant_name=doc['dds']['domain_participant_library']['domain_participant']['@name'];

#protect connector calls via threads
connector = rti.Connector(domain_participant_library+ "::" + domain_participant_name,"./"+xml_file);

publisher=doc['dds']['domain_participant_library']['domain_participant']['publisher']['@name'];
subscriber=doc['dds']['domain_participant_library']['domain_participant']['subscriber']['@name'];
no_of_topics=len(doc['dds']['domain_participant_library']['domain_participant']['publisher']['data_writer']);
no_of_register_types=len(doc['dds']['domain_library']['domain']['register_type']);
no_of_data_types=len(doc['dds']['types']['struct']);


def printData(input,topics):

   while 1:
     for k in range(0,len(input)):
   	 input[k].take();
         numberOfSamples = input[k].samples.getLength();
   	 for j in range(1,numberOfSamples+1):
    	   pos,no_of_members=readTopicData(topics[k]);
   	   if input[k].infos.isValid(j):
                print ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]);
                        
    	        for i in range(0,no_of_members):
         	   if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='string'):
             		 print input[k].samples.getString(j,doc['dds']['types']['struct'][pos]['member'][i]['@name']);
        	   else:
              		if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='long'):
              			print input[k].samples.getNumber(j,doc['dds']['types']['struct'][pos]['member'][i]['@name']);
                        else:
             			if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='short'):
	      	  			print input[k].samples.getNumber(j,doc['dds']['types']['struct'][pos]['member'][i]['@name']);
	  	                else:
             				if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='boolean'):
			    			print input[k].samples.getBoolean(j,doc['dds']['types']['struct'][pos]['member'][i]['@name']);
 	  		       	        else:
            		  		   if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='char'):
				   	      print input[k].samples.getString(j,doc['dds']['types']['struct'][pos]['member'][i]['@name']);
 					   else:
             				      if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='float'):
						print input[k].samples.getNumber(j,doc['dds']['types']['struct'][pos]['member'][i]['@name']);
 					      else:
             					if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='double'):
						  print input[k].samples.getNumber(j,doc['dds']['types']['struct'][pos]['member'][i]['@name']);
	
	


#Generators
def generate(out,gen,topic):
    for i in range(0,len(out)):
       print "Using " + gen[i] + " to generate" + topic[i];
       num=int(gen[i][1])
       g[num](out[i],topic[i]);
       print "Data generated successfully!";


#add more print statements like publishing....published	
def publish(initial_position):
        
        assert(not(sys.argv[initial_position]==subscriber) or i<len(sys.argv)),"No topics specified for the publisher";
	for i in range(initial_position,len(sys.argv),2):#3 is not correct, will re-publish everytime
        	inputValid=False;
                #Error: When no argument is passed instead of the type of generator
                assert(i+1<len(sys.argv)),"No generator specified for Topic:"+sys.argv[i];
		
		if(sys.argv[i]==subscriber):
			subscribe(initial_position+1);
		else:
                        for j in range(0,no_of_topics):
                                
                                topic_name=doc['dds']['domain_participant_library']['domain_participant']['publisher']['data_writer'][j]['@topic_ref'];
				if(sys.argv[i]==topic_name):
                                        data_writer=doc['dds']['domain_participant_library']['domain_participant']['publisher']['data_writer'][j]['@name'];
                                        output.append(connector.getOutput(publisher + "::" + data_writer));
                                        topic.append(topic_name);
                                       
			               	if(sys.argv[i+1]=="g1" or "g2" or "g3" or "g4" or "g5"):
                                           gen.append(sys.argv[i+1]);
                                           inputValid=True;
                                        
                                        assert(inputValid),"No generator specified for Topic:"+sys.argv[i];
               
                        assert(inputValid),"No topic specified for the publisher. Correct Format for parameter list:";
                        initial_position=initial_position+2;
                        generate(output,gen,topic);                
                                             				
        print "Published";
def subscribe(initial_position):

        assert(not(sys.argv[initial_position]==publisher) or i<len(sys.argv)),"No topics specified for the Subscriber";
	for i in range(initial_position,len(sys.argv)):
        	inputValid=False;
             
		if(sys.argv[i]==publisher):
			publish(initial_position+1);
		else:
                        for j in range(0,no_of_topics):
                                
                                topic_name=doc['dds']['domain_participant_library']['domain_participant']['publisher']['data_writer'][j]['@topic_ref'];
				if(sys.argv[i]==topic_name):
                                        data_reader=doc['dds']['domain_participant_library']['domain_participant']['subscriber']['data_reader'][j]['@name'];
                                        input.append(connector.getInput(subscriber + "::" + data_reader));
                                        topic_subscribe.append(topic_name);
                                        inputValid=True;
                                       
                        assert(inputValid),"No topic specified for the subscriber. Correct Format for parameter list:";
                       
        printData(input,topic_subscribe);  
        initial_position=initial_position+1;                                 				
        print "subscribed";

#Reads topic info from xml file
def readTopicData(topic_name):
    for i in range(0, no_of_topics):
      if(doc['dds']['domain_library']['domain']['topic'][i]['@name']==topic_name):
            register_type=doc['dds']['domain_library']['domain']['topic'][i]['@register_type_ref'];
    for i in range(0, no_of_register_types): 
      if(doc['dds']['domain_library']['domain']['register_type'][i]['@name']==register_type): 
         topic_type=doc['dds']['domain_library']['domain']['register_type'][i]['@type_ref']; 
    for i in range(0, no_of_data_types):  
          if(doc['dds']['types']['struct'][i]['@name']==topic_type):
             no_of_members=len(doc['dds']['types']['struct'][i]['member']);
             pos=i;   
    return pos,no_of_members;   

#Generator implementation          
def gen1(output,topic_name):
    n = random.randint(0,59)
    print "delay is:",n,"seconds"
    pos,no_of_members=readTopicData(topic_name);
    for i in range(0,no_of_members):
           if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=="string"):
	      word_file ="http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	      response = requests.get(word_file)
              WORDS = response.content.splitlines()
              word = random.choice(WORDS)
	      print "string is:",word
              output.instance.setString(doc['dds']['types']['struct'][pos]['member'][i]['@name'],word);
           else:
              if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='long'):
	        f = random.randint(-9223372036854775808,9223372036854775807)
		print "long:",f
              	output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],f);
              else:
             	 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='short'):
                        u = random.randint(-128,127)
                        print "value of short is:",u
	      		output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],u);
	  	 else:
             		 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='boolean'):
				y = random.randint(0,1)
				print "value of bool is:",y
				output.instance.setBoolean(doc['dds']['types']['struct'][pos]['member'][i]['@name'],y);
 	  		 else:
            		  	if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='char'):
					o = random.choice(string.ascii_letters + string.digits)
					print "value of char:",o
					output.instance.setString(doc['dds']['types']['struct'][pos]['member'][i]['@name'],o);
 				else:
             			 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='float'):
				        p = random.uniform(-3.4E+38 , 3.4E+38)
					print "float value:",p
					output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],p);
 				 else:
             				 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='double'):
						 do = random.uniform(-1.7E+308 , 1.7E+308)
					         print "double value:",do
						 output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],do);
					 else:
                                               "Wrong type of topic for this generator";
                                               sys.exit();
    h = int(raw_input("print times"));
    for p in range(0,h):    
        output.write();
        time.sleep(n);
#prints string nine times and add nine to short
def gen2(output,topic_name):
    n = random.randint(0,59)
    print "delay is:",n,"seconds"
    pos,no_of_members=readTopicData(topic_name);
    '''g = int(raw_input("Number of times it is to be generated"));
    for k in range(0,g):'''
    for i in range(0,no_of_members):
           if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=="string"):
			mystring = doc['dds']['types']['struct'][pos]['member'][i]['@name'];
			word_file ="http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	      		response = requests.get(word_file)
              		WORDS = response.content.splitlines()
              		word = random.choice(WORDS)
	      		print "string is:",word
              		output.instance.setString(mystring,word*9);
           else:
              if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='long'):
		f = random.randint(-9223372036854775808,9223372036854775807)
		print "long:",f
              	output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],f);
              else:
             	 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='short'):
			u = random.randint(-128,127)
                        print "value of short is:",u
	      		output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],u+9);
	  	 else:
             		 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='boolean'):
				y = random.randint(0,1)
				print "value of bool is:",y
				output.instance.setBoolean(doc['dds']['types']['struct'][pos]['member'][i]['@name'],y);
 	  		 else:
            		  	if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='char'):
					o = random.choice(string.ascii_letters + string.digits)
					print "value of char:",o
					output.instance.setString(doc['dds']['types']['struct'][pos]['member'][i]['@name'],o;
 				else:
             			 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='float'):
					p = random.uniform(-3.4E+38 , 3.4E+38)
					print "float value:",p
					output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],p);
 				 else:
             				 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='double'):
						 do = random.uniform(-1.7E+308 , 1.7E+308)
					         print "double value:",do
						output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],do);
					 else:
                                               "Wrong type of topic for this generator";
                                               sys.exit();
    h = int(raw_input("print times"));
    for p in range(0,h):
    	output.write();
        time.sleep(n);

def gen3(output,topic_name):
    n = int(raw_input("delay in seconds BETWEEN SETS"));
    pos,no_of_members=readTopicData(topic_name);
    for i in range(0,no_of_members):
           if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=="string"):
			mystring = doc['dds']['types']['struct'][pos]['member'][i]['@name'];
              		output.instance.setString(mystring,(raw_input("Enter a string2:")));
           else:
              if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='long'):
              	output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],long(raw_input("Enter a value of type long: ")));
              else:
             	 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='short'):
	      		output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],int(raw_input("Enter an integer of type short: ")));
	  	 else:
             		 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='boolean'):
				st = bool(raw_input("Enter a bool value: ")); 
				tp = not st 
				output.instance.setBoolean(doc['dds']['types']['struct'][pos]['member'][i]['@name'], tp);
 	  		 else:
            		  	if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='char'):
					output.instance.setString(doc['dds']['types']['struct'][pos]['member'][i]['@name'],raw_input("Enter a character: "));
 				else:
             			 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='float'):
					output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],float(raw_input("Enter a floating point number: ")));
 				 else:
             				 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='double'):
						output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],float(raw_input("Enter a double: ")));
					 else:
                                               "Wrong type of topic for this generator";
                                               sys.exit();
    h3 = int(raw_input("print times"));
    for p3 in range(0,h3):    
        output.write();
        time.sleep(n);
#count no of vowels
def gen4(output,topic_name):
    n = int(raw_input("delay in seconds BETWEEN SETS"));
    pos,no_of_members=readTopicData(topic_name);
    for i in range(0,no_of_members):
           if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=="string"):
			mystring = raw_input("Enter a string2:");
			a = "a"
			A = "A"
			e = "e"
			E = "E"
			xi = "i"
			I = "I"
			o = "o"
			O = "O"
			u = "u"
			U = "U"
			count =0; 
			for j in range(0,len(mystring)):              
                          print mystring[j];
			  if (mystring[j]== "A" or mystring[j]=="a" or mystring[j]=="i" or mystring[j]=="I" or mystring[j]== "e" or mystring[j]== "E" or mystring[j]=="o" or mystring[j]=="O" or mystring[j]== "u" or mystring[j]=="U"): 
				count= count +1;
			give = ("Total vowels" + str(count));
            		output.instance.setString(doc['dds']['types']['struct'][pos]['member'][i]['@name'],give);
           else:
              if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='long'):
              	output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],long(raw_input("Enter a value of type long: ")));
              else:
             	 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='short'):
	      		output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],int(raw_input("Enter an integer of type short: ")));
	  	 else:
             		 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='boolean'):
				st = bool(raw_input("Enter a bool value: ")); 
				tp = not st 
				output.instance.setBoolean(doc['dds']['types']['struct'][pos]['member'][i]['@name'], tp);
 	  		 else:
            		  	if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='char'):
					output.instance.setString(doc['dds']['types']['struct'][pos]['member'][i]['@name'],raw_input("Enter a character: "));
 				else:
             			 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='float'):
					output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],float(raw_input("Enter a floating point number: ")));
 				 else:
             				 if(doc['dds']['types']['struct'][pos]['member'][i]['@type']=='double'):
						output.instance.setNumber(doc['dds']['types']['struct'][pos]['member'][i]['@name'],float(raw_input("Enter a double: ")));
					 else:
                                               "Wrong type of topic for this generator";
                                               sys.exit();
    h4 = int(raw_input("print times"));
    for p4 in range(0,h4):    
        output.write();    
        time.sleep(n);     
#Main
#neither publisher nor subscriber 
argument_pos=3;
if(sys.argv[2]==publisher):
	publish(argument_pos);
else:
	if(sys.argv[2]==subscriber):
		subscribe(argument_pos);
	else:
	        print sys.argv[2]
		print publisher
		print "Wrong Parameter list! Correct format:";
connector.delete();
#print len(doc['dds']['types']['struct'][0]['member']);


