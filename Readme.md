# Cut Sheet Creator


### Introduction
**What is cut Sheet Creator?** -
Cut Sheet Creator is a powerful script that is designed to take AKIPS reports
from existing network infrastructure hardware (Network Switches),and output the
commands that would be required to configure new switches based off the HPE
platform. In this process there is also an integrated system that removes all
unused ports and converts the Text Based Vlans from the AKIPS report into
numerical code based off a master Vlan List.

**How it works** -
Cut Sheet Creator is designed to be efficient and deployable as a cron job.
With that in mind all the user is required to do is drop the AKIPS report(s) they
want to process into the Input Folder, and run `python loop.py` from the main
directory, and within minutes will be presented with Not only a terminal output
of the updated ports and Vlans, but also get a text file with the table for each switch,
and also a separate text file in the commands folder of output that contains the
commands that you can cut and paste onto a HPE switch during configuration. The
inspiration for this design was the fact that the previous excel tool that was
used for this process didn't have a simple way to be modified to allow for ports
to be kept on the proper side of the device, as cable management started to be an
issue.

### Usage:
1. **Download From GitHub** - Using `git Clone https://github.com/Hopalonger/CutSheetCreator.git`
2. **Installation** - This tool requires a few Dependencies to operate
these can be installed by running these commands `pip install tabulate`, `pip install beautifulsoup4`,`pip install selenium`. Once these Dependencies have been intalled, open
`loop.py` in a text editor and update the file directory with the proper paths to the Main Directory, the Input Directory, the Output Directory, and the Completed Directory. 

3. **Importing Reports** - This system is designed to Use specific AKIPS reports,
the report that we are going to use is going to to be gotten from using the
unused interfaces menu and selecting a device. Once the device has been selceted
click the csv button on the top to download it as a csv file.
Once this file has been downloaded I recommend renaming it as the device name
just to keep track of it. Then move the file into the Input folder of the Program

4. **Running the Program** - to run the program it is very straight forward,
all it takes is running `python loop.py -u ONID-USERNAME -p ONID-PASSWORD` and it will find all of the files and process them into the reports. Make Sure to replace `ONID-USERNAME` and `ONID-PASSWORD` with your own username and password. 


5. **Understanding output** - Understanding the output of the program can be a
bit much, it was designed to be as simple as possible, but still can be alot
The termal and main ouput file will display a table that looks like this:

| Device       | Interface ID   |      Speed | Status   | State   | Last Change      | Desc              | Vlan Name          |   Vlan ID | New Port   |
|--------------|----------------|------------|----------|---------|------------------|-------------------|--------------------|-----------|------------|
| ILLC-270-fsw | Gi2/25         | 1000000000 | free     | down    | 2019-08-13 16:44 | 175/D.13          | CN-IRS_W           |      1113 | 1/0/25     |
| ILLC-270-fsw | Gi2/26         |  100000000 | used     | up      | 2018-07-02 8:11  | 175/D.14          | CN-IRS_W           |      1113 | 1/0/26     |
| ILLC-270-fsw | Gi2/27         |  100000000 | used     | up      | 2021-09-03 8:07  | 175/D.15          | CN-IRS_W           |      1113 | 1/0/27     |
| ILLC-270-fsw | Gi2/28         | 1000000000 | free     | down    | 2020-10-28 12:35 | 175/D.16          | CN-IRS_W           |      1113 | 1/0/28     |
| ILLC-270-fsw | Gi2/29         |  100000000 | used     | up      | 2022-02-25 13:30 | 175/D.17          | CN-IRS_W           |      1113 | 1/0/29     |
| ILLC-270-fsw | Gi2/30         | 1000000000 | used     | down    | 2022-03-02 12:10 | 175/D.18          | CN-IRS_W           |      1113 | 1/0/30     |
| ILLC-270-fsw | Gi2/31         |  100000000 | used     | up      | 2022-01-20 13:57 | 175/D.19          | CN-IRS_W           |      1113 | 1/0/31     |
| ILLC-270-fsw | Gi2/32         |  100000000 | used     | up      | 2022-04-29 9:44  | 175/D.20          | CN-IRS_W           |      1113 | 1/0/32     |
| ILLC-270-fsw | Gi2/33         |  100000000 | used     | up      | 2021-08-17 9:50  | 181/D.37          | CN-IRS_W           |      1113 | 1/0/33     |
| ILLC-270-fsw | Gi2/34         | 1000000000 | used     | up      | 2022-05-20 8:06  | 181/D.38          | CN-IRS_W           |      1113 | 1/0/34     |
| ILLC-270-fsw | Gi2/35         |  100000000 | used     | up      | 2015-12-01 11:26 | 181 D.55          | CN-IRS_W           |      1113 | 1/0/35     |
| ILLC-270-fsw | Gi2/37         |  100000000 | used     | up      | 2018-07-12 8:34  | 181/D.41          | CN-IRS_W           |      1113 | 1/0/36     |
| ILLC-270-fsw | Gi2/38         | 1000000000 | used     | up      | 2022-05-27 6:59  | 181/D.42          | CN-IRS_W           |      1113 | 1/0/37     |
| ILLC-270-fsw | Gi2/39         |  100000000 | used     | up      | 2021-09-07 14:15 | 181/D.43          | CN-IRS_W           |      1113 | 1/0/38     |
| ILLC-270-fsw | Gi2/40         |  100000000 | used     | up      | 2021-04-14 17:32 | 181/D.44          | CN-Prntr_S         |      1122 | 1/0/39     |
| ILLC-270-fsw | Gi2/41         | 1000000000 | used     | up      | 2022-05-27 8:02  | 182/D.67          | CN-IRS_W           |      1113 | 1/0/40     |
| ILLC-270-fsw | Gi2/42         |  100000000 | used     | up      | 2021-08-31 13:56 | 182/D.68          | CN-IRS_W           |      1113 | 1/0/41     |
| ILLC-270-fsw | Gi2/43         |  100000000 | used     | up      | 2018-07-02 8:22  | 180/D.71          | CN-IRS_W           |      1113 | 1/0/42     |
| ILLC-270-fsw | Gi2/45         | 1000000000 | used     | up      | 2022-05-18 23:51 | 250/D.181         | SCF-Labs_H         |      1160 | 1/0/43     |



This table is well name and formatted but shows the install report information
and also the new information after processing. This will mostly be used when patching over ports,
and only shows the ports that need to be patched over. The commands folder
Contains the HPE commands, which can be just copied and pasted, no need for Explanation
as HPE is another section of hardware.

### Examples:
There are example files that are loaded into the input folder, and its respective outputs are in the output folder, although when the program runs your cutsheets once processed will be moved into the Completed folder.


### Troubleshooting:
If you get an error that states that the chromedriver that is being used is out of date or the wrong version of the chromedriver. Please go to `https://chromedriver.chromium.org/downloads` and download the version of the chromedriver that is requested by the error. Once downloaded please move `chromedriver.exe` to the Main Directory of cutsheet creator, or install it as a path variable and delete the old version. 

### Features:
- Custom Cutoff Date Selection
- OPENL2M Vlan Query
- Automatic Port Configuration Command Generation
- Automatic Vlan Initilzation Command Generation
- Specify Port Types Based off Vlan
- Automatic File management
- Automatic Cable Management

### Todo: 
- 
- Add in ability to Catch and Deal with WAP's and the W.XXX Series of ports
- Add in checking for the password being wrong for the OPENL2M Login
- Build The managed mode into the GUI
- Refactor Code
