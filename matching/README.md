## How to collect the data used in the `match.py` script

### Department of Defense Data

1. Go to http://www.dodsbir.net/awards/ and change `AND Matches Within` to 
   `Keywords, Proposal Title and Abstract`
2. Search for `UAV`
3. Click `Printable Report`, then `Download to Excel`, and save as 
   `AwardsToExcel.csv` to the `data` directory of the `matching` folder.
   
### OpenSecrets Data

1. Go to https://www.opensecrets.org/api/admin/index.php?function=signup to 
   register.

2. Check your email to confirm registration, then log in.

3. Make sure you are logged in, then click `Bulk Data`, then `Lobbying Tables` 
   to begin downloading. Alternatively, try 
   http://www.opensecrets.org/MyOS/download.php?f=Lobby.zip to download 
   directly. Or (perhaps preferably) use the /data in your folder for this 
   session to avoid the large download.

4. Unzip the file, and add the file `lob_indus.txt` to the `data` directory of 
   the `matching` folder. You should find a copy already there in case you have 
   problems.
    
5. Note some differences with each file. `lob_indus.txt` has `,` separated 
   fields with pipes `|` enclosing text fields. It is also missing 
   column/header names. `AwardsToExcel.csv` also has `,` separated fields, but 
   uses `"` to enclose all fields, not just text.

### Bonus Code for Loading Data into MySQL

1. Create a new schema in MySQL:

```mysql
   CREATE DATABASE `icos`;
```

2. Create a new table in the schema for the DOD data.

```mysql
   CREATE TABLE `AwardsToExcel` (
     `Program` varchar(45) DEFAULT NULL,
     `Control_No` varchar(45) DEFAULT NULL,
     `FY` varchar(45) DEFAULT NULL,
     `FY_Report` varchar(45) DEFAULT NULL,
     `Agency` varchar(45) DEFAULT NULL,
     `Top_No` varchar(45) DEFAULT NULL,
     `Field_Off` varchar(45) DEFAULT NULL,
     `Proposal_Title` varchar(250) DEFAULT NULL,
     `Firm` varchar(100) DEFAULT NULL,
     `Street` varchar(100) DEFAULT NULL,
     `City` varchar(100) DEFAULT NULL,
     `State` varchar(45) DEFAULT NULL,
     `Zip` varchar(45) DEFAULT NULL,
     `URL` varchar(45) DEFAULT NULL,
     `Phase` int(11) DEFAULT NULL,
     `Woman` varchar(45) DEFAULT NULL,
     `Minority` varchar(45) DEFAULT NULL,
     `No_Employees` varchar(45) DEFAULT NULL,
     `PI_Name` varchar(100) DEFAULT NULL,
     `PI_Phone` varchar(45) DEFAULT NULL,
     `PI_Ext` varchar(45) DEFAULT NULL,
     `PI_Email` varchar(100) DEFAULT NULL,
     `CO_Name` varchar(100) DEFAULT NULL,
     `CO_Phone` varchar(100) DEFAULT NULL,
     `CO_Ext` varchar(45) DEFAULT NULL,
     `CO_Email` varchar(100) DEFAULT NULL,
     `Award_Amount` int(11) DEFAULT NULL,
     `Award_Date` varchar(45) DEFAULT NULL,
     `End_Date` varchar(45) DEFAULT NULL,
     `Contract` varchar(45) DEFAULT NULL,
     `Keywords` varchar(250) DEFAULT NULL,
     `Abstract` text DEFAULT NULL,
     `Proposal_No` varchar(45) DEFAULT NULL,
     `Full_Topic_No` varchar(45) DEFAULT NULL,
     `Solicitation` varchar(45) DEFAULT NULL
   ) ENGINE=MyISAM DEFAULT CHARSET=latin1;
```

3. Load the data into the table.

```mysql
   load data local infile 'AwardsToExcel.csv' 
      into table AwardsToExcel 
      fields 
         terminated by ',' 
         enclosed by '"'  
      lines terminated by ',\r\n' 
      ignore 1 lines;
```

   You will get a warning, `Row 879 doesn't contain data for all columns` that 
   we can ignore for now.

4. Create a new table in the schema for the OS data.

```mysql
   CREATE TABLE `lob_indus` (
     `Client` varchar(50) DEFAULT NULL,
     `Sub` varchar(50) DEFAULT NULL,
     `Total` int(11) DEFAULT NULL,
     `year` varchar(4) DEFAULT NULL,
     `Catcode` varchar(5) DEFAULT NULL
   ) ENGINE=MyISAM DEFAULT CHARSET=latin1;
```

5. Load the data into the table.

```mysql
   load data local infile 'lob_indus.txt' 
      into table lob_indus 
      fields 
         terminated by ',' 
         optionally enclosed by '|'  
      lines terminated by '\r\n' 
      ignore 0 lines;
```