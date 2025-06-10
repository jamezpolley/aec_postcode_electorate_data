A mapping of Australian postcodes to federal electorates according to the Australian Electoral Commission.

* The `redistributed` column of the data is the electorate which will be used at the next federal electorate for the given locality. For states where there was no redistribution the column will be blank.9s
* The `other` columne is the `Other Locality(s)` data from the AEC site.
* To get a consolidated list of electorate/postcode mappings for the *next* election:

    ```
    select distinct state, suburb, postcode, coalesce(nullif(redistributedElectorate,""), electorate) as electorate from data
    ```

* The list of postcodes is sourced indirectly from the [G-NAF](https://data.gov.au/dataset/ds-ga-074edff7-fd26-4ff5-87e4-0108e71afe43/details?q=g-naf), by way of [openaddresses.io](https://batch.openaddresses.io/data). Download the au/countrywide (addresses - country) file in geojson format. Then:
    ```
    gunzip au_countrywide-addresses-country.geojson.gz
    jq -r '.properties.postcode' au_countrywide-addresses-country.geojson | sort -u > postcodes
    ```
    (Note: you'll need [jq](https://stedolan.github.io/jq/) to process the geojson)
    then remove the first (blank) line.

Pull requests welcome.

Note that the scraper adds to the database so if for any reason a postcode is removed then there will be an old record that doesn't get updated. To fix this simply
delete the database before a run.

This is a scraper that runs on [Morph](https://morph.io). To get started [see the documentation](https://morph.io/documentation)
