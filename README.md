# ReadME

The LUNA project is an interactive app developed by Group G ...

## Installation

Clone the repo

Create a virtual environment on your local machine
```bash
virtualenv env
```
Navigate into Scripts/activate to activate the virtual envrionment and install the required pip modules

```bash
pip install -r requirements.txt
```

To run the program run
```bash
python manage.py runserver
```

## Testing and Linting

Note for developers. We want to ensure that good testing and convention is kept. In order to accomplish we want to.
>Provide good unit tests for developers to use in the future

>Clear documentation over functions and their usage

Below you can see an example template for a testing 

>Test ID | Description | Expected | Passed

>001     | I can vist xxx | /xxx.html | Pass

For linting please use black within the root directory 
```bash
python -m black .
```
Where necessary npm may also be used for linting
```bash
npm run lint
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

