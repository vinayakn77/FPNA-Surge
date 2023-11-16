1. Download the code folders/files from https://github.com/manishjayswal/FPA_final
2. Open the code in VS code

3. To Run the Backend in localhost:
   3.1. Open Bash Terminal(note: this is different than powershell terminal, you can choose it from dropdown there)
   3.2. Change the directory to FPA_final/backend
   3.3. To create virtual environment, run this command in Bash terminal: py -m venv .venv
   3.4. To activate the virtual environment, run this command in Bash terminal: source .venv/Scripts/activate
   3.5. Once the virtual environment is activate, you can see "(.venv)" just on the left of the terminal in current line
   3.6. To install all the required libraries, run: pip install -r requirements.txt
   3.7. Now your Backend is ready, you can start the flask app by the command: flask run
   3.8. To browser your backend: http://localhost:5000/calcm
 
4. To run the Frontend in localhost:
   4.1. Open the powershell terminal
   4.2. Change the directory to FPA_final
   4.3. To install node module, run the command: npm install
   4.4. To run frontend server, run the command: npm start
   4.5. Now your frontend is ready, you can browse frontend at: http://localhost:3000/

5. In case you want to stop the backend or frontend server: press "Ctrl + c" in the respective terminal

6. To Deploy Backend on web(Azure):
   6.1. Download the code from https://github.com/manishjayswal/FPA_final
   6.2. Follow the steps similart to the one in this blog: https://shorturl.at/cryY1
   6.3. while clonning the code repository use this https://github.com/manishjayswal/FPA_final.git
   6.4. After successful deployment you will get one link. Now add /calcm to end of that link and browse, you will get summary output from backend.

7. To Deploy Frontend on web(Vercel):
   7.1. If not already downloaded, Download the code from https://github.com/manishjayswal/FPA_final 
   7.2. Replace all the "https://fpasimulate.azurewebsites.net" with the link of your backend( in the files: package.json, Desktop1.js, Desktop6.js)
   7.3. Create an account on vercel using your github account.
   7.4. Upload the code on your github account and provide this code repository to vercel.
   7.5. Then vercel will provide you one link which you can use to browse the app.
