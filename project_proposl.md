Abstract
GitHub: https://github.com/hcheng10/PIC16B_Project

Analyze whether a specific flight in the future will arrive on time or late, and estimate the overall probability through existing flight data(airport data, airline data…etc.).
To solve this problem, firstly we need to notice that the data we got most are fully known data. That is the data we have are already known whether the flights is on time or not. In that case, we can apply supervised learning in machine learning to trying to solve that problem.
Planned Deliverables
Our Full success is to provide information about flights to help people travel through our own page on github, because Flight delay/cancellation is time consuming and frustrating. If possible, help people based on user input information such as departure location, landing location, and departure time Predict the likelihood of flights or cancellations.
Partial success is to tell users What are the main reasons for flight delays, but it is impossible for users to input data and make predictions based on the input..
We will use pandas, numpy, sqlite3, matplotlib.pyplot, plotly, sklearn, Seaborn, Statsmodels, and Scipy.
Resources Required
All data comes from the U.S. Department of Transportation and other free websites, so no additional accounts are required. Because our dataset will not be very large, only a few thousand rows, so ordinary home computers can complete the relevant calculations.
https://flightaware.com/live/airport/KSEA
https://www.flightstats.com/v2/flight-tracker/AS/500?year=2022&month=4&date=20&flightId=1089542245&utm_source=49e3481552e7c4c9:6fbd1b7f:126ad2b709d:-3ce3&utm_medium=cpc&utm_campaign=weblet
https://aviationweather.gov/
Tools and Skills Required
First of all, we need to get the raw data, so we need to use web scripting to grab the flight information we need from the website, such as flight departure time, departure location, and local weather conditions. After obtaining the information, it is necessary to perform basic cleaning on the data, because it is possible that the weather conditions of the day may not be obtained, resulting in NA. In this case, it is necessary to remove the corresponding observation or use other methods for missing values. The forecast is then filled in the table. In addition, because the flight information contains categorical data such as airline name, or weather, we need encoding to interpret categorical data into numerical data to input into our model. For weather, we will use Label encoding because for different weather, so The degree of correspondence is also different. And for the airline name, I'll use One-Hot Encoding, because the variable itself doesn't represent any frequency. In this project, we predict that the probability of aircraft delay is very small, so we cannot remove outliers from the data. Second, we also need to observe the correlation between each variable and the response, and choose a better predictor. Then, we need to build the logistic model and train the model. Finally, model validation needs to be done, for example, cross validation, and qq plot to ensure the validity of the model with no underfit or overfit.
 
What You Will Learn
Haowei Cheng: I will learn more tools to make statistical models and do statistical analysis. Also, a basic knowledge of doing website editing and data downloading by using scrapy.
Haodong Feng: The first thing that came to my mind was the use of GitHub. GitHub was critical to this project, and through GitHub my team and I were able to better collaborate on every little detail of this project. At the same time, webApp interaction will also be a very important part if we decide to build a website to display our research results. So we may also be interested in html and css languages.
Kai Kang: Secondly,  Machine learning will also be a very important part of the project. As a branch of artificial intelligence technology, machine learning has penetrated into all walks of life around us in just a few years. For example, a very important variable in our model is the weather conditions at the departure and arrival points of the flight. In the face of more complex weather conditions, we need to use the data prediction function of machine learning algorithms. Various algorithm models of machine learning can be applied in our research according to their own characteristics.
Risks
Time risk could prevent us from achieving all of our tasks for this project. We only have a few weeks left to work on this project and all team members have two or three other classes which mean completing all the tasks in our project may take longer than we expected. Since we're 'new workers' doing this kind of job, it's easy to underestimate the time it'll take team members to complete a project during the initial planning phase.
When we are working on the project, we may meet some difficulties that are hard or not possible to solve, which may be caused by the initial project objectives not being well-defined. For example, we thought we could complete a task but we realized it's not possible when working on it.
We may not have enough skills and knowledge to achieve all the tasks, so when we meet some difficulties, we need to spend more time learning new skills and causing time delays for the projects. 
Ethics
Passengers who travel by air will be the beneficiaries of our project, and we haven't found anyone to be harmed by our project. Our products will make people's travel more convenient. Whether the plane should not be delayed or canceled can be predicted by weather conditions, departure time and location. And we assume the local weather forecast is accurate.
Tentative Timeline
We will attend the presentation on May 5 Thursday and complete the data collection, cleaning and building of the most basic ML methods. 
On May 24 Tuesday, we will basically complete the establishment of ML, conduct data analysis and get some practical suggestions.
