How to run:

1. Create virtual environment and activate it:

        virtualenv venv
        cd venv/bin
        source activate

2. Install dependencies by running:

        pip install -r requirements.txt


3. Run application with command when in app directory:

        flask --app app.py run


-------------------------------------------------------

How to run with Docker (pull from DockerHub):

1. Pull image from DockerHub:

        docker pull kamsaf42/elf_manager:latest


2. Run image with docker:

        docker run kamsaf42/elf_manager

-------------------------------------------------------

How to run with Docker (build image):

1. Build image when in /app directory with command:

        docker build -t elf_manager .


2. Run image with docker:

        docker run -d -p 5000:5000 elf_manager


-------------------------------------------------------


Deployment is done through DigitalOcean service:

    <link>