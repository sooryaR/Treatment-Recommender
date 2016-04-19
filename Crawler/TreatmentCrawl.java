import java.io.*;
import java.net.*;
import java.util.*;
import java.lang.*;


public class TreatmentCrawl {

	public static void main(String[] args) throws IOException {
		
		Hashtable<String,String> treatment_link=new Hashtable<String,String>();
        Hashtable<String,Integer> check_link=new Hashtable<String,Integer>();
		File file = new File("treatment_links.txt");
        // creates the file
        file.createNewFile();
        // creates a FileWriter Object
        FileWriter writer = new FileWriter(file);
			
		URL url,url1;
	    InputStream is = null,is1=null;
	    BufferedReader br,br1;
	    String line="",line1="";
	    System.setProperty("http.agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36");
        BufferedReader br_f = new BufferedReader(new FileReader("conditions_link.txt"));
        while ((line = br_f.readLine()) != null) 
        {
                if(check_link.containsKey(line))
                    continue;
                check_link.put(line,1);
        		String link="https://www.patientslikeme.com"+line;
        		System.out.println(link);
        		
        		try {
        			
        			String urlLink=link;
                    url1 = new URL(urlLink);
                    is1 = url1.openStream();  // throws an IOException
                    br1 = new BufferedReader(new InputStreamReader(is1));
                    
                    while((line1=br1.readLine())!=null) {
                    	
                    	
                    	if(line1.contains("<div class=\"mim-inline-label tertiary-title\">Treatment name(s)</div>")) {
                    		
                    		String tmp=br1.readLine();
                    		int i1=tmp.indexOf("itemprop=\"name\"");
                    		int i2=tmp.indexOf("</span>");
                    		int i3=tmp.indexOf("href=");
                    		int i4=tmp.indexOf(">",i3);
                    		String t_name=tmp.substring(i1+16,i2);
                    		String t_link=tmp.substring(i3+6,i4-1);
                    		
                    		//System.out.println(t_name+" "+t_link);
                    	
                    	   if(treatment_link.containsKey(t_name)){
                    			continue;
                    		}
                    		//System.out.println(t_name+" "+t_link);
                    		treatment_link.put(t_name,t_link);
                    	}
                    }
        			
        		}catch(Exception e) {}
        }
        Set<String> keys = treatment_link.keySet();
        for(String key: keys){
            System.out.println("Value of "+key+" is: "+treatment_link.get(key));
        }
        
        for(String key: keys){
            writer.write(key+","+treatment_link.get(key));
            writer.write("\n");
        }
        writer.flush();
        writer.close();
	}
}
