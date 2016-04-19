import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;

import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.util.FileManager;

public class ER_Diseases {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		String query = "PREFIX rdfdisease: <http://www4.wiwiss.fu-berlin.de/diseasome/resource/diseases/> \n" +
					   "PREFIX rdfname: <http://www4.wiwiss.fu-berlin.de/diseasome/resource/diseasome/> \n" +
				       "PREFIX rdfsame: <http://www.w3.org/2002/07/owl#> \n" +
					   "SELECT ?disease_name ?other_name \n" +
					   "WHERE { \n" +
					   "?disease_link rdfname:name ?disease_name . \n" +
					   "?disease_link rdfsame:sameAs ?other_name . \n" +
					   "}";
		
		String str_to_check="http://www.dbpedia.org/resource/";
		String inputFile = "/home/soorya/diseasome_dump.nt";
		String outp = "/home/soorya/ER-Disease.txt";
		InputStream in = FileManager.get().open(inputFile);
		File file = new File(outp);
	    if (!file.exists()) 
	    {
	       file.createNewFile();
	    }
	    FileWriter fw = new FileWriter(file.getAbsoluteFile());
	    BufferedWriter bw = new BufferedWriter(fw);
		Model model = ModelFactory.createDefaultModel(); 
		if (in != null)
        {
                model.read(in, null, "N-TRIPLE");
        }
		QueryExecution exec = QueryExecutionFactory.create(query, model);
		ResultSet rs = exec.execSelect();
	    while(rs.hasNext())
	    {
	    	QuerySolution sol = rs.next();
	    	RDFNode dname = sol.get("other_name");	
	    	if(dname.toString().contains(str_to_check))
	    	{
	    		String other_name = sol.getResource("other_name").getLocalName();
	    		if(!sol.get("disease_name").toString().equals(other_name))
	    			bw.write(sol.get("disease_name")+"\t"+other_name+"\n");
	    	}
	    	
	    }
	    
	    bw.close();
	    System.out.println("Done Processing");
	}

}
