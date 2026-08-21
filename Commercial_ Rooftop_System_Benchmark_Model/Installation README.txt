Instructions on installing the model.

INSTALLATION
1. Install Python 3.7
	a. Install Anaconda Navigator	
		Windows: https://www.anaconda.com/distribution/#windows
		Mac: https://www.anaconda.com/distribution/#macos
	b. Choose the default settings during installation
	
2. Download the "Commercial System Benchmark Model" folder from Box.
	a. Download the Mac or Windows version
		Windows: https://nrel.app.box.com/folder/70559076745
		Mac: https://nrel.app.box.com/folder/70559094071
	b. Download the entire folder and save it in your local files wherever you want to access it

3. Open Anaconda Prompt
	a. Click the start menu and search "Anaconda Prompt", the app should appear as a result

4. In Anaconda Prompt, navigate to the "Commercial System Benchmark Model" folder wherever you saved it
	a. type "cd" and then a space, and then the path of where your model is saved
		ex. >cd "Documents\Solar\Models\Commercial System Benchmark Model"
	b. Hit Enter
	c. You are now in the correct directory

5. Install the "virtual environment" file
	a. This will install all the required modules that the model needs to run.
	b. In command prompt type and enter:
		>conda env creat -f solar_python_model.yml
6. Activate the virtual environment
	a. In command prompt type and enter:
		>conda activate solar_python_model

7. You are now ready to run the model