The Residential Solar PV Adoption Model:
===================
#####by Patrick Bean, Rolando Fuentes, Steven O. Kimbrough, and Mohammed Muaafa
Residential solar installations are becoming an economically attractive alternative to local utility service in some areas of the world due to declining photovoltaic (PV) prices, financial incentives and innovative financing mechanisms. Over 250,000 customers in California added solar PV systems to their homes since 2011, and over 1 percent of the state’s residential customers have PV. In Hawaii, market penetration of residential PV is approaching 6 percent. 
Electricity sales from incumbent utilities are experiencing downward pressure as more customers decide to produce their own electricity with PV. This is a concern for utilities because it threatens their ability to recover their fixed costs, which are recovered through volumetric rates. Some observers view this feedback as a potential “death spiral” in which utilities must continually raise prices to recover costs, which then further perpetuates adoption of PV and erosion of the utility’s revenue.
To begin investigating this phenomenon and its potential implications, KAPSARC developed the Residential Solar PV Adoption Model. The purpose of the model is to describe the adoption over time of residential PV under realistic assumptions regarding consumer behavior. In particular, the model takes into account electricity prices, levelized costs of PV, contagion effects of PV adoption, and the type of residence and whether it is suitable for PV. 
###WHAT IS IT? 
####Context 
Electric power prices charged by utilities reflect the marginal cost of producing the electricity provided, profit, and a charge to recover the fixed costs of transmission and distribution. Residential customers installing solar PV (or indeed any other demand reduction measure) reduce their payments to the associated utility. A portion of the foregone payments, however, is allocated to recovering the fixed costs (and associated profits) of the transmission and distribution system. To the extent that these revenues to the utility are reduced, it must increase its prices in order to recover costs and keep profits fixed. Increased prices, however, serve to encourage more adoption of residential solar PV. 
####Purpose 
The purpose of the Residential Solar PV Adoption model is to describe the adoption over time of residential solar PV under realistic assumptions regarding consumer behavior. In particular, the model takes into account type of residence, size of PV installation, and contagion effects of existing installations. It is assumed that customers adopt probabilistically, depending upon these various conditions. 
####Basic Story 
Time proceeds discretely. At the start of each episode a price schedule for electric power is announced. Also, a price schedule for solar PV is announced. Eligible (to install PV) customers are those who have appropriate residences and who do not already have solar PV installed. During the episode eligible customers adopt solar PV with a probability depending upon the cost of electric power from the utility, the cost of solar power, and the prevalence of solar adopters in the neighborhood. Depending upon the number of adoptions, and possibly external factors, the utility updates its price schedule for electric power, effective at the start of the next period. 
###HOW TO USE IT 
#####See the Interface note: 
 
##### 1-Set the sliders above to the values you desire. Then click the SETUP button.
To begin, click the SETUP button to set up the turtles. There are three kinds of turtles, highs (colored red and representing large residences), lows (colored blue and representing small residences), and nones (colored yellow and representing residences not eligible to install solar PV). Set the percentages desired with the sliders %-highs and %-lows. 

When you click the SETUP button, the program creates number-of-residences (see slider) turtles with kinds highs, lows, and nones in the proportions %-highs, %-lows indicated by the sliders. The turtles are scattered randomly on distinct patches. And then the program clusters the residences weakly by type, using a variant of the Segratation.nlogo algorithm. Setting %-similar-wanted to 0 results in simply random placement of the residences, without regard to type. 

Next, consider the optional step: 
(1a-optional) Set values in the sliders below, then click the DISPLAY-LOGISTIC button to see a plot of the probability function for solar adoption, as well as a tabular display of data in the output box to the left.
> **In any event** , you need to set or at least consider the sliders and input boxes immediately below. They are: 
>- current-price. This is the residential electricity price from the utility, in cents per kilowatt hour. 
- solar-PV-cost. This is the leveled cost of solar PV, in cents per kilowatt hour. 
- neighborhood-effect. This is a premium subtracted from the solar-PV-cost, meant to represent a behavior that in effect reduces the “mental” perceived cost of solar. It might, for example, represent a reduction in the perceived risk of installing solar. It is measured in cents per kilowatt hour. 
- k. This is a scaling parameter in the logistic function, which the model uses to determine the probability, in a given period, of adoption of solar PV. See the “Mirrored Logistic Function” section below for elaboration. 
- L-scale. This is a scaling parameter for the logistic function, which the model uses to determine the probability, in a given period, of adoption of solar PV. See the “Mirrored Logistic Function” section below for elaboration. 
- Prob_big_solar_given_high. This is the probability, for a large (high) customer that is committed to installing solar PV this period, that the customer chooses a big (4 kW) installation, instead of a small (2 kW) installation. 
- Prob_big_solar_given_low. This is the probability, for a small (low) customer that is committed to installing solar PV this period, that the customer chooses a big (4 kW) installation, instead of a small (2 kW) installation. 

Whether or not you choose to execute the optional step, at (1a-optional), set the above sliders and input boxes, then view the note at the bottom, left of center: 
##### 2-Set the count-years-simulated slider (to the left), then click the GO YEARS SIMULATED button to run the model for count-years-simulated. Each tick corresponds to 1 year.
##### 3-Click the GO YEARS SIMULATED button to start the simulation. 
###THINGS TO NOTICE 
When you execute SETUP, the residences are distributed in a random yet clustered fashion, with like preferring like, driven by the value of %-similar-wanted. 
###THINGS TO TRY 
Try different values for %-SIMILAR-WANTED. How does the overall degree of segregation change? 
Measures of performance (MoPs) for the model are embodied in the several reporters on the user Interface. Use BehaviorSpace with these reporters to measure the runs, and
systematically vary the several model variables. 
###EXTENDING THE MODEL 
Perhaps rename highs and lows to big and small. Consider using different logistic functions (parameterized) for the two types of houses, big and small. Add, a decision about sizing the solar panel, once the decision is made to adopt it. This is a step now missing. 
House Type | P(large solar / going solar) | P(small solar / going solar)
-------- | -------- | --------
Big|Small | None 

###THE MIRRORED LOGISTIC FUNCTION 
We need a function whose range is a probability, 0 to 1, and whose domain is a continuous variable, x, such that as x increases the function’s value decreases. 
A natural function here is the mirrored logistic function. That is, 1 - logistic(x). The regular logistic has a general “S”. The mirrored an inverted “S”. This makes good sense for the probability in a given period that an agent will convert to solar if it hasn’t already. 
The general form of the logistic is 
$$
 y = f(x) = L / (1 + e^(-k*x))
 $$
where L is a scaling constant, and
k is a free parameter that affects the slope of the curve. 
Notice that at $$x = 0, f(x) = 0.5 * L. $$
And we want g(x), 
$$ g(x) = 1 - f(x).$$
We need to introduce more parameters here, as follows: 
$$ x = cs - pu - ne$$
With the following interpretations: 
*cs* = cost of solar PV power in cents per kWH, solar-PV-cost in the code and Interface slider. 
*pu* = price of utility power in cents per kWH, current-price in the code and Interface slider. 
Finally, *ne* is the neighborhood effect (a positive number, neighborhood-effect in the code and Interface slider), which serves to reduce the value of x, and hence increase the probability of adoption (as it increases). 
###CREDITS AND REFERENCES 
Chai, D.W.H., Adlakha, S., Low, S.H., De Martini, P., Chandy, K.M. Impact of residential PV adoption on retail electricity rates. (2013). Energy Policy 62, pp. 830-843. 
###HOW TO CITE 
If you mention this model in a publication, we ask that you include these citations for the model itself and for the NetLogo software: 

Bean, Patrick, Fuentes, Rolando, Kimbrough, Steven O., and Muaafa, Mohammed, Residential Solar PV Adoption model, version 1.0, KAPSARC (2015) File: Residential Solar PV Adoption Model.nlogo 


> **Note:** to run the model, simply click on the Nelogo file "Residential Solar PV Adoption.nlogo". It should download the file in your pc. Then, open the Netlogo software. From there you can go to file-open and choose the file you just downloaded. At the interface and info tabs you should find detailed information on how to run the model.

-----
Copyright © [KAPSARC](https://www.kapsarc.org/). Open source [MIT License](http://opensource.org/licenses/MIT).
