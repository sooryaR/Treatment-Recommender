package Crawler;

import java.io.*;
import java.net.*;
import java.util.*;
import java.lang.*;

import com.csvreader.CsvWriter;

public class Crawler {

	static Hashtable<String,String[]> symptoms=new Hashtable<String,String[]>();
	static Hashtable<String,String[]> treatments=new Hashtable<String,String[]>();
        
    public static void read_csv() throws IOException
    {
            String csvFile = "C:\\Soorya\\Final Year Project\\crawler\\disease_list.csv";
	    BufferedReader br = null;
	    String line = "";
	    String cvsSplitBy = ",";
        try 
        {
                    br = new BufferedReader(new FileReader(csvFile));
                    br.readLine();
		    while ((line = br.readLine()) != null)
		    {
		        // use comma as separator
			    String[] disease = line.split(cvsSplitBy);
			    String[] symp = disease[1].split("\\|");
                            symptoms.put(disease[0],symp);

                            String[] tms = disease[2].split("\\|");
                            treatments.put(disease[0],tms);
		   }

	} catch (FileNotFoundException e) {
		e.printStackTrace();
	} catch (IOException e) {
		e.printStackTrace();
	} finally {
		if (br != null) {
			try {
				br.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

    }
    public static void main(String[] args) throws IOException {
       
    URL url,url1;
    InputStream is = null,is1=null;
    BufferedReader br,br1;
    String line="",line1="",condition="";
    String gender="",loc="",name="",val="",val1="";
    int page_num=0;
    boolean flag=false;
    read_csv();
    Random r = new Random();
    String outputFile = "patients_file.csv";
    
    try {
      while(page_num<1189)
      {
        System.setProperty("http.agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36"); 
        page_num+=1;
        String link_crawl="https://www.patientslikeme.com/patients?patient_page="+Integer.toString(page_num)+"&utm_campaign=day_04_ms&utm_medium=email&utm_source=welcome";
        url = new URL(link_crawl);
        is = url.openStream();  // throws an IOException
        br = new BufferedReader(new InputStreamReader(is));

        while ((line = br.readLine()) != null) {
        	
            if(line.contains("<a href=\"/patients/view/"))
            {
                //condition=name="";
            	int Nindex1=line.indexOf(">");
            	int Nindex2=line.indexOf("</");
            	int Lindex1=line.indexOf("href=");
            	int Lindex2=line.indexOf("\">");
            	name = line.substring(Nindex1+1,Nindex2);
            	String link = line.substring(Lindex1+16,Lindex2);
            	link="https://www.patientslikeme.com/patients/"+link;
            	System.out.println("Name: "+name+" Link: "+link);
            	
                try
                {
                 String urlLink=link;
                 url1 = new URL(urlLink);
                 is1 = url1.openStream();  // throws an IOException
                 br1 = new BufferedReader(new InputStreamReader(is1));
                
                 while((line1=br1.readLine())!=null)
                 {
                    
                	if(line1.contains("Male,") || line1.contains("Female,"))
                     {
                		gender=line1;
                		br1.readLine();
                		String temp=br1.readLine();
                		loc=temp;
                		continue;
                		
                	}
                	if(line1.contains("<dt>Primary condition")) {
                		br1.readLine();
                		br1.readLine();
                		String tmp2=br1.readLine();
                		if(tmp2.contains("</abbr>")) {
                			int i1=tmp2.indexOf("title=");
                			int i2=tmp2.indexOf(">",i1+7);
                			condition=tmp2.substring(i1+7,i2-1);
                		}
                		else {
                			int Index1=tmp2.indexOf(">");
                                        int Index2=tmp2.indexOf("</");
                                        condition = tmp2.substring(Index1+1,Index2);
                		}
                		break;
                	}
                }
	            if(symptoms.containsKey(condition))
	            {
                                  //System.out.println("Found Symptoms");
	                	  String symp[]=symptoms.get(condition);
	                	  int total=r.nextInt(symp.length-1);
                                  if(total==0)total+=2;
	                	  int cnt=0;
	                	  Set<String> set=new HashSet<String>();
	                	  while(cnt<total)
	                	  {
	                		  int rand_num=r.nextInt(symp.length);
	                		  if(!set.contains(symp[rand_num]))
	                		  {
	                			  cnt++;
	                			  set.add(symp[rand_num]);
	                			  if(cnt==total)
	                				  val+=symp[rand_num];
	                			  else
	                				  val=val+symp[rand_num]+",";
	                		  }
	                	  }
                          
	            }
	                  
	            if(treatments.containsKey(condition))
	            {
                          
                                  flag=true;
	                	  String tms[]=treatments.get(condition);
	                	  int total=r.nextInt(tms.length-1);
                                  if(total==0)total+=2;
	                	  int cnt=0;
	                	  Set<String> set=new HashSet<String>();
	                	  while(cnt<total)
	                	  {
	                		  int rand_num=r.nextInt(tms.length);
	                		  if(!set.contains(tms[rand_num]))
	                		  {
	                			  cnt++;
	                			  set.add(tms[rand_num]);
	                			  if(cnt==total)
	                				  val1+=tms[rand_num];
	                			  else
	                				  val1=val1+tms[rand_num]+",";
	                		  }
	                	  }
	                	  
	
	            }
	            
                }
                catch(Exception e)
                {
                	System.out.println(e);
                }
                if(gender.equals("")||loc.equals(""))flag=false;
                if(flag) {
                CsvWriter csvoutput = new CsvWriter(new FileWriter(outputFile, true), ',');
        
                    System.out.println(name+" "+gender+" "+loc+" "+condition+" "+val+" "+val1);
                    csvoutput.write(name);
                    csvoutput.write(gender);
                    csvoutput.write(loc);
                    csvoutput.write(condition);
                    csvoutput.write(val);
                    csvoutput.write(val1);
                    csvoutput.endRecord();
                    csvoutput.close();
                }
                name=gender=loc=condition=val=val1="";
                flag=false;
            }
            }
        }
       
    } catch (MalformedURLException mue) {
         mue.printStackTrace();
    } catch (IOException ioe) {
         ioe.printStackTrace();
    } finally {
        try {
            if (is != null) is.close();
        } catch (IOException ioe) {
           
        }
    }
    }
    
}