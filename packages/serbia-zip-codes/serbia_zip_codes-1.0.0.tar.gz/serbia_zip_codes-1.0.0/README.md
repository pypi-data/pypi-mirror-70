# Serbia zip codes

Easy access to Serbia zip codes. You can search zip code by city, or city by zip code.

## Installation

```
pip install serbia-zip-codes
```

## Usage

```python
import serbia_zip_codes
```

Search city by city:

```python
>>> result = serbia_zip_codes.find_by_city("Loznica")
>>> print(result)
[{'city': 'Loznica', 'zip_code': '15300'}]
>>> print(result[0]['zip_code'])
15300
```

Search city by zip code:

```python
>>> result = serbia_zip_codes.find_by_zip("15300")
>>> print(result)
[{'city': 'Loznica', 'zip_code': '15300'}]
>>> print(result[0]['city'])
Loznica
```

Multiple results example:

```python
>>> from pprint import pprint
>>> import serbia_zip_codes
>>> result = serbia_zip_codes.find_by_city("beograd")
>>> pprint(result)
[{'city': 'Beograd', 'zip_code': '11000'},
 {'city': 'Beograd Voždovac', 'zip_code': '11010'},
 {'city': 'Beograd Čukarica', 'zip_code': '11030'},
 {'city': 'Beograd Zvezdara', 'zip_code': '11050'},
 {'city': 'Beograd Palilula', 'zip_code': '11060'},
 {'city': 'Beograd Zemun', 'zip_code': '11080'},
 {'city': 'Beograd Rakovica', 'zip_code': '11090'}]
```

Get all:

```python
>>> result = serbia_zip_codes.get_all()
>>> pprint(result)
[{'city': 'Beograd', 'zip_code': '11000'},
 {'city': 'Beograd Voždovac', 'zip_code': '11010'},
 {'city': 'Beograd Čukarica', 'zip_code': '11030'},
 {'city': 'Beograd Zvezdara', 'zip_code': '11050'},
 {'city': 'Beograd Palilula', 'zip_code': '11060'},
 {'city': 'Novi Beograd', 'zip_code': '11070'},
 {'city': 'Beograd Zemun', 'zip_code': '11080'},
 {'city': 'Beograd Rakovica', 'zip_code': '11090'},
 {'city': 'Kaluđerica', 'zip_code': '11130'},
 {'city': 'Rušanj', 'zip_code': '11194'},
 {'city': 'Borča', 'zip_code': '11211'},
 {'city': 'Ovča', 'zip_code': '11212'},
 {'city': 'Padinska Skela', 'zip_code': '11213'},
 {'city': 'Beli Potok', 'zip_code': '11223'},
 {'city': 'Vrčin', 'zip_code': '11224'},
 {'city': 'Zuce', 'zip_code': '11225'},
 {'city': 'Pinosava', 'zip_code': '11226'},
 {'city': 'Ripanj', 'zip_code': '11232'},
 {'city': 'Ralja', 'zip_code': '11233'},
 {'city': 'Mali Požarevac', 'zip_code': '11235'},
 {'city': 'Ostružnica', 'zip_code': '11251'},
 {'city': 'Sremčica', 'zip_code': '11253'},
 {'city': 'Umka', 'zip_code': '11260'},
 {'city': 'Mala Moštanica', 'zip_code': '11261'},
 {'city': 'Velika Mostanica', 'zip_code': '11262'},
 {'city': 'Surčin', 'zip_code': '11271'},
 {'city': 'Dobanovci', 'zip_code': '11272'},
...
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
