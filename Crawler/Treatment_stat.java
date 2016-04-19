
import java.io.*;
import java.net.*;
import java.util.*;
import java.lang.*;


public class Treatment_stat {

	public static void main(String[] args) throws IOException {
		
		Hashtable<String,String> treatment_link=new Hashtable<String,String>();
		BufferedReader br = new BufferedReader(new FileReader("treatment_links.txt"));
		String line;
		String tname="",pcount="",peval="";
	    while ((line = br.readLine()) != null) {
	    	String[] parts = line.split(",");
	    	String fname=parts[0]+".txt";
	    	System.out.println(parts[0]);
	    	File file = new File(fname);
	    	if(file.exists())
	    		continue;
	        //creates the file
	        file.createNewFile();
	        //creates a FileWriter Object
	        FileWriter writer = new FileWriter(file); 
	    	try {
	    		URL url,url1;
	    		InputStream is = null,is1=null;
	    		BufferedReader br1,br2;
	    		String line1="",line2="";
	    		System.setProperty("http.agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36");
	    	    String link="https://www.patientslikeme.com"+parts[1];
	    	    url = new URL(link);
	            is = url.openStream();  // throws an IOException
	            br1 = new BufferedReader(new InputStreamReader(is));
	            
	            while((line1=br1.readLine())!=null) {
	            	
	            	if(line1.contains("<div class=\"reasons\">")) {
	            		writer.write("\n");
	            		//System.out.println("");
	            		if(line1.contains("</span>")) {
	            		    int index1=line1.indexOf("itemprop=\"name\"");
	            		    int index2=line1.indexOf(">",index1);
	            		    int index3=line1.indexOf("</span>");
	            		    tname=line1.substring(index2+1,index3);
	            		    writer.write(tname+",");
	            		    //System.out.print(tname+",");
	            			
	            		}
	            		else {
	            		 int index1=line1.indexOf("href=");
	            		 int index2=line1.indexOf(">",index1);
	            		 int index3=line1.indexOf("</a>");
	            		 tname=line1.substring(index2+1,index3);
	            		 writer.write(tname+",");
	            		 //System.out.print(tname+",");
	            		}
	            		
	            	}
	            	else if(line1.contains("<div class=\"patients numeric\">")) {
	            		
	            		int i1=line1.indexOf("href=");
	            		int i2=line1.indexOf(">",i1);
	            		int i3=line1.indexOf("</a>");
	            		pcount=line1.substring(i2+1,i3);
	            		writer.write(pcount+",");
	            		//System.out.print(pcount+",");
	            	}
	            	else if(line1.contains("<div class=\"evaluated numeric\">")) {
	            		if(line1.contains("href=")) {
	            		 int i1=line1.indexOf("href=");
	            		 int i2=line1.indexOf(">",i1);
	            		 int i3=line1.indexOf("</a>");
	            		 peval=line1.substring(i2+1,i3);
	            		 writer.write(peval+",");
	            		 //System.out.print(peval+",");
	            		}
	            		else {
	            			int i1=line1.indexOf(">",0);
	            			int i2=line1.indexOf("</div>");
	            			peval=line1.substring(i1+1,i2);
	            			writer.write(peval+",");
	            			//System.out.print(peval+",");
	            		}
	            		//writer.write(tname+","+pcount+","+peval+",");
	            		//System.out.println(tname+","+pcount+","+peval+",");
	            	}
	            	else if(line1.contains("<div class=\"mim-inline-label tertiary-title\">Perceived effectiveness</div>")) {
	            		
            			br1.readLine();
            			String tmp="";
            			while((tmp=br1.readLine())!="</div>"){
            				if(tmp.equals("</div>")) {
            					break;
            				}
            				int i1=tmp.indexOf("</small>",0);
                			String p=tmp.substring(4,i1);
                			writer.write(p+",");
                			//System.out.print(p+",");            			
            		    }
            	    }
	            	
	            	else if(line1.contains("<img alt=\"\" src=")) {
	            		writer.write("\n");
	            		//System.out.println("");
	            		if(line1.contains("</td>")) {
	            			br1.readLine();
	            			String tmp=br1.readLine();
	            			int i1=tmp.indexOf(">",0);
		            		int i2=tmp.indexOf("</a>");
		            		String s=tmp.substring(i1+1,i2);
		            		writer.write(s);
		            		//System.out.print(s);
	            		}
	            		else {
	            			br1.readLine();
	            			br1.readLine();
	            			String tmp=br1.readLine();
	            			int i1=tmp.indexOf(">",0);
		            		int i2=tmp.indexOf("</a>");
		            		String s=tmp.substring(i1+1,i2);
		            		writer.write(s);
		            		//System.out.print(s);
	            		}
	            	}
	            	
	            	
	            	
	            }
	    	 
	    	
	    	}catch(Exception e){ System.out.println(e);}
	        writer.flush();
	        writer.close();
	    	
	    	System.out.println("File finished");
	    }

	}
	
}
