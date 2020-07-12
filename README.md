# What is SimplexConsilium

SimplexConsilium is project management tool that aims at simplicity. It is designed for command line freaks and alike.  
There are three different boards: TODO, DOING, DONE. Those boards are based in [Kanban](https://en.wikipedia.org/wiki/Kanban), instead
of having tasks in each board, there are goals. In [Gantt Chart](https://en.wikipedia.org/wiki/Gantt_chart) oriented projects, usually there are
goals and purposes to guide the chart itself. In SimplexConsilium there are just goals with descriptions. There are NO tasks, nor time labels on the Goals.  

For instance: A goal along with a purpose for a *Gantt Chart* would be something like:  
**Goal 1:** Reduce storage costs by 20% over 2 years,
    - without diminishing the quality of service
    - ensuring the same functionality
    - Taking into account an increase in storage needs of 20% per year  
**Goal 2** ...  
...  
**Goal n**  

**Purpose of goals:** Reduces the overall costs of the company.  

In SimplexConsilium the purpose of goals would not exist. Because SimplexConsilium was created to manage projects done for fun. Hence they are NOT a priority. There should be no time labels as well, like in the previous goal: *"...over 2 years"*.  

As it was already mentioned, tasks are also excluded. Giving an example, one might have the following goal:  
**Goal X:** Pimp my pi.  
**Goal X description:** Change the external part of my raspberry pi to metal black and add an external fan.  

As you can see, there are NO task in this Goal, meaning it is not specified how the goal is going to be accomplished, only **what** is going to be accomplished is specified. This approach frees the user from having purposes for goals, and tasks for each goal.
In short, every Goal description should **answer ONLY one question: "What is it?"**  

Goals are accomplished by Individuals, and each Individual has a name.  

This conception is of course not optimal for big companies or big projects, but the code can very easily be adapted. For instance in the class Goal, it would be rather straight forward to add a limit date for the Goal to be accomplished, but this project managing approach DOES not have those kind of requirements.  

# How to use SimplexConsilium  
It is possible to use SimplexConsilium in your code, or directly as a command line tool.  
If you use it as a command line tool, you will have the following options:

```  
usage: SimplexConsiliumCMD.py [-h] [-sc ] [-sd ] [-sl ]

    Simple project manager made to aim simplicity, for command line freaks and alike.
    Github: https://github.com/OblackatO/SimplexConsilium
    Author: Pedro Gomes (blackat)
    Email: OblackatO@yandex.com
    

optional arguments:
  -h, --help            show this help message and exit
  -sc  , --simplexcreate  
                        Creates a new project: -sc <project_name>
  -sd  , --simplexdelete  
                        Deletes a project: -sd <project_name>
  -sl  , --simplexload  
                        Loads an existing project: -sl <project_name>

License:GPL-3.0

```  

After creating a project you can load it with *-sl*. The information about your projects is saved in cwd, using json format. A fresh created project would look like this:  
``` 
[1].Show project
[2].Add Individual(s)
[3].Create Goal(s)
[4].Add Individual(s) to Goal
[5].Move Goal forward.
[6].Move Goal downward.
[7].Show Goal
[8].Remove Goal
[9].Save changes
[e].Exit
Input:
```

Let us suppose my input is 1. The following output will show up:  
``` 
+------------------+------------------+------------------+
|       TODO       |      DOING       |       DONE       |
+------------------+------------------+------------------+
| Project empty :( | Project empty :( | Project empty :( |
+------------------+------------------+------------------+

[1].Show project
[2].Add Individual(s)
[3].Create Goal(s)
[4].Add Individual(s) to Goal
[5].Move Goal forward.
[6].Move Goal downward.
[7].Show Goal
[8].Remove Goal
[9].Save changes
[e].Exit
Input:
``` 

After creating some goals with input 3, adding some individuals to the project with input 2, and adding some individuals to some created goals with input 4, the output of the project could be something like:  
``` 
+--------------------------------+--------------------------------------+------+
|              TODO              |                DOING                 | DONE |
+--------------------------------+--------------------------------------+------+
|      [Name]--[ID]:Sleep earlie |      [Name]--[ID]:goal1 this is the  |      |
| r -- 6175    [Description]:I m | title -- 8838    [Description]:This  |      |
| ust go to bed earlier tonight  | is the title of goal1, and I am pret |      |
|          [Individuals]:        | ty sure that the table is out.    [I |      |
|                                |          ndividuals]:/Pedro          |      |
+--------------------------------+--------------------------------------+------+
|      [Name]--[ID]:goal3 -- 271 |      [Name]--[ID]:Raise all saleries |      |
| 4    [Description]:Create an a |   more than twenty per cent -- 7966  |      |
| ccount in leafpad after midter |    [Description]:I have to make sure |      |
|  ms exams.    [Individuals]:   |  that everyone in this company gets  |      |
|                                | a higher salary than before.    [Ind |      |
|                                |   ividuals]:/Pedro/Esteves/Ricardo   |      |
+--------------------------------+--------------------------------------+------+
|      [Name]--[ID]:Drink more t |                                      |      |
| ea -- 395    [Description]:I h |                                      |      |
| ave to start drinking more hot |                                      |      |
|  tea, to avoid being ill. I th |                                      |      |
| ink that it might actually hel |                                      |      |
|    p me.    [Individuals]:     |                                      |      |
+--------------------------------+--------------------------------------+------+

[1].Show project
[2].Add Individual(s)
[3].Create Goal(s)
[4].Add Individual(s) to Goal
[5].Move Goal forward.
[6].Move Goal downward.
[7].Show Goal
[8].Remove Goal
[9].Save changes
[e].Exit
Input:

``` 
Please note that these Goals are random, and they do not have a meaning.  
In order to save changes just [e].Exit, or if you want to save your changes and continue working, use [9].Save changes.  

If you would like to integrate SimplexConsilium in your code, please see the [documentation](SimplexConsilium_Docs.pdf)
For instance, to create a project and add some inviduals, you can simply do:  
```
from SimplexConsilium.Individual import Individual
from SimplexConsilium.SimplexConsilium import SimplexConsilium

individual_x = Individual("Matthew")
individual_y = Individual("Someone")

project = SimplexConsilium("ProjectX")
project.addindividual(individual_x)
project.addindividual(individual_y)
```
To create a Goal, and add it the project above:
```
from SimplexConsilium.Goal import Goal

goal = Goal("Goal1")
goal.description = "This is description will be done just for the documentation."
goal.createhash()
```

**VERY important:** Did you notice the function: *goal.createhash()*? This function will create an unique hash to your goal based on the name and description it has. Because In every python session a random seed is established to generate a hash, the ID of a Goal is fixed in its creation process. If this wasn't done, when you exit the project and come back again and python calculates the hash with the **EXACTLY** same input, the output is going to be different. That is the reason why *createhash()* is called. It makes sure that only one hash is generated and saved when a Goal is created.  

# Setup
Create a virtualenv*(optional)*  
**Install beautifultable:**     
```pip3 install beautifultable```    
**clone this repository and cd into it:**  
```git clone https://github.com/OblackatO/SimplexConsilium```  
```cd SimplexConsilium```  
**Start using the CMD tool and have fun**  
```python3 SimplexConsiliumCMD.py --help```   

# Questions
**Why do you have doc strings in the code, and do not provide officially documentation on readthedocs?**  
Initially I wanted to do so. It was planned to provide documentation. After generating the docs with sphinx-quickstart and sphinx-apidoc, it was hard to make the documentation properly appear with readthedocs. Meaning, the README.md is linked to the docs and that works, but all the classes are ignored and only their names are shown, not the doc strings. This does not happen at all if the "index" file in the build dir of the docs is opened with a browser(offline). After searching for an **enormous amount of hours** and trying to understand what is going on, I decided to move on. Hence there will be no docs, and I will not try again linking them in readthedocs.  
As a **workaround** I converted the page that I am able to see offline to a PDF file. It is possible to have a nice [overview](SimplexConsilium_Docs.pdf) over the documentation. Still, not as nice as it would be in readthedocs.  

**Why not PyPi?**  
PyPi without readthedocs, is just not complete.  

**What about security and Synchronization?**  
It is possible to encrypt the data of a project at rest, ask the user for a password and decrypt it again using AES_CBC, or another password derivation encryption algorithm. The thing is, it is rather trivial just to encrypt the folder of the project. For instance if your project is in a usb drive, just use LUKS encryption, and the data is encrypted while resting.  
When it comes to synchronization, simply synch your project folder to the cloud of your choice, to be able to access it in other devices.  
Encryption feautures might be added in the future, synchronization feautures will not be added for sure. 

# Requirements 
beautifultable  
python3.5 =<

# Remarks  
As already stated SimplexConsilium was created to manage my personal projects, hence it lacks several feautures needed for a real world environment. The point of SimplexConsilium is exactly to **avoid** having too many unecessary feautures that are not needed if you are working alone, or in a project for fun with friends.  

SimplexConsilium will be maintained.

# Suggestions 
If you have suggestions or remarks, please contact me directly at: (OblackatO@yandex.com)    
**PGP FingerPrint:** EC56C26526290AE9402216C64EF2D094664FA2B8  
I will accept pull requests or suggestions that do not alter the conception behind SimplexConsilium.  
If you would like to add more feautures to SimplexConsilium that go beyond its simplicity aim, please do a fork and have fun.    



