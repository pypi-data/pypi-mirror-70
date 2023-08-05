# corona-api
An asynchronous wrapper for the [NovelCOVID API](https://github.com/NovelCOVID/API) written in Python.

This is designed for bots using [discord.py](https://github.com/Rapptz/discord.py) but there is no discord-specific code so you are free to use this in any project as required. 

# Requirements
 - Python 3.5 or above
 - aiohttp (`python3 -m pip install -U aiohttp`)

# Installation
### Using pip (recommended)
 - `python3 -m pip install -U corona_api`

# Support
Get support for this on Discord, either on our [official server](https://takagisan.xyz/support) or the [NovelCOVID server](https://discord.gg/cEDxzfW).

# Optional parameters in methods
| Parameter      	| Supported methods                                                                                                                                                                                                                                 	| Accepted values                                                                                                                                                                                                                               	|
|----------------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| `yesterday`    	| - `all()`<br>- `get_country_data()`<br>- `get_country_list()`<br>- `get_all_countries()`<br>- `get_all_states()`<br>- `get_single_state()`<br>- `get_state_list()`<br>- `get_all_continents()`<br>- `get_single_continent()`                      	| - `True`<br>- `False`                                                                                                                                                                                                                         	|
| `two_days_ago` 	| - `all()`<br>- `get_country_data()`<br>- `get_country_list()`<br>- `get_all_countries()`<br>- `get_single_continent()`<br>- `get_all_continents()`                                                                                                	| - `True`<br>- `False`                                                                                                                                                                                                                         	|
| `sort`         	| - `get_all_countries()`<br>- `get_all_states()`<br>- `get_all_continents()`                                                                                                                                                                       	| - `'cases'`<br>- `'deaths'`<br>- `'recovered'`<br>- `'active'`<br>- `'tests'`<br>- `'critical'`<br>- `'deathsPerOneMillion'`<br>- `'testsPerOneMillion'`<br>- `'todayCases'`<br>- `'todayDeaths'`<br>- `'casesPerOneMillion'`<br>- `'active'` 	|
| `allow_none`   	| - `all()`<br>- `get_country_data()`<br>- `get_country_list()`<br>- `get_all_countries()`<br>- `get_all_continents()`<br>- `get_single_continent()`<br>- `get_single_state()`<br>- `get_state_list()`<br>- `get_all_states()`<br>- `gov_country()` 	| - `True`<br>- `False`                                                                                                                                                                                                                         	|

# Examples
The following examples cover the basic usage of the library and its various features. 
Note; many methods also support `yesterday=True`, `sort='sort method'` and `allow_none=True` kwargs to get data from the previous day or sorted by various parameters. Refer to the table above to find out which ones do and do not.

### Discord bot
There is an example cog for your Discord bot [here](https://github.com/apex2504/python-corona-api/blob/master/examples/discord_cog.py).

## Basic data
### Global data
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_all():
    data = await client.all() #get global data
    print(data.cases, data.deaths) #print the number of global cases and deaths

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_all())
```

## Data for a specific country
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_country():
    data = await client.get_country_data('UK') #get data for the UK today,
    print(data.cases, data.deaths) #print the number of cases and deaths for the UK

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_country())
```
 
## Data for more than one country
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_countries():
    data = await client.get_country_list('UK', 'USA', 'China') #get data for specified countries
    #to get data for every country supported, use:  get_all_countries()
    print(data) #prints a list of CountryStatistics

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_countries())
```
## US States
### Data for a specific state
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_state():
    data = await client.get_single_state('Ohio') #get data for Ohio today,
    print(data.cases, data.deaths) #print the number of cases and deaths for Ohio

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_state())
```
 
### Data for more than one state
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_states():
    data = await client.get_state_list('Ohio', 'California', 'Texas') #get data for specified states
    #to get data for every state supported, use:  get_all_states()
    print(data) #prints a list of StateStatistics

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_states())
```

## Historical statistics
### Historical data globally
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_history():
    data = await client.get_country_history('all', 'all') #get all the historical data for the world

    print(data.name, data.case_history[0].date, data.case_history[0].value) #print name (in this case 'Global'), the date of the first entry, and the number of cases for that date

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_history())
```

### Historical data for a country
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_history():
    data = await client.get_country_history('UK', 7) #get the past week of historical data for the UK

    print(data.name, data.case_history[0].date, data.case_history[0].value) #print name, the date of the first entry, and the number of cases for that date

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_history())
```

### Historical data for a province
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_history_province():
    data = await client.get_province_history('UK', 'Gibraltar', 7) #get the past week of historical data for Gibraltar, UK

    print(data.province, data.case_history[0].date, data.case_history[0].value) #print province name, the date of the first entry, and the number of cases for that date

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_history_province())
```

### Historical data for a county within a US state
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_county():
    data = await client.get_state_county_history('Ohio', 'Adams') #get all historical data for Adams, Ohio, USA

    print(data.name, data.province, data.case_history[0].date, data.case_history[0].value) #print state and county name, the date of the first entry, and the number of cases for that date

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_county())
```
## John Hopkins CSSE
### All data from the JHU CSSE
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_jhu():
    data = await client.get_jhu_csse_data() #get data for every province and country JHU supports

    print(data) #print a long list of JhuCsseStatistics

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_jhu())
```

### Data for a county within a US state
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_jhu_county():
    data = await client.get_jhu_county_data('Ohio', 'Adams') #get data for Adams, Ohio

    print(data.province_name, data.county_name, data.confirmed_cases) #print the state, county and case number

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_jhu_county())
```

### Data for every county in the USA
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_jhu_counties():
    data = await client.get_jhu_all_counties() 

    print(data) #print a long list of JhuCsseStatistics

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_jhu_counties())
```

## Continental data
### Data for every continent
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_conts():
    data = await client.get_all_continents() 
    first = data[0]

    print(first.name, first.cases,  first.deaths) #print some info for the first continent in the list

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_conts())
```

### Data for a single continent
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_one_cont():
    data = await client.get_single_continent('Europe') 

    print(data.name, data.cases,  data.deaths) #print some info for the specified continent

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_one_cont())
```

## New York Times
### USA data from NY Times 
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_nyt_us():
    data = await client.get_nyt_usa_data() 
    first = data[0]

    print(first.date, first.cases,  first.deaths) #print first piece of data

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_nyt_us())
```

### All USA state data from NY Times 
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_nyt_states():
    data = await client.get_nyt_all_states() 
    first = data[0]

    print(first.state, first.date,  first.cases) #print some data from the frst element

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_nyt_states())
```

### Data for a single state from NY Times
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_nyt_state():
    data = await client.get_nyt_single_state('Ohio')
    first = date[0]

    print(first.date, first.cases,  first.deaths) #print the first date, and case/death number

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_nyt_state())
```

### Every county from NY Times
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_counts():
    data = await client.get_nyt_all_counties() 
    first = data[0]

    print(first.date, first.cases,  first.deaths) #print part of the first piece of data

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_counts())
```

### Counties from NYT filtered by name
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_one_county():
    data = await client.get_nyt_single_county('Adams') 
    first = data[0]

    print(first.date, first.cases,  first.deaths) #print part of the first piece of data

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_one_county())
```

## Apple Mobility
### Every country supported by Apple Mobility Data
```python
import corona_api
import asyncio

client = corona_api.Client()

async def all_apples():
    data = await client.apple_all_countries()

    print(data) #print all supported countries

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(apples())
```

### Every subregion within a country for Apple Mobility
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_subregions():
    data = await client.apple_subregions('UK')

    print(data.subregions) #print all supported subregions within the country

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_subregions())
```

### Apple's Mobility data for a subregion
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_one_sub():
    data = await client.apple_mobility_data('UK', 'London')
    first = data.statistics[0]

    print(first.date, first.name, first.driving) #print some data about the first result

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_one_sub())
```

## Governmental data
### All countries supported by the API for government data
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_gov_countries():
    data = await client.gov_all_countries()

    print(data) #print the supported countries

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_gov_countries())
```

### Get the data from a country's governmental data
```python
import corona_api
import asyncio

client = corona_api.Client()

async def get_country_gov():
    data = await client.gov_country('UK')

    print(data) #probably will return a large amount of dict data.

    await client.request_client.close() #close the ClientSession

asyncio.get_event_loop().run_until_complete(get_country_gov())
```

# Note
Due to the fact that each country's governmental/official statistics website is different, it is not feasible to create a standardised class for the data. However, if you interpret the data received from the API, it should be relatively simple to work with the given information.
