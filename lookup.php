<?php
/*******************************************************
**
** darmc_lookup.php
** PHP CLI script
**
** Looks up a place by name from the DARMC database
**
** copyright 2012 Brendan Maione-Downing
**
** for internal use ONLY - DO NOT DISTRIBUTE
**
*******************************************************/

// declare a global array to read crom CSV
$arrCSV = array();

// check that the csv is there
if (!file_exists("darmc_settlements.csv"))
	die("ERROR: File not found.\n\n");

// Open the CSV, handling errors other than a missing file as well
elseif (($handle = fopen("darmc_settlements.csv", "r")) !==FALSE) 
{
	// Set the parent array key to 0
	$key = 0;

	// While there is data available from a CSV loop through
	while (($data = fgetcsv($handle, 0, ",")) !==FALSE) 
	{
		// Count the total keys in each row
		$c = count($data);
		//Populate the array
		for ($x=0;$x<$c;$x++) 
		{
			$arrCSV[$key][$x] = $data[$x];
		}
		$key++;
	}

	// Close the CSV file
	fclose($handle);
}

// handle any other error
else
	die("ERROR: An unspecified error occurred\n\n");

// print tool introduction
print("\nDARMC Lookup tool 2012 version 0.1.0\n");
print("Copyright Brendan Maione-Downing: DO NOT DISTRIBUTE\n");
print("Press ctrl-c to quit\n\n");

// loop forever
while(true)
{
	// get user input
	print("Enter a place name to search: ");
	$results = array();
	$fh = fopen('php://stdin', 'r');
	$query = trim(fgets($fh));

	// find all matching results
	foreach($arrCSV as $settlement)
	{
		if (strcasecmp($settlement[4], $query) == 0)
			$results[] = $settlement;
		elseif (strcasecmp($settlement[5], $query) == 0)
			$results[] = $settlement;
	}

	// format and print results if they are found
	if(!empty($results))
	{
		$count = count($results);
		
		// print results header	
		$word = "matches";
		if ($count == 1)
			$word = "match";
		print_r("\n == Found ".$count." ".$word." for ".$query." ==\n\n");
		
		// print out each result
		foreach ($results as $result)
			display($result);
	}

	// run a fuzzy search
	elseif (strlen($query) > 2)
	{
		//define an array of possible results
		$possible = array();
		foreach($arrCSV as $fuzzy)
		{	
			// dynamically vary tolerance of levenshtein function
			if (strlen($fuzzy[4]) <= 5) {$tol = 1;}
			else {$tol = 3;}
			
			// determine if entries may be fuzzy matches
			if (levenshtein($fuzzy[4], $query) <= $tol)
				$possible[] = $fuzzy;
		}
		// if some possible matches were found, display them
		if(!empty($possible))
		{
			$count = count($possible);

			// print results header line
			$word = "possible matches";
			if ($count == 1)
				$word = "possible match";
			print_r("\n == Found ".$count." ".$word." for ".$query." ==\n\n");
			
			// print results
			foreach ($possible as $possible)
				display($possible);
		}
		// else tell the user no matches were found
		else
			print("\n == No results found for ".$query." ==\n\n");
	}

	// else no results were found
	else
		print("\n == No results found for ".$query." ==\n\n");
}

function display($result)
{
	// print name and alternate name, if available
	if (strcasecmp($result[5]," ") == 0)
		print_r($result[4]);
	else
		print_r($result[4]." (".$result[5].")");

	// print settlement type if available	
	if (strcasecmp($result[9]," ") == 0)
		print_r("\n");
	else
		print_r(" [".$result[9]."]\n");

	// print Lat/Long coordinates
	print_r($result[6].",".$result[7]."\n");

	// print Pleiades URL
	print_r("Pleiades URL: ".$result[15]."\n\n");
}
?>