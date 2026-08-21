Instructions on running the model.

1. In command prompt, navigate to the "python" folder within the Residential System Benchmark Model" folder
	a. If you are already inside of the Residential System Benchmark Model" folder, type and enter
		>cd python
	b. If you are not already inside "Residential System Benchmark Model" folder, type and enter the full path of the python folder
		ex. >cd "Documents\Solar\Models\Residential System Benchmark Model\python"

2. Update the BLS labor database
	a. Back in command prompt, navigate to the python folder.
	b. Type and enter
		>python update_labor_database.py
	c. Update labor database should appear in the "input_data" folder under "BLS Labor Database.xlsx"

3. Edit the input data 
	a. Go to the "Residential System Benchmark Model" folder in your file explorer
	b. Click the "input_data" folder
	c. Here exists the spreadsheets that feed data into the model. You can click them and edit the data in them as you see fit.

4. Running the model
	a. In command prompt, type and enter
		>python main.py
	b. It will take approximately 3 minute to run

5. View the results in excel
	a. Go to the "Residential System Benchmark Model" folder in your file explorer
	b. click the "results" folder
	c. Two spreadsheets of results will exist there, one for the national runs and one for the state runs



