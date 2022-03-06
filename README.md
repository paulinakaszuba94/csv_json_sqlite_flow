In this repository you will find:

---- <b> Input files: </b> <br/>
-> <i> przypadki_pomocy_x.csv </i> <br/> <br/>

---- <b> Python script (<i>csv_json_sqlite_flow.py<i/>) that: <b/> <br/>
-> reads (many) .csv files to a DataFrame, <br/>
-> cleans data (preprocessing), <br/>
-> creates .json file from DataFrame (<i>uokik_2022-03-06_pages_1_2.json<i/>), <br/>
-> based on .json file creates .sqlite DB (<i>beneficiaries.sqlite<i/>) where data is inserted, <br/>
-> builds a specific VIEW in DB (the same result saved in <i>total_support_nominal_value_pln.xlsx<i/>). <br/> <br/>
  
---- <b> Helper - how to work with .sqlite DB: <b/> <br/>
-> <i> sqlite_notes.txt <i>
