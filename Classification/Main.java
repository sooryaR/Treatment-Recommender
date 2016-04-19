import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;

import org.apache.jena.query.Dataset;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.tdb.TDBFactory;
import org.apache.jena.util.FileManager;

public class Main {

	//class to query the required fields from N-Triples file by loading into TDB loader.
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		String query = " PREFIX rdftrial: <http://data.linkedct.org/resource/trial/> \n" +
					   " PREFIX rdflabel: <http://www.w3.org/2000/01/rdf-schema#> \n" +
					   " PREFIX rdfgen: <http://data.linkedct.org/vocab/resource/> \n" +
					   "SELECT ?id ?title ?condition ?phase ?prim_measure ?prim_desc ?sec_measure ?sec_desc ?interv_type ?interv_name ?interv_desc  \n" +
					   "WHERE { \n" +
					   "?trial rdfgen:trialid ?id . \n" +
					   "?trial rdfgen:brief_title ?title . \n" +
					   "?trial rdfgen:trial_condition ?condition . \n" +
					   "?trial rdfgen:trial_primary_outcome ?primary_link . \n" +
					   "?trial rdfgen:trial_secondary_outcome ?secondary_link . \n" +
					   "?trial rdfgen:trial_intervention ?intervention_link . \n" +
					   "?primary_link rdfgen:outcome_measure ?prim_measure . \n" +
					   "?secondary_link rdfgen:outcome_measure ?sec_measure . \n" +
					   "?primary_link rdfgen:outcome_description ?prim_desc . \n" +
					   "?secondary_link rdfgen:outcome_description ?sec_desc . \n" +
					   "?intervention_link rdfgen:intervention_description ?interv_desc . \n" +
					   "?intervention_link rdfgen:intervention_intervention_name ?interv_name . \n" +
					   "?intervention_link rdfgen:intervention_intervention_type ?interv_type . \n" +
					   "?trial rdfgen:phase ?phase . \n" +
					   "}";
					  
					   
		String inputFile = "/home/soorya/linkedct-dump-2015-07-01.nt";
		String outp = "/home/soorya/Treatment-Recommender/Dataset.txt";
		String directory = "/home/soorya/Treatment-Recommender/Dataset/MedicalDataTDB";
		Dataset dataset = TDBFactory.createDataset(directory);
		Model tdb = dataset.getDefaultModel();
		FileManager.get().readModel(tdb,inputFile,"N-TRIPLES");
		Query q = QueryFactory.create(query);
		QueryExecution qexec = QueryExecutionFactory.create(q,tdb);
		ResultSet rs = qexec.execSelect();
		File file = new File(outp);
	    if (!file.exists()) 
	    {
	       file.createNewFile();
	    }
	    FileWriter fw = new FileWriter(file.getAbsoluteFile());
	    BufferedWriter bw = new BufferedWriter(fw);
	    while(rs.hasNext())
	    {
	    	QuerySolution sol = rs.next();
	    	String condition = sol.getResource("condition").getLocalName();
	    	bw.write(sol.get("id")+"\t"+sol.get("title")+"\t"+condition+"\t"+sol.get("phase")+"\t"+sol.get("prim_measure")+"\t"+sol.get("prim_desc")+"\t"+sol.get("sec_measure")+"\t"+sol.get("sec_desc")+"\t"+sol.get("interv_type")+"\t"+sol.get("interv_name")+"\t"+sol.get("interv_desc")+"\n");
	    }
	    bw.close();
        System.out.println("Done Processing!");
	}
	
}