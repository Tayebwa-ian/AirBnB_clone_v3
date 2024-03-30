# 0x02. AirBnB clone - MySQL
***

This is the first step towards building your first full web application: the AirBnB clone. This first step is very important because you will use what you build during this project with all other following projects: HTML/CSS templating, database storage, API, front-end integration…

**Each task is linked and will help you to:**  

put in place a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of your future instances  
create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file  
create all classes used for AirBnB (User, State, City, Place…) that inherit from BaseModel  
create the first abstracted storage engine of the project: File storage.  
create all unittests to validate all our classes and storage engine  

## What’s a command interpreter?
---

A shell like interface but limited to a specific use-case. In our case, we want to be able to manage the objects of our project:

Create a new object (ex: a new User or a new Place)  
Retrieve an object from a file, a database etc…  
Do operations on objects (count, compute stats, etc…)  
Update attributes of an object  
Destroy an object  

## Installation
---

1. Clone This Repo git clone [from](https://github.com/Tayebwa-ian/AirBnB_clone_v2)
2. Access AirBnb directory: cd AirBnB_clone
3. Install pycodestyle: `pip install pycodestyle`
4. Run hbnb(interactively): ./console and enter command
5. Run hbnb(non-interactively): echo "<command>" | ./console.py

## Available Command:
---

* quit and EOF to exit the program
* help for every Command
* create
* show
* destroy
* all
* update
* count

## Command interpreter Usage:
---

```
(hbnb) all Vser 
** class doesn't exist ** 
(hbnb) all 
["[User] (337c109d-e787-4b7b-a3f0-88f66ba9953f) {'id': '337c109d-e787-4b7b-a3f0-88f66ba9953f', 'created_at': datetime.datetime(2024, 1, 12, 21, 32, 18, 490270), 'updated_at': datetime.datetime(2024, 1, 12, 21, 32, 18, 490372)}", "[User] (70338bed-f448-4af4-968b-0cbfd091f03a) {'id': '70338bed-f448-4af4-968b-0cbfd091f03a', 'created_at': datetime.datetime(2024, 1, 12, 23, 1, 6, 575487), 'updated_at': datetime.datetime(2024, 1, 12, 23, 1, 6, 575510)}", "[Place] (7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c) {'id': '7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c', 'created_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886310), 'updated_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886327)}", "[User] (51841181-58dd-4f8c-93ef-b8e0102cb1cc) {'id': '51841181-58dd-4f8c-93ef-b8e0102cb1cc', 'created_at': datetime.datetime(2024, 1, 12, 23, 26, 1, 995499), 'updated_at': datetime.datetime(2024, 1, 12, 23, 26, 1, 995519)}"] 
(hbnb) show Place 7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c 
[Place] (7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c) {'id': '7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c', 'created_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886310), 'updated_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886327)} 
(hbnb) all Place 
["[Place] (7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c) {'id': '7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c', 'created_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886310), 'updated_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886327)}"] 
(hbnb) show Place 
** instance id missing ** 
(hbnb) show 
** class name missing ** 
(hbnb) create City 
a78c8527-cfad-4eda-a02d-d43b63a338e0 
(hbnb) update City a78c8527-cfad-4eda-a02d-d43b63a338e0 name Arua 
(hbnb) update City a78c8527-cfad-4eda-a02d-d43b63a338e0 name 
** value missing ** 
(hbnb) update City a78c8527-cfad-4eda-a02d-d43b63a338e0 
** attribute name missing ** 
(hbnb) update City 
** instance id missing ** 
(hbnb) destroy City a78c8527-cfad-4eda-a02d-d43b63a338e0  
(hbnb) User.all()
["[User] (337c109d-e787-4b7b-a3f0-88f66ba9953f) {'id': '337c109d-e787-4b7b-a3f0-88f66ba9953f', 'created_at': datetime.datetime(2024, 1, 12, 21, 32, 18, 490270), 'updated_at': datetime.datetime(2024, 1, 12, 21, 32, 18, 490372)}"]
(hbnb) Place.all()
["[Place] (7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c) {'id': '7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c', 'created_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886310), 'updated_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886327)}"]
(hbnb) Place.show(7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c)
[Place] (7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c) {'id': '7643d25f-18c3-4f47-b9ec-d3f3b64f2f6c', 'created_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886310), 'updated_at': datetime.datetime(2024, 1, 12, 23, 3, 55, 886327)}
(hbnb) User.update("337c109d-e787-4b7b-a3f0-88f66ba9953f", {'first_name': "Samuel", "age": 29})
(hbnb) User.count()
1
(hbnb) create User
c72caf8e-5018-4e04-a253-72694d8b8850
(hbnb) User.count()
2
(hbnb) User.update("c72caf8e-5018-4e04-a253-72694d8b8850", "first_name", "Muhumuza")
(hbnb) count User
2
(hbnb) quit
```
