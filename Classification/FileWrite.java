import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

public class FileWrite {
	
   // class to create seperate files for all the trials and write the content after classification.
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String filename = "/home/soorya/Treatment-Recommender/Dataset/Dataset.csv";
		String outFile; 
		String temp= "/home/soorya/Treatment-Recommender/Dataset/TrialFiles/";
		CSVReader reader;
		CSVWriter writer = null;
		String [] header= "ID,Title,Condition,Phase,Primary_Measure,Primary_Description,Secondary_Measure,Secondary_Description,Intervention_Type,Intervention_Name,Intervention_Description".split(",");
		try
		{
			reader = new CSVReader(new FileReader(filename));
			String[] row;
			HashSet<String> hs = new HashSet<String>();
			row=reader.readNext();
			while ((row = reader.readNext()) != null)
			{
				if(!hs.contains(row[0]))
				{
					hs.add(row[0]);
					if(writer!=null)writer.close();
					outFile="";
					outFile = temp+row[0]+".csv";
				    writer = new CSVWriter(new FileWriter(outFile));
				    writer.writeNext(header);
				    writer.writeNext(row); 	
				}
				else
				{
					writer.writeNext(row);
				}
				row=null;
			}
			System.out.println("Files Created and written successfully!");
		}
		catch (FileNotFoundException e) 
        {
                System.err.println(e.getMessage());
        }
        catch (IOException e) 
        {
                System.err.println(e.getMessage());
        }

	}

}
