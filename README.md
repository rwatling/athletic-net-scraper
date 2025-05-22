This program scrapes publicaly avilable Athletic.net web pages associated with a
set of teams in order to generate theoretical heat sheets for the set of teams.
To specify a set of teams, create a CSV file with `<team_id>,<team_name>` as
shown in the files included.

Additionally, the year of interest will need to be specified and the number of
athletes from each team. Note that the script assumes the `n` athletes follow in
succession from the event header on Athletic.net, so if large `n` is specified
it may pull in other event results into the wrong table. The events presented
here are from MSHSL Outdoor Track (Minnesota).

The information is publicly available on Athletic.net and MSHSL results. I claim
no responsibility for the availability or accuracy of content. Abuse of this
script or the information in the script will prompt me to remove or restrict
access to this respository.

* Usage `python scraper.py <team_id_csv> <year> <top n on team>`
* Example `python scraper.py section.in 2025 3`
* Install the dependencies below with `pip install -r requirements.txt`
* Dependencies
    * python 3.12.9
    * pip 23.3.2
    * pandas 2.2.3
    * playwright 1.52.0
