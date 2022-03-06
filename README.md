In this repository you will find:

---- <b> Input files: </b> <br/>
-> <i> przypadki_pomocy_1.csv </i> - page 1<br/>
-> <i> przypadki_pomocy_2.csv </i> - page 2<br/> <br/>
---- <b> Python script (<i>csv_json_sqlite_flow.py</i>) that: </b> <br/>
-> reads (many) .csv files to a DataFrame, <br/>
-> cleans data (preprocessing), <br/>
-> creates .json file from DataFrame (<i>output file: uokik_2022-03-06_pages_1_2.json</i>), <br/>
-> based on .json file creates .sqlite DB (<i>output file: beneficiaries.sqlite</i>) where data is inserted, <br/>
-> builds a specific VIEW in DB (the same result saved in <i>output file: total_support_nominal_value_pln.xlsx</i>). <br/> <br/>
---- <b> Helper - how to work with .sqlite DB: </b> <br/>
-> <i> sqlite_notes.txt </i><br/><br/><br/>
---- <b> To do: </b> <br/>
-> Create a folder on your local drive.
-> Clone a repository https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository or simply download input files and Python script.
-> Open <i>csv_json_sqlite_flow.py</i> using PyCharm or some other interpreter.
-> Adjust the path in line 111 (csv_path -> use your path!).
-> Execute the code.
-> To play around with sqlite DB take a look at <i> sqlite_notes.txt </i>.

