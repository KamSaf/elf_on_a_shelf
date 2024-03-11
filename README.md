# Overview

Elf management system for Santa Claus. It's a CRUD app created with Flask framework as a final assignment in the subject of Specialized Tool Software. 

<p align="center"><img src="https://github.com/KamSaf/elf_on_a_shelf/assets/116653905/bdbebecc-3c34-4d84-bddb-c6fe524d351d" width="70%" height="70%"/></p>



# Technologies and tools used:

- Python 3.10,
- Flask 3.0.0,
- Flask-SQLAlchemy 3.1.1,
- Bootstrap5 5.3.0,
- jQuery 3.6.0,



# Features:

- Adding/editing/deleting Elves,
- Adding/editing/deleting/marking as delivered Packages,
- Adding/editing/deleting Elves Holidays,



# How to run (no Docker):

1. Create virtual environment and activate it:

        virtualenv venv
        cd venv/bin
        source activate

2. Install dependencies by running:

        pip install -r requirements.txt


3. Run application with command when in app directory:

        python app.py



# How to run with Docker (pull from DockerHub):

1. Pull image from DockerHub:

        docker pull kamsaf42/elf_manager:latest


2. Run image with docker:

        docker run kamsaf42/elf_manager



# How to run with Docker (build image):

1. Build image when in /app directory with command:

        docker build -t elf_manager .


2. Run image with docker:

        docker run -d -p 5000:5000 elf_manager



# Deployment is done through DigitalOcean service (currently not active):

    https://octopus-app-hg7dl.ondigitalocean.app/



# DockerHub repository:

        https://hub.docker.com/r/kamsaf42/elf_manager



# GIFs:


**Add new elf:**
<p align="center"><img src="https://github.com/KamSaf/elf_on_a_shelf/assets/116653905/bdbebecc-3c34-4d84-bddb-c6fe524d351d" width="70%" height="70%"/></p>


**Add new package:**
<p align="center"><img src="https://github.com/KamSaf/elf_on_a_shelf/assets/116653905/a75274f3-b08b-414d-a133-e2a2524e8caf" width="70%" height="70%"/></p>


**Add new holiday:**
<p align="center"><img src="https://github.com/KamSaf/elf_on_a_shelf/assets/116653905/b82f4077-3d42-4bf1-8e82-2701659d9ba1" width="70%" height="70%"/></p>
