It might have happened so many times that you or someone yours need doctors help immediately, but they are not available due to some reason. The Health Prediction system is an end user support and online consultation project. Here we propose a system that allows users to get instant guidance on their health issues through an intelligent health care system online. The system is fed with various symptoms and the disease/illness associated with those systems. The system allows user to share their symptoms and issues. It then processes user’s symptoms to check for various illnesses that could be associated with it. Here we use some intelligent data mining techniques to guess the most accurate illness that could be associated with patient’s symptoms.
![image](https://user-images.githubusercontent.com/86718046/174499458-7b0e3914-abd8-4537-8b57-a9195c262c38.png)
Model Testing
First, we started with collecting input as a symptom given by the user. Then for verification of the input, we matched it with different list of symptom present in the database and returned “invalid input” if the user entered wrong. Then we carried out the work by giving list of disease matched against the symptom.  Then again, we check if there is any more symptoms or not. Then we predict the disease using set of unions of symptoms.

We searched for various renowned doctors across the cities in various different websites spread across the internet. Moreover, we collected the information about the doctors (like – name, specialization) and stored it in our database. We have also gathered the symptoms and diseases dataset after researching many different sites like ‘kaggle.com’ and more and stored it in the database after data preprocessing.
ALGORITHM:
Start:
Step 1: Request the user for a symptom as input.
Step 2: Check the input symptom against list of symptoms in database for validity.
Step 3: If input symptom is not a valid symptom, prompt the user with “Invalid symptom” and go to step 1.
Step 4: Use the finalized input symptom from step 3 to find possible diseases.
Step 5: If possible, disease is only one then present the user with that disease and corresponding doctor.
Step 6: Else Take union of sets of symptoms of each disease found in step 4.
Step 7: If set generated in step 6 is empty then present the user with multiple possible disease list generated in step 4 and corresponding doctor(s). 
Step 8: Else Ask the user to select one more symptom from the set of symptoms generated in step 6.
Step 9: Go to step 4 with symptom selected by user in step 8 as input symptom.
NOTE: Maximum times Loop from step 4 to 9 must not execute more than 9 times.
