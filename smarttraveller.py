import bs4 as bs
import pandas as pd
import geopandas as gp
import requests

website = 'https://www.smartraveller.gov.au/destinations'

r = requests.get(website)

soup = bs.BeautifulSoup(r.content, features="html.parser")

##tables = soup.find_all('table')
##print(tables)

categories_soup = soup.find_all('td', attrs = {'headers': 'view-field-overall-advice-level-table-column'})
countries_soup = soup.find_all('a', attrs = {'hreflang': "en"})

#print(categories_soup)
#print(countries_soup)

advice_categories = []
countries = []

for c in categories_soup:
    c = str(c)
    loc1 = c.find('>')
    loc2 = c.find('</td>')
    status = c[loc1+1:loc2]
    status = status.strip()
    advice_categories.append(status)

for c in countries_soup:
    c = str(c)
    loc1 = c.find('>')
    loc2 = c.find('</a>')
    country = c[loc1+1:loc2]
    countries.append(country)
    
##print(countries)
##print(advice_categories)

shapefile_world = 'C:/Users/Azzla/Downloads/Countries/World.shp'

all_countries = gp.read_file(shapefile_world)

nations_in_shp = all_countries['name']
iso_code = all_countries['iso3']
regions = all_countries['region']
continents = all_countries['continent']

st_iso = []
st_country = []
st_advice = []

string = 'The following countries with their row id are in the shapefile'
for j in range(len(nations_in_shp)):
    line = str(j) + '. ' + str(nations_in_shp[j])
    string += '\n'
    string += line

print(string)

for i in range(len(countries)):
    ctry = countries[i]
    adv = advice_categories[i]
    in_shapefile = False
    for j in range(len(nations_in_shp)):
        if ctry == nations_in_shp[j]:
            st_iso.append(iso_code[j])
            st_country.append(ctry)
            st_advice.append(adv)
            in_shapefile = True
    if in_shapefile == False:
        print(str(ctry) + ' is not in the shapefile. Could it be there?.')               
        yn = input('Please pick the row number corresponding to the right country from above. Press N or n for not in list. If you need to see the list displayed again press A')
        if (yn == 'A' or yn == 'a'):
            print(string)
            yn = input('Please pick the row number corresponding to the right country from above. Press N or n for not in list. If you need to see the list displayed again press A')
        elif (yn == 'N' or yn == 'n'):
            a_country = input('Is it a country? Y for yes, any other key for no.')
            if a_country == 'Y' or a_country == 'y':                              
                iso = input('Enter the three letter abbreviation for the country.')
                st_iso.append(iso)
                st_country.append(ctry)
                st_advice.append(adv)
        else:
            try:
                yn = int(yn)
                correct = False
                if yn >= 0 and yn < len(nations_in_shp):
                    st_iso.append(iso_code[yn])
                    st_country.append(ctry)
                    st_advice.append(adv)
                    correct = True
                else:
                    while correct == False:
                        print('ERROR. Value entered was out of range, try again.')
                        yn = input('Please pick the row number corresponding to the right country from above. Press N or n for not in list. If you need to see the list displayed again press A')
                        if yn >= 0 and yn < len(nations_in_shp):
                            correct = True
                        else:
                            correct = False
                        
            except:
                correct = False
                while correct == False:
                    print('Your answer is not numeric or in range, try again.')
                    yn = input('Please pick the row number corresponding to the right country from above. Press N or n for not in list. If you need to see the list displayed again press A')
                    try:
                        yn = int(yn)
                        if yn >= 0 and yn < len(nations_in_shp):
                            correct = True
                        else:
                            correct = False
                    except:
                        correct = False
                                            

df_dict = {}
df_dict['iso_code'] = st_iso
df_dict['country'] = st_country
df_dict['advice'] = st_advice


#df_st = pd.DataFrame{df_dict}
df_st = pd.DataFrame(df_dict)

df_st.to_csv('C:/Users/Azzla/Downloads/Countries/SmartTraveller_May.csv')
print('Complete!')

                        
                
            
            
            



##<td class="views-field views-field-title" headers="view-title-table-column"><a href="/destinations/americas/ecuador" hreflang="en">Ecuador</a> </td>
##<td class="views-field views-field-field-region" headers="view-field-region-table-column"><a href="/destinations/Americas">Americas</a> </td>
##<td class="views-field views-field-field-overall-advice-level" headers="view-field-overall-advice-level-table-column">Exercise a high degree of caution          </td>
##<td class="views-field views-field-field-updated" headers="view-field-updated-table-column"><time class="datetime" datetime="2023-05-19T12:00:00Z">19 May 2023</time>
##</td>
