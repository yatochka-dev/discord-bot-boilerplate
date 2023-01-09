# Pydantic models

Pydantic is a Python library that is used to validate and parse data. It is designed to be easy to use, efficient, and extendable, and is often used in the development of web APIs and other applications that deal with a lot of structured data.

Pydantic models are classes that are used to define the structure of data that you want to validate and parse. These models use class attributes to define the fields of the data, and Pydantic provides a set of validators that you can use to ensure that the data meets certain criteria. For example, you can use validators to ensure that a field is required, or that it is of a certain type or format.

Once you have defined your model, you can use it to parse and validate data by creating an instance of the model and passing in the data as keyword arguments. Pydantic will automatically validate the data and return an instance of the model with the parsed data. You can then access the parsed data using the attributes of the model instance.

Here's an example of how you might define a simple Pydantic model:

```python
from pydantic import BaseModel

class UserDANT(BaseModel):
    name: str
    age: int
    email: str
```

This model defines a User class with three fields: `name`, `age`, and `email`. The type annotations indicate that the `name` field is a string, the `age` field is an integer, and the `email` field is a string.

You can then use this model to parse and validate data like this:

```python
data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
user = UserDANT(**data)
print(user.name)  # prints "John"
print(user.age)  # prints 30
print(user.email)  # prints "john@example.com"
```

Pydantic provides many more features and options for defining and validating data, such as support for nested models, custom validators, and more. You can learn more about Pydantic by reading the documentation at https://pydantic-docs.helpmanual.io/.

## In this project 

1. Make sure that you're creating pydantic models only in **app.dantic** directory 
2. For naming convention purposes, add **`DANT`** to the end of each class(model) name(e.g. **UserDANT**).
3. Don't create all models in one file, create a separate file for each group of models.