# AirBnB Clone - The Console

The console is the first segment of the AirBnB project at Holberton School, which collectively covers fundamental concepts of higher level programming. The goal of the AirBnB project is to eventually deploy a simple copy of the AirBnB Website (HBnB). The command interpreter created in this segment manages objects for the AirBnB (HBnB) website.

## Functionalities of this command interpreter:
* Create a new object (e.g., a new User or a new Place)
* Retrieve an object from a file, a database, etc.
* Perform operations on objects (e.g., count, compute stats, etc.)
* Update attributes of an object
* Destroy an object

## Table of Contents
* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Examples of Use](#examples-of-use)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Environment
This project is interpreted/tested on Ubuntu 14.04 LTS using Python 3 (version 3.4.3).

## Installation
* Clone this repository: `git clone "https://github.com/alexaorrico/AirBnB_clone.git"`
* Access the AirBnB directory: `cd AirBnB_clone`
* Run the console (interactively): `./console` and enter commands
* Run the console (non-interactively): `echo "<command>" | ./console.py`

## File Descriptions
* [console.py](console.py) - The console contains the entry point of the command interpreter. 
  List of commands this console currently supports:
  - `EOF` - exits console 
  - `quit` - exits console
  - `<emptyline>` - overwrites default emptyline method and does nothing
  - `create` - Creates a new instance of `BaseModel`, saves it (to the JSON file), and prints the id
  - `destroy` - Deletes an instance based on the class name and id (saves the change into the JSON file)
  - `show` - Prints the string representation of an instance based on the class name and id
  - `all` - Prints all string representations of all instances based or not on the class name
  - `update` - Updates an instance based on the class name and id by adding or updating attribute (saves the change into the JSON file)

* `/models` directory contains classes used for this project:
  - [base_model.py](/models/base_model.py) - The BaseModel class from which future classes will be derived
    + `def __init__(self, *args, **kwargs)`: Initialization of the base model
    + `def __str__(self)`: String representation of the BaseModel class
    + `def save(self)`: Updates the attribute `updated_at` with the current datetime
    + `def to_dict(self)`: Returns a dictionary containing all keys/values of the instance
  - Classes inherited from Base Model:
    + [amenity.py](/models/amenity.py)
    + [city.py](/models/city.py)
    + [place.py](/models/place.py)
    + [review.py](/models/review.py)
    + [state.py](/models/state.py)
    + [user.py](/models/user.py)

* `/models/engine` directory contains File Storage class that handles JSON serialization and deserialization:
  - [file_storage.py](/models/engine/file_storage.py) - Serializes instances to a JSON file & deserializes back to instances
    + `def all(self)`: Returns the dictionary __objects
    + `def new(self, obj)`: Sets in __objects the obj with key <obj class name>.id
    + `def save(self)`: Serializes __objects to the JSON file (path: __file_path)
    + ` def reload(self)`: Deserializes the JSON file to __objects

* `/tests` directory contains all unit test cases for this project:
  - [/test_models/test_base_model.py](/tests/test_models/test_base_model.py) - Contains the TestBaseModel and TestBaseModelDocs classes
    + TestBaseModelDocs class:
      - `def setUpClass(cls)`: Set up for the doc tests
      - `def test_pep8_conformance_base_model(self)`: Test that models/base_model.py conforms to PEP8
      - `def test_pep8_conformance_test_base_model(self)`: Test that tests/test_models/test_base_model.py conforms to PEP8
      - `def test_bm_module_docstring(self)`: Test for the base_model.py module docstring
      - `def test_bm_class_docstring(self)`: Test for the BaseModel class docstring
      - `def test_bm_func_docstrings(self)`: Test for the presence of docstrings in BaseModel methods
    + TestBaseModel class:
      - `def test_is_base_model(self)`: Test that the instantiation of a BaseModel works
      - `def test_created_at_instantiation(self)`: Test created_at is a public instance attribute of type datetime
      - `def test_updated_at_instantiation(self)`: Test updated_at is a public instance attribute of type datetime
      - `def test_diff_datetime_objs(self)`: Test that two BaseModel instances have different datetime objects

## Examples of Use

