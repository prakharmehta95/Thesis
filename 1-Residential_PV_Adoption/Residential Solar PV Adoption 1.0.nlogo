globals [
  percent-similar  ;; on the average, what percent of a turtle's neighbors
                   ;; are the same color as that turtle?
  percent-unhappy  ;; what percent of the turtles are unhappy?
  
  current-cost ;; of solar, discounted in cents/kWH
  
  new-installations ;; the count of new installations occurring during a tick
  neighborhood-size ;; the radius that a residence examines for solar among its neighbors
  new-high-installations new-low-installations ;; See beginning of go for explanation.
  solar-low solar-high  ;; Simply end points for plotting and reporting.
]

turtles-own [
  happy?       ;; for each turtle, indicates whether at least %-similar-wanted percent of
               ;; that turtles' neighbors are the same color as the turtle
  similar-nearby   ;; how many neighboring patches have a turtle with my color?
  other-nearby ;; how many have a turtle of another color?
  total-nearby  ;; sum of previous two variables
  
  has-solar?
  getting-solar?
  solar-size
]

breed [highs high-guy]
breed [lows low-guy]
breed [nones none-guy]

to setup
  clear-all
  set solar-low -5
  set solar-high 50
  if number-of-residences > count patches
    [ user-message (word "This pond only has room for " count patches " turtles.")
      stop ]
  ;; create turtles on random patches.
  ask n-of number-of-residences patches
    [ let my-type random-float 1
      ;; Here we are assuming three breeds of turtle residences.
      if my-type <= %-highs
      [sprout-highs 1
      [ set color red ] ]
      if my-type > %-highs and my-type <= %-highs + %-lows
      [sprout-lows 1
        [set color blue]]
      if my-type > %-highs + %-lows
      [sprout-nones 1 
        [set color yellow]]
    ]

  ask turtles [set shape "dot"
    set has-solar? false
    set getting-solar? false]
  ask patches [set pcolor 7]
  update-variables
  go-setup
  display-logistic 
  set current-cost solar-PV-cost 
  set neighborhood-size 3 ;; Note this is hard wired. Later,
  ;; consider adding a widget to explore different values.
  reset-ticks
end

to go-setup
  let mycount 0
  while [not all? turtles [happy?] and mycount < 1000]
  [set mycount (mycount + 1)
    move-unhappy-turtles
  update-variables]
end

to move-unhappy-turtles
  ask turtles with [ not happy? ]
    [ find-new-spot ]
end

to find-new-spot
  rt random-float 360
  fd random-float 10
  if any? other turtles-here
    [ find-new-spot ]          ;; keep going until we find an unoccupied patch
  move-to patch-here  ;; move to center of patch
end

to update-variables
  update-turtles
  update-globals
end

to update-turtles
  ask turtles [
    ;; in next two lines, we use "neighbors" to test the eight patches
    ;; surrounding the current patch
    set similar-nearby count (turtles-on neighbors)
      with [color = [color] of myself]
    set other-nearby count (turtles-on neighbors)
      with [color != [color] of myself]
    set total-nearby similar-nearby + other-nearby
    set happy? similar-nearby >= ( %-similar-wanted * total-nearby / 100 )
  ]
end

to update-globals
  let similar-neighbors sum [similar-nearby] of turtles
  let total-neighbors sum [total-nearby] of turtles
  set percent-similar (similar-neighbors / total-neighbors) * 100
  set percent-unhappy (count turtles with [not happy?]) / (count turtles) * 100
end

to go
  set new-high-installations 0 ;; This will be our counter for the tick, to 
  ;; record the number of new installations to the high (large) houses.
  set new-low-installations 0  ;; This will be our counter for the tick, to 
  ;; record the number of new installations to the low (small) houses.
  set new-installations 0 ;; This will be our counter for the total number of
  ;; new installations during the tick/period.
  
  ;; Process first the highs, that is, the larger residences.
  ask highs [
    ;; Does the residence already have solar? If so, then just skip 
    ;; what follows and go on to the next one.
    if not has-solar?
    [ ;; OK, this residence does not have solar installed at this time.
      ;; Now, we will determine whether it will adopt solar during this period.
      ;; First, we need to determine if a neighborhood effect will happen.
      ;; From the Interface tab, neighborhood-effect is a positive floating
      ;; number, representing a cents per kWH effective cost reduction for solar
      ;; to the potential adopter. That is, we do this to model a positive effect
      ;; from having neighbors with solar already.
      ;; So, the value we want to use is either 0 if no one has solar or
      ;; neighborhood-effect if at least one residence nearby has solar.
      ;; Just to be a little clearer, the agent's probability of adopting solar
      ;; is a function of the solar cost - the utility price - the neighborhood effect.
      ;; Here, we either have 0 neighborhood effect, or the value neighborhood-effect (from the 
      ;; Interface slider) depending upon whether there is at least one neighbor within 3 patches who
      ;; already has solar.
      let ne 0
      if count turtles in-radius neighborhood-size with [has-solar? = true] > 0
      [set ne neighborhood-effect]
      ;; Now determine whether this guy will in fact adopt solar this period.
      ;; Use the logistic (simple-mirrored-logistic) function/reporter to
      ;; determine its probability, draw the random number and if (and only if)
      ;; it is < the probabilty, install solar.
      ;; See below for the the-score reporter, but basically it calcuates
      ;; x = solar PV cost - current price from the utility - the neighborhood effect.
      ;; Then simple-mirrored-logistic, calculates the probability of adoption, given x and
      ;; k, the scaling parameter, and then L-scale compresses it overall.
      ;; We promise: more information in the Info tab.
      if random-float 1 < 
        (simple-mirrored-logistic(the-score(solar-PV-cost)(current-price)(ne))(k) * L-scale)
      ;; So if indeed the guy installs PV this period, set its flag to say "I'm going to get solar"
      ;; (that is, getting-solar?) to true. Increment the number new high installations by 1.
      ;; And finally, call the get-solar-size reporter to determine what size solar the residence
      ;; is getting, and set its solar-size attribute to that value.
      [set getting-solar? true
       set new-high-installations (new-high-installations + 1)
       set solar-size get-solar-size(Prob_big_solar_given_high)
       ]
    ]
  ] ;; end of ask highs [
  ;; OK, that completes the initial processing of the larger residences.

  ;; Now we repeat the same process for the smaller residences, the lows. 
  ask lows [
    if not has-solar?
    [ let ne 0
      if count turtles in-radius neighborhood-size with [has-solar? = true] > 0
      [set ne neighborhood-effect
        ]
      if random-float 1 < 
      (simple-mirrored-logistic(the-score(solar-PV-cost)(current-price)(ne))(k) * L-scale)
      [set getting-solar? true
       set new-low-installations (new-low-installations + 1)
       set solar-size get-solar-size(Prob_big_solar_given_low)
       ]
    ]
  ]

  ;; Finally, we process all of the turtles, highs or lows, who
  ;; have adopted solar PV this period (if any).
  ask turtles with [getting-solar? = true] [
    set new-installations (new-installations + 1)
    set has-solar? true
    set shape "sun"
    set size 1.1
    set getting-solar? false]
  ;; Last of all, advance the tick counter, so we'll start a new period.
  tick
end

to-report get-solar-size [the-prob]
  let sol-sz 0
  ifelse random-float 1 <= the-prob
    [set sol-sz 4]
    [set sol-sz 2]
  report sol-sz
end


;;;;;;;; Below, from sok's Reporter Library NetLogo model.  ;;;;;;;;;;;;;;

to plotvectors [x y]
;  Assumes a plot has been selected and
;  made the current plot and been cleared.
  let dalength length x
  let dacount 1
  while [dacount < dalength]
  [plotxy item dacount x item dacount y
    set dacount (dacount + 1)]
end

to-report linspace [dastart dastop  numpoints]
  ;; Modeled after MATLAB's linspace.
  ;; Returns a list numpoints long consisting
  ;; of evenly spaced floating point numbers,
  ;; the first of which is start and the last
  ;; of which is stop. 
  ;; Note that this reporter does no error checking.
  ;; However, it works properly with negative numbers 
  ;; and going from both high to low and low to high.
  let toreport (list dastart)
  let increment ((dastop - dastart)) / (numpoints - 1)
  repeat numpoints - 1 
  [set toreport lput ((last toreport) + increment) toreport]
  report toreport
end

to-report simple-mirrored-logistic [x the-k]
  ;; Given the inputs, returns a probability value.
  ;; Fixing base and temperature, varying score yields
  ;; an "s"-shaped (sigmoid) curve, increasing in score.
  ;; See logistic curve.
  ;; See SOK's book Agents, Games, and Evolution, appendix B.4
  ;; for explanation. See also:
  ;; http://mathworld.wolfram.com/LogisticEquation.html
  ;; Most directly, the logistic function:
  ;; http://en.wikipedia.org/wiki/Logistic_function
  ;; f(x) = 1 / (1 + e^(-k*x))
  ;; where L is a proportionality constant. k is a constant
  ;; and x0 is a constant at which f(x) = 0.5 * L.
  report 1 - (1 / (1 + e ^ ( -1 * the-k * x)))
  ;; Notice we have 1 minus the normal function's value, because
  ;; as the cost of solar decreases, the probability of installation
  ;; increases.
end

to-report the-score [the-solarPVcost the-utilityPrice the-neighborhood-effect]
  report the-solarPVcost - the-utilityPrice - the-neighborhood-effect
end

to display-logistic
;;  The general form of the logistic is
;;  y = f(x) = L / (1 + e^(-k*x))
;;  where L is a scaling constant, which we set to 1 so we get a probability, 
;;  and k is a free parameter that affects the slope of the curve.
;;  Notice that at x = 0, f(x) = 0.5 (assuming as we shall that L = 1).
;;  And we want g(x),
;;  g(x) = 1 - f(x).
;;  We need to introduce more parameters here, as follows:
;;  x = cs - pu - ne
;;  With the following interpretations:
;;  cs = cost of solar PV power in cents per kWH
;;  pu = price of utility power in cents per kWH
;;  Finally, ne is the neighborhood effect (a positive number), 
;;  which serves to reduce the value of x, and hence increase the probability 
;;  of adoption (as it increases).

  ;; So now we initialize the variables.
  ;; current-price  taken from the Interface slider corresponds to pu, price from the utility
  ;; neighborhood-effect corresponds to  ne and is taken from the Interface slider.
  
  set-current-plot "Probability of Adoption Function"
  clear-plot
  plot-simple-mirrored-logistic(L-scale)
  clear-output
  let solar-costs linspace(solar-low)(solar-high)(51)
  output-print (word "solar cost" "   " "net score (x)" "      " "p(x)")
  output-print (word "--------------------------------------")
  foreach solar-costs [
    let x the-score(?)(current-price)(0) ;; neighborhood-effect
  output-print (word precision ? 2 "\t\t" precision x 2 "\t\t" precision (simple-mirrored-logistic(x)(k) * L-scale) 3)]
end

to plot-simple-mirrored-logistic [da-scale]
  let the-solar-costs linspace(solar-low)(solar-high)(51)
  let davalues []
  let a-score 0
  foreach the-solar-costs [
    set a-score the-score(?)(current-price)(0) ;; neighborhood-effect
    set davalues lput (simple-mirrored-logistic(a-score)(k) * 10 * da-scale) davalues]
  plotvectors(the-solar-costs)(davalues)
end

to scaled-display-logistic
;;  The general form of the logistic is
;;  y = f(x) = L / (1 + e^(-k*x))
;;  where L is a scaling constant, which we set to 1 so we get a probability, 
;;  and k is a free parameter that affects the slope of the curve.
;;  Notice that at x = 0, f(x) = 0.5 (assuming as we shall that L = 1).
;;  And we want g(x),
;;  g(x) = 1 - f(x).
;;  We need to introduce more parameters here, as follows:
;;  x = cs - pu  - ne
;;  With the following interpretations:
;;  cs = cost of solar PV power in cents per kWH
;;  pu = price of utility power in cents per kWH
;;  Finally, ne is the neighborhood effect (a positive number), 
;;  which serves to reduce the value of x, and hence increase the probability 
;;  of adoption (as it increases).

  ;; So now we initialize the variables.
  ;; current-price  taken from the Interface slider corresponds to pu, price from the utility
  ;; neighborhood-effect corresponds to  ne and is taken from the Interface slider.
  
  ;;plot-mirrored-logistic(-50)(50)(0)(temperature)(k-scale)
  set-current-plot "L-Scaled Probability of Adoption Function"
  clear-plot
  plot-simple-mirrored-logistic(L-scale)
  clear-output
  let solar-costs linspace(solar-low)(solar-high)(51)
  ;print percentages
  output-print (word "solar cost" "   " "net score (x)" "      " "p(x)")
  output-print (word "--------------------------------------")
  foreach solar-costs [
    let x the-score(?)(current-price)(0)  ;; neighborhood-effect
  output-print (word precision ? 2 "\t\t" precision x 2 "\t\t" precision (simple-mirrored-logistic(x)(k) * L-scale) 3)]
end
@#$#@#$#@
GRAPHICS-WINDOW
341
10
861
551
25
25
10.0
1
10
1
1
1
0
0
0
1
-25
25
-25
25
1
1
1
ticks
30.0

MONITOR
242
281
317
326
% similar
percent-similar
1
1
11

SLIDER
15
10
227
43
number-of-residences
number-of-residences
500
2500
2100
10
1
NIL
HORIZONTAL

SLIDER
15
48
227
81
%-similar-wanted
%-similar-wanted
0
100
7
1
1
%
HORIZONTAL

BUTTON
13
244
93
277
setup
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
14
106
186
139
%-highs
%-highs
0
1.0
0.47
0.01
1
NIL
HORIZONTAL

SLIDER
14
165
186
198
%-lows
%-lows
0
1 - %-highs
0.2
0.01
1
NIL
HORIZONTAL

MONITOR
243
120
309
165
%-nones
1 - %-highs - %-lows
2
1
11

OUTPUT
862
237
1175
575
10

SLIDER
1142
407
1350
440
current-price
current-price
0
50
20
0.1
1
cents/kWH
HORIZONTAL

TEXTBOX
15
86
165
104
Highs are red.
11
0.0
1

TEXTBOX
15
144
165
162
Lows are blue.
11
0.0
1

TEXTBOX
242
100
337
118
Nones are yellow.
11
0.0
1

BUTTON
189
644
322
677
Go Years Simulated
repeat count-years-simulated [go]
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
335
552
473
597
Percent highs with solar
100 * count highs with [has-solar? = true] / count highs
2
1
11

MONITOR
475
552
605
597
Percent lows with solar
100 * count lows with [has-solar? = true] / count lows
2
1
11

PLOT
8
332
336
482
Total Solar PV Installations
Year
NIL
0.0
20.0
0.0
10.0
true
false
"" ""
PENS
"pen1" 1.0 0 -16777216 true "" "plot count turtles with [has-solar? = true]"

MONITOR
607
551
728
596
Total PV Installations
count turtles with [has-solar? = true]
2
1
11

SLIDER
11
644
178
677
count-years-simulated
count-years-simulated
1
100
20
1
1
NIL
HORIZONTAL

PLOT
8
486
335
636
New Installations
Year
NIL
0.0
20.0
0.0
10.0
true
true
"" ""
PENS
"Total" 1.0 0 -16777216 true "" "plot new-installations"
"Highs" 1.0 0 -2674135 true "" "plot new-high-installations"
"Lows" 1.0 0 -13345367 true "" "plot new-low-installations"

MONITOR
729
551
866
596
Fraction PV Installations
count turtles with [has-solar? = true] / count turtles
2
1
11

SLIDER
1140
440
1350
473
solar-PV-cost
solar-PV-cost
0
50
16
0.1
1
cents/kWH
HORIZONTAL

SLIDER
1136
472
1350
505
neighborhood-effect
neighborhood-effect
0
20
0
0.1
1
cents/kWH
HORIZONTAL

SLIDER
1178
504
1350
537
k
k
0
0.3
0.1
0.001
1
NIL
HORIZONTAL

PLOT
862
10
1347
237
Probability of Adoption Function
Cost of Solar PV (cents/kWH) (w/o neighborhood-effect)
Prob. of Adoption per tick
0.0
10.0
0.0
0.1
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" ""

BUTTON
1178
240
1279
273
NIL
display-logistic
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
238
182
325
227
NIL
count highs
17
1
11

MONITOR
239
231
326
276
NIL
count lows
17
1
11

SLIDER
1178
537
1350
570
L-scale
L-scale
0
0.2
0.02
0.005
1
NIL
HORIZONTAL

MONITOR
336
598
510
643
NIL
sum [solar-size] of turtles
17
1
11

TEXTBOX
101
244
223
301
(1) Set the sliders above to the values you desire. Then click the SETUP button.
11
0.0
1

TEXTBOX
1180
275
1367
387
(1a-optional) Set values in the sliders below, then click the DISPLAY-LOGISTIC button to see a plot of the probability function for solar adoption, as well as a tabular display of data in the output box to the left.
11
0.0
1

TEXTBOX
335
647
669
689
(2) Set the count-years-simulated slider (to the left), then click the GO YEARS SIMULATED button to run the model for count-years-simulated. Each tick corresponds to 1 year.
11
0.0
1

INPUTBOX
866
574
1021
634
Prob_big_solar_given_high
0.5
1
0
Number

INPUTBOX
1020
574
1175
634
Prob_big_solar_given_low
0.1
1
0
Number

@#$#@#$#@
# THE RESIDENTIAL SOLAR PV ADOPTION MODEL, Version 1.0


Patrick Bean, Rolando Fuentes, Steven O. Kimbrough, and Mohammed Muaafa

Residential solar installations are becoming an economically attractive alternative to local utility service in some areas of the world due to declining photovoltaic (PV) prices, financial incentives and innovative financing mechanisms. Over 250,000 customers in California added solar PV systems to their homes since 2011, and over 1 percent of the state’s residential customers have PV.  In Hawaii, market penetration of residential PV is approaching 6 percent.  

Electricity sales from incumbent utilities are experiencing downward pressure as more customers decide to produce their own electricity with PV. This is a concern for utilities because it threatens their ability to recover their fixed costs, which are recovered through volumetric rates. Some observers view this feedback as a potential “death spiral” in which utilities must continually raise prices to recover costs, which then further perpetuates adoption of PV and erosion of the utility’s revenue.
To begin investigating this phenomenon and its potential implications, KAPSARC developed the Residential Solar PV Adoption Model. The purpose of the model is to describe the adoption over time of residential PV under realistic assumptions regarding consumer behavior. In particular, the model takes into account electricity prices, levelized costs of PV, contagion effects of PV adoption, and the type of residence and whether it is suitable for PV.  


## WHAT IS IT?  

### Context

Electric power prices charged by utilities reflect the marginal cost of producing the electricity provided, profit, and a charge to recover the fixed costs of transmission and distribution. Residential customers installing solar PV (or indeed any other demand reduction measure) reduce their payments to the associated utility. A portion of the foregone payments, however, is allocated to recovering the fixed costs (and associated profits) of the transmission and distribution system. To the extent that these revenues to the utility are reduced, it must increase its prices in order to recover costs and keep profits fixed. Increased prices, however, serve to encourage more adoption of residential solar PV.

### Purpose

The purpose of the Residential Solar PV Adoption model is to describe the adoption over time of residential solar PV under realistic assumptions regarding consumer behavior. In particular, the model takes into account type of residence, size of PV installation, and contagion effects of existing installations. It is assumed that customers adopt probabilistically, depending upon these various conditions.

### Basic Story

Time proceeds discretely. At the start of each episode a price schedule for electric power is announced. Also, a price schedule for solar PV is announced. Eligible (to install PV) customers are those who have appropriate residences and who do not already have solar PV installed. During the episode eligible customers adopt solar PV with a probability depending upon the cost of electric power from the utility, the cost of solar power, and the prevalence of solar adopters in the neighborhood. Depending upon the number of adoptions, and possibly external factors, the utility updates its price schedule for electric power, effective at the start of the next period.



## HOW TO USE IT

See the Interface note:

     (1) Set the sliders above to the values you desire. Then click the SETUP button.

To begin, click the SETUP button to set up the turtles. There are three kinds of turtles, highs  (colored red and representing large residences), lows (colored blue and representing small residences), and nones (colored yellow and representing residences not eligible to install solar PV). Set the percentages desired with the sliders %-highs and %-lows. 

When you click the SETUP button, the program creates number-of-residences (see slider) turtles with kinds highs, lows, and nones in the proportions %-highs, %-lows indicated by the sliders. The turtles are scattered randomly on distinct patches. And then the program clusters the residences weakly by type, using a variant of the Segratation.nlogo algorithm. Setting %-similar-wanted to 0 results in simply random placement of the residences, without regard to type. 

Next, consider the optional step:

     (1a-optional) Set values in the sliders below, then click the DISPLAY-LOGISTIC
     button to see a plot of the probability function for solar adoption, as well as a
     tabular display of data in the output box to the left.

In any event, you need to set or at least consider the sliders and input boxes immediately below. They are:

   * `current-price`. This is the residential electricity price from the utility, in cents per kilowatt hour.
   * `solar-PV-cost`. This is the leveled cost of solar PV, in cents per kilowatt hour.
   * `neighborhood-effect`. This is a premium subtracted from the solar-PV-cost, meant to represent a behavior that in effect reduces the "mental" perceived cost of solar. It might, for example, represent a reduction in the perceived risk of installing solar. It is measured in cents per kilowatt hour.
   * `k`. This is a scaling parameter in the logistic function, which the model uses to determine the probability, in a given period, of adoption of solar PV. See the "Mirrored Logistic Function" section below for elaboration.
   * `L-scale`. This is a scaling parameter for the logistic function, which the model uses to determine the probability, in a given period, of adoption of solar PV. See the "Mirrored Logistic Function" section below for elaboration.
   * `Prob_big_solar_given_high`. This is the probability, for a large (high) customer that is committed to installing solar PV this period, that the customer chooses a big (4 kW) installation, instead of a small (2 kW) installation.
   * `Prob_big_solar_given_low`. This is the probability, for a small (low) customer that is committed to installing solar PV this period, that the customer chooses a big (4 kW) installation, instead of a small (2 kW) installation.

Whether or not you choose to execute the optional step, at (1a-optional), set the above sliders and input boxes, then view the note at the bottom, left of center:

    (2) Set the count-years-simulated slider (to the left), then click the GO YEARS 
    SIMULATED button to run the model for count-years-simulated. Each tick corresponds
    to 1 year.

  Click the GO YEARS SIMULATED button to start the simulation. 

## THINGS TO NOTICE

When you execute SETUP, the residences are distributed in a random yet clustered fashion, with like preferring like, driven by the value of `%-similar-wanted`.

## THINGS TO TRY

Try different values for %-SIMILAR-WANTED. How does the overall degree of segregation change?

Measures of performance (MoPs) for the model are embodied in the several reporters on the user Interface. Use BehaviorSpace with these reporters to measure the runs, and
systematically vary the several model variables.

## EXTENDING THE MODEL

Perhaps rename highs and lows to big and small. Consider using different logistic functions (parameterized) for the two types of houses, big and small. Add, a decision about sizing the solar panel, once the decision is made to adopt it. This is a step now missing.

House Type     P(large solar | going solar) P(small solar | going solar)
==========     ============================ ============================
Big
Small
None

Rolando: Can we have an initial layout that is a realistic geography, with richer and poorer neighborhood? Steve: Yes, absolutely. In the future. We first need to tell a
basic story on how this work, then it can be coded.

Add the capability of using an empirical distribution of PV sizes. Do this to constitute version 1.1.

## THE MIRRORED LOGISTIC FUNCTION

We need a function whose range is a probability, 0 to 1, and whose domain is a continuous variable, x, such that as x increases the function's value decreases.

A natural function here is the mirrored logistic function. That is, 1 - logistic(x). The regular logistic has a general "S". The mirrored an inverted "S". This makes good sense for the probability in a given period that an agent will convert to solar if it hasn't already.

The general form of the logistic is

     y = f(x) = L / (1 + e^(-k*x))

where L is a scaling constant, and
k is a free parameter that affects the slope of the curve.

Notice that at x = 0, f(x) = 0.5 * L.

And we want g(x),

     g(x) = 1 - f(x).

We need to introduce more parameters here, as follows:

     x = cs - pu - ne

With the following interpretations:

cs = cost of solar PV power in cents per kWH, `solar-PV-cost` in the code and Interface slider.

pu = price of utility power in cents per kWH, `current-price` in the code and Interface slider.

Finally, ne is the neighborhood effect (a positive number, `neighborhood-effect` in the code and Interface slider), which serves to reduce the value of x, and hence increase the probability of adoption (as it increases).



## CREDITS AND REFERENCES

Chai, D.W.H., Adlakha, S., Low, S.H., De Martini, P., Chandy, K.M. Impact of residential PV adoption on retail electricity rates. (2013). Energy Policy 62, pp. 830-843. 

Bean, Patrick, Fuentes, Rolando, Kimbrough, Steven O., and Muaafa, Mohammed, Residential Solar PV Adoption model, version 1.0. (2015) File: _Residential Solar PV Adoption Model.nlogo_


## HOW TO CITE

If you mention this model in a publication, we ask that you include these citations for the model itself and for the NetLogo software:

* Bean, Patrick, Fuentes, Rolando, Kimbrough, Steven O., and Muaafa, Mohammed, Residential Solar PV Adoption model, version 1.0. (2015) File: _Residential Solar PV Adoption Model.nlogo_
* Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

## COPYRIGHT AND LICENSE

![CC BY-NC-SA 3.0](http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png)

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.

Commercial licenses are also available. To inquire about commercial licenses, please contact Uri Wilensky at uri@northwestern.edu.

This model was created as part of the project: CONNECTED MATHEMATICS: MAKING SENSE OF COMPLEX PHENOMENA THROUGH BUILDING OBJECT-BASED PARALLEL MODELS (OBPML).  The project gratefully acknowledges the support of the National Science Foundation (Applications of Advanced Technologies Program) -- grant numbers RED #9552950 and REC #9632612.

This model was converted to NetLogo as part of the projects: PARTICIPATORY SIMULATIONS: NETWORK-BASED DESIGN FOR SYSTEMS LEARNING IN CLASSROOMS and/or INTEGRATED SIMULATION AND MODELING ENVIRONMENT. The project gratefully acknowledges the support of the National Science Foundation (REPP & ROLE programs) -- grant numbers REC #9814682 and REC-0126227. Converted from StarLogoT to NetLogo, 2001.
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

sun
false
0
Circle -7500403 true true 75 75 150
Polygon -7500403 true true 300 150 240 120 240 180
Polygon -7500403 true true 150 0 120 60 180 60
Polygon -7500403 true true 150 300 120 240 180 240
Polygon -7500403 true true 0 150 60 120 60 180
Polygon -7500403 true true 60 195 105 240 45 255
Polygon -7500403 true true 60 105 105 60 45 45
Polygon -7500403 true true 195 60 240 105 255 45
Polygon -7500403 true true 240 195 195 240 255 255

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 5.1.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="experiment 1" repetitions="10" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks &gt;= count-years-simulated</exitCondition>
    <metric>count turtles with [has-solar? = true] / count turtles</metric>
    <metric>count highs with [has-solar? = true] / count highs</metric>
    <metric>count lows with [has-solar? = true] / count lows</metric>
    <steppedValueSet variable="current-price" first="10" step="2" last="20"/>
    <enumeratedValueSet variable="number-of-residences">
      <value value="2100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="solar-high">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="solar-low">
      <value value="-50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%-similar-wanted">
      <value value="7"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="count-years-simulated">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="neighborhood-effect">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="solar-PV-cost">
      <value value="16"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%-lows">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="k">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="L-scale">
      <value value="0.02"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%-highs">
      <value value="0.47"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Prob_big_solar_given_low">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Prob_big_solar_given_high">
      <value value="0.5"/>
    </enumeratedValueSet>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

@#$#@#$#@
0
@#$#@#$#@
