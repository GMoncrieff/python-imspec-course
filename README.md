# python-imspec-course
_A course on using Python to analyse imaging spectroscopy data at scale_

This is a series of notebooks and lectures aimed at teaching you the basics of working with multidimensional spatial data in Python. We will work towards acquiring the skills to analyse data from imaging spectrometers such as [EMIT](https://earth.jpl.nasa.gov/emit/) and [AVIRIS](https://aviris.jpl.nasa.gov/). Our aim is to prepare collaborators involved in the [Biodiversity of the Cape (BioSCape)](https://www.bioscape.io/) campaign for the large volumes of data that the campaign will produce. We will start by introducing the basics of Python, then we will build on this by diving into more advanced data stuctures and geospatial analyses. Then we will look at details about how to make our analyses scale to very large multidimensional datasets. Finally we will analyse an imaging spectroscopy data cube using all the tool and techniques we have learnt in the preceding weeks.

The plan currently is:

- Prep session - (at home):     Python basics
- Session 1 - 17 July 2023 1-3pm SAST, UCT:  Geospatial Python & Scalable geospatial analysis in Python
- Session 2 - 31 July 2023 1-3pm SAST, UCT:  Imaging spectroscopy data at scale

## Who is this course for?

This course is designed for those who have some background in programming and/or knowledge of geospatial data. You should have experience with one of the following: R, ENVI, QGIS, ArcGIS, GEE. I will not talk about foundational geospatial concepts such as geo datatypes and projections. I will assume you know this. I will also assume you know some basic programming. You do not need to have experience with Python. There is a intro notebook that will give you the necessary background. But if you already know some Python you can skip it.  

This is not a course on imaging spectroscopy. It is a general course on handling large, high dimensional spatial data in Python. I will skip over the details and nuances of imaging spectroscopy data and dive straight into analyses. A great course on the theory and analysis of imaging spectroscopy data in Python is [David Thompson's Imaging Spectroscopy Tutorial Materials on github](https://github.com/davidraythompson/istutor). The [EMIT data resources](https://github.com/nasa/EMIT-Data-Resources) repo also contains lots of very handy code for getting started that is applicable beyond just EMIT.

## Content

| Week | Topic                                  | Notebook                               | Video            |
| ---- | -------------------------------------- | -------------------------------------- | ---------------- |
| 0    | Python basics                          | [0_Basics.ipynb](0_Basics.ipynb)       |                  |
| 1    | Scalable geospatial analysis in Python | [1_Geopython.ipynb](1_Geopython.ipynb) | [link](https://ub.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=8c60f4b4-9c4e-4803-adbe-b04200e9b869)    |
| 2    | Imaging spectroscopy data at scale     | _coming soonish_                       | _coming soonish_ |

## Setup 
### 1. Get a python package manager
If you already have a python environment manager installed, you can simply create a new environment from the [environment.yml](environment.yml).  

If what I just said makes no sense to you, you need to install a python package and environment manager. I recommend [mamba](https://mamba.readthedocs.io/en/latest/index.html). You can download the installer for mamba [here](https://github.com/conda-forge/miniforge#mambaforge). Once downloaded, if you are using windows you can just double-click the installer. On mac/linux you will need to execute the downloaded file in your terminal. This will look like  

`bash Mambaforge-something-something.sh`  

replace something-something with the actual filename from your download.  

Once installed, you might need to close and reopen your terminal before the `mamba` command becomes available

### 2. Clone the course repo
Copy the content of this repo  

`git clone https://github.com/GMoncrieff/python-imspec-course.git`  

and cd into the folder you just cloned

`cd python-imspec-course`

### 3. Install the python packages we need  
This involves creating the python environment and installing all the packages we need into that environment  

`mamba env create --name ispython --file=environment.yml`    

Now activate the environment  

`mamba activate ispython`  

and launch jupyter by typing   

`jupyter-lab` 

### 4. Other places to learn

If you think this course is lame, or want to learn about similar things from a different perspective (using the same tools) have a look at these courses:

[The Carpentries Geospatial Python lesson by Ryan Avery](https://carpentries-incubator.github.io/geospatial-python/).   
The course focuses on accessing and analysing multiband traditional Earth Observation data   

[An Introduction to Earth and Environmental Data Science](https://earth-env-data-science.github.io/intro.html).  
This course focuses on analysing earth science data more broadly.

## Contribute

We really welcome any contributions, additions, or corrections that you might wish to add. Please see the [contributing guide](CONTRIBUTE.md)
