# python-imspec-course
_A course on using Python to analyse imaging spectroscopy data_

This series of notebooks and lectures aimed at teaching you the basics of working with multidimensional spatial data in Python. We will work towards acquiring the skills to analyse data from imaging spectrometers such as EMIT and AVIRIS. We will start by introducing the basic of Python, then we will build on this by diving into more advanced data stuctures, geospatial analyses. Then we will look at some details about how to make our analyses scale to very large multidimensional datasets. Finally we will analyse an imaging spectroscopy data cube using all the tool and techniques we have learnt in the preceding weeks.

The plan currently is:

- Prep session - (at home):     Python basics
- Session 1 - 17 July 2023 1-3pm SAST, UCT:  Geospatial Python & Scalable geospatial analysis in Python
- Session 2 - 31 July 2023 1-3pm SAST, UCT:  Imaging spectroscopy data at scale

## Who is this course for?

This course is desinged for those who have some background in programming and/or knowledege pf geospatail data. You should have experience with one or the following: R, ENVI, QGIS, ArcGIS, GEE. I will not talk about foundational geposptail conceprts such as geo dtatypes and projectins. I will assume you know this. I will also assume you know some basis programming. You do not need to have experience with Python. There is a intro notebook that will give you the nessasary background. But if you do know some Python you can skip it.

This is not a course on imaging spectroscopy. It is a general course on hangling large, high dimensional spatial data in Python. I will skip over the details and nuanaces of imaging spectroscopy data and dive straight into analyses. A great course on the theory and analysis of imaging spectroscopy data in Python is [David Thompson's Imaging Spectroscopy Tutorial Materials on github](https://github.com/davidraythompson/istutor). The [EMIT data resources](https://github.com/nasa/EMIT-Data-Resources) repo also contains lots of very handy code for getting started that is applicable beyond just EMIT.

## Setup 
### Get a python package manager
If you already have a python environment manager installed, you can jjsimply create a new environment from the [environment.yml](environment.yml).  

If what I just said makes no sense to you, you need to intall a python package and environment manager. I recommend [mamba](https://mamba.readthedocs.io/en/latest/index.html). You can download the intaller for mamba [here](https://github.com/conda-forge/miniforge#mambaforge). Once downloaded, if you are usig windows you can just double-click the intsaller. On mac/linux you will need to execute the downloaded file your terminal. This will look like  

`bash Mambaforge-something-something.sh`  

### clone the course repo
Copy the content of this repo  

`git clone https://github.com/GMoncrieff/python-imspec-course.git`  

### install the python packages we need  
This involves creating the python environmental and installing all the packages we need into that environment  

`mamba env create --name ispython --file=environment.yml`    

Now activate the environment  

`mamba activate ispython`  

and launch jupyter by typing   
 
`jupyter-lab`  


## Content

| Week | Topic                                  | Notebook                               | Video            |
| ---- | -------------------------------------- | -------------------------------------- | ---------------- |
| 0    | Python basics                          | [0_Basics.ipynb](0_Basics.ipynb)       |                  |
| 1    | Scalable geospatial analysis in Python | [1_Geopython.ipynb](1_Geopython.ipynb) | _coming soon_    |
| 2    | Imaging spectroscopy data at scale     | _coming soonish_                       | _coming soonish_ |

## Contribute

We really welcome any contributions, additions, or corrections that you might wish to add. Please see the [contriburting guide](CONTRIBUITE.md)
